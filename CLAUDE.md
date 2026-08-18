# CLAUDE.md

이 레포에서 Claude Code로 작업할 때 지켜야 할 규칙.

## 프로젝트 성격

CTF/모의해킹 훈련을 위한 **에이전트 하네스**다. 실제 공격 스크립트를 실행하는 곳이 아니라,
Recon / Injection / Access Control / CVE 진단 절차를 에이전트·스킬로 정의하고,
증거(evidence)를 구조화해서 남기는 것이 목적이다.

## 범위 제한 (Rules of Engagement)

- `target-info.md`에 명시된 호스트/URL/IP 대역 외에는 스캔·요청하지 않는다.
- 공개 인터넷의 무관한 서비스에 대해 대량 스캔, 무차별 대입, DoS성 요청을 절대 수행하지 않는다.
- 실제 크리덴셜, 개인정보, 플래그 원문은 커밋하지 않는다 — evidence 파일에는 해시/마스킹/요약만 남긴다.
- 대상 시스템 상태를 변경하는 행위(쓰기, 삭제, 설정 변경)는 대회 규정상 명시적으로 허용된 경우에만 수행한다.

## 디렉터리 규칙

- `.claude/agents/*.md` : 서브에이전트 정의 (역할별 1개 파일, frontmatter로 `name`/`description`/`tools` 지정)
- `.claude/skills/<name>/SKILL.md` : 해당 에이전트가 따르는 절차/체크리스트
- `.claude/hooks/` : PreToolUse/PostToolUse 등 훅 스크립트 (증거 자동 로깅, 위험 명령 차단용)
- `evidence/evidence.csv` : 발견 사항을 한 줄씩 구조화 기록 (기계 판독용)
- `evidence/evidence.md` : 사람이 읽는 리포트 초안, csv를 요약/서술

## 커밋/PR 규칙

- 커밋 메시지: `[영역] 요약` (예: `[injection] SQLi 체크리스트 v2`)
- 각자 담당 디렉터리 밖의 파일은 리뷰 요청 없이 수정하지 않는다
- 새 에이전트/스킬을 추가하면 이 파일의 "에이전트 목록"과 README 표를 함께 갱신한다

## 에이전트 목록

| 에이전트 | 정의 파일 | 절차(Skill) |
| --- | --- | --- |
| recon-agent | `.claude/agents/recon-agent.md` | `.claude/skills/recon/SKILL.md` |
| injection-agent | `.claude/agents/injection-agent.md` | `.claude/skills/injection/SKILL.md` |
| access-control-agent | `.claude/agents/access-control-agent.md` | `.claude/skills/access-control/SKILL.md` |
| cve-agent | `.claude/agents/cve-agent.md` | `.claude/skills/cve/SKILL.md` |

## 공통 산출 형식

모든 에이전트는 시도 하나마다 다음 필드로 `evidence/evidence.csv`에 append 한다.
이 스키마는 `1TEAM-Main-Orchestration-Project-Infrastructure`의
`evidence-logging` 스킬이 정의한 팀 공통 스키마와 동일하며, 5개 레포
전원이 같은 형식을 쓴다 — 임의로 컬럼을 바꾸지 않는다.

```
timestamp, target, endpoint, agent, operator, caller, hypothesis, payload, observation, new_info, status, evidence_ref
```

- `agent`는 `Recon` / `Injection` / `IDOR` / `Auth` / `CVE` 중 하나 (닫힌 어휘)
- `caller`는 `manual`(사람이 직접 실행) / `orchestrator`(오케스트레이터 지시로 실행)
- `status`는 `unconfirmed`(1차 관찰) / `confirmed`(재현 2~3회 확인 후 승격) / `dead-end` 중 하나
- **append-only**: 기존 행은 고치지 않는다 — 승격도 새 행 추가로 처리
- 원문 응답, 스크린샷 등 원자료는 `evidence/raw/` 하위에 저장하고 `evidence_ref`로 참조 (해당 디렉터리는 `.gitignore` 처리)
- 자세한 기록 절차는 [evidence/evidence.md](evidence/evidence.md) 참고
