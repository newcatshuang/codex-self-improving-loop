"""Install v2 skill resources from the bundled app copy."""

from __future__ import annotations

import shutil
from pathlib import Path


START = "<!-- codex-self-improving-loop:start -->"
END = "<!-- codex-self-improving-loop:end -->"


def copy_tree(src: Path, dst: Path, force: bool = True) -> None:
    if dst.exists() and force:
        shutil.rmtree(dst)
    if dst.exists():
        return
    shutil.copytree(src, dst)


def copy_file_if_missing(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists():
        shutil.copy2(src, dst)


def append_learning_block(src: Path, dst: Path, force: bool = True) -> None:
    block = src.read_text(encoding="utf-8").strip() + "\n"
    existing = dst.read_text(encoding="utf-8") if dst.exists() else "# AGENTS.md\n\n"
    if START in existing and END in existing:
        if not force:
            return
        before, rest = existing.split(START, 1)
        _, after = rest.split(END, 1)
        dst.write_text(before.rstrip() + "\n\n" + block + after.lstrip(), encoding="utf-8")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(existing.rstrip() + "\n\n" + block, encoding="utf-8")


def install_skills(app_root: Path, codex_root: Path, agents_root: Path | None = None) -> dict[str, str]:
    agents = agents_root or Path.home() / ".agents"
    copy_tree(app_root / "agents" / "skills" / "session-recall", agents / "skills" / "session-recall")
    copy_tree(app_root / "agents" / "skills" / "memory-capture", agents / "skills" / "memory-capture")
    copy_file_if_missing(app_root / "codex" / "memories" / "USER.template.md", codex_root / "memories" / "USER.md")
    append_learning_block(app_root / "codex" / "AGENTS.learning-block.md", codex_root / "AGENTS.md", force=True)
    return {"agents_root": str(agents), "codex_root": str(codex_root), "status": "ok"}
