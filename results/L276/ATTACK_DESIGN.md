# L276 — Leave-3-out CV (deferred from L255)

## 8인 공격
A1: BB ΔAICc 우위가 specific 3 anchors 빠지면 사라지나?
A2: cosmic anchor 만 빠지면? cluster 만? galactic 만?
A3: 모든 1-out subset 에서 ΔAICc>0 유지?
A4: Cross-validation predictive log-likelihood.
A5: K-fold (k=5) on SPARC subset.
A6: Stratified by halo mass.
A7: Test set unbiased estimate.
A8: NULL hypothesis: random 3-anchor placement chi^2 distribution.

## Top 3
A1, A2, A8 (null distribution).

## 권고
3 anchors 의 leave-1-out + leave-2-out 모두 수행.
모든 subset 에서 ΔAICc>0 유지면 robust.
