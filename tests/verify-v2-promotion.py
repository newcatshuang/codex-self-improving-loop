#!/usr/bin/env python3
"""Verify WebUI-backed promotion operations write files with backups and audit rows."""

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
    session = root / "sessions" / "promotion.jsonl"
    session.parent.mkdir(parents=True, exist_ok=True)
    session.write_text('{"role":"user","content":"请记住 SQL 查询必须先确认字段，避免 SELECT *。"}\n', encoding="utf-8")
    user = root / "memories" / "USER.md"
    user.parent.mkdir(parents=True, exist_ok=True)
    user.write_text("# USER.md\n", encoding="utf-8")

    env = os.environ.copy()
    env["CODEX_SIL_DISABLE_CODEX"] = "1"
    subprocess.run([sys.executable, str(repo / "sil.py"), "rebuild", "--codex-root", str(root), "--backup"], cwd=repo, env=env, check=True)
    sys.path.insert(0, str(repo / "src"))
    from codex_sil.exporter import export_candidates, export_digest
    from codex_sil.promotion import promote_to_skill, promote_to_skill_patch, promote_to_user_memory

    db = root / "self-improving-loop" / "self-improving-loop.sqlite"
    with sqlite3.connect(db) as conn:
        candidate_id = int(conn.execute("select id from candidates where type='memory' limit 1").fetchone()[0])
    result = promote_to_user_memory(root, candidate_id)
    text = user.read_text(encoding="utf-8")
    if "avoid SELECT *" not in text:
        raise AssertionError(text)
    if not result["backup_path"] or not Path(result["backup_path"]).exists():
        raise AssertionError("promotion should create a USER.md backup before writing")
    with sqlite3.connect(db) as conn:
        promoted = conn.execute("select status from candidates where id=?", (candidate_id,)).fetchone()[0]
        promotions = conn.execute("select count(*) from promotions").fetchone()[0]
        audit = conn.execute("select count(*) from audit_log where action='promote_user_memory'").fetchone()[0]
    if promoted != "promoted" or promotions != 1 or audit != 1:
        raise AssertionError("promotion should update candidate status and audit tables")
    skill_result = promote_to_skill(root, candidate_id, skills_root=root / "skills")
    patch_result = promote_to_skill_patch(root, candidate_id)
    if not Path(skill_result["target_path"]).exists() or not Path(patch_result["target_path"]).exists():
        raise AssertionError("skill and patch promotions should write target artifacts")
    second_skill = promote_to_skill(root, candidate_id, skills_root=root / "skills")
    if Path(second_skill["target_path"]).parent.name != Path(skill_result["target_path"]).parent.name:
        raise AssertionError("same candidate should keep a stable skill directory")
    with sqlite3.connect(db) as conn:
        conn.execute(
            """
            insert into candidates(type, title, text, normalized, destination, rewrite_suggestion, safety, confidence, extractor)
            values('skill', 'Another Workflow', 'A second reusable workflow.', 'a second reusable workflow', 'skill_candidate', 'Use a separate skill.', 'review', 0.8, 'test')
            """
        )
        second_candidate = int(conn.execute("select id from candidates where title='Another Workflow'").fetchone()[0])
    other_skill = promote_to_skill(root, second_candidate, skills_root=root / "skills")
    if Path(other_skill["target_path"]).parent == Path(skill_result["target_path"]).parent:
        raise AssertionError("different skill candidates should create independent skill directories")
    digest = export_digest(root)
    candidates = export_candidates(root)
    if not digest.exists() or not candidates.exists():
        raise AssertionError("exports should be written on demand")
    print("verify-v2-promotion passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
