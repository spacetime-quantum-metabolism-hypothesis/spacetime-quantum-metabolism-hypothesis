# L327 — NEXT STEP

## 즉시 (논문 본문)
1. ΔAICc=99 옆 *반드시* 다음 caveat 두 줄 추가:
   - (a) "Anchor χ² is dominated (~98%) by the cluster regime (A1689)."
   - (b) "Under Tukey-biweight robust loss (cluster treated as outlier), ΔAICc collapses to ≈ 4.85."
2. Inflation table (f=1/2/5/10 ΔAICc=97/20/−2/−5) 를 supplementary 에 부록.
3. f_crit (=2.53 for ΔAICc=10) 를 *quantitative robustness statement* 로 본문 명시.

## 단기 (L328~L330 후속)
- **L328**: 추가 cluster anchor 수집 (Coma A1656, Perseus A426, Virgo).
  단일 anchor → 4-anchor 로 single-source dominance 해소. 같은 universal a0
  로 fit 했을 때 LCDM 의 individual cluster χ² 분포 확인.
- **L329**: SPARC × cluster joint posterior (BB 3-regime full MCMC) — anchor
  weight 를 데이터에서 학습. 현재는 anchor 가 "δ-function prior".
- **L330**: σ_cluster mis-estimation 을 marginalize — hierarchical model 에서
  σ_cluster 자체를 nuisance 로 fit. ΔAICc 가 기댓값으로 어떻게 이동하는지.

## 중기
- 학계 reviewer FAQ 작성: "cluster outlier 처리" / "single-source dominance"
  / "anchor σ budget" 세 항목 정리.
- Branch B 의 진짜 evidence 는 *cluster regime ≠ SPARC regime* 라는 1-bit 신호.
  논문 abstract 도 이 1-bit 에 정직하게 정렬.

## 회피 해소 상태
- L208 회피 ("anchor by-construction"): 정량 공격 → 인플레이션 f≤2 robust, f≥5 fail.
- 새 회피 발견: **single-source (cluster) dominance** — L328 신규 anchor 필수.
