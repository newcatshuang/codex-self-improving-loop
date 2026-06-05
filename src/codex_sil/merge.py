"""Candidate merge suggestion generation and application."""

from __future__ import annotations

import difflib
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from .db import connect, init_db
from .fallback_extractor import normalize


SIMILARITY_THRESHOLD = 0.72


def candidate_signature(row: dict[str, object]) -> str:
    text = str(row.get("rewrite_suggestion") or row.get("text") or "")
    normalized = normalize(text)
    words = [word for word in normalized.split() if len(word) > 2]
    return " ".join(words[:18]) or normalized


def similarity(left: str, right: str) -> float:
    if not left or not right:
        return 0
    left_words = set(left.split())
    right_words = set(right.split())
    overlap = len(left_words & right_words) / max(1, min(len(left_words), len(right_words)))
    sequence = difflib.SequenceMatcher(None, left, right).ratio()
    return max(overlap, sequence)


def _load_candidates(root: Path) -> list[dict[str, object]]:
    with connect(root) as conn:
        return [
            dict(row)
            for row in conn.execute(
                """
                select id, type, title, text, normalized, destination, rewrite_suggestion, status, confidence
                from candidates
                where status not in ('promoted', 'archived', 'rejected', 'merged')
                order by confidence desc, id asc
                """
            )
        ]


def generate_merge_suggestions(root: Path) -> dict[str, object]:
    init_db(root)
    rows = _load_candidates(root)
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["type"]), str(row["destination"]))].append(row)
    suggestions: list[dict[str, object]] = []
    for (candidate_type, destination), items in grouped.items():
        consumed: set[int] = set()
        for item in items:
            item_id = int(item["id"])
            if item_id in consumed:
                continue
            signature = candidate_signature(item)
            peers: list[dict[str, object]] = [item]
            for peer in items:
                peer_id = int(peer["id"])
                if peer_id == item_id or peer_id in consumed:
                    continue
                if similarity(signature, candidate_signature(peer)) >= SIMILARITY_THRESHOLD:
                    peers.append(peer)
            if len(peers) < 2:
                continue
            peers = sorted(peers, key=lambda row: (-float(row.get("confidence") or 0), int(row["id"])))
            primary = peers[0]
            duplicates = peers[1:]
            ids = [int(row["id"]) for row in peers]
            group_key = hashlib.sha256(f"{candidate_type}:{destination}:{':'.join(map(str, sorted(ids)))}".encode("utf-8")).hexdigest()
            recommended_text = str(primary.get("rewrite_suggestion") or primary.get("text") or "")
            reason = f"{len(peers)} similar {candidate_type} candidates share destination {destination}."
            with connect(root) as conn:
                conn.execute(
                    """
                    insert into merge_suggestions(group_key, primary_candidate_id, duplicate_candidate_ids, recommended_text, reason, status)
                    values(?, ?, ?, ?, ?, 'review')
                    on conflict(group_key) do update set
                      primary_candidate_id=excluded.primary_candidate_id,
                      duplicate_candidate_ids=excluded.duplicate_candidate_ids,
                      recommended_text=excluded.recommended_text,
                      reason=excluded.reason,
                      updated_at=current_timestamp
                    """,
                    (group_key, int(primary["id"]), json.dumps([int(row["id"]) for row in duplicates]), recommended_text, reason),
                )
            suggestions.append(
                {
                    "group_key": group_key,
                    "candidate_ids": ids,
                    "primary_candidate_id": int(primary["id"]),
                    "duplicate_candidate_ids": [int(row["id"]) for row in duplicates],
                    "recommended_text": recommended_text,
                    "reason": reason,
                }
            )
            consumed.update(ids)
    return merge_suggestions_payload(root)


def merge_suggestions_payload(root: Path) -> dict[str, object]:
    init_db(root)
    with connect(root) as conn:
        rows = [dict(row) for row in conn.execute("select * from merge_suggestions order by updated_at desc, id desc")]
    items: list[dict[str, object]] = []
    for row in rows:
        duplicates = json.loads(str(row["duplicate_candidate_ids"] or "[]"))
        candidate_ids = [int(row["primary_candidate_id"]), *[int(item) for item in duplicates]]
        row["duplicate_candidate_ids"] = duplicates
        row["candidate_ids"] = candidate_ids
        items.append(row)
    return {"merge_suggestions": items}


def apply_merge_suggestion(root: Path, suggestion_id: int) -> dict[str, object]:
    init_db(root)
    with connect(root) as conn:
        row = conn.execute("select * from merge_suggestions where id=?", (suggestion_id,)).fetchone()
        if row is None:
            raise ValueError(f"merge suggestion not found: {suggestion_id}")
        duplicates = [int(item) for item in json.loads(str(row["duplicate_candidate_ids"] or "[]"))]
        for candidate_id in duplicates:
            conn.execute("update candidates set status='merged', updated_at=current_timestamp where id=?", (candidate_id,))
        conn.execute("update merge_suggestions set status='merged', updated_at=current_timestamp where id=?", (suggestion_id,))
        conn.execute(
            "insert into audit_log(action, target, detail) values('merge_candidates', ?, ?)",
            (str(row["primary_candidate_id"]), json.dumps({"merged": duplicates}, ensure_ascii=False)),
        )
    return {"id": suggestion_id, "status": "merged", "merged_candidate_ids": duplicates}
