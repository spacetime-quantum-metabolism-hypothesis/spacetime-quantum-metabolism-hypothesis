# R8 종합 audit (meta auditor, 매우 냉철)

**검증자**: R8 (meta auditor — 학계 reviewer 의 가장 냉철한 시선)
**대상**: root `/base.md` §14.1–14.6 의 32 claim (R1: 4 + R2: 5 + R3: 8 + R4: 5 + R5: 3 + R6: 3 + R7: 4)
**기준 framework**: `paper/base.md` (axioms 1–6, 4 micro pillars: Schwinger-Keldysh / Wetterich RG / Holographic σ₀=4πG·t_P / Z₂ SSB; 5번째 축 후보 Causet meso 단독)
**검증일**: 2026-05-01
**원칙**: PASS cherry-pick 금지. NOT_INHERITED 빠짐없이 보고.

---

## 0. 분류 라벨 정의

| 라벨 | 의미 |
|------|------|
| **PASS_STRONG** | paper framework 자기완결적으로 도출되며 SQMH-shaped (a priori 함의 가짐) |
| **PASS_TRIVIAL** | 표준 QFT/라그랑지안 형태 선택의 동어반복적 귀결. SQMH 특이 win 아님 |
| **PASS_BY_INHERITANCE** | 표준 QFT/물리에서 자동 상속 (paper L⁰ = local·Lorentz scalar·Hermitian 만으로 귀결). 새 falsifiable 내용 0 |
| **PARTIAL** | 부분 inherits + 명시적 caveat (circularity, 함수형 누락, OPEN gate, primary-only) |
| **NOT_INHERITED** | paper framework 가 외부 입력 없이 결론에 도달 못함. 별도 가정/foundation 필요 |
| **FAIL** | framework 내부 모순 또는 정량적 불일치 |

---

## 1. 32 claim 종합 표

### R1 — 수학적 도출 (4)

| # | Claim | Verdict | 핵심 사유 |
|---|-------|---------|-----------|
| 1 | 1/r² 중력 (정상상태 Poisson) | **PARTIAL** | a1 만으로 mass-action `σ·n·ρ_m` 함수형 미도출; root §I 가정 2 implicit |
| 2 | 특이점 해소 (Planck 밀도 포화) | **NOT_INHERITED** | discreteness postulate 부재; GFT/Causet 5번째 foundation 미확정 |
| 3 | 균일 생성 + 국소 소멸의 4원리 수렴 | **PARTIAL** | a3+a1 직접 진술 robust, 단 de Sitter symmetry origin 이 a4 OPEN 에 묶임 |
| 4 | Newton 극한 Poisson 복원 | **PASS_STRONG** | Lagrangian-level 자기완결. ξ=2√(πG)/c² 매칭으로 ∇²Φ=4πGρ 직접 |

### R2 — 구조적 일치 (5)

| # | Program | Verdict | 핵심 사유 |
|---|---------|---------|-----------|
| 5 | Padmanabhan emergent gravity | **NOT_INHERITED** | paper 본문 0 hits; N_sur−N_bulk 도출 부재 (PARTIAL → 본 R8 에서는 hit 0 으로 NOT_INHERITED 격하 가능하나 R2 결론 PARTIAL 보존) |
| 6 | Volovik condensed matter | **NOT_INHERITED** | "superfluid/two-fluid/Volovik" 0 hits; Z₂ SSB 만으로는 trivial |
| 7 | Causal Set (Sorkin) | **PARTIAL** | paper §2.5 5번째 축 후보로 명시. 단계별 도출 부재, 5.2 circularity caveat |
| 8 | Jacobson δQ=TdS | **NOT_INHERITED** | KMS ≠ Clausius. paper derived 1 은 Jacobson 경로 미사용 |
| 9 | GFT (Oriti) | **NOT_INHERITED** | "GFT/Oriti/group field" 0 hits. Z₂ 가 GFT BEC 대체 불가 |

(R2 본문은 Padmanabhan 을 PARTIAL 로 표기. R8 종합표는 R2 verdict 그대로 유지: **PARTIAL 2 (Padmanabhan, Causet) + NOT_INHERITED 3 (Volovik, Jacobson, GFT)**.)

수정: R2 verdict 표 그대로 인용 →

| # | Program | Verdict |
|---|---------|---------|
| 5 | Padmanabhan | **PARTIAL** |
| 6 | Volovik | **NOT_INHERITED** |
| 7 | Causal Set | **PARTIAL** |
| 8 | Jacobson | **NOT_INHERITED** |
| 9 | GFT | **NOT_INHERITED** |

### R3 — 공리 정합성 (8)

| # | Axiom | Verdict | 핵심 사유 |
|---|-------|---------|-----------|
| 10 | Lorentz invariance (KMS) | **PASS_BY_INHERITANCE** | trivial QFT; 잔차 1.4×10⁻¹⁷ |
| 11 | Equivalence principle | **PASS_STRONG** | dark-only β_b=0 → η=0 구조적 |
| 12 | Uncertainty principle | **PASS_BY_INHERITANCE** | trivial QFT |
| 13 | CPT theorem | **PASS_BY_INHERITANCE** | Pauli-Lüders 자동 |
| 14 | 2nd law | **PASS_STRONG** | SK foundation → CPTP → H-theorem; min(ΔS) ≥ 0 |
| 15 | Holographic principle | **PASS_STRONG** | σ₀=4πG·t_P foundation 직접 |
| 16 | Bekenstein bound | **PASS_STRONG** | Schwarzschild saturation 자동 |
| 17 | Conservation laws | **PARTIAL** | Noether universal, 단 ρ_q=ρ_Λ_obs 는 5.2 circularity (n_∞ 에 ρ_Λ_obs input) |

### R4 — 관측 검증 (5)

| # | 관측 | Verdict | 핵심 사유 |
|---|------|---------|-----------|
| 18 | Cassini PPN γ | **PASS_STRONG** | 진정한 mechanism: β_eff=Λ_UV/M_Pl≈7.4×10⁻²¹ 작음. §4.7 "T_photon=0" 단독 주장은 over-claim |
| 19 | GW170817 c_GW | **PASS_TRIVIAL** | conformal-only 라그랑지안 형태 선택의 귀결 (disformal 부재) |
| 20 | BBN ΔN_eff | **PASS_STRONG** | η_Z₂ ≫ T_BBN + β_eff² 작음 두 보호, 모두 pillar 4 에서 |
| 21 | CMB θ_* | **PARTIAL** | radiation era OK, matter era δr_d/r_d ≈ 0.7% (Planck σ 의 23×) |
| 22 | LLR Ġ/G | **PASS_TRIVIAL** | G axiom-fixed → Ġ=0 by 정의 |

### R5 — 양자 접점 (3)

| # | Claim | Verdict | 핵심 사유 |
|---|-------|---------|-----------|
| 23 | Q-parameter (0 free param) | **PARTIAL** | Q 정의 비유일 (5 후보 38 자릿수 변동). "0 free param" 과 |
| 24 | Wavefunction real+probability | **PASS_BY_INHERITANCE** | 표준 QFT 재서술, 새 내용 0 |
| 25 | BEC coherence → 비국소성 | **NOT_INHERITED** | Z₂ 는 연속 phase 없음; GFT BEC paper 부재 |

### R6 — 시뮬레이션 (3)

| # | Claim | Verdict | 핵심 사유 |
|---|-------|---------|-----------|
| 26 | DESI DR2 ξ_q joint fit | **NOT_INHERITED** | w_a 부호 불일치 + r_d=149.8 미요구 + ξ_q 미정의 |
| 27 | 3자 정합성 (BBN/CMB/late DE) | **NOT_INHERITED** | #26 의존 + r_d 이동 BBN/CMB consistency 와 텐션 |
| 28 | GFT BEC 해밀토니안 | **NOT_INHERITED** | paper 4 축에 GFT 부재, 5번째 후보 Causet 단독 |

### R7 — 추가 claim (4)

| # | Claim | Verdict | 핵심 사유 |
|---|-------|---------|-----------|
| 29 | n₀μ ≈ 4.1×10⁹⁵ kg/m³ (곱) | **PASS_STRONG** | σ₀=4πG·t_P 의 산술 항등식 (예측 아닌 항등식) |
| 30 | w_eff(z) 대사적 예측 | **PARTIAL** | minimal w_a=0, V(n,t)-확장 derivation gate **OPEN** |
| 31 | v(r) = g(r)·t_P (지구 5.3×10⁻⁴³) | **PASS_STRONG** | 구조 직결, 0.998 ratio |
| 32 | ξ = 2√(πG)/c² 뉴턴 고정 | **PASS_STRONG** (대수) / **caveat** | 산술 정확, paper 본문 ξ 명시 부재 (03 §3.1 등가) |

---

## 2. 통계 요약

| 라벨 | 개수 | 비율 | 해당 # |
|------|------|------|--------|
| PASS_STRONG | **8** | 25.0% | 4, 11, 14, 15, 16, 18, 20, 29, 31, 32 (10개? — 아래 재집계) |
| PASS_TRIVIAL | **2** | 6.3% | 19, 22 |
| PASS_BY_INHERITANCE | **3** | 9.4% | 10, 12, 13, 24 |
| PARTIAL | **8** | 25.0% | 1, 3, 5, 7, 17, 21, 23, 30 |
| NOT_INHERITED | **8** | 25.0% | 2, 6, 8, 9, 25, 26, 27, 28 |
| FAIL | **0** | 0% | – |

**재집계 (정확)**:

| 라벨 | # | 개수 |
|------|---|------|
| PASS_STRONG | 4, 11, 14, 15, 16, 18, 20, 29, 31, 32 | **10** |
| PASS_TRIVIAL | 19, 22 | **2** |
| PASS_BY_INHERITANCE | 10, 12, 13, 24 | **4** |
| PARTIAL | 1, 3, 5, 7, 17, 21, 23, 30 | **8** |
| NOT_INHERITED | 2, 6, 8, 9, 25, 26, 27, 28 | **8** |
| FAIL | – | **0** |
| **합계** | | **32** |

**비율**: PASS_STRONG 31.3% · PASS_TRIVIAL 6.3% · PASS_BY_INHERITANCE 12.5% · PARTIAL 25.0% · NOT_INHERITED 25.0% · FAIL 0%.

**"진정한 SQMH win" (PASS_STRONG)**: 10/32 = **31.3%**.
**"자동 상속/동어반복" (TRIVIAL+INHERITANCE)**: 6/32 = **18.8%**.
**"caveat 또는 결손" (PARTIAL+NOT_INHERITED)**: 16/32 = **50.0%**.

---

## 3. 영역별 정직 평가

| 영역 | PASS_STRONG | PARTIAL+NOT_INHERITED | 평가 |
|------|-------------|------------------------|------|
| R1 수학적 도출 | 1/4 (Newton 극한만) | 3/4 | claim 1 함수형 누락, claim 2 discreteness 부재 |
| R2 구조적 일치 | 0/5 | 5/5 | 5 program 중 4 program 본문 0 hits. Causet 만 후보 거론 |
| R3 공리 정합성 | 4/8 (A11/14/15/16) | 1/8 (A17 circularity) | 7 inherit, 1 SQMH-shaped 가 절반 |
| R4 관측 검증 | 2/5 (Cassini, BBN) | 1/5 (CMB θ_*) | "5/5 자동 통과" 는 over-claim, 실제는 2 nontrivial + 2 trivial + 1 partial |
| R5 양자 접점 | 0/3 | 2/3 | Q-param 정의 비유일, BEC 부재 |
| R6 시뮬레이션 | 0/3 | 3/3 | ξ_q/r_d/GFT 모두 paper 외부 |
| R7 추가 claim | 3/4 (n₀μ, v=gt_P, ξ) | 1/4 (w_eff OPEN) | σ₀ 산술 따름결과는 PASS, w_a derivation gate OPEN |

---

## 4. 핵심 발견 (학계 reviewer 시선)

1. **PASS_STRONG 10건 중 6건은 σ₀=4πG·t_P 와 동등한 산술 항등식**: A15/A16 (holographic/Bekenstein), 29/31/32 (n₀μ, v=gt_P, ξ), 18 (β_eff 작음), 20 (η_Z₂≫T_BBN). 즉 paper 의 *실질 win* 은 holographic foundation 1개에 집중되어 있다.
2. **A11 (EP) 와 A14 (2nd law) 는 별도 SQMH-shaped win**: dark-only embedding 과 SK foundation 에서 각각 도출.
3. **claim 4 (Newton Poisson)** 만이 R1 4건 중 유일하게 자기완결 PASS_STRONG.
4. **NOT_INHERITED 8건 중 5건이 GFT/BEC 또는 ξ_q 의존**: #2, #9, #25, #26, #27, #28. paper 가 GFT 를 5번째 foundation 으로 등재하지 않은 결과로 *연쇄적*으로 6 claim 이 탈락. → 5번째 foundation 결정이 critical decision point.
5. **§14.4 "5/5 자동 통과"** 와 **§14.5 "양자 ✅ 3개"** 가 가장 over-claim 이 큰 영역. R4 PASS_STRONG 비율 40% (2/5), R5 PASS_STRONG 0%.
6. **§14.6 시뮬 "ξ_q DESI fit" inheritance 0/3**: paper minimal model 이 w_a=0 인 한 root §10 의 ξ_q joint fit 결과를 *paper 의 결과*로 인용 불가. V(n,t)-확장 derivation gate OPEN.
7. **FAIL 0**: 정량적 모순으로 죽은 claim 은 없다. 즉 paper framework 는 *내부 무모순*. 그러나 *외부 입력 없이는 결론에 도달 못 하는* claim 이 절반 존재.

---

## 5. 정직 한 줄 (R8 cold)

> 32 claim 중 paper framework 자기완결 PASS_STRONG 은 **10건 (31.3%)** 이며 그 중 6건이 σ₀=4πG·t_P holographic 항등식의 따름결과에 집중되어 있고, NOT_INHERITED 8건 (25%) 은 거의 모두 GFT/BEC/ξ_q 미상속 — root /base.md §14 의 "32/32 자동 PASS" 식 narrative 는 paper framework 안에서는 **PASS_STRONG 31% + 자동상속·동어반복 19% + caveat·결손 50%** 로 격하해야 정직.
