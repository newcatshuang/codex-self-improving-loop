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
    count_file = path / "fake-codex-count.txt"
    if count_file.exists():
        count_file.unlink()
    extraction = "{\"memory_candidates\":[{\"title\":\"Model preference\",\"text\":\"Remember this model preference from the transcript.\",\"destination\":\"global_user_memory\",\"rewrite_suggestion\":\"Remember this model preference from the transcript.\",\"confidence\":0.91}],\"skill_candidates\":[],\"skill_patch_candidates\":[],\"summary\":\"ok\",\"risks\":[],\"confidence\":0.91}"
    recommendation = "{\"recommendation_en\":\"Promote after human review.\",\"recommendation_zh\":\"人工复核后可以晋升。\",\"recommendation_reason_en\":\"The candidate is directly supported by the transcript.\",\"recommendation_reason_zh\":\"该候选有会话记录直接支撑。\",\"suggested_action\":\"promote\"}"
    analysis = "{\"analysis\":{\"evidence_assessment_en\":\"The transcript directly supports the candidate.\",\"evidence_assessment_zh\":\"会话记录直接支撑该候选。\",\"stability\":\"stable\",\"scope\":\"global\",\"risk_level\":\"low\",\"conflicts_en\":\"No conflict found.\",\"conflicts_zh\":\"未发现冲突。\",\"rewrite_quality_en\":\"The rewrite is concise.\",\"rewrite_quality_zh\":\"改写内容较简洁。\",\"recommended_next_step_en\":\"Review the proposal in the WebUI.\",\"recommended_next_step_zh\":\"在 WebUI 中复核该建议。\"},\"proposal\":{\"target_type\":\"USER.md\",\"target_path\":\"$CODEX_ROOT/memories/USER.md\",\"proposed_text_en\":\"Remember this model preference from the transcript.\",\"proposed_text_zh\":\"记住会话中的模型偏好。\",\"rationale_en\":\"This is a stable user preference candidate.\",\"rationale_zh\":\"这是稳定的用户偏好候选。\",\"verification_en\":\"Preview the diff before manual promotion.\",\"verification_zh\":\"人工晋升前先预览 diff。\",\"requires_manual_approval\":true}}"
    helper = path / "fake_codex.py"
    helper.write_text(
        "\n".join(
            [
                "from pathlib import Path",
                "state = Path(__file__).with_name('fake-codex-count.txt')",
                "try:",
                "    count = int(state.read_text(encoding='utf-8').strip())",
                "except Exception:",
                "    count = 0",
                "state.write_text(str(count + 1), encoding='utf-8')",
                f"payloads = [{extraction!r}, {analysis!r}, {recommendation!r}]",
                "print(payloads[count] if count < len(payloads) else payloads[-1])",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    if os.name == "nt":
        script.write_text(
            "\r\n".join(
                [
                    "@echo off",
                    f"\"{sys.executable}\" \"%~dp0fake_codex.py\"",
                ]
            ),
            encoding="utf-8",
        )
    else:
        script.write_text(
            "#!/bin/sh\n"
            f"\"{sys.executable}\" \"$(dirname \"$0\")/fake_codex.py\"\n",
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
    with sqlite3.connect(db_path) as conn:
        analysis_engines = {row[0] for row in conn.execute("select engine from candidate_analyses")}
        proposal_flags = {row[0] for row in conn.execute("select requires_manual_approval from evolution_proposals")}
        bilingual_recommendations = conn.execute(
            "select count(*) from recommendations where recommendation_en<>'' and recommendation_zh<>''"
        ).fetchone()[0]
        bilingual_analyses = conn.execute(
            "select count(*) from candidate_analyses where evidence_assessment_en<>'' and evidence_assessment_zh<>''"
        ).fetchone()[0]
    if analysis_engines != {"codex"}:
        raise AssertionError(f"Codex analysis should be preferred, got {analysis_engines}")
    if proposal_flags != {1}:
        raise AssertionError(f"Codex evolution proposals must require manual approval, got {proposal_flags}")
    if int(bilingual_recommendations) < 1 or int(bilingual_analyses) < 1:
        raise AssertionError("Codex guidance should be persisted in both English and Chinese")

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
        fallback_analysis_engines = {row[0] for row in conn.execute("select engine from candidate_analyses")}
    if "fallback" not in fallback_extractors:
        raise AssertionError("fallback extractor should run when codex is unavailable")
    if "fallback_rules" not in fallback_analysis_engines:
        raise AssertionError("fallback analysis should run when codex is unavailable")

    print("verify-codex-runner passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
