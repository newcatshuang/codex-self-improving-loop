"""Session scanning, rebuild, and SQLite persistence."""

from __future__ import annotations

import hashlib
import json
import shutil
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .db import connect, init_db
from .codex_runner import extract_with_codex
from .fallback_extractor import ExtractedCandidate, extract_candidates, normalize
from .paths import backups_dir, db_path


SKILL_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_-]*(?::[a-z][a-z0-9_-]*)?$", re.IGNORECASE)
USER_EXPLICIT_SKILL_PATTERN = re.compile(r"(?<![\w$])\$([A-Za-z][A-Za-z0-9_-]*(?::[A-Za-z][A-Za-z0-9_-]*)?)")
ASSISTANT_DECLARED_SKILL_PATTERNS = (
    re.compile(r"\bUsing\s+`([^`]+)`", re.IGNORECASE),
    re.compile(r"\bI(?:'ll| will)\s+use\s+`([^`]+)`", re.IGNORECASE),
    re.compile(r"我(?:会|将|准备用|会先|将会)?(?:使用|用)\s*`([^`]+)`"),
    re.compile(r"使用\s*`([^`]+)`\s*(?:skill|技能)?", re.IGNORECASE),
)
SKILL_SPLIT_PATTERN = re.compile(r"\s*(?:/|、|，|,|\band\b|和)\s*", re.IGNORECASE)
IGNORED_DOLLAR_NAMES = {
    "home",
    "codex_home",
    "path",
    "pwd",
    "tmp",
    "temp",
    "user",
    "username",
    "userprofile",
}
SOURCE_RANK = {"assistant_declared": 1, "user_explicit": 2}
SECRET_VALUE_PATTERN = re.compile(
    r"(?i)(api[_-]?key|token|secret|password|passwd)\s*[:=]\s*['\"]?[^'\"\s]+"
)
SKILL_CONTEXT_PATTERN = re.compile(r"(?i)\bskill\b|技能|superpowers")


@dataclass(frozen=True)
class SkillUsageEvent:
    skill_name: str
    source: str
    confidence: float
    evidence: str


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


def iter_session_messages(path: Path) -> list[tuple[str, str]]:
    messages: list[tuple[str, str]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            messages.append(("text", line))
            continue
        if isinstance(payload, dict):
            if payload.get("type") in {"response_item", "event_msg"} and isinstance(payload.get("payload"), dict):
                message = message_from_payload(payload["payload"])
                if message:
                    role, text = message
                    if text:
                        messages.append((role, text))
                continue
            message = message_from_payload(payload)
            if message:
                role, text = message
                if text:
                    messages.append((role, text))
        else:
            messages.append(("text", str(payload)))
    return messages


def messages_to_text(messages: list[tuple[str, str]]) -> str:
    rows: list[str] = []
    for role, text in messages:
        if role in {"user", "assistant"}:
            rows.append(f"{role}: {text}")
        else:
            rows.append(text)
    return "\n".join(rows)


def read_session_text(path: Path) -> str:
    return messages_to_text(iter_session_messages(path))


def normalize_skill_name(name: str) -> str | None:
    normalized = name.strip().strip("`'\"()[]{}<>:;,.，。；：").casefold()
    if not normalized or normalized in IGNORED_DOLLAR_NAMES:
        return None
    if not SKILL_NAME_PATTERN.fullmatch(normalized):
        return None
    return normalized


def split_skill_names(raw: str) -> list[str]:
    skills: list[str] = []
    seen: set[str] = set()
    for part in SKILL_SPLIT_PATTERN.split(raw.strip()):
        skill = normalize_skill_name(part)
        if skill and skill not in seen:
            seen.add(skill)
            skills.append(skill)
    return skills


def is_likely_skill_declaration_skill(skill: str, evidence: str) -> bool:
    if SKILL_CONTEXT_PATTERN.search(evidence):
        return True
    return "-" in skill or ":" in skill


def is_likely_user_explicit_skill(skill: str, text: str, start: int, end: int) -> bool:
    if "-" in skill or ":" in skill:
        return True
    suffix = text[end : end + 1]
    if suffix in {"=", ".", "[", "("}:
        return False
    if start <= len(text) - len(text.lstrip()) + 1:
        return True
    prefix = text[max(0, start - 24) : start]
    return bool(re.search(r"(?i)(?:use|using|activate|invoke|call|skill|使用|调用|启用|激活|用)\s*$", prefix))


def redact_detail(text: str) -> str:
    compact = " ".join(text.split())
    return SECRET_VALUE_PATTERN.sub(lambda match: f"{match.group(1)}=[REDACTED]", compact)[:240]


def extract_skill_usage_events(messages: list[tuple[str, str]]) -> list[SkillUsageEvent]:
    by_skill: dict[str, SkillUsageEvent] = {}
    for role, text in messages:
        if role == "user":
            for match in USER_EXPLICIT_SKILL_PATTERN.finditer(text):
                skill = normalize_skill_name(match.group(1))
                if not skill or not is_likely_user_explicit_skill(skill, text, match.start(), match.end()):
                    continue
                by_skill[skill] = SkillUsageEvent(skill, "user_explicit", 1.0, match.group(0))
            continue
        if role != "assistant":
            continue
        for pattern in ASSISTANT_DECLARED_SKILL_PATTERNS:
            for match in pattern.finditer(text):
                for skill in split_skill_names(match.group(1)):
                    if not is_likely_skill_declaration_skill(skill, match.group(0)):
                        continue
                    event = SkillUsageEvent(skill, "assistant_declared", 0.85, match.group(0))
                    existing = by_skill.get(skill)
                    if not existing or SOURCE_RANK[event.source] > SOURCE_RANK[existing.source]:
                        by_skill[skill] = event
    return sorted(by_skill.values(), key=lambda event: event.skill_name)


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


def persist_skill_usage(root: Path, session_id: int, event: SkillUsageEvent) -> int:
    detail = (
        f"session_id={session_id};source={event.source};confidence={event.confidence:.2f};"
        f"evidence={redact_detail(event.evidence)}"
    )
    with connect(root) as conn:
        existing = conn.execute(
            "select id, detail from skill_usage where skill_name=? and detail like ?",
            (event.skill_name, f"session_id={session_id};%"),
        ).fetchone()
        if existing:
            existing_detail = str(existing["detail"] or "")
            if "source=assistant_declared" in existing_detail and event.source == "user_explicit":
                conn.execute(
                    "update skill_usage set status='success', used_at=current_timestamp, detail=? where id=?",
                    (detail, int(existing["id"])),
                )
            return int(existing["id"])
        cur = conn.execute(
            "insert into skill_usage(skill_name, status, detail) values(?, 'success', ?)",
            (event.skill_name, detail),
        )
        return int(cur.lastrowid)


def process_session(root: Path, run_id: int, path: Path) -> int:
    session_id, should_process = upsert_session(root, path)
    if not should_process:
        add_step(root, run_id, "session_skipped", "ok", str(path))
        return 0
    messages = iter_session_messages(path)
    text = messages_to_text(messages)
    skill_usage_events = extract_skill_usage_events(messages)
    for event in skill_usage_events:
        persist_skill_usage(root, session_id, event)
    codex_candidates = extract_with_codex(text, root)
    candidates = codex_candidates if codex_candidates else extract_candidates(text)
    for candidate in candidates:
        persist_candidate(root, session_id, candidate, text[:1000])
    with connect(root) as conn:
        conn.execute("update sessions set status='processed', last_processed_at=current_timestamp where id=?", (session_id,))
    add_step(root, run_id, "session_processed", "ok", f"{path} candidates={len(candidates)} skill_usage={len(skill_usage_events)}")
    return len(candidates)


def backup_db(root: Path) -> Path | None:
    source = db_path(root)
    if not source.exists():
        return None
    target = backups_dir(root) / f"self-improving-loop.backup-{now_stamp()}.sqlite"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return target


def reset_db_for_rebuild(root: Path, keep_run_id: int | None = None) -> None:
    init_db(root)
    tables = (
        "candidate_sources",
        "candidate_fingerprints",
        "scan_results",
        "reviews",
        "promotions",
        "skill_usage",
        "skills",
        "schedules",
        "audit_log",
        "run_steps",
        "runs",
        "candidates",
        "sessions",
    )
    with connect(root) as conn:
        conn.execute("pragma foreign_keys = off")
        try:
            for table in tables:
                if table == "runs" and keep_run_id is not None:
                    conn.execute("delete from runs where id<>?", (keep_run_id,))
                else:
                    conn.execute(f"delete from {table}")
            placeholders = ", ".join("?" for _ in tables)
            conn.execute(f"delete from sqlite_sequence where name in ({placeholders})", tables)
        finally:
            conn.execute("pragma foreign_keys = on")


def scan_into_run(root: Path, run_id: int, sessions: list[Path]) -> dict[str, int]:
    processed = 0
    candidates = 0
    for path in sessions:
        before = candidates
        candidates += process_session(root, run_id, path)
        if candidates != before:
            processed += 1
    return {"run_id": run_id, "sessions": len(sessions), "processed": processed, "candidates": candidates}


def scan_once(root: Path, kind: str = "scan") -> dict[str, int]:
    init_db(root)
    run_id = start_run(root, kind)
    sessions = iter_session_files(root)
    try:
        result = scan_into_run(root, run_id, sessions)
        finish_run(root, run_id, "ok", f"sessions={result['sessions']} candidates={result['candidates']}")
        return result
    except Exception as exc:
        finish_run(root, run_id, "failed", str(exc))
        raise


def rebuild(root: Path, backup: bool = False) -> dict[str, int | str | None]:
    backup_path = backup_db(root) if backup else None
    reset_db_for_rebuild(root)
    result = scan_once(root, "rebuild")
    return {**result, "backup": str(backup_path) if backup_path else None}
