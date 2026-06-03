#!/usr/bin/env python3
"""Verify the embedded-data local dashboard renderer."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def write_candidate(path: Path, title: str, text: str, category: str = "review", safety: str = "review", status: str = "review") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                f"# {title}",
                "",
                "- generated_at: 2026-06-02T00:00:00+08:00",
                "- source: synthetic-test",
                "- status: review",
                "",
                "## Candidates",
                "",
                "### Candidate 1",
                "",
                f"- category: {category}",
                f"- safety: {safety}",
                f"- status: {status}",
                "",
                "```text",
                text,
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )


def extract_payload(html: str) -> dict[str, object]:
    match = re.search(r"window\.__CSIL_DASHBOARD_DATA__\s*=\s*(\{.*?\});\s*</script>", html, re.DOTALL)
    if not match:
        raise AssertionError("dashboard should embed JSON payload in window.__CSIL_DASHBOARD_DATA__")
    return json.loads(match.group(1))


def assert_contains(text: str, expected: str, message: str) -> None:
    if expected not in text:
        raise AssertionError(message)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--work-root", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    root = args.work_root.resolve()
    output = root / "codex-self-improving-loop-dashboard.html"
    today = datetime.now().strftime("%Y-%m-%d")
    today_parts = today.split("-")
    old_parts = ["2026", "05", "31"]
    old_date = "-".join(old_parts)

    sql_correction = "这个sql不对，字段都错了，而且不应该返回*，需要指定具体字段"
    project_fact = "GitHub Trending publishing workflow should use https://github.com/trending as the source of truth."
    reusable_workflow = "Reusable workflow: first run verify-learning-extraction.py, then run verify-install.py before handoff."
    skill_patch = "memory-capture SKILL.md missing a rule: skill patch candidates must name the target skill before promotion."

    write_candidate(root / "memories" / "inbox" / Path(*today_parts) / "sql-memory-candidates.md", "Memory Candidates", sql_correction, "review")
    write_candidate(root / "memories" / "inbox" / Path(*old_parts) / "github-memory-candidates.md", "Memory Candidates", project_fact, "user_preference")
    write_candidate(root / "skill-candidates" / "inbox" / Path(*today_parts) / "skill-candidates.md", "Skill Candidates", reusable_workflow, "workflow_pattern")
    write_candidate(root / "skill-candidates" / "patches" / Path(*old_parts) / "patch-candidates.md", "Skill Patch Candidates", skill_patch, "workflow_pattern")

    subprocess.run(
        [
            sys.executable,
            str(repo / "agents" / "skills" / "memory-capture" / "scripts" / "render_dashboard.py"),
            "--root",
            str(root),
            "--output",
            str(output),
        ],
        check=True,
    )

    html = output.read_text(encoding="utf-8")
    assert_contains(html, "Codex Self-Improving Loop Dashboard", "dashboard should include the product title")
    assert_contains(html, "All Records Summary", "dashboard should include all-records summary")
    assert_contains(html, "Today's Records", "dashboard should include today's default section")
    assert_contains(html, "copyPromotionCommand", "dashboard should expose copy promotion command action")
    assert_contains(html, "dateFilter", "dashboard should expose a date filter")
    assert_contains(html, "historyTimeline", "dashboard should expose history navigation")
    assert_contains(html, "promote_memory.py", "dashboard should embed promotion commands")
    assert_contains(html, "scan_skill_candidates.py", "dashboard should embed skill review command guidance")
    assert_contains(html, "workbench-shell", "dashboard should use the compact workbench shell")
    assert_contains(html, "kpi-strip", "dashboard should render compact KPI summaries")
    assert_contains(html, "sticky-controls", "dashboard filters should stay close to the table")
    assert_contains(html, "detail-rail", "dashboard should render the selected record as a review rail")
    assert_contains(html, "dense-table", "dashboard should use a dense scanner-friendly table")
    assert_contains(html, "module-color-system", "dashboard should use richer module colors")
    assert_contains(html, "fluid-workspace", "dashboard should adapt to the available window width")
    assert_contains(html, "destination-global_user_memory", "dashboard should color-code global memory records")
    assert_contains(html, "destination-project_agents", "dashboard should color-code project AGENTS records")
    assert_contains(html, "destination-skill_candidate", "dashboard should color-code skill candidate records")
    assert_contains(html, "destination-skill_patch", "dashboard should color-code skill patch records")
    assert_contains(html, "filled-kpi", "dashboard summary KPI cards should use filled module backgrounds")
    assert_contains(html, "filled-destination", "dashboard destination cards should use filled module backgrounds")

    payload = extract_payload(html)
    if payload["default_date"] != today:
        raise AssertionError(f"dashboard should default to today's date, got {payload['default_date']}")
    dates = payload["dates"]
    if today not in dates or old_date not in dates:
        raise AssertionError(f"dashboard should include today and historical dates, got {dates}")
    candidates = payload["candidates"]
    if len(candidates) != 4:
        raise AssertionError(f"expected four merged candidates, got {len(candidates)}")
    destinations = {item["destination"] for item in candidates}
    for expected in {"global_user_memory", "project_agents", "skill_candidate", "skill_patch"}:
        if expected not in destinations:
            raise AssertionError(f"missing destination {expected}: {destinations}")
    sql_item = next(item for item in candidates if item["text"] == sql_correction)
    if today not in sql_item["dates"] or sql_item["latest_date"] != today:
        raise AssertionError(f"sql item should be dated today: {sql_item}")
    if "avoid SELECT *" not in sql_item["rewrite_suggestion"]:
        raise AssertionError(f"sql item should include rewrite suggestion: {sql_item}")
    summary = payload["summary"]
    if summary["total_candidates"] != 4:
        raise AssertionError(f"summary should count all records: {summary}")
    if summary["today_candidates"] != 2:
        raise AssertionError(f"summary should count today's records: {summary}")
    if summary["by_area"]["memory_candidates"] != 2:
        raise AssertionError(f"summary should count memory candidates: {summary}")

    print("verify-dashboard-render passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
