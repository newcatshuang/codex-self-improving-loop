#!/usr/bin/env python3
"""Verify low-output mode avoids empty reports and writes one daily digest."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--work-root", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    root = args.work_root.resolve()
    session_dir = root / "sessions"
    session_dir.mkdir(parents=True, exist_ok=True)
    session = session_dir / "no-candidates.jsonl"
    session.write_text('{"role":"user","content":"请把这个句子改得更自然一点。"}\n', encoding="utf-8")

    nudge = repo / "agents" / "skills" / "memory-capture" / "scripts" / "codex_memory_nudge.py"
    completed = subprocess.run(
        [
            sys.executable,
            str(nudge),
            "--root",
            str(root),
            "--session-file",
            str(session),
        ],
        check=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    if "Review digest summary:" not in completed.stdout:
        raise AssertionError("nudge should print review digest summary")
    if "Promotion options:" not in completed.stdout:
        raise AssertionError("nudge should print promotion options location")

    if list((root / "memories" / "inbox").rglob("*.md")):
        raise AssertionError("empty memory candidate reports should not be written")
    if list((root / "skill-candidates" / "inbox").rglob("*.md")):
        raise AssertionError("empty skill candidate reports should not be written")
    if list((root / "skill-candidates" / "patches").rglob("*.md")):
        raise AssertionError("empty skill patch candidate reports should not be written")
    if list((root / "nudge-reports").rglob("*-end-of-task-nudge.md")):
        raise AssertionError("successful no-candidate nudge should not write detailed nudge report")
    if list((root / "nudge-reports").rglob("*-skill-candidate-security-scan.md")):
        raise AssertionError("skill scan should use latest report path, not timestamped reports")
    if list((root / "nudge-reports").rglob("*-user-memory-budget.md")):
        raise AssertionError("memory budget should use latest report path, not timestamped reports")

    daily_digests = list((root / "daily-digests").rglob("review-digest.md"))
    if len(daily_digests) != 1:
        raise AssertionError(f"expected one daily digest, got {daily_digests}")
    digest_text = daily_digests[0].read_text(encoding="utf-8")
    if "# Learning Inbox Review Digest" not in digest_text:
        raise AssertionError("daily digest should contain review digest")
    if not (root / "learning-inbox-summary.md").exists():
        raise AssertionError("latest learning inbox summary should still be written")
    if not (root / "learning-index.json").exists():
        raise AssertionError("shared learning index should be refreshed even when there are no candidates")
    if not (root / "latest-skill-candidate-security-scan.md").exists():
        raise AssertionError("latest skill scan report should be written")
    if not (root / "latest-user-memory-budget.md").exists():
        raise AssertionError("latest memory budget report should be written")
    dashboard = root / "codex-self-improving-loop-dashboard.html"
    if not dashboard.exists():
        raise AssertionError("dashboard should be refreshed even when there are no candidates")
    dashboard_text = dashboard.read_text(encoding="utf-8")
    if "Codex Self-Improving Loop Dashboard" not in dashboard_text:
        raise AssertionError("dashboard should contain the local WebUI title")

    print("verify-low-output-mode passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
