#!/usr/bin/env python3
"""Verify the learning inbox Review Digest output."""

from __future__ import annotations

import argparse
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
    write_candidate(root / "memories" / "inbox" / "2026" / "06" / "01" / "a-memory-candidates.md", "Memory Candidates", repeated, "user_preference")
    write_candidate(root / "memories" / "inbox" / "2026" / "06" / "02" / "b-memory-candidates.md", "Memory Candidates", repeated, "user_preference")
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
    assert_contains(digest, "promote_memory.py", "digest should include a memory promotion command")
    assert_contains(digest, "--approved", "memory promotion command should require approval")
    assert_contains(digest, "scan_skill_candidates.py", "skill candidates should point to scan before promotion")
    assert_contains(digest, "memory-capture SKILL.md missing", "digest should surface skill patch candidates")
    assert_contains(digest, "Inspect target SKILL.md", "skill patch candidates should require manual target skill inspection")

    print("verify-review-digest passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
