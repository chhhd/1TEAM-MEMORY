---
name: recon
description: 인가된 대상에 대한 정찰 절차 — 포트/서비스 스캔부터 기술스택·엔드포인트 파악까지. recon-agent가 새 대상을 조사할 때 사용.
---

# Recon 절차

## 0. 스코프 확인 (필수, 생략 불가)

- `target-info.md`의 "인가된 대상" 표에 이번 대상이 있는지 확인
- 없으면 즉시 중단, 사용자에게 "스코프 밖 대상"이라고 보고

## 1. 네트워크/서비스 스캔

- 포트 스캔: `nmap -sV -Pn <target>` (범위가 넓으면 `-p-` 대신 상위 포트부터)
- 배너 그래빙으로 서비스/버전 확인
- 결과에서 특이 포트(관리 콘솔, DB 직접 노출 등)는 즉시 표시

## 2. 웹 서비스 지문

- HTTP 응답 헤더(Server, X-Powered-By), 쿠키 이름 패턴으로 프레임워크 추정
- `curl -I`, `curl -s` 로 홈페이지/정적 자원 확인
- robots.txt, sitemap.xml, `.well-known/`, 공개 API 스펙(`/swagger`, `/openapi.json`) 확인
- JS 번들에서 API 엔드포인트 문자열 grep

## 3. 엔드포인트/파라미터 목록화

- 발견한 URL, HTTP 메서드, 파라미터명을 표로 정리
- 로그인/회원가입/파일업로드/검색 등 "입력을 받는 지점" 우선 표시 — injection-agent에 넘길 후보
- 사용자 식별자(id, uuid 등)가 URL/파라미터에 노출되는 지점 표시 — access-control-agent에 넘길 후보
- 사용 중인 라이브러리/프레임워크 버전 표시 — cve-agent에 넘길 후보

## 4. 기록

- `evidence/evidence.csv`에 한 줄: `category=recon, severity=info, status=confirmed`
- 상세 원자료(스캔 raw output)는 `evidence/raw/recon-<target>-<timestamp>.md`
- 핸드오프 요약은 recon-agent 정의의 "산출물 핸드오프" 형식을 따른다

## 금지 사항

- 스코프 밖 IP/도메인 스캔 금지
- 무차별 대입, 대량 요청(DoS 성격) 금지
- 발견한 취약점으로 실제 익스플로잇 시도 금지 (다른 에이전트 역할)
