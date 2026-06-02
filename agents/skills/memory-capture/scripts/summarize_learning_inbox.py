#!/usr/bin/env python3
"""Generate a review digest for memory, skill, patch, scan, and usage signals."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from learning_loop_common import clean_candidate_text, default_codex_root, markdown_files_recursive, normalize_memory_text, read_usage, write_text


def count_files(path: Path, pattern: str = "*.md") -> int:
    if pattern == "*.md":
        return len(markdown_files_recursive(path))
    return len(list(path.rglob(pattern))) if path.exists() else 0


def latest_files(path: Path, top: int = 5) -> list[str]:
    if not path.exists():
        return []
    files = sorted(markdown_files_recursive(path), key=lambda item: item.stat().st_mtime, reverse=True)
    return [str(item) for item in files[:top]]


def candidate_blocks(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    blocks = re.split(r"(?m)^### Candidate \d+\s*$", text)
    items: list[dict[str, str]] = []
    for block in blocks[1:]:
        fenced = re.search(r"```text\s*(.*?)\s*```", block, re.DOTALL)
        if not fenced:
            continue
        candidate_text = clean_candidate_text(fenced.group(1))
        if not candidate_text:
            continue
        meta = dict(re.findall(r"(?m)^- ([a-zA-Z_-]+):\s*(.+)$", block))
        items.append(
            {
                "text": candidate_text,
                "normalized": normalize_memory_text(candidate_text),
                "category": meta.get("category", "review"),
                "safety": meta.get("safety", "review"),
                "status": meta.get("status", "review"),
                "file": str(path),
            }
        )
    return items


def merged_candidates(path: Path) -> list[dict[str, object]]:
    grouped: dict[str, dict[str, object]] = {}
    for file in markdown_files_recursive(path):
        for item in candidate_blocks(file):
            normalized = str(item["normalized"])
            if not normalized:
                continue
            entry = grouped.setdefault(
                normalized,
                {
                    "text": item["text"],
                    "category": item["category"],
                    "safety": item["safety"],
                    "status": item["status"],
                    "occurrences": 0,
                    "files": set(),
                },
            )
            entry["occurrences"] = int(entry["occurrences"]) + 1
            files = entry["files"]
            if isinstance(files, set):
                files.add(item["file"])
            if len(str(item["text"])) > len(str(entry["text"])):
                entry["text"] = item["text"]
            if entry["safety"] != "blocked" and item["safety"] == "blocked":
                entry["safety"] = "blocked"
            if entry["status"] == "review" and item["status"] != "review":
                entry["status"] = item["status"]
    merged = []
    for entry in grouped.values():
        files = entry["files"] if isinstance(entry["files"], set) else set()
        merged.append(
            {
                "text": str(entry["text"]),
                "category": str(entry["category"]),
                "safety": str(entry["safety"]),
                "status": str(entry["status"]),
                "occurrences": int(entry["occurrences"]),
                "file_count": len(files),
                "files": sorted(str(file) for file in files),
            }
        )
    return sorted(
        merged,
        key=lambda item: (-int(item["occurrences"]), -int(item["file_count"]), str(item["text"]).lower()),
    )


def action_for(area: str, item: dict[str, object]) -> str:
    safety = str(item["safety"])
    occurrences = int(item["occurrences"])
    category = str(item["category"])
    if safety == "blocked":
        return "Inspect blocked candidate before any promotion"
    if area == "memory_candidates" and occurrences >= 2 and category == "user_preference":
        return "Review repeated safe preference for possible USER.md promotion"
    if area == "skill_patches":
        return "Review skill patch candidate and target skill before applying"
    if area == "skill_candidates":
        return "Review reusable workflow and scan before creating a skill"
    return "Review candidate manually"


def shell_quote(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


def promotion_option_for(area: str, item: dict[str, object]) -> str:
    text = str(item["text"])
    if area == "memory_candidates" and str(item["safety"]) != "blocked":
        return f"python \"$HOME/.agents/skills/memory-capture/scripts/promote_memory.py\" --text {shell_quote(text)} --approved"
    if area == "skill_candidates":
        return "Run scan_skill_candidates.py, then create or update a skill manually after review."
    if area == "skill_patches":
        return "Inspect target SKILL.md, run scan_skill_candidates.py, then apply the patch manually after review."
    return "Review manually before promotion."


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
        "candidates": {
            name: merged_candidates(path)
            for name, path in dirs.items()
            if name in {"memory_candidates", "skill_candidates", "skill_patches"}
        },
        "skills_with_usage": len(usage.get("skills", {})),
    }
    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0
    action_rows: list[tuple[str, str, dict[str, object]]] = []
    for area, items in summary["candidates"].items():
        for item in items[:5]:
            action_rows.append((area, action_for(area, item), item))
    action_rows.sort(key=lambda row: (-int(row[2]["occurrences"]), str(row[0]), str(row[2]["text"]).lower()))
    lines = [
        "# Learning Inbox Review Digest",
        "",
        f"- root: {root}",
        f"- skills_with_usage: {summary['skills_with_usage']}",
        f"- open_review_items: {sum(len(items) for items in summary['candidates'].values())}",
        "",
        "## Action Queue",
        "",
        "| Area | Action | Candidate | Evidence |",
        "| --- | --- | --- | --- |",
    ]
    if action_rows:
        for area, action, item in action_rows[:10]:
            text = str(item["text"])
            excerpt = text if len(text) <= 160 else text[:157] + "..."
            lines.append(
                f"| {area} | {action} | {excerpt} | occurrences: {item['occurrences']}, files: {item['file_count']} |"
            )
    else:
        lines.append("| all | No open candidates detected | None | occurrences: 0, files: 0 |")
    lines.extend(["", "## Area Overview", "", "| Area | Files | Merged Candidates |", "| --- | ---: | ---: |"])
    for name, count in summary["counts"].items():
        merged_count = len(summary["candidates"].get(name, []))
        lines.append(f"| {name} | {count} | {merged_count} |")
    lines.extend(["", "## Promotion Options", ""])
    for name, items in summary["candidates"].items():
        lines.append(f"### {name}")
        if not items:
            lines.append("- None")
        for index, item in enumerate(items[:5], start=1):
            text = str(item["text"])
            excerpt = text if len(text) <= 180 else text[:177] + "..."
            lines.extend(
                [
                    f"{index}. {excerpt}",
                    f"   - evidence: occurrences: {item['occurrences']}, files: {item['file_count']}",
                    f"   - option: {promotion_option_for(name, item)}",
                ]
            )
        lines.append("")
    lines.extend(["", "## Candidate Highlights", ""])
    for name, items in summary["candidates"].items():
        lines.append(f"### {name}")
        if not items:
            lines.append("- None")
        for item in items[:5]:
            lines.extend(
                [
                    f"- {item['text']}",
                    f"  - category: {item['category']}",
                    f"  - safety: {item['safety']}",
                    f"  - status: {item['status']}",
                    f"  - occurrences: {item['occurrences']}, files: {item['file_count']}",
                ]
            )
        lines.append("")
    lines.extend(["## Latest Files", ""])
    for name, files in summary["latest"].items():
        lines.append(f"### {name}")
        lines.extend([f"- {file}" for file in files] or ["- None"])
        lines.append("")
    write_text(report_path, "\n".join(lines))
    print(f"Learning inbox review digest written: {report_path}")
    print(
        "Review digest summary: "
        f"memory_candidates={len(summary['candidates'].get('memory_candidates', []))}, "
        f"skill_candidates={len(summary['candidates'].get('skill_candidates', []))}, "
        f"skill_patches={len(summary['candidates'].get('skill_patches', []))}"
    )
    print(f"Promotion options: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
