#!/usr/bin/env python3
"""Run the Codex self-improving loop in review mode."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

from learning_loop_common import dated_output_path, default_codex_root, ensure_dir, now_stamp, today_dir_parts, write_text


def run_step(name: str, command: list[str]) -> dict[str, object]:
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    completed = subprocess.run(command, text=True, capture_output=True, encoding="utf-8", errors="replace", env=env)
    return {
        "name": name,
        "status": "ok" if completed.returncode == 0 else "failed",
        "returncode": completed.returncode,
        "stdout": (completed.stdout or "").strip(),
        "stderr": (completed.stderr or "").strip(),
    }


def candidate_count(step: dict[str, object]) -> int:
    match = re.search(r"(?m)^Candidates:\s*(\d+)\s*$", str(step.get("stdout", "")))
    return int(match.group(1)) if match else 0


def should_write_detail_report(steps: list[dict[str, object]]) -> bool:
    if any(step["status"] != "ok" for step in steps):
        return True
    return sum(candidate_count(step) for step in steps if str(step["name"]).startswith("extract_")) > 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_codex_root())
    parser.add_argument("--session-file", type=Path, help="Specific Codex session file to inspect")
    parser.add_argument("--report-dir", type=Path)
    parser.add_argument("--max-messages", type=int, default=80)
    parser.add_argument("--skip-skill-candidate-scan", action="store_true")
    parser.add_argument("--skip-skills-index", action="store_true")
    parser.add_argument("--skip-learning-summary", action="store_true")
    args = parser.parse_args()

    root = args.root.expanduser()
    script_dir = Path(__file__).resolve().parent
    report_dir = args.report_dir.expanduser() if args.report_dir else root / "nudge-reports"
    ensure_dir(report_dir)
    stamp = now_stamp()
    session_suffix = ""
    if args.session_file:
        digest = hashlib.sha1(str(args.session_file.expanduser().resolve()).encode("utf-8")).hexdigest()[:8]
        session_suffix = f"-{digest}"
    report_path = dated_output_path(report_dir, f"{stamp}{session_suffix}-end-of-task-nudge.md")
    usage_file = root / "skill-usage.json"
    session_args = ["--session-file", str(args.session_file.expanduser())] if args.session_file else []

    py = sys.executable
    steps: list[dict[str, object]] = []
    steps.append(run_step("extract_memory", [py, str(script_dir / "extract_memory.py"), "--root", str(root), "--max-messages", str(args.max_messages), *session_args]))
    steps.append(run_step("extract_skill_candidate", [py, str(script_dir / "extract_skill_candidate.py"), "--root", str(root), "--max-messages", str(args.max_messages), *session_args]))
    steps.append(run_step("extract_skill_patch_candidate", [py, str(script_dir / "extract_skill_patch_candidate.py"), "--root", str(root), "--max-messages", str(args.max_messages), *session_args]))
    if not args.skip_skill_candidate_scan:
        steps.append(run_step("scan_skill_candidates", [py, str(script_dir / "scan_skill_candidates.py"), "--root", str(root), "--report-path", str(root / "latest-skill-candidate-security-scan.md")]))
    steps.append(run_step("promote_candidates_report", [py, str(script_dir / "promote_candidates.py"), "--root", str(root)]))
    steps.append(run_step("compact_user_memory", [py, str(script_dir / "compact_user_memory.py"), "--root", str(root), "--report-path", str(root / "latest-user-memory-budget.md")]))
    steps.append(run_step("record_skill_usage", [py, str(script_dir / "record_skill_usage.py"), "--root", str(root), "--skill-name", "memory-capture", "--status", "success", "--notes", "Ran end-of-task nudge"]))
    if not args.skip_skills_index:
        skills_root = Path.home() / ".agents" / "skills"
        steps.append(run_step("generate_skills_index", [py, str(script_dir / "generate_skills_index.py"), "--skills-root", str(skills_root), "--usage-file", str(usage_file), "--output-path", str(root / "skills-index.md")]))
    if not args.skip_learning_summary:
        steps.append(run_step("summarize_learning_inbox", [py, str(script_dir / "summarize_learning_inbox.py"), "--root", str(root), "--usage-file", str(usage_file), "--report-path", str(root / "learning-inbox-summary.md")]))
        daily_digest = root / "daily-digests" / Path(*today_dir_parts()) / "review-digest.md"
        steps.append(run_step("summarize_daily_digest", [py, str(script_dir / "summarize_learning_inbox.py"), "--root", str(root), "--usage-file", str(usage_file), "--report-path", str(daily_digest)]))

    lines = ["# End-of-task Nudge Report", "", f"- root: {root}", f"- session_file: {args.session_file.expanduser() if args.session_file else 'latest'}", f"- failed_steps: {sum(1 for step in steps if step['status'] != 'ok')}", ""]
    for step in steps:
        lines.extend(
            [
                f"## {step['name']}",
                "",
                f"- status: {step['status']}",
                f"- returncode: {step['returncode']}",
                "",
                "### stdout",
                "",
                "```text",
                str(step["stdout"]),
                "```",
                "",
            ]
        )
        if step["stderr"]:
            lines.extend(["### stderr", "", "```text", str(step["stderr"]), "```", ""])
    wrote_detail = should_write_detail_report(steps)
    if wrote_detail:
        write_text(report_path, "\n".join(lines))
    print("End-of-task nudge complete")
    print(f"Report: {report_path if wrote_detail else 'skipped (no candidates and no failures)'}")
    for step in steps:
        if step["name"] in {"summarize_learning_inbox", "summarize_daily_digest"} and step["stdout"]:
            print(str(step["stdout"]))
    failed = [step for step in steps if step["status"] != "ok"]
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
