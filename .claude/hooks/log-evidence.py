#!/usr/bin/env python3
"""
PostToolUse hook (Bash matcher).

정찰/진단성 Bash 명령이 실행된 뒤, 사람이 나중에 대조할 수 있도록
evidence/raw/ 에 원본 명령+출력을 타임스탬프 파일로 남긴다.
(이 로그는 "감사 추적"용이며, evidence.csv/evidence.md에 올리는 정제된 기록을 대신하지 않는다 —
 각 에이전트가 여전히 SKILL.md 절차에 따라 csv/md에 직접 기록해야 한다.)
"""

import datetime as dt
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = REPO_ROOT / "evidence" / "raw"

LOGGED_COMMANDS = re.compile(
    r"\b(nmap|curl|wget|dig|nslookup|whois|sqlmap|nikto|gobuster|ffuf)\b",
    re.IGNORECASE,
)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    tool_input = payload.get("tool_input", {})
    command = tool_input.get("command", "") if isinstance(tool_input, dict) else ""
    if not command or not LOGGED_COMMANDS.search(command):
        return 0

    output = payload.get("tool_response", {})
    stdout = output.get("stdout", "") if isinstance(output, dict) else str(output)
    stderr = output.get("stderr", "") if isinstance(output, dict) else ""

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_file = RAW_DIR / f"cmdlog-{ts}.md"
    log_file.write_text(
        f"# Command log ({ts})\n\n"
        f"## Command\n```\n{command}\n```\n\n"
        f"## Stdout\n```\n{stdout}\n```\n\n"
        f"## Stderr\n```\n{stderr}\n```\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
