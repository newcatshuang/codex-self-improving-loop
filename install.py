#!/usr/bin/env python3
"""Install Codex Self-Improving Loop from this repository."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


START = "<!-- codex-self-improving-loop:start -->"
END = "<!-- codex-self-improving-loop:end -->"
COPY_IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", ".pytest_cache", ".mypy_cache", ".ruff_cache")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def copy_tree(src: Path, dst: Path, force: bool) -> None:
    if dst.exists() and force:
        shutil.rmtree(dst)
    if dst.exists():
        print(f"SKIP existing: {dst}")
        return
    shutil.copytree(src, dst, ignore=COPY_IGNORE)
    print(f"COPY: {src} -> {dst}")


def copy_file_if_missing(src: Path, dst: Path, force: bool = False) -> None:
    ensure_dir(dst.parent)
    if dst.exists() and not force:
        print(f"SKIP existing: {dst}")
        return
    shutil.copy2(src, dst)
    print(f"COPY: {src} -> {dst}")


def install_app(repo: Path, dst: Path, force: bool) -> None:
    if dst.exists() and force:
        shutil.rmtree(dst)
    ensure_dir(dst)
    copy_file_if_missing(repo / "sil.py", dst / "sil.py", force=True)
    copy_tree(repo / "src", dst / "src", force=True)
    copy_tree(repo / "agents", dst / "agents", force=True)
    copy_tree(repo / "codex", dst / "codex", force=True)
    print(f"COPY app: {repo} -> {dst}")


def remove_learning_block(dst: Path) -> None:
    if not dst.exists():
        return
    existing = dst.read_text(encoding="utf-8")
    if START not in existing or END not in existing:
        return
    before, rest = existing.split(START, 1)
    _, after = rest.split(END, 1)
    cleaned = before.rstrip() + "\n\n" + after.lstrip()
    dst.write_text(cleaned.rstrip() + "\n", encoding="utf-8")
    print(f"REMOVE learning block: {dst}")


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
        codex_root / "self-improving-loop",
        codex_root / "self-improving-loop" / "backups",
        codex_root / "self-improving-loop" / "exports",
        codex_root / "self-improving-loop" / "tmp",
    ):
        ensure_dir(directory)

    copy_tree(repo / "agents" / "skills" / "session-recall", agents_root / "skills" / "session-recall", args.force)
    copy_tree(repo / "agents" / "skills" / "memory-capture", agents_root / "skills" / "memory-capture", args.force)
    install_app(repo, agents_root / "codex-self-improving-loop", args.force)
    copy_file_if_missing(repo / "codex" / "memories" / "USER.template.md", codex_root / "memories" / "USER.md", force=False)
    remove_learning_block(codex_root / "AGENTS.md")

    print()
    print("Installed Codex Self-Improving Loop.")
    print(f"Codex root: {codex_root}")
    print(f"Agents root: {agents_root}")
    print("Restart Codex or open a new session so skill discovery reloads installed files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
