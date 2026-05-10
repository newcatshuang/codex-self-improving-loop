#!/usr/bin/env python3
"""Verify installation into temporary or custom roots."""

from __future__ import annotations

import argparse
import py_compile
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
    install = repo / "install.py"
    subprocess.run([sys.executable, str(install), "--codex-root", str(codex), "--agents-root", str(agents), "--force"], check=True)

    expected = [
        codex / "memories" / "USER.md",
        codex / "AGENTS.md",
        agents / "skills" / "session-recall" / "SKILL.md",
        agents / "skills" / "session-recall" / "scripts" / "search_sessions.py",
        agents / "skills" / "memory-capture" / "SKILL.md",
        agents / "skills" / "memory-capture" / "scripts" / "codex_memory_nudge.py",
    ]
    for path in expected:
        if not path.exists():
            raise FileNotFoundError(path)

    for script in (agents / "skills").rglob("*.py"):
        py_compile.compile(str(script), doraise=True)

    scripts = agents / "skills" / "memory-capture" / "scripts"
    subprocess.run([sys.executable, str(scripts / "record_skill_usage.py"), "--root", str(codex), "--skill-name", "memory-capture"], check=True)
    subprocess.run([sys.executable, str(scripts / "show_skill_usage.py"), "--root", str(codex), "--json"], check=True)
    subprocess.run([sys.executable, str(scripts / "generate_skills_index.py"), "--root", str(codex), "--skills-root", str(agents / "skills")], check=True)
    subprocess.run([sys.executable, str(scripts / "summarize_learning_inbox.py"), "--root", str(codex)], check=True)

    for path in (codex / "skills-index.md", codex / "learning-inbox-summary.md", codex / "skill-usage.json"):
        if not path.exists():
            raise FileNotFoundError(path)

    print("verify-install passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
