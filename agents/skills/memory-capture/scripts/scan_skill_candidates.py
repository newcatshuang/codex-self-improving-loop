#!/usr/bin/env python3
"""Scan skill candidates and patch candidates for safety risks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from learning_loop_common import (
    PRIVATE_URL_RE,
    PROMPT_INJECTION_RE,
    RAW_TRANSCRIPT_RE,
    SECRET_PATTERNS,
    default_codex_root,
    read_text,
    write_text,
)


def scan_text(text: str) -> list[str]:
    findings: list[str] = []
    if "[REDACTED]" in text:
        findings.append("contains_redacted_value")
    if PRIVATE_URL_RE.search(text):
        findings.append("contains_private_url")
    if PROMPT_INJECTION_RE.search(text):
        findings.append("prompt_injection_like_text")
    if RAW_TRANSCRIPT_RE.search(text):
        findings.append("raw_transcript_marker")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            findings.append("secret_like_text")
            break
    return sorted(set(findings))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_codex_root())
    parser.add_argument("--skill-candidate-dir", type=Path)
    parser.add_argument("--skill-patch-dir", type=Path)
    parser.add_argument("--report-path", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = args.root.expanduser()
    dirs = [
        args.skill_candidate_dir.expanduser() if args.skill_candidate_dir else root / "skill-candidates" / "inbox",
        args.skill_patch_dir.expanduser() if args.skill_patch_dir else root / "skill-candidates" / "patches",
    ]
    results = []
    for directory in dirs:
        for path in sorted(directory.glob("*.md")) if directory.exists() else []:
            findings = scan_text(read_text(path))
            status = "blocked" if any(item in findings for item in ("secret_like_text", "contains_redacted_value")) else ("review" if findings else "ok")
            results.append({"file": str(path), "status": status, "findings": findings})
    summary = {
        "scanned": len(results),
        "blocked": sum(1 for item in results if item["status"] == "blocked"),
        "review": sum(1 for item in results if item["status"] == "review"),
        "ok": sum(1 for item in results if item["status"] == "ok"),
        "results": results,
    }
    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        lines = [
            "# Skill Candidate Security Scan",
            "",
            f"- scanned: {summary['scanned']}",
            f"- blocked: {summary['blocked']}",
            f"- review: {summary['review']}",
            f"- ok: {summary['ok']}",
            "",
        ]
        for item in results:
            lines.append(f"- [{item['status']}] {item['file']} :: {', '.join(item['findings']) or 'no findings'}")
        report = "\n".join(lines) + "\n"
        if args.report_path:
            write_text(args.report_path.expanduser(), report)
            print(f"Skill candidate scan report written: {args.report_path}")
        else:
            print(report)
    return 0 if summary["blocked"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
