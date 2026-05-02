# L335 — NEXT STEP

## 즉시 (논문 본문)
1. Sec 5 (cluster anchor expansion priority) 에 본 forecast 표 1줄 추가:
   - "13-cluster candidate pool, 7 with full 3-probe + equilibrium-clean access."
   - "Forecast: realistic mode N=10 Tukey ΔAICc≈130, PR=0.40 (single-source dominance 해소)."
2. Sec 6 limitations: "Forecast 는 mode 가정 의존 — pessimistic mode (A1689 가
   유일한 outlier) 에서는 N 확장으로도 회복 어려움" 명시.
3. Supplementary: 13-cluster candidate table + 가용 archive (LoCuSS/CLASH/PSZ2).

## 단기 (L336~L340)
- **L336**: LoCuSS / CLASH archive 에서 lensing convergence profile 추출.
  4-cluster pilot (A1689, A2029, A1835, RXJ1347) → individual a0_eq 추정.
- **L337**: Chandra ACCEPT + REXCESS X-ray hydrostatic mass profiles 결합.
  Joint lensing + X-ray σ_cluster (cluster 별).
- **L338**: Planck PSZ2 + ACT-DR5 SZ pressure profiles 추가. 3-probe joint.
- **L339**: 7-cluster (eq-clean ∩ 3-probe) joint MCMC. universality 가설
  (single a0) vs cluster-specific (7 a0) Bayes factor.
- **L340**: ΔAICc / Tukey / PR 실측. mode 판정 (realistic / universal / pessimistic).

## 중기 (L341+)
- 실효 N_eff (mass bias + non-equilibrium contamination 후) 정량.
- universality 부분만 PASS 면 BB cluster regime 을 *cluster-class-conditional*
  로 reformulate (e.g. relaxed vs disturbed 분리).
- L327 caveat 업데이트: "Single-source dominance resolved with N_eff = X"
  명시.

## 회피 해소 상태
- L327 회피 ("cluster A1689 single-source 98%"): forecast path 명확화.
  *해소 보장 X — 실측 필요*.
- L331 honest limitation #8 ("Cluster anchor single-source"):
  L340 실측 후 RESOLVED / RETAINED / DOWNGRADED 셋 중 하나로 갱신.

## 데이터 archive 즉시 접근 경로
- LoCuSS: https://www.sr.bham.ac.uk/locuss/
- CLASH: https://archive.stsci.edu/prepds/clash/
- ACCEPT: http://www.pa.msu.edu/astro/MC2/accept/
- Planck PSZ2: https://pla.esac.esa.int/
- ACT-DR5: https://lambda.gsfc.nasa.gov/product/act/
- SPT-3G: https://pole.uchicago.edu/public/data/

## Honest open
- forecast 만으로 ΔAICc=99 robustness 단정 불가.
- pessimistic mode 가 진실이면 BB 우위는 본질적으로 1-cluster 신호 → ★ 격하.
- realistic / universal 이면 ΔAICc 신호 안정 + ★ 회복 +0.02 가능.
