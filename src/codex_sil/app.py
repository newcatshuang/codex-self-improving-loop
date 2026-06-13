"""Local-only HTTP backend for the v3 WebUI."""

from __future__ import annotations

import json
import re
import secrets
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse
import webbrowser

from .analysis import analysis_payload, batch_analysis
from . import __version__
from .bundle import export_bundle, import_preview
from .db import connect, init_db
from .digest import latest_digest
from .exporter import export_candidates, export_digest
from .installer import install_skills
from .merge import apply_merge_suggestion, generate_merge_suggestions, merge_suggestions_payload
from .paths import db_path, html_path, runtime_dir
from .promotion import (
    archive_candidate,
    promote_to_project_agents,
    promote_to_skill,
    promote_to_skill_patch,
    promote_to_user_memory,
    promotion_preview,
    review_candidate,
)
from .recall import search as recall_search
from .recommendations import recommend_candidate, recommendations_payload
from .scanner import backup_db, finalize_scan, finish_run, iter_session_files, rebuild, reset_db_for_rebuild, scan_into_run, scan_once, start_run
from .scheduler import install_schedule, install_shortcut, schedule_status, uninstall_schedule, uninstall_shortcut
from .skills import skill_health


LOCAL_HOST = "127.0.0.1"


def _json_group_array_values(value: str | None) -> list[str]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return []
    return [str(item) for item in parsed if item]


def write_webui(root: Path) -> Path:
    web_root = Path(__file__).parent / "web"
    source = web_root / "index.html"
    target = html_path(root)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    runtime_web = runtime_dir(root) / "web"
    runtime_web.mkdir(parents=True, exist_ok=True)
    for name in ("styles.css", "app.js"):
        asset = web_root / name
        if asset.exists():
            (runtime_web / name).write_text(asset.read_text(encoding="utf-8"), encoding="utf-8")
    return target


def doctor_payload(root: Path) -> dict[str, Any]:
    init_db(root)
    return {
        "version": __version__,
        "codex_root": str(root),
        "runtime_dir": str(runtime_dir(root)),
        "database": str(db_path(root)),
        "webui": str(html_path(root)),
        "service_host": LOCAL_HOST,
    }


def setup_status_payload(root: Path) -> dict[str, Any]:
    init_db(root)
    database = db_path(root)
    with connect(root) as conn:
        session_count = int(conn.execute("select count(*) from sessions").fetchone()[0])
        candidate_count = int(conn.execute("select count(*) from candidates").fetchone()[0])
        skill_usage_count = int(conn.execute("select count(*) from skill_usage").fetchone()[0])
    repo_root = Path(__file__).resolve().parents[2]
    schedule = schedule_status(repo_root, root)
    skills_installed = (Path.home() / ".agents" / "skills" / "session-recall" / "SKILL.md").exists() and (
        Path.home() / ".agents" / "skills" / "memory-capture" / "SKILL.md"
    ).exists()
    return {
        "database_exists": database.exists(),
        "session_count": session_count,
        "candidate_count": candidate_count,
        "skill_usage_count": skill_usage_count,
        "schedule_installed": bool(schedule.get("installed")),
        "skills_installed": skills_installed,
        "ready": database.exists() and session_count > 0 and candidate_count > 0,
    }


def summary_payload(root: Path) -> dict[str, Any]:
    init_db(root)
    with connect(root) as conn:
        rows = conn.execute("select type, count(*) as count from candidates group by type").fetchall()
        status_rows = conn.execute("select status, count(*) as count from candidates group by status").fetchall()
        destination_rows = conn.execute("select destination, count(*) as count from candidates group by destination").fetchall()
        analysis_count = conn.execute(
            "select count(*) as count from candidates c join candidate_analyses ca on ca.candidate_id=c.id"
        ).fetchone()["count"]
        pending_analysis = conn.execute(
            "select count(*) as count from candidates c left join candidate_analyses ca on ca.candidate_id=c.id where ca.id is null and c.status='review'"
        ).fetchone()["count"]
        skill_usage_rows = conn.execute("select status, count(*) as count from skill_usage group by status").fetchall()
        skill_usage_by_skill_rows = conn.execute(
            """
            select
              skill_name,
              count(*) as total,
              sum(case when status='success' then 1 else 0 end) as success,
              sum(case when status in ('failed', 'error') then 1 else 0 end) as failed
            from skill_usage
            group by skill_name
            order by total desc, skill_name asc
            limit 20
            """
        ).fetchall()
        candidates = conn.execute(
            """
            select
              c.id,
              c.type,
              c.title,
              c.destination,
              c.text,
              c.rewrite_suggestion,
              c.status,
              c.safety,
              c.confidence,
              c.created_at,
              c.updated_at,
              r.recommendation,
              r.recommendation_reason,
              r.suggested_action,
              ca.risk_level as analysis_risk_level,
              ca.recommended_next_step as analysis_next_step,
              ep.target_type as proposal_target_type,
              ep.requires_manual_approval as proposal_requires_manual_approval,
              count(distinct cs.session_id) as source_count,
              json_group_array(distinct s.rel_path) as source_files
            from candidates c
            left join candidate_sources cs on cs.candidate_id=c.id
            left join sessions s on s.id=cs.session_id
            left join recommendations r on r.candidate_id=c.id
            left join candidate_analyses ca on ca.candidate_id=c.id
            left join evolution_proposals ep on ep.candidate_id=c.id
            group by c.id
            order by c.updated_at desc, c.id desc
            limit 200
            """
        ).fetchall()
    status_counts = {str(row["status"]): int(row["count"]) for row in status_rows}
    destination_counts = {str(row["destination"]): int(row["count"]) for row in destination_rows}
    skill_usage_counts = {str(row["status"]): int(row["count"]) for row in skill_usage_rows}
    skill_usage_by_skill = [
        {
            "skill_name": str(row["skill_name"]),
            "total": int(row["total"] or 0),
            "success": int(row["success"] or 0),
            "failed": int(row["failed"] or 0),
        }
        for row in skill_usage_by_skill_rows
    ]
    summary = {
        "memory": 0,
        "skill": 0,
        "skill_patch": 0,
        "review": status_counts.get("review", 0),
        "blocked": status_counts.get("blocked", 0),
        "promoted": status_counts.get("promoted", 0),
        "rejected": status_counts.get("rejected", 0),
        "archived": status_counts.get("archived", 0),
        "skill_usage_total": sum(skill_usage_counts.values()),
        "skill_usage_success": skill_usage_counts.get("success", 0),
        "skill_usage_failed": skill_usage_counts.get("failed", 0) + skill_usage_counts.get("error", 0),
        "by_status": status_counts,
        "by_destination": destination_counts,
        "skill_usage_by_status": skill_usage_counts,
        "skill_usage_by_skill": skill_usage_by_skill,
        "analysis_count": analysis_count,
        "pending_analysis": pending_analysis,
    }
    for row in rows:
        summary[str(row["type"])] = int(row["count"])
    candidate_items = []
    for row in candidates:
        item = dict(row)
        item["source_files"] = _json_group_array_values(item.get("source_files"))[:5]
        candidate_items.append(item)
    return {"summary": summary, "candidates": candidate_items}


def run_status_payload(root: Path, run_id: int) -> dict[str, Any]:
    init_db(root)
    with connect(root) as conn:
        run = conn.execute("select * from runs where id=?", (run_id,)).fetchone()
        if not run:
            return {"error": "run not found"}
        total = conn.execute(
            "select count(*) as count from run_steps where run_id=? and name in ('session_processed', 'session_skipped')",
            (run_id,),
        ).fetchone()["count"]
        processed = conn.execute(
            "select count(*) as count from run_steps where run_id=? and name='session_processed'",
            (run_id,),
        ).fetchone()["count"]
        skipped = conn.execute(
            "select count(*) as count from run_steps where run_id=? and name='session_skipped'",
            (run_id,),
        ).fetchone()["count"]
        latest = conn.execute(
            "select name, status, detail, finished_at from run_steps where run_id=? order by id desc limit 1",
            (run_id,),
        ).fetchone()
    return {
        "run_id": int(run["id"]),
        "kind": str(run["kind"]),
        "status": str(run["status"]),
        "started_at": str(run["started_at"]),
        "finished_at": str(run["finished_at"] or ""),
        "detail": str(run["detail"] or ""),
        "processed": int(processed),
        "skipped": int(skipped),
        "total": int(total),
        "latest_step": dict(latest) if latest else None,
    }


def runs_payload(root: Path) -> dict[str, Any]:
    init_db(root)
    with connect(root) as conn:
        runs = [dict(row) for row in conn.execute("select * from runs order by id desc limit 25")]
        steps = [
            dict(row)
            for row in conn.execute(
                """
                select rs.*
                from run_steps rs
                join runs r on r.id=rs.run_id
                order by rs.id desc
                limit 80
                """
            )
        ]
    return {"runs": runs, "steps": steps}


def audit_payload(root: Path) -> dict[str, Any]:
    init_db(root)
    with connect(root) as conn:
        rows = [
            dict(row)
            for row in conn.execute(
                "select id, action, target, detail, created_at from audit_log order by id desc limit 200"
            )
        ]
    return {"audit": rows}


def history_payload(root: Path) -> dict[str, Any]:
    init_db(root)
    with connect(root) as conn:
        promotions = [
            dict(row)
            for row in conn.execute(
                """
                select
                  p.id,
                  p.candidate_id,
                  p.target_type,
                  p.target_path,
                  p.backup_path,
                  p.status,
                  p.detail,
                  p.created_at,
                  c.type as candidate_type,
                  c.title as candidate_title
                from promotions p
                left join candidates c on c.id=p.candidate_id
                order by p.id desc
                limit 200
                """
            )
        ]
        reviews = [
            dict(row)
            for row in conn.execute(
                """
                select
                  r.id,
                  r.candidate_id,
                  r.status,
                  r.note,
                  r.rewrite_text,
                  r.created_at,
                  c.type as candidate_type,
                  c.destination,
                  c.title as candidate_title
                from reviews r
                left join candidates c on c.id=r.candidate_id
                order by r.id desc
                limit 200
                """
            )
        ]
    return {"promotions": promotions, "reviews": reviews}


def rollback_preview_payload(root: Path, promotion_id: int) -> dict[str, Any]:
    init_db(root)
    with connect(root) as conn:
        row = conn.execute("select * from promotions where id=?", (promotion_id,)).fetchone()
    if row is None:
        return {"error": "promotion not found"}
    promotion = dict(row)
    backup = Path(str(promotion.get("backup_path") or ""))
    target = Path(str(promotion.get("target_path") or ""))
    can_restore = bool(str(promotion.get("backup_path") or "").strip()) and backup.exists()
    script = f"import shutil; shutil.copy2({json.dumps(str(backup))}, {json.dumps(str(target))})"
    return {
        "promotion": promotion,
        "can_restore": can_restore,
        "backup_path": str(backup) if promotion.get("backup_path") else "",
        "target_path": str(target) if promotion.get("target_path") else "",
        "restore_command": f"python -c {json.dumps(script)}",
        "restore_script": script,
    }


def run_rebuild_background(root: Path, run_id: int, backup_path: Path | None) -> None:
    try:
        reset_db_for_rebuild(root, keep_run_id=run_id)
        sessions = iter_session_files(root)
        result = scan_into_run(root, run_id, sessions)
        finalize_scan(root, run_id)
        detail = f"sessions={result['sessions']} candidates={result['candidates']}"
        if backup_path:
            detail += f" backup={backup_path}"
        finish_run(root, run_id, "ok", detail)
    except Exception as exc:
        finish_run(root, run_id, "failed", str(exc))


def start_background_rebuild(root: Path) -> dict[str, Any]:
    init_db(root)
    backup_path = backup_db(root)
    run_id = start_run(root, "rebuild", f"backup={backup_path}" if backup_path else None)
    worker = threading.Thread(target=run_rebuild_background, args=(root, run_id, backup_path), daemon=True)
    worker.start()
    return {"async": True, "run_id": run_id, "status": "running", "backup": str(backup_path) if backup_path else None}


class SilHandler(BaseHTTPRequestHandler):
    server_version = "CodexSIL/2"

    def _json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        if not raw:
            return {}
        try:
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return {}
        return payload if isinstance(payload, dict) else {}

    def _authorized(self) -> bool:
        expected = getattr(self.server, "token", "")
        header = self.headers.get("Authorization", "")
        return secrets.compare_digest(header, f"Bearer {expected}")

    def _query_authorized(self) -> bool:
        expected = getattr(self.server, "token", "")
        parsed = urlparse(self.path)
        token = parse_qs(parsed.query).get("token", [""])[0]
        return secrets.compare_digest(token, expected)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            self._json(200, {"ok": True, "host": LOCAL_HOST, "token_required": True})
            return
        if parsed.path == "/api/summary":
            if not self._authorized():
                self._json(401, {"error": "token required"})
                return
            self._json(200, summary_payload(getattr(self.server, "codex_root")))
            return
        if parsed.path == "/api/setup/status":
            if not self._authorized():
                self._json(401, {"error": "token required"})
                return
            self._json(200, setup_status_payload(getattr(self.server, "codex_root")))
            return
        if parsed.path == "/api/doctor":
            if not self._authorized():
                self._json(401, {"error": "token required"})
                return
            self._json(200, doctor_payload(getattr(self.server, "codex_root")))
            return
        if parsed.path == "/api/runs":
            if not self._authorized():
                self._json(401, {"error": "token required"})
                return
            self._json(200, runs_payload(getattr(self.server, "codex_root")))
            return
        if parsed.path == "/api/schedule/status":
            if not self._authorized():
                self._json(401, {"error": "token required"})
                return
            root = getattr(self.server, "codex_root")
            repo_root = Path(__file__).resolve().parents[2]
            self._json(200, schedule_status(repo_root, root))
            return
        if parsed.path == "/api/audit":
            if not self._authorized():
                self._json(401, {"error": "token required"})
                return
            self._json(200, audit_payload(getattr(self.server, "codex_root")))
            return
        if parsed.path == "/api/history":
            if not self._authorized():
                self._json(401, {"error": "token required"})
                return
            self._json(200, history_payload(getattr(self.server, "codex_root")))
            return
        if parsed.path == "/api/recommendations":
            if not self._authorized():
                self._json(401, {"error": "token required"})
                return
            self._json(200, recommendations_payload(getattr(self.server, "codex_root")))
            return
        if parsed.path == "/api/merge-suggestions":
            if not self._authorized():
                self._json(401, {"error": "token required"})
                return
            self._json(200, merge_suggestions_payload(getattr(self.server, "codex_root")))
            return
        if parsed.path == "/api/digests/latest":
            if not self._authorized():
                self._json(401, {"error": "token required"})
                return
            self._json(200, latest_digest(getattr(self.server, "codex_root")))
            return
        if parsed.path == "/api/skills/health":
            if not self._authorized():
                self._json(401, {"error": "token required"})
                return
            self._json(200, skill_health(getattr(self.server, "codex_root")))
            return
        run_match = re.fullmatch(r"/api/runs/(\d+)", parsed.path)
        if run_match:
            if not self._authorized():
                self._json(401, {"error": "token required"})
                return
            payload = run_status_payload(getattr(self.server, "codex_root"), int(run_match.group(1)))
            self._json(404 if "error" in payload else 200, payload)
            return
        rollback_match = re.fullmatch(r"/api/promotions/(\d+)/rollback-preview", parsed.path)
        if rollback_match:
            if not self._authorized():
                self._json(401, {"error": "token required"})
                return
            payload = rollback_preview_payload(getattr(self.server, "codex_root"), int(rollback_match.group(1)))
            self._json(404 if "error" in payload else 200, payload)
            return
        preview_match = re.fullmatch(r"/api/candidates/(\d+)/promotion-preview", parsed.path)
        if preview_match:
            if not self._authorized():
                self._json(401, {"error": "token required"})
                return
            query_params = parse_qs(parsed.query)
            target = query_params.get("target", ["user"])[0]
            try:
                payload = promotion_preview(getattr(self.server, "codex_root"), int(preview_match.group(1)), target)
            except ValueError as exc:
                self._json(404, {"error": str(exc)})
                return
            self._json(200, payload)
            return
        analysis_match = re.fullmatch(r"/api/candidates/(\d+)/analysis", parsed.path)
        if analysis_match:
            if not self._authorized():
                self._json(401, {"error": "token required"})
                return
            try:
                payload = analysis_payload(getattr(self.server, "codex_root"), int(analysis_match.group(1)))
            except ValueError as exc:
                self._json(404, {"error": str(exc)})
                return
            self._json(200, payload)
            return
        if parsed.path == "/api/recall":
            if not self._authorized():
                self._json(401, {"error": "token required"})
                return
            query_params = parse_qs(parsed.query)
            query = query_params.get("q", [""])[0].strip()
            try:
                max_results = max(1, min(50, int(query_params.get("max_results", ["10"])[0])))
            except ValueError:
                max_results = 10
            self._json(
                200,
                recall_search(getattr(self.server, "codex_root"), query, max_results=max_results)
                if query
                else {"query": query, "results": []},
            )
            return
        if parsed.path in {"/", "/index.html"}:
            if not (self._authorized() or self._query_authorized()):
                self._json(401, {"error": "token required"})
                return
            body = write_webui(getattr(self.server, "codex_root")).read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if parsed.path in {"/styles.css", "/app.js"}:
            asset_name = parsed.path.lstrip("/")
            asset = Path(__file__).parent / "web" / asset_name
            if not asset.exists():
                self._json(404, {"error": "not found"})
                return
            body = asset.read_bytes()
            content_type = "text/css; charset=utf-8" if asset_name.endswith(".css") else "application/javascript; charset=utf-8"
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
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
        if parsed.path == "/api/scan-and-analyze":
            result = scan_once(root)
            batch_result = batch_analysis(root)
            merge_result = {}
            try:
                from .merge import generate_merge_suggestions
                merge_result = generate_merge_suggestions(root)
            except Exception:
                pass
            self._json(200, {"scan": result, "analysis": batch_result, "merge": merge_result})
            return
        if parsed.path == "/api/rebuild":
            self._json(200, start_background_rebuild(root))
            return
        if parsed.path == "/api/backup":
            backup = backup_db(root)
            self._json(200, {"backup": str(backup) if backup else None})
            return
        if parsed.path == "/api/analyze/batch":
            self._json(200, batch_analysis(root))
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
        recommend_match = re.fullmatch(r"/api/candidates/(\d+)/recommend", parsed.path)
        if recommend_match:
            try:
                self._json(200, recommend_candidate(root, int(recommend_match.group(1))))
            except ValueError as exc:
                self._json(404, {"error": str(exc)})
            return
        merge_apply_match = re.fullmatch(r"/api/merge-suggestions/(\d+)/apply", parsed.path)
        if parsed.path == "/api/merge-suggestions/refresh":
            self._json(200, generate_merge_suggestions(root))
            return
        if merge_apply_match:
            try:
                self._json(200, apply_merge_suggestion(root, int(merge_apply_match.group(1))))
            except ValueError as exc:
                self._json(404, {"error": str(exc)})
            return
        review_match = re.fullmatch(r"/api/candidates/(\d+)/review", parsed.path)
        archive_match = re.fullmatch(r"/api/candidates/(\d+)/archive", parsed.path)
        promote_match = re.fullmatch(r"/api/candidates/(\d+)/promote", parsed.path)
        if review_match:
            payload = self._read_json_body()
            status = str(payload.get("status") or "reviewed")
            note = payload.get("note")
            rewrite_text = payload.get("rewrite_text")
            review_candidate(
                root,
                int(review_match.group(1)),
                status,
                note=str(note) if note is not None else None,
                rewrite_text=str(rewrite_text) if rewrite_text is not None else None,
            )
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
        agents_match = re.fullmatch(r"/api/candidates/(\d+)/promote-agents", parsed.path)
        reject_match = re.fullmatch(r"/api/candidates/(\d+)/reject", parsed.path)
        if skill_match:
            self._json(200, promote_to_skill(root, int(skill_match.group(1))))
            return
        if patch_match:
            self._json(200, promote_to_skill_patch(root, int(patch_match.group(1))))
            return
        if agents_match:
            self._json(200, promote_to_project_agents(root, int(agents_match.group(1))))
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
        if parsed.path == "/api/export/bundle":
            self._json(200, {"path": str(export_bundle(root))})
            return
        if parsed.path == "/api/import/preview":
            payload = self._read_json_body()
            path = Path(str(payload.get("path") or ""))
            self._json(200, import_preview(path, root))
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
