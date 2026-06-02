#!/usr/bin/env python3
"""Score memory candidates, optionally auto-promote safe repeated preferences, and archive processed files."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path

from learning_loop_common import (
    clean_candidate_text,
    contains_secret_like_text,
    default_codex_root,
    ensure_dir,
    is_noisy_learning_line,
    markdown_files_recursive,
    normalize_memory_text,
    read_text,
    write_text,
)


def extract_candidate_blocks(path: Path) -> list[str]:
    content = read_text(path)
    blocks = re.findall(r"```text\s*(.*?)```", content, flags=re.DOTALL | re.IGNORECASE)
    candidates = []
    for block in blocks:
        candidate = clean_candidate_text(block)
        if not candidate or is_noisy_learning_line(candidate):
            continue
        candidates.append(candidate)
    return candidates


def merge_candidate_items(items: list[tuple[Path, str]]) -> list[dict[str, object]]:
    grouped: dict[str, dict[str, object]] = {}
    for path, text in items:
        normalized = normalize_memory_text(text)
        if not normalized:
            continue
        entry = grouped.setdefault(
            normalized,
            {
                "text": text,
                "normalized": normalized,
                "occurrences": 0,
                "files": set(),
                "examples": [],
            },
        )
        entry["occurrences"] = int(entry["occurrences"]) + 1
        files = entry["files"]
        if isinstance(files, set):
            files.add(path)
        examples = entry["examples"]
        if isinstance(examples, list) and len(examples) < 3:
            examples.append({"file": str(path), "text": text})
        if len(text) > len(str(entry["text"])):
            entry["text"] = text
    merged = []
    for entry in grouped.values():
        files = entry["files"]
        file_set = files if isinstance(files, set) else set()
        examples = entry["examples"] if isinstance(entry["examples"], list) else []
        merged.append(
            {
                "text": str(entry["text"]),
                "normalized": str(entry["normalized"]),
                "occurrences": int(entry["occurrences"]),
                "file_count": len(file_set),
                "files": sorted(str(path) for path in file_set),
                "examples": examples,
            }
        )
    return sorted(
        merged,
        key=lambda item: (-int(item["occurrences"]), -int(item["file_count"]), str(item["text"]).lower()),
    )


def status_for(text: str, existing_normalized: set[str], occurrences: int) -> str:
    normalized = normalize_memory_text(text)
    if contains_secret_like_text(text):
        return "blocked"
    if normalized in existing_normalized:
        return "already_present"
    category = "preference" if re.search(r"(?i)(prefer|default|always|never|avoid|以后|默认|记住|不要)", text) else "review"
    if category == "preference" and len(text) <= 180 and occurrences >= 2:
        return "auto_promote_candidate"
    return "review"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_codex_root(), help="Codex root directory")
    parser.add_argument("--inbox", type=Path, help="Memory candidate inbox")
    parser.add_argument("--target", type=Path, help="USER.md path")
    parser.add_argument("--auto-promote", action="store_true", help="Promote safe auto candidates")
    parser.add_argument("--archive-processed", action="store_true", help="Archive files with no unresolved candidates")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    root = args.root.expanduser()
    inbox = args.inbox.expanduser() if args.inbox else root / "memories" / "inbox"
    target = args.target.expanduser() if args.target else root / "memories" / "USER.md"
    archive = root / "memories" / "archive"
    files = markdown_files_recursive(inbox)
    existing = read_text(target)
    existing_normalized = {normalize_memory_text(line.lstrip("- ").strip()) for line in existing.splitlines() if line.strip().startswith("-")}

    all_items: list[tuple[Path, str]] = []
    for path in files:
        all_items.extend((path, text) for text in extract_candidate_blocks(path))
    merged_items = merge_candidate_items(all_items)

    report_items = []
    promoted: list[str] = []
    unresolved_by_file: dict[Path, int] = defaultdict(int)
    for item in merged_items:
        text = str(item["text"])
        occurrences = int(item["occurrences"])
        status = status_for(text, existing_normalized, occurrences)
        if status == "auto_promote_candidate" and args.auto_promote:
            existing = read_text(target)
            write_text(target, existing.rstrip() + f"\n- {text.strip()}\n")
            existing_normalized.add(normalize_memory_text(text))
            status = "promoted"
            promoted.append(text)
        files_for_item = [Path(file) for file in item["files"] if isinstance(file, str)]
        if status in {"review", "auto_promote_candidate"}:
            for path in files_for_item:
                unresolved_by_file[path] += 1
        report_items.append(
            {
                "text": text,
                "normalized": item["normalized"],
                "occurrences": occurrences,
                "file_count": item["file_count"],
                "files": item["files"],
                "examples": item["examples"],
                "status": status,
            }
        )

    archived = []
    if args.archive_processed:
        ensure_dir(archive)
        for path in files:
            if unresolved_by_file.get(path, 0) == 0:
                try:
                    relative = path.relative_to(inbox)
                except ValueError:
                    relative = Path(path.name)
                destination = archive / relative
                ensure_dir(destination.parent)
                shutil.move(str(path), str(destination))
                archived.append(str(destination))

    summary = {
        "candidate_files": len(files),
        "candidate_count": len(all_items),
        "merged_candidate_count": len(merged_items),
        "promoted_count": len(promoted),
        "archived_count": len(archived),
        "items": report_items,
        "archived": archived,
    }
    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print("# Memory Candidate Promotion Report")
        print()
        print(f"- candidate_files: {summary['candidate_files']}")
        print(f"- candidate_count: {summary['candidate_count']}")
        print(f"- merged_candidate_count: {summary['merged_candidate_count']}")
        print(f"- promoted_count: {summary['promoted_count']}")
        print(f"- archived_count: {summary['archived_count']}")
        print()
        for item in report_items:
            print(f"- [{item['status']}] {item['text']} (occurrences: {item['occurrences']}, files: {item['file_count']})")
            for example in item.get("examples", [])[:2]:
                print(f"  - source: {example['file']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
