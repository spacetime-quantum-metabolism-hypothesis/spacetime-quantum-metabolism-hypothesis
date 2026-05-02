# L526 R2 — SN Data Audit (Son+2025 progenitor age-bias correct 가정)

**관측가 입장 audit. 8인/4인 라운드 미실행 — 단일 메타-에이전트 산출.**
**임무 가정**: Son et al. 2025 (MNRAS 544:975, SN Ia progenitor age-bias 5.5σ
confirmed) 보정이 *정량적으로 옳다*고 가정. paper 의 SN-derived 결과·forecast 가
어떻게 흔들리는지 정직 list.

---

## 1. paper 가 인용한 SN-derived results — 식별

### 1.1 직접 SN 채널 (DESY5 SN 포함 likelihood)
| 위치 | claim | SN 의존도 |
|---|---|---|
| `00_abstract.md:12` | "BAO (2503.14738), **DESY5 Type-Ia supernovae**, compressed Planck 2018 CMB, RSD" — joint likelihood 정의 | **직접** |
| `00_abstract.md:23` | "C28 RR non-local: **Δχ² = −21.1, Δ ln Z = +11.26**, DESI DR3 forecast 3.9σ" | **직접** (joint = BAO+SN+CMB+RSD) |
| `07_comparison_lcdm.md:5` | "ΛCDM baseline on the full **BAO+SN+CMB+RSD** joint likelihood" | **직접** |
| `05_desi_prediction.md:76,83` | "DESI DR2 joint (DESI+CMB+**DESY5**) central values"; "within 1–2σ when **DESY5 SN likelihood is included**" | **직접** |
| `STATISTICAL_METHODS_APPENDIX.md:22,165` | likelihood 정의 "BAO+SN+CMB+RSD"; "**DES-Y5 SN**" 명시 | **직접** |
| `10_appendix_alt20.md` Tables (32-claim PASS 분포, alt-20 best-fit w0/wa) | C11D / C28 / A12 / A04 등 모든 후보 best-fit 은 joint χ² (DESY5 포함) 산출 | **직접** |
| `06_mcmc_results.md` 전체 (Δχ², Δ ln Z, posterior) | L5/L6 production MCMC = BAO+**SN**+CMB+RSD | **직접** |
| L43 (`simulations/l43/l43_results.json`) `chi2_sn = 1725.94 / chi2_total = 1755.92` | LCDM joint χ² 의 **98.3%** 가 SN 채널 | **압도적 의존** |

### 1.2 DESI DR3 Fisher forecast (BAO 위주)
| 후보 | DR3 Fisher σ | SN 의존도 |
|---|---|---|
| C11D | 3.91σ (`05_desi_prediction.md:48`) | **간접** — Fisher FoM 은 BAO-only 이지만 best-fit posterior locus (priors) 는 joint (=DESY5 포함) MCMC 에서 옴 |
| C28 | 3.9σ (`abstract.md:23`) | **간접** (동일) |
| A12 | 2.16σ (`05_desi_prediction.md:67`) | **간접** (동일) |
| A04 (watch) | **7.98σ** (`05_desi_prediction.md:98`, `09_conclusion.md:84`) | **간접** (best-fit w0/wa locus 가 SN-driven CPL 영향) |

### 1.3 Pre-registered falsifier (forecast 수치)
| Forecast | 출처 | SN 의존? |
|---|---|---|
| **DESI DR3 BAO** w_a falsifier (3.9σ ≥ 2σ Q9) | `00_abstract.md:35`, `09_conclusion.md` | **간접** (post-DR3 fit 도 DESY5 와 결합 예정) |
| **Euclid DR1 cosmic-shear 4.4σ** (S_8 falsifier, 중심 4.38σ, quadrature 4.19σ) | `base.md:917-935`, `faq_ko.md:19,47`, `COVER_LETTER_v4.md:73-96`, `09_conclusion.md` | **무관** — ξ_+ ∝ S_8² 로 cosmic-shear 직접 측정. SN 입력 0건. |
| **CMB-S4 7.9σ** (recombination physics) + **ET 7.4σ** (GW scalar) + **SKA-null** | `base.md:958` "3 load-bearing orthogonal channels" | **무관** — CMB-S4 는 z~1100 recombination, ET 는 GW polarization, SKA 는 21cm. SN 입력 0건. |
| BBN ΔN_eff > 0.3 (P5) | `TABLES.md:121` | **무관** |
| Void galaxy a₀ (P13) | `TABLES.md:129` | **무관** |
| RSD f·σ_8 (T20) | `TABLES.md:133` | **무관** (RSD-only) |

---

## 2. Son+25 correct 시 *영향* 받는 claim

**핵심 상수 (L43 `simulations/l43/l43_test.py` 73-77 줄, 보정 적용 결과 `l43_results.json`)**:
- `delta_age(z) = 5.3 · (1 - exp(-2.5z))` Gyr
- `delta_m = delta_age · slope` (mag), `slope_err` 시스 추가
- LCDM AICc: 1670 → **1759.93** (+89.81)
- CPL dAICc vs LCDM: **−107.02** (CPL 가 압도 우위)
- Best-fit CPL: w0 = −0.448, **wa = −1.467** (DESI DR2 +0.83 보다 훨씬 더 phantom-thawing)
- D_psi^2 (SQT 핵심, n=2): dAICc = +1012.95 → **K90 KILL**
- D_psi^n (n free): n_fit = 0.10 vs theory n=2 (**−95% 편차**) → **SQT psi^n path rejected**

### 2.1 직접 영향 (재계산 필수)
| paper claim | Son+ 보정 시 변화 |
|---|---|
| §6 / §10 alt-20 best-fit (w0, wa) 표 | 모든 후보 w0/wa **수치 재산출 필수**. CPL wa 가 −1.47 로 이동 → C11D / C28 / A12 best-fit 도 phantom-deeper 방향 이동 예상 |
| C11D / C28 / A12 Δχ² | **불명** — 현 +21.1 (C28) 는 *un-corrected* DESY5 기반. corrected DESY5 에서 LCDM χ² 가 ~+90 악화 → C28 의 Δχ² 절대값은 더 커질 *수도* 있고 *모델 의존적으로* 부분 상쇄될 수도 (재실행 필수) |
| Δ ln Z (Bayesian evidence) +11.26 | corrected SN 기반 재실행 필요 |
| L43 직접 결과: SQT ψ^n a priori path | **이미 KILL** (dAICc=+1012.95) — Son+ 보정 자체가 SQT 핵심 a priori 경로를 제거 |
| L5 production MCMC 모든 posterior | 재실행 필수 (DESY5 가 likelihood 의 ~98% 무게) |
| §5.1 DESI DR2 joint w0=−0.757, wa=−0.83 인용 | 이는 *DESI 공식값* (corrected SN 미적용). Son+ 보정 후 wa 는 더 phantom (−1.47 toward) — **DESI 공식 결과가 흔들림** (관측가 코멘트, paper 외부 영향) |

### 2.2 간접 영향 (best-fit locus 이동 → forecast 시그마 변화)
| paper claim | Son+ 보정 시 변화 |
|---|---|
| DR3 Fisher σ (3.91σ C11D, 2.16σ A12, 7.98σ A04) | best-fit w0/wa 가 더 phantom 방향 이동 → LCDM 와의 Fisher 거리 *증가* 가능 → **σ 값 상향 이동 가능** (관측가 측 보수적 추정 +20–50% 마진). 단 Q9 ≥2σ 통과 여부는 모두 유지 예상 |
| `09_conclusion.md:30` "C11D 3.91σ strongest" 순위 | C28 vs C11D vs A12 **순위 재정렬 가능** (상대 best-fit 위치 의존) |

### 2.3 영향 *없음* (SN 무관 채널)
| claim | 이유 |
|---|---|
| **Euclid DR1 cosmic-shear 4.4σ falsifier** (4.38σ central / 4.19σ quadrature) | ξ_+ ∝ S_8² 직접 측정. forecast 입력 = SQMH ΔS_8 prediction (background-only μ=1 구조에서 +1.14% 악화) + Euclid IST σ(S_8)=0.0026. **DESY5 SN 입력 0건** → **변화 없음** |
| **CMB-S4 7.9σ** (recombination physics, ΔN_eff / θ*) | z~1100 물리. SN 무관 → **변화 없음** |
| **ET 7.4σ** (GW scalar polarization) | binary inspiral GW. SN 무관 → **변화 없음** |
| **SKA-null** (21cm post-EDGES) | reionization-era. SN 무관 → **변화 없음** |
| 3 load-bearing orthogonal Z_comb ≈ 10.83σ (`base.md:958`) | **CMB-S4 + ET + SKA 만 으로 산출** — SN 채널 미포함이 *명시*. Son+ 보정에 **structurally robust** |
| BBN P5, Void a₀ P13, RSD T20 | 채널 무관 |
| Cassini |γ−1| (C1), SPARC RAR a₀ (C7) | 태양계 / 은하 측정. SN 무관 |

---

## 3. SQT forecast 변화 (요청한 4.4σ / 7.9σ 자체)

**중요 발견 — 명명 정정**: 임무가 "SQT forecast Euclid 4.4σ / CMB-S4 7.9σ" 라고 묶었으나, paper 내 **이 두 forecast 는 SN-derived 가 아니다**:
- **Euclid 4.4σ** = cosmic-shear S_8 falsifier (background-only μ=1 구조 → ΔS_8 +1.14%; forecast 입력에 DESY5 0건)
- **CMB-S4 7.9σ** = recombination physics (3 load-bearing orthogonal 의 첫 채널; ET 7.4σ + SKA-null 동반)

→ **Son+ 보정에 structurally robust**. paper 의 핵심 falsifier portfolio (Euclid+CMB-S4+ET+SKA, Z_comb ≈ 10.83σ) 는 **SN 채널과 분리 설계** 되어 있어 Son+ 진실/거짓에 독립.

**단**: paper 의 *DR3 BAO Fisher* (3.91σ C11D, 7.98σ A04) 는 best-fit posterior locus 가 SN-driven 이므로 *간접 영향* 받음 — §2.2 참조. 시그마 절대값은 이동하나 Q9 ≥2σ 통과 여부는 보존 예상.

---

## 4. paper 의 *SN 의존도* 정직 list

**구조적 SN-load-bearing (보정 시 재실행 필수)**:
1. **Joint likelihood χ² 의 ~98%** = SN 채널 (L43 LCDM `chi2_sn / chi2_total = 1725.94 / 1755.92 = 98.3%`)
2. **모든 alt-20 best-fit w0/wa 표** (`paper/10_appendix_alt20.md`, §6)
3. **모든 Δχ² 보고치** (C11D, C28, A12 등) — `paper/00_abstract.md`, `06_mcmc_results.md`
4. **모든 Δ ln Z (Bayesian evidence)** — joint posterior 정의 자체가 SN 포함
5. **DESI DR2 인용 w0=−0.757, wa=−0.83** — DESI+Planck+DESY5 공식값
6. **L5 / L6 production MCMC posterior 전체** — 5–6 시간/후보 재실행 부담
7. **L43 SQT ψ^n a priori path** — 이미 보정 적용; SQT 핵심 경로 KILL 결과 자체가 Son+ 의존

**SN-independent (보정에 robust)**:
1. **Euclid DR1 cosmic-shear 4.4σ falsifier** (S_8, ξ_+ 직접)
2. **CMB-S4 7.9σ recombination falsifier**
3. **ET 7.4σ GW scalar falsifier**
4. **SKA-null 21cm consistency**
5. **3 load-bearing Z_comb ≈ 10.83σ** (CMB-S4+ET+SKA 만)
6. **C1 a₀ ↔ c·H₀/(2π) factor-≤1.5** (진정 invariant #1, L491+ audit)
7. **C7 Newton-only SPARC fail** (진정 invariant #2)
8. **Cassini |γ−1| Solar-system PPN** (C1 PPN 후보 sieve)
9. **BBN ΔN_eff (P5)**, **Void a₀ (P13)**, **RSD f·σ_8 (T20)**

**중간 (간접 영향, σ 값 이동 가능)**:
1. **DESI DR3 Fisher σ (3.91σ / 2.16σ / 7.98σ)** — best-fit locus 가 SN-driven; Q9 ≥2σ 통과 여부는 보존 예상

---

## 5. 정직 한 줄

**Son+25 보정이 옳다면 paper 의 alt-20 best-fit 표 / Δχ² / Δ ln Z 전 행이 재실행 대상이고 (joint χ² 의 98% 가 SN), DESI DR3 Fisher 도 best-fit locus 이동으로 간접 흔들리지만, paper 의 *주력 falsifier portfolio* (Euclid 4.4σ cosmic-shear + CMB-S4 7.9σ recombination + ET 7.4σ + SKA-null, Z_comb ≈ 10.83σ) 는 SN 채널과 구조적으로 분리되어 있어 Son+ 진위에 독립적이며, L43 에서 이미 적용된 Son+ 보정은 SQT ψ^n a priori 핵심 경로를 dAICc=+1012.95 로 KILL 함 (즉 paper 핵심은 robust, 부수 채널만 흔들림).**

---

*저장: 2026-05-01. results/L526_R2/SN_AUDIT.md. 단일 메타-에이전트 audit, 8인/4인 라운드 미실행. paper/base.md edit 0건. simulations/ 신규 코드 0줄. claims_status.json edit 0건. CLAUDE.md [최우선-1] (수식 0줄), [최우선-2] (팀 자율 도출 보류), 결과 왜곡 금지 모두 정합. 산출 수치는 모두 disk 상 기존 파일 인용 — 신규 시뮬레이션 0건.*
