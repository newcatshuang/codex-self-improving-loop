#!/usr/bin/env python3
"""Watch Codex session files and run the self-improving nudge after idle periods."""

from __future__ import annotations

import argparse
from datetime import date, datetime
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from learning_loop_common import default_codex_root, ensure_dir, now_iso, read_text, write_text


def load_state(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(read_text(path, "{}"))
    except json.JSONDecodeError:
        data = {}
    if not isinstance(data, dict):
        data = {}
    data.setdefault("processed", {})
    data.setdefault("processed_paths", {})
    data.setdefault("events", [])
    return data


def save_state(path: Path, state: dict[str, Any]) -> None:
    state["events"] = state.get("events", [])[-50:]
    write_text(path, json.dumps(state, indent=2, ensure_ascii=False) + "\n")


def backfill_processed_paths(state: dict[str, Any]) -> None:
    processed_paths = state.setdefault("processed_paths", {})
    for event in state.get("events", []):
        if not isinstance(event, dict) or event.get("returncode") != 0:
            continue
        session = event.get("session")
        if not session:
            continue
        path = Path(str(session))
        try:
            fp = path_fingerprint(path)
        except OSError:
            continue
        processed_paths.setdefault(fp["path"], {"at": event.get("at"), "mtime": fp["mtime"], "size": fp["size"]})


def session_key(path: Path, root: Path | None = None) -> str:
    resolved = path.expanduser().resolve()
    try:
        stat = resolved.stat()
    except FileNotFoundError:
        return str(resolved)
    if root is not None:
        try:
            name = str(resolved.relative_to(root.expanduser().resolve()))
        except ValueError:
            name = str(resolved)
    else:
        name = str(resolved)
    return f"{name.replace(os.sep, '/')}|{int(stat.st_mtime)}|{stat.st_size}"


def legacy_session_keys(path: Path) -> list[str]:
    resolved = path.expanduser().resolve()
    try:
        stat = resolved.stat()
    except FileNotFoundError:
        return [str(resolved)]
    return [
        str(resolved),
        f"{resolved}|{stat.st_mtime_ns}|{stat.st_size}",
        f"{resolved}|{int(stat.st_mtime)}|{stat.st_size}",
    ]


def is_processed(path: Path, root: Path, processed: dict[str, Any]) -> bool:
    keys = [session_key(path, root), *legacy_session_keys(path)]
    return any(key in processed for key in keys)


def path_fingerprint(path: Path) -> dict[str, Any]:
    resolved = path.expanduser().resolve()
    stat = resolved.stat()
    return {"path": str(resolved), "mtime": int(stat.st_mtime), "size": stat.st_size}


def is_processed_path(path: Path, processed_paths: dict[str, Any]) -> bool:
    try:
        fp = path_fingerprint(path)
    except OSError:
        return False
    entry = processed_paths.get(fp["path"])
    if not isinstance(entry, dict):
        return False
    if entry.get("baseline") is True:
        return False
    return int(entry.get("mtime", -1)) == fp["mtime"] and int(entry.get("size", -1)) == fp["size"]


def iter_watcher_session_files(root: Path) -> list[Path]:
    sessions_dir = root.expanduser() / "sessions"
    if not sessions_dir.exists():
        return []
    files = [*sessions_dir.rglob("*.jsonl"), *sessions_dir.rglob("*.json")]
    return sorted({path.resolve() for path in files if path.is_file()}, key=lambda path: path.stat().st_mtime)


def parse_since_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("--since-date must use YYYY-MM-DD") from exc


def session_date(path: Path, root: Path) -> date:
    resolved = path.expanduser().resolve()
    sessions_dir = (root.expanduser() / "sessions").resolve()
    try:
        relative_parts = resolved.relative_to(sessions_dir).parts
    except ValueError:
        relative_parts = ()
    if len(relative_parts) >= 4:
        year, month, day = relative_parts[:3]
        if year.isdigit() and month.isdigit() and day.isdigit():
            try:
                return date(int(year), int(month), int(day))
            except ValueError:
                pass
    return datetime.fromtimestamp(resolved.stat().st_mtime).date()


def find_ready_sessions(root: Path, state: dict[str, Any], idle_seconds: int, max_sessions: int, since: date | None) -> list[Path]:
    now = time.time()
    processed = state.get("processed", {})
    processed_paths = state.get("processed_paths", {})
    ready: list[Path] = []
    for path in iter_watcher_session_files(root):
        if not path.exists() or not path.is_file():
            continue
        try:
            stat = path.stat()
        except OSError:
            continue
        if stat.st_size <= 0:
            continue
        if since is not None and session_date(path, root) < since:
            continue
        if now - stat.st_mtime < idle_seconds:
            continue
        if is_processed(path, root, processed) or is_processed_path(path, processed_paths):
            continue
        ready.append(path)
        if max_sessions > 0 and len(ready) >= max_sessions:
            break
    return ready


def acquire_lock(lock_path: Path, stale_seconds: int) -> bool:
    ensure_dir(lock_path.parent)
    now = time.time()
    try:
        fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        try:
            age = now - lock_path.stat().st_mtime
        except OSError:
            return False
        if age < stale_seconds:
            return False
        try:
            lock_path.unlink()
        except OSError:
            return False
        return acquire_lock(lock_path, stale_seconds)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(json.dumps({"pid": os.getpid(), "created_at": now_iso()}, ensure_ascii=False))
    return True


def release_lock(lock_path: Path) -> None:
    try:
        lock_path.unlink()
    except FileNotFoundError:
        pass


def run_nudge(script_dir: Path, root: Path, session: Path, report_dir: Path, max_messages: int) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    command = [
        sys.executable,
        str(script_dir / "codex_memory_nudge.py"),
        "--root",
        str(root),
        "--session-file",
        str(session),
        "--report-dir",
        str(report_dir),
        "--max-messages",
        str(max_messages),
    ]
    return subprocess.run(command, text=True, capture_output=True, encoding="utf-8", errors="replace", env=env)


def process_once(args: argparse.Namespace) -> int:
    root = args.root.expanduser()
    state_path = args.state_file.expanduser() if args.state_file else root / "memory-watcher-state.json"
    report_dir = args.report_dir.expanduser() if args.report_dir else root / "nudge-reports"
    lock_path = args.lock_file.expanduser() if args.lock_file else root / ".tmp" / "memory-watcher.lock"
    since = args.since_date
    ensure_dir(report_dir)

    if not acquire_lock(lock_path, args.lock_stale_seconds):
        print(f"Another watcher appears to be running: {lock_path}")
        return 0
    try:
        state = load_state(state_path)
        backfill_processed_paths(state)
        ready = find_ready_sessions(root, state, args.idle_seconds, args.max_sessions_per_run, since)
        if args.dry_run:
            print(
                json.dumps(
                    {
                        "ready_sessions": [str(path) for path in ready],
                        "state_file": str(state_path),
                        "since_date": args.since_date.isoformat() if args.since_date else None,
                        "max_sessions_per_run": args.max_sessions_per_run,
                    },
                    indent=2,
                    ensure_ascii=False,
                )
            )
            return 0

        script_dir = Path(__file__).resolve().parent
        processed = state.setdefault("processed", {})
        processed_paths = state.setdefault("processed_paths", {})
        events = state.setdefault("events", [])
        failures = 0
        for session in ready:
            key = session_key(session, root)
            completed = run_nudge(script_dir, root, session, report_dir, args.max_messages)
            event = {
                "at": now_iso(),
                "session": str(session),
                "session_key": key,
                "returncode": completed.returncode,
                "stdout": (completed.stdout or "").strip()[-2000:],
                "stderr": (completed.stderr or "").strip()[-2000:],
            }
            events.append(event)
            if completed.returncode == 0:
                processed[key] = {"at": event["at"], "session": str(session)}
                try:
                    fp = path_fingerprint(session)
                    processed_paths[fp["path"]] = {"at": event["at"], "mtime": fp["mtime"], "size": fp["size"]}
                except OSError:
                    pass
                print(f"Processed session: {session}")
                if completed.stdout:
                    print(completed.stdout.strip())
            else:
                failures += 1
                print(f"Failed session: {session}", file=sys.stderr)
                if completed.stderr:
                    print(completed.stderr, file=sys.stderr)
        save_state(state_path, state)
        if not ready:
            print("No idle unprocessed Codex sessions found.")
        return 1 if failures else 0
    finally:
        release_lock(lock_path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_codex_root(), help="Codex root directory")
    parser.add_argument("--interval-seconds", type=int, default=86400, help="Polling interval in seconds")
    parser.add_argument("--idle-seconds", type=int, default=600, help="Session must be unchanged for this long before processing")
    parser.add_argument("--max-messages", type=int, default=80)
    parser.add_argument("--max-sessions-per-run", type=int, default=0, help="Maximum sessions per cycle; 0 means all ready sessions")
    parser.add_argument("--state-file", type=Path)
    parser.add_argument("--lock-file", type=Path)
    parser.add_argument("--report-dir", type=Path)
    parser.add_argument("--lock-stale-seconds", type=int, default=7200)
    parser.add_argument("--once", action="store_true", help="Run one polling cycle and exit")
    parser.add_argument("--dry-run", action="store_true", help="Show sessions that would be processed without running nudge")
    parser.add_argument("--since-date", type=parse_since_date, help="Only process sessions on or after YYYY-MM-DD")
    args = parser.parse_args()

    if args.once or args.dry_run:
        return process_once(args)

    print(f"Watching Codex sessions under {args.root.expanduser()} every {args.interval_seconds}s.")
    while True:
        code = process_once(args)
        if code:
            print(f"Watcher cycle completed with failures: {code}", file=sys.stderr)
        time.sleep(args.interval_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
