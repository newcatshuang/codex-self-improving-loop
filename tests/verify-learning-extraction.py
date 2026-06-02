#!/usr/bin/env python3
"""Verify learning candidate extraction quality."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def latest_report(directory: Path) -> str:
    reports = sorted(directory.rglob("*.md"), key=lambda path: path.stat().st_mtime)
    if not reports:
        raise AssertionError(f"no report written under {directory}")
    return reports[-1].read_text(encoding="utf-8")


def assert_report_under_today(directory: Path) -> None:
    today_parts = (datetime.now().strftime("%Y"), datetime.now().strftime("%m"), datetime.now().strftime("%d"))
    reports = sorted(directory.rglob("*.md"), key=lambda path: path.stat().st_mtime)
    if not reports:
        raise AssertionError(f"no report written under {directory}")
    relative = reports[-1].relative_to(directory)
    if relative.parts[:3] != today_parts:
        expected = "/".join(today_parts)
        raise AssertionError(f"report should be written under {expected}/, got {relative}")


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


def assert_contains(text: str, expected: str, message: str) -> None:
    if expected not in text:
        raise AssertionError(message)


def assert_not_contains(text: str, unexpected: str, message: str) -> None:
    if unexpected in text:
        raise AssertionError(message)


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
                        "改为 schtasks.exe /SC DAILY /ST 12:00，并通过 verify-install 验证。"
                    ),
                },
            }
        ],
    )
    run_script(scripts / "extract_memory.py", root, assistant_session)
    assert_report_under_today(root / "memories" / "inbox")
    memory_report = latest_report(root / "memories" / "inbox")
    assert_contains(memory_report, "Daily+Repetition", "assistant outcome should be extracted as a memory candidate")
    assert_contains(memory_report, "DAILY", "assistant outcome should preserve the verified fix")

    run_script(scripts / "extract_skill_candidate.py", root, assistant_session)
    assert_report_under_today(root / "skill-candidates" / "inbox")
    skill_report = latest_report(root / "skill-candidates" / "inbox")
    assert_contains(skill_report, "verify-install", "assistant verification workflow should be extracted as a skill candidate")

    reusable_workflow_session = root / "sessions" / "reusable-workflow.jsonl"
    write_jsonl(
        reusable_workflow_session,
        [
            {
                "type": "event_msg",
                "payload": {
                    "type": "agent_message",
                    "message": (
                        "Reusable workflow: first run verify-learning-extraction.py, then run verify-install.py, "
                        "then run python -m compileall agents install.py tests before handoff."
                    ),
                },
            }
        ],
    )
    run_script(scripts / "extract_skill_candidate.py", root, reusable_workflow_session)
    skill_report = latest_report(root / "skill-candidates" / "inbox")
    assert_contains(skill_report, "verify-learning-extraction.py", "reusable command sequence should become a skill candidate")

    preference_session = root / "sessions" / "preference-only.jsonl"
    write_jsonl(
        preference_session,
        [
            {
                "type": "event_msg",
                "payload": {
                    "type": "agent_message",
                    "message": "默认不要把一次性生产排查细节写入长期记忆。",
                },
            }
        ],
    )
    run_script(scripts / "extract_skill_candidate.py", root, preference_session)
    skill_report = latest_report(root / "skill-candidates" / "inbox")
    assert_not_contains(skill_report, "一次性生产排查", "preference-only memory should not become a skill candidate")

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
    assert_report_under_today(root / "memories" / "inbox")
    task_report = latest_report(root / "memories" / "inbox")
    assert_not_contains(task_report, "fin_bad_debt_record", "one-off task requests should not become memory candidates")

    transient_session = root / "sessions" / "transient-status.jsonl"
    write_jsonl(
        transient_session,
        [
            {
                "type": "event_msg",
                "payload": {
                    "type": "agent_message",
                    "message": "Any running unified exec processes may still be running in the background.",
                },
            },
            {
                "type": "event_msg",
                "payload": {
                    "type": "agent_message",
                    "message": "本地 PowerShell 初始化失败，暂时没法直接检索仓库。",
                },
            },
        ],
    )
    run_script(scripts / "extract_memory.py", root, transient_session)
    task_report = latest_report(root / "memories" / "inbox")
    assert_not_contains(task_report, "unified exec", "tool interruption text should not become memory")
    assert_not_contains(task_report, "PowerShell 初始化失败", "temporary environment failures should not become memory")

    noisy_artifact_session = root / "sessions" / "noisy-artifacts.jsonl"
    noisy_lines = [
        "::inbox-item{title=\"自动化重试规则确认\" summary=\"脚本默认会重试到当天结束\"}",
        "![Claude Code 工作流说明图](./claude-code-flow.png) ## 先说结论 `Claude Code` 的价值，可以用一句话讲清楚。",
        "+二次改稿说明：根据 2026-06-01 反馈，原正文结构与前几天文章趋同，本次改为资料流叙事。",
        "`/PreVerifyRecordView/GetList` 里有这个条件：",
        "`FinCompanyVisibilityRuleCompanyRel`：配置公司角色，比如“深圳默认可见公司”“受限部门可见公司”。",
        "验证已跑： `dotnet build OHL.Finance\\src\\OHL.Finance.sln -c Debug --no-restore /clp:ErrorsOnly` 通过，0 Error。",
        "验证通过。现在我会把增强过滤同步到本机真实 `.agents`，并手动跑一次 watcher/digest，看候选数量是否下降。",
        "测试文件里已经有一部分噪声用例，我会追加真实运行暴露出的几类噪声，并让它同时覆盖 memory 和 skill candidate。",
        "同步完成。因为旧候选文件已经存在，单独重跑 digest 不会减少历史候选；要验证过滤效果，需要对现有会话重新跑 watcher。",
        "学习提取测试通过，并且噪声 session 没再落 memory/skill 报告。接下来跑 review digest、install、低产物模式和编译检查。",
    ]
    write_jsonl(
        noisy_artifact_session,
        [
            {
                "type": "event_msg",
                "payload": {"type": "agent_message", "message": line},
            }
            for line in noisy_lines
        ],
    )
    run_script(scripts / "extract_memory.py", root, noisy_artifact_session)
    memory_noise_report = latest_report(root / "memories" / "inbox")
    run_script(scripts / "extract_skill_candidate.py", root, noisy_artifact_session)
    skill_noise_report = latest_report(root / "skill-candidates" / "inbox")
    for noisy in noisy_lines:
        assert_not_contains(memory_noise_report, noisy, f"artifact noise should not become memory: {noisy}")
        assert_not_contains(skill_noise_report, noisy, f"artifact noise should not become skill candidate: {noisy}")

    patch_session = root / "sessions" / "skill-patch.jsonl"
    write_jsonl(
        patch_session,
        [
            {
                "type": "event_msg",
                "payload": {
                    "type": "agent_message",
                    "message": "memory-capture SKILL.md missing a rule: skill patch candidates must name the target skill before promotion.",
                },
            },
            {
                "type": "event_msg",
                "payload": {
                    "type": "agent_message",
                    "message": "根因是脚本只扫描用户消息，已修复并通过验证。",
                },
            },
        ],
    )
    run_script(scripts / "extract_skill_patch_candidate.py", root, patch_session)
    patch_report = latest_report(root / "skill-candidates" / "patches")
    assert_contains(patch_report, "memory-capture SKILL.md missing", "specific skill gaps should become patch candidates")
    assert_not_contains(patch_report, "只扫描用户消息", "generic fixes should not become patch candidates without a skill target")

    print("verify-learning-extraction passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
