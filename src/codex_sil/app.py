"""Local-only HTTP backend for the v2 WebUI."""

from __future__ import annotations

import json
import re
import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
import webbrowser

from .db import connect, init_db
from .exporter import export_candidates, export_digest
from .installer import install_skills
from .paths import html_path
from .promotion import archive_candidate, promote_to_skill, promote_to_skill_patch, promote_to_user_memory, review_candidate
from .scanner import rebuild, scan_once
from .scheduler import install_schedule, install_shortcut, uninstall_schedule, uninstall_shortcut


LOCAL_HOST = "127.0.0.1"


def write_webui(root: Path) -> Path:
    source = Path(__file__).parent / "web" / "index.html"
    target = html_path(root)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    return target


def summary_payload(root: Path) -> dict[str, Any]:
    init_db(root)
    with connect(root) as conn:
        rows = conn.execute("select type, count(*) as count from candidates group by type").fetchall()
        review = conn.execute("select count(*) as count from candidates where status='review'").fetchone()
        candidates = conn.execute(
            "select id, type, destination, text, status from candidates order by updated_at desc, id desc limit 200"
        ).fetchall()
    summary = {"memory": 0, "skill": 0, "skill_patch": 0, "review": int(review["count"])}
    for row in rows:
        summary[str(row["type"])] = int(row["count"])
    return {"summary": summary, "candidates": [dict(row) for row in candidates]}


class SilHandler(BaseHTTPRequestHandler):
    server_version = "CodexSIL/2"

    def _json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _authorized(self) -> bool:
        expected = getattr(self.server, "token", "")
        header = self.headers.get("Authorization", "")
        return header == f"Bearer {expected}"

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            self._json(200, {"ok": True, "host": LOCAL_HOST, "token_required": True})
            return
        if not self._authorized():
            self._json(401, {"error": "token required"})
            return
        if parsed.path == "/api/summary":
            self._json(200, summary_payload(getattr(self.server, "codex_root")))
            return
        if parsed.path in {"/", "/index.html"}:
            body = write_webui(getattr(self.server, "codex_root")).read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self._json(404, {"error": "not found"})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if not self._authorized():
            self._json(401, {"error": "token required"})
            return
        root = getattr(self.server, "codex_root")
        if parsed.path == "/api/init":
            self._json(200, {"database": str(init_db(root)), "webui": str(write_webui(root))})
            return
        if parsed.path == "/api/scan":
            self._json(200, scan_once(root))
            return
        if parsed.path == "/api/rebuild":
            self._json(200, rebuild(root, backup=True))
            return
        repo_root = Path(__file__).resolve().parents[2]
        if parsed.path == "/api/schedule/install":
            self._json(200, {"result": install_schedule(repo_root, root)})
            return
        if parsed.path == "/api/schedule/uninstall":
            self._json(200, {"result": uninstall_schedule(root)})
            return
        if parsed.path == "/api/shortcut/install":
            self._json(200, {"result": install_shortcut(repo_root, root)})
            return
        if parsed.path == "/api/shortcut/uninstall":
            self._json(200, {"result": uninstall_shortcut()})
            return
        if parsed.path == "/api/install/skills":
            self._json(200, install_skills(repo_root, root))
            return
        review_match = re.fullmatch(r"/api/candidates/(\d+)/review", parsed.path)
        archive_match = re.fullmatch(r"/api/candidates/(\d+)/archive", parsed.path)
        promote_match = re.fullmatch(r"/api/candidates/(\d+)/promote", parsed.path)
        if review_match:
            review_candidate(root, int(review_match.group(1)), "reviewed")
            self._json(200, {"ok": True})
            return
        if archive_match:
            archive_candidate(root, int(archive_match.group(1)))
            self._json(200, {"ok": True})
            return
        if promote_match:
            self._json(200, promote_to_user_memory(root, int(promote_match.group(1))))
            return
        skill_match = re.fullmatch(r"/api/candidates/(\d+)/promote-skill", parsed.path)
        patch_match = re.fullmatch(r"/api/candidates/(\d+)/promote-patch", parsed.path)
        reject_match = re.fullmatch(r"/api/candidates/(\d+)/reject", parsed.path)
        if skill_match:
            self._json(200, promote_to_skill(root, int(skill_match.group(1))))
            return
        if patch_match:
            self._json(200, promote_to_skill_patch(root, int(patch_match.group(1))))
            return
        if reject_match:
            review_candidate(root, int(reject_match.group(1)), "rejected")
            self._json(200, {"ok": True})
            return
        if parsed.path == "/api/export/digest":
            self._json(200, {"path": str(export_digest(root))})
            return
        if parsed.path == "/api/export/candidates":
            self._json(200, {"path": str(export_candidates(root))})
            return
        self._json(404, {"error": "not found"})

    def log_message(self, format: str, *args: object) -> None:
        return


def smoke(root: Path) -> dict[str, Any]:
    init_db(root)
    write_webui(root)
    token = secrets.token_urlsafe(18)
    return {"host": LOCAL_HOST, "port": 0, "token_required": True, "token_length": len(token), "webui": str(html_path(root))}


def serve(root: Path, port: int = 8765, open_browser: bool = False) -> int:
    if LOCAL_HOST != "127.0.0.1":
        raise RuntimeError("service host must be 127.0.0.1")
    init_db(root)
    write_webui(root)
    token = secrets.token_urlsafe(24)
    server = ThreadingHTTPServer((LOCAL_HOST, port), SilHandler)
    server.codex_root = root
    server.token = token
    url = f"http://{LOCAL_HOST}:{server.server_port}/?token={token}"
    print(f"Serving Codex Self-Improving Loop on {url}")
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        return 0
    finally:
        server.server_close()
    return 0
