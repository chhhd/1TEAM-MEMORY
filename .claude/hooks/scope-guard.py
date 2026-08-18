#!/usr/bin/env python3
"""
PreToolUse hook (Bash matcher).

Bash 명령이 실행되기 전에 target-info.md의 "인가된 대상" 표에 없는
호스트/IP로 향하는 것으로 보이는 명령을 차단한다.

동작:
- stdin으로 hook 입력(JSON: {"tool_input": {"command": "..."}, ...})을 받는다
- target-info.md에서 인가된 대상 목록을 파싱한다
- 명령어에서 IP/도메인처럼 보이는 토큰을 뽑아 목록과 대조한다
- 목록에 없는 대상이 나오고, 위험 명령(nmap/curl/nc/hydra 등)이면 차단(exit code 2)
- 목록이 비어 있거나(target-info.md 미작성) 판단이 애매하면 차단하지 않고 경고만 출력
  (오탐으로 팀 작업을 막지 않기 위함 — 최종 책임은 사람의 리뷰에 있다)
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TARGET_INFO = REPO_ROOT / "target-info.md"

RISKY_COMMANDS = re.compile(
    r"\b(nmap|curl|wget|nc|ncat|netcat|hydra|sqlmap|nikto|gobuster|ffuf|masscan)\b",
    re.IGNORECASE,
)
HOST_TOKEN = re.compile(
    r"\b(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|[a-zA-Z0-9][a-zA-Z0-9-]*\.[a-zA-Z]{2,})\b"
)


def load_authorized_hosts() -> set[str]:
    if not TARGET_INFO.exists():
        return set()
    text = TARGET_INFO.read_text(encoding="utf-8", errors="ignore")
    hosts = set()
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        for cell in cells:
            for m in HOST_TOKEN.findall(cell):
                hosts.add(m.lower())
    return hosts


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # 입력을 파싱 못하면 막지 않는다

    command = (
        payload.get("tool_input", {}).get("command", "")
        if isinstance(payload.get("tool_input"), dict)
        else ""
    )
    if not command or not RISKY_COMMANDS.search(command):
        return 0

    authorized = load_authorized_hosts()
    if not authorized:
        print(
            "[scope-guard] target-info.md에 인가된 대상이 아직 없습니다. "
            "스코프를 확인하세요.",
            file=sys.stderr,
        )
        return 0

    found_hosts = {h.lower() for h in HOST_TOKEN.findall(command)}
    unauthorized = found_hosts - authorized
    if unauthorized:
        print(
            f"[scope-guard] 스코프 밖으로 보이는 대상 발견: {sorted(unauthorized)}. "
            f"target-info.md의 인가된 대상 목록을 확인하세요. 명령: {command}",
            file=sys.stderr,
        )
        return 2  # PreToolUse에서 2를 반환하면 도구 실행을 차단

    return 0


if __name__ == "__main__":
    sys.exit(main())
