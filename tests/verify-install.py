#!/usr/bin/env python3
"""Run the v2 installation and core verification suite."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(command: list[str], cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--codex-root", type=Path, required=True)
    parser.add_argument("--agents-root", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    codex = args.codex_root.resolve()
    agents = args.agents_root.resolve()

    run([sys.executable, str(repo / "tests" / "verify-v2-core.py"), "--repo-root", str(repo), "--work-root", str(codex / "core")], repo)
    run([sys.executable, str(repo / "tests" / "verify-codex-runner.py"), "--repo-root", str(repo), "--work-root", str(codex / "runner")], repo)
    run([sys.executable, str(repo / "tests" / "verify-v2-recall.py"), "--repo-root", str(repo), "--work-root", str(codex / "recall")], repo)
    run([sys.executable, str(repo / "tests" / "verify-v2-session-filter.py"), "--repo-root", str(repo), "--work-root", str(codex / "filter")], repo)
    run([sys.executable, str(repo / "tests" / "verify-v2-promotion.py"), "--repo-root", str(repo), "--work-root", str(codex / "promotion")], repo)
    run([sys.executable, str(repo / "tests" / "verify-v2-scheduler.py"), "--repo-root", str(repo), "--work-root", str(codex / "scheduler")], repo)
    run([sys.executable, str(repo / "tests" / "verify-webui-browser.py"), "--repo-root", str(repo), "--work-root", str(codex / "webui-browser")], repo)
    run(
        [
            sys.executable,
            str(repo / "tests" / "verify-v2-install.py"),
            "--repo-root",
            str(repo),
            "--codex-root",
            str(codex / "install-codex"),
            "--agents-root",
            str(agents / "install-agents"),
        ],
        repo,
    )
    print("verify-install passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
