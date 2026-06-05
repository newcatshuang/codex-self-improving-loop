"""Skill health summaries for the WebUI."""

from __future__ import annotations

from pathlib import Path

from .db import connect, init_db


VALID_STATUSES = {"active", "cold", "needs_patch", "duplicate_suspected"}


def skill_health(root: Path) -> dict[str, object]:
    init_db(root)
    with connect(root) as conn:
        usage_rows = [
            dict(row)
            for row in conn.execute(
                """
                select skill_name, count(*) as total, max(used_at) as last_used_at
                from skill_usage
                group by skill_name
                """
            )
        ]
        patch_rows = [
            dict(row)
            for row in conn.execute(
                """
                select title, text, rewrite_suggestion, status, updated_at
                from candidates
                where type='skill_patch' and status not in ('archived', 'rejected', 'merged')
                order by updated_at desc
                """
            )
        ]
    items = []
    names = [str(row["skill_name"]) for row in usage_rows]
    for row in usage_rows:
        name = str(row["skill_name"])
        patch_count = sum(1 for patch in patch_rows if name in str(patch.get("text", "") + " " + patch.get("rewrite_suggestion", "")).casefold())
        status = "active" if int(row["total"] or 0) >= 2 else "cold"
        if patch_count:
            status = "needs_patch"
        if any(other != name and (other.startswith(name + "-") or name.startswith(other + "-")) for other in names):
            status = "duplicate_suspected"
        items.append(
            {
                "skill_name": name,
                "usage_count": int(row["total"] or 0),
                "last_used_at": str(row["last_used_at"] or ""),
                "patch_candidates": patch_count,
                "status": status,
                "recommended_action": "review patch" if status == "needs_patch" else "keep" if status == "active" else "review",
            }
        )
    if not items and patch_rows:
        items.append(
            {
                "skill_name": "unassigned-skill-patch",
                "usage_count": 0,
                "last_used_at": "",
                "patch_candidates": len(patch_rows),
                "status": "needs_patch",
                "recommended_action": "assign patch",
            }
        )
    return {"skills": sorted(items, key=lambda item: (-int(item["usage_count"]), str(item["skill_name"])))}
