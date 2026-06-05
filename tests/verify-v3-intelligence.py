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
    if table_count(db, "digests") < 1:
        raise AssertionError("rebuild should persist a daily digest row")

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

        merge_payload = fetch_json(server.port, server.token, "/api/merge-suggestions")
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
    required_layout_rules = (
        "td > *",
        ".col-destination .tag",
        "text-overflow: ellipsis",
        "overflow-wrap: anywhere",
        "word-break: break-word",
    )
    for rule in required_layout_rules:
        if rule not in css:
            raise AssertionError(f"WebUI table layout should prevent long candidate text overflow: missing {rule}")
    js = js_path.read_text(encoding="utf-8")
    for marker in ("setupWizard", "dailyDigestPanel", "mergeSuggestionsPanel", "promotionPreview", "skillHealthList", "exportBundle", "importPreview"):
        if marker not in html and marker not in js:
            raise AssertionError(f"WebUI missing v3 marker: {marker}")

    print("verify-v3-intelligence passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
