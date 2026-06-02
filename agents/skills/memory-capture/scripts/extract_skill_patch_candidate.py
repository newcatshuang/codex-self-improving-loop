#!/usr/bin/env python3
"""Extract review-only patch candidates for existing skills."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from learning_loop_common import clean_candidate_text, default_codex_root, is_patch_candidate_text, latest_session_file, normalize_memory_text, read_session_messages, split_learning_fragments, write_candidate_report


def suggest_patch_candidates(messages: list[str], skill_name: str | None, limit: int = 8) -> list[str]:
    candidates: list[str] = []
    seen: set[str] = set()
    for message in reversed(messages):
        for fragment in split_learning_fragments(message):
            compact = clean_candidate_text(fragment)
            if not is_patch_candidate_text(compact, skill_name):
                continue
            if skill_name and skill_name.lower() not in compact.lower():
                compact = f"Target skill: {skill_name}. Evidence: {compact}"
            excerpt = compact[:600]
            key = normalize_memory_text(excerpt)
            if key in seen:
                continue
            seen.add(key)
            candidates.append(excerpt)
            if len(candidates) >= limit:
                return candidates
    return candidates


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_codex_root(), help="Codex root directory")
    parser.add_argument("--session-file", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--skill-name", help="Target skill name")
    parser.add_argument("--max-messages", type=int, default=80)
    parser.add_argument("--pass-thru", action="store_true")
    parser.add_argument("--write-empty", action="store_true", help="Write an empty report when no candidates are detected")
    args = parser.parse_args()
    root = args.root.expanduser()
    session = args.session_file.expanduser() if args.session_file else latest_session_file(root)
    output_dir = args.output_dir.expanduser() if args.output_dir else root / "skill-candidates" / "patches"
    messages = read_session_messages(session, args.max_messages) if session else []
    candidates = suggest_patch_candidates(messages, args.skill_name)
    if not candidates and not args.write_empty:
        print("No skill patch candidates detected; report skipped.")
        print("Candidates: 0")
        return 0
    suffix = "-" + hashlib.sha1(str(session.expanduser().resolve()).encode("utf-8")).hexdigest()[:8] if session else ""
    path = write_candidate_report(output_dir, "Skill Patch Candidates", candidates, str(session or "no session found"), "skill-patch-candidates", suffix=suffix)
    print(path if args.pass_thru else f"Skill patch candidate report written: {path}")
    print(f"Candidates: {len(candidates)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
