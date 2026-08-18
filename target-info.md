# Target Info / Rules of Engagement

> 이 파일이 **5개 레포 + MEMORY 전체의 단일 진실 소스(single source of truth)**다.
> 실제 대회/훈련이 시작되면 이 파일부터 채우고, 각자 레포의 `target-info.md`는
> 여기를 가리키기만 한다 — 대상 정보를 레포마다 따로 유지하지 않는다.
> 여기 없는 대상은 어떤 에이전트도 건드리지 않는다.

## 대회/훈련 개요

- 대회명: _(TBD — 실제 대회/훈련 확정 시 채움)_
- 기간: _(TBD, 시작~종료 시각 명시)_
- 규정 문서 링크: _(TBD)_
- 허용 행위: _(예: 정찰, 취약점 스캔, PoC 수준 익스플로잇 — 대회 규정에 맞게 수정)_
- 금지 행위: DoS/무차별 대입/사회공학/스코프 밖 대상 공격 등

## 인가된 대상 (실제 대회/훈련용 — 확정되면 채움)

| 이름 | URL/IP | 포트/범위 | 비고 |
| --- | --- | --- | --- |
| _(예: web-01)_ | _(예: 10.10.x.x)_ | _(예: 80,443)_ | _(예: 로그인 필요 계정 정보는 팀 비공개 채널 참고)_ |

## 현재 사용 중인 리허설/개발용 로컬 대상

> 실제 대회 대상이 아직 없어서, 각자 레포가 agent 정의를 검증하려고 만든
> **로컬 전용(127.0.0.1) 연습 앱**들이다. 서로 다른 포트를 쓰므로 Phase 1~4
> 게임을 실제로 합동 진행할 때는 **이 중 하나로 통일하거나, 위 "인가된 대상"
> 표에 실제 대상을 채워서 그걸 기준으로 진행**해야 한다 — 지금처럼 각자 다른
> 로컬 앱을 보면서 "Recon 결과를 보고 흩어진다"는 성립하지 않는다.

| 대상 | 소유 레포 | 포트 | 엔드포인트 |
| --- | --- | --- | --- |
| `vulnapp/app.py` | `1TEAM-Main-Orchestration-Project-Infrastructure` | `127.0.0.1:5000` | `/search`(SQLi), `/lookup`(대조군), `/user?id=`(IDOR), `/admin`(무인증), `/upload`, `/fetch?url=`(SSRF) |
| `testapp/app.py` | `1TEAM-IDOR-Authorization-Web-Logic-Subagent` | `127.0.0.1:5055` | `/api/orders/<id>`(IDOR), `/api/profile/<id>`(대조군), `/admin/stats`(수직 권한상승), `/api/coupon/redeem`(로직 우회) |
| `dast-harness/targets/vulnerable_app` | `1TEAM-Main-Orchestration-Project-Infrastructure` (submodule) | `127.0.0.1:8080` | `dast-harness` 쪽 `ground_truth.json` 참고 |

각 레포에 있는 자체 연습 앱(Recon/Injection/CVE 레포)도 위와 같은 성격이며,
필요하면 해당 레포 README에서 포트를 확인한다.

## 제외 대상 (Out of Scope)

- 위 표에 없는 모든 IP/도메인 — 로컬(`127.0.0.1`) 외 공인 인터넷 대상은
  실제 대회/훈련 대상으로 명시되기 전까지 전부 제외

## 팀 접속/계정 정보

- 실제 크리덴셜은 이 파일(레포)에 적지 않는다 — 팀 비공개 채널(Notion/Vault 등)에 별도 보관
- 여기에는 "계정이 어디 있는지"에 대한 포인터만 남긴다
- Phase 0 규칙: 계정은 팀원별로 분리한다 (예: IDOR 레포 testapp의 `alice-token`/`bob-token`처럼
  같은 앱에 대해 최소 2개 이상 서로 다른 권한의 테스트 계정)
