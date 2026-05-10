#!/usr/bin/env python3
"""Generate a lightweight index of installed skills plus usage metadata."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from learning_loop_common import default_agents_root, default_codex_root, load_skill_metadata, read_usage, write_text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_codex_root())
    parser.add_argument("--skills-root", type=Path, default=default_agents_root() / "skills")
    parser.add_argument("--usage-file", type=Path)
    parser.add_argument("--output-path", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = args.root.expanduser()
    usage_file = args.usage_file.expanduser() if args.usage_file else root / "skill-usage.json"
    output_path = args.output_path.expanduser() if args.output_path else root / "skills-index.md"
    usage = read_usage(usage_file).get("skills", {})
    rows = []
    skills_root = args.skills_root.expanduser()
    for skill_dir in sorted(skills_root.iterdir()) if skills_root.exists() else []:
        if not skill_dir.is_dir() or not (skill_dir / "SKILL.md").exists():
            continue
        meta = load_skill_metadata(skill_dir)
        entry = usage.get(meta["name"], {})
        rows.append(
            {
                "name": meta["name"],
                "description": meta.get("description", ""),
                "path": str(skill_dir),
                "use_count": entry.get("use_count", 0),
                "last_used": entry.get("last_used", ""),
            }
        )
    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return 0
    lines = [
        "# Skills Index",
        "",
        f"- skills_root: {skills_root}",
        f"- usage_file: {usage_file}",
        "",
        "| Skill | Uses | Last Used | Description |",
        "| --- | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(f"| {row['name']} | {row['use_count']} | {row['last_used']} | {row['description']} |")
    write_text(output_path, "\n".join(lines) + "\n")
    print(f"Skills index written: {output_path}")
    print(f"Skill count: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
