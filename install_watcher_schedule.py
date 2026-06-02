#!/usr/bin/env python3
"""Install a daily OS schedule for the installed Codex session watcher."""

from __future__ import annotations

import argparse
import html
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


TASK_NAME = "CodexSelfImprovingLoopWatcher"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def installed_watcher(agents_root: Path) -> Path:
    return agents_root.expanduser() / "skills" / "memory-capture" / "scripts" / "codex_session_watcher.py"


def command_parts(args: argparse.Namespace) -> list[str]:
    command = [sys.executable, str(installed_watcher(args.agents_root)), "--once"]
    if args.since_date:
        command.extend(["--since-date", args.since_date])
    if args.max_sessions_per_run is not None:
        command.extend(["--max-sessions-per-run", str(args.max_sessions_per_run)])
    return command


def shell_quote(parts: list[str]) -> str:
    import shlex

    return " ".join(shlex.quote(part) for part in parts)


def windows_task_quote(part: str) -> str:
    escaped = part.replace('"', r'\"')
    if not part or any(ch.isspace() for ch in part) or "\\" in part or "/" in part:
        return f'"{escaped}"'
    return escaped


def install_windows(args: argparse.Namespace) -> None:
    task_run = " ".join(windows_task_quote(part) for part in command_parts(args))
    subprocess.run(
        [
            "schtasks.exe",
            "/Create",
            "/TN",
            TASK_NAME,
            "/SC",
            "DAILY",
            "/ST",
            f"{int(args.hour):02d}:{int(args.minute):02d}",
            "/TR",
            task_run,
            "/F",
        ],
        check=True,
    )


def install_linux(args: argparse.Namespace) -> None:
    config_dir = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    systemd_dir = config_dir / "systemd" / "user"
    ensure_dir(systemd_dir)
    service = systemd_dir / f"{TASK_NAME}.service"
    timer = systemd_dir / f"{TASK_NAME}.timer"
    service.write_text(
        "\n".join(
            [
                "[Unit]",
                "Description=Run Codex Self-Improving Loop watcher",
                "",
                "[Service]",
                "Type=oneshot",
                f"ExecStart={shell_quote(command_parts(args))}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    timer.write_text(
        "\n".join(
            [
                "[Unit]",
                "Description=Run Codex Self-Improving Loop watcher daily",
                "",
                "[Timer]",
                f"OnCalendar=*-*-* {int(args.hour):02d}:{int(args.minute):02d}:00",
                "Persistent=true",
                "",
                "[Install]",
                "WantedBy=timers.target",
                "",
            ]
        ),
        encoding="utf-8",
    )
    systemctl = shutil.which("systemctl")
    if systemctl:
        subprocess.run([systemctl, "--user", "daemon-reload"], check=True)
        subprocess.run([systemctl, "--user", "enable", "--now", f"{TASK_NAME}.timer"], check=True)
    else:
        print(f"systemctl not found. Timer files written to {systemd_dir}.")


def install_macos(args: argparse.Namespace) -> None:
    launch_agents = Path.home() / "Library" / "LaunchAgents"
    ensure_dir(launch_agents)
    plist = launch_agents / "com.codex.self-improving-loop.watcher.plist"
    program_arguments = "\n".join(f"    <string>{html.escape(part)}</string>" for part in command_parts(args))
    stdout_path = html.escape(str(Path.home() / ".codex" / "memory-watcher.out.log"))
    stderr_path = html.escape(str(Path.home() / ".codex" / "memory-watcher.err.log"))
    plist.write_text(
        f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.codex.self-improving-loop.watcher</string>
  <key>ProgramArguments</key>
  <array>
{program_arguments}
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key>
    <integer>{int(args.hour)}</integer>
    <key>Minute</key>
    <integer>{int(args.minute)}</integer>
  </dict>
  <key>StandardOutPath</key>
  <string>{stdout_path}</string>
  <key>StandardErrorPath</key>
  <string>{stderr_path}</string>
</dict>
</plist>
""",
        encoding="utf-8",
    )
    launchctl = shutil.which("launchctl")
    if launchctl:
        subprocess.run([launchctl, "unload", str(plist)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run([launchctl, "load", str(plist)], check=True)
    else:
        print(f"launchctl not found. plist written to {plist}.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agents-root", type=Path, default=Path.home() / ".agents", help="Installed agents root; defaults to $HOME/.agents")
    parser.add_argument("--hour", type=int, default=12, help="Hour of day to run, 0-23; defaults to 12")
    parser.add_argument("--minute", type=int, default=0, help="Minute of hour to run, 0-59; defaults to 0")
    parser.add_argument("--since-date", help="Pass through to codex_session_watcher.py")
    parser.add_argument("--max-sessions-per-run", type=int, default=None, help="Pass through to codex_session_watcher.py; omit for watcher default")
    parser.add_argument("--dry-run", action="store_true", help="Print the scheduled command without installing")
    args = parser.parse_args()

    if args.hour < 0 or args.hour > 23:
        raise SystemExit("--hour must be between 0 and 23")
    if args.minute < 0 or args.minute > 59:
        raise SystemExit("--minute must be between 0 and 59")
    watcher = installed_watcher(args.agents_root)
    if not watcher.exists():
        raise SystemExit(f"Installed watcher not found: {watcher}. Run install.py first.")

    if args.dry_run:
        print(shell_quote(command_parts(args)))
        return 0

    system = platform.system()
    if system == "Windows":
        install_windows(args)
    elif system == "Linux":
        install_linux(args)
    elif system == "Darwin":
        install_macos(args)
    else:
        raise SystemExit(f"Unsupported platform: {system}")

    print(f"Installed daily watcher schedule for {watcher} at {int(args.hour):02d}:{int(args.minute):02d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
