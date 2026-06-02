# Codex Self-Improving Loop

**A local, review-first self-improvement layer for Codex.**

Codex Self-Improving Loop helps Codex recall previous sessions, capture durable preferences, propose reusable skills, detect unsafe learning candidates, and evolve through a governed learning loop.

It is designed for developers who want their coding agent to improve over time without giving it unchecked permission to rewrite its own long-term behavior.

[中文说明](./README.zh-CN.md)

## What You Get

| Capability             | What it does                                                                                    | Default output                           |
| ---------------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------- |
| Session recall         | Searches previous Codex sessions and returns short redacted snippets                            | terminal output                          |
| Memory candidates      | Extracts stable preferences, safety corrections, and durable lessons                            | `$HOME/.codex/memories/inbox`            |
| Memory promotion       | Promotes one reviewed memory into global `USER.md`                                              | `$HOME/.codex/memories/USER.md`          |
| Candidate scoring      | Finds repeated, short, safe memory candidates                                                   | terminal or JSON report                  |
| Skill candidates       | Captures reusable workflows that may become future skills                                       | `$HOME/.codex/skill-candidates/inbox`    |
| Skill patch candidates | Captures evidence that an existing skill should be upgraded                                     | `$HOME/.codex/skill-candidates/patches`  |
| Safety scan            | Flags secrets, private URLs, redacted values, prompt injection text, and raw transcript markers | terminal or Markdown report              |
| End-of-task nudge      | Runs the learning loop in review mode near handoff                                              | `$HOME/.codex/nudge-reports`             |
| Session watcher        | Polls Codex session files and runs the nudge after idle periods                                 | `$HOME/.codex/memory-watcher-state.json` |
| Usage metadata         | Tracks skill `use_count`, `last_used`, and failures                                             | `$HOME/.codex/skill-usage.json`          |
| Learning reports       | Generates skill index and learning inbox summaries                                              | `$HOME/.codex/*.md`                      |

## Why This Exists

Many coding agents are strong inside one session but lose useful collaboration context across sessions. Users end up repeating preferences, project rules, verification habits, and hard-won lessons.

This project turns session experience into governed assets:

```text
task experience
  -> reviewable candidates
  -> safety scan and scoring
  -> explicit promotion or archival
  -> future recall and skill evolution
```

The goal is not to dump every conversation into long-term memory. The goal is to keep a clean learning loop:

- Stable user preferences go into global memory.
- Project facts stay in project-level `AGENTS.md`.
- Reusable procedures become skill candidates.
- Risky or ambiguous findings stay in review.
- Secrets and redacted values are blocked.

## Design Principles

This project is inspired by the self-improving loop in [Hermes Agent](https://github.com/NousResearch/hermes-agent): memory, reusable skills, session search, and nudges that encourage the agent to preserve useful lessons.

Codex Self-Improving Loop adapts that idea into a smaller local tool for Codex:

| Principle           | Implementation                                                                  |
| ------------------- | ------------------------------------------------------------------------------- |
| Local first         | Files live under `$HOME/.codex` and `$HOME/.agents`; no hosted service required |
| Review first        | Capture creates candidates; promotion is explicit                               |
| Cross-platform      | Python standard library only, no shell-specific runtime dependency              |
| Agent-readable      | Skills are plain `SKILL.md` files with small command scripts                    |
| Installable by copy | `install.py` copies repository files instead of embedding generated blobs       |
| Safe by default     | Secret-like content and redacted values are blocked from promotion              |

## What This Is Not

- It is not a replacement for Codex.
- It is not a vector database or hosted memory service.
- It does not auto-edit project code.
- It does not automatically enable newly proposed skills.
- It does not make unsafe memories safe; it only helps detect and quarantine them.

## Requirements

- Python 3.10 or newer.
- Codex configured to discover skills from `$HOME/.agents/skills`.

No third-party Python packages are required.

## Quickstart

```bash
git clone https://github.com/newcatshuang/codex-self-improving-loop.git
cd codex-self-improving-loop
python install.py
```

Restart Codex or open a new session after installing so skill discovery reloads the new files.

Verify the installation in temporary directories:

```bash
python tests/verify-install.py --codex-root /tmp/codex-sil --agents-root /tmp/agents-sil
```

Windows users can use any temporary paths:

```bash
python tests/verify-install.py --codex-root C:/Temp/codex-sil --agents-root C:/Temp/agents-sil
```

## Install Details

Custom install roots:

```bash
python install.py --codex-root /tmp/codex-test --agents-root /tmp/agents-test --force
```

The installer:

- Copies `agents/skills/session-recall` into `$HOME/.agents/skills/session-recall`.
- Copies `agents/skills/memory-capture` into `$HOME/.agents/skills/memory-capture`.
- Creates learning inbox directories under `$HOME/.codex`.
- Copies `codex/memories/USER.template.md` to `$HOME/.codex/memories/USER.md` only if it does not exist.
- Appends `codex/AGENTS.learning-block.md` to `$HOME/.codex/AGENTS.md` using idempotent markers.

## Daily Workflow

Search previous sessions:

```bash
python "$HOME/.agents/skills/session-recall/scripts/search_sessions.py" --query "previous error" --max-results 10
```

Capture memory candidates from the latest session:

```bash
python "$HOME/.agents/skills/memory-capture/scripts/extract_memory.py" --max-messages 40
```

Promote one reviewed memory:

```bash
python "$HOME/.agents/skills/memory-capture/scripts/promote_memory.py" \
  --text "Prefer concise engineering handoffs with verification and residual risk." \
  --approved
```

Run the end-of-task self-improvement loop:

```bash
python "$HOME/.agents/skills/memory-capture/scripts/codex_memory_nudge.py"
```

Run the automatic session watcher. In long-running mode, it polls once per day by default and processes sessions that have been idle for at least 10 minutes:

```bash
python "$HOME/.agents/skills/memory-capture/scripts/codex_session_watcher.py"
```

Run one watcher cycle for testing:

```bash
python "$HOME/.agents/skills/memory-capture/scripts/codex_session_watcher.py" --once --dry-run
```

For OS schedulers such as cron, launchd, systemd timers, or Windows Task Scheduler, schedule one real cycle daily at 12:00:

```bash
python install_watcher_schedule.py
```

Generate maintenance reports:

```bash
python "$HOME/.agents/skills/memory-capture/scripts/generate_skills_index.py"
python "$HOME/.agents/skills/memory-capture/scripts/summarize_learning_inbox.py"
python "$HOME/.agents/skills/memory-capture/scripts/show_skill_usage.py"
```

## Command Reference

| Script                             | Purpose                                                                 |
| ---------------------------------- | ----------------------------------------------------------------------- |
| `search_sessions.py`               | Search local Codex session history with redaction                       |
| `extract_memory.py`                | Create memory candidates from recent session context                    |
| `promote_memory.py`                | Promote one reviewed memory into `USER.md`                              |
| `promote_candidates.py`            | Score, optionally auto-promote, and archive processed memory candidates |
| `compact_user_memory.py`           | Report global memory budget, duplicates, conflicts, and safety risks    |
| `extract_skill_candidate.py`       | Create review-only skill candidates                                     |
| `extract_skill_patch_candidate.py` | Create review-only skill patch candidates                               |
| `scan_skill_candidates.py`         | Scan skill candidates and patch candidates for safety risks             |
| `record_skill_usage.py`            | Record usage metadata for a skill                                       |
| `show_skill_usage.py`              | Show skill usage metadata                                               |
| `generate_skills_index.py`         | Generate a skill index from installed `SKILL.md` files                  |
| `summarize_learning_inbox.py`      | Generate a Review Digest with memory, skill, patch, and promotion options |
| `codex_memory_nudge.py`            | Run the full review-mode learning loop                                  |
| `codex_session_watcher.py`         | Watch session files and run nudge after idle periods                    |
| `install_watcher_schedule.py`      | Install a daily 12:00 OS schedule for the installed watcher              |

## Repository Layout

```text
codex-self-improving-loop/
├─ README.md
├─ README.zh-CN.md
├─ LICENSE
├─ install.py
├─ install_watcher_schedule.py
├─ tests/
│  └─ verify-install.py
├─ codex/
│  ├─ AGENTS.learning-block.md
│  └─ memories/
│     └─ USER.template.md
└─ agents/
   └─ skills/
      ├─ session-recall/
      │  ├─ SKILL.md
      │  └─ scripts/
      │     └─ search_sessions.py
      └─ memory-capture/
         ├─ SKILL.md
         └─ scripts/
            ├─ codex_memory_nudge.py
            ├─ codex_session_watcher.py
            ├─ compact_user_memory.py
            ├─ extract_memory.py
            ├─ extract_skill_candidate.py
            ├─ extract_skill_patch_candidate.py
            ├─ generate_skills_index.py
            ├─ learning_loop_common.py
            ├─ promote_candidates.py
            ├─ promote_memory.py
            ├─ record_skill_usage.py
            ├─ scan_skill_candidates.py
            ├─ show_skill_usage.py
            └─ summarize_learning_inbox.py
```

## Runtime Outputs

Default runtime outputs live under `$HOME/.codex`:

```text
.codex/
├─ memories/
│  ├─ USER.md
│  ├─ inbox/
│  └─ archive/
├─ skill-candidates/
│  ├─ inbox/
│  ├─ patches/
│  └─ archive/
├─ daily-digests/
├─ nudge-reports/
├─ latest-skill-candidate-security-scan.md
├─ latest-user-memory-budget.md
├─ memory-watcher-state.json
├─ skill-usage.json
├─ skills-index.md
└─ learning-inbox-summary.md
```

Generated candidate files are grouped by date, for example `$HOME/.codex/memories/inbox/YYYY/MM/DD/*.md`, but empty candidate reports are skipped by default. The main daily entry point is `$HOME/.codex/daily-digests/YYYY/MM/DD/review-digest.md`. Security scan and memory budget reports are overwritten at `latest-*` paths to reduce file count. Detailed nudge reports are written only when candidates are found or a step fails.

## Automatic Session Watcher

Codex does not always expose a reliable session-end hook across every environment. The watcher provides a lightweight external trigger:

```text
poll $HOME/.codex/sessions
  -> find idle unprocessed session files
  -> run codex_memory_nudge.py --session-file <file>
  -> write daily digest, latest reports, optional nudge report, and watcher state
```

Defaults:

| Option                   | Default |
| ------------------------ | ------: |
| `--interval-seconds`     | `86400` |
| `--idle-seconds`         |   `600` |
| `--max-sessions-per-run` |     `0` |

`--max-sessions-per-run 0` means all ready sessions in the current cycle. This is the default because the watcher is I/O-light and uses a lock plus processed-session state to avoid duplicate work.

By default, the first run processes all historical session files that are idle and not already marked processed. To limit the first run and future runs to a time window, pass `--since-date YYYY-MM-DD`.

The watcher is review-first. It creates candidate reports automatically, but it does not run `promote_memory.py --approved`, does not apply skill patches, and does not auto-promote candidates into `USER.md`.

After each real watcher cycle, the nudge prints a Review Digest summary and writes both `$HOME/.codex/learning-inbox-summary.md` and `$HOME/.codex/daily-digests/YYYY/MM/DD/review-digest.md`. The digest groups memory candidates, skill candidates, and skill patch candidates, then lists promotion options. Memory options include explicit `promote_memory.py --approved` commands. Skill and patch options remain review-only and point you to scan and inspect the target skill before applying anything.

Candidate extraction reads both user instructions and assistant outcomes. It favors durable lessons such as root causes, fixes, verification results, reusable workflows, preferences, and safety corrections. One-off task requests such as "find X", "list Y", or "only return Z" are treated as work items rather than long-term memory.

Examples:

```bash
# Long-running watcher
python "$HOME/.agents/skills/memory-capture/scripts/codex_session_watcher.py"

# One cycle without writing reports
python "$HOME/.agents/skills/memory-capture/scripts/codex_session_watcher.py" --once --dry-run

# One real cycle
python "$HOME/.agents/skills/memory-capture/scripts/codex_session_watcher.py" --once

# Only process sessions on or after a date
python "$HOME/.agents/skills/memory-capture/scripts/codex_session_watcher.py" --once --since-date 2026-05-01

# Install a daily 12:00 OS schedule, using the installed watcher under $HOME/.agents
python install_watcher_schedule.py
```

For workstation setups, a daily OS scheduler that runs the `--once` command at 12:00 is usually more reliable than keeping a terminal process open. Long-running mode remains available when a persistent process manager is already in use.

Schedule installer backends:

| Platform | Backend                           |
| -------- | --------------------------------- |
| Windows  | Task Scheduler via `schtasks.exe /SC DAILY /ST 12:00` |
| Linux    | systemd user timer with `OnCalendar=*-*-* 12:00:00` |
| macOS    | `launchd` LaunchAgent with `Hour=12`, `Minute=0` |

## Safety Model

This project intentionally separates discovery from promotion.

| Stage   | Behavior                                                                                    |
| ------- | ------------------------------------------------------------------------------------------- |
| Capture | Writes review-only candidate files                                                          |
| Scan    | Flags secrets, redacted values, prompt injection text, private URLs, and transcript markers |
| Score   | Identifies repeated, short, safe preference candidates                                      |
| Promote | Requires explicit `--approved`, except conservative `--auto-promote` candidate flow         |
| Archive | Moves only processed candidate files; unresolved review items stay visible                  |

Hard rules:

- Never store raw secrets in memory files.
- Never reconstruct `[REDACTED]` values.
- Treat `conflict_review` as a hard stop for automatic promotion.
- Keep project facts in project-level `AGENTS.md`, not global `USER.md`.
- Review and scan skill candidates before turning them into real skills.

## Development

Run local verification:

```bash
python tests/verify-install.py --codex-root ./tmp/codex --agents-root ./tmp/agents
python tests/verify-learning-extraction.py --work-root ./tmp/learning
```

Run syntax checks:

```bash
python -m compileall agents install.py install_watcher_schedule.py tests
```

## Inspiration

- [Hermes Agent](https://github.com/NousResearch/hermes-agent): the self-improving agent loop built around memory, skill creation, skill evolution, session search, and learning nudges.

## License

MIT
