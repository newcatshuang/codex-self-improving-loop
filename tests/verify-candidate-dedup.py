#!/usr/bin/env python3
"""Verify cross-file memory candidate deduplication."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def write_candidate(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                "# Memory Candidates",
                "",
                "- status: review",
                "",
                "## Candidates",
                "",
                "### Candidate 1",
                "",
                "- category: user_preference",
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--work-root", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    root = args.work_root.resolve()
    inbox = root / "memories" / "inbox"
    target = root / "memories" / "USER.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("# User Memory\n\n", encoding="utf-8")

    repeated = "默认不要把一次性生产排查细节写入长期记忆。"
    write_candidate(inbox / "2026" / "06" / "01" / "a-memory-candidates.md", repeated)
    write_candidate(inbox / "2026" / "06" / "02" / "b-memory-candidates.md", repeated)
    write_candidate(inbox / "2026" / "06" / "02" / "c-memory-candidates.md", "以后优先给出验证命令和剩余风险。")

    completed = subprocess.run(
        [
            sys.executable,
            str(repo / "agents" / "skills" / "memory-capture" / "scripts" / "promote_candidates.py"),
            "--root",
            str(root),
            "--json",
        ],
        check=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    report = json.loads(completed.stdout)
    if report["candidate_count"] != 3:
        raise AssertionError(f"expected 3 raw candidates, got {report['candidate_count']}")
    if report["merged_candidate_count"] != 2:
        raise AssertionError(f"expected 2 merged candidates, got {report['merged_candidate_count']}")
    repeated_items = [item for item in report["items"] if item["text"] == repeated]
    if len(repeated_items) != 1:
        raise AssertionError("repeated candidate should appear once in merged report")
    repeated_item = repeated_items[0]
    if repeated_item["occurrences"] != 2 or repeated_item["file_count"] != 2:
        raise AssertionError(f"unexpected repeated candidate stats: {repeated_item}")
    if len(repeated_item["examples"]) != 2:
        raise AssertionError("merged candidate should preserve source examples")

    print("verify-candidate-dedup passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
