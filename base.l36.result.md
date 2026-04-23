# base.l36.result.md — L36 결과

> 실행일: 2026-04-20. wa<0 복원 탐색. 총 소요시간: 17201s (4.78시간).
> ΛCDM baseline AICc = 1670.12 (L35 확정값).

---

## ■ 핵심 결론

**wa<0 구조와 ΔAICc<0은 현재 SQT psi(z) 구조에서 동시 달성 불가.**

| 모델 | ΔAICc | wa | 판정 |
|------|-------|----|------|
| B' (k=4, gamma<0) | **-6.04** | +0.63 | Q91 STRONG |
| D (k=4, exp감쇠) | **-8.44** | +0.37 | Q91 STRONG |
| C' (k=4, 재최적화) | +1468 | -1.01 | K92 INVALID |
| A'_fixed (k=2, n=1/3) | +65.8 | -0.33 | K90 KILL |
| A'_free (k=3, n피팅) | **+0.40** | -0.054 | K90 KILL |

---

## ■ ΛCDM 기준선 (L35 재사용)

Om=0.3094, H0=68.41, chi2_joint=1666.12, AICc=1670.12, H0 tension=4.01σ

---

## ■ 모델별 상세 결과

### Model B' (k=4, phantom 허용 구조)

g = tanh(sqrt(pi/2)*1.47*(ratio-1)) + gamma*(ratio-1)^2, rho_DE=OL0*(1+amp*g)

| 지표 | 값 |
|------|-----|
| Om | 0.3193 |
| H₀ | 67.27 |
| amp | 0.1309 |
| gamma | -0.0348 |
| chi2_BAO | 10.03 |
| chi2_CMB | 0.12 |
| chi2_SN | 1639.29 |
| chi2_RSD | 6.62 |
| chi2_joint | 1656.06 |
| AICc | 1664.09 |
| **ΔAICc** | **-6.04** |
| w0 | -1.217 |
| wa | **+0.631** (wa>0) |
| H₀ tension | 5.00σ |
| 경계 도달 | 없음 |
| **판정** | **Q91 STRONG** |

- gamma=-0.035 (음수 허용됨) → phantom 구조 사용
- 그러나 최적화 결과는 wa=+0.63 (quintessence 방향)
- gamma<0 항의 효과가 작아 타 파라미터가 wa>0 방향으로 수렴
- ΔAICc 개선 주 동력: SN 1639.3 (LCDM 1646.8 대비 -7.5pt)

---

### Model D (k=4, phantom 자연 구조) — 최고 ΔAICc

rho_DE = OL0 * (1 + amp*(ratio-1)*exp(-beta*z))

| 지표 | 값 |
|------|-----|
| Om | 0.3220 |
| H₀ | 66.98 |
| amp | 0.8178 |
| beta | 3.533 |
| chi2_BAO | 9.86 |
| chi2_CMB | 0.10 |
| chi2_SN | 1636.85 |
| chi2_RSD | 6.85 |
| chi2_joint | 1653.66 |
| AICc | 1661.68 |
| **ΔAICc** | **-8.44** |
| w0 | -1.137 |
| wa | **+0.367** (wa>0) |
| H₀ tension | 5.25σ |
| 경계 도달 | 없음 |
| **판정** | **Q91 STRONG** |

- amp=+0.818 > 0: 최적화가 phantom(amp<0) 아닌 quintessence 방향 선택
- beta=3.53: exp(-3.53*z)가 z~0.3 이상에서 급격히 0으로 수렴
- 물리적 해석: 저z에서 amp*(ratio-1)의 bump → DE가 중간z에서 최고, 이후 OL0로 감소
- SN chi2=1636.85로 L35 최저치 달성 (LCDM 1646.8 대비 -9.95pt)

---

### Model C' (k=4, 전환 구조 재최적화) — K92 INVALID

| 지표 | 값 |
|------|-----|
| Om | 0.381 |
| H₀ | 56.02 (하한 근접) |
| amp | **0.500 (하한 도달)** |
| c | **2.500 (상한 도달)** |
| chi2_joint | 3129.74 |
| ΔAICc | +1467.6 |
| wa | -1.005 (wa<0이나 무효) |
| **판정** | **K92 INVALID** |

- L35 Model C: amp=0.100(하한), c=2.998(상한). L36 경계 변경해도 여전히 경계 도달.
- amp 하한 0.10→0.50 변경이 오히려 모델을 더 불안정 영역으로 강제
- 결론: Model C 수식은 Om~0.30 제약 하에서 구조적으로 적합하지 않음

---

### Model A'_fixed (k=2, n=1/3 고정)

rho_DE = OL0 * ratio^(1/3)

| 지표 | 값 |
|------|-----|
| Om | 0.3215 |
| H₀ | 64.98 |
| chi2_BAO | 43.29 |
| chi2_CMB | 38.85 |
| chi2_joint | 1731.89 |
| ΔAICc | +65.77 |
| w0 | -1.098 |
| wa | **-0.328** (wa<0 달성) |
| H₀ tension | 6.98σ |
| **판정** | **K90 KILL** |

- wa<0 달성! (구조적으로 ratio^n → (1+z)^n at high z → CPL phantom)
- 그러나 BAO chi2=43.3, CMB chi2=38.9 → 데이터 적합도 매우 불량
- H0=64.98 → H₀ tension 6.98σ (악화)
- n=1/3 고정이 너무 강한 제약

---

### Model A'_free (k=3, n 피팅)

rho_DE = OL0 * ratio^n, n 자유 파라미터

| 지표 | 값 |
|------|-----|
| Om | 0.3113 |
| H₀ | 67.92 |
| n | **0.0545** |
| chi2_BAO | 13.17 |
| chi2_CMB | 0.78 |
| chi2_SN | 1643.66 |
| chi2_RSD | 6.90 |
| chi2_joint | 1664.51 |
| AICc | 1670.52 |
| **ΔAICc** | **+0.40** |
| w0 | -1.015 |
| wa | **-0.054** (wa<0 달성) |
| H₀ tension | 4.44σ |
| 경계 도달 | 없음 |
| **판정** | **K90 KILL** |

**이 모델이 가장 흥미로운 결과:**
- n=0.055 ≈ 0: 거의 ΛCDM에 가까운 미세 perturbation
- wa=-0.054 < 0: DESI 방향 phantom 달성 (작지만 유의미)
- ΔAICc=+0.40: ΛCDM 대비 0.40 열세 (사실상 통계적 동등)
- 모든 chi2 성분이 합리적인 범위
- H₀ tension 4.44σ → LCDM보다 약간 높음

**물리적 의미**: 데이터가 n≈0.055의 미세한 quintessence/phantom 혼합을 선호하나 ΛCDM과 구별 불가 (ΔAICc~0.4).

---

## ■ 핵심 발견: wa 부호 vs ΔAICc 트레이드오프

| 모델 | ΔAICc | wa | AICc 개선? | wa<0? |
|------|-------|----|---------|----- |
| D | -8.44 | +0.37 | ✅ | ❌ |
| B' | -6.04 | +0.63 | ✅ | ❌ |
| B (L35) | -4.83 | +0.18 | ✅ | ❌ |
| A'_free | +0.40 | -0.054 | ❌ | ✅ |
| A'_fixed | +65.8 | -0.33 | ❌ | ✅ |
| C' | +1468 | -1.01 | ❌ | ✅ |

**패턴 확정**: 현 SQT psi(z) 구조에서 AICc 개선(quintessence 방향)과 wa<0(phantom 방향)이 상충.

---

## ■ 구조적 원인 분석

**왜 SQT가 quintessence(wa>0) 방향으로 수렴하는가?**

psi(z) = 1/(1+alpha*(1+z)^3) → ratio = psi(0)/psi(z) > 1 for z>0

rho_DE는 z 증가 시 항상 OL0보다 크거나 같음 (ratio ≥ 1이므로).
→ DE는 과거에 더 밀도가 높았음 → quintessence (drho/da < 0, w>-1)

phantom(wa<0)을 위해서는 rho_DE < OL0 at intermediate z가 필요하나,
psi 구조의 단조 증가 특성이 이를 원천 차단.

유일한 예외: Model D에서 amp<0 허용 시 rho_DE < OL0 가능하나,
최적화가 chi2 감소를 위해 amp>0 quintessence 방향을 선택함.

---

## ■ L36 판정 종합

| 등급 | 모델 |
|------|------|
| Q92 GAME | — (없음) |
| Q91 STRONG | **D** (ΔAICc=-8.44), **B'** (ΔAICc=-6.04) |
| Q90 PASS | — |
| K90 KILL | A'_fixed (+65.8), A'_free (+0.40) |
| K92 INVALID | C' |

---

## ■ 다음 방향 (L37 또는 공리 확장)

### 옵션 1: 현 SQT 공리로 wa<0 달성 시도
- rho_DE < OL0 가능한 새 구조 필요
- 예: rho_DE = OL0 * f(ratio) where f(1)=1, f'(1) < 0 (역전형)
- 매우 비자연적 구조 필요

### 옵션 2: 공리 확장
- SQMH 공리에서 비롯되는 phantom 항 추가
- C26(Perez-Sudarsky drift), C28(RR non-local) 등 기존 탐색과 통합
- 새 공리 기반 rho_DE 구조 도출

### 옵션 3: L35/L36 결과 그대로 수용
- Model D Q91 STRONG (ΔAICc=-8.44)을 현 SQT 최선
- "wa>0 SQT" vs "wa<0 DESI" 긴장을 솔직히 보고
- MCMC(Phase 5)로 Model D 파라미터 불확실도 정량화

### 옵션 4: 현재 분석 범위 재평가
- DESI wa=-0.83 선호는 DESI+Planck+DES 결합 분석
- BAO-only DESI DR2는 wa 제약 약함 (L35/L36 chi2_RSD ≈ 7/8)
- RSD 추가 데이터 또는 더 tight CMB prior 적용 시 wa 제약 달라질 수 있음

---

*작성: 2026-04-20. L36 wa<0 탐색 완료. 현 SQT psi 구조에서 AICc 개선과 wa<0 동시 달성 불가 확인. Model D Q91 STRONG (ΔAICc=-8.44)이 현재 최선. 총 실행 17201초.*
