#!/usr/bin/env python3
"""Verify the v2 SQLite + local WebUI control-plane core."""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import subprocess
import sys
import threading
import urllib.request
from pathlib import Path


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["CODEX_SIL_DISABLE_CODEX"] = "1"
    return subprocess.run(command, cwd=cwd, env=env, check=True, text=True, encoding="utf-8", errors="replace", capture_output=True)


def write_session(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                '{"type":"message","role":"user","content":"请记住：SQL 查询必须先确认字段，避免 SELECT *。"}',
                '{"type":"message","role":"assistant","content":"已完成验证，并发现可以沉淀为数据库查询偏好。"}',
                '{"type":"message","role":"user","content":"这个流程可以做成 skill：先跑 doctor，再 rebuild，再 scan --once。"}',
                '{"type":"message","role":"assistant","content":"记录为可复用工作流，并建议补充 memory-capture skill。"}',
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def table_count(db_path: Path, table: str) -> int:
    with sqlite3.connect(db_path) as conn:
        return int(conn.execute(f"select count(*) from {table}").fetchone()[0])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--work-root", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    root = args.work_root.resolve()
    sil = repo / "sil.py"
    runtime = root / "self-improving-loop"
    db_path = runtime / "self-improving-loop.sqlite"
    html_path = runtime / "codex-self-improving-loop.html"

    if not sil.exists():
        raise FileNotFoundError(sil)

    write_session(root / "sessions" / "2026" / "06" / "04" / "session-v2.jsonl")

    doctor = run([sys.executable, str(sil), "doctor", "--codex-root", str(root), "--json"], repo)
    doctor_payload = json.loads(doctor.stdout)
    if doctor_payload["runtime_dir"] != str(runtime):
        raise AssertionError(f"doctor should use unified runtime dir: {doctor_payload}")
    if doctor_payload["service_host"] != "127.0.0.1":
        raise AssertionError("local service must be restricted to 127.0.0.1")

    run([sys.executable, str(sil), "init", "--codex-root", str(root)], repo)
    if not db_path.exists():
        raise FileNotFoundError(db_path)

    run([sys.executable, str(sil), "rebuild", "--codex-root", str(root), "--backup"], repo)
    if table_count(db_path, "sessions") != 1:
        raise AssertionError("rebuild should register historical sessions")
    if table_count(db_path, "candidates") < 2:
        raise AssertionError("rebuild should extract memory and skill candidates into SQLite")
    if table_count(db_path, "runs") < 1 or table_count(db_path, "run_steps") < 1:
        raise AssertionError("rebuild should record runs and run steps")

    before = table_count(db_path, "candidates")
    run([sys.executable, str(sil), "scan", "--codex-root", str(root), "--once"], repo)
    after = table_count(db_path, "candidates")
    if after != before:
        raise AssertionError("scan should be idempotent for already processed sessions")

    serve_smoke = run([sys.executable, str(sil), "serve", "--codex-root", str(root), "--smoke-test"], repo)
    smoke_payload = json.loads(serve_smoke.stdout)
    if smoke_payload["host"] != "127.0.0.1" or not smoke_payload["token_required"]:
        raise AssertionError(f"serve smoke should enforce local token auth: {smoke_payload}")
    if not html_path.exists():
        raise FileNotFoundError(html_path)
    sys.path.insert(0, str(repo / "src"))
    from codex_sil.app import LOCAL_HOST, SilHandler
    from http.server import ThreadingHTTPServer

    server = ThreadingHTTPServer((LOCAL_HOST, 0), SilHandler)
    server.codex_root = root
    server.token = "test-token"
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with urllib.request.urlopen(f"http://{LOCAL_HOST}:{server.server_port}/?token=test-token", timeout=5) as response:
            page = response.read().decode("utf-8")
        if "Codex Self-Improving Loop" not in page:
            raise AssertionError("tokenized WebUI landing URL should return HTML")
        request = urllib.request.Request(
            f"http://{LOCAL_HOST}:{server.server_port}/api/summary",
            headers={"Authorization": "Bearer test-token"},
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            summary_api = json.loads(response.read().decode("utf-8"))
        if summary_api["candidates"]:
            candidate_keys = set(summary_api["candidates"][0])
            required_detail_keys = {
                "id",
                "type",
                "title",
                "destination",
                "text",
                "rewrite_suggestion",
                "status",
                "safety",
                "confidence",
                "created_at",
                "updated_at",
                "source_count",
                "source_files",
            }
            if not required_detail_keys.issubset(candidate_keys):
                raise AssertionError(f"summary API should expose detail panel fields: {candidate_keys}")
        summary_keys = set(summary_api["summary"])
        required_summary_keys = {"memory", "skill", "skill_patch", "review", "blocked", "promoted", "rejected", "archived", "skill_usage_total", "skill_usage_success", "skill_usage_failed"}
        if not required_summary_keys.issubset(summary_keys):
            raise AssertionError(f"summary API should expose dashboard metrics: {summary_keys}")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    html = html_path.read_text(encoding="utf-8")
    for expected in (
        "Codex Self-Improving Loop",
        "Candidate Center",
        "候选中心",
        "Schedule Center",
        "调度中心",
        "Skill Usage",
        "技能使用",
        "Status Summary",
        "状态统计",
        "Rebuild Database",
        "重建数据库",
        "clear active data, and rescan all historical sessions",
        "清空当前数据并全量重扫历史会话",
        "navigator.language",
        "localStorage",
        "languageToggle",
        "data-i18n",
        "statusToast",
        "selectedTitle",
        "selectedText",
        "selectedRewrite",
        "selectedMeta",
        "createdAtHeader",
        "updatedAtHeader",
        "createdAtFilter",
        "statusFilter",
        "detailActions",
        "initializeData",
        "installSchedule",
        "installShortcut",
        "installSkills",
        "exportDigest",
        "promoteSkill",
        "promotePatch",
        "/api/init",
        "/api/schedule/install",
        "/api/shortcut/install",
        "/api/install/skills",
        "/api/export/digest",
        "/api/rebuild",
        "/api/candidates/${window.selectedCandidateId}/promote-skill",
    ):
        if expected not in html:
            raise AssertionError(f"WebUI missing {expected}")
    if "promotion-panel" in html or 'data-i18n="promotionCenter"' in html:
        raise AssertionError("promotion actions should live inside selected record details, not a separate promotion panel")

    schedule = run([sys.executable, str(sil), "schedule", "install", "--codex-root", str(root), "--dry-run"], repo)
    if "sil.py scan --once" not in schedule.stdout:
        raise AssertionError("schedule dry-run should invoke sil.py scan --once")

    shortcut = run([sys.executable, str(sil), "shortcut", "install", "--codex-root", str(root), "--dry-run"], repo)
    if "sil.py serve --open" not in shortcut.stdout:
        raise AssertionError("shortcut dry-run should launch sil.py serve --open")

    print("verify-v2-core passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
