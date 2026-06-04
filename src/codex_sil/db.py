"""SQLite storage for Codex Self-Improving Loop v2."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from . import __version__
from .paths import db_path, ensure_runtime


SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def connect(root: Path | None = None) -> sqlite3.Connection:
    ensure_runtime(root)
    conn = sqlite3.connect(db_path(root))
    conn.row_factory = sqlite3.Row
    conn.execute("pragma foreign_keys = on")
    return conn


def init_db(root: Path | None = None) -> Path:
    ensure_runtime(root)
    path = db_path(root)
    with connect(root) as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        conn.execute(
            "insert into settings(key, value) values('schema_version', ?) "
            "on conflict(key) do update set value=excluded.value, updated_at=current_timestamp",
            (__version__,),
        )
    return path
