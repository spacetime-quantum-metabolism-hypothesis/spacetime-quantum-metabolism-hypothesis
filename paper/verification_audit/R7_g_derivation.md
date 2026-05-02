# R7 검증 — base.md 추가 claim (이론, 우주론가, 매우 냉철)

**Date**: 2026-05-01
**Scope**: paper/base.md 의 "추가" 4 claim 정량 검증
**Mode**: cold-blooded (자비 없음, framework 자기무모순만 인정)

---

## 1. 검증 대상

| ID | claim | 위치 |
|----|-------|------|
| C1 | G = n_0 μ σ²/(4π), n_0·μ ≈ 4.1×10⁹⁵ kg/m³ (포텐셜 매칭 ✅, 개별값 ❌) | base.md 표제 §3.4 — **실제 수식은 03_background_derivation.md §3.1** |
| C2 | w_eff(z) 대사적 예측 (coupled ODE) | base.md §5.1, §5.3, §5.4, §10.2 |
| C3 | v(r) = g(r)·t_P, 지구 표면 v ≈ 5.3×10⁻⁴³ m/s | base.md §3 일반 (σ_0 = 4πG·t_P 의 inflow 해석) |
| C4 | ξ = 2√(πG)/c² 뉴턴 극한 고정 (자유 매개변수 아님) | base.md §14.4 #21 |

---

## 2. base.md framework (5.2 회로 포함)

```
σ_0 = 4πG·t_P          (foundation 3 holographic)
τ_q = 1/(3 H_0)        (cosmic timescale, postulate 3)
ε   = ℏ/τ_q
ρ_q = n_∞·ε/c² = ρ_Λ_obs    (5.2 ★ circularity: n_∞ ← ρ_Λ_obs input)
```

수치 (h=0.73, Ω_Λ=0.685):

| 양 | 값 |
|---|---|
| σ_0 | 4.522×10⁻⁵³ m³/(kg s) |
| t_P | 5.392×10⁻⁴⁴ s |
| ρ_Planck | 5.154×10⁹⁶ kg/m³ |
| ρ_Planck/(4π) | **4.101×10⁹⁵ kg/m³** |
| n_∞ | 8.23×10⁴¹ m⁻³ |
| ε | 7.49×10⁻⁵² J = 4.67×10⁻³³ eV |

---

## 3. claim 별 판정

### C1. G = σ²·n_0·μ/(4π), n_0·μ ≈ 4.1×10⁹⁵ kg/m³

**framework 도출**:

뉴턴 매칭 (`03_background_derivation.md §3.1`)

```
∇·v = −σ n_0 ρ_m  →  Φ(r) = −GM/r,    G = σ²·n_0·μ/(4π)
```

이를 σ_0 = 4πG·t_P 와 결합하면

```
n_0·μ = 4πG / σ_0² = 4πG / (4πG·t_P)² = 1/(4πG·t_P²) = ρ_Planck/(4π)
```

→ **n_0·μ = ρ_Planck/(4π) 는 framework 의 산술 항등식**이지 추가 가정이 아님.

**수치**: 계산값 4.1013×10⁹⁵ vs claim 4.1×10⁹⁵ → ratio 1.0000 (4자리 일치)

**개별 n_0, μ**: n_∞ = 8.23×10⁴¹ m⁻³ (cosmic) 채택 시 μ_implied = 4.98×10⁵³ kg = 2.3×10⁶¹ m_P → SI 자기무모순 명백 (Planck 질량의 10⁶¹ 배). claim 의 ❌ 인정 일치.

**판정**: **곱 PASS, 개별 FAIL (claim 자체와 일치)**.
**경고**: G derivation 의 수식 자체는 base.md 표제 §3.4 가 아니라 03_background_derivation.md §3.1. base.md 본문은 "Three-regime σ₀(env) parameterization" 만. claim 위치 표기 오류.

---

### C2. w_eff(z) 대사적 예측

**framework**:
- §5.1 cosmic: w_q = −1 (정적 vacuum)
- §5.3 Bianchi: ∇T = −Q, sink 약 10.4%/Hubble → effective |w_a| ~ 0.3
- §5.4 minimal SQT w_a=0, V(n,t)-확장 w_a 부호 OK 하나 box 미충족, **derivation gate OPEN**

**DESI DR2 (DESI+Planck+DES-all)**: w_0 = −0.757±0.058, w_a = −0.83±0.225

| 모델 | w_0 | w_a | 단방 sigma |
|------|-----|------|-----|
| minimal | −1 | 0 | (4.19, 3.69) |
| V(n,t) toy | ~−1 | ~−0.30 | wa: −2.36 |

minimal joint sqrt(χ²) ≈ 5.58σ (uncorr 근사). base.md "8σ tension" 은 full covariance 일 때 다소 더 큼 — **방향성 일치, 정확값 보고 필요**. V(n,t) toy: 부호 OK, 진폭 factor ~3 부족 (base.md 자체 인정).

**판정**: framework **자기일치** (즉, base.md 가 "minimal w_a=0, ext w_a~−0.3 gate OPEN" 이라고 정직하게 인정한 것은 검증 PASS). 단 V(n,t) 의 first-principle 동역학 도출은 **OPEN — 본문 §6.1 #12 한계로 등재**.

---

### C3. v(r) = g(r)·t_P

**차원**: v[m/s] = g[m/s²]·t_P[s] ✅
**framework 도출**: σ_0 = 4πG·t_P 로부터 ∇·v = −σ_0·n·ρ_m → 정적 점질량 한계
v(r) = σ_0·n_0·M/(4π r²) = (4πG·t_P)(n_0)(M)/(4π r²). 그리고 n_0·μ = ρ_Planck/(4π) 와 ρ_local = n_0 μ 식별 (점질량은 n_0 → ρ M δ³ ) 하면

v(r) = G M t_P / r² = g_Newton(r)·t_P ✅ (구조적 도출)

**지구 표면**: g=9.81, t_P=5.392×10⁻⁴⁴ → v = **5.289×10⁻⁴³ m/s** vs claim 5.3×10⁻⁴³ → ratio 0.998. **PASS**.

**판정**: claim **PASS** (framework 직결, 수치 0.2% 일치).

---

### C4. ξ = 2√(πG)/c² (뉴턴 극한 고정)

**대수 검증**: ξ² = 4πG/c⁴ → ξ = 2√(πG)/c² = **3.222×10⁻²²** SI. Newton 매칭 (h_00 = 2Φ/c², Φ ↔ ξ φ T 결합) 으로 자동 고정. 자유 매개변수 아님.

**판정**: 대수 **PASS**. 단 base.md 본문에 **ξ 표기 자체는 명시 부재**. 03_background_derivation.md §3.1 의 σ = 4πG·t_P 와 변수 변환만 다름 (등가). claim 위치 §14.4 #21 은 이 대응을 명시한 표인 것으로 추정 — 명시 표기 보강 권고.

---

## 4. 종합 판정 (verdict)

| 항목 | 판정 | 비고 |
|------|------|------|
| C1 (n_0 μ 곱) | ✅ PASS | 산술 항등식, 4.101×10⁹⁵ 일치 |
| C1 (개별 n_0, μ) | ❌ FAIL (claim 일치) | SI 자기모순 ~10⁶¹배 |
| C2 (framework 자기일치) | ✅ PASS | minimal & V(n,t)-확장 분리 정직 |
| C2 (V(n,t) first-principle) | ⚠ OPEN | derivation gate 미충족 |
| C3 (v = g t_P) | ✅ PASS | 지구 0.998 비율, 차원/구조 직결 |
| C4 (ξ 대수) | ✅ PASS | ξ² = 4πG/c⁴ 산술 정확 |
| C4 (base.md 명시) | ⚠ ABSENT | 본문 표기 부재, 03 §3.1 와 등가 |

**핵심 발견**:
1. C1, C3, C4 는 모두 framework 자기무모순 산술 항등식. **추가 자유도 없음**.
2. n_0·μ = ρ_Planck/(4π) 는 σ_0 = 4πG·t_P 의 자명 따름결과 — claim 의 "포텐셜 매칭" 표현은 약함. **항등식**이 더 정확.
3. C2 는 framework 자체가 derivation gate OPEN 으로 정직 인정 — 검증 통과지만 dark-energy w_a 의 a priori 도출은 여전히 OPEN.
4. claim 위치 표기 오류 (§3.4 ← 실제 03 §3.1), §14.4 #21 의 ξ 는 base.md 본문 직접 노출 부재.

---

## 5. 정직 한 줄

> **C1 곱·C3·C4 는 σ_0 = 4πG·t_P 의 산술 따름결과로 PASS — "예측"이 아니라 "항등식"이며, C1 개별값과 C2 V(n,t) w_a 진폭은 framework 가 인정한 대로 OPEN/FAIL 이다.**
