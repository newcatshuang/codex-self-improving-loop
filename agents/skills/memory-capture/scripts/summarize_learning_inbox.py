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


def is_push_retry_rule(text: str) -> bool:
    return bool(re.search(r"(?i)(push|推送)", text) and re.search(r"(?i)(retry|重试|最多.*3|3 次|three)", text))


def is_sql_preference(text: str) -> bool:
    return bool(re.search(r"(?i)(sql|query|select\s+\*|不应该返回\*)", text))


def is_project_data_fact(text: str) -> bool:
    return bool(re.search(r"(?i)(table|field|表名|核心字段|数据库|bms\.|soms\.|fin_|fee_type|order_id|/[^/\s]+/[^/\s]+)", text))


def is_transcript_artifact(text: str) -> bool:
    return bool(text.startswith("::") or text.startswith("![") or text.startswith("+二次改稿说明"))


def destination_for(area: str, item: dict[str, object]) -> str:
    text = str(item["text"])
    lower = text.lower()
    safety = str(item["safety"])
    category = str(item["category"])
    if safety == "blocked":
        return "blocked_review"
    if area == "skill_patches":
        return "skill_patch"
    if area == "skill_candidates":
        return "skill_candidate"
    if area != "memory_candidates":
        return "manual_review"
    if is_transcript_artifact(text):
        return "manual_review"
    if is_push_retry_rule(text):
        return "global_user_memory"
    if is_sql_preference(text):
        return "global_user_memory"
    if is_project_data_fact(text):
        return "project_agents"
    project_markers = (
        "github trending",
        "github 官方趋势",
        "github 趋势",
        "article.md",
        "publishing-notes.md",
        "cover-preview.png",
        "verify-daily-post",
        "daily-post",
        "visiblecount",
        "项目事实",
        "仓库",
    )
    if any(marker in lower for marker in project_markers):
        return "project_agents"
    if category == "workflow_pattern":
        return "skill_candidate"
    if "skill" in lower and ("missing" in lower or "缺" in lower or "patch" in lower or "补丁" in lower):
        return "skill_patch"
    if category in {"user_preference", "safety_rule"}:
        return "global_user_memory"
    return "manual_review"


def rewrite_suggestion_for(area: str, item: dict[str, object]) -> str:
    text = clean_candidate_text(str(item["text"]))
    lower = text.lower()
    destination = destination_for(area, item)
    if destination == "blocked_review":
        return "Do not rewrite until the blocked safety finding is reviewed."
    if is_push_retry_rule(text):
        return "When git push fails due to environment or network access, retry at most three times; if still blocked, stop and report the commit hash, remote, failure reason, and a manual push command instead of claiming success."
    if is_sql_preference(text):
        return "When writing SQL, verify table columns before drafting queries; avoid SELECT * by default and select only the required fields."
    if "github trending" in lower or "github 官方趋势" in lower or "github 趋势" in lower:
        return "For GitHub Trending publishing workflows, use https://github.com/trending as the source of truth; do not replace the official daily page with GitTrend, search results, history, or adjacent time windows."
    if area == "skill_candidates":
        return "Convert this repeated workflow into a small SKILL.md with trigger conditions, steps, verification, and safety notes."
    if area == "skill_patches":
        return "Patch the named target SKILL.md only after inspecting the skill and running the skill-candidate safety scan."
    if destination == "project_agents":
        return f"Move this project-specific rule into the nearest project AGENTS.md: {text}"
    if destination == "global_user_memory":
        return text.rstrip(".。")
    return "Rewrite as one short, durable rule before promotion."


def shell_quote(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


def promotion_option_for(area: str, item: dict[str, object]) -> str:
    destination = destination_for(area, item)
    rewrite = rewrite_suggestion_for(area, item)
    if destination == "global_user_memory" and str(item["safety"]) != "blocked":
        return f"python \"$HOME/.agents/skills/memory-capture/scripts/promote_memory.py\" --text {shell_quote(rewrite)} --approved"
    if destination == "project_agents":
        return "Move the rewritten rule into the nearest project AGENTS.md after review."
    if area == "skill_candidates":
        return "Run scan_skill_candidates.py, then create or update a skill manually after review."
    if area == "skill_patches":
        return "Inspect target SKILL.md, run scan_skill_candidates.py, then apply the patch manually after review."
    return "Review manually before promotion."


def short_text(value: object, limit: int = 120) -> str:
    text = clean_candidate_text(str(value)).replace("\n", " ")
    return text if len(text) <= limit else text[: limit - 3] + "..."


def markdown_cell(value: object, limit: int = 120) -> str:
    text = short_text(value, limit)
    return text.replace("|", "\\|")


def index_counts(payload: dict[str, object]) -> dict[str, int]:
    candidates = payload.get("candidates", [])
    counts = {"memory_candidates": 0, "skill_candidates": 0, "skill_patches": 0}
    if not isinstance(candidates, list):
        return counts
    for item in candidates:
        if isinstance(item, dict):
            area = str(item.get("area", ""))
            if area in counts:
                counts[area] += 1
    return counts


def write_light_digest(root: Path, payload: dict[str, object], report_path: Path, index_path: Path | None) -> None:
    candidates_raw = payload.get("candidates", [])
    candidates = [item for item in candidates_raw if isinstance(item, dict)] if isinstance(candidates_raw, list) else []
    summary = payload.get("summary", {}) if isinstance(payload.get("summary"), dict) else {}
    dashboard_path = root / "codex-self-improving-loop-dashboard.html"
    index_display = index_path or Path(str(payload.get("index_path") or root / "learning-index.json"))
    action_rows = sorted(
        candidates,
        key=lambda item: (-int(item.get("occurrences", 0)), str(item.get("area", "")), str(item.get("text", "")).lower()),
    )
    lines = [
        "# Learning Inbox Review Digest",
        "",
        f"- root: {root}",
        f"- open_review_items: {summary.get('total_candidates', len(candidates))}",
        f"- dashboard: {dashboard_path}",
        f"- learning_index: {index_display}",
        "",
        "## Review Entry Points",
        "",
        "| Entry | Path | Purpose |",
        "| --- | --- | --- |",
        f"| WebUI Dashboard | {dashboard_path} | Review today, history, summaries, and copy commands. |",
        f"| Shared Index | {index_display} | Shared JSON data used by the dashboard and this digest. |",
        f"| Latest Summary | {root / 'learning-inbox-summary.md'} | Longer Markdown review report when details are needed. |",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Total Candidates | {summary.get('total_candidates', len(candidates))} |",
        f"| Today Candidates | {summary.get('today_candidates', 0)} |",
    ]
    by_area = summary.get("by_area", {}) if isinstance(summary.get("by_area"), dict) else {}
    for area in ("memory_candidates", "skill_candidates", "skill_patches"):
        lines.append(f"| {area} | {by_area.get(area, 0)} |")
    lines.extend(
        [
            "",
            "## Action Queue",
            "",
            "| Area | Destination | Action | Candidate | Evidence | Option |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    if action_rows:
        for item in action_rows[:12]:
            area = str(item.get("area", "manual_review"))
            action = action_for(area, item)
            evidence = f"occurrences: {item.get('occurrences', 0)}, files: {item.get('file_count', 0)}"
            lines.append(
                "| "
                + " | ".join(
                    [
                        markdown_cell(area, 48),
                        markdown_cell(item.get("destination", "manual_review"), 56),
                        markdown_cell(action, 96),
                        markdown_cell(item.get("rewrite_suggestion") or item.get("text", ""), 140),
                        markdown_cell(evidence, 56),
                        markdown_cell(item.get("promotion_option", "Review manually before promotion."), 120),
                    ]
                )
                + " |"
            )
    else:
        lines.append("| all | none | No open candidates detected | None | occurrences: 0, files: 0 | Review manually before promotion. |")
    write_text(report_path, "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_codex_root())
    parser.add_argument("--usage-file", type=Path)
    parser.add_argument("--report-path", type=Path)
    parser.add_argument("--index-path", type=Path, help="Read candidates from an existing learning-index.json payload")
    parser.add_argument("--light", action="store_true", help="Write a compact digest with review entry points and an action queue")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = args.root.expanduser()
    usage_file = args.usage_file.expanduser() if args.usage_file else root / "skill-usage.json"
    report_path = args.report_path.expanduser() if args.report_path else root / "learning-inbox-summary.md"
    index_path = args.index_path.expanduser() if args.index_path else None
    if index_path:
        payload = json.loads(index_path.read_text(encoding="utf-8"))
        if args.json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
            return 0
        if args.light:
            write_light_digest(root, payload, report_path, index_path)
            counts = index_counts(payload)
            print(f"Learning inbox review digest written: {report_path}")
            print(
                "Review digest summary: "
                f"memory_candidates={counts['memory_candidates']}, "
                f"skill_candidates={counts['skill_candidates']}, "
                f"skill_patches={counts['skill_patches']}"
            )
            print(f"Promotion options: {report_path}")
            return 0
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
    for area, items in summary["candidates"].items():
        for item in items:
            item["destination"] = destination_for(area, item)
            item["rewrite_suggestion"] = rewrite_suggestion_for(area, item)
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
        "| Area | Destination | Action | Candidate | Rewrite Suggestion | Evidence |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    if action_rows:
        for area, action, item in action_rows[:10]:
            text = str(item["text"])
            excerpt = text if len(text) <= 160 else text[:157] + "..."
            rewrite = rewrite_suggestion_for(area, item)
            rewrite_excerpt = rewrite if len(rewrite) <= 160 else rewrite[:157] + "..."
            lines.append(
                f"| {area} | {destination_for(area, item)} | {action} | {excerpt} | {rewrite_excerpt} | occurrences: {item['occurrences']}, files: {item['file_count']} |"
            )
    else:
        lines.append("| all | none | No open candidates detected | None | None | occurrences: 0, files: 0 |")
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
                    f"   - destination: {destination_for(name, item)}",
                    f"   - rewrite: {rewrite_suggestion_for(name, item)}",
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
                    f"  - destination: {destination_for(name, item)}",
                    f"  - rewrite: {rewrite_suggestion_for(name, item)}",
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
