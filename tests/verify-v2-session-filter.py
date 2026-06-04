#!/usr/bin/env python3
"""Verify session scanning ignores metadata and extracts only real dialogue."""

from __future__ import annotations

import argparse
import os
import sqlite3
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
    session = root / "sessions" / "filter.jsonl"
    session.parent.mkdir(parents=True, exist_ok=True)
    session.write_text(
        "\n".join(
            [
                '{"type":"session_meta","payload":{"base_instructions":{"text":"Use skill, patch, workflow, and reusable instructions everywhere."}}}',
                '{"type":"response_item","payload":{"type":"message","role":"developer","content":[{"type":"input_text","text":"developer skill patch text should be ignored"}]}}',
                '{"type":"response_item","payload":{"type":"function_call_output","output":"tool output with skill patch should be ignored"}}',
                '{"type":"response_item","payload":{"type":"message","role":"user","content":[{"type":"input_text","text":"# AGENTS.md instructions\\n<INSTRUCTIONS>skill patch workflow noise</INSTRUCTIONS>\\n\\n请记住：SQL 查询必须先确认字段，避免 SELECT *。"}]}}',
                '{"type":"response_item","payload":{"type":"message","role":"assistant","content":[{"type":"output_text","text":"已记录为稳定偏好。"}]}}',
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    env = os.environ.copy()
    env["CODEX_SIL_DISABLE_CODEX"] = "1"
    subprocess.run([sys.executable, str(repo / "sil.py"), "rebuild", "--codex-root", str(root)], cwd=repo, env=env, check=True)
    db = root / "self-improving-loop" / "self-improving-loop.sqlite"
    with sqlite3.connect(db) as conn:
        counts = dict(conn.execute("select type, count(*) from candidates group by type").fetchall())
        evidence = conn.execute("select evidence from candidate_sources limit 1").fetchone()[0]
    if counts != {"memory": 1}:
        raise AssertionError(f"metadata should not produce skill or patch candidates: {counts}")
    if "session_meta" in evidence or "developer skill patch" in evidence:
        raise AssertionError(f"evidence should only contain real dialogue: {evidence[:400]}")

    code_patch_root = root / "code-patch"
    code_patch_session = code_patch_root / "sessions" / "code-patch.jsonl"
    code_patch_session.parent.mkdir(parents=True, exist_ok=True)
    code_patch_session.write_text(
        '{"type":"response_item","payload":{"type":"message","role":"user","content":[{"type":"input_text","text":"请修复这个代码补丁，生成 patch，但这不是技能改进。"}]}}\n',
        encoding="utf-8",
    )
    subprocess.run([sys.executable, str(repo / "sil.py"), "rebuild", "--codex-root", str(code_patch_root)], cwd=repo, env=env, check=True)
    with sqlite3.connect(code_patch_root / "self-improving-loop" / "self-improving-loop.sqlite") as conn:
        patch_count = conn.execute("select count(*) from candidates where type='skill_patch'").fetchone()[0]
    if patch_count:
        raise AssertionError("ordinary code patch wording should not become a skill_patch candidate")
    print("verify-v2-session-filter passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
