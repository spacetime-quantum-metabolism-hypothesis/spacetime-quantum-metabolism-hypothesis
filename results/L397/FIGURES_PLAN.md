# L397 — FIGURES_PLAN (F1–F9 condensed master sheet)

L318 spec + L397 outline 을 한 장 표로 압축. paper figure 빌드 매니페스트로 직접 사용.

## 빌드 매니페스트

| ID | Title | Script | Inputs | Outputs | Status | Caption tag |
|----|-------|--------|--------|---------|--------|-------------|
| F1 | σ₀(env) 3-regime | `paper/figures/fig1_sigma0_env.py` | `results/L319/sigma0_{galactic,cluster,void}.json` (TBD), `paper/theory/sigma0_prediction.json` | `paper/figures/out/fig1.{pdf,png}` | **BLOCKED**: L319 aggregator | `[Source: results/L319, script: paper/figures/fig1_sigma0_env.py]` |
| F2 | SPARC fit examples | `paper/figures/fig2_sparc.py` | SPARC raw (Lelli+2016) for 3 selected, `results/L1xx/sparc_fits/{NAME}.json` | `paper/figures/out/fig2.{pdf,png}` | partial | `[Source: results/L1xx/sparc_fits, script: paper/figures/fig2_sparc.py]` |
| F3 | a₀ = c·H₀/(2π) | `paper/figures/fig3_a0.py` | `paper/data/a0_lit.csv`, `paper/theory/a0_prediction.py` | `paper/figures/out/fig3.{pdf,png}` | OK | `[Source: paper/data/a0_lit.csv, script: paper/figures/fig3_a0.py]` |
| F4 | Cluster M(<r) | `paper/figures/fig4_cluster.py` | lensing+X-ray (Umetsu+ etc.), `results/L1xx/cluster_{NAME}.json` | `paper/figures/out/fig4.{pdf,png}` | partial | `[Source: results/L1xx/cluster_{NAME}.json, script: paper/figures/fig4_cluster.py]` |
| F5 | ρ_q(z) Bianchi I | `paper/figures/fig5_rhoq_bianchi.py` | `results/L207/report.json` | `paper/figures/out/fig5.{pdf,png}` | **OK** | `[Source: results/L207/report.json, script: paper/figures/fig5_rhoq_bianchi.py]` |
| F6 | Hierarchical GMM | `paper/figures/fig6_gmm.py` | `results/L273/report.json` | `paper/figures/out/fig6.{pdf,png}` | **OK** | `[Source: results/L273/report.json, script: paper/figures/fig6_gmm.py]` |
| F7 | Mock injection | `paper/figures/fig7_injection.py` | `results/L272/report.json` | `paper/figures/out/fig7.{pdf,png}` | **OK** | `[Source: results/L272/report.json, script: paper/figures/fig7_injection.py]` |
| F8 | IC bar (4 IC × 4 model) | `paper/figures/fig8_ic_bar.py` | `results/L1xx/ic_summary.json` (TBD) | `paper/figures/out/fig8.{pdf,png}` | **BLOCKED**: IC aggregator | `[Source: results/L1xx/ic_summary.json, script: paper/figures/fig8_ic_bar.py]` |
| F9 | Forecast P15–P22 | `paper/figures/fig9_forecast.py` | `paper/data/forecast_etc.json`, `paper/theory/predictions.json` | `paper/figures/out/fig9.{pdf,png}` | partial (ETC 수기) | `[Source: paper/data/forecast_etc.json, script: paper/figures/fig9_forecast.py]` |

## 즉시 실행 가능 (Phase A)
- F5, F6, F7 — `report.json` 존재. 스크립트 작성 후 바로 빌드.

## 부분 실행 (Phase B, 입력 표준화 후)
- F2, F4, F9 — raw 데이터/문헌 값을 표준 JSON 으로 정리하는 사전 작업 1회.

## 차단 (Phase C, upstream loop 필요)
- F1 → L319 σ₀(env) aggregator pipeline.
- F8 → joint IC aggregator (BAO+SN+CMB+RSD+SPARC 동일 likelihood 평가).

## 빌드 명령
```
make figures   # paper/figures/figN_*.py 9개 일괄 실행
make paper     # TeX + figure 통합
```
- 각 스크립트는 `np.random.seed(42)`, 86 mm or 178 mm width, dpi ≥ 300, PDF + PNG dual output.
- caption 은 `paper/captions/figN.tex` 분리 파일로 관리, main.tex 에서 `\input{}`.

## 색맹 / grayscale
- palette: Wong 8-color (idx 0,1,2,4,6 권장).
- linestyle 차이: solid / dashed / dotted / dashdot 4종 사용.
- F8 grouped bar: hatch pattern (`/`, `\\`, `x`, `.`) per IC.

## 현재 진행 가능 figure 수
- 즉시 (Phase A): **3 / 9**
- 입력 정리 후 (Phase B): **+3 → 6 / 9**
- upstream blocker 해결 후 (Phase C): **+2 → 8 / 9** (F9 의 forecast ETC 까지 채우면 9/9)

## 정직 한 줄
9 figure 중 3개 (F5/F6/F7) 만 즉시 빌드 가능하며 나머지 6개는 입력 표준화 또는 upstream aggregator (L319, IC) 작업이 선행되어야 한다.
