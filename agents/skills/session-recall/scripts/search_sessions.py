#!/usr/bin/env python3
"""Search local Codex sessions and return redacted snippets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
COMMON_DIR = None
for ancestor in SCRIPT_DIR.parents:
    for candidate in (
        ancestor / "memory-capture" / "scripts",
        ancestor / "skills" / "memory-capture" / "scripts",
    ):
        if (candidate / "learning_loop_common.py").exists():
            COMMON_DIR = candidate
            break
    if COMMON_DIR:
        break
if COMMON_DIR is None:
    raise RuntimeError("Could not locate memory-capture/scripts/learning_loop_common.py")
sys.path.insert(0, str(COMMON_DIR))

from learning_loop_common import default_codex_root, iter_session_files, parse_jsonish_line, redact, tokenize_query


def make_snippet(text: str, terms: list[str], width: int = 220) -> str:
    lowered = text.lower()
    positions = [lowered.find(term) for term in terms if term and lowered.find(term) >= 0]
    pos = min(positions) if positions else 0
    start = max(0, pos - width // 3)
    end = min(len(text), start + width)
    snippet = text[start:end].replace("\n", " ")
    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet += "..."
    return redact(snippet)


def search(root: Path, query: str, max_results: int) -> list[dict[str, object]]:
    terms = tokenize_query(query)
    results: list[dict[str, object]] = []
    for path in iter_session_files(root):
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except TypeError:
            lines = path.read_text(encoding="utf-8").splitlines()
        for number, line in enumerate(lines, start=1):
            text = parse_jsonish_line(line)
            if not text:
                continue
            lowered = text.lower()
            score = sum(1 for term in terms if term in lowered)
            if score == 0:
                continue
            results.append(
                {
                    "file": str(path),
                    "line": number,
                    "score": score,
                    "modified": path.stat().st_mtime,
                    "snippet": make_snippet(text, terms),
                }
            )
    results.sort(key=lambda item: (item["score"], item["modified"]), reverse=True)
    return results[:max_results]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", "-q", required=True, help="Search query")
    parser.add_argument("--root", type=Path, default=default_codex_root(), help="Codex root directory")
    parser.add_argument("--max-results", type=int, default=10, help="Maximum results")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    results = search(args.root.expanduser(), args.query, args.max_results)
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 0
    if not results:
        print("No matching session snippets found.")
        return 1
    for index, result in enumerate(results, start=1):
        print(f"## Result {index}")
        print(f"- file: {result['file']}")
        print(f"- line: {result['line']}")
        print(f"- score: {result['score']}")
        print()
        print(result["snippet"])
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
