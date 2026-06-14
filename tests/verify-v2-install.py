#!/usr/bin/env python3
"""Verify v2 installation layout and removal of old script-based runtime."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--codex-root", type=Path, required=True)
    parser.add_argument("--agents-root", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    codex = args.codex_root.resolve()
    agents = args.agents_root.resolve()
    codex.mkdir(parents=True, exist_ok=True)
    (codex / "AGENTS.md").write_text(
        "# AGENTS.md\n\n"
        "<!-- codex-self-improving-loop:start -->\n"
        "legacy global block\n"
        "<!-- codex-self-improving-loop:end -->\n",
        encoding="utf-8",
    )

    forbidden = [
        repo / "agents" / "skills" / "memory-capture" / "scripts",
        repo / "agents" / "skills" / "session-recall" / "scripts",
        repo / "agents" / "skills" / "memory-capture" / "templates",
        repo / "install_watcher_schedule.py",
    ]
    for path in forbidden:
        if path.exists():
            raise AssertionError(f"old v1 artifact should be removed: {path}")

    subprocess.run(
        [sys.executable, str(repo / "install.py"), "--codex-root", str(codex), "--agents-root", str(agents), "--force"],
        check=True,
    )

    expected = [
        agents / "codex-self-improving-loop" / "sil.py",
        agents / "codex-self-improving-loop" / "src" / "codex_sil" / "cli.py",
        agents / "codex-self-improving-loop" / "agents" / "skills" / "memory-capture" / "SKILL.md",
        agents / "skills" / "session-recall" / "SKILL.md",
        agents / "skills" / "memory-capture" / "SKILL.md",
        codex / "memories" / "USER.md",
        codex / "self-improving-loop",
    ]
    for path in expected:
        if not path.exists():
            raise FileNotFoundError(path)
    installed_app = agents / "codex-self-improving-loop"
    compiled_artifacts = [path for path in installed_app.rglob("*") if "__pycache__" in path.parts or path.suffix == ".pyc"]
    if compiled_artifacts:
        raise AssertionError(f"installed app should not include Python bytecode artifacts: {compiled_artifacts[:5]}")
    agents_text = (codex / "AGENTS.md").read_text(encoding="utf-8")
    if "codex-self-improving-loop:start" in agents_text or "Codex Self-Improving Loop" in agents_text:
        raise AssertionError("installer should remove old global AGENTS.md self-improving-loop blocks")
    if (repo / "codex" / "AGENTS.learning-block.md").exists():
        raise AssertionError("global AGENTS.md learning block template should be removed")

    recall_skill = (agents / "skills" / "session-recall" / "SKILL.md").read_text(encoding="utf-8")
    memory_skill = (agents / "skills" / "memory-capture" / "SKILL.md").read_text(encoding="utf-8")
    for text in (recall_skill, memory_skill):
        if "codex-self-improving-loop" not in text or "sil.py" not in text:
            raise AssertionError("skills should point to the v2 sil.py entrypoint")
        if "/scripts/" in text or "extract_memory.py" in text or "search_sessions.py" in text:
            raise AssertionError("skills should not reference removed v1 scripts")

    subprocess.run(
        [
            sys.executable,
            str(agents / "codex-self-improving-loop" / "sil.py"),
            "doctor",
            "--codex-root",
            str(codex),
            "--json",
        ],
        check=True,
    )
    print("verify-v2-install passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
