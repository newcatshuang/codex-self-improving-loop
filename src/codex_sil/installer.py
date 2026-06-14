"""Install skill resources from the bundled app copy."""

from __future__ import annotations

import shutil
from pathlib import Path


COPY_IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", ".pytest_cache", ".mypy_cache", ".ruff_cache")


def copy_tree(src: Path, dst: Path, force: bool = True) -> None:
    if dst.exists() and force:
        shutil.rmtree(dst)
    if dst.exists():
        return
    shutil.copytree(src, dst, ignore=COPY_IGNORE)


def copy_file_if_missing(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists():
        shutil.copy2(src, dst)


def install_skills(app_root: Path, codex_root: Path, agents_root: Path | None = None) -> dict[str, str]:
    agents = agents_root or Path.home() / ".agents"
    copy_tree(app_root / "agents" / "skills" / "session-recall", agents / "skills" / "session-recall")
    copy_tree(app_root / "agents" / "skills" / "memory-capture", agents / "skills" / "memory-capture")
    return {"agents_root": str(agents), "codex_root": str(codex_root), "status": "ok"}


def install_user_template(app_root: Path, codex_root: Path) -> dict[str, str]:
    target = codex_root / "memories" / "USER.md"
    copy_file_if_missing(app_root / "codex" / "memories" / "USER.template.md", codex_root / "memories" / "USER.md")
    return {"codex_root": str(codex_root), "target": str(target), "status": "ok"}
