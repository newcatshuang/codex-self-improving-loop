#!/usr/bin/env python3
"""Score memory candidates, optionally auto-promote safe repeated preferences, and archive processed files."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path

from learning_loop_common import (
    clean_candidate_text,
    contains_secret_like_text,
    default_codex_root,
    ensure_dir,
    is_noisy_learning_line,
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
    files = sorted(inbox.glob("*.md")) if inbox.exists() else []
    existing = read_text(target)
    existing_normalized = {normalize_memory_text(line.lstrip("- ").strip()) for line in existing.splitlines() if line.strip().startswith("-")}

    all_items: list[tuple[Path, str]] = []
    for path in files:
        all_items.extend((path, text) for text in extract_candidate_blocks(path))
    counts = Counter(normalize_memory_text(text) for _, text in all_items)

    report_items = []
    promoted: list[str] = []
    unresolved_by_file: dict[Path, int] = defaultdict(int)
    for path, text in all_items:
        occurrences = counts[normalize_memory_text(text)]
        status = status_for(text, existing_normalized, occurrences)
        if status == "auto_promote_candidate" and args.auto_promote:
            existing = read_text(target)
            write_text(target, existing.rstrip() + f"\n- {text.strip()}\n")
            existing_normalized.add(normalize_memory_text(text))
            status = "promoted"
            promoted.append(text)
        if status in {"review", "auto_promote_candidate"}:
            unresolved_by_file[path] += 1
        report_items.append({"file": str(path), "text": text, "occurrences": occurrences, "status": status})

    archived = []
    if args.archive_processed:
        ensure_dir(archive)
        for path in files:
            if unresolved_by_file.get(path, 0) == 0:
                destination = archive / path.name
                shutil.move(str(path), str(destination))
                archived.append(str(destination))

    summary = {
        "candidate_files": len(files),
        "candidate_count": len(all_items),
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
        print(f"- promoted_count: {summary['promoted_count']}")
        print(f"- archived_count: {summary['archived_count']}")
        print()
        for item in report_items:
            print(f"- [{item['status']}] {item['text']} (occurrences: {item['occurrences']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
