---
name: memory-capture
description: Use when a Codex session should preserve stable user preferences, reusable workflow patterns, project facts, safety corrections, or lessons learned; also use when the user says remember, learn, capture memory, 沉淀记忆, 记住, or asks to promote reviewed memory.
---

# Memory Capture

## Purpose

Create a safe review inbox for Codex self-improvement. This skill captures memory and skill candidates first; it does not directly rewrite stable memory or patch skills unless explicitly instructed.

## When To Use

Use this skill when:

- The user asks Codex to remember, learn, or capture a finding.
- A substantial task ends and produced a stable preference, workflow pattern, project fact, or safety correction worth reusing.
- The user corrects agent behavior in a way future sessions should honor.
- A reviewed candidate memory should be promoted into `USER.md`.
- A repeated workflow should become a skill candidate or skill patch candidate.

Do not use it for one-off task details, secrets, temporary debugging data, or raw transcript archival.

## Core Commands

```bash
# Capture memory candidates from the latest session.
python "$HOME/.agents/skills/memory-capture/scripts/extract_memory.py" --max-messages 40

# Promote one reviewed memory into USER.md.
python "$HOME/.agents/skills/memory-capture/scripts/promote_memory.py" --text "Use concise engineering handoffs." --approved

# Score and consolidate memory candidates without writing USER.md.
python "$HOME/.agents/skills/memory-capture/scripts/promote_candidates.py"

# Run the full end-of-task learning nudge in review mode.
python "$HOME/.agents/skills/memory-capture/scripts/codex_memory_nudge.py"

# Rebuild the shared index used by digest and dashboard renderers.
python "$HOME/.agents/skills/memory-capture/scripts/build_learning_index.py"

# Rebuild the read-only local review dashboard.
python "$HOME/.agents/skills/memory-capture/scripts/render_dashboard.py"
```

## Safety Rules

- Never store secrets, credentials, tokens, cookies, private URLs, connection strings, or raw auth headers.
- Prefer stable preferences and reusable workflows over session narration.
- Keep promoted memories short and directly actionable.
- Project-specific facts should usually go in the project's `AGENTS.md`; global user preferences go in `$HOME/.codex/memories/USER.md`.
- If a candidate contains `[REDACTED]`, do not reconstruct or promote the hidden value.
- Treat `conflict_review` as a hard stop for automatic promotion.

## Output Locations

- Generated review files are grouped under `YYYY/MM/DD` subdirectories.
- Memory candidate inbox: `$HOME/.codex/memories/inbox`
- Stable global memory: `$HOME/.codex/memories/USER.md`
- Skill candidates: `$HOME/.codex/skill-candidates/inbox`
- Skill patch candidates: `$HOME/.codex/skill-candidates/patches`
- Nudge reports: `$HOME/.codex/nudge-reports`
- Skill usage metadata: `$HOME/.codex/skill-usage.json`
- Skill index: `$HOME/.codex/skills-index.md`
- Shared learning index: `$HOME/.codex/learning-index.json`
- Learning inbox summary: `$HOME/.codex/learning-inbox-summary.md`
- Local review dashboard: `$HOME/.codex/codex-self-improving-loop-dashboard.html`

## Review Workflow

1. Capture candidates with `extract_memory.py` or `codex_memory_nudge.py`.
2. Inspect the Review Digest destination and rewrite suggestion before promotion.
3. Run `scan_skill_candidates.py` before applying any skill candidate.
4. Promote only reviewed global memories with `promote_memory.py --approved`; move project facts to project `AGENTS.md`.
5. Use `promote_candidates.py --auto-promote` only for safe, short, repeated user preferences or avoidance rules.
6. Use `promote_candidates.py --archive-processed` only after unresolved review and conflict items have been intentionally left in the inbox.
