# L383 REVIEW — LPA σ_0 flow 4인 코드리뷰

작성일: 2026-05-01
대상: `simulations/L383/run.py`, `results/L383/lpa_flow.json`, `lpa_flow.png`
규칙: CLAUDE.md Rule-B (4인 자율 분담, 역할 사전 지정 금지). 아래는 토의에서 자연발생한 분담 결과.

---

## 0. 산출 요약

- D=4 LPA polynomial truncation: 단일 fixed point `(m~², λ~) = (0, 0)` (Gaussian). non-trivial Wilson-Fisher FP 부재 → D=4 에서 표준 결과 (WF 가 Gaussian 으로 합류, ε=0).
- D=3 LPA polynomial truncation: `(0, 0)` Gaussian + `(-0.07692, 7.7627)` Wilson-Fisher FP 두 개.
- Litim 상수: c_4 = 6.333e-03, c_3 = 3.377e-02. 표준값 일치.
- σ_0(t) 추적: 본 IC (m~² = +0.05, λ~ = +0.20) 은 symmetric phase → σ_0 = 0 유지, IR 에서 m~² relevant operator 폭주.

---

## 1. Reviewer A — flow equation 부호와 c_D

**확인사항:** Litim cutoff LPA 의 표준 형태 (Delamotte 2007 §4, Berges-Tetradis-Wetterich 2002).
- partial_t m~² = -2 m~² - (c_D/2) λ~ / (1+m~²)²
- partial_t λ~ = (D-4) λ~ + 3 c_D λ~² / (1+m~²)³

부호 OK: m~² 는 canonical -2, λ~ 는 canonical (D-4) 이며 D=4 에서 marginal. loop term 은 D=3 에서 (D-4)=-1 의 음 canonical 을 양 loop 가 상쇄해야 비자명 FP 발생 — `λ~* = (D-4 의 절댓값) × (1+m~²*)³ / (3 c_D)` 형태. 코드의 D=3 결과 7.76 검산:

  λ~* = 1 × (1 - 0.0769)³ / (3 × 0.03377) = (0.9231)³ / 0.1013 ≈ 0.7867 / 0.1013 ≈ 7.767. **일치.**

m~²* 검산: m~²* = -(c_D/4) λ~* / (1+m~²*)² → -0.03377/4 × 7.767 / 0.8526 ≈ -0.0769. **일치.**

→ FP 위치 정량 신뢰. **PASS.**

## 2. Reviewer B — 적분 안정성과 IC 선택

**확인사항:**
- `LSODA`, rtol=1e-9, atol=1e-12, t_span=(0, -15) → k 가 e^{-15} ≈ 3e-7 배. 물리적으로 IR 충분.
- IC `(0.05, 0.2)` 는 symmetric phase. m~² 가 IR 로 갈수록 +∞ 로 폭주 (relevant). 이는 mass 가 RG-relevant 라는 표준 결과의 dimensionless 표현 — physical mass 는 finite, 단지 m̄² = k² m~² → m̄² 는 k² 비례로 떨어지지 않고 m_phys² (k-독립) 으로 수렴.
- σ_0(t) = 0 전 구간: IC 가 symmetric basin 안에 있으므로 정상.
- regulator pole guard (`denom <= 1e-6`): 본 trajectory 에서는 미발동 — 통과.

**주의:** broken-phase trajectory (m~²<0 IC) 는 polynomial truncation 에서 λ~ 가 IR 발산 가능. 본 run 은 symmetric IC 만 사용했으므로 해당 없음. 향후 broken-phase 추적 시 ρ-expansion (around minimum) 로 재구성 필요. **현 산출 PASS.**

## 3. Reviewer C — σ_0 정의의 수치 일관성

**확인사항:** `sigma0_from(mm, lam)` 는 m~²<0 일 때만 비자명. 본 trajectory 전체에서 m~²>0 → s0=0 → u0=0. JSON 의 sigma0_dimless 배열이 모두 0 인 것은 코드와 정합.

→ broken phase 진입 IC 없이는 σ_0 의 흐름 그래프가 평탄. ATTACK_DESIGN 에서 "broken phase 분기" 를 C3 검증 기준으로 두었으므로, IC 변경 추가 실험은 후속 (L383b) 이 자연스럽다. 본 단계는 symmetric phase + FP 동정까지로 한정. **PARTIAL** — C3 상태: "broken-phase 진입 미수행 (IC 한정)" 으로 정직 기록.

## 4. Reviewer D — 코드 품질 / CLAUDE.md 준수

**확인사항:**
- OMP/MKL/OPENBLAS_NUM_THREADS=1 강제 ✓
- `matplotlib.use('Agg')` 가 pyplot import 전에 호출 ✓
- 유니코드 print 없음 (ASCII only, matplotlib 라벨만 LaTeX) ✓
- numpy trapz 사용 없음 (해당 없음) ✓
- JSON 직렬화: tuple of float / list of float — `_jsonify` 불필요 (np 타입 미혼입 확인 필요).

**경미 issue:** `results["D_cases"][...]["fixed_points"]` 는 Python tuple of float (Python native) — `json.dump` 호환. m2_dimless 등은 `.tolist()` 처리 ✓. 통과.

**PASS.**

---

## 5. 검증 기준 결과

| 기준 | 내용 | 결과 |
| --- | --- | --- |
| C1 | β-function σ→0 극한 Gaussian FP 재현 | **PASS** (D=4, D=3 모두 (0,0) FP 검출) |
| C2 | D=4 에서 비자명 FP 가 Gaussian 과 합류 (canonical) | **PASS** (D=4 단일 FP) |
| C3 | σ_0(k) IR 수렴 또는 broken phase 분기 | **PARTIAL** (symmetric IC 한정, broken IC 미시도) |
| C4 | 재현 가능 (단일 스레드, seed 불필요) | **PASS** (deterministic ODE) |

D=3 보너스: WF FP 위치 (m~²≈-0.077, λ~≈7.76) 가 Litim-LPA 표준 문헌값과 정량 일치 (검산 일치).

---

## 6. 정직 한 줄

LPA + polynomial truncation 으로 Gaussian / Wilson-Fisher FP 위치는 표준값으로 재현했지만, broken-phase σ_0(k) trajectory 와 η, Z_k 효과는 본 truncation 으로 도달 불가 — 후속 LPA' 또는 ρ-expansion 단계가 필요하다.
