# L354 ATTACK DESIGN — Wetterich Functional RG for σ_0 flow

## 0. 메타 원칙 (CLAUDE.md 최우선-1, -2 준수)

본 Attack Design 은 "방향" 만 제공한다.
- **금지**: 구체적 truncation ansatz 의 함수 형태, β-function 수치 계수, σ_0 의 fixed-point 값, RG flow 적분 경로 힌트, 임의의 "A = ..." 형태.
- **허용**: 물리 현상 이름, 수학 분야 이름, 수치적 검증 절차의 일반 원칙.
- 8인 팀이 방향만 듣고 truncation, β-function, σ_0 (z=0) 값까지 독립 도출한다.

---

## 1. 독립성 선언

L354 는 L353 이전 결과에 의존하지 않는 **독립 세션**이다.
- 이전 세션의 σ_0 추정값, perturbative 1-loop 결과, fixed-point 위치를 사전에 노출하지 않는다.
- 8인 팀은 Wetterich 방정식의 표준 형태와 문헌만 참조하여 독립적으로 truncation 을 선택한다.

## 2. 주제 (방향만)

> **"SQMH 의 대사 결합 상수 σ_0 의 RG flow 를 Wetterich 의 exact functional RG equation 으로 수치적으로 도출하라. Wilson 류의 functional truncation 을 사용하라."**

이 한 문장 외 추가 지시 없음.

## 3. 핵심 비교 축 (방향)

산출물의 핵심은 **두 가지 계산의 비교**다.
- (A) Wetterich exact equation 기반 non-perturbative flow.
- (B) 표준 perturbative loop expansion (1-loop 또는 2-loop, 팀 자율 선택).

비교 항목은 팀이 자율로 정한다 — fixed-point 존재 유무, IR 값, UV asymptotic, 비-Gaussian 영역 진입 여부 등.

## 4. 팀 구성 (역할 사전 지정 금지)

- **이론 도출 팀: 8인 (Rule-A)**. 역할 분담은 토의에서 자연 발생만 허용. "FRG truncation 담당", "perturbative 담당" 등 사전 배정 금지.
- **코드리뷰 팀: 4인 (Rule-B)**. 시뮬레이션 코드 자율 분담. 역할 사전 지정 금지.

## 5. 시뮬레이션 원칙

- 병렬 실행 우선 (`multiprocessing.get_context('spawn').Pool`, 워커당 `OMP/MKL/OPENBLAS_NUM_THREADS=1`).
- ODE flow 는 `solve_ivp` (RG scale t = ln(k/k_0) 방향 — UV→IR 또는 IR→UV 는 팀 결정).
- 적분 경계 폭주 (예: trans-Planckian, IR pole) 는 해석 toy 또는 분기 처리로 회피. 폭주를 수치 결과로 보고 금지.
- 새 standalone flow 함수 작성 시 알려진 Gaussian 한계 (자유 이론) 와 비교하여 단일점 검증 후 본 스캔 진입.
- numpy 2.x: `np.trapezoid`. 식별자에 공백/유니코드 금지.

## 6. 과적합 방지

- truncation 차수 증가 시 AICc 패널티 명시 — 기준 (LPA, LPA', 2nd-order derivative expansion 등) 별로 χ² 또는 적합도 지표 비교.
- truncation 개선 < AICc 패널티 이면 단순 truncation 채택.

## 7. 정직성

- Wetterich flow 가 perturbative 결과와 일치하지 않으면 정직하게 보고. 불일치를 "non-perturbative 효과 발견" 으로 과장 금지 — truncation artefact 가능성 우선 검토.
- truncation 의존성 (LPA vs LPA' vs higher derivative) 을 반드시 함께 보고. 단일 truncation 결과로 "σ_0 결정" 주장 금지.
- 결과가 SQMH base.md 와 충돌하면 base.fix.md 에 기록.

## 8. 산출물

- `ATTACK_DESIGN.md` (본 문서) — 방향과 원칙.
- `NEXT_STEP.md` — 8인 팀과 4인 코드리뷰 팀이 진입할 다음 액션.
- `REVIEW.md` — 8인/4인 리뷰 합의 결과 양식 (실행 후 채움).

## 9. 종료 조건

- 8인 팀이 σ_0 의 Wetterich flow 와 perturbative loop 비교를 자율 도출하고 `REVIEW.md` 에 합의 서명 완료.
- 시뮬레이션 코드가 4인팀의 자율 분담 리뷰를 통과.
- Wetterich vs perturbative 차이 (또는 일치) 가 정직하게 명시.
