# L572 — Action Items 우선순위 표

세션 범위: L322 ~ L571 후속 행동 항목.
작성일: 2026-05-02.
범위: 단일 표 (5 카테고리). 디스크 edit 0건 (본 표 자체만 산출).

## 정직 한 줄

본 표는 우선순위/의존성/거버넌스 라벨만 정리한 것이며, 실제 trigger / commit / 제출은 각 항목에 명시된 Rule-A (8인 순차) 또는 Rule-B (4인 자율 분담) 합의 통과 후에만 수행한다.

---

## 우선순위 표

| # | 카테고리 | Action Item | 의존성 | CLAUDE.md 의무 |
|---|---|---|---|---|
| 1 | 즉시 (~05-08) | L570 권고서 review + 옵션 C 채택 결정 | 없음 (선행 항목) | 단일 에이전트 (사용자 결정) |
| 2 | 즉시 (~05-08) | `paper/MNRAS_DRAFT.md` (untracked) 처리 — 단순 삭제 또는 `git status` 정리 | #1 통과 후 | 단일 에이전트 (디스크 edit) |
| 3 | 즉시 (~05-08) | arXiv preprint 의 fabrication disclosure paragraph 삽입 trigger | #1 통과 후 | 8인 Rule-A 라운드 |
| 4 | 즉시 (~05-08) | `claims_status.json` L631 estimator 라벨 정정 (L558 발견) | 없음 | 4인 Rule-B (코드/JSON 검증) |
| 5 | 1주 (~05-15) | L555 정정 protocol 3-라운드 trigger (L556 수치 / L557 grade+universality / L558 통합 commit) | #4 선행 | 8인 Rule-A (이론/수치 클레임) |
| 6 | 1주 (~05-15) | `paper/MNRAS_DRAFT.md` L74/L192 PASS_STRONG mismatch 정정 (L555 R6 발견) | #5 R6 통과 후 | 4인 Rule-B (문서 정합성) |
| 7 | 1주 (~05-15) | `expected_outputs` JSON 자기모순 (classification=PASS_STRONG vs verdict=PASS) 정정 | #4, #5 선행 | 4인 Rule-B (JSON 스키마) |
| 8 | 1주 (~05-15) | L569 phenomenology pivot 의 CLAUDE.md 등록 합의 | #5 통과 후 | 8인 Rule-A (포지셔닝 변경) |
| 9 | 1달 (~06-02) | arXiv D 변환 Rule-A 8인 라운드 (L567 의제 8건) | #3, #8 통과 후 | 8인 Rule-A |
| 10 | 1달 (~06-02) | Companion B (OJA) 제출 준비 — case study 주체 변경 | #8 통과 후 | 8인 Rule-A (이론 포지셔닝) |
| 11 | 1달 (~06-02) | D2 (holographic boundary) 4 protocol 사전등록 시도 (L566 박탈 default 재검토) | #5 통과 후 | 8인 Rule-A (이론 등록) |
| 12 | 1달 (~06-02) | L498 falsifier independence Rule-B 4인 재검증 (estimator 라벨 정합) | #4, #7 통과 후 | 4인 Rule-B |
| 13 | 1분기 (~08-02) | arXiv-D-as-paper PRD/JCAP 제출 (L567 timeline) | #9 통과 후 | 8인 Rule-A (제출 합의) |
| 14 | 1분기 (~08-02) | Companion B (OJA) 제출 | #10 통과 후 | 8인 Rule-A |
| 15 | 1분기 (~08-02) | DR3 결과 도착 (2027-Q2) 시 revision protocol 사전등록 | #11 통과 후 | 8인 Rule-A (사전등록) |
| 16 | 1분기 (~08-02) | L572 표 자체 mid-quarter review (drift 점검) | 없음 (자동 1회) | 4인 Rule-B |
| 17 | 장기 (DR3 이후, 2027-Q2~) | DR3 결과 falsifier 평가 (D2/D-as-paper 사전등록 protocol 적용) | #11, #15 통과 후 | 8인 Rule-A |
| 18 | 장기 (DR3 이후) | Round 11 후속 paper 작성 (DR3 결과별 분기) | #17 결과 확정 후 | 8인 Rule-A |
| 19 | 장기 (DR3 이후) | DR3 결과 → falsifier verdict 의 CLAUDE.md 재발방지 등록 | #17 통과 후 | 8인 Rule-A + 4인 Rule-B |
| 20 | 장기 (DR3 이후) | `simulations/l6/dr3/run_dr3.sh` 실행 (DESI DR3 공개 후에만) | DESI DR3 공개 | 4인 Rule-B (코드 실행) |

---

## 카테고리별 요약 카운트

- 즉시 (이번 주, 05-02 ~ 05-08): 4건 (#1–#4)
- 1주 (~ 05-15): 4건 (#5–#8)
- 1달 (~ 06-02): 4건 (#9–#12)
- 1분기 (~ 08-02): 4건 (#13–#16)
- 장기 (DR3 이후, 2027-Q2~): 4건 (#17–#20)
- 합계: 20건

## 의존성 체인 (요약)

- 정정 체인: #4 → #5 → {#6, #7, #8}
- 발표 체인: {#3, #8} → #9 → #13
- Companion 체인: #8 → #10 → #14
- 사전등록 체인: #5 → #11 → #15 → #17 → {#18, #19}
- DR3 실행 체인: DESI DR3 공개 → #20 (병렬), #17 (분석)

## CLAUDE.md 정합 체크

- paper / claims_status / 디스크 edit 0건 — 본 표는 `results/L572/ACTION_ITEMS.md` 신규 생성만 (L572 산출물 디렉터리). paper/, claims_status.json 미터치.
- 결과 왜곡 금지 — 모든 항목은 해당 라운드 (L555/L567/L569/L570) 의 기록을 그대로 인용.
- 단일 에이전트 / 8인 Rule-A / 4인 Rule-B 라벨을 항목별로 명시.
