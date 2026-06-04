"""Rule-based fallback extractor for offline or unavailable Codex CLI runs."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ExtractedCandidate:
    type: str
    title: str
    text: str
    destination: str
    rewrite_suggestion: str
    safety: str = "review"
    confidence: float = 0.45
    extractor: str = "fallback"


def clean_text(text: str) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    return compact[:500]


def normalize(text: str) -> str:
    return re.sub(r"\W+", " ", text.casefold()).strip()


def extract_candidates(text: str) -> list[ExtractedCandidate]:
    lower = text.casefold()
    candidates: list[ExtractedCandidate] = []
    if re.search(r"sql|select\s+\*|字段|query", lower):
        candidates.append(
            ExtractedCandidate(
                type="memory",
                title="SQL query preference",
                text="When writing SQL, verify table columns before drafting queries; avoid SELECT * by default and select only required fields.",
                destination="global_user_memory",
                rewrite_suggestion="When writing SQL, verify table columns before drafting queries; avoid SELECT * by default and select only required fields.",
                confidence=0.72,
            )
        )
    if re.search(r"做成\s*skill|生成\s*skill|可复用流程|reusable workflow|workflow candidate|沉淀.*skill|流程.*复用", lower):
        candidates.append(
            ExtractedCandidate(
                type="skill",
                title="Reusable workflow candidate",
                text=clean_text("Capture this repeated workflow as a reviewed skill candidate: " + text),
                destination="skill_candidate",
                rewrite_suggestion="Convert this repeated workflow into a small SKILL.md with trigger conditions, steps, verification, and safety notes.",
                confidence=0.58,
            )
        )
    if re.search(r"skill\s*patch|技能补丁|skill.*补丁|补丁.*skill|patch.*skill|改进.*skill|skill.*missing|skill.*缺", lower):
        candidates.append(
            ExtractedCandidate(
                type="skill_patch",
                title="Skill patch candidate",
                text=clean_text("Review existing skill instructions for this improvement: " + text),
                destination="skill_patch",
                rewrite_suggestion="Patch the target SKILL.md only after inspecting the skill and confirming the safer instruction.",
                confidence=0.5,
            )
        )
    return candidates
