#!/usr/bin/env python3
"""Browser-level smoke test for the redesigned WebUI workflow."""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

from helpers import TestServer, run_sil, write_jsonl_session


NODE = Path(r"C:\Users\Newcats\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe")
PLAYWRIGHT_CORE = Path(
    r"C:\Users\Newcats\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules\.pnpm\playwright-core@1.60.0\node_modules\playwright-core\index.mjs"
)
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")


def skip(reason: str) -> int:
    print(f"verify-webui-browser skipped: {reason}")
    return 0


def prepare_data(repo: Path, root: Path) -> None:
    os.environ["CODEX_SIL_DISABLE_CODEX"] = "1"
    write_jsonl_session(
        root / "sessions" / "2026" / "06" / "09" / "browser.jsonl",
        [
            {"role": "user", "content": "Remember the GitHub Trending workflow must use the official trending page."},
            {"role": "user", "content": "请记住：SQL 查询必须先确认字段，避免 SELECT *。"},
            {"role": "user", "content": "这个流程可以做成 skill：先 doctor，再 rebuild，再 scan --once。"},
        ],
    )
    (root / "memories").mkdir(parents=True, exist_ok=True)
    (root / "memories" / "USER.md").write_text("# USER.md\n", encoding="utf-8")
    (root / "AGENTS.md").write_text("# AGENTS.md\n\n## Project Learned Facts\n", encoding="utf-8")
    run_sil(repo, root, "rebuild", "--backup")

    db = root / "self-improving-loop" / "self-improving-loop.sqlite"
    with sqlite3.connect(db) as conn:
        conn.execute(
            """
            insert into runs(kind, status, finished_at, detail)
            values('scan', 'failed', current_timestamp, 'browser qa synthetic failed run')
            """
        )
        conn.execute(
            """
            insert into audit_log(action, target, detail)
            values('browser_qa_signal', 'workflow', 'browser qa synthetic audit signal')
            """
        )
        conn.commit()


def assert_report(payload: dict[str, object], screenshot: Path) -> None:
    checks = payload.get("checks") or {}
    errors = payload.get("errors") or []
    dark_screenshot = screenshot.with_name(screenshot.stem + ".dark" + screenshot.suffix)
    if errors:
        raise AssertionError(f"browser console/page errors found: {errors}")
    if checks.get("title") != "Codex Self-Improving Loop":
        raise AssertionError(f"unexpected WebUI title: {checks}")
    if int(checks.get("primaryNavCount") or 0) != 10 or checks.get("hasFunctionalNavigation") is not True:
        raise AssertionError(f"left navigation should expose ten functional modules: {checks}")
    if not checks.get("dashboardNextAction"):
        raise AssertionError(f"dashboard next action should render: {checks}")
    if int(checks.get("dashboardButtons") or 0) != 0:
        raise AssertionError(f"dashboard should stay read-only and contain no buttons: {checks}")
    if int(checks.get("dashboardActionButtons") or 0) != 0 or int(checks.get("dashboardNavJumpButtons") or 0) != 0:
        raise AssertionError(f"dashboard should not expose action or same-page jump controls: {checks}")
    if int(checks.get("setupChecklistItems") or 0) < 4:
        raise AssertionError(f"first-run wizard should render status checklist items: {checks}")
    if int(checks.get("operationsViewContainers") or 0) != 1:
        raise AssertionError(f"operations should render as one single view container: {checks}")
    if int(checks.get("candidateCards") or 0) < 1:
        raise AssertionError(f"workflow should render candidate cards: {checks}")
    if "diff" not in str(checks.get("workflowNextActionAfterSelect", "")).lower() and "预览" not in str(checks.get("workflowNextActionAfterSelect", "")):
        raise AssertionError(f"workflow should guide the user to preview after selection: {checks}")
    if not checks.get("previewTextHead"):
        raise AssertionError(f"promotion preview should load a diff before approval: {checks}")
    if int(checks.get("confirmCallsAfterPromoteClick") or 0) != 0:
        raise AssertionError(f"promotion click should not use window.confirm: {checks}")
    if checks.get("confirmModalVisible") is not True:
        raise AssertionError(f"promotion click should open the structured confirmation modal: {checks}")
    if checks.get("confirmPreviewIncluded") is not True:
        raise AssertionError(f"manual confirmation should include the diff preview: {checks}")
    if checks.get("confirmModalHasDanger") is not True:
        raise AssertionError(f"promotion confirmation should use the high-risk button style: {checks}")
    if checks.get("approvalDockVisible") is not True:
        raise AssertionError(f"manual approval dock should stay visible during review: {checks}")
    if int(checks.get("operationsLifecycleCards") or 0) != 4:
        raise AssertionError(f"operations lifecycle should expose four flow cards: {checks}")
    if int(checks.get("operationsVisiblePanels") or 0) != 1:
        raise AssertionError(f"operations navigation should activate one operations view: {checks}")
    module_navigation = checks.get("moduleNavigation") or {}
    for module_name, result in module_navigation.items():
        if result.get("currentNav") != module_name or result.get("activeNav") is not True:
            raise AssertionError(f"module navigation should update stable nav state for {module_name}: {checks}")
        if result.get("hash"):
            raise AssertionError(f"module navigation should not rely on URL hash anchors for {module_name}: {checks}")
        if int(result.get("scrollY") or 0) > 80:
            raise AssertionError(f"module navigation should switch panels instead of scrolling to anchors for {module_name}: {checks}")
        if not result.get("targetVisible"):
            raise AssertionError(f"module navigation should show target for {module_name}: {checks}")
        if int(result.get("visibleSections") or 0) < 1:
            raise AssertionError(f"module navigation should leave visible content for {module_name}: {checks}")
    if checks.get("workflowModuleState") != "queue" or checks.get("evidenceModuleState") != "evidence" or checks.get("approvalModuleState") != "approval":
        raise AssertionError(f"workflow left navigation should switch real modules: {checks}")
    if checks.get("darkThemeNoWhiteControls") is not True:
        raise AssertionError(f"dark theme should cover sampled interactive panels and controls: {checks}")
    if checks.get("noHorizontalOverflowDesktop") is not True:
        raise AssertionError(f"desktop viewport should not horizontally overflow: {checks}")
    if checks.get("dashboardCompactPanelsFit") is not True:
        raise AssertionError(f"dashboard short-information panels should not stretch into full-width strips: {checks}")
    workflow_action_strip = checks.get("workflowActionStripLayout") or {}
    if workflow_action_strip.get("compact") is not True:
        raise AssertionError(f"workflow status strip should not stretch sparse guidance across the full desktop width: {checks}")
    approval_layout = checks.get("approvalDesktopLayout") or {}
    if approval_layout.get("compact") is not True:
        raise AssertionError(f"approval module should not reserve a large empty leading column on desktop: {checks}")
    if checks.get("darkNavTextReadable") is not True:
        raise AssertionError(f"dark theme side navigation should keep readable contrast: {checks}")
    if not screenshot.exists() or screenshot.stat().st_size < 10_000:
        raise AssertionError(f"browser screenshot should be generated: {screenshot}")
    if not dark_screenshot.exists() or dark_screenshot.stat().st_size < 10_000:
        raise AssertionError(f"dark theme browser screenshot should be generated: {dark_screenshot}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--work-root", type=Path, required=True)
    parser.add_argument("--require-browser", action="store_true", help="Fail instead of skipping when local browser dependencies are unavailable.")
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    root = args.work_root.resolve()

    missing = [str(path) for path in (NODE, PLAYWRIGHT_CORE, EDGE) if not path.exists()]
    if missing:
        if args.require_browser:
            raise FileNotFoundError("Missing browser QA dependency: " + ", ".join(missing))
        return skip("missing " + ", ".join(missing))

    prepare_data(repo, root)
    screenshot = root / "self-improving-loop" / "webui-browser-qa.png"
    with TestServer(repo, root) as server:
        url = f"http://127.0.0.1:{server.port}/?token={server.token}"
        completed = subprocess.run(
            [str(NODE), str(repo / "tests" / "webui-browser-qa.mjs"), url, str(screenshot), str(EDGE)],
            cwd=repo,
            check=False,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
        )
    if completed.returncode != 0:
        if args.require_browser:
            raise AssertionError(completed.stderr or completed.stdout)
        return skip((completed.stderr or completed.stdout or "browser command failed").splitlines()[0])
    payload = json.loads(completed.stdout)
    assert_report(payload, screenshot)
    print("verify-webui-browser passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
