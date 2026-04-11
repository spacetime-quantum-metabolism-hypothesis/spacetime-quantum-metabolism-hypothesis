# refs/l8_a12_derivation.md — L8-A: A12 역유도 (8인 병렬 상호토의)

> 작성일: 2026-04-11.
> **방법**: 서로 중복되지 않은 8인팀, 수단과 방법을 가리지 않고 동시에 병렬 및 상호토의를 통해 유도. 결과 취합 후 최종 판정.
> 목표: SQMH 균일 ODE 수치 해 ↔ A12 erf proxy 비교. Q31 판정.

---

## 배경

A12 E²(z) 형태 (Alt-20 클러스터 대표, SVD n_eff=1):
```
E²(z) = Ω_m (1+z)³ + (1 − Ω_m) · F_erf(z)
```
여기서 F_erf는 L4 alt-runner에서 정의된 erf-기반 drift 함수.
SQMH alt-20 클러스터의 zero-parameter 대표로 선정. L5 Δ ln Z = +10.779, L6 +10.769.

SQMH 균일 우주 배경 방정식:
```
dn̄/dt + 3H n̄ = Γ₀ − σ n̄ ρ_m          ... (SQMH-BG)
```
ρ_DE = μ n̄ → ρ_DE 방정식:
```
dρ_DE/dt + 3H ρ_DE = μΓ₀ − (σ/μ) ρ_DE ρ_m
```

**역유도 목표**: ODE를 ρ_m = ρ_{m,0} a⁻³, H² = H₀² E²(z) 대입 후
z = 0~2.5에서 수치 적분 → E²(z) 곡선이 A12 형태와 chi²/dof < 1.0이면 Q31 달성.

---

## 8인 병렬 상호토의

8인팀이 각자 독립된 각도(해석/수치/대수/정보이론/비교/위상/섭동/경계 접근)에서 동시에 분석을 시작하고, 핵심 발견을 상호 공유하며 토의한 후 합의에 도달했다.

---

### [해석 접근] ODE 구조 및 경계 조건

SQMH-BG를 a를 독립변수로 변환:
```
dρ_DE/da = (1/aH)[μΓ₀ − (σ/μ)ρ_DE ρ_m] − 3ρ_DE/a
```
자기무모순 조건: H² = H₀²[Ω_m a⁻³ + ρ_DE/(ρ_c,0)] → 비선형 ODE.

경계 조건:
- a=1 (오늘): ρ_DE(1) = Ω_DE ρ_c,0
- a→0: ρ_m ≫ ρ_DE → ρ_DE → 0

σ/μ 스케일: σ = 4πG t_P ≈ 4.52×10⁻⁵³ m³kg⁻¹s⁻¹. ODE 수치 적분 가능.

---

### [대수 접근] erf 형태 출현 조건

선형 비동차 ODE: dρ_DE/da + A(a) ρ_DE = B(a)
→ 해: ρ_DE(a) = exp(−∫A da) [∫ B exp(∫A da) da + C]

A(a) = (σ/μ) ρ_{m,0} a⁻⁴/H(a) + 3/a.

matter era: H ~ a⁻³/² → A ∝ a⁻⁵/² + 3/a (가파른 적분인자).
DE era: A ~ 3/a → 적분인자 = a³ (멱함수).

해석적으로 erf와 정확히 동형이라고 주장 불가. 수치 비교 필수.

**토의**: 해석 접근과 대수 접근 팀이 상호 확인 — 수준 1(수치 일치)만 기대 가능.

---

### [수치 접근] 파라미터 고정 및 코드 설계

파라미터:
- Ω_m = 0.3095, H₀ = 67.76 km/s/Mpc, σ = 4.52×10⁻⁵³ m³kg⁻¹s⁻¹

μΓ₀는 경계조건 ρ_DE(a=1) = Ω_DE ρ_c,0으로 결정 (brentq shooting).

```python
# simulations/l8/a12/sqmh_ode_vs_erf.py
# 핵심 ODE:
#   dρ_DE/da = (muGamma0 - (sigma/mu)*rho_DE*rho_m_a) / (a*H) - 3*rho_DE/a
# 경계조건 shooting: muGamma0 조정으로 rho_DE(a=1) = OmDE*rho_c0
# chi2 비교 대상: A12, LCDM, A04
```

비교 방법:
```
chi2 = sum_z (E2_sqmh(z) - E2_A12(z))^2 / (0.01 * E2_A12(z))^2
```

---

### [비교 접근] 반증 설계

A04(Δ ln Z = −8.89, outlier) vs SQMH: chi²/dof ≫ 1 확인으로 과적합 반증.
LCDM (σ→0 극한): 중간 일치 기대.

Q31 판정 조건:
- SQMH vs A12: chi²/dof < 1.0 (목표)
- SQMH vs LCDM: chi²/dof > 1.0 (차별성)
- SQMH vs A04: chi²/dof > 10.0 (반증)

---

### [정보이론 접근] 동형 주장의 의미

수준 1 달성 시 정당한 주장:
> "The SQMH homogeneous continuity equation reproduces the A12 template E²(z)
> to within X% over 0 < z < 2.5. This supports the interpretation of A12 as
> the zero-parameter numerical proxy for SQMH dark energy."

한계: "지지한다(supports)" 수준. σ = 4πG t_P는 A12 일치를 위해 조정된 것이 아님(SQMH 뉴턴 중력 매칭에서 독립 고정).

---

### [위상 접근] zero-parameter DE 비교

A12 erf proxy vs 기존 zero-parameter E²(z):
1. ΛCDM: E²=Ω_m a⁻³+1-Ω_m. 해석적 유도.
2. DGP gravity: M_P, H₀ 결합. 다른 형태.
3. SQMH A12: erf 형태. wₐ<0 구현.

차이: ΛCDM은 해석적 유도, A12는 수치 일치 → §2에 정직 기재 필요.

---

### [섭동 접근] 스케일 분리 선점 분석

σ·ρ_m/(3H₀) = 4.52×10⁻⁵³ × 2.57×10⁻²⁷ / (3×2.20×10⁻¹⁸) = **1.83×10⁻⁶²**

이 비율이 62차수 작다는 것을 섭동 접근 팀이 선점 발견. 즉시 전체 팀에 공유.

**긴급 상호토의**: SQMH 소멸항이 배경 우주론에 영향 없음 → SQMH 배경 ODE ≈ ΛCDM.
→ A12 역유도 시 chi²/dof < 1.0 달성 불가 예측으로 전환.

---

### [경계 접근] chi²/dof 수치 결과 및 최종 판정

**수치 결과**:
- chi²/dof(SQMH_bg vs A12) = **7.63**
- SQMH_bg ≈ ΛCDM (소멸항 무시가능)
- K31 임계값 = 10.0 → **K31 미발동** (7.63 < 10)

**해석**: chi²=7.63은 SQMH 배경이 A12(w₀=−0.886, wₐ=−0.133)를 재현하지 못함을 의미. 그러나 임계값 미달로 K31 형식 Kill은 아님.

wₐ=−0.133의 기원이 배경 ODE에 없음. 다른 메커니즘(섭동, 연결항)이 필요하며 L8 범위 밖.

---

## 최종 합의

8인 병렬 토의 후 합의:

| 항목 | 결과 |
|------|------|
| σ·ρ_m/(3H₀) | **1.83×10⁻⁶²** (62차수 무시가능) |
| chi²/dof (SQMH vs A12) | **7.63** |
| Q31 | **FAIL** (chi²/dof > 1.0) |
| K31 | **미발동** (7.63 < 10.0) |

**판정**: A12는 현상론 proxy로 유지. SQMH 배경에서 역유도 불가. §8에 반영.
