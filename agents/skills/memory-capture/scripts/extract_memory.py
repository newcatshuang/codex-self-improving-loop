#!/usr/bin/env python3
"""Extract review-only memory candidates from the latest Codex session."""

from __future__ import annotations

import argparse
from pathlib import Path

from learning_loop_common import (
    default_codex_root,
    latest_session_file,
    read_session_messages,
    suggest_memory_candidates,
    write_candidate_report,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_codex_root(), help="Codex root directory")
    parser.add_argument("--session-file", type=Path, help="Specific session file")
    parser.add_argument("--output-dir", type=Path, help="Memory candidate inbox")
    parser.add_argument("--max-messages", type=int, default=80, help="Messages to inspect from session tail")
    parser.add_argument("--pass-thru", action="store_true", help="Print generated candidate file path only")
    args = parser.parse_args()

    root = args.root.expanduser()
    session = args.session_file.expanduser() if args.session_file else latest_session_file(root)
    output_dir = args.output_dir.expanduser() if args.output_dir else root / "memories" / "inbox"
    if not session:
        path = write_candidate_report(output_dir, "Memory Candidates", [], "no session found", "memory-candidates")
        print(path if args.pass_thru else f"Memory candidate report written: {path}")
        return 1
    messages = read_session_messages(session, args.max_messages)
    candidates = suggest_memory_candidates(messages)
    path = write_candidate_report(output_dir, "Memory Candidates", candidates, str(session), "memory-candidates")
    print(path if args.pass_thru else f"Memory candidate report written: {path}")
    print(f"Candidates: {len(candidates)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
