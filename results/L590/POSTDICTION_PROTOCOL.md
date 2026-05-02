# L590 — Postdiction Root Cause 회피 Protocol 사전등록 *방향*

**작성일**: 2026-05-02
**원칙**: [최우선-1] 절대 준수 — 수식 0줄, 파라미터 값 0개, 도출 0건. 방향만.
**목적**: L549~L589 의 priori 회복 실패 (R3/R5/R6/R8 반복 위반) root cause = "결과값을 알고서 path/보조가정/부분집합 선택" (postdiction cherry-pick) 을 *blind protocol* 사전등록으로 회피하는 5 방향 검토.

---

## §1. 5 Protocol 비교 표 (방향 / retrospective 가능성 / 본 세션 적용성 / hidden DOF)

| # | Protocol 방향 | retrospective 인정? | 본 세션 적용 가능성 | hidden DOF 위험 | 핵심 한계 |
|---|---|---|---|---|---|
| 1 | **OSF Pre-registration (DOI lock)**: path 후보·결과값 *공개 전* 외부 timestamp 등록 | **불가** — 결과값 (1/(2π), Q17 amplitude 형태) 이 L321 / L498 에서 이미 공개되어 retrospective 등록은 사전등록 정의 위반 | 낮음 (이미 노출) | 외부 timestamp 자체엔 hidden DOF 없음, 그러나 *현 시점 등록 = 무의미* | 시간 순서 자체가 깨짐 (R3 default FAIL) |
| 2 | **Independent third-party derivation**: SQT axiom 만 본 외부 연구자 / 별도 AI agent 가 blind 도출 | 부분 가능 — 외부 agent 가 본 세션 환경 / 과거 transcripts 비접촉 시 | 중간 — 본 세션 권한 외 의존, 별도 컨텍스트 격리 필요. AI agent 일 경우 학습 데이터에 SQT 결과 포함 여부 불명 | agent prompt 설계자 (= 본 세션) 가 hint 주입 가능 → meta hidden DOF | 격리 검증 자체가 또 다른 신뢰 게이트 |
| 3 | **Negative-control derivation**: 다른 결과값 (1/π / 1/(4π) / 1/(2π)²) 도 *동일 protocol* 로 도출 가능한지 시뮬 | 가능 (사후 시뮬) — 결과 다양화 가능성 자체가 cherry-pick 정량 지표 | 중간 — 시뮬레이션 자체 비용. [최우선-1] 위반 회피 위해 *결과값 후보군 명세 / path 분기 카운트* 만 보고하고 수식 도출은 외부에 위임 | 시뮬 디자이너의 path 후보 cherry-pick (선택 편향 한 단계 위로 이동) | 모든 후보 도출 가능 시 cherry-pick 입증, 일부만 가능 시 부분적 priori 회복 |
| 4 | **Counterfactual axiom variation**: SQT axiom (예: axiom 4 의 인자 자리) 변형 시 도출이 자동 변화? | 가능 — axiom 의존성 자체는 retrospective 검증 의미 있음 | 중간 — axiom 변형 catalog 작성은 본 세션 권한 가능, 변형별 도출은 외부 위임 | axiom 변형 카탈로그 선택 자체가 cherry-pick (어떤 변형을 시험할지) | "변형 → 자동 변화" = path 가 axiom 진정 의존, "변형해도 같은 결과" = path 가 axiom 무관 (후자가 priori 약화) |
| 5 | **Bayesian posterior + Bayes factor**: prior=axiom only, likelihood=관측 anchor, posterior 계산 → cherry-pick 정량화 | 가능 (정량 지표) | 중간 — 본 세션 내 prior/likelihood 명세 가능, 단 prior choice 자체 hidden DOF | prior 형태 (uniform / Jeffreys / informative) 선택 = 추가 hidden DOF. likelihood 가 anchor 결과 알고서 fit 시 cherry-pick 정량화 자체가 오염 | Bayes factor 가 1 근처면 cherry-pick 입증, ≫1 이면 부분적 priori 정당화 |

---

## §2. Top-2 Protocol (실행 가능성 기반)

**우선순위 판정 기준**: (a) retrospective 인정 가능성, (b) 본 세션 권한 내 *방향만* 으로 산출 가능, (c) [최우선-1] 위반 위험 최소.

### Top-1: **Protocol 3 (Negative-control derivation)**
- 사유: 결과값 후보군 (1/π, 1/(4π), 1/(2π)², ...) 의 *catalog* 만 본 세션이 명세, 도출은 외부 / 별도 agent 위임. 본 세션은 path 분기 수와 후보별 유도 가능 여부의 binary table 만 수신.
- 회복 가능성: 모든 후보가 도출 가능 → cherry-pick 입증, priori 영구 박탈. 일부만 → 부분적 priori 회복 후보 식별.
- 한계: 시뮬레이션 비용, 후보 catalog 자체 cherry-pick.

### Top-2: **Protocol 4 (Counterfactual axiom variation)**
- 사유: axiom 변형 catalog 는 SQT 명세 내부 구조 (axiom 1~N 자리) 에 정의된 것이므로 외부 대비 자유도 작음. 변형별 "도출 변화 / 무변화" binary table 수신 가능.
- 회복 가능성: 변형 → 자동 변화 시 path 가 axiom 에 의존 (priori 부분 회복). 무변화 시 path 가 axiom 외 hidden 가정에 의존 (priori 추가 박탈).
- 한계: 변형 catalog 선택 cherry-pick, 본 세션 권한 내 변형 catalog 명세 가능성 의존.

**기각**: Protocol 1 (retrospective 무효), Protocol 2 (외부 agent 격리 미보장), Protocol 5 (prior choice hidden DOF).

---

## §3. Priori 회복 게이트 통과 가능성 (path × protocol 매트릭스)

| L 세션 / path | 위반 룰 | Protocol 3 적용 시 | Protocol 4 적용 시 | 회복 가능? |
|---|---|---|---|---|
| L549 P3a (K-Z 보조) | R5 | 보조가정 catalog negative-control | axiom 변형 시 K-Z 보조 자동 도출? | 부분 (Protocol 4 우선) |
| L552 RG anchor | truncation cherry-pick | truncation 차수별 negative-control | axiom 변형 시 anchor 자동 이동? | 부분 |
| L562 D4 SK measure | R3 시간 순서 | 다른 measure 후보 도출 catalog | axiom 변형 시 measure 자동 결정? | 낮음 (R3 시간 순서 자체는 회복 불가) |
| L566 D2 default | condition 4 미충족 | 다른 default 후보 negative-control | axiom 변형 시 default 자동 변화? | 부분 (Protocol 4) |
| L578 Q17 P3 cross-product | R8 | a_i × a_j 조합 전체 catalog | axiom 변형 시 자동 선택? | 부분 |
| L587 A7-2 보존량 종류 | R5/R6/R8 | 보존량 후보 (energy/charge/...) catalog | axiom 변형 시 자동 결정? | 부분 |
| L588 A7-1 causality 부분집합 | R8 | 부분집합 catalog negative-control | axiom 변형 시 자동? | 부분 |
| L589 D2 P2 Z₂ wall | R3 default FAIL | 다른 wall 후보 negative-control | axiom 변형 시 자동? | 부분 |

**핵심 관찰**: R3 (시간 순서 자체) 위반 path 는 어떤 protocol 도 회복 불가. R5/R6/R8 (선택 cherry-pick) 위반 path 는 Protocol 3/4 로 부분 회복 후보.

---

## §4. 회의적 통과 0/4 → 회복 가능 건수

**현 상태**: L549~L589 가 회의적 통과 게이트 0/4 (모두 postdiction 외형).

**Protocol 3+4 결합 적용 시 회복 후보**:
- R5/R6/R8 위반 (L549, L552, L578, L587, L588, L589 P2): **6 건 부분 회복 후보**
- R3 시간 순서 위반 (L562, L566, L589 default): **회복 불가**

**낙관적 상한**: 6/9 부분 회복 가능 (도출 검증 후). **현실적 하한**: 0/9 (모든 protocol 자체에 hidden DOF 잔존, 회의적 통과 게이트 강화 시).

**중간 시나리오**: Protocol 3 negative-control 시뮬 비용 + Protocol 4 axiom 변형 catalog 둘 다 외부 위임 가능 시, 1~3 건 priori 회복. 외부 위임 불가 시 0 건.

---

## §5. 정직 한 줄

**모든 priori 회복 protocol 은 본 세션 권한 외 외부 검증 (third-party / negative-control 시뮬 / axiom catalog blind 도출) 에 의존하며, 본 세션 단독으로는 0/9 회복이 솔직한 결론이다.**

---

## CLAUDE.md 정합 확인
- [최우선-1] 수식 0줄, 파라미터 값 0개, 도출 0건 — **준수**
- 단일 에이전트 결정 금지 — protocol 자체가 외부 위임 구조 — **준수**
- LXX 공통 원칙 (방향만 제공, 지도 금지) — **준수**
