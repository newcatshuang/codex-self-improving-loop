#!/usr/bin/env python3
"""Install Codex Self-Improving Loop from this repository."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


START = "<!-- codex-self-improving-loop:start -->"
END = "<!-- codex-self-improving-loop:end -->"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def copy_tree(src: Path, dst: Path, force: bool) -> None:
    if dst.exists() and force:
        shutil.rmtree(dst)
    if dst.exists():
        print(f"SKIP existing: {dst}")
        return
    shutil.copytree(src, dst)
    print(f"COPY: {src} -> {dst}")


def copy_file_if_missing(src: Path, dst: Path, force: bool = False) -> None:
    ensure_dir(dst.parent)
    if dst.exists() and not force:
        print(f"SKIP existing: {dst}")
        return
    shutil.copy2(src, dst)
    print(f"COPY: {src} -> {dst}")


def append_learning_block(src: Path, dst: Path, force: bool) -> None:
    block = src.read_text(encoding="utf-8").strip() + "\n"
    existing = dst.read_text(encoding="utf-8") if dst.exists() else "# AGENTS.md\n\n"
    if START in existing and END in existing:
        if not force:
            print(f"SKIP existing learning block: {dst}")
            return
        before, rest = existing.split(START, 1)
        _, after = rest.split(END, 1)
        dst.write_text(before.rstrip() + "\n\n" + block + after.lstrip(), encoding="utf-8")
        print(f"REPLACE learning block: {dst}")
        return
    ensure_dir(dst.parent)
    dst.write_text(existing.rstrip() + "\n\n" + block, encoding="utf-8")
    print(f"APPEND: {dst}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-root", type=Path, default=Path.home() / ".codex")
    parser.add_argument("--agents-root", type=Path, default=Path.home() / ".agents")
    parser.add_argument("--force", action="store_true", help="Overwrite installed skills managed by this repo")
    args = parser.parse_args()

    repo = Path(__file__).resolve().parent
    codex_root = args.codex_root.expanduser().resolve()
    agents_root = args.agents_root.expanduser().resolve()

    for directory in (
        codex_root,
        agents_root,
        codex_root / "memories" / "inbox",
        codex_root / "memories" / "archive",
        codex_root / "skill-candidates" / "inbox",
        codex_root / "skill-candidates" / "patches",
        codex_root / "skill-candidates" / "archive",
        codex_root / "nudge-reports",
    ):
        ensure_dir(directory)

    copy_tree(repo / "agents" / "skills" / "session-recall", agents_root / "skills" / "session-recall", args.force)
    copy_tree(repo / "agents" / "skills" / "memory-capture", agents_root / "skills" / "memory-capture", args.force)
    copy_file_if_missing(repo / "codex" / "memories" / "USER.template.md", codex_root / "memories" / "USER.md", force=False)
    append_learning_block(repo / "codex" / "AGENTS.learning-block.md", codex_root / "AGENTS.md", args.force)

    print()
    print("Installed Codex Self-Improving Loop.")
    print(f"Codex root: {codex_root}")
    print(f"Agents root: {agents_root}")
    print("Restart Codex or open a new session so skill discovery reloads installed files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
