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

## 어디에 기록하는가 — 자기 레포 + MEMORY 이중 기록

각자(이나윤/임희영/박나현/박정근)는 평소 자기 전문 레포(`1TEAM-Recon-Subagent` 등)
에서 agent를 돌리고, 그 레포의 `evidence/evidence.csv`에 먼저 기록한다 — 이건
지금까지 해온 방식 그대로다.

**추가로**, 실제 Phase 1~4 게임 중에는 같은 행을 **이 레포(`1TEAM-MEMORY`)의
evidence.csv에도 append하고 push**한다. `1TEAM-MEMORY`가 팀 전체 결과가
모이는 곳이기 때문에(README §링크·§작업 흐름 참고), 각자 레포에만 남기면
팀원1이 Phase 3에서 5곳을 일일이 pull해서 취합해야 한다.

```bash
# 1TEAM-MEMORY 클론을 옆에 두고, 시도 하나 끝날 때마다:
python scripts/append_evidence.py \
  --target http://127.0.0.1:5055 --endpoint "/api/orders/<id>" --agent IDOR \
  --operator 박나현 --caller manual \
  --hypothesis "alice 토큰으로 bob의 주문 조회가 가능한가" \
  --payload "GET /api/orders/102, Authorization: Bearer alice-token" \
  --observation "200 OK, bob 소유 주문 데이터 반환 — 소유권 검증 없음" \
  --new-info yes --status unconfirmed --evidence-ref -

git add evidence/evidence.csv
git commit -m "<이름>: <endpoint> <agent> 시도 N건 (MEMORY 동기화)"
git push
```

(스크립트는 각자 레포에 있는 `scripts/append_evidence.py`와 완전히 동일하다 —
같은 스키마이므로 커맨드도 그대로 재사용 가능.)

## 오케스트레이터 전달용 요약 (Phase 3)

팀원1은 체이닝 판단 전에 아래로 confirmed 행만 모아 오케스트레이터 세션에 전달한다:

```bash
python scripts/confirmed_summary.py               # 전체
python scripts/confirmed_summary.py --agent IDOR   # 특정 agent만
```

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
