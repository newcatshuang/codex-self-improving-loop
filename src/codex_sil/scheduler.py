"""Cross-platform schedule and shortcut command generation."""

from __future__ import annotations

import platform
import subprocess
import sys
from pathlib import Path


def sil_command(repo_root: Path, *args: str) -> list[str]:
    return [sys.executable, str(repo_root / "sil.py"), *args]


def display_command(parts: list[str]) -> str:
    return " ".join(f'"{part}"' if " " in part else part for part in parts)


def windows_task_command(parts: list[str]) -> str:
    return subprocess.list2cmdline(parts)


def schedule_command(repo_root: Path, codex_root: Path) -> str:
    return display_command(sil_command(repo_root, "scan", "--once", "--codex-root", str(codex_root)))


def shortcut_command(repo_root: Path, codex_root: Path) -> str:
    return display_command(sil_command(repo_root, "serve", "--open", "--codex-root", str(codex_root)))


def install_schedule_dry_run(repo_root: Path, codex_root: Path) -> str:
    system = platform.system()
    parts = sil_command(repo_root, "scan", "--once", "--codex-root", str(codex_root))
    command = windows_task_command(parts) if system == "Windows" else schedule_command(repo_root, codex_root)
    if system == "Windows":
        return f"schtasks.exe /Create /TN CodexSelfImprovingLoop /SC DAILY /ST 12:00 /TR {command} /F"
    if system == "Darwin":
        return f"launchd daily 12:00 -> {command}"
    return f"systemd user timer daily 12:00 -> {command}"


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
                "12:00",
                "/TR",
                command,
                "/F",
            ],
            check=True,
        )
    else:
        # Non-Windows installation is intentionally file-based for portability in v2.
        path = codex_root / "self-improving-loop" / "schedule-command.txt"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n", encoding="utf-8")
    return text


def uninstall_schedule(codex_root: Path, dry_run: bool = False) -> str:
    system = platform.system()
    if system == "Windows":
        command = "schtasks.exe /Delete /TN CodexSelfImprovingLoop /F"
        if not dry_run:
            subprocess.run(["schtasks.exe", "/Delete", "/TN", "CodexSelfImprovingLoop", "/F"], check=False)
        return command
    path = codex_root / "self-improving-loop" / "schedule-command.txt"
    if not dry_run and path.exists():
        path.unlink()
    return f"remove {path}"


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
