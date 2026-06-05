"""Promotion and review operations triggered from the local WebUI."""

from __future__ import annotations

import shutil
import re
import difflib
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


def _candidate_text(root: Path, candidate_id: int) -> tuple[str, str]:
    with connect(root) as conn:
        row = conn.execute("select title, rewrite_suggestion, text from candidates where id=?", (candidate_id,)).fetchone()
        if row is None:
            raise ValueError(f"candidate not found: {candidate_id}")
        title = str(row["title"] or "Learned From Codex")
        text = str(row["rewrite_suggestion"] or row["text"]).strip()
        return title, text


def _append_bullet(existing: str, text: str) -> str:
    if text in existing:
        return existing
    return existing.rstrip() + "\n\n- " + text + "\n"


def _project_agents_content(existing: str, text: str) -> str:
    if text in existing:
        return existing
    section = "## Project Learned Facts"
    if section not in existing:
        existing = existing.rstrip() + f"\n\n{section}\n"
    return existing.rstrip() + "\n\n- " + text + "\n"


def _skill_content(slug: str, title: str, body: str) -> str:
    return "\n".join(
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


def _unified_diff(before: str, after: str, target: Path) -> str:
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=f"before/{target.name}",
            tofile=f"after/{target.name}",
            lineterm="",
        )
    )


def promotion_preview(
    root: Path,
    candidate_id: int,
    target: str,
    user_memory_path: Path | None = None,
    agents_path: Path | None = None,
    skills_root: Path | None = None,
    patch_path: Path | None = None,
) -> dict[str, str]:
    init_db(root)
    title, text = _candidate_text(root, candidate_id)
    if target == "user":
        target_path = user_memory_path or root / "memories" / "USER.md"
        before = target_path.read_text(encoding="utf-8") if target_path.exists() else "# USER.md\n"
        after = _append_bullet(before, text)
        target_type = "USER.md"
    elif target == "agents":
        target_path = agents_path or root / "AGENTS.md"
        before = target_path.read_text(encoding="utf-8") if target_path.exists() else "# AGENTS.md\n"
        after = _project_agents_content(before, text)
        target_type = "AGENTS.md"
    elif target == "skill":
        slug = skill_slug(title, candidate_id)
        target_path = (skills_root or Path.home() / ".agents" / "skills") / slug / "SKILL.md"
        before = target_path.read_text(encoding="utf-8") if target_path.exists() else ""
        after = _skill_content(slug, title, text)
        target_type = "skill"
    elif target == "patch":
        target_path = patch_path or root / "self-improving-loop" / "exports" / f"skill-patch-{candidate_id}.md"
        before = target_path.read_text(encoding="utf-8") if target_path.exists() else ""
        after = f"# {title}\n\n{text}\n"
        target_type = "skill_patch"
    else:
        raise ValueError(f"unknown promotion preview target: {target}")
    return {
        "candidate_id": str(candidate_id),
        "target": target,
        "target_type": target_type,
        "target_path": str(target_path),
        "write_text": after,
        "diff": _unified_diff(before, after, target_path),
        "will_change": str(before != after).lower(),
    }


def promote_to_user_memory(root: Path, candidate_id: int, user_memory_path: Path | None = None) -> dict[str, str]:
    init_db(root)
    user_memory = user_memory_path or root / "memories" / "USER.md"
    user_memory.parent.mkdir(parents=True, exist_ok=True)
    _, text = _candidate_text(root, candidate_id)
    backup_path = ""
    if user_memory.exists():
        backup = backups_dir(root) / f"USER.backup-{now_stamp()}.md"
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(user_memory, backup)
        backup_path = str(backup)
    existing = user_memory.read_text(encoding="utf-8") if user_memory.exists() else "# USER.md\n"
    updated = _append_bullet(existing, text)
    if updated != existing:
        user_memory.write_text(updated, encoding="utf-8")
    with connect(root) as conn:
        conn.execute("update candidates set status='promoted', updated_at=current_timestamp where id=?", (candidate_id,))
        conn.execute(
            "insert into promotions(candidate_id, target_type, target_path, backup_path, status, detail) values(?, 'USER.md', ?, ?, 'ok', ?)",
            (candidate_id, str(user_memory), backup_path, text),
        )
        conn.execute("insert into audit_log(action, target, detail) values('promote_user_memory', ?, ?)", (str(user_memory), text))
    return {"target_path": str(user_memory), "backup_path": backup_path, "status": "ok"}


def promote_to_project_agents(root: Path, candidate_id: int, agents_path: Path | None = None) -> dict[str, str]:
    init_db(root)
    target = agents_path or root / "AGENTS.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    _, text = _candidate_text(root, candidate_id)
    backup_path = ""
    if target.exists():
        backup = backups_dir(root) / f"AGENTS.backup-{now_stamp()}.md"
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, backup)
        backup_path = str(backup)
    existing = target.read_text(encoding="utf-8") if target.exists() else "# AGENTS.md\n"
    updated = _project_agents_content(existing, text)
    if updated != existing:
        target.write_text(updated, encoding="utf-8")
    with connect(root) as conn:
        conn.execute("update candidates set status='promoted', updated_at=current_timestamp where id=?", (candidate_id,))
        conn.execute(
            "insert into promotions(candidate_id, target_type, target_path, backup_path, status, detail) values(?, 'AGENTS.md', ?, ?, 'ok', ?)",
            (candidate_id, str(target), backup_path, text),
        )
        conn.execute("insert into audit_log(action, target, detail) values('promote_project_agents', ?, ?)", (str(target), text))
    return {"target_path": str(target), "backup_path": backup_path, "status": "ok"}


def promote_to_skill(root: Path, candidate_id: int, skills_root: Path | None = None) -> dict[str, str]:
    init_db(root)
    target_root = skills_root or Path.home() / ".agents" / "skills"
    title, body = _candidate_text(root, candidate_id)
    slug = skill_slug(title, candidate_id)
    target = target_root / slug / "SKILL.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    backup_path = ""
    if target.exists():
        backup = backups_dir(root) / f"SKILL.backup-{now_stamp()}.md"
        shutil.copy2(target, backup)
        backup_path = str(backup)
    content = _skill_content(slug, title, body)
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
    title, body = _candidate_text(root, candidate_id)
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
