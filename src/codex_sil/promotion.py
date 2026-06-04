"""Promotion and review operations triggered from the local WebUI."""

from __future__ import annotations

import shutil
import re
from pathlib import Path

from .db import connect, init_db
from .paths import backups_dir
from .scanner import now_stamp


def review_candidate(root: Path, candidate_id: int, status: str, note: str | None = None, rewrite_text: str | None = None) -> None:
    init_db(root)
    with connect(root) as conn:
        conn.execute("update candidates set status=?, updated_at=current_timestamp where id=?", (status, candidate_id))
        conn.execute(
            "insert into reviews(candidate_id, status, note, rewrite_text) values(?, ?, ?, ?)",
            (candidate_id, status, note, rewrite_text),
        )
        conn.execute("insert into audit_log(action, target, detail) values('review_candidate', ?, ?)", (str(candidate_id), status))


def archive_candidate(root: Path, candidate_id: int, note: str | None = None) -> None:
    review_candidate(root, candidate_id, "archived", note=note)


def skill_slug(title: str, candidate_id: int) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", title.casefold()).strip("-")
    if not base:
        base = "learned-from-codex"
    return f"{base[:48].strip('-')}-{candidate_id}"


def promote_to_user_memory(root: Path, candidate_id: int, user_memory_path: Path | None = None) -> dict[str, str]:
    init_db(root)
    user_memory = user_memory_path or root / "memories" / "USER.md"
    user_memory.parent.mkdir(parents=True, exist_ok=True)
    with connect(root) as conn:
        row = conn.execute("select rewrite_suggestion, text from candidates where id=?", (candidate_id,)).fetchone()
        if row is None:
            raise ValueError(f"candidate not found: {candidate_id}")
        text = str(row["rewrite_suggestion"] or row["text"]).strip()
    backup_path = ""
    if user_memory.exists():
        backup = backups_dir(root) / f"USER.backup-{now_stamp()}.md"
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(user_memory, backup)
        backup_path = str(backup)
    existing = user_memory.read_text(encoding="utf-8") if user_memory.exists() else "# USER.md\n"
    if text not in existing:
        user_memory.write_text(existing.rstrip() + "\n\n- " + text + "\n", encoding="utf-8")
    with connect(root) as conn:
        conn.execute("update candidates set status='promoted', updated_at=current_timestamp where id=?", (candidate_id,))
        conn.execute(
            "insert into promotions(candidate_id, target_type, target_path, backup_path, status, detail) values(?, 'USER.md', ?, ?, 'ok', ?)",
            (candidate_id, str(user_memory), backup_path, text),
        )
        conn.execute("insert into audit_log(action, target, detail) values('promote_user_memory', ?, ?)", (str(user_memory), text))
    return {"target_path": str(user_memory), "backup_path": backup_path, "status": "ok"}


def promote_to_skill(root: Path, candidate_id: int, skills_root: Path | None = None) -> dict[str, str]:
    init_db(root)
    target_root = skills_root or Path.home() / ".agents" / "skills"
    with connect(root) as conn:
        row = conn.execute("select title, rewrite_suggestion, text from candidates where id=?", (candidate_id,)).fetchone()
        if row is None:
            raise ValueError(f"candidate not found: {candidate_id}")
        title = str(row["title"] or "Learned From Codex")
        body = str(row["rewrite_suggestion"] or row["text"]).strip()
    slug = skill_slug(title, candidate_id)
    target = target_root / slug / "SKILL.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    backup_path = ""
    if target.exists():
        backup = backups_dir(root) / f"SKILL.backup-{now_stamp()}.md"
        shutil.copy2(target, backup)
        backup_path = str(backup)
    content = "\n".join(
        [
            "---",
            f"name: {slug}",
            f"description: {title}",
            "---",
            "",
            f"# {title}",
            "",
            body,
            "",
        ]
    )
    target.write_text(content, encoding="utf-8")
    with connect(root) as conn:
        conn.execute("update candidates set status='promoted', updated_at=current_timestamp where id=?", (candidate_id,))
        conn.execute(
            "insert into promotions(candidate_id, target_type, target_path, backup_path, status, detail) values(?, 'skill', ?, ?, 'ok', ?)",
            (candidate_id, str(target), backup_path, body),
        )
        conn.execute("insert into audit_log(action, target, detail) values('promote_skill', ?, ?)", (str(target), body))
    return {"target_path": str(target), "backup_path": backup_path, "status": "ok"}


def promote_to_skill_patch(root: Path, candidate_id: int, patch_path: Path | None = None) -> dict[str, str]:
    init_db(root)
    target = patch_path or root / "self-improving-loop" / "exports" / f"skill-patch-{candidate_id}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    with connect(root) as conn:
        row = conn.execute("select title, rewrite_suggestion, text from candidates where id=?", (candidate_id,)).fetchone()
        if row is None:
            raise ValueError(f"candidate not found: {candidate_id}")
        title = str(row["title"] or "Skill Patch Candidate")
        body = str(row["rewrite_suggestion"] or row["text"]).strip()
    backup_path = ""
    if target.exists():
        backup = backups_dir(root) / f"skill-patch.backup-{now_stamp()}.md"
        shutil.copy2(target, backup)
        backup_path = str(backup)
    target.write_text(f"# {title}\n\n{body}\n", encoding="utf-8")
    with connect(root) as conn:
        conn.execute("update candidates set status='promoted', updated_at=current_timestamp where id=?", (candidate_id,))
        conn.execute(
            "insert into promotions(candidate_id, target_type, target_path, backup_path, status, detail) values(?, 'skill_patch', ?, ?, 'ok', ?)",
            (candidate_id, str(target), backup_path, body),
        )
        conn.execute("insert into audit_log(action, target, detail) values('promote_skill_patch', ?, ?)", (str(target), body))
    return {"target_path": str(target), "backup_path": backup_path, "status": "ok"}
