#!/usr/bin/env python3
"""Verify schema migrations are explicit, idempotent, and preserve old data."""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--work-root", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    root = args.work_root.resolve()
    db = root / "self-improving-loop" / "self-improving-loop.sqlite"
    db.parent.mkdir(parents=True, exist_ok=True)
    if db.exists():
        db.unlink()
    with sqlite3.connect(db) as conn:
        conn.execute("create table settings(key text primary key, value text not null, updated_at text not null default current_timestamp)")
        conn.execute("insert into settings(key, value) values('schema_version', '2.0.0')")
        conn.execute(
            """
            create table candidates(
              id integer primary key autoincrement,
              type text not null,
              title text not null,
              text text not null,
              normalized text not null,
              destination text not null,
              rewrite_suggestion text not null,
              status text not null default 'review',
              safety text not null default 'review',
              confidence real not null default 0,
              extractor text not null,
              created_at text not null default current_timestamp,
              updated_at text not null default current_timestamp,
              unique(type, normalized)
            )
            """
        )
        conn.execute(
            """
            insert into candidates(type, title, text, normalized, destination, rewrite_suggestion, safety, confidence, extractor)
            values('memory', 'Legacy memory', 'Keep this legacy row.', 'keep this legacy row', 'global_user_memory', 'Keep this legacy row.', 'review', 0.6, 'legacy')
            """
        )

    sys.path.insert(0, str(repo / "src"))
    from codex_sil.db import init_db

    init_db(root)
    init_db(root)
    with sqlite3.connect(db) as conn:
        tables = {str(row[0]) for row in conn.execute("select name from sqlite_master where type in ('table', 'virtual')")}
        required = {"recommendations", "merge_suggestions", "digests", "sessions_fts", "candidates_fts", "schema_migrations"}
        if not required.issubset(tables):
            raise AssertionError(f"migration should create v3 tables: {tables}")
        version = str(conn.execute("select value from settings where key='schema_version'").fetchone()[0])
        if not version.startswith("3."):
            raise AssertionError(f"schema_version should be upgraded to v3: {version}")
        rows = int(conn.execute("select count(*) from candidates where title='Legacy memory'").fetchone()[0])
        if rows != 1:
            raise AssertionError("migration should preserve existing candidate rows")
        applied = int(conn.execute("select count(*) from schema_migrations").fetchone()[0])
        if applied < 1:
            raise AssertionError("migration should record applied steps")
        duplicate_names = conn.execute(
            "select name, count(*) from schema_migrations group by name having count(*) > 1"
        ).fetchall()
        if duplicate_names:
            raise AssertionError(f"migrations must be idempotent: {duplicate_names}")

    print("verify-v3-migration passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
