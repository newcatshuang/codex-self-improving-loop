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
import time
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
                '{"type":"message","role":"user","content":"$grill-me 我想优化整体流程和输出。路径里有 $HOME，不应该当成 skill。"}',
                '{"type":"message","role":"user","content":"代码变量 $i 和 $entry 只是普通文本，不是用户指定的 skill。"}',
                '{"type":"message","role":"user","content":"$entry=@\\"code\\" 是脚本变量赋值，不是 skill。"}',
                '{"type":"message","role":"user","content":"$imagegen 生成一张项目配图。"}',
                '{"type":"message","role":"assistant","content":"Using `using-superpowers / brainstorming` to clarify the workflow before implementation."}',
                '{"type":"message","role":"assistant","content":"我会用 `verification-before-completion` 来做完成前校验。"}',
                '{"type":"message","role":"assistant","content":"Using `python` to run the verifier should not be counted as skill usage."}',
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


def skill_usage_names(db_path: Path) -> set[str]:
    with sqlite3.connect(db_path) as conn:
        return {str(row[0]) for row in conn.execute("select skill_name from skill_usage")}


def main() -> int:
    os.environ["CODEX_SIL_DISABLE_CODEX"] = "1"
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
    expected_skill_usage = {"grill-me", "imagegen", "using-superpowers", "brainstorming", "verification-before-completion"}
    actual_skill_usage = skill_usage_names(db_path)
    if not expected_skill_usage.issubset(actual_skill_usage):
        raise AssertionError(f"rebuild should record explicit skill usage: {actual_skill_usage}")
    if "home" in actual_skill_usage:
        raise AssertionError("$HOME should be treated as environment text, not skill usage")
    if {"i", "entry"} & actual_skill_usage:
        raise AssertionError("ordinary dollar-prefixed variables should not be counted as skill usage")
    if "python" in actual_skill_usage:
        raise AssertionError("generic tools inside assistant messages should not be counted as skill usage")

    before = table_count(db_path, "candidates")
    before_skill_usage = table_count(db_path, "skill_usage")
    run([sys.executable, str(sil), "scan", "--codex-root", str(root), "--once"], repo)
    after = table_count(db_path, "candidates")
    if after != before:
        raise AssertionError("scan should be idempotent for already processed sessions")
    after_skill_usage = table_count(db_path, "skill_usage")
    if after_skill_usage != before_skill_usage:
        raise AssertionError("scan should not duplicate skill usage for already processed sessions")

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
        held_connection = sqlite3.connect(db_path)
        try:
            held_connection.execute("select count(*) from sessions").fetchone()
            rebuild_request = urllib.request.Request(
                f"http://{LOCAL_HOST}:{server.server_port}/api/rebuild",
                method="POST",
                headers={"Authorization": "Bearer test-token"},
            )
            with urllib.request.urlopen(rebuild_request, timeout=15) as response:
                rebuild_api = json.loads(response.read().decode("utf-8"))
            if not rebuild_api.get("async") or not rebuild_api.get("run_id"):
                raise AssertionError(f"WebUI rebuild should start an async tracked run: {rebuild_api}")
            status_request = urllib.request.Request(
                f"http://{LOCAL_HOST}:{server.server_port}/api/runs/{rebuild_api['run_id']}",
                headers={"Authorization": "Bearer test-token"},
            )
            run_status = {}
            deadline = time.time() + 15
            while time.time() < deadline:
                with urllib.request.urlopen(status_request, timeout=5) as response:
                    run_status = json.loads(response.read().decode("utf-8"))
                if run_status["status"] != "running":
                    break
                time.sleep(0.2)
            if run_status["status"] != "ok" or run_status["processed"] != 1 or run_status["total"] != 1:
                raise AssertionError(f"WebUI rebuild progress should report completion: {run_status}")
            if table_count(db_path, "sessions") != 1:
                raise AssertionError(f"WebUI rebuild should rescan sessions while SQLite is open: {rebuild_api}")
        finally:
            held_connection.close()
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
        required_summary_keys = {
            "memory",
            "skill",
            "skill_patch",
            "review",
            "blocked",
            "promoted",
            "rejected",
            "archived",
            "skill_usage_total",
            "skill_usage_success",
            "skill_usage_failed",
            "skill_usage_by_skill",
        }
        if not required_summary_keys.issubset(summary_keys):
            raise AssertionError(f"summary API should expose dashboard metrics: {summary_keys}")
        summary_usage_names = {item["skill_name"] for item in summary_api["summary"]["skill_usage_by_skill"]}
        if not expected_skill_usage.issubset(summary_usage_names):
            raise AssertionError(f"summary API should expose recorded skill usage: {summary_usage_names}")
        request = urllib.request.Request(
            f"http://{LOCAL_HOST}:{server.server_port}/api/runs",
            headers={"Authorization": "Bearer test-token"},
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            runs_api = json.loads(response.read().decode("utf-8"))
        if not runs_api.get("runs") or "steps" not in runs_api:
            raise AssertionError(f"runs API should expose recent runs and steps: {runs_api}")
        request = urllib.request.Request(
            f"http://{LOCAL_HOST}:{server.server_port}/api/schedule/status",
            headers={"Authorization": "Bearer test-token"},
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            schedule_api = json.loads(response.read().decode("utf-8"))
        if schedule_api.get("schedule_time") != "03:00" or "scan --once" not in schedule_api.get("command", ""):
            raise AssertionError(f"schedule status API should expose the daily scan target: {schedule_api}")
        request = urllib.request.Request(
            f"http://{LOCAL_HOST}:{server.server_port}/api/doctor",
            headers={"Authorization": "Bearer test-token"},
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            doctor_api = json.loads(response.read().decode("utf-8"))
        if doctor_api["service_host"] != "127.0.0.1" or not doctor_api["database"].endswith("self-improving-loop.sqlite"):
            raise AssertionError(f"doctor API should expose runtime diagnostics: {doctor_api}")
        request = urllib.request.Request(
            f"http://{LOCAL_HOST}:{server.server_port}/api/recall?q=SQL&max_results=3",
            headers={"Authorization": "Bearer test-token"},
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            recall_api = json.loads(response.read().decode("utf-8"))
        if recall_api["query"] != "SQL" or not recall_api["results"]:
            raise AssertionError(f"recall API should search sessions and candidates: {recall_api}")
        if len(recall_api["results"]) > 3:
            raise AssertionError(f"recall API should honor max_results: {recall_api}")
        review_request = urllib.request.Request(
            f"http://{LOCAL_HOST}:{server.server_port}/api/candidates/{summary_api['candidates'][0]['id']}/review",
            method="POST",
            data=json.dumps({"status": "reviewed", "note": "checked", "rewrite_text": "Reviewed rewrite"}).encode("utf-8"),
            headers={"Authorization": "Bearer test-token", "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(review_request, timeout=5) as response:
            review_api = json.loads(response.read().decode("utf-8"))
        if not review_api.get("ok"):
            raise AssertionError(f"review API should accept note and rewrite text: {review_api}")
        with sqlite3.connect(db_path) as conn:
            stored_review = conn.execute("select status, note, rewrite_text from reviews order by id desc limit 1").fetchone()
        if tuple(stored_review) != ("reviewed", "checked", "Reviewed rewrite"):
            raise AssertionError(f"review note/rewrite should be stored: {stored_review}")
        backup_request = urllib.request.Request(
            f"http://{LOCAL_HOST}:{server.server_port}/api/backup",
            method="POST",
            headers={"Authorization": "Bearer test-token"},
        )
        with urllib.request.urlopen(backup_request, timeout=5) as response:
            backup_api = json.loads(response.read().decode("utf-8"))
        if not backup_api.get("backup"):
            raise AssertionError(f"backup API should create a backup path: {backup_api}")
        (root / "AGENTS.md").write_text("# AGENTS.md\n\n## Project Learned Facts\n", encoding="utf-8")
        promote_agents_request = urllib.request.Request(
            f"http://{LOCAL_HOST}:{server.server_port}/api/candidates/{summary_api['candidates'][0]['id']}/promote-agents",
            method="POST",
            headers={"Authorization": "Bearer test-token"},
        )
        with urllib.request.urlopen(promote_agents_request, timeout=5) as response:
            agents_api = json.loads(response.read().decode("utf-8"))
        if agents_api["status"] != "ok" or not agents_api["target_path"].endswith("AGENTS.md"):
            raise AssertionError(f"project AGENTS promotion should be available: {agents_api}")
        if not agents_api.get("backup_path") or not Path(agents_api["backup_path"]).exists():
            raise AssertionError(f"project AGENTS promotion should create a restorable backup: {agents_api}")
        request = urllib.request.Request(
            f"http://{LOCAL_HOST}:{server.server_port}/api/audit",
            headers={"Authorization": "Bearer test-token"},
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            audit_api = json.loads(response.read().decode("utf-8"))
        audit_actions = {item["action"] for item in audit_api.get("audit", [])}
        if {"review_candidate", "promote_project_agents"} - audit_actions:
            raise AssertionError(f"audit API should expose review and promotion actions: {audit_api}")
        request = urllib.request.Request(
            f"http://{LOCAL_HOST}:{server.server_port}/api/history",
            headers={"Authorization": "Bearer test-token"},
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            history_api = json.loads(response.read().decode("utf-8"))
        if not history_api.get("promotions") or not history_api.get("reviews"):
            raise AssertionError(f"history API should expose promotions and reviews: {history_api}")
        if not any(item.get("target_type") == "AGENTS.md" for item in history_api["promotions"]):
            raise AssertionError(f"history API should include project AGENTS promotions: {history_api}")
        if not any(item.get("note") == "checked" and item.get("rewrite_text") == "Reviewed rewrite" for item in history_api["reviews"]):
            raise AssertionError(f"history API should preserve review note and rewrite text: {history_api}")
        promotion_id = next(item["id"] for item in history_api["promotions"] if item.get("target_type") == "AGENTS.md")
        request = urllib.request.Request(
            f"http://{LOCAL_HOST}:{server.server_port}/api/promotions/{promotion_id}/rollback-preview",
            headers={"Authorization": "Bearer test-token"},
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            rollback_api = json.loads(response.read().decode("utf-8"))
        if not rollback_api.get("can_restore") or not rollback_api.get("backup_path") or not rollback_api.get("target_path"):
            raise AssertionError(f"rollback preview should expose restorable paths: {rollback_api}")
        if "shutil.copy2" not in rollback_api.get("restore_command", ""):
            raise AssertionError(f"rollback preview should provide a copy-safe Python restore command: {rollback_api}")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    html = html_path.read_text(encoding="utf-8")
    runtime_web = runtime / "web"
    for asset in ("styles.css", "app.js"):
        asset_path = runtime_web / asset
        if asset_path.exists():
            html += "\n" + asset_path.read_text(encoding="utf-8")
    for expected in (
        "Codex Self-Improving Loop",
        "appShell",
        "sideNav",
        "tab-dashboard",
        "tab-workflow",
        "tab-operations",
        "data-view=\"dashboard\"",
        "data-view=\"workflow\"",
        "data-view=\"operations\"",
        "dailyCommandCenter",
        "workflowReviewQueue",
        "evolutionProposalBoard",
        "manualApprovalDock",
        "operationsConsole",
        "auditRecoveryPanel",
        "recallWorkbench",
        "Candidate Center",
        "候选中心",
        "candidateWorkspace",
        "candidateDetailPanel",
        "homeTodoList",
        "homeRiskPanel",
        "homeRecentPromotions",
        "homeQuickActions",
        "candidateActionPanel",
        "candidateRiskSummary",
        "candidateRecommendation",
        "proposalTarget",
        "proposalManualApproval",
        "renderEvolutionProposalBoard",
        "loadCandidateAnalysis",
        "operationResult",
        "renderCandidateActionPanel",
        "safeOperationZone",
        "dangerOperationZone",
        "exportOperationZone",
        "scheduleStatusPanel",
        "scheduleCurrentStatus",
        "nextRunTime",
        "lastScheduledRun",
        "schedulerCommandPreview",
        "runWorkspace",
        "runListPanel",
        "runDetailPanel",
        "selectedRunSummary",
        "selectedRunId",
        "recallTypeFilter",
        "recallResultSummary",
        "highlightText",
        "<mark",
        "doctorHealthGrid",
        "doctorFixActions",
        "renderDoctorHealth",
        "promotionTimeline",
        "targetChangeSummary",
        "reviewHistoryFilters",
        "reviewTimeline",
        "auditFilterBar",
        "auditTimeline",
        "待处理工作台",
        "危险操作",
        "健康检查",
        "时间线",
        "下一次运行",
        "Audit Center",
        "审计中心",
        "Promotion History",
        "晋升历史",
        "Review History",
        "审阅历史",
        "Rollback Preview",
        "回滚预览",
        "Schedule Center",
        "调度中心",
        "Skill Usage",
        "技能使用",
        "Status Summary",
        "状态统计",
        "Rebuild Database",
        "重建数据库",
        "clear active SQLite tables, and rescan all historical sessions",
        "清空当前 SQLite 表，并全量重扫历史会话",
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
        "paginationControls",
        "pageSizeSelect",
        "prevPage",
        "nextPage",
        "currentPageLabel",
        "skillUsageList",
        "compact-density",
        "min-height: 30px",
        "initializeData",
        "installSchedule",
        "installShortcut",
        "installSkills",
        "exportDigest",
        "backupDatabase",
        "runRows",
        "runStepRows",
        "recallSearch",
        "recallLimit",
        "recallResults",
        "doctorRows",
        "auditRows",
        "promotionRows",
        "reviewRows",
        "rollbackPreview",
        "copyRollback",
        "previewRollback",
        "reviewNote",
        "reviewRewrite",
        "saveReview",
        "confirmAction",
        "confirmActionLabel",
        "confirmFilesLabel",
        "confirmResultLabel",
        "confirmInitializeData",
        "confirmBackupDatabase",
        "confirmScanOnce",
        "confirmRebuildDatabase",
        "confirmExportDigest",
        "confirmExportCandidates",
        "confirmInstallSkills",
        "confirmSaveReview",
        "confirmArchiveSelected",
        "confirmRejectSelected",
        "confirmPromoteUser",
        "confirmPromoteAgents",
        "confirmPromoteSkill",
        "confirmPromotePatch",
        "confirmInstallSchedule",
        "confirmUninstallSchedule",
        "confirmInstallShortcut",
        "confirmUninstallShortcut",
        "promoteSkill",
        "promotePatch",
        "promoteAgents",
        "/api/init",
        "/api/backup",
        "/api/doctor",
        "/api/audit",
        "/api/history",
        "/api/schedule/status",
        "/rollback-preview",
        "/api/schedule/install",
        "/api/shortcut/install",
        "/api/install/skills",
        "/api/export/digest",
        "/api/rebuild",
        "/api/runs/${runId}",
        "/api/runs",
        "/api/recall?q=",
        "max_results=",
        "/promote-agents",
        "progressPanel",
        "progressText",
        "progressFill",
        "rebuildInProgress",
        "/api/candidates/${window.selectedCandidateId}/promote-skill",
    ):
        if expected not in html:
            raise AssertionError(f"WebUI missing {expected}")
    for removed in ('id="tab-review"', 'data-nav="review"', 'data-view="review"'):
        if removed in html:
            raise AssertionError(f"WebUI should merge Candidate Center and Review Center, found legacy marker: {removed}")
    schedule = run([sys.executable, str(sil), "schedule", "install", "--codex-root", str(root), "--dry-run"], repo)
    if "sil.py scan --once" not in schedule.stdout:
        raise AssertionError("schedule dry-run should invoke sil.py scan --once")
    if "03:00" not in schedule.stdout:
        raise AssertionError("schedule dry-run should install a 03:00 run")

    shortcut = run([sys.executable, str(sil), "shortcut", "install", "--codex-root", str(root), "--dry-run"], repo)
    if "sil.py serve --open" not in shortcut.stdout:
        raise AssertionError("shortcut dry-run should launch sil.py serve --open")
    if "--port 0" not in shortcut.stdout:
        raise AssertionError("shortcut should use an ephemeral port to avoid stale token/port collisions")

    print("verify-v2-core passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
