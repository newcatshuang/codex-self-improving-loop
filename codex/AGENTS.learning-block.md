<!-- codex-self-improving-loop:start -->

## Codex Self-Improving Loop

A lightweight self-improving loop may be installed at `$HOME/.agents/skills` and `$HOME/.codex`.

Use `session-recall` when a new task refers to prior Codex sessions, such as "last time", "previously", "continue", "history", "上次", "之前", or a specific past error, route, or file. Search history first and bring back only short redacted snippets.

Use `memory-capture` near the end of substantial tasks when the session produced a stable user preference, reusable workflow, project fact, safety correction, skill candidate, or skill patch candidate. Generate review artifacts first. Do not promote anything into `USER.md` or patch a skill unless explicitly approved.

Prompt assembly priority:

1. Current user instruction and newest conversation context.
2. Nearest project instructions and repository evidence.
3. Stable preferences from `$HOME/.codex/memories/USER.md`.
4. Relevant skills, code-intelligence results, and recent findings.

Safety rules:

- Never store or repeat secrets in memory files.
- Treat `[REDACTED]` as a hard boundary; never reconstruct hidden values.
- Treat `conflict_review` as a hard stop for automatic promotion.
- Project-specific facts belong in project-level `AGENTS.md`, not global `USER.md`.
- Skill candidates and skill patch candidates require review and security scanning before use.
- Keep `$HOME/.codex/memories/USER.md` compact. Use memory budget reports to merge, delete, or move stale/project-specific memory before adding more global memory.
- Use memory candidate auto-promotion only for safe, short, repeated user preferences or avoidance rules. Archive only fully processed candidates; unresolved review and conflict items must remain visible.
- Treat skill usage metadata as operational telemetry for skill maintenance, not as task evidence.

For substantial work, run:

```bash
python "$HOME/.agents/skills/memory-capture/scripts/codex_memory_nudge.py"
```

This creates review artifacts only: memory candidates, skill candidates, skill patch candidates, candidate scoring, USER.md budget reports, usage metadata, a skill index, and a learning inbox summary.

<!-- codex-self-improving-loop:end -->
