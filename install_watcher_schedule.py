#!/usr/bin/env python3
"""Install an hourly OS schedule for the installed Codex session watcher."""

from __future__ import annotations

import argparse
from datetime import datetime
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


def install_windows(args: argparse.Namespace) -> None:
    command = command_parts(args)
    arguments = " ".join(f'"{part}"' if " " in part or "\\" in part else part for part in command[1:])
    start_date = datetime.now().date().isoformat()
    tmp_dir = Path(os.environ.get("TEMP", str(Path.home())))
    ensure_dir(tmp_dir)
    xml_path = tmp_dir / f"{TASK_NAME}.xml"
    xml_path.write_text(
        f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Runs Codex Self-Improving Loop watcher once per hour.</Description>
  </RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>{start_date}T00:{int(args.minute):02d}:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
      <Repetition>
        <Interval>PT1H</Interval>
        <StopAtDurationEnd>false</StopAtDurationEnd>
      </Repetition>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT2H</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{html.escape(command[0])}</Command>
      <Arguments>{html.escape(arguments)}</Arguments>
    </Exec>
  </Actions>
</Task>
""",
        encoding="utf-16",
    )
    subprocess.run(
        [
            "schtasks.exe",
            "/Create",
            "/TN",
            TASK_NAME,
            "/XML",
            str(xml_path),
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
                "Description=Run Codex Self-Improving Loop watcher hourly",
                "",
                "[Timer]",
                f"OnCalendar=*-*-* *:{int(args.minute):02d}:00",
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
    parser.add_argument("--minute", type=int, default=0, help="Minute within each hour to run; 0 means on the hour")
    parser.add_argument("--since-date", help="Pass through to codex_session_watcher.py")
    parser.add_argument("--max-sessions-per-run", type=int, default=None, help="Pass through to codex_session_watcher.py; omit for watcher default")
    parser.add_argument("--dry-run", action="store_true", help="Print the scheduled command without installing")
    args = parser.parse_args()

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

    print(f"Installed hourly watcher schedule for {watcher}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
