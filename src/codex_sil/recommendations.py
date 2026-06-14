"""Candidate review recommendations."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .codex_runner import codex_available, recommend_with_codex
from .db import connect, init_db


ALLOWED_ACTIONS = {"promote", "merge", "archive", "reject", "needs_review"}


@dataclass(frozen=True)
class Recommendation:
    recommendation: str
    recommendation_reason: str
    suggested_action: str
    engine: str = "fallback_rules"
    error: str = ""


def fallback_recommendation(candidate: dict[str, object]) -> Recommendation:
    fallback_error = (
        "codex recommendation unavailable or invalid; fallback_rules used"
        if codex_available()
        else "codex unavailable or disabled; fallback_rules used"
    )
    safety = str(candidate.get("safety") or "review")
    status = str(candidate.get("status") or "review")
    confidence = float(candidate.get("confidence") or 0)
    candidate_type = str(candidate.get("type") or "")
    source_count = int(candidate.get("source_count") or 0)
    if status in {"promoted", "archived", "rejected", "merged"}:
        return Recommendation(
            recommendation=f"Candidate is already {status}.",
            recommendation_reason="Processed items should stay out of the active promotion queue.",
            suggested_action="archive" if status != "promoted" else "needs_review",
            error=fallback_error,
        )
    if safety in {"blocked", "conflict_review", "unsafe"}:
        return Recommendation(
            recommendation="Do not promote until the safety issue is resolved.",
            recommendation_reason=f"Safety state is {safety}, which is a hard review boundary.",
            suggested_action="needs_review",
            error=fallback_error,
        )
    if candidate_type == "skill_patch":
        return Recommendation(
            recommendation="Review the target skill before applying this patch.",
            recommendation_reason="Skill patches can change agent behavior and should be inspected manually.",
            suggested_action="needs_review",
            error=fallback_error,
        )
    if confidence >= 0.7 or source_count >= 2:
        return Recommendation(
            recommendation="Promote after a quick human review.",
            recommendation_reason="The candidate has enough confidence or repeated evidence to be useful.",
            suggested_action="promote",
            error=fallback_error,
        )
    if confidence < 0.35:
        return Recommendation(
            recommendation="Archive unless better evidence appears.",
            recommendation_reason="Low-confidence candidates usually create review noise.",
            suggested_action="archive",
            error=fallback_error,
        )
    return Recommendation(
        recommendation="Needs manual review before promotion.",
        recommendation_reason="The candidate is plausible but does not have enough confidence or repeated evidence.",
        suggested_action="needs_review",
        error=fallback_error,
    )


def candidate_payload(root: Path, candidate_id: int) -> dict[str, object]:
    with connect(root) as conn:
        row = conn.execute(
            """
            select
              c.*,
              count(distinct cs.session_id) as source_count
            from candidates c
            left join candidate_sources cs on cs.candidate_id=c.id
            where c.id=?
            group by c.id
            """,
            (candidate_id,),
        ).fetchone()
    if row is None:
        raise ValueError(f"candidate not found: {candidate_id}")
    return dict(row)


def persist_recommendation(root: Path, candidate_id: int, recommendation: Recommendation) -> dict[str, object]:
    init_db(root)
    if recommendation.suggested_action not in ALLOWED_ACTIONS:
        raise ValueError(f"invalid recommendation action: {recommendation.suggested_action}")
    with connect(root) as conn:
        conn.execute(
            """
            insert into recommendations(candidate_id, recommendation, recommendation_reason, suggested_action, engine, error)
            values(?, ?, ?, ?, ?, ?)
            on conflict(candidate_id) do update set
              recommendation=excluded.recommendation,
              recommendation_reason=excluded.recommendation_reason,
              suggested_action=excluded.suggested_action,
              engine=excluded.engine,
              error=excluded.error,
              updated_at=current_timestamp
            """,
            (
                candidate_id,
                recommendation.recommendation,
                recommendation.recommendation_reason,
                recommendation.suggested_action,
                recommendation.engine,
                recommendation.error[:1200],
            ),
        )
        row = conn.execute(
            """
            select r.*, c.type, c.title, c.destination, c.status, c.safety
            from recommendations r
            join candidates c on c.id=r.candidate_id
            where r.candidate_id=?
            """,
            (candidate_id,),
        ).fetchone()
    return dict(row)


def recommend_candidate(root: Path, candidate_id: int) -> dict[str, object]:
    payload = candidate_payload(root, candidate_id)
    codex_payload = recommend_with_codex(payload, root)
    if codex_payload:
        recommendation = Recommendation(
            recommendation=codex_payload["recommendation"],
            recommendation_reason=codex_payload["recommendation_reason"],
            suggested_action=codex_payload["suggested_action"],
            engine="codex",
            error="",
        )
    else:
        recommendation = fallback_recommendation(payload)
    return persist_recommendation(root, candidate_id, recommendation)


def generate_missing(root: Path) -> None:
    init_db(root)
    with connect(root) as conn:
        ids = [
            int(row["id"])
            for row in conn.execute(
                """
                select c.id
                from candidates c
                left join recommendations r on r.candidate_id=c.id
                where r.id is null
                """
            )
        ]
    for candidate_id in ids:
        recommend_candidate(root, candidate_id)


def recommendations_payload(root: Path) -> dict[str, object]:
    init_db(root)
    generate_missing(root)
    with connect(root) as conn:
        rows = [
            dict(row)
            for row in conn.execute(
                """
                select
                  r.id,
                  r.candidate_id,
                  r.recommendation,
                  r.recommendation_reason,
                  r.suggested_action,
                  r.engine,
                  r.created_at,
                  r.updated_at,
                  c.type,
                  c.title,
                  c.destination,
                  c.status,
                  c.safety
                from recommendations r
                join candidates c on c.id=r.candidate_id
                order by r.updated_at desc, r.id desc
                limit 500
                """
            )
        ]
    return {"recommendations": rows}
