# USER.md

Stable global memory for Codex. Current user instructions and project-local `AGENTS.md` always override this file. Keep this file compact and factual.

## Preferences

- Keep engineering handoffs concise and evidence-based: result/change first, then verification, then remaining risk.
- For code tasks, inspect repository instructions and project evidence before editing; make the smallest correct change and run real verification when practical.
- Prefer local project rules, build config, and current repository evidence over stale memory.
- Protect secrets strictly: do not print, summarize, transform, or commit tokens, API keys, passwords, cookies, private URLs, or sensitive env/config values.

## Context Priority

1. Current user instruction and newest conversation context.
2. Project `AGENTS.md`, README, build config, and repository evidence.
3. Stable preferences from this file.
4. Relevant skills, code-intelligence results, and recent verification facts.
