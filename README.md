# CTF Agent Harness

Claude Code 기반 CTF 팀 자동화 하네스. 정찰(Recon) → 취약점 진단(Injection / Access Control / CVE) →
증거 수집(Evidence)까지 서브에이전트/스킬/훅으로 파이프라인화한다.

> ⚠️ 본 레포의 모든 에이전트는 **대회/훈련 규정에서 허용된 대상**에 한해서만 사용한다.
> `target-info.md`에 명시되지 않은 호스트·범위는 스캔/공격하지 않는다.

## 팀 규칙

- 브랜치: `main` 직접 push 금지, 기능 브랜치 → PR 후 머지
- 커밋 메시지: `[영역] 요약` (예: `[recon] nmap 결과 파싱 스크립트 추가`)
- 산출물(에이전트/스킬 정의)은 **역할별 디렉터리**에서만 작업 (아래 표 참고)
- 모든 에이전트는 작업 결과를 `evidence/evidence.csv`, `evidence/evidence.md`에 기록한다
  (형식은 [evidence/evidence.md](evidence/evidence.md) 상단 규칙 참고)
- 실제 플래그/크리덴셜/개인정보는 레포에 커밋하지 않는다 (evidence 파일은 메타데이터·근거 위주로 기록)

## 디렉터리 구조

```
ctf-agent-harness/
├── README.md              # 팀 규칙, 링크(Notion 상태판 등) 정리
├── CLAUDE.md
├── .claude/
│   ├── agents/*.md
│   ├── skills/*/SKILL.md
│   ├── hooks/
│   └── settings.json
├── evidence/
│   ├── evidence.csv
│   └── evidence.md
└── target-info.md
```

## 팀 구성 및 산출물

| 팀원 | 산출물 | 확장자 | 경로 |
| --- | --- | --- | --- |
| 이동건 | 프로젝트 규칙, 권한 설정 | `CLAUDE.md`, `settings.json` | 레포 루트, `.claude/` |
| 이나윤 | Recon Agent 정의 + 절차 | `.md` | `.claude/agents/recon-agent.md`, `.claude/skills/recon/SKILL.md` |
| 임희영 | Injection Agent 정의 + 진단 절차 | `.md` | `.claude/agents/injection-agent.md`, `.claude/skills/injection/SKILL.md` |
| 박나현 | IDOR/Auth Agent 정의 + 체크리스트 | `.md` | `.claude/agents/access-control-agent.md`, `.claude/skills/access-control/SKILL.md` |
| 박정근 | CVE Agent, Hooks 스크립트 | `.md` + `.py`/`.sh`/`.js`(Hook용) | `.claude/agents/cve-agent.md`, `.claude/hooks/` |

## 링크

- Notion 상태판: https://app.notion.com/p/3ba73ca863d880b9b13ddb4d07c91b9c
- 대회/훈련 규정(Rules of Engagement): [target-info.md](target-info.md)

## 작업 흐름

1. `target-info.md`에서 이번 세션 대상/범위 확인
2. `recon-agent`로 대상 표면 파악 → `evidence/`에 기록
3. recon 결과 기반으로 `injection-agent` / `access-control-agent` / `cve-agent` 병렬 투입
4. 각 에이전트는 발견 사항을 evidence 규칙에 맞춰 기록, 확정된 것만 팀에 공유
5. 대회 종료 후 `evidence/evidence.md`를 리포트 초안으로 정리
