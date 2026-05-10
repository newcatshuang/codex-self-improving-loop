#!/usr/bin/env python3
"""Record lightweight skill usage metadata."""

from __future__ import annotations

import argparse
from pathlib import Path

from learning_loop_common import default_codex_root, now_iso, read_usage, write_usage


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_codex_root())
    parser.add_argument("--usage-file", type=Path)
    parser.add_argument("--skill-name", required=True)
    parser.add_argument("--status", default="success", choices=["success", "failure", "review"])
    parser.add_argument("--notes", default="")
    args = parser.parse_args()
    usage_file = args.usage_file.expanduser() if args.usage_file else args.root.expanduser() / "skill-usage.json"
    data = read_usage(usage_file)
    skills = data.setdefault("skills", {})
    entry = skills.setdefault(args.skill_name, {"use_count": 0, "failure_count": 0, "last_used": None, "events": []})
    entry["use_count"] = int(entry.get("use_count", 0)) + 1
    if args.status == "failure":
        entry["failure_count"] = int(entry.get("failure_count", 0)) + 1
    entry["last_used"] = now_iso()
    events = entry.setdefault("events", [])
    events.append({"at": entry["last_used"], "status": args.status, "notes": args.notes})
    entry["events"] = events[-20:]
    write_usage(usage_file, data)
    print(f"Recorded usage for {args.skill_name}: {usage_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
