---
name: session-recall
description: Use when the user asks to find, recall, search, or summarize prior Codex conversations, mentions previous sessions, says "last time", "previously", "history", "上次", "之前", "历史会话", or needs context recovered from local Codex history without exposing secrets.
---

# Session Recall

## Purpose

Recover useful context from prior Codex sessions with narrow local search. Prefer short, redacted excerpts over loading entire transcripts.

## When To Use

Use this skill when the user asks about:

- A previous or historical Codex conversation.
- Something they said before, asked last time, or want to continue from.
- Recovering project decisions, errors, commands, file names, or summaries from earlier sessions.
- Comparing current work with a prior session.

Do not use it for current repository code search; use project search or code intelligence tools for that.

## Workflow

1. Identify 1-4 distinctive search terms from the user's request.
2. Run the bundled search script:

```bash
python "$HOME/.agents/skills/session-recall/scripts/search_sessions.py" --query "keyword" --max-results 10
```

3. Read only the redacted snippets returned by the script.
4. If results are noisy, refine the query instead of opening full transcript files.
5. Summarize findings with dates, session files, and short evidence snippets.

## Safety Rules

- Never print raw secrets from session history.
- Do not open a full session transcript unless the user explicitly asks and the search snippet is insufficient.
- Treat snippets as potentially stale context. Verify against current repository files before editing code.
- If a result contains `[REDACTED]`, do not try to reconstruct the hidden value.

## Useful Options

```bash
# Search a custom Codex root.
python "$HOME/.agents/skills/session-recall/scripts/search_sessions.py" --query "GitNexus impact" --root "$HOME/.codex"

# JSON output for automation.
python "$HOME/.agents/skills/session-recall/scripts/search_sessions.py" --query "error code" --json
```
