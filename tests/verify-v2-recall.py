#!/usr/bin/env python3
"""Verify v2 session recall searches SQLite and redacts sensitive values."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--work-root", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    root = args.work_root.resolve()
    session = root / "sessions" / "recall.jsonl"
    session.parent.mkdir(parents=True, exist_ok=True)
    session.write_text(
        "\n".join(
            [
                json.dumps({"role": "user", "content": "Remember the GitHub Trending workflow and token sk-SECRET123."}),
                json.dumps({"role": "assistant", "content": "The GitHub Trending workflow should use the official trending page."}),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    env = os.environ.copy()
    env["CODEX_SIL_DISABLE_CODEX"] = "1"
    subprocess.run([sys.executable, str(repo / "sil.py"), "rebuild", "--codex-root", str(root), "--backup"], cwd=repo, env=env, check=True)
    completed = subprocess.run(
        [sys.executable, str(repo / "sil.py"), "recall", "--codex-root", str(root), "--query", "GitHub Trending", "--json"],
        cwd=repo,
        check=True,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    payload = json.loads(completed.stdout)
    if not payload["results"]:
        raise AssertionError("recall should return matching session snippets")
    text = json.dumps(payload, ensure_ascii=False)
    if "GitHub Trending" not in text:
        raise AssertionError(payload)
    if "sk-SECRET123" in text:
        raise AssertionError("recall output should redact secret-like values")
    if "[REDACTED]" not in text:
        raise AssertionError("recall should show redaction boundary")
    print("verify-v2-recall passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
