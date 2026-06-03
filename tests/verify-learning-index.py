#!/usr/bin/env python3
"""Verify the shared learning index powers dashboard and lightweight digest output."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def write_candidate(path: Path, title: str, text: str, category: str = "review") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                f"# {title}",
                "",
                "- generated_at: 2026-06-02T00:00:00+00:00",
                "- source: synthetic-test",
                "- status: review",
                "",
                "## Candidates",
                "",
                "### Candidate 1",
                "",
                f"- category: {category}",
                "- safety: review",
                "- status: review",
                "",
                "```text",
                text,
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )


def assert_contains(text: str, expected: str, message: str) -> None:
    if expected not in text:
        raise AssertionError(message)


def assert_not_contains(text: str, forbidden: str, message: str) -> None:
    if forbidden in text:
        raise AssertionError(message)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--work-root", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    root = args.work_root.resolve()
    today = datetime.now().strftime("%Y-%m-%d")
    today_parts = today.split("-")
    old_parts = ["2026", "05", "31"]
    index_path = root / "learning-index.json"
    dashboard_path = root / "dashboard.html"
    digest_path = root / "daily-digest.md"

    write_candidate(
        root / "memories" / "inbox" / Path(*today_parts) / "sql-memory-candidates.md",
        "Memory Candidates",
        "When writing SQL, verify table columns first and avoid SELECT * by default.",
        "user_preference",
    )
    write_candidate(
        root / "skill-candidates" / "inbox" / Path(*today_parts) / "skill-candidates.md",
        "Skill Candidates",
        "Reusable workflow: first run verify-learning-extraction.py, then run verify-install.py before handoff.",
        "workflow_pattern",
    )
    write_candidate(
        root / "skill-candidates" / "patches" / Path(*old_parts) / "patch-candidates.md",
        "Skill Patch Candidates",
        "memory-capture SKILL.md missing a rule: skill patch candidates must name the target skill before promotion.",
        "workflow_pattern",
    )

    subprocess.run(
        [
            sys.executable,
            str(repo / "agents" / "skills" / "memory-capture" / "scripts" / "build_learning_index.py"),
            "--root",
            str(root),
            "--output",
            str(index_path),
        ],
        check=True,
    )
    payload = json.loads(index_path.read_text(encoding="utf-8"))
    if payload["summary"]["total_candidates"] != 3:
        raise AssertionError(f"learning index should count all candidates: {payload['summary']}")
    if today not in payload["dates"] or "2026-05-31" not in payload["dates"]:
        raise AssertionError(f"learning index should preserve date navigation: {payload['dates']}")
    destinations = {item["destination"] for item in payload["candidates"]}
    for expected in {"global_user_memory", "skill_candidate", "skill_patch"}:
        if expected not in destinations:
            raise AssertionError(f"learning index missing destination {expected}: {destinations}")

    subprocess.run(
        [
            sys.executable,
            str(repo / "agents" / "skills" / "memory-capture" / "scripts" / "render_dashboard.py"),
            "--root",
            str(root),
            "--index-path",
            str(index_path),
            "--output",
            str(dashboard_path),
        ],
        check=True,
    )
    dashboard = dashboard_path.read_text(encoding="utf-8")
    assert_contains(dashboard, "window.__CSIL_DASHBOARD_DATA__", "dashboard should embed the shared index payload")
    assert_contains(dashboard, "learning-index.json", "dashboard renderer should preserve shared index references")

    subprocess.run(
        [
            sys.executable,
            str(repo / "agents" / "skills" / "memory-capture" / "scripts" / "summarize_learning_inbox.py"),
            "--root",
            str(root),
            "--index-path",
            str(index_path),
            "--report-path",
            str(digest_path),
            "--light",
        ],
        check=True,
    )
    digest = digest_path.read_text(encoding="utf-8")
    assert_contains(digest, "# Learning Inbox Review Digest", "light digest should keep the digest title")
    assert_contains(digest, "## Review Entry Points", "light digest should lead with review entry points")
    assert_contains(digest, "learning-index.json", "light digest should point to the shared index")
    assert_contains(digest, "codex-self-improving-loop-dashboard.html", "light digest should point to WebUI")
    assert_contains(digest, "## Action Queue", "light digest should still include a compact action queue")
    assert_not_contains(digest, "## Candidate Highlights", "light digest should not duplicate long candidate details")
    assert_not_contains(digest, "## Latest Files", "light digest should not duplicate file inventory")
    if len(digest) > 5000:
        raise AssertionError("light digest should remain compact")

    print("verify-learning-index passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
