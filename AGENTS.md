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
python tests/verify-v2-core.py --work-root ./tmp/v2-core
python tests/verify-codex-runner.py --work-root ./tmp/codex-runner
python tests/verify-v2-recall.py --work-root ./tmp/v2-recall
python tests/verify-v2-install.py --codex-root ./tmp/codex-v2 --agents-root ./tmp/agents-v2
python -m compileall src sil.py install.py tests
```
