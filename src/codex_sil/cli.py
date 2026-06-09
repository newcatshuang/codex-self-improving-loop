"""CLI implementation for Codex Self-Improving Loop v3."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .app import serve, smoke
from . import __version__
from .db import init_db
from .paths import db_path, ensure_runtime, html_path, runtime_dir
from .recall import search
from .scanner import rebuild, scan_once
from .scheduler import install_schedule, install_shortcut, uninstall_schedule, uninstall_shortcut


LOCAL_HOST = "127.0.0.1"


def cmd_doctor(args: argparse.Namespace) -> int:
    root = args.codex_root.expanduser().resolve()
    payload = {
        "version": __version__,
        "codex_root": str(root),
        "runtime_dir": str(runtime_dir(root)),
        "database": str(db_path(root)),
        "webui": str(html_path(root)),
        "service_host": LOCAL_HOST,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    path = init_db(args.codex_root)
    print(f"Initialized database: {path}")
    return 0


def cmd_rebuild(args: argparse.Namespace) -> int:
    result = rebuild(args.codex_root.expanduser().resolve(), backup=args.backup)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_scan(args: argparse.Namespace) -> int:
    result = scan_once(args.codex_root.expanduser().resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    root = args.codex_root.expanduser().resolve()
    if args.smoke_test:
        print(json.dumps(smoke(root), ensure_ascii=False, indent=2))
        return 0
    return serve(root, port=args.port, open_browser=args.open)


def cmd_schedule_install(args: argparse.Namespace) -> int:
    repo = Path(__file__).resolve().parents[2]
    print(install_schedule(repo, args.codex_root.expanduser().resolve(), dry_run=args.dry_run))
    return 0


def cmd_schedule_uninstall(args: argparse.Namespace) -> int:
    print(uninstall_schedule(args.codex_root.expanduser().resolve(), dry_run=args.dry_run))
    return 0


def cmd_shortcut_install(args: argparse.Namespace) -> int:
    repo = Path(__file__).resolve().parents[2]
    print(install_shortcut(repo, args.codex_root.expanduser().resolve(), dry_run=args.dry_run))
    return 0


def cmd_shortcut_uninstall(args: argparse.Namespace) -> int:
    print(uninstall_shortcut(dry_run=args.dry_run))
    return 0


def cmd_recall(args: argparse.Namespace) -> int:
    payload = search(args.codex_root.expanduser().resolve(), args.query, args.max_results)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for item in payload["results"]:
            print(f"{item['kind']}: {item.get('path', '')}")
            print(item["snippet"])
            print()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Codex Self-Improving Loop v3")
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="Show runtime diagnostics")
    add_runtime_args(doctor)
    doctor.add_argument("--json", action="store_true")
    doctor.set_defaults(func=cmd_doctor)

    init = sub.add_parser("init", help="Initialize the SQLite runtime database")
    add_runtime_args(init)
    init.set_defaults(func=cmd_init)

    rebuild_parser = sub.add_parser("rebuild", help="Backup and rebuild SQLite data from session history")
    add_runtime_args(rebuild_parser)
    rebuild_parser.add_argument("--backup", action="store_true")
    rebuild_parser.set_defaults(func=cmd_rebuild)

    scan = sub.add_parser("scan", help="Scan new session history into SQLite")
    add_runtime_args(scan)
    scan.add_argument("--once", action="store_true", help="Run one scan cycle and exit")
    scan.set_defaults(func=cmd_scan)

    serve_parser = sub.add_parser("serve", help="Run the local-only WebUI backend")
    add_runtime_args(serve_parser)
    serve_parser.add_argument("--port", type=int, default=8765)
    serve_parser.add_argument("--open", action="store_true", help="Open the WebUI in the default browser")
    serve_parser.add_argument("--smoke-test", action="store_true", help="Validate serve configuration without starting a server")
    serve_parser.set_defaults(func=cmd_serve)

    schedule = sub.add_parser("schedule", help="Install or remove the daily scan schedule")
    schedule_sub = schedule.add_subparsers(dest="schedule_command", required=True)
    schedule_install = schedule_sub.add_parser("install")
    add_runtime_args(schedule_install)
    schedule_install.add_argument("--dry-run", action="store_true")
    schedule_install.set_defaults(func=cmd_schedule_install)
    schedule_uninstall = schedule_sub.add_parser("uninstall")
    add_runtime_args(schedule_uninstall)
    schedule_uninstall.add_argument("--dry-run", action="store_true")
    schedule_uninstall.set_defaults(func=cmd_schedule_uninstall)

    shortcut = sub.add_parser("shortcut", help="Install or remove the desktop launcher")
    shortcut_sub = shortcut.add_subparsers(dest="shortcut_command", required=True)
    shortcut_install = shortcut_sub.add_parser("install")
    add_runtime_args(shortcut_install)
    shortcut_install.add_argument("--dry-run", action="store_true")
    shortcut_install.set_defaults(func=cmd_shortcut_install)
    shortcut_uninstall = shortcut_sub.add_parser("uninstall")
    add_runtime_args(shortcut_uninstall)
    shortcut_uninstall.add_argument("--dry-run", action="store_true")
    shortcut_uninstall.set_defaults(func=cmd_shortcut_uninstall)

    recall = sub.add_parser("recall", help="Search historical sessions and candidates")
    add_runtime_args(recall)
    recall.add_argument("--query", required=True)
    recall.add_argument("--max-results", type=int, default=10)
    recall.add_argument("--json", action="store_true")
    recall.set_defaults(func=cmd_recall)

    return parser


def add_runtime_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--codex-root", type=Path, default=Path.home() / ".codex")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    ensure_runtime(args.codex_root)
    return int(args.func(args))
