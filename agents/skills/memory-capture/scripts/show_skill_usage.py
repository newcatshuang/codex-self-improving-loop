#!/usr/bin/env python3
"""Show skill usage metadata."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from learning_loop_common import default_codex_root, read_usage


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_codex_root())
    parser.add_argument("--usage-file", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    usage_file = args.usage_file.expanduser() if args.usage_file else args.root.expanduser() / "skill-usage.json"
    data = read_usage(usage_file)
    rows = []
    for name, entry in data.get("skills", {}).items():
        rows.append(
            {
                "skill": name,
                "use_count": entry.get("use_count", 0),
                "failure_count": entry.get("failure_count", 0),
                "last_used": entry.get("last_used"),
            }
        )
    rows.sort(key=lambda row: (row["use_count"], row["last_used"] or ""), reverse=True)
    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        print("| Skill | Uses | Failures | Last Used |")
        print("| --- | ---: | ---: | --- |")
        for row in rows:
            print(f"| {row['skill']} | {row['use_count']} | {row['failure_count']} | {row['last_used'] or ''} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
