"""Session scanning, rebuild, and SQLite persistence."""

from __future__ import annotations

import hashlib
import json
import shutil
import re
from datetime import datetime
from pathlib import Path

from .db import connect, init_db
from .codex_runner import extract_with_codex
from .fallback_extractor import ExtractedCandidate, extract_candidates, normalize
from .paths import backups_dir, db_path


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def iter_session_files(root: Path) -> list[Path]:
    sessions = root.expanduser() / "sessions"
    if not sessions.exists():
        return []
    files = [*sessions.rglob("*.jsonl"), *sessions.rglob("*.json")]
    return sorted({path.resolve() for path in files if path.is_file()}, key=lambda path: str(path))


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def content_text(content: object) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
            elif isinstance(item, str):
                parts.append(item)
        return "\n".join(parts)
    return ""


def strip_user_preamble(text: str) -> str:
    stripped = text.strip()
    if "</INSTRUCTIONS>" in stripped:
        stripped = stripped.split("</INSTRUCTIONS>", 1)[1].strip()
    stripped = re.sub(r"(?s)<environment_context>.*?</environment_context>", "", stripped).strip()
    return stripped


def message_from_payload(payload: dict[str, object]) -> tuple[str, str] | None:
    payload_type = payload.get("type")
    role = str(payload.get("role") or "")
    if not payload_type and role in {"user", "assistant"}:
        text = content_text(payload.get("content") or payload.get("message") or payload.get("text"))
        if role == "user":
            text = strip_user_preamble(text)
        return role, text.strip()
    if payload_type == "message":
        if role not in {"user", "assistant"}:
            return None
        text = content_text(payload.get("content"))
        if role == "user":
            text = strip_user_preamble(text)
        return role, text.strip()
    if payload_type in {"user_message", "agent_message"}:
        role = "user" if payload_type == "user_message" else "assistant"
        text = str(payload.get("message") or "").strip()
        return role, strip_user_preamble(text) if role == "user" else text
    return None


def read_session_text(path: Path) -> str:
    rows: list[str] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            rows.append(line)
            continue
        if isinstance(payload, dict):
            if payload.get("type") in {"response_item", "event_msg"} and isinstance(payload.get("payload"), dict):
                message = message_from_payload(payload["payload"])
                if message:
                    role, text = message
                    if text:
                        rows.append(f"{role}: {text}")
                continue
            message = message_from_payload(payload)
            if message:
                role, text = message
                if text:
                    rows.append(f"{role}: {text}")
        else:
            rows.append(str(payload))
    return "\n".join(rows)


def start_run(root: Path, kind: str, detail: str | None = None) -> int:
    with connect(root) as conn:
        cur = conn.execute("insert into runs(kind, status, detail) values(?, 'running', ?)", (kind, detail))
        return int(cur.lastrowid)


def finish_run(root: Path, run_id: int, status: str, detail: str | None = None) -> None:
    with connect(root) as conn:
        conn.execute(
            "update runs set status=?, finished_at=current_timestamp, detail=coalesce(?, detail) where id=?",
            (status, detail, run_id),
        )


def add_step(root: Path, run_id: int, name: str, status: str, detail: str | None = None) -> None:
    with connect(root) as conn:
        conn.execute(
            "insert into run_steps(run_id, name, status, finished_at, detail) values(?, ?, ?, current_timestamp, ?)",
            (run_id, name, status, detail),
        )


def upsert_session(root: Path, path: Path) -> tuple[int, bool]:
    resolved = path.resolve()
    stat = resolved.stat()
    sha = file_hash(resolved)
    sessions_root = (root / "sessions").resolve()
    try:
        rel = str(resolved.relative_to(sessions_root))
    except ValueError:
        rel = str(resolved)
    with connect(root) as conn:
        existing = conn.execute("select id, sha256, status from sessions where path=?", (str(resolved),)).fetchone()
        if existing:
            changed = str(existing["sha256"]) != sha
            conn.execute(
                "update sessions set rel_path=?, mtime=?, size=?, sha256=?, status=case when ? then 'new' else status end where id=?",
                (rel, int(stat.st_mtime), stat.st_size, sha, 1 if changed else 0, int(existing["id"])),
            )
            return int(existing["id"]), changed or str(existing["status"]) != "processed"
        cur = conn.execute(
            "insert into sessions(path, rel_path, mtime, size, sha256, status) values(?, ?, ?, ?, ?, 'new')",
            (str(resolved), rel, int(stat.st_mtime), stat.st_size, sha),
        )
        return int(cur.lastrowid), True


def persist_candidate(root: Path, session_id: int, candidate: ExtractedCandidate, evidence: str) -> int:
    normalized = normalize(candidate.text)
    with connect(root) as conn:
        conn.execute(
            """
            insert into candidates(type, title, text, normalized, destination, rewrite_suggestion, safety, confidence, extractor)
            values(?, ?, ?, ?, ?, ?, ?, ?, ?)
            on conflict(type, normalized) do update set
              updated_at=current_timestamp,
              confidence=max(confidence, excluded.confidence)
            """,
            (
                candidate.type,
                candidate.title,
                candidate.text,
                normalized,
                candidate.destination,
                candidate.rewrite_suggestion,
                candidate.safety,
                candidate.confidence,
                candidate.extractor,
            ),
        )
        row = conn.execute("select id from candidates where type=? and normalized=?", (candidate.type, normalized)).fetchone()
        candidate_id = int(row["id"])
        conn.execute(
            "insert or ignore into candidate_sources(candidate_id, session_id, evidence) values(?, ?, ?)",
            (candidate_id, session_id, evidence[:1000]),
        )
        fingerprint = hashlib.sha256(f"{candidate.type}:{normalized}".encode("utf-8")).hexdigest()
        conn.execute(
            "insert or ignore into candidate_fingerprints(fingerprint, candidate_id) values(?, ?)",
            (fingerprint, candidate_id),
        )
        return candidate_id


def process_session(root: Path, run_id: int, path: Path) -> int:
    session_id, should_process = upsert_session(root, path)
    if not should_process:
        add_step(root, run_id, "session_skipped", "ok", str(path))
        return 0
    text = read_session_text(path)
    codex_candidates = extract_with_codex(text, root)
    candidates = codex_candidates if codex_candidates else extract_candidates(text)
    for candidate in candidates:
        persist_candidate(root, session_id, candidate, text[:1000])
    with connect(root) as conn:
        conn.execute("update sessions set status='processed', last_processed_at=current_timestamp where id=?", (session_id,))
    add_step(root, run_id, "session_processed", "ok", f"{path} candidates={len(candidates)}")
    return len(candidates)


def backup_db(root: Path) -> Path | None:
    source = db_path(root)
    if not source.exists():
        return None
    target = backups_dir(root) / f"self-improving-loop.backup-{now_stamp()}.sqlite"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return target


def scan_once(root: Path, kind: str = "scan") -> dict[str, int]:
    init_db(root)
    run_id = start_run(root, kind)
    sessions = iter_session_files(root)
    processed = 0
    candidates = 0
    try:
        for path in sessions:
            before = candidates
            candidates += process_session(root, run_id, path)
            if candidates != before:
                processed += 1
        finish_run(root, run_id, "ok", f"sessions={len(sessions)} candidates={candidates}")
        return {"run_id": run_id, "sessions": len(sessions), "processed": processed, "candidates": candidates}
    except Exception as exc:
        finish_run(root, run_id, "failed", str(exc))
        raise


def rebuild(root: Path, backup: bool = False) -> dict[str, int | str | None]:
    backup_path = backup_db(root) if backup else None
    database = db_path(root)
    if database.exists():
        database.unlink()
    result = scan_once(root, "rebuild")
    return {**result, "backup": str(backup_path) if backup_path else None}
