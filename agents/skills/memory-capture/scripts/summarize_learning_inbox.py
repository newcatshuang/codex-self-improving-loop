#!/usr/bin/env python3
"""Summarize memory, skill, patch, scan, and usage signals."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from learning_loop_common import default_codex_root, read_usage, write_text


def count_files(path: Path, pattern: str = "*.md") -> int:
    return len(list(path.glob(pattern))) if path.exists() else 0


def latest_files(path: Path, top: int = 5) -> list[str]:
    if not path.exists():
        return []
    files = sorted(path.glob("*.md"), key=lambda item: item.stat().st_mtime, reverse=True)
    return [str(item) for item in files[:top]]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_codex_root())
    parser.add_argument("--usage-file", type=Path)
    parser.add_argument("--report-path", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = args.root.expanduser()
    usage_file = args.usage_file.expanduser() if args.usage_file else root / "skill-usage.json"
    report_path = args.report_path.expanduser() if args.report_path else root / "learning-inbox-summary.md"
    dirs = {
        "memory_candidates": root / "memories" / "inbox",
        "memory_archive": root / "memories" / "archive",
        "skill_candidates": root / "skill-candidates" / "inbox",
        "skill_patches": root / "skill-candidates" / "patches",
        "skill_archive": root / "skill-candidates" / "archive",
        "nudge_reports": root / "nudge-reports",
    }
    usage = read_usage(usage_file)
    summary = {
        "root": str(root),
        "usage_file": str(usage_file),
        "counts": {name: count_files(path) for name, path in dirs.items()},
        "latest": {name: latest_files(path) for name, path in dirs.items()},
        "skills_with_usage": len(usage.get("skills", {})),
    }
    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0
    lines = [
        "# Learning Inbox Summary",
        "",
        f"- root: {root}",
        f"- skills_with_usage: {summary['skills_with_usage']}",
        "",
        "| Area | Count |",
        "| --- | ---: |",
    ]
    for name, count in summary["counts"].items():
        lines.append(f"| {name} | {count} |")
    lines.extend(["", "## Latest Files", ""])
    for name, files in summary["latest"].items():
        lines.append(f"### {name}")
        lines.extend([f"- {file}" for file in files] or ["- None"])
        lines.append("")
    write_text(report_path, "\n".join(lines))
    print(f"Learning inbox summary written: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
