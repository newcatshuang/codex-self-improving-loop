#!/usr/bin/env python3
"""Verify repository hygiene for open-source distribution."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    repo = args.repo_root.resolve()

    gitignore = repo / ".gitignore"
    if not gitignore.exists():
        raise AssertionError(".gitignore is required")
    content = gitignore.read_text(encoding="utf-8")
    required_patterns = ("__pycache__/", "*.pyc", "tmp/")
    for pattern in required_patterns:
        if pattern not in content:
            raise AssertionError(f".gitignore should include {pattern}")

    tracked = subprocess.run(
        ["git", "ls-files", "*.pyc", "__pycache__/*", "src/**/__pycache__/*"],
        cwd=repo,
        check=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    ).stdout.strip()
    if tracked:
        raise AssertionError(f"compiled Python artifacts should not be tracked:\n{tracked}")

    print("verify-repo-hygiene passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
