#!/usr/bin/env python3
"""Verify installation into temporary or custom roots."""

from __future__ import annotations

import argparse
import json
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
        agents / "skills" / "memory-capture" / "scripts" / "codex_session_watcher.py",
        repo / "install_watcher_schedule.py",
    ]
    for path in expected:
        if not path.exists():
            raise FileNotFoundError(path)

    for script in (agents / "skills").rglob("*.py"):
        py_compile.compile(str(script), doraise=True)
    py_compile.compile(str(repo / "install_watcher_schedule.py"), doraise=True)

    scripts = agents / "skills" / "memory-capture" / "scripts"
    session_dir = codex / "sessions"
    session_dir.mkdir(parents=True, exist_ok=True)
    session_file = session_dir / "verify-session.jsonl"
    session_file.write_text('{"role":"user","content":"Please remember: prefer verification before completion."}\n', encoding="utf-8")
    subprocess.run([sys.executable, str(scripts / "record_skill_usage.py"), "--root", str(codex), "--skill-name", "memory-capture"], check=True)
    subprocess.run([sys.executable, str(scripts / "show_skill_usage.py"), "--root", str(codex), "--json"], check=True)
    subprocess.run([sys.executable, str(scripts / "generate_skills_index.py"), "--root", str(codex), "--skills-root", str(agents / "skills")], check=True)
    subprocess.run([sys.executable, str(scripts / "summarize_learning_inbox.py"), "--root", str(codex)], check=True)
    subprocess.run([sys.executable, str(scripts / "codex_memory_nudge.py"), "--root", str(codex), "--session-file", str(session_file), "--skip-skills-index", "--skip-learning-summary"], check=True)
    schedule_dry_run = subprocess.run(
        [
            sys.executable,
            str(repo / "install_watcher_schedule.py"),
            "--agents-root",
            str(agents),
            "--dry-run",
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    if "codex_session_watcher.py" not in schedule_dry_run.stdout or str(agents) not in schedule_dry_run.stdout:
        raise AssertionError("schedule installer should target the installed watcher under agents root")
    watcher_state = codex / "watcher-test-state.json"
    dry_run = subprocess.run(
        [
            sys.executable,
            str(scripts / "codex_session_watcher.py"),
            "--root",
            str(codex),
            "--state-file",
            str(watcher_state),
            "--once",
            "--dry-run",
            "--idle-seconds",
            "0",
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    default_payload = json.loads(dry_run.stdout)
    if len(default_payload.get("ready_sessions", [])) != 1:
        raise AssertionError("default watcher dry-run should process existing session history")
    future_dry_run = subprocess.run(
        [
            sys.executable,
            str(scripts / "codex_session_watcher.py"),
            "--root",
            str(codex),
            "--state-file",
            str(watcher_state),
            "--once",
            "--dry-run",
            "--idle-seconds",
            "0",
            "--since-date",
            "2999-01-01",
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    future_payload = json.loads(future_dry_run.stdout)
    if future_payload.get("ready_sessions"):
        raise AssertionError("--since-date should filter out older sessions")
    subprocess.run(
        [
            sys.executable,
            str(scripts / "codex_session_watcher.py"),
            "--root",
            str(codex),
            "--once",
            "--idle-seconds",
            "0",
        ],
        check=True,
    )

    for path in (codex / "skills-index.md", codex / "learning-inbox-summary.md", codex / "skill-usage.json", codex / "memory-watcher-state.json"):
        if not path.exists():
            raise FileNotFoundError(path)
    if not list((codex / "nudge-reports").glob("*-end-of-task-nudge.md")):
        raise FileNotFoundError(codex / "nudge-reports" / "*-end-of-task-nudge.md")

    print("verify-install passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
