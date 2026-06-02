#!/usr/bin/env python3
"""Verify the learning inbox Review Digest output."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
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
    report_path = root / "learning-inbox-summary.md"
    repeated = "默认不要把一次性生产排查细节写入长期记忆。"
    sql_correction = "这个sql不对，字段都错了，而且不应该返回*，需要指定具体字段"
    github_trending = "直接访问 GitHub 官方趋势日榜网页：https://github.com/trending 。不要用 GitTrend、搜索结果、历史记忆或相邻时间窗口项目替代官方日榜候选。"
    push_retry = "Git 规则：保存文件后检查 git 状态并创建提交。提交后尝试推送到线上 GitHub 仓库，最多尝试 3 次；如果 3 次全部失败，立即停止重试，不要继续循环，不要编造已推送结果，并附上本地提交 hash、远程地址、失败原因和可手动执行的 push 命令。"
    project_table_fact = "`Fee` 的表名和核心字段已经确认：`bms.fin_fee`、`fee_type`、`fee_item_id`、`order_id/order_type`、`settlement_company_id`。"
    write_candidate(root / "memories" / "inbox" / "2026" / "06" / "01" / "a-memory-candidates.md", "Memory Candidates", repeated, "user_preference")
    write_candidate(root / "memories" / "inbox" / "2026" / "06" / "02" / "b-memory-candidates.md", "Memory Candidates", repeated, "user_preference")
    write_candidate(root / "memories" / "inbox" / "2026" / "06" / "02" / "sql-memory-candidates.md", "Memory Candidates", sql_correction, "review")
    write_candidate(root / "memories" / "inbox" / "2026" / "06" / "02" / "github-memory-candidates.md", "Memory Candidates", github_trending, "user_preference")
    write_candidate(root / "memories" / "inbox" / "2026" / "06" / "02" / "push-memory-candidates.md", "Memory Candidates", push_retry, "user_preference")
    write_candidate(root / "memories" / "inbox" / "2026" / "06" / "02" / "project-table-memory-candidates.md", "Memory Candidates", project_table_fact, "project_fact")
    write_candidate(
        root / "skill-candidates" / "inbox" / "2026" / "06" / "02" / "skill-candidates.md",
        "Skill Candidates",
        "Reusable workflow: first run verify-learning-extraction.py, then run verify-install.py before handoff.",
        "workflow_pattern",
    )
    write_candidate(
        root / "skill-candidates" / "patches" / "2026" / "06" / "02" / "patch-candidates.md",
        "Skill Patch Candidates",
        "memory-capture SKILL.md missing a rule: skill patch candidates must name the target skill before promotion.",
        "workflow_pattern",
    )

    subprocess.run(
        [
            sys.executable,
            str(repo / "agents" / "skills" / "memory-capture" / "scripts" / "summarize_learning_inbox.py"),
            "--root",
            str(root),
            "--report-path",
            str(report_path),
        ],
        check=True,
    )
    json_output = subprocess.run(
        [
            sys.executable,
            str(repo / "agents" / "skills" / "memory-capture" / "scripts" / "summarize_learning_inbox.py"),
            "--root",
            str(root),
            "--json",
        ],
        check=True,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    summary = json.loads(json_output.stdout)
    memory_items = summary["candidates"]["memory_candidates"]
    sql_item = next(item for item in memory_items if item["text"] == sql_correction)
    github_item = next(item for item in memory_items if item["text"] == github_trending)
    push_item = next(item for item in memory_items if item["text"] == push_retry)
    project_table_item = next(item for item in memory_items if item["text"] == project_table_fact)
    if sql_item["destination"] != "global_user_memory":
        raise AssertionError(f"sql correction should route to global memory: {sql_item}")
    if "avoid SELECT *" not in sql_item["rewrite_suggestion"]:
        raise AssertionError(f"sql correction should include rewrite suggestion: {sql_item}")
    if github_item["destination"] != "project_agents":
        raise AssertionError(f"github workflow should route to project agents: {github_item}")
    if push_item["destination"] != "global_user_memory":
        raise AssertionError(f"push retry rule should route to global memory: {push_item}")
    if "retry at most three times" not in push_item["rewrite_suggestion"]:
        raise AssertionError(f"push retry rule should include a push-specific rewrite: {push_item}")
    if project_table_item["destination"] != "project_agents":
        raise AssertionError(f"project table facts should route to project agents: {project_table_item}")

    digest = report_path.read_text(encoding="utf-8")
    assert_contains(digest, "# Learning Inbox Review Digest", "digest should use Review Digest title")
    assert_contains(digest, "## Action Queue", "digest should include an action queue")
    assert_contains(digest, "## Promotion Options", "digest should include promotion options")
    assert_contains(digest, "## Area Overview", "digest should include area-level counts")
    assert_contains(digest, "## Candidate Highlights", "digest should include candidate highlights")
    assert_contains(digest, "memory_candidates", "digest should include memory candidate area")
    assert_contains(digest, "skill_candidates", "digest should include skill candidate area")
    assert_contains(digest, "skill_patches", "digest should include skill patch area")
    assert_contains(digest, repeated, "digest should include repeated memory candidate text")
    assert_contains(digest, "occurrences: 2, files: 2", "digest should merge duplicate candidates")
    assert_contains(digest, "Review repeated safe preference", "digest should suggest promotion review for repeated memory")
    assert_contains(digest, "Destination", "digest action queue should include a destination column")
    assert_contains(digest, "Rewrite Suggestion", "digest should include rewrite suggestions")
    assert_contains(digest, "destination: global_user_memory", "stable global preferences should route to USER.md")
    assert_contains(digest, "destination: project_agents", "project-specific memory should route to project AGENTS.md")
    assert_contains(digest, "destination: skill_candidate", "reusable workflow should route to skill candidates")
    assert_contains(digest, "destination: skill_patch", "patch evidence should route to skill patch review")
    assert_contains(
        digest,
        "When writing SQL, verify table columns before drafting queries; avoid SELECT * by default and select only the required fields.",
        "sql correction should receive a concise reusable rewrite suggestion",
    )
    assert_contains(
        digest,
        "For GitHub Trending publishing workflows, use https://github.com/trending as the source of truth",
        "project-specific GitHub Trending candidate should receive a scoped rewrite suggestion",
    )
    assert_contains(digest, "promote_memory.py", "digest should include a memory promotion command")
    assert_contains(digest, "--approved", "memory promotion command should require approval")
    assert_contains(digest, "scan_skill_candidates.py", "skill candidates should point to scan before promotion")
    assert_contains(digest, "memory-capture SKILL.md missing", "digest should surface skill patch candidates")
    assert_contains(digest, "Inspect target SKILL.md", "skill patch candidates should require manual target skill inspection")

    print("verify-review-digest passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
