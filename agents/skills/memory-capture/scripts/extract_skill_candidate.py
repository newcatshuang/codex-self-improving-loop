#!/usr/bin/env python3
"""Extract review-only skill candidates from the latest session."""

from __future__ import annotations

import argparse
from pathlib import Path

from learning_loop_common import clean_candidate_text, default_codex_root, is_noisy_learning_line, latest_session_file, read_session_messages, write_candidate_report


def suggest_skill_candidates(messages: list[str], limit: int = 8) -> list[str]:
    import re

    signals = re.compile(r"(?i)(workflow|procedure|skill|reusable|repeat|verification|pitfall|流程|步骤|技能|复用|验证|踩坑)")
    candidates: list[str] = []
    seen: set[str] = set()
    for message in reversed(messages):
        compact = clean_candidate_text(" ".join(line.strip() for line in message.splitlines() if line.strip()))
        if len(compact) < 30:
            continue
        if is_noisy_learning_line(compact):
            continue
        if not signals.search(compact):
            continue
        excerpt = compact[:500]
        key = excerpt.lower()
        if key in seen:
            continue
        seen.add(key)
        candidates.append(excerpt)
        if len(candidates) >= limit:
            break
    return candidates


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_codex_root(), help="Codex root directory")
    parser.add_argument("--session-file", type=Path, help="Specific session file")
    parser.add_argument("--output-dir", type=Path, help="Skill candidate inbox")
    parser.add_argument("--max-messages", type=int, default=80)
    parser.add_argument("--pass-thru", action="store_true")
    args = parser.parse_args()
    root = args.root.expanduser()
    session = args.session_file.expanduser() if args.session_file else latest_session_file(root)
    output_dir = args.output_dir.expanduser() if args.output_dir else root / "skill-candidates" / "inbox"
    messages = read_session_messages(session, args.max_messages) if session else []
    candidates = suggest_skill_candidates(messages)
    path = write_candidate_report(output_dir, "Skill Candidates", candidates, str(session or "no session found"), "skill-candidates")
    print(path if args.pass_thru else f"Skill candidate report written: {path}")
    print(f"Candidates: {len(candidates)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
