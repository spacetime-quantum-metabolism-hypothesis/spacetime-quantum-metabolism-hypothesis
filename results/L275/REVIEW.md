# L275 — 4인 review (prior sensitivity)

시뮬 simulations/L275/run.py: 4 prior 조합 (uniform/log-uniform × narrow/wide) BB MAP shift.

## 결과
- log_σ_galactic: 9.561 ± 0.014 (prior-independent)
- log_σ_cluster: 7.748 ± 0.045 (mild prior shift, anchor weak)
- log_σ_cosmic: 8.371 ± 0.008 (anchor strong)
- max shift across priors: 0.045 dex << 0.3 dex threshold

## 4인
- P: BB 3 regime MAP prior-robust — 강력한 결과.
- N: cluster anchor 만 약간 prior-sensitive (single A1689 한 개 anchor).
- O: SPARC weight scheme 영향은 별도 검증.
- H: L208 anchor caveat 와 정합.

정직 결론: PRIOR-ROBUST, 회피 #X 부분 해소.
