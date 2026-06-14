"""Candidate analysis and manual evolution proposal persistence."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .codex_runner import analyze_with_codex, codex_available
from .db import connect, init_db


TARGET_TYPES = {"USER.md", "AGENTS.md", "skill", "skill_patch", "manual_review"}
RISK_LEVELS = {"low", "medium", "high"}


@dataclass(frozen=True)
class CandidateAnalysis:
    evidence_assessment: str
    stability: str
    scope: str
    risk_level: str
    conflicts: str
    rewrite_quality: str
    recommended_next_step: str
    engine: str = "fallback_rules"
    error: str = ""


@dataclass(frozen=True)
class EvolutionProposal:
    target_type: str
    target_path: str
    proposed_text: str
    rationale: str
    verification: str
    requires_manual_approval: bool = True
    engine: str = "fallback_rules"


def target_for_candidate(candidate: dict[str, object]) -> tuple[str, str]:
    candidate_type = str(candidate.get("type") or "")
    destination = str(candidate.get("destination") or "").casefold()
    title = str(candidate.get("title") or "candidate").strip() or "candidate"
    if candidate_type == "skill":
        return "skill", "$HOME/.agents/skills/<reviewed-skill>/SKILL.md"
    if candidate_type == "skill_patch":
        return "skill_patch", "$HOME/.codex/self-improving-loop/exports/skill-patch-<candidate-id>.md"
    if "agents" in destination or "project" in destination:
        return "AGENTS.md", "$CODEX_ROOT/AGENTS.md"
    if "global_user_memory" in destination or candidate_type == "memory":
        return "USER.md", "$CODEX_ROOT/memories/USER.md"
    return "manual_review", title


def fallback_analysis(candidate: dict[str, object]) -> tuple[CandidateAnalysis, EvolutionProposal]:
    confidence = float(candidate.get("confidence") or 0)
    source_count = int(candidate.get("source_count") or 0)
    candidate_type = str(candidate.get("type") or "")
    safety = str(candidate.get("safety") or "review")
    risk_level = "low" if confidence >= 0.7 and source_count >= 2 and safety == "review" else "medium"
    if safety in {"blocked", "conflict_review", "unsafe"} or candidate_type in {"skill", "skill_patch"}:
        risk_level = "high" if safety in {"blocked", "conflict_review", "unsafe"} else "medium"
    text = str(candidate.get("rewrite_suggestion") or candidate.get("text") or "").strip()
    target_type, target_path = target_for_candidate(candidate)
    analysis = CandidateAnalysis(
        evidence_assessment=(
            "Repeated or high-confidence evidence is present."
            if confidence >= 0.7 or source_count >= 2
            else "Evidence is plausible but should be checked before promotion."
        ),
        stability="stable" if confidence >= 0.7 and candidate_type == "memory" else "review",
        scope="project" if target_type == "AGENTS.md" else "global" if target_type == "USER.md" else candidate_type or "manual",
        risk_level=risk_level,
        conflicts="No explicit conflict detected by fallback rules.",
        rewrite_quality="Use the candidate rewrite as a draft; review for specificity and portability.",
        recommended_next_step="Review the proposed text in the WebUI before any manual promotion.",
        error=(
            "codex analysis unavailable or invalid; fallback_rules used"
            if codex_available()
            else "codex unavailable or disabled; fallback_rules used"
        ),
    )
    proposal = EvolutionProposal(
        target_type=target_type,
        target_path=target_path,
        proposed_text=text,
        rationale="Fallback proposal keeps the existing candidate text and requires manual approval.",
        verification="Preview the diff in the WebUI, then run the relevant project checks after manual promotion.",
        requires_manual_approval=True,
    )
    return analysis, proposal


def _analysis_from_payload(payload: dict[str, object]) -> CandidateAnalysis | None:
    risk_level = str(payload.get("risk_level") or "medium").strip().lower()
    if risk_level not in RISK_LEVELS:
        risk_level = "medium"
    required = (
        "evidence_assessment",
        "stability",
        "scope",
        "conflicts",
        "rewrite_quality",
        "recommended_next_step",
    )
    values = {key: str(payload.get(key) or "").strip() for key in required}
    if not all(values.values()):
        return None
    return CandidateAnalysis(
        evidence_assessment=values["evidence_assessment"],
        stability=values["stability"],
        scope=values["scope"],
        risk_level=risk_level,
        conflicts=values["conflicts"],
        rewrite_quality=values["rewrite_quality"],
        recommended_next_step=values["recommended_next_step"],
        engine="codex",
        error="",
    )


def _proposal_from_payload(payload: dict[str, object]) -> EvolutionProposal | None:
    target_type = str(payload.get("target_type") or "manual_review").strip()
    if target_type not in TARGET_TYPES:
        target_type = "manual_review"
    proposed_text = str(payload.get("proposed_text") or "").strip()
    rationale = str(payload.get("rationale") or "").strip()
    verification = str(payload.get("verification") or "").strip()
    if not proposed_text or not rationale or not verification:
        return None
    return EvolutionProposal(
        target_type=target_type,
        target_path=str(payload.get("target_path") or "").strip() or target_type,
        proposed_text=proposed_text,
        rationale=rationale,
        verification=verification,
        requires_manual_approval=True,
        engine="codex",
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


def persist_analysis(
    root: Path,
    candidate_id: int,
    analysis: CandidateAnalysis,
    proposal: EvolutionProposal,
) -> dict[str, object]:
    init_db(root)
    with connect(root) as conn:
        conn.execute(
            """
            insert into candidate_analyses(
              candidate_id, engine, evidence_assessment, stability, scope, risk_level,
              conflicts, rewrite_quality, recommended_next_step, error
            )
            values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            on conflict(candidate_id) do update set
              engine=excluded.engine,
              evidence_assessment=excluded.evidence_assessment,
              stability=excluded.stability,
              scope=excluded.scope,
              risk_level=excluded.risk_level,
              conflicts=excluded.conflicts,
              rewrite_quality=excluded.rewrite_quality,
              recommended_next_step=excluded.recommended_next_step,
              error=excluded.error,
              updated_at=current_timestamp
            """,
            (
                candidate_id,
                analysis.engine,
                analysis.evidence_assessment[:1200],
                analysis.stability[:120],
                analysis.scope[:120],
                analysis.risk_level,
                analysis.conflicts[:1200],
                analysis.rewrite_quality[:1200],
                analysis.recommended_next_step[:1200],
                analysis.error[:1200],
            ),
        )
        conn.execute(
            """
            insert into evolution_proposals(
              candidate_id, engine, target_type, target_path, proposed_text,
              rationale, verification, requires_manual_approval
            )
            values(?, ?, ?, ?, ?, ?, ?, 1)
            on conflict(candidate_id) do update set
              engine=excluded.engine,
              target_type=excluded.target_type,
              target_path=excluded.target_path,
              proposed_text=excluded.proposed_text,
              rationale=excluded.rationale,
              verification=excluded.verification,
              requires_manual_approval=1,
              updated_at=current_timestamp
            """,
            (
                candidate_id,
                proposal.engine,
                proposal.target_type,
                proposal.target_path[:500],
                proposal.proposed_text[:4000],
                proposal.rationale[:1200],
                proposal.verification[:1200],
            ),
        )
        analysis_row = conn.execute("select * from candidate_analyses where candidate_id=?", (candidate_id,)).fetchone()
        proposal_row = conn.execute("select * from evolution_proposals where candidate_id=?", (candidate_id,)).fetchone()
    result = {"analysis": dict(analysis_row) if analysis_row else None, "proposal": dict(proposal_row) if proposal_row else None}
    if result["proposal"]:
        result["proposal"]["requires_manual_approval"] = bool(result["proposal"].get("requires_manual_approval"))
    return result


def analyze_candidate(root: Path, candidate_id: int) -> dict[str, object]:
    payload = candidate_payload(root, candidate_id)
    codex_payload = analyze_with_codex(payload, root)
    if codex_payload:
        analysis = _analysis_from_payload(dict(codex_payload.get("analysis") or {}))
        proposal = _proposal_from_payload(dict(codex_payload.get("proposal") or {}))
        if analysis and proposal:
            return persist_analysis(root, candidate_id, analysis, proposal)
    analysis, proposal = fallback_analysis(payload)
    return persist_analysis(root, candidate_id, analysis, proposal)


def generate_missing(root: Path) -> None:
    init_db(root)
    with connect(root) as conn:
        ids = [
            int(row["id"])
            for row in conn.execute(
                """
                select c.id
                from candidates c
                left join candidate_analyses ca on ca.candidate_id=c.id
                left join evolution_proposals ep on ep.candidate_id=c.id
                where ca.id is null or ep.id is null
                """
            )
        ]
    for candidate_id in ids:
        analyze_candidate(root, candidate_id)


def batch_analysis(root: Path) -> dict[str, object]:
    """Analyze all candidates that are missing analysis. Returns counts."""
    init_db(root)
    with connect(root) as conn:
        ids = [
            int(row["id"])
            for row in conn.execute(
                """
                select c.id
                from candidates c
                left join candidate_analyses ca on ca.candidate_id=c.id
                left join evolution_proposals ep on ep.candidate_id=c.id
                where ca.id is null or ep.id is null
                """
            )
        ]
    analyzed = 0
    for candidate_id in ids:
        try:
            analyze_candidate(root, candidate_id)
            analyzed += 1
        except Exception:
            pass
    return {"analyzed": analyzed, "total": len(ids)}


def analysis_payload(root: Path, candidate_id: int) -> dict[str, object]:
    init_db(root)
    with connect(root) as conn:
        analysis = conn.execute("select * from candidate_analyses where candidate_id=?", (candidate_id,)).fetchone()
        proposal = conn.execute("select * from evolution_proposals where candidate_id=?", (candidate_id,)).fetchone()
    if analysis is None or proposal is None:
        return analyze_candidate(root, candidate_id)
    payload = {"analysis": dict(analysis), "proposal": dict(proposal)}
    payload["proposal"]["requires_manual_approval"] = bool(payload["proposal"].get("requires_manual_approval"))
    return payload
