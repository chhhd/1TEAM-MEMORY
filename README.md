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
| 팀원3 | Injection Agent 정의 + 진단 절차 | `.md` | `.claude/agents/injection-agent.md`, `.claude/skills/injection/SKILL.md` |
| 팀원4 | IDOR/Auth Agent 정의 + 체크리스트 | `.md` | `.claude/agents/access-control-agent.md`, `.claude/skills/access-control/SKILL.md` |
| 팀원5 | CVE Agent, Hooks 스크립트 | `.md` + `.py`/`.sh`/`.js`(Hook용) | `.claude/agents/cve-agent.md`, `.claude/hooks/` |

## 링크

- Notion 상태판: https://app.notion.com/p/3ba73ca863d880b9b13ddb4d07c91b9c
- 대회/훈련 규정(Rules of Engagement): [target-info.md](target-info.md)

## 팀 진행 흐름 (Phase 0~4)

실제 게임 진행은 5개 전문 레포(아래 §관련 저장소)에서 각자 agent를 돌리고,
그 결과를 이 레포로 모으는 방식이다.

- **Phase 0 (시작 전)**: 팀원1(이동건)이 전원 레포 pull 완료 / 계정 분리
  (팀원별로 다른 테스트 계정) / `target-info.md`의 대상 정보 공유를 확인한다.
  이후 팀원1은 **Team Lead 겸 오케스트레이터 운영자** 역할을 맡는다.
- **Phase 1 (Recon, 단독 실행)**: 팀원2(이나윤)만 `1TEAM-Recon-Subagent`로
  Recon을 수행한다. 동시에 여러 명이 하면 중복이라 의미가 없다. 결과는
  즉시 `evidence/`(자기 레포 + 이 레포 둘 다, 아래 §evidence 참고)에 기록하고
  전원에게 공유한다.
- **Phase 2 (병렬 탐색)**: Recon 결과를 보고 각자 전문 레포로 흩어진다 —
  팀원3은 `1TEAM-Injection-Subagent`, 팀원4은
  `1TEAM-IDOR-Authorization-Web-Logic-Subagent`. 팀원5은 두 사람의 evidence를
  10분 주기로 보면서 `1TEAM-CVE-Analysis-Evaluation-System`으로 보조 검증한다.
  이동건은 이 구간엔 직접 agent를 돌리기보다 상태판 모니터링/중복 방지/
  20분 이상 막힌 사람 지원에 집중한다. 이나윤은 Recon 종료 후 새로 발견된
  엔드포인트에 대한 후속 recon이나 막힌 사람 지원으로 투입된다.
- **Phase 3 (체이닝)**: evidence가 2~3개 쌓일 때마다 팀원1이
  `scripts/confirmed_summary.py`로 confirmed 행만 모아 오케스트레이터 세션에
  판단시킨다("이 발견들을 조합하면 권한상승이 가능한가"). 유망한 조합이 나오면
  담당자에게 재할당해 Phase 2 방식으로 검증 — 실제 권한상승 체인이 확인될
  때까지 Phase 2 ↔ 3을 반복한다.
- **Phase 4 (완료)**: 체인이 확인되면 즉시 전원에게 브로드캐스트하고 재현
  절차를 기록한다. **브로드캐스트 채널은 아직 전용 채널이 없어 Notion 상태판
  코멘트로 대체한다**(위 §링크의 Notion 상태판) — 전용 채널이 정해지면 이
  항목을 갱신한다. 이후 팀원5이 전체 evidence 로그를 정리해서 "어떤 Agent가
  몇 번 만에 뭘 찾았는지" 실험 결과 요약본을 만든다(Baseline vs Harness 비교
  데이터로 사용).

## Evidence는 어디에 쌓이는가

각자 자기 전문 레포에서 agent를 돌리고 그 레포의 `evidence/evidence.csv`에
먼저 기록하되, **이 레포(`1TEAM-MEMORY`)에도 같은 행을 동기화**한다 —
팀원1이 Phase 3에서 참조하는 곳은 이 레포다. 구체적인 절차는
[evidence/evidence.md](evidence/evidence.md) 참고.

## 관련 저장소

| 레포 | 담당 |
| --- | --- |
| [`1TEAM-Main-Orchestration-Project-Infrastructure`](https://github.com/chhhd/1TEAM-Main-Orchestration-Project-Infrastructure) | 팀원1 이동건 — 오케스트레이션/인프라 |
| [`1TEAM-Recon-Subagent`](https://github.com/chhhd/1TEAM-Recon-Subagent) | 팀원2 이나윤 — Recon |
| [`1TEAM-Injection-Subagent`](https://github.com/chhhd/1TEAM-Injection-Subagent) | 팀원3 팀원3 — Injection |
| [`1TEAM-IDOR-Authorization-Web-Logic-Subagent`](https://github.com/chhhd/1TEAM-IDOR-Authorization-Web-Logic-Subagent) | 팀원4 팀원4 — IDOR/Auth |
| [`1TEAM-CVE-Analysis-Evaluation-System`](https://github.com/chhhd/1TEAM-CVE-Analysis-Evaluation-System) | 팀원5 팀원5 — CVE |
