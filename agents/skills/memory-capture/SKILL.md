---
name: memory-capture
description: Use when a Codex session should preserve stable user preferences, reusable workflow patterns, project facts, safety corrections, or lessons learned; also use when the user says remember, learn, capture memory, 沉淀记忆, 记住, or asks to promote reviewed memory.
---

# Memory Capture

## Purpose

Use the local Codex Self-Improving Loop v2 control plane to capture and review durable learning candidates. Runtime data is stored in SQLite under `$HOME/.codex/self-improving-loop/`.

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
# Start the local-only WebUI backend and open the dashboard.
python "$HOME/.agents/codex-self-improving-loop/sil.py" serve --open

# Scan new Codex sessions once. The scanner prefers Codex CLI extraction and falls back to rules when Codex is unavailable.
python "$HOME/.agents/codex-self-improving-loop/sil.py" scan --once

# Backup the SQLite database and rebuild it from all historical sessions.
python "$HOME/.agents/codex-self-improving-loop/sil.py" rebuild --backup

# Install the daily 03:00 scan schedule or the desktop launcher.
python "$HOME/.agents/codex-self-improving-loop/sil.py" schedule install
python "$HOME/.agents/codex-self-improving-loop/sil.py" shortcut install
```

## Safety Rules

- Never store secrets, credentials, tokens, cookies, private URLs, connection strings, or raw auth headers.
- Prefer stable preferences and reusable workflows over session narration.
- Keep promoted memories short and directly actionable.
- Project-specific facts should usually go in the project's `AGENTS.md`; global user preferences go in `$HOME/.codex/memories/USER.md`.
- If a candidate contains `[REDACTED]`, do not reconstruct or promote the hidden value.
- Treat `conflict_review` as a hard stop for automatic promotion.

## Output Locations

- Runtime directory: `$HOME/.codex/self-improving-loop`
- SQLite database: `$HOME/.codex/self-improving-loop/self-improving-loop.sqlite`
- Local WebUI HTML: `$HOME/.codex/self-improving-loop/codex-self-improving-loop.html`
- Installed app copy: `$HOME/.agents/codex-self-improving-loop`
- Backups: `$HOME/.codex/self-improving-loop/backups`
- Exports: `$HOME/.codex/self-improving-loop/exports`
- Stable global memory: `$HOME/.codex/memories/USER.md`

## Review Workflow

1. Run `sil.py serve --open`.
2. Review memory, skill, and skill patch candidates in the WebUI.
3. Use WebUI buttons for review, archive, clear-and-rebuild, scan, schedule, and promotion actions.
4. Behavior-changing actions require confirmation; the backend backs up target files and records audit logs.
5. Do not manually edit the SQLite database unless debugging a backup copy.
