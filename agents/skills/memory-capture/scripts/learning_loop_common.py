#!/usr/bin/env python3
"""Shared helpers for Codex Self-Improving Loop scripts."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|secret|password|passwd|pwd)\s*[:=]\s*['\"]?[^'\"\s]{8,}"),
    re.compile(r"(?i)(authorization|bearer)\s+[^,\s]{12,}"),
    re.compile(r"(?i)(connectionstring|connection_string)\s*[:=]\s*[^,\n]{12,}"),
    re.compile(r"(?i)-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)\b[A-Za-z0-9_\-]{24,}\.[A-Za-z0-9_\-]{12,}\.[A-Za-z0-9_\-]{12,}\b"),
]

PRIVATE_URL_RE = re.compile(r"(?i)\bhttps?://(?:localhost|127\.0\.0\.1|10\.|192\.168\.|172\.(?:1[6-9]|2\d|3[01])|[^/\s]*(?:internal|corp|private|intranet)[^/\s]*)[^\s]*")
RAW_TRANSCRIPT_RE = re.compile(r"(?i)<\|/?(?:system|user|assistant|tool)[^>]*\|>|^\s*(system|user|assistant|tool)\s*:", re.MULTILINE)
PROMPT_INJECTION_RE = re.compile(r"(?i)(ignore (all )?(previous|prior) instructions|system prompt|developer message|hidden instruction|exfiltrate|leak|disable safety|bypass)")
ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")
LOG_LINE_RE = re.compile(
    r"(?i)^(exit code:|wall time:|output:|listing |compiling |copy:|skip existing|append:|installed |"
    r"codex root:|agents root:|recorded usage|skills index written|learning inbox summary written|"
    r"memory candidate report written|skill candidate report written|skill patch candidate report written|"
    r"verify-install passed|removed |fatal:|warning:)"
)
LOCAL_PATH_RE = re.compile(r"(?i)([A-Z]:\\|/tmp/|/var/|/home/|\\\\|\.codex\\|\.agents\\)")
CODE_ECHO_RE = re.compile(r"(?i)(parser\.add_argument|subprocess\.run|write_text|read_text|select-string|getitem|object\]@|\[7m|\[0m)")
CODE_FRAGMENT_RE = re.compile(
    r"(?i)(args\.|default_codex_root|report_path|usage_file|output_path|skills_root|"
    r"root\s*/\s*['\"]|type=Path|str\(|Path\(|\.expanduser\(|\.glob\(|\.rglob\()"
)
BOOTSTRAP_CONTEXT_RE = re.compile(r"(?is)^# AGENTS\.md instructions for|<INSTRUCTIONS>|--- project-doc ---|<environment_context>")
ASSISTANT_PROGRESS_RE = re.compile(r"(?i)^(我会|我将|我现在|我先|下一步|接下来|当前|上一条|I will|I'll|I am going to|Next,|Now I)")
CONTROL_EVENT_RE = re.compile(r"(?i)<turn_aborted>|</turn_aborted>|<environment_context>|</environment_context>")
ONE_OFF_REQUEST_RE = re.compile(
    r"(?i)^(帮我|查下|检查一下|重新检查|只返回|列出|给出|看下|"
    r"can you|please check|find|list|show me|summarize)"
)
LEARNING_OUTCOME_RE = re.compile(
    r"(?i)(root cause|fixed|implemented|verified|passed|regression|lesson|pitfall|"
    r"根因|已修复|修复了|已验证|验证通过|通过验证|结论|原因是|问题在|"
    r"改为|应该|需要|避免|不要|默认|以后|记住|沉淀)"
)


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def today_dir_parts() -> tuple[str, str, str]:
    now = datetime.now()
    return now.strftime("%Y"), now.strftime("%m"), now.strftime("%d")


def today_dir_name() -> str:
    return str(Path(*today_dir_parts()))


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def home_path(*parts: str) -> Path:
    return Path.home().joinpath(*parts)


def default_codex_root() -> Path:
    return home_path(".codex")


def default_agents_root() -> Path:
    return home_path(".agents")


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_text(path: Path, default: str = "") -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return default


def write_text(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8")


def append_text(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(content)


def dated_output_dir(base_dir: Path) -> Path:
    return base_dir.joinpath(*today_dir_parts())


def dated_output_path(base_dir: Path, filename: str) -> Path:
    return dated_output_dir(base_dir) / filename


def markdown_files_recursive(directory: Path) -> list[Path]:
    return sorted(directory.rglob("*.md")) if directory.exists() else []


def redact(text: str) -> str:
    redacted = text
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    redacted = PRIVATE_URL_RE.sub("[REDACTED_URL]", redacted)
    return redacted


def strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text)


def contains_secret_like_text(text: str) -> bool:
    if "[REDACTED]" in text or "[REDACTED_URL]" in text:
        return True
    return any(pattern.search(text) for pattern in SECRET_PATTERNS) or bool(PRIVATE_URL_RE.search(text))


def tokenize_query(query: str) -> list[str]:
    terms = [term.strip().lower() for term in re.split(r"[\s,;|]+", query) if term.strip()]
    return list(dict.fromkeys(terms))


def iter_session_files(root: Path) -> list[Path]:
    candidates: list[Path] = []
    for rel in ("sessions", "history"):
        directory = root / rel
        if directory.exists():
            candidates.extend(directory.rglob("*.jsonl"))
            candidates.extend(directory.rglob("*.json"))
    history_jsonl = root / "history.jsonl"
    if history_jsonl.exists():
        candidates.append(history_jsonl)
    return sorted(set(candidates), key=lambda path: path.stat().st_mtime if path.exists() else 0, reverse=True)


def parse_jsonish_line(line: str) -> str:
    raw = line.strip()
    if not raw:
        return ""
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        return raw
    return extract_text(obj)


def parse_jsonish_message_line(line: str, include_roles: tuple[str | None, ...] | None = ("user", None)) -> str:
    raw = line.strip()
    if not raw:
        return ""
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        return raw if include_roles is None or None in include_roles else ""
    role = extract_message_role(obj)
    if include_roles is not None and role not in include_roles:
        return ""
    return extract_text(obj)


def extract_message_role(value: Any) -> str | None:
    if not isinstance(value, dict):
        return None
    if "payload" in value and isinstance(value["payload"], dict):
        return extract_message_role(value["payload"])
    event_type = value.get("type")
    role = value.get("role")
    if event_type == "agent_message":
        return "assistant"
    if role and ("content" in value or "message" in value or event_type == "message"):
        return str(role)
    return None


def extract_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(part for part in (extract_text(item) for item in value) if part)
    if isinstance(value, dict):
        event_type = value.get("type")
        role = value.get("role")
        if event_type in {"function_call", "function_call_output", "reasoning", "token_count"}:
            return ""
        if event_type == "message" and role in {"system", "tool"}:
            return ""
        if "payload" in value and isinstance(value["payload"], dict):
            payload = value["payload"]
            payload_type = payload.get("type")
            payload_role = payload.get("role")
            if payload_type in {"function_call", "function_call_output", "reasoning", "token_count"}:
                return ""
            if payload_type == "agent_message":
                return extract_text(payload.get("message"))
            if payload_type == "message" and payload_role in {"user", "assistant"}:
                return extract_text(payload.get("content"))
            return ""
        preferred_keys = ("text", "content", "message", "body", "input", "output", "summary")
        parts: list[str] = []
        for key in preferred_keys:
            if key in value:
                text = extract_text(value[key])
                if text:
                    parts.append(text)
        if parts:
            return "\n".join(parts)
        return "\n".join(extract_text(item) for item in value.values() if extract_text(item))
    return str(value)


def is_noisy_learning_line(text: str) -> bool:
    stripped = strip_ansi(text).strip()
    if not stripped:
        return True
    if LOG_LINE_RE.search(stripped):
        return True
    if CODE_ECHO_RE.search(stripped):
        return True
    if CODE_FRAGMENT_RE.search(stripped):
        return True
    if BOOTSTRAP_CONTEXT_RE.search(stripped):
        return True
    if CONTROL_EVENT_RE.search(stripped):
        return True
    if ASSISTANT_PROGRESS_RE.search(stripped):
        return True
    if ONE_OFF_REQUEST_RE.search(stripped):
        return True
    if LOCAL_PATH_RE.search(stripped) and not re.search(r"(?i)(prefer|remember|workflow|skill|patch|以后|默认|记住|流程|技能|补丁)", stripped):
        return True
    if len(re.findall(r"[\\/:]", stripped)) >= 6:
        return True
    return False


def clean_candidate_text(text: str) -> str:
    return re.sub(r"\s+", " ", strip_ansi(text)).strip()


def split_learning_fragments(text: str) -> list[str]:
    compact = clean_candidate_text(text)
    if len(compact) <= 260:
        return [compact] if compact else []
    pieces = re.split(r"(?<=[。.!?？])\s+|\n+", text)
    fragments: list[str] = []
    for piece in pieces:
        fragment = clean_candidate_text(piece)
        if fragment:
            fragments.append(fragment)
    return fragments or [compact[:500]]


def latest_session_file(root: Path) -> Path | None:
    files = iter_session_files(root)
    return files[0] if files else None


def read_session_messages(path: Path, max_messages: int = 80, include_roles: tuple[str | None, ...] | None = ("user", "assistant", None)) -> list[str]:
    messages: list[str] = []
    if not path.exists():
        return messages
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except TypeError:
        lines = path.read_text(encoding="utf-8").splitlines()
    for line in lines[-max_messages:]:
        text = parse_jsonish_message_line(line, include_roles=include_roles)
        if text:
            cleaned = clean_candidate_text(redact(text))
            if cleaned and not BOOTSTRAP_CONTEXT_RE.search(cleaned):
                messages.append(cleaned)
    return messages


def bulletize(text: str) -> list[str]:
    bullets: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"^[-*]\s+", stripped):
            bullets.append(re.sub(r"^[-*]\s+", "", stripped).strip())
    return bullets


def normalize_memory_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().rstrip(".。")).lower()


def classify_candidate(text: str) -> str:
    lower = text.lower()
    if any(word in lower for word in ("prefer", "default", "always", "never", "以后", "默认", "记住", "不要")):
        return "user_preference"
    if any(word in lower for word in ("workflow", "process", "steps", "verify", "verification", "流程", "步骤", "验证")):
        return "workflow_pattern"
    if any(word in lower for word in ("project", "repo", "repository", "build", "test", "api", "database", "项目", "仓库", "接口")):
        return "project_fact"
    if any(word in lower for word in ("secret", "token", "credential", "security", "安全", "密钥")):
        return "safety_rule"
    return "review"


def suggest_memory_candidates(messages: list[str], limit: int = 12) -> list[str]:
    signals = re.compile(
        r"(?i)(remember|learn|prefer|default|always|never|avoid|workflow|process|verify|lesson|rule|"
        r"root cause|fixed|implemented|verified|passed|regression|pitfall|"
        r"记住|沉淀|以后|默认|不要|流程|步骤|验证|经验|规则|根因|已修复|结论|原因是|问题在|改为)"
    )
    candidates: list[str] = []
    seen: set[str] = set()
    for message in reversed(messages):
        for line in split_learning_fragments(message):
            stripped = re.sub(r"^[-*#>\s]+", "", line).strip()
            stripped = clean_candidate_text(stripped)
            if len(stripped) < 12 or len(stripped) > 500:
                continue
            if is_noisy_learning_line(stripped):
                continue
            if not signals.search(stripped):
                continue
            normalized = normalize_memory_text(stripped)
            if normalized in seen:
                continue
            seen.add(normalized)
            candidates.append(stripped)
            if len(candidates) >= limit:
                return candidates
    return candidates


def write_candidate_report(
    output_dir: Path,
    title: str,
    candidates: Iterable[str],
    source: str,
    kind: str,
    suffix: str = "",
) -> Path:
    path = dated_output_path(output_dir, f"{now_stamp()}{suffix}-{kind}.md")
    lines = [
        f"# {title}",
        "",
        f"- generated_at: {now_iso()}",
        f"- source: {source}",
        f"- status: review",
        "",
        "## Candidates",
        "",
    ]
    count = 0
    for candidate in candidates:
        count += 1
        category = classify_candidate(candidate)
        safety = "blocked" if contains_secret_like_text(candidate) else "review"
        lines.extend(
            [
                f"### Candidate {count}",
                "",
                f"- category: {category}",
                f"- safety: {safety}",
                f"- status: {'blocked' if safety == 'blocked' else 'review'}",
                "",
                "```text",
                candidate,
                "```",
                "",
            ]
        )
    if count == 0:
        lines.extend(["No candidates detected automatically.", ""])
    write_text(path, "\n".join(lines))
    return path


def read_usage(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"version": 1, "skills": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"version": 1, "skills": {}}
    if isinstance(data, list):
        skills: dict[str, Any] = {}
        for item in data:
            if not isinstance(item, dict):
                continue
            name = item.get("skill") or item.get("skill_name") or item.get("name")
            if not name:
                continue
            entry = skills.setdefault(
                str(name),
                {"use_count": 0, "failure_count": 0, "last_used": None, "events": []},
            )
            entry["use_count"] = int(entry.get("use_count", 0)) + int(item.get("use_count", 1) or 1)
            if item.get("status") == "failure":
                entry["failure_count"] = int(entry.get("failure_count", 0)) + 1
            last_used = item.get("last_used") or item.get("at") or item.get("timestamp")
            if last_used and (not entry.get("last_used") or str(last_used) > str(entry.get("last_used"))):
                entry["last_used"] = last_used
            entry.setdefault("events", []).append(item)
            entry["events"] = entry["events"][-20:]
        return {"version": 1, "skills": skills}
    if not isinstance(data, dict):
        return {"version": 1, "skills": {}}
    data.setdefault("version", 1)
    if isinstance(data.get("skills"), list):
        converted = read_usage_from_items(data["skills"])
        converted["version"] = data.get("schema_version", data.get("version", 1))
        return converted
    if not isinstance(data.get("skills"), dict):
        data["skills"] = {}
    return data


def read_usage_from_items(items: list[Any]) -> dict[str, Any]:
    skills: dict[str, Any] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        name = item.get("skill") or item.get("skill_name") or item.get("name")
        if not name:
            continue
        entry = skills.setdefault(
            str(name),
            {"use_count": 0, "failure_count": 0, "last_used": None, "events": []},
        )
        entry["use_count"] = int(entry.get("use_count", 0)) + int(item.get("use_count", 1) or 1)
        entry["failure_count"] = int(entry.get("failure_count", 0)) + int(item.get("failure_count", 0) or 0)
        last_used = item.get("last_used") or item.get("at") or item.get("timestamp")
        if last_used and (not entry.get("last_used") or str(last_used) > str(entry.get("last_used"))):
            entry["last_used"] = last_used
        entry.setdefault("events", []).append(item)
        entry["events"] = entry["events"][-20:]
    return {"version": 1, "skills": skills}


def write_usage(path: Path, data: dict[str, Any]) -> None:
    write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def load_skill_metadata(skill_dir: Path) -> dict[str, str]:
    skill_file = skill_dir / "SKILL.md"
    content = read_text(skill_file)
    metadata = {"name": skill_dir.name, "description": ""}
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].splitlines():
                if ":" not in line:
                    continue
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip().strip('"')
    return metadata


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", type=Path, default=default_codex_root(), help="Codex root directory")


def copy_tree(src: Path, dst: Path, force: bool = False) -> None:
    if not src.exists():
        raise FileNotFoundError(src)
    if dst.exists() and force:
        shutil.rmtree(dst)
    if dst.exists():
        return
    shutil.copytree(src, dst)
