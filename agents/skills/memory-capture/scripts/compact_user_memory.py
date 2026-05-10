#!/usr/bin/env python3
"""Report USER.md memory budget, duplicates, conflicts, and safety risks."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from learning_loop_common import contains_secret_like_text, default_codex_root, normalize_memory_text, read_text, write_text


def analyze(path: Path, soft_limit: int) -> dict[str, object]:
    content = read_text(path)
    bullets = [line.strip()[2:].strip() for line in content.splitlines() if line.strip().startswith("- ")]
    normalized = [normalize_memory_text(item) for item in bullets]
    duplicates = [text for text, count in Counter(normalized).items() if text and count > 1]
    long_bullets = [item for item in bullets if len(item) > 180]
    secret_like = [item for item in bullets if contains_secret_like_text(item)]
    language_conflicts = []
    lower = "\n".join(bullets).lower()
    if "reply in chinese" in lower and "reply in english" in lower and "default" in lower:
        language_conflicts.append("Potential conflicting default language preferences.")
    return {
        "path": str(path),
        "characters": len(content),
        "soft_limit": soft_limit,
        "over_budget": len(content) > soft_limit,
        "bullet_count": len(bullets),
        "duplicate_count": len(duplicates),
        "duplicates": duplicates,
        "long_bullets": long_bullets,
        "secret_like": secret_like,
        "language_conflicts": language_conflicts,
    }


def render_report(data: dict[str, object]) -> str:
    lines = [
        "# USER.md Memory Budget Report",
        "",
        f"- path: {data['path']}",
        f"- characters: {data['characters']} / {data['soft_limit']}",
        f"- over_budget: {data['over_budget']}",
        f"- bullet_count: {data['bullet_count']}",
        f"- duplicate_count: {data['duplicate_count']}",
        "",
        "## Duplicates",
        "",
    ]
    duplicates = data["duplicates"] or []
    lines.extend([f"- {item}" for item in duplicates] or ["None"])
    lines.extend(["", "## Long Bullets", ""])
    lines.extend([f"- {item}" for item in data["long_bullets"]] or ["None"])
    lines.extend(["", "## Secret-Like Content", ""])
    lines.extend([f"- {item}" for item in data["secret_like"]] or ["None"])
    lines.extend(["", "## Potential Conflicts", ""])
    lines.extend([f"- {item}" for item in data["language_conflicts"]] or ["None"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_codex_root(), help="Codex root directory")
    parser.add_argument("--target", type=Path, help="USER.md path")
    parser.add_argument("--soft-limit", type=int, default=6000, help="Character soft budget")
    parser.add_argument("--report-path", type=Path, help="Write Markdown report")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()
    target = args.target.expanduser() if args.target else args.root.expanduser() / "memories" / "USER.md"
    data = analyze(target, args.soft_limit)
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        report = render_report(data)
        if args.report_path:
            write_text(args.report_path.expanduser(), report)
            print(f"Memory budget report written: {args.report_path}")
        else:
            print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
