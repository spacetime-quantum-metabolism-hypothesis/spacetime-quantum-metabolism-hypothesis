# L397 — Attack Design (F1–F9 actual generation script outline + caption)

## 목적
L318 에서 확정한 9 essential figures spec 을 받아, **실제 생성 스크립트 outline**
(파일 경로, 입력 데이터 source, 함수 signature, 출력 PDF/PNG 경로) 와
**최종 JCAP caption draft** 를 한 곳에 묶는다. 본 loop 는 spec → 실행 단계
사이의 bridge 이며, 실제 PDF rendering 은 별도 long-running session 에서 수행.

## 방향 (지도 아님)
- L318 spec 변경 금지. 색맹/단위/재현성 규약 그대로 승계.
- 각 figure 마다 (a) input source 경로, (b) script outline (의사코드), (c) caption final draft 3종 세트.
- caption 은 JCAP 스타일: 1–2 문장 핵심 + "[Source: ...]" 태그 + 지지/기각 statement.
- 데이터 결손 figure 는 "needs upstream pipeline (Lxxx)" 명시 — 거짓 source 금지.
- script outline 은 함수 signature + 의존성만. 실제 matplotlib 코드 본문 금지 (지도).

---

## F1 — σ_0(env) 3-regime
- **input**:
  - `results/L1xx/sigma0_galactic.json` (TBD aggregator, 없을 가능성 높음)
  - `results/L1xx/sigma0_cluster.json`
  - `results/L1xx/sigma0_void.json`
  - 이론 band: `paper/theory/sigma0_prediction.json` (n₀μ, t_P 로부터 계산)
- **script outline**: `paper/figures/fig1_sigma0_env.py`
  - load 3 JSON → mean ± 1σ
  - errorbar(x=[0,1,2], y=σ_0, yerr=...) + axhspan(이론 band)
  - log-y, Wong palette idx 0/2/4
  - savefig PDF + PNG @ 300 dpi, 86 mm width
- **caption (final draft)**:
  > **Figure 1.** Environment dependence of the SQMH coupling σ_0 measured in
  > three regimes (galactic disks, cluster cores, cosmic voids). Error bars are
  > 1σ statistical; the horizontal band is the SQMH universal-constant
  > prediction σ_0 = 4π G t_P. Consistency across regimes within 1σ supports
  > the universality axiom; deviation > 3σ in any bin would falsify it.
  > [Source: results/L319 (aggregator), script: paper/figures/fig1_sigma0_env.py]
- **status**: BLOCKED — L319 σ_0(env) aggregation pipeline 선행 필요.

## F2 — SPARC fit examples (3 galaxies)
- **input**:
  - SPARC 공식 (`Lelli+2016`) rotation curve files for 3 selected galaxies (LSB / mid / HSB 대표).
  - `results/L1xx/sparc_fits/{NAME}.json` (SQMH best-fit + MOND + Newton baryon)
- **script outline**: `paper/figures/fig2_sparc.py`
  - 1×3 subplot, sharey=False
  - per panel: errorbar(R, V_obs, V_err) + plot(SQMH solid) + plot(MOND dashed) + plot(Newton dotted)
  - axis: x=R [kpc], y=V [km/s]
  - linestyle 차이로 grayscale 안전 보장
- **caption (final draft)**:
  > **Figure 2.** Rotation-curve fits for three SPARC galaxies spanning the
  > surface-brightness range (LSB, intermediate, HSB). Solid: SQMH; dashed:
  > MOND with a₀ = 1.2×10⁻¹⁰ m s⁻²; dotted: Newtonian baryons only. Galaxy
  > selection is by representative SB only and reported reduced χ² are not
  > used to claim model preference here; see Table 4 for full sample.
  > [Source: results/L1xx/sparc_fits, script: paper/figures/fig2_sparc.py]

## F3 — a_0 = c·H_0/(2π) derivation
- **input**:
  - SQMH derivation: `paper/theory/a0_prediction.py` (numeric value from H_0)
  - measured a_0: McGaugh+2016, Lelli+2017 (literature compilation), `paper/data/a0_lit.csv`
- **script outline**: `paper/figures/fig3_a0.py`
  - errorbar over 3–4 literature determinations
  - axhline + axhspan: SQMH prediction with Planck H_0=67.4 vs SH0ES H_0=73.0 두 band
  - y = a_0 [m s⁻²], linear scale
- **caption (final draft)**:
  > **Figure 3.** Comparison of the empirical MOND-like acceleration scale a₀
  > with the SQMH **derivation** a₀ = c H₀/(2π). The two horizontal bands
  > correspond to Planck (H₀ = 67.4) and SH0ES (H₀ = 73.0) inputs. This is
  > a parameter-free prediction, not a fit; agreement at the 1σ level closes
  > the MOND coincidence at the cost of inheriting the H₀ tension band-width.
  > [Source: paper/data/a0_lit.csv, script: paper/figures/fig3_a0.py]

## F4 — Cluster mass profile
- **input**:
  - Coma OR A1689 lensing+X-ray profile (literature, e.g. Umetsu+2016)
  - `results/L1xx/cluster_{NAME}.json` (SQMH M(<r), NFW best-fit)
- **script outline**: `paper/figures/fig4_cluster.py`
  - log-log plot, M(<r) vs r
  - errorbar (lensing) + line (SQMH solid, NFW dashed)
- **caption (final draft)**:
  > **Figure 4.** Enclosed mass profile of {cluster} from joint lensing + X-ray.
  > SQMH (solid) reproduces the profile with σ_0 fixed to its galactic value;
  > NFW (dashed) shown for reference. Outer-radius (>R₂₀₀) extrapolation is
  > model-dependent and excluded from the fit window (shaded).
  > [Source: results/L1xx/cluster_{NAME}.json, script: paper/figures/fig4_cluster.py]

## F5 — ρ_q evolution Bianchi (L207)
- **input**:
  - `results/L207/report.json` (background ρ_q(z) under Bianchi I shear σ/H ∈ {0, 0.01, 0.05})
  - `results/L207/L207.png` 재가공이 아닌 **report.json 재플롯**
- **script outline**: `paper/figures/fig5_rhoq_bianchi.py`
  - log-log: x = 1+z, y = ρ_q/ρ_q0
  - 3 lines (3 shear levels), linestyle 차이
- **caption (final draft)**:
  > **Figure 5.** SQMH metabolic density ρ_q(z) on a Bianchi-I anisotropic
  > background for three shear levels σ/H ∈ {0, 10⁻², 5×10⁻²}. The σ/H = 0
  > line coincides with the FLRW reference. Shear levels chosen to bracket
  > current CMB anisotropy bounds (σ/H ≲ 10⁻⁹ at last scattering, weakening
  > to ≲ 10⁻² at z ≲ 1).
  > [Source: results/L207/report.json, script: paper/figures/fig5_rhoq_bianchi.py]

## F6 — Hierarchical GMM (L273)
- **input**: `results/L273/report.json` (per-cluster posteriors + hyperparameters)
- **script outline**: `paper/figures/fig6_gmm.py`
  - per-cluster KDE/violin (x=σ_0, vertical violins side-by-side)
  - global posterior overlay (filled curve at top axis)
- **caption (final draft)**:
  > **Figure 6.** Hierarchical Gaussian-mixture posterior on σ_0 across N
  > galaxy clusters. Per-cluster KDEs (Wong palette) and the global
  > hyper-posterior (top, shaded) test whether σ_0 is universal (single-peak
  > global) or environment-dependent (multi-modal). Multimodality > 3σ would
  > falsify the universality axiom.
  > [Source: results/L273/report.json, script: paper/figures/fig6_gmm.py]

## F7 — Mock injection (L272)
- **input**: `results/L272/report.json` (injected vs recovered parameters)
- **script outline**: `paper/figures/fig7_injection.py`
  - scatter (true, recovered) + 1:1 line + ±1σ recovery band
  - residual subplot (bottom) optional
- **caption (final draft)**:
  > **Figure 7.** Injection–recovery test of the SQMH parameter pipeline on
  > N mock realizations. Diagonal: 1:1 line; shaded band: ±1σ recovery
  > scatter. Bias < 1σ across the full prior range demonstrates the
  > pipeline introduces no systematic preference and the posteriors in
  > Figs. 1, 6 are not artefacts of the inference machinery.
  > [Source: results/L272/report.json, script: paper/figures/fig7_injection.py]

## F8 — IC 4종 비교 bar
- **input**: `results/L1xx/ic_summary.json` (AIC, AICc, BIC, DIC for SQMH/LCDM/MOND/wCDM, joint dataset)
- **script outline**: `paper/figures/fig8_ic_bar.py`
  - grouped bar: 4 IC × 4 model, ΔIC vs best-of-row
  - hatch pattern per IC (grayscale safe)
  - axhline at ΔIC = 2, 6, 10
  - footnote: SQMH free-param count k explicit
- **caption (final draft)**:
  > **Figure 8.** Information-criterion comparison (AIC, AICc, BIC, DIC) for
  > SQMH against ΛCDM, MOND, and wCDM on the joint dataset (BAO + SN +
  > CMB-compressed + RSD + SPARC). Bars show ΔIC relative to the best
  > model per criterion; reference lines mark the conventional ΔIC = 2/6/10
  > thresholds. AICc penalty uses k_SQMH = {N} explicit free parameters
  > (footnote).
  > [Source: results/L1xx/ic_summary.json, script: paper/figures/fig8_ic_bar.py]
- **status**: BLOCKED — IC aggregator (joint dataset 동일 likelihood 평가) 미존재.

## F9 — Facility forecast P15–P22
- **input**:
  - `paper/data/forecast_etc.json` (per-facility 1σ from public ETC: DESI DR3, Euclid Red Book, LSST SRD, SKA1-MID Phase B, CMB-S4 DSR)
  - SQMH 예측 중심값: `paper/theory/predictions.json` (P15..P22)
- **script outline**: `paper/figures/fig9_forecast.py`
  - x = prediction id (categorical, P15..P22)
  - y = SQMH central value (normalized to LCDM=1 or absolute, per prediction)
  - errorbar per facility, marker 차이, dodge x position
  - legend = facilities
- **caption (final draft)**:
  > **Figure 9.** Forecast 1σ sensitivity to the eight SQMH falsifiable
  > predictions P15–P22 from upcoming facilities (DESI DR3, Euclid, LSST
  > Y10, SKA1-MID, CMB-S4). Central values are SQMH posterior medians;
  > error bars are **approximate** projections from public ETC documents
  > (citations in caption). Crossings of the y = ΛCDM reference indicate
  > facility-level falsifiability windows.
  > [Source: paper/data/forecast_etc.json, script: paper/figures/fig9_forecast.py]

---

## 데이터 source 요약 (L318 follow-up)

| Fig | 입력 source | 상태 | upstream blocker |
|-----|------------|------|------------------|
| F1  | L319 σ_0(env) aggregator | **MISSING** | L319 pipeline build 필요 |
| F2  | SPARC raw + L1xx fits | partial | sparc_fits/ 표준화 |
| F3  | lit a_0 + theory deriv | OK | — |
| F4  | cluster lensing + L1xx fit | partial | cluster_{NAME}.json 표준화 |
| F5  | results/L207/report.json | **OK** | — |
| F6  | results/L273/report.json | **OK** | — |
| F7  | results/L272/report.json | **OK** | — |
| F8  | L1xx ic_summary.json | **MISSING** | joint IC aggregator 필요 |
| F9  | forecast_etc.json + predictions.json | partial | ETC 수기 입력 |

## 재현성 규약 (L318 승계)
1. 스크립트 경로 `paper/figures/figN_*.py` 고정.
2. 입력 의존은 `report.json` / `paper/data/*.json` 만. raw 재실행 금지.
3. caption 끝 `[Source: ..., script: ...]` 강제.
4. `np.random.seed(42)`, git hash footnote.
5. `make figures && make paper` 빌드.

## 위험
- F1, F8 두 figure 가 upstream 데이터 부재로 즉시 생성 불가 — paper 제출 전 L319 / IC aggregator 별도 loop 필수.
- F9 ETC 1σ 가 "approximate" 명시 의무 — peer review 에서 challenge 예상.
- caption 의 falsifiability statement (지지/기각 명시) 가 reviewer 에게 over-claim 으로 비칠 수 있음 — Limitations 섹션과 cross-ref 필수.

## 정직 한 줄
본 loop 는 9 figure 의 script outline + caption draft 만 산출했으며 실제 PDF/PNG 렌더링과 F1·F8 의 upstream 데이터 aggregator 는 미수행이다.
