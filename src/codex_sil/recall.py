"""SQLite-backed session recall with redacted snippets."""

from __future__ import annotations

import json
import re
from pathlib import Path

from .db import connect, init_db
from .scanner import read_session_text


SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{6,}"),
    re.compile(r"(?i)(token|api[_-]?key|password|secret)\s*[:=]\s*['\"]?[^'\"\s]+"),
]


def redact(text: str) -> str:
    redacted = text
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return redacted


def snippet(text: str, query: str, limit: int = 260) -> str:
    lower = text.casefold()
    needle = query.casefold()
    index = lower.find(needle)
    if index < 0:
        index = 0
    start = max(0, index - 80)
    end = min(len(text), index + len(query) + 180)
    excerpt = text[start:end].strip()
    if start > 0:
        excerpt = "..." + excerpt
    if end < len(text):
        excerpt += "..."
    return redact(excerpt[:limit])


def search(root: Path, query: str, max_results: int = 10) -> dict[str, object]:
    init_db(root)
    results: list[dict[str, object]] = []
    with connect(root) as conn:
        sessions = conn.execute("select id, path, rel_path from sessions order by last_processed_at desc, id desc").fetchall()
        sources = conn.execute(
            """
            select c.id, c.type, c.text, c.destination, s.rel_path
            from candidates c
            left join candidate_sources cs on cs.candidate_id=c.id
            left join sessions s on s.id=cs.session_id
            order by c.updated_at desc
            """
        ).fetchall()
    needle = query.casefold()
    for row in sessions:
        text = read_session_text(Path(row["path"]))
        if needle in text.casefold():
            results.append({"kind": "session", "path": row["rel_path"], "snippet": snippet(text, query)})
            if len(results) >= max_results:
                return {"query": query, "results": results}
    for row in sources:
        text = str(row["text"])
        if needle in text.casefold():
            results.append(
                {
                    "kind": "candidate",
                    "path": row["rel_path"],
                    "type": row["type"],
                    "destination": row["destination"],
                    "snippet": snippet(text, query),
                }
            )
            if len(results) >= max_results:
                break
    return {"query": query, "results": results}
