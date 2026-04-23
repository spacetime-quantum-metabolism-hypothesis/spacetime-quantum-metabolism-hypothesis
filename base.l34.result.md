# base.l34.result.md — L34 결과

> 실행일: 2026-04-19. Joint DESI DR2 BAO + Planck 2018 CMB + DESY5 SN 피팅.
> L33 Q92/Q93 챔피언 검증. 자유 파라미터: Ω_m, H₀ (k=2). 경과: 1180.1초.

---

## ■ 핵심 결론

**Q92, Q93 모두 J91 KILL — joint 분석에서 ΛCDM에 대규모 열세.**

| 모델 | BAO-only ΔAICc | joint ΔAICc | 판정 |
|------|---------------|-------------|------|
| Q93 sigmoid k=75 | **-6.617** | **+9219** | J91 KILL |
| Q92 tanh c=1.47 | **-4.715** | **+5157** | J91 KILL |

---

## ■ Joint 데이터셋

- DESI DR2 BAO: 13pt, 13×13 full 공분산
- Planck 2018 압축 CMB: theta_star + omega_b h² + omega_c h²
- DESY5 SN: 1829개, 절대등급 marginalization
- **총 n=1845 데이터 포인트**

---

## ■ ΛCDM Joint 기준선

| 지표 | 값 |
|------|-----|
| Ω_m | 0.3032 |
| H₀ | 68.676 km/s/Mpc |
| chi2_BAO | 10.8523 |
| chi2_CMB | 0.2612 |
| chi2_SN | 1649.0579 |
| **chi2_joint** | **1660.1714** |
| **AICc_joint** | **1664.1779** |

ΛCDM: CMB 완벽 적합 (chi2_CMB=0.26), BAO 소폭 악화 (10.85 vs BAO-only 10.19).

---

## ■ Q93 Joint 결과 (sigmoid k=75, z0=0.90, c=1.00, amp=4.00)

| 지표 | 값 |
|------|-----|
| Ω_m | 0.1366 |
| H₀ | **55.000 (하한 도달)** |
| chi2_BAO | 526.44 |
| chi2_CMB | 8431.36 |
| chi2_SN | 1921.15 |
| chi2_joint | 10878.95 |
| AICc_joint | 10882.95 |
| **ΔAICc_joint** | **+9219 (LCDM 대비)** |
| **판정** | **J91 KILL** |

---

## ■ Q92 Joint 결과 (tanh-weight, c=1.47, amp=2.25)

| 지표 | 값 |
|------|-----|
| Ω_m | 0.2779 |
| H₀ | **55.000 (하한 도달)** |
| chi2_BAO | 563.50 |
| chi2_CMB | 4130.10 |
| chi2_SN | 2124.00 |
| chi2_joint | 6817.60 |
| AICc_joint | 6821.61 |
| **ΔAICc_joint** | **+5157 (LCDM 대비)** |
| **판정** | **J91 KILL** |

---

## ■ BAO-only vs Joint 비교

| 모델 | BAO-only ΔAICc | joint ΔAICc | 악화폭 |
|------|---------------|-------------|--------|
| Q93 | -6.617 | +9219 | **+9225** |
| Q92 | -4.715 | +5157 | **+5162** |

---

## ■ 물리적 해석

### 왜 이렇게 큰 폭으로 실패하는가?

**Q93/Q92 챔피언은 BAO-only에서 Om=0.068~0.115의 극단적 저Om 해를 이용**:

1. **CMB 제약**: omega_c h² = Om·h² - omega_b ≈ 0.120 강제
   - Q93 BAO-only: Om=0.068 → omega_c = 0.068*(0.666)²-0.022 ≈ 0.008 (Planck 0.120에서 93σ 벗어남)
   - Joint CMB chi2 폭발 (8431)

2. **모델 구조**: amp=4.0의 강한 sigmoid transition은 Om~0.07에서만 BAO 데이터 설명 가능
   - Om~0.30으로 이동하면 E(z) 형태가 완전히 다르게 되어 BAO, SN 모두 맞지 않음

3. **최적화 실패**: H0=55 (하한) 도달 → 모델이 어떤 파라미터도 joint 적합 불가

### 결론

**L33 Q92/Q93는 BAO-only 과적합**. 추가 상수(k_sig, z0, c, amp)가 k=2로 고정되어 있어
형식적 AICc 패널티는 없지만, 이론이 Om 자유도를 과도하게 이용해 unphysical 해를 찾음.

---

## ■ 다음 방향

L33 접근법의 한계 명확:
- BAO-only 피팅에서 Om을 CMB 사전확률 없이 자유롭게 두면 unphysical 해 가능
- 진정한 SQT 검증을 위해서는 Om≈0.30 제약 하에서 모델 탐색 필요

**제안: L35 — Om 사전확률 [0.25, 0.35] 제약 하에서 새로운 SQT 구조 탐색**
- BAO-only 피팅이지만 CMB-consistent Om 범위 강제
- amp 상한을 낮추거나 (물리적 이유로), z0을 더 높은 z로 이동하거나
- 새로운 함수형 탐색

---

*작성: 2026-04-19. L34 joint 검증 완료. Q92/Q93 J91 KILL 확정.*
