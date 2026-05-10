#!/usr/bin/env python3
"""Promote one explicitly approved memory into USER.md."""

from __future__ import annotations

import argparse
from pathlib import Path

from learning_loop_common import contains_secret_like_text, default_codex_root, ensure_dir, normalize_memory_text, read_text, write_text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_codex_root(), help="Codex root directory")
    parser.add_argument("--target", type=Path, help="USER.md path")
    parser.add_argument("--text", required=True, help="Reviewed memory text")
    parser.add_argument("--approved", action="store_true", help="Required explicit approval flag")
    args = parser.parse_args()

    if not args.approved:
        print("Refusing to promote memory without --approved.")
        return 2
    text = args.text.strip()
    if not text:
        print("Refusing to promote empty memory.")
        return 2
    if contains_secret_like_text(text):
        print("Refusing to promote secret-like or redacted content.")
        return 2
    target = args.target.expanduser() if args.target else args.root.expanduser() / "memories" / "USER.md"
    ensure_dir(target.parent)
    existing = read_text(target)
    normalized_existing = {normalize_memory_text(line.lstrip("- ").strip()) for line in existing.splitlines() if line.strip().startswith("-")}
    normalized = normalize_memory_text(text)
    if normalized in normalized_existing:
        print("Memory already present.")
        return 0
    if not existing.strip():
        existing = "# USER.md\n\nStable global memory for Codex.\n\n## Preferences\n\n"
    if "## Preferences" not in existing:
        existing = existing.rstrip() + "\n\n## Preferences\n\n"
    updated = existing.rstrip() + f"\n- {text}\n"
    write_text(target, updated)
    print(f"Promoted memory to: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
