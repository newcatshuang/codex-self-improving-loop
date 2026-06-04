# Codex Self-Improving Loop

**A local-only SQLite and WebUI control plane for Codex self-improvement.**

Codex Self-Improving Loop helps Codex recall prior sessions, extract durable memory candidates, identify reusable skill candidates, propose skill patches, and review promotions from a single local WebUI.

The v2 architecture replaces scattered Markdown/JSON outputs with one SQLite database and a temporary Python backend. The backend binds only to `127.0.0.1`, uses a per-run token, and is intended for this machine only.

[中文说明](./README.zh-CN.md)

## What You Get

| Capability | How v2 handles it |
| --- | --- |
| Session recall | `sil.py recall` searches SQLite-backed session records with redacted snippets |
| Memory capture | Daily or manual scans extract memory candidates into SQLite |
| Skill candidates | Reusable workflows are stored as `type=skill` candidates |
| Skill patches | Existing skill improvement ideas are stored as `type=skill_patch` candidates |
| WebUI management | `sil.py serve --open` starts a local backend and opens the dashboard |
| Scheduled scan | `sil.py schedule install` prepares a daily 12:00 scan command |
| Desktop launcher | `sil.py shortcut install` prepares a one-click launcher command |

## Runtime Layout

All runtime files owned by this project live under one folder:

```text
$HOME/.codex/self-improving-loop/
├─ self-improving-loop.sqlite
├─ codex-self-improving-loop.html
├─ self-improving-loop.log
├─ backups/
├─ exports/
└─ tmp/
```

The project no longer writes default candidate Markdown files, daily digests, `learning-index.json`, `latest-*` reports, usage JSON, or watcher state files.

## Install

```bash
git clone https://github.com/newcatshuang/codex-self-improving-loop.git
cd codex-self-improving-loop
python install.py
```

The installer copies:

- `sil.py` and `src/codex_sil` to `$HOME/.agents/codex-self-improving-loop`.
- `session-recall` and `memory-capture` skills to `$HOME/.agents/skills`.
- `codex/AGENTS.learning-block.md` into `$HOME/.codex/AGENTS.md`.
- `codex/memories/USER.template.md` to `$HOME/.codex/memories/USER.md` only if missing.

## Daily Use

Start the temporary local WebUI backend:

```bash
python "$HOME/.agents/codex-self-improving-loop/sil.py" serve --open
```

From the WebUI you can initialize or rebuild the database, scan sessions, install or remove the daily schedule, install the desktop shortcut, export review data, archive or reject candidates, and promote reviewed items to `USER.md`, a learned skill, or a skill patch artifact.

Scan new sessions once:

```bash
python "$HOME/.agents/codex-self-improving-loop/sil.py" scan --once
```

Backup the database and rebuild from all historical sessions:

```bash
python "$HOME/.agents/codex-self-improving-loop/sil.py" rebuild --backup
```

Search prior sessions:

```bash
python "$HOME/.agents/codex-self-improving-loop/sil.py" recall --query "previous error"
```

Install helper commands:

```bash
python "$HOME/.agents/codex-self-improving-loop/sil.py" schedule install
python "$HOME/.agents/codex-self-improving-loop/sil.py" shortcut install
```

## Extraction Strategy

Scans prefer Codex CLI for higher-quality extraction:

```text
codex exec --ephemeral --skip-git-repo-check --sandbox read-only --output-schema extraction.schema.json
```

If Codex is unavailable, fails, times out, or returns invalid JSON, the scanner falls back to a small rule-based extractor.

`--ephemeral` prevents automated extraction runs from creating new session files that would be scanned again later.

For tests or fast historical rebuilds, set `CODEX_SIL_DISABLE_CODEX=1` to force the deterministic fallback extractor. Daily scheduled scans leave this unset by default, so they still try Codex first.

## Local Service Boundary

- The backend binds only to `127.0.0.1`.
- It does not support LAN or public access.
- Each `serve` run creates a token; API requests must include it.
- Daily scans do not require the backend to be running.
- The WebUI is the normal place for review and promotion actions; users should not copy shell commands for normal promotion.

## Verification

```bash
python tests/verify-v2-core.py --work-root ./tmp/v2-core
python tests/verify-codex-runner.py --work-root ./tmp/codex-runner
python tests/verify-v2-recall.py --work-root ./tmp/v2-recall
python tests/verify-v2-session-filter.py --work-root ./tmp/v2-filter
python tests/verify-v2-promotion.py --work-root ./tmp/v2-promotion
python tests/verify-v2-install.py --codex-root ./tmp/codex-v2 --agents-root ./tmp/agents-v2
python tests/verify-install.py --codex-root ./tmp/install-codex --agents-root ./tmp/install-agents
python -m compileall src sil.py install.py tests
```
