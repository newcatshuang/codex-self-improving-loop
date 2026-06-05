"""Daily review digest persistence."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .db import connect, init_db
from .recommendations import generate_missing


def generate_digest(root: Path, run_id: int | None = None) -> dict[str, object]:
    init_db(root)
    generate_missing(root)
    today = datetime.now().date().isoformat()
    with connect(root) as conn:
        new_candidates = int(conn.execute("select count(*) from candidates").fetchone()[0])
        recommended_promotions = int(
            conn.execute("select count(*) from recommendations where suggested_action='promote'").fetchone()[0]
        )
        risk_items = int(conn.execute("select count(*) from candidates where safety in ('blocked', 'conflict_review', 'unsafe')").fetchone()[0])
        skill_usage_changes = int(conn.execute("select count(*) from skill_usage").fetchone()[0])
        failed_runs = int(conn.execute("select count(*) from runs where status='failed'").fetchone()[0])
        summary = {
            "new_candidates": new_candidates,
            "recommended_promotions": recommended_promotions,
            "risk_items": risk_items,
            "skill_usage_changes": skill_usage_changes,
            "failed_runs": failed_runs,
        }
        cur = conn.execute(
            """
            insert into digests(run_id, digest_date, summary, new_candidates, recommended_promotions, risk_items, skill_usage_changes, failed_runs)
            values(?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                today,
                json.dumps(summary, ensure_ascii=False),
                new_candidates,
                recommended_promotions,
                risk_items,
                skill_usage_changes,
                failed_runs,
            ),
        )
        digest_id = int(cur.lastrowid)
    return {"id": digest_id, "digest_date": today, **summary}


def latest_digest(root: Path) -> dict[str, object]:
    init_db(root)
    with connect(root) as conn:
        row = conn.execute("select * from digests order by id desc limit 1").fetchone()
    if row is None:
        return {"digest": None}
    payload = dict(row)
    try:
        summary = json.loads(str(payload.get("summary") or "{}"))
    except json.JSONDecodeError:
        summary = {}
    payload.update(summary)
    return {"digest": payload}
