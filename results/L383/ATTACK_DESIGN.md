# L383 ATTACK DESIGN — Wetterich Γ_k 1차 truncation (LPA) 으로 σ_0 flow 도출

작성일: 2026-05-01
독립성: L383 단독. 외부 SQT 결과 (L33, L46 등) 의 수치 가져오기 금지. 본 세션은 RG flow 도출 자체에만 집중.

---

## 0. 정직 한 줄

LPA 는 cutoff k 에 의존하는 effective potential `U_k(σ)` 만 truncation 으로 남기는 가장 단순한 ansatz 이며, σ_0 의 fixed-point (FP) 위치 정량은 dimensionless flow `du/dt = β(u, ...)` 의 0 점을 수치적으로 푸는 문제로 환원된다. 본 도출은 이 단계까지 수행하고, 이후 universality class / critical exponent 추출은 L383 범위 밖으로 둔다.

---

## 1. 목표

- Wetterich exact RG equation 의 LPA truncation 에서 σ-field potential `U_k(σ)` 의 flow 를 유도한다.
- 무차원화 후 σ_0(k) (potential minimum 위치) 의 RG 흐름 ODE 를 얻는다.
- σ_0 의 fixed-point (Gaussian, Wilson-Fisher 형) 위치를 수치적으로 동정한다.
- σ(k) = σ_0(k) 의 k-의존성 그래프를 산출한다.

비목표 (L383 외):
- η (anomalous dimension) 의 LPA' 보정.
- 우주론 데이터 피팅 (BAO/CMB/SN/RSD).
- SQMH 다른 후보와의 평가 (K1~K20).

---

## 2. 이론 방향 (수식 금지 — CLAUDE.md 최우선-1)

다음 "방향" 만 본 attack 에서 인용한다. 구체 수식은 simulations/L383/run.py 안에서 표준 RG 교과서 형태로 직접 구현한다.

- Wetterich equation: scale k 에 따른 effective average action `Γ_k` 의 1-loop exact flow.
- Truncation level: 1차 (LPA) — 운동항 z-factor 동결 (Z_k=1), `U_k(σ)` 만 RG 흐름.
- Regulator: Litim optimised cutoff (해석적 단순성).
- Field content: 단일 실수 스칼라 σ (SQMH 의 metabolic field 직접 차원 D=4 Euclidean 공간).
- 유도 경로: Wetterich eq → background field 에서 second functional derivative → Litim regulator 분모 단순화 → dimensionless `u_k(σ̃)` flow.
- FP: `du/dt = 0` 의 두 해 — 자명한 Gaussian FP 와 비자명 Wilson-Fisher 형 FP.

---

## 3. 산출 명세

### 3.1 simulations/L383/run.py
- LPA flow 의 dimensionless ODE 를 직접 구현.
- σ_0(k) 추적: 매 RG step 에서 `dU_k/dσ |_{σ_0}=0` 조건으로 minimum 위치 갱신.
- D=4 Euclidean, single real scalar, Z2 invariant `U_k(σ) = U_k(σ²)`.
- 두 가지 출력:
  1. `(t, σ_0(t), u(σ_0,t))` 시계열 (t = ln(k/Λ), Λ=UV cutoff).
  2. FP 동정: `β_λ(λ*)=0, β_m²(m²*)=0` 의 2D Newton 해.
- 결과 JSON: `results/L383/lpa_flow.json` (t array, σ_0 array, FP 좌표).
- 그림: `results/L383/lpa_flow.png` — σ_0(t), u(σ_0, t).

### 3.2 results/L383/REVIEW.md
- 4인 코드리뷰 (역할 사전 지정 없음, 자율 분담).
- 검증 항목:
  - β-function 의 부호 / known Gaussian FP 위치 (origin) 도달 확인.
  - Wilson-Fisher 형 FP 가 D=4 에서는 Gaussian 으로 합쳐짐 (canonical 결과) — 코드가 이를 재현하는가.
  - D=3 sanity check (선택): WF FP 가 비자명 위치로 분리되는지.
  - 수치 적분 안정성 (RG step Δt, k_min/k_max 범위).

### 3.3 results/L383/ATTACK_DESIGN.md
- 본 문서.

---

## 4. 검증 기준

- C1: β-function 이 σ → 0 극한에서 Gaussian FP 를 정확히 재현.
- C2: D=4 LPA 에서 비자명 FP 가 (수치 정밀도 안에서) Gaussian 과 합쳐지거나 marginal — 표준 결과 일치.
- C3: σ_0(k) flow 가 IR 극한 (k→0) 에서 finite 값으로 수렴 또는 broken phase 로 명확히 분기.
- C4: 결과 JSON / 그림 재현 가능 (seed 고정, single-thread).

C1-C3 모두 통과 시 L383 은 SQMH σ-flow 의 LPA-level 정량을 확보한 것으로 본다. 실패 시 base.fix 패턴으로 정직 기록.

---

## 5. 일정

- 단일 세션 내 완결.
- 코드: 100~150 줄 내외, multiprocessing 불필요 (FP Newton + 1D ODE).
- CLAUDE.md OMP/MKL/OPENBLAS_NUM_THREADS=1 준수.

---

## 6. 정직 한 줄

LPA 는 σ-flow 의 가장 거친 근사이고, η, Z_k 동결 가정 때문에 D=4 비자명 FP 부재 같은 표준 결과 외에는 SQMH-specific 새 정보를 거의 주지 않는다. 본 결과는 후속 LPA' / DE2 truncation 의 baseline 으로만 의미가 있다.
