"""SQLite FTS synchronization helpers."""

from __future__ import annotations

import sqlite3


def fts_available(conn: sqlite3.Connection) -> bool:
    try:
        conn.execute("select rowid from sessions_fts limit 1").fetchone()
        conn.execute("select rowid from candidates_fts limit 1").fetchone()
        return True
    except sqlite3.DatabaseError:
        return False


def sync_session(conn: sqlite3.Connection, session_id: int, rel_path: str, body: str) -> None:
    if not fts_available(conn):
        return
    conn.execute("delete from sessions_fts where session_id=?", (session_id,))
    conn.execute(
        "insert into sessions_fts(session_id, rel_path, body) values(?, ?, ?)",
        (session_id, rel_path, body),
    )


def sync_candidate(conn: sqlite3.Connection, candidate_id: int) -> None:
    if not fts_available(conn):
        return
    row = conn.execute(
        "select id, type, destination, title, text, rewrite_suggestion from candidates where id=?",
        (candidate_id,),
    ).fetchone()
    if row is None:
        return
    conn.execute("delete from candidates_fts where candidate_id=?", (candidate_id,))
    conn.execute(
        """
        insert into candidates_fts(candidate_id, type, destination, title, body, rewrite)
        values(?, ?, ?, ?, ?, ?)
        """,
        (
            int(row["id"]),
            str(row["type"]),
            str(row["destination"]),
            str(row["title"]),
            str(row["text"]),
            str(row["rewrite_suggestion"]),
        ),
    )


def clear(conn: sqlite3.Connection) -> None:
    if not fts_available(conn):
        return
    conn.execute("delete from sessions_fts")
    conn.execute("delete from candidates_fts")
