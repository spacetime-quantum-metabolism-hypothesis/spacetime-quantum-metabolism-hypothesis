# base.l35.result.md — L35 결과

> 실행일: 2026-04-20. BAO+CMB+SN+RSD 4-dataset joint 피팅.
> 모델 A/B/C (k=2/3/4) vs ΛCDM. 총 소요시간: 6056.7s (~101분).

---

## ■ 핵심 결론

| 모델 | ΔAICc | 판정 |
|------|-------|------|
| Model A (k=2) | +5170.6 | K90 KILL |
| Model B (k=3) | **-4.83** | **Q91 STRONG** |
| Model C (k=4) | +84.6 | K90 KILL |

**Model B가 유일하게 ΛCDM보다 우수. 단 wa=+0.18 > 0으로 tension 완전 해소 미달 — Q92 GAME 조건 불충족.**

---

## ■ ΛCDM 기준선

| 지표 | 값 |
|------|-----|
| Ω_m | 0.3094 |
| H₀ | 68.41 km/s/Mpc |
| chi2_BAO | 12.2996 |
| chi2_CMB | 0.0095 |
| chi2_SN | 1646.8409 |
| chi2_RSD | 6.9662 |
| **chi2_joint** | **1666.1162** |
| **AICc** | **1670.1227** |
| w0 | -1.000 |
| wa | ≈0 |
| H₀ tension vs SH0ES | 4.01σ |

---

## ■ Model A 결과 (k=2, 순수 선험)

psi(z) = 1/(1+alpha*(1+z)^3), rho_DE = OL0 * psi(0)/psi(z)

| 지표 | 값 |
|------|-----|
| Ω_m | 0.276 |
| H₀ | **55.000 (하한 도달)** |
| chi2_BAO | 2114.70 |
| chi2_CMB | 3012.38 |
| chi2_SN | 1686.29 |
| chi2_RSD | 23.32 |
| chi2_joint | 6836.68 |
| AICc | 6840.69 |
| **ΔAICc** | **+5170.56** |
| **판정** | **K90 KILL** |

Model A는 L34 Q93/Q92와 동일한 패턴: H0 하한 도달, 모든 데이터셋 폭발.
원인: ratio = psi(0)/psi(z) → (1+z)^3 as z→∞, rho_DE가 matter처럼 성장 → E(z) 왜곡.
Om~0.30 제약 하에서 이 구조는 BAO/CMB 동시 설명 불가.

---

## ■ Model B 결과 (k=3, 비선형 응답)

g(z) = tanh(sqrt(pi/2)*(ratio-1)), rho_DE = OL0*(1+amp*g)

| 지표 | 값 |
|------|-----|
| Ω_m | 0.3164 |
| H₀ | 67.26 km/s/Mpc |
| amp | 0.1339 |
| chi2_BAO | 11.1654 |
| chi2_CMB | 1.3588 |
| chi2_SN | 1640.0500 |
| chi2_RSD | 6.7049 |
| chi2_joint | 1659.2792 |
| AICc | 1665.2921 |
| **ΔAICc** | **-4.83** |
| w0 | -1.108 |
| wa | +0.178 |
| H₀ tension vs SH0ES | 5.01σ |
| **판정** | **Q91 STRONG** |

코드 출력 "Q92 GAME"은 ΔAICc 기준만 적용한 결과. L35 command Q92 조건은 "ΔAICc<-4 AND 모든 tension 개선"이므로:
- wa = +0.178 > 0 → wa<0 tension 미해소
- H₀ tension 4.01→5.01σ → 악화

따라서 **Q91 STRONG**으로 하향 판정.

### chi2 개선 분석 (vs ΛCDM)
| 데이터셋 | ΛCDM chi2 | Model B chi2 | 개선 |
|---------|-----------|--------------|------|
| BAO | 12.30 | 11.17 | **+1.13** |
| CMB | 0.01 | 1.36 | -1.35 |
| SN | 1646.84 | 1640.05 | **+6.79** |
| RSD | 6.97 | 6.70 | **+0.27** |
| **총** | **1666.12** | **1659.28** | **+6.84** |

SN chi2 개선 6.79가 주 동력. AICc 패널티 +2(k=3→k=2 추가 파라미터) 이후에도 ΔAICc=-4.83.

### 물리적 해석
- amp=0.134 → ΛCDM에서 13.4% 비선형 응답 perturbation
- tanh 포화 구조: z→∞에서 rho_DE=OL0*(1+amp) 유한 수렴 (Model A와 달리 폭발 없음)
- wa=+0.178: 고z에서 w가 -1보다 덜 음수 (thawing형)
- DESI DR2 선호 (wa<0, phantom 방향)와 반대 — DESI tension 해소 불가

---

## ■ Model C 결과 (k=4, 전환 구조)

wt=tanh(z), g=(1-wt)*tanh(sqrt(pi/2)*c*(ratio-1))+wt*(ratio-1), rho_DE=OL0*(1+amp*g)

| 지표 | 값 |
|------|-----|
| Ω_m | 0.3151 |
| H₀ | 65.74 km/s/Mpc |
| amp | 0.1000 (하한 도달) |
| c | 2.9984 (상한 근접) |
| chi2_BAO | 64.08 |
| chi2_CMB | 37.92 |
| chi2_SN | 1637.52 |
| chi2_RSD | 7.21 |
| chi2_joint | 1746.74 |
| AICc | 1754.76 |
| **ΔAICc** | **+84.63** |
| w0 | -0.956 |
| wa | -0.520 |
| H₀ tension | 6.33σ |
| **판정** | **K90 KILL** |

amp=0.100 (하한), c=2.998 (상한 근접) → 최적화 미수렴 신호.
BAO chi2=64.08 (ΛCDM 12.3 대비 5× 악화), CMB chi2=37.92 (ΛCDM 0.01 대비 폭발).
물리적 원인: wt*(ratio-1) 항이 고z에서 선형 성장 → rho_DE 폭발.

---

## ■ 판정 요약

| 모델 | chi2_joint | AICc | ΔAICc | wa | H0 tension | 판정 |
|------|-----------|------|-------|----|-----------|----|
| ΛCDM | 1666.12 | 1670.12 | 0 | 0 | 4.01σ | baseline |
| A | 6836.68 | 6840.69 | +5170.6 | -1.04 | 15.6σ | K90 KILL |
| **B** | **1659.28** | **1665.29** | **-4.83** | **+0.18** | **5.01σ** | **Q91 STRONG** |
| C | 1746.74 | 1754.76 | +84.6 | -0.52 | 6.33σ | K90 KILL |

---

## ■ 해석

### Model B: 왜 ΔAICc=-4.83인가?
- amp=0.134의 소폭 비선형 응답이 SN 적합도를 6.8 개선
- BAO, RSD도 소폭 개선 (CMB는 0.01→1.36 소폭 악화)
- 총 chi2 6.84 개선 - AICc 패널티 2 = 4.84 순 이득

### 왜 Q92 GAME 미달인가?
- wa = +0.178 > 0: thawing 방향, DESI 선호(phantom, wa<0)와 반대
- H₀ 4.01σ→5.01σ: Hubble tension 악화 (H0=67.26 < ΛCDM 68.41)
- "모든 tension 개선" 조건 미충족

### 근본적 구조 한계
- Model A/C: ratio = psi(0)/psi(z)가 z→∞에서 발산 → chi2 폭발
- Model B: tanh 포화로 발산을 막지만, 그 대가로 고z 거동이 ΛCDM과 유사 → 개선폭 제한적
- Om~0.30 (CMB 제약) 하에서 SQT 비선형 응답이 BAO/RSD를 동시에 크게 개선하기 어려움

---

## ■ Model C 재실행 권고사항

amp, c 파라미터가 경계에 박힘 → 최적화 불완전. 가능한 개선:
- amp 초기값: [0.05, 0.3, 0.5] 고르게
- c 초기값: [0.5, 1.0, 1.5] 저c 탐색
- bounds 확장: c→[0.3, 5.0]
- Model C wt*(ratio-1) 항 클리핑 강화

---

## ■ L36 방향 제안

Model B의 Q91 STRONG 달성은 긍정적 신호. 개선 방향:
1. **wa<0 유도 구조 탐색**: 고z에서 w가 -1보다 더 음수인 구조 (freezing형)
2. **H₀ 향상**: H₀>68.41 허용하는 구조 (CMB-consistent)
3. **Model B amp 최적화**: MCMC로 amp 불확실도 정량화
4. **Model C 재최적화**: 경계 박힘 문제 해결 후 재실행

---

*작성: 2026-04-20. L35 BAO+CMB+SN+RSD 4-dataset joint. Model B Q91 STRONG (ΔAICc=-4.83). 총 실행 6057초.*
