# L489 — Independent Re-verification of L482 RAR PASS_STRONG Candidate

**Verdict (one-line, honest):** PASS_STRONG 격상 *부분만 진짜* — M16-functional-form 한정에서 PASS, 함수 형태 변경 시 a₀ best-fit이 1.04 ↔ 1.21×10⁻¹⁰로 0.064 dex (16%) 흔들림. SQT 1.042e-10 일치는 **simple-nu에서 0.05%, M16에서 2.5%, standard-mu에서 16%**. Cherry-pick 의혹: K-criteria 5개는 functional form 가정에 묶여 있으며, "0.006 dex 통계오차"는 **M16 안에서만 의미**.

---

## 1. L482 재현 — 100% 일치
- 독립 구현으로 동일 SPARC 175 galaxies / 3389 points / Υ_disk=0.5, Υ_bul=0.7 에서:
  - a₀ = 1.0687×10⁻¹⁰ (L482 동일, Δa₀/a₀ = 0.000%)
  - χ² = 4384.46 (L482 동일, Δχ² = 0.0)
  - σ(log₁₀a₀) = 0.0060 dex (L482 동일)
- **코드 버그 없음. 수치 자체는 진짜.**

## 2. 함수 형태 의존성 (원본 L482가 검증하지 않은 채널)
같은 데이터·같은 Υ에서 interpolating function만 바꿔 best-fit a₀:

| 함수 | a₀ (×10⁻¹⁰) | χ² | SQT(1.042) 일치 |
|---|---|---|---|
| M16 (L482 채택) | 1.0687 | 4384.5 | 2.5% (PASS) |
| simple-nu (Famaey-Binney) | **1.0427** | **4380.2** | **0.05% (거의 정확)** |
| standard-mu | 1.2080 | 5070.2 | 16% (FAIL K_R1 경계) |

- **Cross-form spread = 0.064 dex (16%)** — 통계오차 0.006 dex 보다 **10배 큼**.
- L482가 채택한 σ_log(a₀)=0.006 dex는 함수형 시스테매틱을 무시한 **하한** 추정. 진짜 시스테매틱 σ ≈ 0.06 dex.
- McGaugh 2016 본문도 systematic ±0.24×10⁻¹⁰ (≈0.09 dex) 명시 — L482는 이 시스테매틱을 K_R2에 반영하지 않고 통계오차만으로 판정.

## 3. McGaugh 1.20 vs SQT 1.04 — 어느 것이 진짜?
- McGaugh 2016 PRL: a₀ = 1.20 (±0.02 stat ±0.24 sys)×10⁻¹⁰. 이는 **standard-mu 분석 + SPARC Q≥1 cuts**.
- 본 재구현 standard-mu 결과 a₀ = 1.208e-10 → McGaugh 값 정확히 재현 (±0.7%). **McGaugh 1.20은 standard-mu 산물**.
- 본 재구현 M16 결과 a₀ = 1.069e-10 → 후속 SPARC 재분석 (Li+18 1.10, Chae+20 1.1) 과 정합.
- 즉 "McGaugh 1.20 vs SQT 1.04 차이"는 ~80%가 **함수 선택 시스테매틱**이지 데이터 vs 이론 충돌 아님. L482가 "SQT가 McGaugh를 -56 AICc로 이긴다"고 보고한 것은 **functional form 선택을 SQT 쪽에 유리하게 잡은 결과** — Cherry-pick.

## 4. Cherry-pick audit: K-criteria 정의 검토
| K | 원래 정의 | 검증 |
|---|---|---|
| K_R1 (a₀ within 30%) | M16 fit | M16에서 PASS (2.5%), standard에서 PASS (16%), simple-nu에서 PASS (0.05%) — 함수 무관 PASS, 그러나 30% 임계는 매우 느슨 |
| K_R2 (within 2σ) | σ_stat=0.006 사용 | **stat-only 사용 부적절**. σ_systematic ≈ 0.06 dex 포함 시 지나치게 쉽게 PASS — 정보량 0 |
| K_R3 (χ²/dof ≤ 1.5) | M16 SQT-locked | 1.295 PASS but χ²/dof > 1 → 0.13 dex 잡음 floor 과소평가. σ rescale 후 PASS 유지 |
| K_R4 (ΔAICc(SQT-free) ≤ 2) | M16 한정 | M16 PASS (+0.70). simple-nu에서는 +0.001 (더 강한 PASS). standard-mu에서는 +83 (대실패) |
| K_R5 (ΔAICc(SQT-Newton) ≤ −10) | trivial | 모든 함수에서 −40,000 이상. 정보량 거의 0 (Newton은 RAR 어떤 합리적 fit에도 압도됨) |

**K_R5는 사실상 free pass** (Newton이 SPARC를 못 맞추는 건 70년대부터 알려진 사실, SQT 검증과 무관).
**K_R4는 함수형 의존**: M16에서 통과, simple-nu에서 더 강하게 통과, standard-mu에서 대실패.

본 재검증의 추가 K (사후 정직):
- **K_R6 shape-robust** (cross-form |Δlog a₀| ≤ 0.04): **FAIL** (0.064 dex)
- **K_R7 outer/inner 일치** (|log a₀_outer − log a₀_inner| ≤ 0.10): PASS (0.097)

## 5. RAR ↔ BTFR 채널 독립성
L422/L448은 V_flat-only로 a₀_BTFR ≈ 1.53×10⁻¹⁰ 보고 (5σ off SQT). L482는 같은 175 galaxies에서 점별 RAR로 1.07×10⁻¹⁰ 얻음. 차이 ≈ 0.16 dex.

본 재검증: 갤럭시당 outermost-radius-only RAR로 fit → a₀ = 0.856×10⁻¹⁰. innermost-only → 0.685×10⁻¹⁰. 둘 다 BTFR값 (1.53)과 매우 다름. 즉:
- BTFR-only (V_flat 추출) 1.53e-10 vs outer-radius-only RAR 0.86e-10 → **0.25 dex 차이**.
- 이는 **V_flat 추출 단계의 정의 차이** (asymptotic limit fit vs largest-R sample)에서 발생, 새 물리 아님.
- L448 K_Z FAIL은 V_flat 정의 시스테매틱이지 데이터 vs SQT 충돌 아닐 가능성 — L448 결과 자체를 재해석할 필요.
- **결론: RAR/BTFR은 *진정* 독립 채널이 아니라 같은 데이터의 *집계 방식 차이***. L482가 "5/5 PASS"를 BTFR 채널과 별도 확증으로 제시한 것은 부분적 cherry-pick.

## 6. 다른 SQT-MOND 비교 paper
- Verlinde 2017 entropic gravity: a₀ ~ cH/(2π) 동일 형태 — 본 SQT 예측과 *함수적으로 동일*. 즉 SQT 일치는 SQT 고유 검증 아니라 "Verlinde-class 이론 + M16 SPARC" 일치 (ambiguous attribution).
- Milgrom 2020 (arXiv:2001.09729): a₀ = 1.14e-10 SPARC re-analysis. 본 simple-nu fit (1.043) 보다 높음.
- Lelli+17 SPARC database paper: 함수 의존성 명시. M16과 simple-nu 차이 ~10% 보고 — 본 결과 (16%)와 정합.

## 7. 정직 등급
- **PASS_STRONG 격상 = 50% 진짜, 50% cherry-pick.**
  - 진짜 부분: a₀ ~ cH₀/(2π) 형태 prediction은 M16 + simple-nu 어느 쪽으로 봐도 SPARC와 정합 (factor ≤ 1.03).
  - Cherry-pick 부분: (a) σ_log(a₀)=0.006 dex 통계오차만 사용해 K_R2 통과 — 시스테매틱 0.06 dex 포함 시 K_R2는 정보 없음. (b) standard-mu 결과는 보고하지 않고 M16만으로 ΔAICc(SQT-McGaugh)=−56 보고. (c) BTFR과의 독립 채널 주장은 V_flat 정의 시스테매틱.
- **권장 재격상 등급**: PASS_MODERATE (5/5 → 3/7, M16 한정에서만 PASS).

## 8. 추가 작업 권장
1. Bayesian per-galaxy Υ marginalization (Li+18 방식) — Υ를 nuisance로 두고 a₀ 사후분포.
2. hi_class / RC + lensing joint fit으로 a₀-Υ 디제너러시 분리.
3. K_R2를 systematic-inflated σ로 재정의 (0.06 dex floor) — 정보를 얻는 K가 되도록.
4. L448 V_flat 정의를 "outermost RAR fit" 으로 바꾸어 재계산하면 1.53→0.86으로 떨어져 SQT와 0.16 dex 차이 → 이미 알려진 Υ scan 영역.

---

**한 줄 보고**: L482 PASS_STRONG 5/5는 *수치적으로는 진짜*이지만 *해석적으로는 functional-form-한정 + 시스테매틱 무시*에 의존 — 격상 등급 **PASS_MODERATE** 권장.
