"""SQLite storage for Codex Self-Improving Loop."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from . import __version__
from .paths import db_path, ensure_runtime


SCHEMA_PATH = Path(__file__).with_name("schema.sql")
SCHEMA_VERSION = __version__
MIGRATIONS: tuple[tuple[str, str], ...] = (
    (
        "0001_v3_control_plane",
        """
        create table if not exists recommendations (
          id integer primary key autoincrement,
          candidate_id integer not null unique references candidates(id) on delete cascade,
          recommendation text not null,
          recommendation_reason text not null,
          suggested_action text not null,
          engine text not null,
          error text not null default '',
          created_at text not null default current_timestamp,
          updated_at text not null default current_timestamp
        );
        create table if not exists merge_suggestions (
          id integer primary key autoincrement,
          group_key text not null unique,
          primary_candidate_id integer not null references candidates(id) on delete cascade,
          duplicate_candidate_ids text not null,
          recommended_text text not null,
          reason text not null,
          status text not null default 'review',
          created_at text not null default current_timestamp,
          updated_at text not null default current_timestamp
        );
        create table if not exists digests (
          id integer primary key autoincrement,
          run_id integer references runs(id) on delete set null,
          digest_date text not null,
          summary text not null,
          new_candidates integer not null default 0,
          recommended_promotions integer not null default 0,
          risk_items integer not null default 0,
          skill_usage_changes integer not null default 0,
          failed_runs integer not null default 0,
          created_at text not null default current_timestamp
        );
        """,
    ),
    (
        "0002_llm_evolution_proposals",
        """
        create table if not exists candidate_analyses (
          id integer primary key autoincrement,
          candidate_id integer not null unique references candidates(id) on delete cascade,
          engine text not null,
          evidence_assessment text not null,
          stability text not null,
          scope text not null,
          risk_level text not null,
          conflicts text not null,
          rewrite_quality text not null,
          recommended_next_step text not null,
          error text not null default '',
          created_at text not null default current_timestamp,
          updated_at text not null default current_timestamp
        );
        create table if not exists evolution_proposals (
          id integer primary key autoincrement,
          candidate_id integer not null unique references candidates(id) on delete cascade,
          engine text not null,
          target_type text not null,
          target_path text not null,
          proposed_text text not null,
          rationale text not null,
          verification text not null,
          requires_manual_approval integer not null default 1,
          created_at text not null default current_timestamp,
          updated_at text not null default current_timestamp
        );
        """,
    ),
    (
        "0003_engine_failure_reasons",
        """
        alter table recommendations add column error text not null default '';
        """,
    ),
    (
        "0004_analysis_failure_reasons",
        """
        alter table candidate_analyses add column error text not null default '';
        """,
    ),
    (
        "0005_bilingual_ai_guidance",
        """
        alter table recommendations add column recommendation_en text not null default '';
        alter table recommendations add column recommendation_zh text not null default '';
        alter table recommendations add column recommendation_reason_en text not null default '';
        alter table recommendations add column recommendation_reason_zh text not null default '';
        alter table candidate_analyses add column evidence_assessment_en text not null default '';
        alter table candidate_analyses add column evidence_assessment_zh text not null default '';
        alter table candidate_analyses add column conflicts_en text not null default '';
        alter table candidate_analyses add column conflicts_zh text not null default '';
        alter table candidate_analyses add column rewrite_quality_en text not null default '';
        alter table candidate_analyses add column rewrite_quality_zh text not null default '';
        alter table candidate_analyses add column recommended_next_step_en text not null default '';
        alter table candidate_analyses add column recommended_next_step_zh text not null default '';
        alter table evolution_proposals add column proposed_text_en text not null default '';
        alter table evolution_proposals add column proposed_text_zh text not null default '';
        alter table evolution_proposals add column rationale_en text not null default '';
        alter table evolution_proposals add column rationale_zh text not null default '';
        alter table evolution_proposals add column verification_en text not null default '';
        alter table evolution_proposals add column verification_zh text not null default '';
        """,
    ),
)


def connect(root: Path | None = None) -> sqlite3.Connection:
    ensure_runtime(root)
    conn = sqlite3.connect(db_path(root))
    conn.row_factory = sqlite3.Row
    conn.execute("pragma foreign_keys = on")
    return conn


def apply_migrations(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        create table if not exists schema_migrations (
          name text primary key,
          applied_at text not null default current_timestamp
        )
        """
    )
    for name, sql in MIGRATIONS:
        existing = conn.execute("select 1 from schema_migrations where name=?", (name,)).fetchone()
        if existing:
            continue
        for statement in (part.strip() for part in sql.split(";")):
            if not statement:
                continue
            try:
                conn.execute(statement)
            except sqlite3.OperationalError as exc:
                if "duplicate column name" not in str(exc).lower():
                    raise
        conn.execute("insert into schema_migrations(name) values(?)", (name,))
    ensure_fts_tables(conn)
    conn.execute(
        "insert into settings(key, value) values('schema_version', ?) "
        "on conflict(key) do update set value=excluded.value, updated_at=current_timestamp",
        (SCHEMA_VERSION,),
    )


def ensure_fts_tables(conn: sqlite3.Connection) -> None:
    try:
        conn.execute("create virtual table if not exists sessions_fts using fts5(session_id unindexed, rel_path, body)")
        conn.execute(
            "create virtual table if not exists candidates_fts using fts5(candidate_id unindexed, type unindexed, destination, title, body, rewrite)"
        )
    except sqlite3.DatabaseError:
        conn.execute(
            "insert into settings(key, value) values('fts5_available', '0') "
            "on conflict(key) do update set value='0', updated_at=current_timestamp"
        )
    else:
        conn.execute(
            "insert into settings(key, value) values('fts5_available', '1') "
            "on conflict(key) do update set value='1', updated_at=current_timestamp"
        )


def init_db(root: Path | None = None) -> Path:
    ensure_runtime(root)
    path = db_path(root)
    with connect(root) as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        apply_migrations(conn)
    return path
