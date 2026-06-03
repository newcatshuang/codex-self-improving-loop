#!/usr/bin/env python3
"""Render a local single-file dashboard for Codex learning review artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_learning_index import build_payload, read_index
from learning_loop_common import default_codex_root, write_text


def load_template() -> str:
    template_path = SCRIPT_DIR.parent / "templates" / "dashboard.html"
    if not template_path.exists():
        raise FileNotFoundError(template_path)
    return template_path.read_text(encoding="utf-8")


def render_html(payload: dict[str, Any]) -> str:
    payload_json = json.dumps(payload, ensure_ascii=False, indent=2)
    payload_json = payload_json.replace("</", "<\\/")
    return load_template().replace("__DASHBOARD_DATA_JSON__", payload_json)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_codex_root())
    parser.add_argument("--index-path", type=Path, help="Use an existing learning-index.json payload")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", help="Print dashboard payload instead of writing HTML")
    args = parser.parse_args()

    root = args.root.expanduser()
    index_path = args.index_path.expanduser() if args.index_path else None
    payload = read_index(index_path) if index_path else build_payload(root, root / "learning-index.json")
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    output = args.output.expanduser() if args.output else root / "codex-self-improving-loop-dashboard.html"
    write_text(output, render_html(payload))
    print(f"Dashboard written: {output}")
    print(
        "Dashboard summary: "
        f"total={payload['summary']['total_candidates']}, "
        f"today={payload['summary']['today_candidates']}, "
        f"dates={len(payload['dates'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
