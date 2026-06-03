#!/usr/bin/env python3
"""Verify installation into temporary or custom roots."""

from __future__ import annotations

import argparse
import importlib.util
import json
import py_compile
import subprocess
import sys
from pathlib import Path


def load_schedule_module(repo: Path):
    spec = importlib.util.spec_from_file_location("install_watcher_schedule_for_test", repo / "install_watcher_schedule.py")
    if spec is None or spec.loader is None:
        raise AssertionError("could not load install_watcher_schedule.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
        agents / "skills" / "memory-capture" / "scripts" / "build_learning_index.py",
        agents / "skills" / "memory-capture" / "scripts" / "render_dashboard.py",
        agents / "skills" / "memory-capture" / "templates" / "dashboard.html",
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
    subprocess.run([sys.executable, str(repo / "tests" / "verify-learning-extraction.py"), "--repo-root", str(repo), "--work-root", str(codex / "learning-extraction-test")], check=True)
    subprocess.run([sys.executable, str(repo / "tests" / "verify-candidate-dedup.py"), "--repo-root", str(repo), "--work-root", str(codex / "candidate-dedup-test")], check=True)
    subprocess.run([sys.executable, str(repo / "tests" / "verify-review-digest.py"), "--repo-root", str(repo), "--work-root", str(codex / "review-digest-test")], check=True)
    subprocess.run([sys.executable, str(repo / "tests" / "verify-learning-index.py"), "--repo-root", str(repo), "--work-root", str(codex / "learning-index-test")], check=True)
    subprocess.run([sys.executable, str(repo / "tests" / "verify-dashboard-render.py"), "--repo-root", str(repo), "--work-root", str(codex / "dashboard-render-test")], check=True)
    subprocess.run([sys.executable, str(repo / "tests" / "verify-readme-assets.py"), "--repo-root", str(repo)], check=True)
    subprocess.run([sys.executable, str(repo / "tests" / "verify-daily-schedule.py"), "--repo-root", str(repo), "--work-root", str(codex / "daily-schedule-test")], check=True)
    subprocess.run([sys.executable, str(repo / "tests" / "verify-low-output-mode.py"), "--repo-root", str(repo), "--work-root", str(codex / "low-output-test")], check=True)
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
    schedule = load_schedule_module(repo)
    schtasks_calls = []

    def fake_run(command, check=True, **_kwargs):
        schtasks_calls.append(command)

    original_argv = sys.argv
    original_system = schedule.platform.system
    original_run = schedule.subprocess.run
    try:
        sys.argv = [
            "install_watcher_schedule.py",
            "--agents-root",
            str(agents),
        ]
        schedule.platform.system = lambda: "Windows"
        schedule.subprocess.run = fake_run
        schedule.main()
    finally:
        sys.argv = original_argv
        schedule.platform.system = original_system
        schedule.subprocess.run = original_run
    if not schtasks_calls:
        raise AssertionError("Windows schedule installer should call schtasks.exe")
    windows_create = schtasks_calls[0]
    if "/XML" in windows_create:
        raise AssertionError("Windows schedule installer should not use XML Daily+Repetition")
    expected_flags = ["/SC", "DAILY", "/ST", "12:00"]
    for flag in expected_flags:
        if flag not in windows_create:
            raise AssertionError(f"Windows daily schedule missing {flag}: {windows_create}")
    if "/MO" in windows_create or "HOURLY" in windows_create:
        raise AssertionError(f"Windows schedule should run daily, not hourly: {windows_create}")
    if "/TR" not in windows_create or "codex_session_watcher.py" not in " ".join(windows_create):
        raise AssertionError("Windows schedule should run the installed watcher command")
    pause_calls = []
    try:
        sys.argv = [
            "install_watcher_schedule.py",
            "--agents-root",
            str(agents),
            "--pause-on-exit",
        ]
        schedule.platform.system = lambda: "Windows"
        schedule.subprocess.run = lambda command, check=True, **_kwargs: pause_calls.append(command)
        schedule.main()
    finally:
        sys.argv = original_argv
        schedule.platform.system = original_system
        schedule.subprocess.run = original_run
    pause_wrapper = agents / "codex-self-improving-loop-watcher.cmd"
    if not pause_wrapper.exists():
        raise AssertionError("Windows pause-on-exit should create a wrapper under agents root")
    pause_text = pause_wrapper.read_text(encoding="utf-8")
    if "pause" not in pause_text or "codex_session_watcher.py" not in pause_text:
        raise AssertionError("Windows pause wrapper should run watcher and wait for user input")
    if not pause_calls or str(pause_wrapper) not in " ".join(pause_calls[0]):
        raise AssertionError("Windows pause-on-exit task should run the wrapper")
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
    watcher_run = subprocess.run(
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
        text=True,
        capture_output=True,
    )
    if "Review digest summary:" not in watcher_run.stdout:
        raise AssertionError("watcher should print the post-run review digest summary")
    if "Promotion options:" not in watcher_run.stdout:
        raise AssertionError("watcher should print promotion option location after processing")

    for path in (
        codex / "skills-index.md",
        codex / "learning-inbox-summary.md",
        codex / "latest-skill-candidate-security-scan.md",
        codex / "latest-user-memory-budget.md",
        codex / "skill-usage.json",
        codex / "memory-watcher-state.json",
        codex / "learning-index.json",
        codex / "codex-self-improving-loop-dashboard.html",
    ):
        if not path.exists():
            raise FileNotFoundError(path)
    if not list((codex / "daily-digests").rglob("review-digest.md")):
        raise FileNotFoundError(codex / "daily-digests" / "review-digest.md")

    print("verify-install passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
