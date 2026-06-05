# Codex Self-Improving Loop

**A local-only SQLite and WebUI control plane for Codex self-improvement.**

Codex Self-Improving Loop helps Codex recall prior sessions, extract durable memory candidates, identify reusable skill candidates, propose skill patches, and review promotions from a single local WebUI.

The v3 architecture replaces scattered Markdown/JSON outputs with one SQLite database and a temporary Python backend. The backend binds only to `127.0.0.1`, uses a per-run token, and is intended for this machine only.

[中文说明](./README.zh-CN.md)

## What You Get

| Capability | How v3 handles it |
| --- | --- |
| Session recall | `sil.py recall` searches SQLite FTS-backed session/candidate records with redacted snippets and fallback search |
| Memory capture | Daily or manual scans extract memory candidates into SQLite |
| Skill candidates | Reusable workflows are stored as `type=skill` candidates |
| Skill patches | Existing skill improvement ideas are stored as `type=skill_patch` candidates |
| WebUI management | `sil.py serve --open` starts a local backend and opens the dashboard |
| Review suggestions | Each candidate gets a deterministic review recommendation, with Codex-ready extension points |
| Candidate merge | Similar candidates are grouped, and merge actions keep original evidence while marking duplicates `merged` |
| Promotion preview | USER.md, AGENTS.md, skill, and skill patch promotions show a diff before writing files |
| Daily digest | Each scan/rebuild stores one SQLite digest with candidate, risk, skill usage, and failed-run counts |
| Backup bundle | Export SQLite, memory files, skills, and audit history into a zip; import has dry-run preview |
| Skill health | Skill usage and patch candidates produce `active`, `cold`, `needs_patch`, or `duplicate_suspected` states |
| Audit and history | The WebUI shows audit logs, review history, promotion history, and rollback previews |
| Scheduled scan | `sil.py schedule install` prepares a daily 03:00 scan command |
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
├─ web/
│  ├─ styles.css
│  └─ app.js
└─ tmp/
```

The project no longer writes default candidate Markdown files, `learning-index.json`, `latest-*` reports, usage JSON, or watcher state files. Daily review summaries are stored as one SQLite digest row and can be exported on demand.

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

The `$HOME/.agents/codex-self-improving-loop` directory is the installed runtime copy used by schedules, shortcuts, and skills. Keeping this copy outside the Git checkout lets the local loop keep working even if the repository is moved, renamed, or deleted.

## Daily Use

Start the temporary local WebUI backend:

```bash
python "$HOME/.agents/codex-self-improving-loop/sil.py" serve --open
```

From the WebUI you can initialize the database, clear current SQLite data and rebuild from all historical sessions, scan sessions, install or remove the daily schedule, install the desktop shortcut, export review data or a migration bundle, archive or reject candidates, merge duplicate candidates, and promote reviewed items to `USER.md`, project `AGENTS.md`, independent learned skills, or skill patch artifacts.

The WebUI also includes a first-run wizard, daily digest, candidate merge suggestions, promotion diff preview, skill health, audit logs, review history, promotion history, and rollback preview. Rollback is intentionally preview-only: the UI shows the target path, backup path, and a copy-safe Python restore command, but it does not overwrite files automatically.

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

Schedule installation is cross-platform:

- Windows: creates or replaces the `CodexSelfImprovingLoop` Task Scheduler task.
- macOS: writes and loads `~/Library/LaunchAgents/com.codex.self-improving-loop.plist`.
- Linux: writes and enables a `systemd --user` timer at `$XDG_CONFIG_HOME/systemd/user` or `~/.config/systemd/user`.

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

## API Surface

The WebUI uses these local-only JSON APIs in addition to the existing scan, rebuild, schedule, review, and promotion endpoints:

- `GET /api/setup/status`
- `GET /api/recommendations`
- `POST /api/candidates/{id}/recommend`
- `GET /api/merge-suggestions`
- `POST /api/merge-suggestions/{id}/apply`
- `GET /api/candidates/{id}/promotion-preview?target=user|agents|skill|patch`
- `GET /api/digests/latest`
- `GET /api/skills/health`
- `POST /api/export/bundle`
- `POST /api/import/preview`

## Verification

```bash
python tests/verify-v2-core.py --work-root ./tmp/v2-core
python tests/verify-codex-runner.py --work-root ./tmp/codex-runner
python tests/verify-v2-recall.py --work-root ./tmp/v2-recall
python tests/verify-v2-session-filter.py --work-root ./tmp/v2-filter
python tests/verify-v2-promotion.py --work-root ./tmp/v2-promotion
python tests/verify-v2-scheduler.py --work-root ./tmp/v2-scheduler
python tests/verify-v3-migration.py --work-root ./tmp/v3-migration
python tests/verify-v3-intelligence.py --work-root ./tmp/v3-intelligence
python tests/verify-v2-install.py --codex-root ./tmp/codex-v2 --agents-root ./tmp/agents-v2
python tests/verify-install.py --codex-root ./tmp/install-codex --agents-root ./tmp/install-agents
python -m compileall src sil.py install.py tests
```
