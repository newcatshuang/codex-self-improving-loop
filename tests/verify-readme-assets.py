#!/usr/bin/env python3
"""Verify README screenshot assets are present and sanitized."""

from __future__ import annotations

import argparse
from pathlib import Path


def assert_contains(text: str, expected: str, message: str) -> None:
    if expected not in text:
        raise AssertionError(message)


def assert_not_contains_bytes(data: bytes, forbidden: bytes, message: str) -> None:
    if forbidden.lower() in data.lower():
        raise AssertionError(message)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    asset_rel = "docs/assets/webui-dashboard.png"
    asset = repo / asset_rel
    readme = (repo / "README.md").read_text(encoding="utf-8")
    readme_zh = (repo / "README.zh-CN.md").read_text(encoding="utf-8")

    assert_contains(readme, asset_rel, "English README should reference the WebUI screenshot")
    assert_contains(readme_zh, asset_rel, "Chinese README should reference the WebUI screenshot")
    assert_contains(readme, "WebUI Dashboard", "English README should include WebUI usage docs")
    assert_contains(readme_zh, "WebUI Dashboard", "Chinese README should include WebUI usage docs")
    if not asset.exists():
        raise FileNotFoundError(asset)
    data = asset.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise AssertionError("WebUI screenshot should be a PNG file")
    combined_docs = (readme + "\n" + readme_zh).encode("utf-8", errors="ignore")
    for forbidden in (b"C:\\Users", b"/Users/", b"readme-demo-root"):
        assert_not_contains_bytes(combined_docs, forbidden, f"README should not expose local path token {forbidden!r}")
        assert_not_contains_bytes(data, forbidden, f"screenshot should not expose local path token {forbidden!r}")

    print("verify-readme-assets passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
