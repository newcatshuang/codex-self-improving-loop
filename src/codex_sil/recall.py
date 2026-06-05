"""SQLite-backed session recall with redacted snippets."""

from __future__ import annotations

import json
import re
import sqlite3
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


def fts_query(query: str) -> str:
    terms = [term for term in re.findall(r"[\w\u4e00-\u9fff]+", query, flags=re.UNICODE) if term]
    if not terms:
        return '"' + query.replace('"', '""') + '"'
    return " OR ".join('"' + term.replace('"', '""') + '"' for term in terms)


def fts_search(root: Path, query: str, max_results: int) -> list[dict[str, object]] | None:
    results: list[dict[str, object]] = []
    match = fts_query(query)
    try:
        with connect(root) as conn:
            session_rows = conn.execute(
                """
                select
                  'session' as kind,
                  s.rel_path as path,
                  snippet(sessions_fts, 2, '<mark>', '</mark>', '...', 18) as snippet,
                  bm25(sessions_fts) as rank
                from sessions_fts
                join sessions s on s.id=sessions_fts.session_id
                where sessions_fts match ?
                order by rank
                limit ?
                """,
                (match, max_results),
            ).fetchall()
            for row in session_rows:
                results.append(
                    {
                        "kind": "session",
                        "path": str(row["path"]),
                        "snippet": redact(str(row["snippet"])),
                        "rank": float(row["rank"] or 0),
                        "search": "fts",
                    }
                )
            remaining = max_results - len(results)
            if remaining > 0:
                candidate_rows = conn.execute(
                    """
                    select
                      c.type,
                      c.destination,
                      c.id,
                      s.rel_path as path,
                      snippet(candidates_fts, 4, '<mark>', '</mark>', '...', 18) as snippet,
                      bm25(candidates_fts) as rank
                    from candidates_fts
                    join candidates c on c.id=candidates_fts.candidate_id
                    left join candidate_sources cs on cs.candidate_id=c.id
                    left join sessions s on s.id=cs.session_id
                    where candidates_fts match ?
                    group by c.id
                    order by rank
                    limit ?
                    """,
                    (match, remaining),
                ).fetchall()
                for row in candidate_rows:
                    results.append(
                        {
                            "kind": "candidate",
                            "path": str(row["path"] or ""),
                            "type": str(row["type"]),
                            "destination": str(row["destination"]),
                            "snippet": redact(str(row["snippet"])),
                            "rank": float(row["rank"] or 0),
                            "search": "fts",
                        }
                    )
    except sqlite3.DatabaseError:
        return None
    return results


def fallback_search(root: Path, query: str, max_results: int) -> list[dict[str, object]]:
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
            results.append({"kind": "session", "path": row["rel_path"], "snippet": snippet(text, query), "rank": len(results), "search": "fallback"})
            if len(results) >= max_results:
                return results
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
                    "rank": len(results),
                    "search": "fallback",
                }
            )
            if len(results) >= max_results:
                break
    return results


def search(root: Path, query: str, max_results: int = 10) -> dict[str, object]:
    init_db(root)
    results = fts_search(root, query, max_results)
    if results is None or not results:
        results = fallback_search(root, query, max_results)
    return {"query": query, "results": results}
