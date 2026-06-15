#!/usr/bin/env python3
"""Verify v3 intelligence APIs, review digest, bundle export, and FTS recall."""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import urllib.request
from pathlib import Path

from helpers import TestServer, fetch_json, run_sil, table_count, write_jsonl_session


def main() -> int:
    os.environ["CODEX_SIL_DISABLE_CODEX"] = "1"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--work-root", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    root = args.work_root.resolve()
    db = root / "self-improving-loop" / "self-improving-loop.sqlite"

    write_jsonl_session(
        root / "sessions" / "2026" / "06" / "05" / "one.jsonl",
        [
            {"role": "user", "content": "Remember the GitHub Trending workflow. token=sk-SECRET123"},
            {"role": "assistant", "content": "Using `memory-capture` to preserve the reusable rule."},
            {"role": "user", "content": "请记住：SQL 查询必须先确认字段，避免 SELECT *。"},
            {"role": "user", "content": "这个流程可以做成 skill：先 doctor，再 rebuild，再 scan --once。"},
        ],
    )
    write_jsonl_session(
        root / "sessions" / "2026" / "06" / "05" / "two.jsonl",
        [
            {"role": "user", "content": "请把 skill patch 候选记录下来：memory-capture 应补充冲突检测。"},
            {"role": "assistant", "content": "I will use `session-recall` before touching prior context."},
        ],
    )
    (root / "memories").mkdir(parents=True, exist_ok=True)
    (root / "memories" / "USER.md").write_text("# USER.md\n", encoding="utf-8")
    (root / "AGENTS.md").write_text("# AGENTS.md\n\n## Project Learned Facts\n", encoding="utf-8")

    run_sil(repo, root, "rebuild", "--backup")
    if table_count(db, "recommendations") < table_count(db, "candidates"):
        raise AssertionError("rebuild should generate a recommendation row for each candidate")
    if table_count(db, "candidate_analyses") < table_count(db, "candidates"):
        raise AssertionError("rebuild should persist an analysis row for each candidate")
    if table_count(db, "evolution_proposals") < table_count(db, "candidates"):
        raise AssertionError("rebuild should persist an evolution proposal row for each candidate")
    if table_count(db, "digests") < 1:
        raise AssertionError("rebuild should persist a daily digest row")
    with sqlite3.connect(db) as conn:
        auto_promoted = conn.execute("select count(*) from candidates where status='promoted'").fetchone()[0]
        if int(auto_promoted) != 0:
            raise AssertionError("scan must not auto-promote candidates; all promotion stays manual")

    with sqlite3.connect(db) as conn:
        conn.execute(
            """
            insert into candidates(type, title, text, normalized, destination, rewrite_suggestion, safety, confidence, extractor)
            values('memory', 'SQL columns one', 'When writing SQL, verify table columns before drafting queries; avoid SELECT *.', 'sql columns one', 'global_user_memory', 'When writing SQL, verify table columns before drafting queries; avoid SELECT *.', 'review', 0.74, 'test')
            """
        )
        first = int(conn.execute("select last_insert_rowid()").fetchone()[0])
        conn.execute(
            """
            insert into candidates(type, title, text, normalized, destination, rewrite_suggestion, safety, confidence, extractor)
            values('memory', 'SQL columns two', 'Before writing SQL queries, verify table columns first and avoid SELECT star.', 'sql columns two', 'global_user_memory', 'Before writing SQL queries, verify table columns first and avoid SELECT star.', 'review', 0.71, 'test')
            """
        )
        second = int(conn.execute("select last_insert_rowid()").fetchone()[0])

    with TestServer(repo, root) as server:
        recommendations = fetch_json(server.port, server.token, "/api/recommendations")
        actions = {item["suggested_action"] for item in recommendations.get("recommendations", [])}
        if not actions or actions - {"promote", "merge", "archive", "reject", "needs_review"}:
            raise AssertionError(f"recommendations should use fixed actions: {recommendations}")
        if not all(item.get("recommendation_reason") for item in recommendations["recommendations"]):
            raise AssertionError(f"recommendations should include reasons: {recommendations}")
        regenerated = fetch_json(server.port, server.token, f"/api/candidates/{first}/recommend", method="POST")
        if regenerated.get("suggested_action") not in {"promote", "merge", "archive", "reject", "needs_review"}:
            raise AssertionError(f"single candidate recommendation should be regenerated: {regenerated}")
        analysis = fetch_json(server.port, server.token, f"/api/candidates/{first}/analysis")
        if not analysis.get("analysis") or not analysis.get("proposal"):
            raise AssertionError(f"candidate analysis endpoint should expose analysis and proposal: {analysis}")
        if analysis["analysis"].get("engine") not in {"codex", "fallback_rules"}:
            raise AssertionError(f"candidate analysis should identify its engine: {analysis}")
        if analysis["proposal"].get("requires_manual_approval") is not True:
            raise AssertionError(f"evolution proposals must keep manual approval required: {analysis}")
        if analysis["proposal"].get("target_type") not in {"USER.md", "AGENTS.md", "skill", "skill_patch", "manual_review"}:
            raise AssertionError(f"proposal should target a known manual review surface: {analysis}")

        with sqlite3.connect(db) as conn:
            conn.execute("delete from merge_suggestions")
            conn.commit()
            before_summary_read = int(conn.execute("select count(*) from merge_suggestions").fetchone()[0])
        summary_payload = fetch_json(server.port, server.token, "/api/summary")
        if not summary_payload.get("summary"):
            raise AssertionError(f"summary should return current counters: {summary_payload}")
        with sqlite3.connect(db) as conn:
            after_summary_read = int(conn.execute("select count(*) from merge_suggestions").fetchone()[0])
        if before_summary_read != after_summary_read:
            raise AssertionError("/api/summary should be read-only and must not generate merge suggestions")

        merge_payload = fetch_json(server.port, server.token, "/api/merge-suggestions")
        if merge_payload.get("merge_suggestions"):
            raise AssertionError(f"/api/merge-suggestions should be read-only before refresh: {merge_payload}")
        merge_payload = fetch_json(server.port, server.token, "/api/merge-suggestions/refresh", method="POST")
        groups = merge_payload.get("merge_suggestions", [])
        group = next((item for item in groups if first in item.get("candidate_ids", []) and second in item.get("candidate_ids", [])), None)
        if not group:
            raise AssertionError(f"similar SQL candidates should be grouped: {merge_payload}")
        applied = fetch_json(server.port, server.token, f"/api/merge-suggestions/{group['id']}/apply", method="POST")
        if applied.get("status") != "merged":
            raise AssertionError(f"merge apply should report merged: {applied}")
        with sqlite3.connect(db) as conn:
            merged = conn.execute("select count(*) from candidates where id in (?, ?) and status='merged'", (first, second)).fetchone()[0]
        if int(merged) < 1:
            raise AssertionError("merge apply should set duplicate candidate status to merged")

        with sqlite3.connect(db) as conn:
            candidate_id = int(conn.execute("select id from candidates where type='memory' and status='review' limit 1").fetchone()[0])
        preview = fetch_json(server.port, server.token, f"/api/candidates/{candidate_id}/promotion-preview?target=user")
        if preview.get("target_type") != "USER.md" or "--- before" not in preview.get("diff", ""):
            raise AssertionError(f"promotion preview should return a unified diff before writing: {preview}")
        if "avoid SELECT *" in (root / "memories" / "USER.md").read_text(encoding="utf-8"):
            raise AssertionError("promotion preview must not write USER.md")

        recall = fetch_json(server.port, server.token, "/api/recall?q=GitHub%20Trending&max_results=5")
        if not recall.get("results"):
            raise AssertionError(f"FTS recall should return matches: {recall}")
        first_result = recall["results"][0]
        if "rank" not in first_result or "snippet" not in first_result:
            raise AssertionError(f"recall should include rank and snippet: {recall}")
        if "sk-SECRET123" in json.dumps(recall):
            raise AssertionError("recall snippets must redact secret-like values")

        digest = fetch_json(server.port, server.token, "/api/digests/latest")
        if not digest.get("digest") or "new_candidates" not in digest["digest"]:
            raise AssertionError(f"latest digest should be available: {digest}")
        bundle = fetch_json(server.port, server.token, "/api/export/bundle", method="POST")
        bundle_path = Path(bundle.get("path", ""))
        if not bundle_path.exists() or bundle_path.suffix != ".zip":
            raise AssertionError(f"export bundle should create a zip: {bundle}")
        import_preview = fetch_json(server.port, server.token, "/api/import/preview", method="POST", payload={"path": str(bundle_path)})
        if not import_preview.get("valid") or not import_preview.get("entries"):
            raise AssertionError(f"import preview should validate bundle structure: {import_preview}")

        setup = fetch_json(server.port, server.token, "/api/setup/status")
        if not setup.get("database_exists") or setup.get("session_count", 0) < 2:
            raise AssertionError(f"setup status should describe initialization state: {setup}")
        health = fetch_json(server.port, server.token, "/api/skills/health")
        statuses = {item["status"] for item in health.get("skills", [])}
        if not statuses or statuses - {"active", "cold", "needs_patch", "duplicate_suspected"}:
            raise AssertionError(f"skill health should expose fixed statuses: {health}")

        request = urllib.request.Request(f"http://127.0.0.1:{server.port}/styles.css")
        with urllib.request.urlopen(request, timeout=5) as response:
            css = response.read().decode("utf-8")
        request = urllib.request.Request(f"http://127.0.0.1:{server.port}/app.js")
        with urllib.request.urlopen(request, timeout=5) as response:
            js = response.read().decode("utf-8")
        if ".app-shell" not in css or "setupWizard" not in js:
            raise AssertionError("split WebUI resources should be served as CSS and JS")

    html = (repo / "src" / "codex_sil" / "web" / "index.html").read_text(encoding="utf-8")
    css_path = repo / "src" / "codex_sil" / "web" / "styles.css"
    js_path = repo / "src" / "codex_sil" / "web" / "app.js"
    if not css_path.exists() or not js_path.exists():
        raise FileNotFoundError("WebUI should be split into index.html, styles.css, and app.js")
    css = css_path.read_text(encoding="utf-8")
    scanner_text = (repo / "src" / "codex_sil" / "scanner.py").read_text(encoding="utf-8")
    analysis_text = (repo / "src" / "codex_sil" / "analysis.py").read_text(encoding="utf-8")
    for forbidden in ("promote_to_user_memory", "promote_to_project_agents", "promote_to_skill", "promote_to_skill_patch"):
        if forbidden in scanner_text or forbidden in analysis_text:
            raise AssertionError(f"Scan/analysis paths must never call promotion functions automatically: {forbidden}")
    required_layout_rules = (
        ".candidate-table",
        ".candidate-row",
        ".candidate-col-priority",
        "td > *",
        ".col-destination .tag",
        "text-overflow: ellipsis",
        "overflow-wrap: anywhere",
        "word-break: break-word",
        "@media (max-width: 900px)",
        ".candidate-workspace",
        ".workflow-shell",
        ".nav-group-label",
        ".next-action-body",
    )
    for rule in required_layout_rules:
        if rule not in css:
            raise AssertionError(f"WebUI table layout should prevent long candidate text overflow: missing {rule}")
    js = js_path.read_text(encoding="utf-8")
    for marker in ("candidate-row", "candidate-title", "candidate-snippet"):
        if marker not in js:
            raise AssertionError(f"Candidate Center should render dense review table rows: missing {marker}")
    for marker in ("setupWizard", "dailyDigestPanel", "mergeSuggestionsPanel", "promotionPreview", "skillHealthTable", "skillHealthRows", "exportBundle", "importPreview"):
        if marker not in html and marker not in js:
            raise AssertionError(f"WebUI missing v3 marker: {marker}")
    required_workflow_markers = (
        "data-view=\"dashboard\"",
        "data-view=\"workflow\"",
        "data-view=\"operations\"",
        "dailyCommandCenter",
        "dashboardNextActionPanel",
        "dashboardNextActionCopy",
        "dashboardTopPriorities",
        "dashboardPriorityList",
        "sideNav",
        'data-nav="dashboard"',
        'data-nav="workflow"',
        'data-nav="evidence"',
        'data-nav="approval"',
        'data-nav="data"',
        'data-nav="automation"',
        'data-nav="skills"',
        'data-nav="recall"',
        'data-nav="history"',
        'data-nav="doctor"',
        "workflowReviewQueue",
        "workflowActionStrip",
        "workflowNextActionCopy",
        "workflowPrimaryAction",
        "workflowSecondaryAction",
        "evolutionProposalBoard",
        "manualApprovalDock",
        "operationsConsole",
        "auditRecoveryPanel",
        "recallWorkbench",
        "workflowStageRail",
        "workflowReadinessPanel",
        "approvalReadiness",
        "previewOnlyActions",
        "previewUserDiff",
        "previewAgentsDiff",
        "previewSkillDiff",
        "previewPatchDiff",
        "candidateSortMode",
        "selectedPriorityReasons",
        "operationsRecoveryQueue",
        "recoveryQueueList",
        "operationsData",
        "operationsAutomation",
        "operationsKnowledge",
        "operationsEvidence",
    )
    for marker in required_workflow_markers:
        if marker not in html:
            raise AssertionError(f"WebUI should expose the full self-improvement workflow surface: missing {marker}")
    dashboard_html = html.split('data-view="dashboard"', 1)[1].split('data-view="operations"', 1)[0]
    if "<button" in dashboard_html:
        raise AssertionError("Dashboard should be a read-only status panel; move operation buttons into their real modules")
    if html.index("sideNav") > html.index("operationsConsole"):
        raise AssertionError("Primary module navigation should appear before operations panels")
    if html.index('id="operationsAutomation"') < html.index("schedule-panel"):
        raise AssertionError("Operations automation shortcut should point to Schedule Center, not promotion guidance")
    required_workflow_js = (
        "renderEvolutionProposalBoard",
        "loadCandidateAnalysis",
        "/api/candidates/${id}/analysis",
        "proposalTarget",
        "proposalManualApproval",
        "renderWorkflowReadiness",
        "workflow-stage-done",
        "approvalReady",
        "approvalBlocked",
        "renderDashboardNextAction",
        "renderWorkflowNextAction",
        "runWorkflowPrimaryAction",
        "runWorkflowSecondaryAction",
        "toastPreviewLoaded",
        "candidatePriorityScore",
        "priorityReviewFirst",
        "candidate-row-note",
        "candidatePriorityReasons",
        "priorityReasonReview",
        "priorityReasonProposal",
        "renderDashboardTopPriorities",
        "dashboardPriorityItem",
        "renderOperationsRecoveryQueue",
        "recoveryQueueItem",
        "recoveryQueueRunFailure",
    )
    for marker in required_workflow_js:
        if marker not in js:
            raise AssertionError(f"WebUI should make LLM analysis central to manual review: missing {marker}")
    for marker in (
        "sortedCandidates(visibleCandidates())",
        'document.getElementById("candidateSortMode").addEventListener("change"',
        "candidatePriorityLabel",
    ):
        if marker not in js:
            raise AssertionError(f"Candidate queue should support AI-assisted review ordering: missing {marker}")
    if "dashboardPrimaryAction" in html or "dashboardSecondaryAction" in html or "openPriorityWorkflow" in html:
        raise AssertionError("Dashboard should not expose action buttons")
    if "runDashboardPrimaryAction" in js or "runDashboardSecondaryAction" in js:
        raise AssertionError("Dashboard status guidance should stay read-only")
    if "renderDashboardNextAction()" not in js:
        raise AssertionError("Dashboard should render read-only workflow guidance")
    if "renderWorkflowNextAction()" not in js or "workflowNextActionCopy" not in js:
        raise AssertionError("Review Workflow should guide the next manual review step")
    if 'api(`/api/candidates/${window.selectedCandidateId}/promote' in js.split("async function runWorkflowPrimaryAction", 1)[1].split("async function runWorkflowSecondaryAction", 1)[0]:
        raise AssertionError("Workflow primary next action must not call promotion endpoints directly")
    if "runAction(() => api(`/api/candidates/${window.selectedCandidateId}/promote" not in js:
        raise AssertionError("Promotion writes should remain explicit Manual Approval Dock actions")
    for target, button_id in (
        ("user", "previewUserDiff"),
        ("agents", "previewAgentsDiff"),
        ("skill", "previewSkillDiff"),
        ("patch", "previewPatchDiff"),
    ):
        expected = f'document.getElementById("{button_id}").addEventListener("click", () => runPreviewOnly("{target}"))'
        if expected not in js:
            raise AssertionError(f"Preview-only button should not call promotion endpoints directly: missing {button_id}")
    for button_id, confirm_key, preview_target in (
        ("promoteSelected", "confirmPromoteUser", "user"),
        ("promoteAgents", "confirmPromoteAgents", "agents"),
        ("promoteSkill", "confirmPromoteSkill", "skill"),
        ("promotePatch", "confirmPromotePatch", "patch"),
    ):
        expected = f'document.getElementById("{button_id}").addEventListener("click", () => runAction('
        if expected not in js or f'confirmKey: "{confirm_key}"' not in js or f'previewTarget: "{preview_target}"' not in js:
            raise AssertionError(f"Promotion button must require manual confirmation and preview: {button_id}")
    required_workflow_css = (
        ".command-center",
        ".workflow-shell",
        ".workflow-queue",
        ".proposal-board",
        ".manual-approval-dock",
        ".operations-console",
        ".audit-recovery-panel",
        ".recall-workbench",
        ".workflow-map",
        ".workflow-stage-rail",
        ".workflow-stage-done",
        ".workflow-stage-current",
        ".workflow-readiness-panel",
        ".readiness-list",
        ".candidate-row-note",
        ".priority-reason-list",
        ".selected-priority-panel",
        ".dashboard-priority-list",
        ".dashboard-priority-item",
        ".recovery-queue",
        ".recovery-queue-list",
        ".recovery-queue-item",
        ".operations-index",
        ".operations-section",
    )
    for marker in required_workflow_css:
        if marker not in css:
            raise AssertionError(f"WebUI should style the redesigned workflow surface: missing {marker}")
    if "workflowMap" in html or "operationsLifecycleMap" in html:
        raise AssertionError("Dashboard and Operations should not include flow-card explainer sections")
    for marker in ("skillNameHeader", "skillStatusHeader", "skillUsageHeader", "skillPatchHeader", "skillActionHeader"):
        if marker not in html and marker not in js:
            raise AssertionError(f"Skill health should render as a table with column marker: {marker}")

    readme_en = (repo / "README.md").read_text(encoding="utf-8")
    readme_zh = (repo / "README.zh-CN.md").read_text(encoding="utf-8")
    quickstart_zh = (repo / "QUICKSTART.zh-CN.md").read_text(encoding="utf-8")
    memory_skill = (repo / "agents" / "skills" / "memory-capture" / "SKILL.md").read_text(encoding="utf-8")
    stale_manual_boundary_markers = (
        "Use memory candidate auto-promotion only",
        "safe, short, repeated",
        "hard stop for automatic promotion",
    )
    for marker in stale_manual_boundary_markers:
        if marker in memory_skill:
            raise AssertionError(f"Installed instructions must not re-enable automatic promotion wording: {marker}")
    if (repo / "codex" / "AGENTS.learning-block.md").exists():
        raise AssertionError("Global AGENTS.md self-improving-loop block template should not be installed")
    if "v2 是一个" in quickstart_zh:
        raise AssertionError("Quickstart should describe the current v3 control plane, not the old v2 wording")
    if "所有晋升都必须人工确认" not in quickstart_zh:
        raise AssertionError("Quickstart should state the manual promotion boundary")
    for marker in (
        "Dashboard",
        "Review Workflow",
        "Operations",
        "Manual Approval Dock",
        "GET /api/candidates/{id}/analysis",
    ):
        if marker not in readme_en:
            raise AssertionError(f"English README should document the redesigned WebUI workflow: missing {marker}")
    for marker in (
        "总览",
        "审阅工作流",
        "运维与历史",
        "人工审批操作台",
        "GET /api/candidates/{id}/analysis",
    ):
        if marker not in readme_zh:
            raise AssertionError(f"Chinese README should document the redesigned WebUI workflow: missing {marker}")

    print("verify-v3-intelligence passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
