"""Backup and migration bundle helpers."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

from .db import connect, init_db
from .paths import db_path, exports_dir
from .scanner import now_stamp


def _add_if_exists(bundle: zipfile.ZipFile, path: Path, arcname: str) -> None:
    if path.exists() and path.is_file():
        bundle.write(path, arcname)


def export_bundle(root: Path, agents_root: Path | None = None) -> Path:
    init_db(root)
    output = exports_dir(root) / f"codex-sil-bundle-{now_stamp()}.zip"
    output.parent.mkdir(parents=True, exist_ok=True)
    agents = agents_root or Path.home() / ".agents"
    manifest = {"created_at": now_stamp(), "root": str(root)}
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        _add_if_exists(bundle, db_path(root), "self-improving-loop.sqlite")
        _add_if_exists(bundle, root / "memories" / "USER.md", "memories/USER.md")
        _add_if_exists(bundle, root / "AGENTS.md", "AGENTS.md")
        skills_dir = agents / "skills"
        if skills_dir.exists():
            for path in skills_dir.rglob("SKILL.md"):
                bundle.write(path, f"skills/{path.parent.name}/SKILL.md")
        with connect(root) as conn:
            audit = [dict(row) for row in conn.execute("select * from audit_log order by id")]
        bundle.writestr("audit-history.json", json.dumps(audit, ensure_ascii=False, indent=2))
        bundle.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    return output


def import_preview(bundle_path: Path, root: Path) -> dict[str, object]:
    if not bundle_path.exists():
        return {"valid": False, "error": "bundle not found", "entries": []}
    try:
        with zipfile.ZipFile(bundle_path, "r") as bundle:
            entries = sorted(bundle.namelist())
    except zipfile.BadZipFile:
        return {"valid": False, "error": "invalid zip", "entries": []}
    required = {"manifest.json", "self-improving-loop.sqlite"}
    impacts = []
    for entry in entries:
        if entry == "self-improving-loop.sqlite":
            impacts.append(str(db_path(root)))
        elif entry == "memories/USER.md":
            impacts.append(str(root / "memories" / "USER.md"))
        elif entry == "AGENTS.md":
            impacts.append(str(root / "AGENTS.md"))
        elif entry.startswith("skills/"):
            impacts.append(str(Path.home() / ".agents" / entry))
    return {
        "valid": required.issubset(set(entries)),
        "entries": entries,
        "would_touch": impacts,
        "error": "" if required.issubset(set(entries)) else "missing required bundle entries",
    }
