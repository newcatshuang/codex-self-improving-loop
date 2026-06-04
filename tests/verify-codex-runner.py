#!/usr/bin/env python3
"""Verify Codex CLI extraction is preferred and fallback remains available."""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import stat
import subprocess
import sys
from pathlib import Path


def make_fake_codex(path: Path) -> None:
    script = path / ("codex.cmd" if os.name == "nt" else "codex")
    if os.name == "nt":
        script.write_text(
            "\r\n".join(
                [
                    "@echo off",
                    "echo {\"memory_candidates\":[{\"title\":\"Model preference\",\"text\":\"Remember this model preference from the transcript.\",\"destination\":\"global_user_memory\",\"rewrite_suggestion\":\"Remember this model preference from the transcript.\",\"confidence\":0.91}],\"skill_candidates\":[],\"skill_patch_candidates\":[],\"summary\":\"ok\",\"risks\":[],\"confidence\":0.91}",
                ]
            ),
            encoding="utf-8",
        )
    else:
        script.write_text(
            "#!/bin/sh\n"
            "printf '%s\n' '{\"memory_candidates\":[{\"title\":\"Model preference\",\"text\":\"Remember this model preference from the transcript.\",\"destination\":\"global_user_memory\",\"rewrite_suggestion\":\"Remember this model preference from the transcript.\",\"confidence\":0.91}],\"skill_candidates\":[],\"skill_patch_candidates\":[],\"summary\":\"ok\",\"risks\":[],\"confidence\":0.91}'\n",
            encoding="utf-8",
        )
        script.chmod(script.stat().st_mode | stat.S_IEXEC)


def write_session(path: Path, content: str = "remember this model preference") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"role": "user", "content": content}, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--work-root", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    root = args.work_root.resolve()
    fake_bin = root / "fake-bin"
    fake_bin.mkdir(parents=True, exist_ok=True)
    make_fake_codex(fake_bin)
    write_session(root / "sessions" / "model.jsonl")

    env = os.environ.copy()
    env["PATH"] = str(fake_bin) + os.pathsep + env.get("PATH", "")
    subprocess.run(
        [sys.executable, str(repo / "sil.py"), "rebuild", "--codex-root", str(root), "--backup"],
        cwd=repo,
        env=env,
        check=True,
    )
    db_path = root / "self-improving-loop" / "self-improving-loop.sqlite"
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute("select text, extractor from candidates").fetchall()
    if not rows:
        raise AssertionError("Codex runner should persist model candidates")
    if rows[0][1] != "codex":
        raise AssertionError(f"Codex extractor should be preferred, got {rows}")
    if "Remember this model preference" not in rows[0][0]:
        raise AssertionError(rows)

    no_codex_root = root / "fallback"
    write_session(no_codex_root / "sessions" / "fallback.jsonl", "请记住 SQL 查询要确认字段，避免 SELECT *，这个流程也可以做成 skill。")
    env["PATH"] = str(root / "empty-bin")
    subprocess.run(
        [sys.executable, str(repo / "sil.py"), "rebuild", "--codex-root", str(no_codex_root), "--backup"],
        cwd=repo,
        env=env,
        check=True,
    )
    with sqlite3.connect(no_codex_root / "self-improving-loop" / "self-improving-loop.sqlite") as conn:
        fallback_extractors = {row[0] for row in conn.execute("select extractor from candidates")}
    if "fallback" not in fallback_extractors:
        raise AssertionError("fallback extractor should run when codex is unavailable")

    print("verify-codex-runner passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
