#!/usr/bin/env python3
"""Extract review-only patch candidates for existing skills."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from learning_loop_common import clean_candidate_text, default_codex_root, is_noisy_learning_line, latest_session_file, read_session_messages, split_learning_fragments, write_candidate_report


def suggest_patch_candidates(messages: list[str], skill_name: str | None, limit: int = 8) -> list[str]:
    import re

    signals = re.compile(r"(?i)(skill|SKILL\\.md|patch|pitfall|workaround|missing|improve|regression|root cause|技能|补丁|缺口|改进|回归|根因|踩坑)")
    candidates: list[str] = []
    for message in reversed(messages):
        for fragment in split_learning_fragments(message):
            compact = clean_candidate_text(fragment)
            if len(compact) < 30 or not signals.search(compact):
                continue
            if is_noisy_learning_line(compact):
                continue
            if skill_name and skill_name.lower() not in compact.lower():
                compact = f"Target skill: {skill_name}. Evidence: {compact}"
            candidates.append(compact[:600])
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
    args = parser.parse_args()
    root = args.root.expanduser()
    session = args.session_file.expanduser() if args.session_file else latest_session_file(root)
    output_dir = args.output_dir.expanduser() if args.output_dir else root / "skill-candidates" / "patches"
    messages = read_session_messages(session, args.max_messages) if session else []
    candidates = suggest_patch_candidates(messages, args.skill_name)
    suffix = "-" + hashlib.sha1(str(session.expanduser().resolve()).encode("utf-8")).hexdigest()[:8] if session else ""
    path = write_candidate_report(output_dir, "Skill Patch Candidates", candidates, str(session or "no session found"), "skill-patch-candidates", suffix=suffix)
    print(path if args.pass_thru else f"Skill patch candidate report written: {path}")
    print(f"Candidates: {len(candidates)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
