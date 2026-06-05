"""Cross-platform schedule and shortcut command generation."""

from __future__ import annotations

import platform
import subprocess
import sys
import os
from pathlib import Path
from typing import Any


SCHEDULE_HOUR = 3
SCHEDULE_TIME = "03:00"


def sil_command(repo_root: Path, *args: str) -> list[str]:
    return [sys.executable, str(repo_root / "sil.py"), *args]


def display_command(parts: list[str]) -> str:
    return " ".join(f'"{part}"' if " " in part else part for part in parts)


def windows_task_command(parts: list[str]) -> str:
    return subprocess.list2cmdline(parts)


def launch_agent_path() -> Path:
    return Path.home() / "Library" / "LaunchAgents" / "com.codex.self-improving-loop.plist"


def systemd_user_dir() -> Path:
    base = os.environ.get("XDG_CONFIG_HOME")
    return (Path(base) if base else Path.home() / ".config") / "systemd" / "user"


def schedule_command(repo_root: Path, codex_root: Path) -> str:
    return display_command(sil_command(repo_root, "scan", "--once", "--codex-root", str(codex_root)))


def shortcut_command(repo_root: Path, codex_root: Path) -> str:
    return display_command(sil_command(repo_root, "serve", "--open", "--port", "0", "--codex-root", str(codex_root)))


def install_schedule_dry_run(repo_root: Path, codex_root: Path) -> str:
    system = platform.system()
    parts = sil_command(repo_root, "scan", "--once", "--codex-root", str(codex_root))
    command = windows_task_command(parts) if system == "Windows" else schedule_command(repo_root, codex_root)
    if system == "Windows":
        return f"schtasks.exe /Create /TN CodexSelfImprovingLoop /SC DAILY /ST {SCHEDULE_TIME} /TR {command} /F"
    if system == "Darwin":
        return f"launchd plist {launch_agent_path()} daily {SCHEDULE_TIME} -> {command}"
    return f"systemd user timer {systemd_user_dir() / 'codex-self-improving-loop.timer'} daily {SCHEDULE_TIME} -> {command}"


def schedule_status(repo_root: Path, codex_root: Path) -> dict[str, Any]:
    """Return a best-effort, read-only view of the local daily schedule."""
    system = platform.system()
    installed = False
    detail = ""
    if system == "Windows":
        try:
            result = subprocess.run(
                ["schtasks.exe", "/Query", "/TN", "CodexSelfImprovingLoop"],
                check=False,
                text=True,
                encoding="utf-8",
                errors="replace",
                capture_output=True,
            )
            installed = result.returncode == 0
            detail = (result.stdout or result.stderr or "").strip()
        except OSError as exc:
            detail = str(exc)
    elif system == "Darwin":
        path = launch_agent_path()
        installed = path.exists()
        detail = str(path)
    else:
        timer = systemd_user_dir() / "codex-self-improving-loop.timer"
        installed = timer.exists()
        detail = str(timer)
    return {
        "system": system or "Unknown",
        "installed": installed,
        "schedule_time": SCHEDULE_TIME,
        "command": schedule_command(repo_root, codex_root),
        "detail": detail[:1200],
    }


def install_shortcut_dry_run(repo_root: Path, codex_root: Path) -> str:
    system = platform.system()
    command = shortcut_command(repo_root, codex_root)
    if system == "Windows":
        return f"Desktop shortcut Codex Self-Improving Loop -> {command}"
    if system == "Darwin":
        return f"Desktop .command Codex Self-Improving Loop -> {command}"
    return f"Desktop .desktop Codex Self-Improving Loop -> {command}"


def install_schedule(repo_root: Path, codex_root: Path, dry_run: bool = False) -> str:
    text = install_schedule_dry_run(repo_root, codex_root)
    if dry_run:
        return text
    system = platform.system()
    parts = sil_command(repo_root, "scan", "--once", "--codex-root", str(codex_root))
    command = windows_task_command(parts) if system == "Windows" else display_command(parts)
    if system == "Windows":
        subprocess.run(
            [
                "schtasks.exe",
                "/Create",
                "/TN",
                "CodexSelfImprovingLoop",
                "/SC",
                "DAILY",
                "/ST",
                SCHEDULE_TIME,
                "/TR",
                command,
                "/F",
            ],
            check=True,
        )
    elif system == "Darwin":
        path = launch_agent_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        program_arguments = "\n".join(f"    <string>{part}</string>" for part in parts)
        path.write_text(
            "\n".join(
                [
                    '<?xml version="1.0" encoding="UTF-8"?>',
                    '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">',
                    '<plist version="1.0">',
                    "<dict>",
                    "  <key>Label</key>",
                    "  <string>com.codex.self-improving-loop</string>",
                    "  <key>ProgramArguments</key>",
                    "  <array>",
                    program_arguments,
                    "  </array>",
                    "  <key>StartCalendarInterval</key>",
                    "  <dict>",
                    "    <key>Hour</key>",
                    f"    <integer>{SCHEDULE_HOUR}</integer>",
                    "    <key>Minute</key>",
                    "    <integer>0</integer>",
                    "  </dict>",
                    "  <key>StandardOutPath</key>",
                    f"  <string>{codex_root / 'self-improving-loop' / 'schedule.log'}</string>",
                    "  <key>StandardErrorPath</key>",
                    f"  <string>{codex_root / 'self-improving-loop' / 'schedule.err.log'}</string>",
                    "</dict>",
                    "</plist>",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        subprocess.run(["launchctl", "unload", str(path)], check=False)
        subprocess.run(["launchctl", "load", str(path)], check=True)
    else:
        user_dir = systemd_user_dir()
        user_dir.mkdir(parents=True, exist_ok=True)
        service = user_dir / "codex-self-improving-loop.service"
        timer = user_dir / "codex-self-improving-loop.timer"
        service.write_text(
            "\n".join(
                [
                    "[Unit]",
                    "Description=Codex Self-Improving Loop daily scan",
                    "",
                    "[Service]",
                    "Type=oneshot",
                    f"ExecStart={display_command(parts)}",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        timer.write_text(
            "\n".join(
                [
                    "[Unit]",
                    f"Description=Run Codex Self-Improving Loop daily scan at {SCHEDULE_TIME}",
                    "",
                    "[Timer]",
                    f"OnCalendar=*-*-* {SCHEDULE_TIME}:00",
                    "Persistent=true",
                    "",
                    "[Install]",
                    "WantedBy=timers.target",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)
        subprocess.run(["systemctl", "--user", "enable", "--now", "codex-self-improving-loop.timer"], check=True)
    return text


def uninstall_schedule(codex_root: Path, dry_run: bool = False) -> str:
    system = platform.system()
    if system == "Windows":
        command = "schtasks.exe /Delete /TN CodexSelfImprovingLoop /F"
        if not dry_run:
            subprocess.run(["schtasks.exe", "/Delete", "/TN", "CodexSelfImprovingLoop", "/F"], check=False)
        return command
    if system == "Darwin":
        path = launch_agent_path()
        if not dry_run:
            subprocess.run(["launchctl", "unload", str(path)], check=False)
            if path.exists():
                path.unlink()
        return f"remove launchd plist {path}"
    user_dir = systemd_user_dir()
    service = user_dir / "codex-self-improving-loop.service"
    timer = user_dir / "codex-self-improving-loop.timer"
    if not dry_run:
        subprocess.run(["systemctl", "--user", "disable", "--now", "codex-self-improving-loop.timer"], check=False)
        for path in (service, timer):
            if path.exists():
                path.unlink()
        subprocess.run(["systemctl", "--user", "daemon-reload"], check=False)
    return f"remove systemd user timer {timer}"


def install_shortcut(repo_root: Path, codex_root: Path, dry_run: bool = False) -> str:
    text = install_shortcut_dry_run(repo_root, codex_root)
    if dry_run:
        return text
    desktop = Path.home() / "Desktop"
    desktop.mkdir(parents=True, exist_ok=True)
    system = platform.system()
    command = shortcut_command(repo_root, codex_root)
    if system == "Windows":
        path = desktop / "Codex Self-Improving Loop.cmd"
        path.write_text("@echo off\r\n" + command + "\r\npause\r\n", encoding="utf-8")
    elif system == "Darwin":
        path = desktop / "Codex Self-Improving Loop.command"
        path.write_text("#!/bin/sh\n" + command + "\n", encoding="utf-8")
        path.chmod(0o755)
    else:
        path = desktop / "codex-self-improving-loop.desktop"
        path.write_text(
            "\n".join(
                [
                    "[Desktop Entry]",
                    "Type=Application",
                    "Name=Codex Self-Improving Loop",
                    f"Exec={command}",
                    "Terminal=true",
                    "",
                ]
            ),
            encoding="utf-8",
        )
    return str(path)


def uninstall_shortcut(dry_run: bool = False) -> str:
    desktop = Path.home() / "Desktop"
    paths = [
        desktop / "Codex Self-Improving Loop.cmd",
        desktop / "Codex Self-Improving Loop.command",
        desktop / "codex-self-improving-loop.desktop",
    ]
    if not dry_run:
        for path in paths:
            if path.exists():
                path.unlink()
    return "remove desktop shortcut"
