# AGENTS.md

This repository contains a cross-platform, open-source Codex self-improvement kit.

## Rules

- Keep the project independent from any private repository or local machine path.
- Do not add PowerShell-only scripts; runtime scripts should be Python standard library unless there is a strong reason otherwise.
- Do not commit generated memories, session histories, nudge reports, or local usage metadata.
- Do not include secrets, private URLs, credentials, or raw session transcripts.
- Installation scripts must copy repository files; do not embed large skill or script bodies inside installers.
- Prefer small, reviewable scripts with clear command-line interfaces.

## Verification

Before handoff, run:

```bash
python tests/verify-install.py --codex-root ./tmp/codex --agents-root ./tmp/agents
python -m compileall agents install.py tests
```
