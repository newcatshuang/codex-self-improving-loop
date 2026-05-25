#!/usr/bin/env python3
"""Verify learning candidate extraction quality."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def latest_report(directory: Path) -> str:
    reports = sorted(directory.glob("*.md"), key=lambda path: path.stat().st_mtime)
    if not reports:
        raise AssertionError(f"no report written under {directory}")
    return reports[-1].read_text(encoding="utf-8")


def run_script(script: Path, root: Path, session: Path) -> None:
    subprocess.run(
        [
            sys.executable,
            str(script),
            "--root",
            str(root),
            "--session-file",
            str(session),
            "--max-messages",
            "20",
        ],
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--work-root", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    root = args.work_root.resolve()
    scripts = repo / "agents" / "skills" / "memory-capture" / "scripts"

    assistant_session = root / "sessions" / "assistant-outcome.jsonl"
    write_jsonl(
        assistant_session,
        [
            {
                "type": "event_msg",
                "payload": {
                    "type": "agent_message",
                    "message": (
                        "已修复定时执行问题。根因是 Windows 计划任务使用 XML Daily+Repetition 后出现漏跑；"
                        "改为 schtasks.exe /SC HOURLY /MO 1，并通过 verify-install 验证。"
                    ),
                },
            }
        ],
    )
    run_script(scripts / "extract_memory.py", root, assistant_session)
    memory_report = latest_report(root / "memories" / "inbox")
    if "Daily+Repetition" not in memory_report or "HOURLY" not in memory_report:
        raise AssertionError("assistant outcome should be extracted as a memory candidate")

    run_script(scripts / "extract_skill_candidate.py", root, assistant_session)
    skill_report = latest_report(root / "skill-candidates" / "inbox")
    if "verify-install" not in skill_report:
        raise AssertionError("assistant verification workflow should be extracted as a skill candidate")

    task_request_session = root / "sessions" / "task-request.jsonl"
    write_jsonl(
        task_request_session,
        [
            {
                "role": "user",
                "content": "帮我查下项目里面对表 bms.fin_bad_debt_record 的删除逻辑，只返回类名和方法名，不要展开分析。",
            }
        ],
    )
    run_script(scripts / "extract_memory.py", root, task_request_session)
    task_report = latest_report(root / "memories" / "inbox")
    if "fin_bad_debt_record" in task_report:
        raise AssertionError("one-off task requests should not become memory candidates")

    print("verify-learning-extraction passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
