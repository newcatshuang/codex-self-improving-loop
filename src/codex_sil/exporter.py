"""On-demand exports from the SQLite control plane."""

from __future__ import annotations

import json
from pathlib import Path

from .db import connect, init_db
from .paths import exports_dir
from .scanner import now_stamp


def export_candidates(root: Path) -> Path:
    init_db(root)
    output = exports_dir(root) / f"candidates-{now_stamp()}.json"
    with connect(root) as conn:
        rows = [dict(row) for row in conn.execute("select * from candidates order by updated_at desc")]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output


def export_digest(root: Path) -> Path:
    init_db(root)
    output = exports_dir(root) / f"review-digest-{now_stamp()}.md"
    with connect(root) as conn:
        rows = conn.execute("select type, destination, status, text from candidates order by updated_at desc limit 100").fetchall()
    lines = ["# Codex Self-Improving Loop Review Digest", ""]
    for row in rows:
        lines.append(f"- **{row['type']}** `{row['destination']}` `{row['status']}`: {row['text']}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output
