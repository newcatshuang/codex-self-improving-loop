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
    recommendation_en: str = ""
    recommendation_zh: str = ""
    recommendation_reason_en: str = ""
    recommendation_reason_zh: str = ""
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
            recommendation_en=f"Candidate is already {status}.",
            recommendation_zh=f"候选已处于 {status} 状态。",
            recommendation_reason_en="Processed items should stay out of the active promotion queue.",
            recommendation_reason_zh="已处理的候选不应继续占用活跃晋升队列。",
            error=fallback_error,
        )
    if safety in {"blocked", "conflict_review", "unsafe"}:
        return Recommendation(
            recommendation="Do not promote until the safety issue is resolved.",
            recommendation_reason=f"Safety state is {safety}, which is a hard review boundary.",
            suggested_action="needs_review",
            recommendation_en="Do not promote until the safety issue is resolved.",
            recommendation_zh="安全问题解决前不要晋升。",
            recommendation_reason_en=f"Safety state is {safety}, which is a hard review boundary.",
            recommendation_reason_zh=f"安全状态为 {safety}，需要先完成人工复核。",
            error=fallback_error,
        )
    if candidate_type == "skill_patch":
        return Recommendation(
            recommendation="Review the target skill before applying this patch.",
            recommendation_reason="Skill patches can change agent behavior and should be inspected manually.",
            suggested_action="needs_review",
            recommendation_en="Review the target skill before applying this patch.",
            recommendation_zh="应用补丁前先复核目标 skill。",
            recommendation_reason_en="Skill patches can change agent behavior and should be inspected manually.",
            recommendation_reason_zh="Skill 补丁会改变代理行为，必须先人工检查。",
            error=fallback_error,
        )
    if confidence >= 0.7 or source_count >= 2:
        return Recommendation(
            recommendation="Promote after a quick human review.",
            recommendation_reason="The candidate has enough confidence or repeated evidence to be useful.",
            suggested_action="promote",
            recommendation_en="Promote after a quick human review.",
            recommendation_zh="快速人工复核后可以晋升。",
            recommendation_reason_en="The candidate has enough confidence or repeated evidence to be useful.",
            recommendation_reason_zh="该候选已有较高置信度或重复证据，具备复用价值。",
            error=fallback_error,
        )
    if confidence < 0.35:
        return Recommendation(
            recommendation="Archive unless better evidence appears.",
            recommendation_reason="Low-confidence candidates usually create review noise.",
            suggested_action="archive",
            recommendation_en="Archive unless better evidence appears.",
            recommendation_zh="除非出现更强证据，否则建议归档。",
            recommendation_reason_en="Low-confidence candidates usually create review noise.",
            recommendation_reason_zh="低置信度候选通常会增加审阅噪音。",
            error=fallback_error,
        )
    return Recommendation(
        recommendation="Needs manual review before promotion.",
        recommendation_reason="The candidate is plausible but does not have enough confidence or repeated evidence.",
        suggested_action="needs_review",
        recommendation_en="Needs manual review before promotion.",
        recommendation_zh="晋升前需要人工复核。",
        recommendation_reason_en="The candidate is plausible but does not have enough confidence or repeated evidence.",
        recommendation_reason_zh="该候选看起来合理，但置信度或重复证据还不够充分。",
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
    recommendation_en = (recommendation.recommendation_en or recommendation.recommendation)[:800]
    recommendation_zh = (recommendation.recommendation_zh or recommendation.recommendation)[:800]
    reason_en = (recommendation.recommendation_reason_en or recommendation.recommendation_reason)[:1200]
    reason_zh = (recommendation.recommendation_reason_zh or recommendation.recommendation_reason)[:1200]
    with connect(root) as conn:
        conn.execute(
            """
            insert into recommendations(
              candidate_id, recommendation, recommendation_en, recommendation_zh,
              recommendation_reason, recommendation_reason_en, recommendation_reason_zh,
              suggested_action, engine, error
            )
            values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            on conflict(candidate_id) do update set
              recommendation=excluded.recommendation,
              recommendation_en=excluded.recommendation_en,
              recommendation_zh=excluded.recommendation_zh,
              recommendation_reason=excluded.recommendation_reason,
              recommendation_reason_en=excluded.recommendation_reason_en,
              recommendation_reason_zh=excluded.recommendation_reason_zh,
              suggested_action=excluded.suggested_action,
              engine=excluded.engine,
              error=excluded.error,
              updated_at=current_timestamp
            """,
            (
                candidate_id,
                recommendation_en,
                recommendation_en,
                recommendation_zh,
                reason_en,
                reason_en,
                reason_zh,
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
            recommendation=codex_payload["recommendation_en"],
            recommendation_reason=codex_payload["recommendation_reason_en"],
            suggested_action=codex_payload["suggested_action"],
            recommendation_en=codex_payload["recommendation_en"],
            recommendation_zh=codex_payload["recommendation_zh"],
            recommendation_reason_en=codex_payload["recommendation_reason_en"],
            recommendation_reason_zh=codex_payload["recommendation_reason_zh"],
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
                   or r.recommendation_en=''
                   or r.recommendation_zh=''
                   or r.recommendation_reason_en=''
                   or r.recommendation_reason_zh=''
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
                  r.recommendation_en,
                  r.recommendation_zh,
                  r.recommendation_reason,
                  r.recommendation_reason_en,
                  r.recommendation_reason_zh,
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
