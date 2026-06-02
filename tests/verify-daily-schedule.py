#!/usr/bin/env python3
"""Verify the watcher schedule defaults to daily noon on supported platforms."""

from __future__ import annotations

import argparse
import importlib.util
import os
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
    parser.add_argument("--work-root", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    root = args.work_root.resolve()
    agents = root / "agents"
    watcher = agents / "skills" / "memory-capture" / "scripts" / "codex_session_watcher.py"
    watcher.parent.mkdir(parents=True, exist_ok=True)
    watcher.write_text("# watcher\n", encoding="utf-8")
    schedule = load_schedule_module(repo)

    windows_calls = []

    def fake_windows_run(command, check=True, **_kwargs):
        windows_calls.append(command)

    original_argv = sys.argv
    original_system = schedule.platform.system
    original_run = schedule.subprocess.run
    try:
        sys.argv = ["install_watcher_schedule.py", "--agents-root", str(agents)]
        schedule.platform.system = lambda: "Windows"
        schedule.subprocess.run = fake_windows_run
        schedule.main()
    finally:
        sys.argv = original_argv
        schedule.platform.system = original_system
        schedule.subprocess.run = original_run
    if not windows_calls:
        raise AssertionError("Windows install should call schtasks.exe")
    windows_create = windows_calls[0]
    if "/SC" not in windows_create or "DAILY" not in windows_create or "/ST" not in windows_create or "12:00" not in windows_create:
        raise AssertionError(f"Windows schedule should be daily at 12:00: {windows_create}")
    if "HOURLY" in windows_create or "/MO" in windows_create:
        raise AssertionError(f"Windows schedule should not be hourly: {windows_create}")

    windows_pause_calls = []
    try:
        sys.argv = ["install_watcher_schedule.py", "--agents-root", str(agents), "--pause-on-exit"]
        schedule.platform.system = lambda: "Windows"
        schedule.subprocess.run = lambda command, check=True, **_kwargs: windows_pause_calls.append(command)
        schedule.main()
    finally:
        sys.argv = original_argv
        schedule.platform.system = original_system
        schedule.subprocess.run = original_run
    if not windows_pause_calls:
        raise AssertionError("Windows pause-on-exit install should call schtasks.exe")
    wrapper = agents / "codex-self-improving-loop-watcher.cmd"
    if not wrapper.exists():
        raise AssertionError("Windows pause-on-exit should write a cmd wrapper")
    wrapper_text = wrapper.read_text(encoding="utf-8")
    if "pause" not in wrapper_text or "codex_session_watcher.py" not in wrapper_text:
        raise AssertionError(f"Windows pause wrapper should run watcher and pause: {wrapper_text}")
    if str(wrapper) not in " ".join(windows_pause_calls[0]):
        raise AssertionError(f"Windows task should run the pause wrapper: {windows_pause_calls[0]}")

    systemctl_calls = []

    def fake_linux_run(command, check=True, **_kwargs):
        systemctl_calls.append(command)

    original_env = os.environ.get("XDG_CONFIG_HOME")
    original_which = schedule.shutil.which
    try:
        os.environ["XDG_CONFIG_HOME"] = str(root / "xdg")
        sys.argv = ["install_watcher_schedule.py", "--agents-root", str(agents)]
        schedule.platform.system = lambda: "Linux"
        schedule.shutil.which = lambda name: "/usr/bin/systemctl" if name == "systemctl" else None
        schedule.subprocess.run = fake_linux_run
        schedule.main()
    finally:
        sys.argv = original_argv
        schedule.platform.system = original_system
        schedule.shutil.which = original_which
        schedule.subprocess.run = original_run
        if original_env is None:
            os.environ.pop("XDG_CONFIG_HOME", None)
        else:
            os.environ["XDG_CONFIG_HOME"] = original_env
    timer = root / "xdg" / "systemd" / "user" / "CodexSelfImprovingLoopWatcher.timer"
    timer_text = timer.read_text(encoding="utf-8")
    if "OnCalendar=*-*-* 12:00:00" not in timer_text:
        raise AssertionError(f"Linux timer should run daily at 12:00: {timer_text}")
    if "*:*" in timer_text:
        raise AssertionError(f"Linux timer should not be hourly: {timer_text}")

    launchctl_calls = []

    def fake_macos_run(command, check=True, **_kwargs):
        launchctl_calls.append(command)

    original_home = schedule.Path.home
    try:
        sys.argv = ["install_watcher_schedule.py", "--agents-root", str(agents)]
        schedule.platform.system = lambda: "Darwin"
        schedule.Path.home = lambda: root
        schedule.shutil.which = lambda name: "/bin/launchctl" if name == "launchctl" else None
        schedule.subprocess.run = fake_macos_run
        schedule.main()
    finally:
        sys.argv = original_argv
        schedule.platform.system = original_system
        schedule.Path.home = original_home
        schedule.shutil.which = original_which
        schedule.subprocess.run = original_run
    plist = root / "Library" / "LaunchAgents" / "com.codex.self-improving-loop.watcher.plist"
    plist_text = plist.read_text(encoding="utf-8")
    if "<key>Hour</key>" not in plist_text or "<integer>12</integer>" not in plist_text:
        raise AssertionError(f"macOS plist should include Hour 12: {plist_text}")
    if "<key>Minute</key>" not in plist_text or "<integer>0</integer>" not in plist_text:
        raise AssertionError(f"macOS plist should include Minute 0: {plist_text}")

    print("verify-daily-schedule passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
