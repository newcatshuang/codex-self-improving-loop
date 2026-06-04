"""Runtime path helpers for Codex Self-Improving Loop v2."""

from __future__ import annotations

from pathlib import Path


RUNTIME_DIR_NAME = "self-improving-loop"
DB_NAME = "self-improving-loop.sqlite"
HTML_NAME = "codex-self-improving-loop.html"
LOG_NAME = "self-improving-loop.log"


def default_codex_root() -> Path:
    return Path.home() / ".codex"


def codex_root(value: Path | None = None) -> Path:
    return (value or default_codex_root()).expanduser().resolve()


def runtime_dir(root: Path | None = None) -> Path:
    return codex_root(root) / RUNTIME_DIR_NAME


def db_path(root: Path | None = None) -> Path:
    return runtime_dir(root) / DB_NAME


def html_path(root: Path | None = None) -> Path:
    return runtime_dir(root) / HTML_NAME


def log_path(root: Path | None = None) -> Path:
    return runtime_dir(root) / LOG_NAME


def backups_dir(root: Path | None = None) -> Path:
    return runtime_dir(root) / "backups"


def exports_dir(root: Path | None = None) -> Path:
    return runtime_dir(root) / "exports"


def tmp_dir(root: Path | None = None) -> Path:
    return runtime_dir(root) / "tmp"


def ensure_runtime(root: Path | None = None) -> Path:
    base = runtime_dir(root)
    for directory in (base, backups_dir(root), exports_dir(root), tmp_dir(root), base / "web"):
        directory.mkdir(parents=True, exist_ok=True)
    return base
