"""Shared verification helpers for script-style tests."""

from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
import threading
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any


def run_sil(repo: Path, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["CODEX_SIL_DISABLE_CODEX"] = "1"
    return subprocess.run(
        [sys.executable, str(repo / "sil.py"), *args, "--codex-root", str(root)],
        cwd=repo,
        env=env,
        check=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )


def write_jsonl_session(path: Path, messages: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(item, ensure_ascii=False) for item in messages) + "\n", encoding="utf-8")


def table_count(db_path: Path, table: str) -> int:
    with sqlite3.connect(db_path) as conn:
        return int(conn.execute(f"select count(*) from {table}").fetchone()[0])


def fetch_json(port: int, token: str, path: str, method: str = "GET", payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        f"http://127.0.0.1:{port}{path}",
        data=data,
        method=method,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


class TestServer:
    def __init__(self, repo: Path, root: Path, token: str = "test-token") -> None:
        sys.path.insert(0, str(repo / "src"))
        from codex_sil.app import LOCAL_HOST, SilHandler

        self.server = ThreadingHTTPServer((LOCAL_HOST, 0), SilHandler)
        self.server.codex_root = root
        self.server.token = token
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.token = token

    @property
    def port(self) -> int:
        return int(self.server.server_port)

    def __enter__(self) -> "TestServer":
        self.thread.start()
        return self

    def __exit__(self, *_: object) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)
