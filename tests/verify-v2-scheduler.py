#!/usr/bin/env python3
"""Verify cross-platform schedule installers create real scheduler artifacts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from unittest.mock import patch


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--work-root", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    root = args.work_root.resolve()
    sys.path.insert(0, str(repo / "src"))

    from codex_sil import scheduler

    calls: list[list[str]] = []

    def fake_run(command: list[str], check: bool = False, **_: object) -> object:
        calls.append(command)
        return object()

    with patch("codex_sil.scheduler.platform.system", return_value="Windows"), patch(
        "codex_sil.scheduler.subprocess.run", side_effect=fake_run
    ):
        text = scheduler.install_schedule(repo, root)
    if not calls or calls[0][:3] != ["schtasks.exe", "/Create", "/TN"]:
        raise AssertionError(f"Windows install should call schtasks: {calls}")
    if "/SC" not in calls[0] or "DAILY" not in calls[0] or "12:00" not in calls[0]:
        raise AssertionError(calls[0])
    if "schtasks.exe /Create" not in text:
        raise AssertionError(text)

    launch_agents = root / "home" / "Library" / "LaunchAgents"
    with patch("codex_sil.scheduler.platform.system", return_value="Darwin"), patch("pathlib.Path.home", return_value=root / "home"), patch(
        "codex_sil.scheduler.subprocess.run", side_effect=fake_run
    ):
        text = scheduler.install_schedule(repo, root)
    plist = launch_agents / "com.codex.self-improving-loop.plist"
    if not plist.exists():
        raise FileNotFoundError(plist)
    plist_text = plist.read_text(encoding="utf-8")
    if "StartCalendarInterval" not in plist_text or "<integer>12</integer>" not in plist_text:
        raise AssertionError(plist_text)
    if not any(call[:2] == ["launchctl", "load"] for call in calls):
        raise AssertionError(f"Darwin install should call launchctl load: {calls}")
    if "launchd plist" not in text:
        raise AssertionError(text)

    systemd = root / "config" / "systemd" / "user"
    with patch("codex_sil.scheduler.platform.system", return_value="Linux"), patch.dict("os.environ", {"XDG_CONFIG_HOME": str(root / "config")}), patch(
        "codex_sil.scheduler.subprocess.run", side_effect=fake_run
    ):
        text = scheduler.install_schedule(repo, root)
    service = systemd / "codex-self-improving-loop.service"
    timer = systemd / "codex-self-improving-loop.timer"
    if not service.exists() or not timer.exists():
        raise FileNotFoundError(f"{service} / {timer}")
    if "OnCalendar=*-*-* 12:00:00" not in timer.read_text(encoding="utf-8"):
        raise AssertionError(timer.read_text(encoding="utf-8"))
    if not any(call[:3] == ["systemctl", "--user", "enable"] for call in calls):
        raise AssertionError(f"Linux install should enable timer: {calls}")
    if "systemd user timer" not in text:
        raise AssertionError(text)

    print("verify-v2-scheduler passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
