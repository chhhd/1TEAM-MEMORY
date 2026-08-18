# Evidence Report

이 파일은 `evidence.csv`를 사람이 읽는 리포트로 요약/서술한 것이다.
대회 종료 후 최종 제출 리포트의 초안으로 사용한다.

> 이 스키마는 `1TEAM-Main-Orchestration-Project-Infrastructure`의
> `.claude/skills/evidence-logging/SKILL.md`가 정의한 팀 공통 스키마와
> 동일하다. Recon/Injection/IDOR·Auth/CVE 5개 레포 전원이 같은 형식으로
> 기록하기 때문에, 각 레포에서 결과를 이 파일로 복사해와도 형식이 깨지지
> 않는다. **스키마를 임의로 바꾸지 않는다** — 바꿔야 하면 먼저 팀 전체(5개
> 레포 + 오케스트레이션 레포)와 합의한다.

## 스키마

```
timestamp,target,endpoint,agent,operator,caller,hypothesis,payload,observation,new_info,status,evidence_ref
```

| 컬럼 | 의미 |
| --- | --- |
| `timestamp` | 기록 시각, `HH:MM` (예: `14:32`). 날짜는 없음 — 여러 날짜에 걸치면 git 커밋 시각으로 보정 |
| `target` | 테스트 대상 base URL |
| `endpoint` | 구체적인 엔드포인트/파라미터 (예: `/search?q=`) |
| `agent` | 사용한 전문 agent — `Recon` \| `Injection` \| `IDOR` \| `Auth` \| `CVE` (닫힌 어휘, 임의 추가 금지) |
| `operator` | 실행한 사람 이름 |
| `caller` | `manual`(사람이 직접 실행) \| `orchestrator`(오케스트레이터 지시로 실행) |
| `hypothesis` | 이번 시도로 뭘 확인하려 했는지 한 줄 — **결과를 보기 전에** 작성 |
| `payload` | 실제 사용한 payload/요청 — 재현의 핵심, 생략·요약 금지 |
| `observation` | 관찰된 응답/차이 (상태코드, 문자열 등 구체적으로) |
| `new_info` | `yes` \| `no` — 새로운 정보를 얻었는가 |
| `status` | `unconfirmed` \| `confirmed` \| `dead-end` |
| `evidence_ref` | 스크린샷/로그 파일 경로, 없으면 `-` |

## 기록 규칙

- **append-only**: 기존 행을 고치지 않는다. `unconfirmed` → `confirmed` 승격도
  기존 행을 수정하지 않고 같은 endpoint/payload로 새 행을 추가한다 (재현 2~3회
  확인 후).
- CSV를 텍스트 에디터로 직접 편집하지 않는다 — `payload`/`observation`에 쉼표·따옴표가
  섞이면 손 편집으로 CSV가 깨진다. 각 레포의 `scripts/append_evidence.py` 같은
  헬퍼로 기록하거나, 동일한 방식으로 이스케이프해서 append 한다.
- `hypothesis`는 결과를 보기 전에 적는다 (사후 정당화 금지).
- `status=confirmed`는 재현 없이 1회 관찰만으로 부여하지 않는다.
- 원자료(요청/응답 전문, 스캔 raw output, 스크린샷)는 `evidence/raw/<endpoint>-<n>.*`에
  저장하고 `evidence_ref`에 경로만 남긴다.
- 실제 크리덴셜/개인정보/플래그 원문은 이 파일에 적지 않는다 (마스킹 또는 필드명만 기록).
- `status`가 `confirmed`인 행만 최종 리포트에 포함한다 (`unconfirmed`/`dead-end`는 부록으로 별도 정리).

## 요약 (대회 종료 후 채움 — confirmed 행만)

| timestamp | target | endpoint | agent | 요약 | evidence_ref |
| --- | --- | --- | --- | --- | --- |

## 상세

_(각 confirmed 항목마다 아래 형식으로 추가)_

### <endpoint> — <agent>

- 대상 / 엔드포인트: 
- hypothesis: 
- payload (재현 방법): 
- observation: 
- 영향: 
- 근거: (`evidence_ref` 링크)
- 제안 조치: 
