#!/usr/bin/env python3
"""Build the shared learning index for digest and dashboard renderers."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from learning_loop_common import default_codex_root, markdown_files_recursive, normalize_memory_text, now_iso, write_text
from summarize_learning_inbox import candidate_blocks, destination_for, promotion_option_for, rewrite_suggestion_for


AREAS = {
    "memory_candidates": ("Memory", ("memories", "inbox")),
    "skill_candidates": ("Skill", ("skill-candidates", "inbox")),
    "skill_patches": ("Patch", ("skill-candidates", "patches")),
}


def date_from_path(path: Path) -> str:
    parts = path.parts
    for index in range(0, max(len(parts) - 2, 0)):
        year, month, day = parts[index : index + 3]
        if re.fullmatch(r"\d{4}", year) and re.fullmatch(r"\d{2}", month) and re.fullmatch(r"\d{2}", day):
            return f"{year}-{month}-{day}"
    return "unknown"


def compact_path(path: str, root: Path) -> str:
    candidate = Path(path)
    try:
        return str(candidate.relative_to(root))
    except ValueError:
        return path


def merge_area_candidates(root: Path, area: str, directory: Path) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for file in markdown_files_recursive(directory):
        source_date = date_from_path(file)
        for item in candidate_blocks(file):
            normalized = str(item.get("normalized") or normalize_memory_text(str(item.get("text", ""))))
            if not normalized:
                continue
            key = f"{area}:{normalized}"
            entry = grouped.setdefault(
                key,
                {
                    "area": area,
                    "area_label": AREAS[area][0],
                    "text": str(item["text"]),
                    "category": str(item.get("category", "review")),
                    "safety": str(item.get("safety", "review")),
                    "status": str(item.get("status", "review")),
                    "occurrences": 0,
                    "files": set(),
                    "dates": set(),
                },
            )
            entry["occurrences"] = int(entry["occurrences"]) + 1
            entry["files"].add(str(file))
            entry["dates"].add(source_date)
            if len(str(item["text"])) > len(str(entry["text"])):
                entry["text"] = str(item["text"])
            if entry["safety"] != "blocked" and item.get("safety") == "blocked":
                entry["safety"] = "blocked"
            if entry["status"] == "review" and item.get("status") != "review":
                entry["status"] = str(item.get("status"))
            if entry["category"] == "review" and item.get("category") != "review":
                entry["category"] = str(item.get("category"))
    merged: list[dict[str, Any]] = []
    for index, entry in enumerate(grouped.values(), start=1):
        dates = sorted(str(item) for item in entry["dates"])
        files = sorted(compact_path(str(file), root) for file in entry["files"])
        item_for_rules = {
            "text": str(entry["text"]),
            "category": str(entry["category"]),
            "safety": str(entry["safety"]),
            "status": str(entry["status"]),
            "occurrences": int(entry["occurrences"]),
            "file_count": len(files),
            "files": files,
        }
        entry_id = f"{area}-{index}"
        merged.append(
            {
                "id": entry_id,
                "area": area,
                "area_label": AREAS[area][0],
                "text": item_for_rules["text"],
                "category": item_for_rules["category"],
                "safety": item_for_rules["safety"],
                "status": item_for_rules["status"],
                "occurrences": item_for_rules["occurrences"],
                "file_count": item_for_rules["file_count"],
                "files": files,
                "dates": dates,
                "latest_date": max(dates) if dates else "unknown",
                "destination": destination_for(area, item_for_rules),
                "rewrite_suggestion": rewrite_suggestion_for(area, item_for_rules),
                "promotion_option": promotion_option_for(area, item_for_rules),
            }
        )
    return sorted(
        merged,
        key=lambda item: (
            str(item["latest_date"]) != "unknown",
            str(item["latest_date"]),
            int(item["occurrences"]),
            int(item["file_count"]),
            str(item["text"]).lower(),
        ),
        reverse=True,
    )


def build_payload(root: Path, index_path: Path | None = None) -> dict[str, Any]:
    root = root.expanduser().resolve()
    today = datetime.now().strftime("%Y-%m-%d")
    candidates: list[dict[str, Any]] = []
    for area, (_, rel_parts) in AREAS.items():
        candidates.extend(merge_area_candidates(root, area, root.joinpath(*rel_parts)))

    known_dates = sorted({date for item in candidates for date in item["dates"] if date != "unknown"}, reverse=True)
    dates = sorted({today, *known_dates}, reverse=True)
    by_area = Counter(str(item["area"]) for item in candidates)
    by_destination = Counter(str(item["destination"]) for item in candidates)
    by_safety = Counter(str(item["safety"]) for item in candidates)
    by_date = Counter(date for item in candidates for date in item["dates"] if date != "unknown")
    summary = {
        "total_candidates": len(candidates),
        "today_candidates": int(by_date.get(today, 0)),
        "historical_dates": len(known_dates),
        "by_area": {area: int(by_area.get(area, 0)) for area in AREAS},
        "by_destination": dict(sorted(by_destination.items())),
        "by_safety": dict(sorted(by_safety.items())),
        "by_date": dict(sorted(by_date.items(), reverse=True)),
    }
    payload = {
        "version": 1,
        "generated_at": now_iso(),
        "root": str(root),
        "default_date": today,
        "dates": dates,
        "summary": summary,
        "candidates": candidates,
    }
    if index_path is not None:
        payload["index_path"] = str(index_path)
    return payload


def read_index(path: Path) -> dict[str, Any]:
    return json.loads(path.expanduser().read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_codex_root())
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = args.root.expanduser()
    output = args.output.expanduser() if args.output else root / "learning-index.json"
    payload = build_payload(root, output)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    write_text(output, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(f"Learning index written: {output}")
    print(
        "Learning index summary: "
        f"total={payload['summary']['total_candidates']}, "
        f"today={payload['summary']['today_candidates']}, "
        f"dates={len(payload['dates'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
