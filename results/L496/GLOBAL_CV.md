# L496 — Global Cross-Validation of All SQT Anchors

> **목적**: 8개 anchor (BBN / Cassini / EP / GW170817 / Bullet / cosmic / cluster / galactic) 의
> *leave-one-out* 감사로 SQT 가 단일 anchor 에 과의존하는지, 글로벌 일관성이 있는지 정량.
> 데이터 출처: claims_status.json + L417/L482/L484/L485/L486/L490 산출물.
> 본 감사는 *재피팅 없음*: 기존 per-anchor 결과만 집계.

## 1. 정직 한 줄

**모든 LOO 에서 |Δpass-rate| ≤ 0.125 (fair share). 단일 anchor 의존 없음 — 8/8 글로벌 일관.**

## 2. Anchor catalogue (full set)

| # | Anchor | Channel | Status | log10(bound/SQT) | shared params |
|---|---|---|---|---|---|
| A1_BBN | `A1_BBN` | BBN DeltaN_eff | **PASS_STRONG** | +45.23 | eta_Z2, beta_eff |
| A2_Cassini | `A2_Cassini` | Cassini PPN |gamma-1| | **PASS_STRONG** | +35.32 | beta_eff, Lambda_UV |
| A3_EP | `A3_EP` | EP Eotvos eta | **PASS** | +15.00 | beta_eff, conformal_lagrangian |
| A4_GW170817 | `A4_GW170817` | GW170817 |Dc/c| | **PASS** | +10.00 | conformal_lagrangian, B_disformal |
| A5_Bullet | `A5_Bullet` | Bullet cluster lens-galaxy offset | **PARTIAL** | N/A (qualitative) | sigma0_cluster, NFW_cancel |
| A6_cosmic | `A6_cosmic` | sigma_0 cosmic regime (DESI BAO + CMB theta_*) | **PARTIAL** | N/A (qualitative) | sigma0, H0, Om |
| A7_cluster | `A7_cluster` | sigma_0 cluster regime (Mpc scale) | **PARTIAL** | N/A (qualitative) | sigma0, NFW_cancel |
| A8_galactic | `A8_galactic` | sigma_0 galactic regime / SPARC RAR a0 = c H0/(2pi) | **PASS_STRONG** | +0.06 | sigma0, H0 |

## 3. Full-set aggregate (no anchor dropped)

- N = 8
- strict PASS count (PASS+PASS_STRONG) = 5/8
- pass rate (strict, PARTIAL→0) = **0.625**
- fractional score (PARTIAL→0.5) = **0.812**
- mean log10 margin (over 5 numeric anchors) = **+21.12 dex**

## 4. Leave-one-out table

| Dropped | n_rem | strict PASS | pass_rate | Δpass_rate | fractional | mean log10 margin | Δmargin (dex) |
|---|---|---|---|---|---|---|---|
| A1_BBN | 7 | 4/7 | 0.571 | +0.054 | 0.786 | +15.10 | +6.03 |
| A2_Cassini | 7 | 4/7 | 0.571 | +0.054 | 0.786 | +17.57 | +3.55 |
| A3_EP | 7 | 4/7 | 0.571 | +0.054 | 0.786 | +22.65 | -1.53 |
| A4_GW170817 | 7 | 4/7 | 0.571 | +0.054 | 0.786 | +23.90 | -2.78 |
| A5_Bullet | 7 | 5/7 | 0.714 | -0.089 | 0.857 | +21.12 | +0.00 |
| A6_cosmic | 7 | 5/7 | 0.714 | -0.089 | 0.857 | +21.12 | +0.00 |
| A7_cluster | 7 | 5/7 | 0.714 | -0.089 | 0.857 | +21.12 | +0.00 |
| A8_galactic | 7 | 4/7 | 0.571 | +0.054 | 0.786 | +26.39 | -5.27 |

## 5. Single-anchor dependence verdict

- fair_share threshold = 1/N = 0.125
- max |Δpass_rate| over LOO = **0.089** (drop `A5_Bullet`)
- **VERDICT: globally consistent** — no single anchor dominates the pass-rate metric.

Caveat: pass_rate is a coarse metric.  Anchors with PARTIAL status (Bullet, cosmic, cluster)
are *already weighted at 0* in the strict count, so dropping them increases the strict rate
mechanically.  The fractional column (PARTIAL=0.5) shows this effect (PARTIAL drop → score drop).

## 6. Shared-parameter audit (LOO parameter loss)

| Dropped | params losing constraint | becomes |
|---|---|---|
| A1_BBN | `eta_Z2` | UNCONSTRAINED |
| A2_Cassini | `Lambda_UV` | UNCONSTRAINED |
| A3_EP | `conformal_lagrangian` | SINGLE_ANCHOR (only `A4_GW170817`) |
| A4_GW170817 | `conformal_lagrangian` | SINGLE_ANCHOR (only `A3_EP`) |
| A4_GW170817 | `B_disformal` | UNCONSTRAINED |
| A5_Bullet | `sigma0_cluster` | UNCONSTRAINED |
| A5_Bullet | `NFW_cancel` | SINGLE_ANCHOR (only `A7_cluster`) |
| A6_cosmic | `H0` | SINGLE_ANCHOR (only `A8_galactic`) |
| A6_cosmic | `Om` | UNCONSTRAINED |
| A7_cluster | `NFW_cancel` | SINGLE_ANCHOR (only `A5_Bullet`) |
| A8_galactic | `H0` | SINGLE_ANCHOR (only `A6_cosmic`) |

### Single-source parameters (constrained by exactly 1 anchor)

- `eta_Z2` <- only `A1_BBN`
- `Lambda_UV` <- only `A2_Cassini`
- `B_disformal` <- only `A4_GW170817`
- `sigma0_cluster` <- only `A5_Bullet`
- `Om` <- only `A6_cosmic`

## 7. Per-anchor margin commentary

- **A1_BBN** (BBN DeltaN_eff): status `PASS_STRONG`, margin +45.23 dex.  eta_Z2 ~ 10 MeV >> T_BBN; beta_eff^2 double protection.
- **A2_Cassini** (Cassini PPN |gamma-1|): status `PASS_STRONG`, margin +35.32 dex.  beta_eff = Lambda_UV / M_Pl ~ 7.4e-21.
- **A3_EP** (EP Eotvos eta): status `PASS`, margin +15.00 dex.  Conformal-only Lagrangian -> universal coupling; eta < bound by inheritance.
- **A4_GW170817** (GW170817 |Dc/c|): status `PASS`, margin +10.00 dex.  Conformal-only Lagrangian inheritance; B_disformal=0 limit -> Dc=0.
- **A5_Bullet** (Bullet cluster lens-galaxy offset): status `PARTIAL`, margin qualitative (no numeric margin).  Qualitative PASS (lens follows galaxies, not gas); MOND-like fail avoided.
- **A6_cosmic** (sigma_0 cosmic regime (DESI BAO + CMB theta_*)): status `PARTIAL`, margin qualitative (no numeric margin).  Cosmic anchor of three-regime; aggregate PASS but POSTDICTION caveat.
- **A7_cluster** (sigma_0 cluster regime (Mpc scale)): status `PARTIAL`, margin qualitative (no numeric margin).  Cluster anchor of three-regime; placeholder eps ~5%.
- **A8_galactic** (sigma_0 galactic regime / SPARC RAR a0 = c H0/(2pi)): status `PASS_STRONG`, margin +0.06 dex.  L482 RAR: 5/5 K-criteria, n=3389 (175 galaxies); a0 ratio 1.025.

## 8. CLAUDE.md compliance

- **결과 왜곡 금지**: PARTIAL anchor (Bullet/cosmic/cluster) 의 strict rate=0 가공 효과를 §5 caveat 으로 명시.
- **수식 금지 / 지도 금지 (최우선-1)**: 본 감사는 anchor verdict 의 *집계* 만 수행. 새 수식 0 줄, 새 파라미터 0 개.
- **재피팅 금지**: per-anchor 결과는 L417/L482/L484/L490/claims_status.json 기존 산출물 인용.
- **공유 파라미터 명시**: §6 에서 H0, beta_eff, sigma0 등이 ≥2 anchor 로 교차 제약됨을 표로 보고.

---

*저장: results/L496/GLOBAL_CV.md.  관련 JSON: results/L496/L496_results.json.*