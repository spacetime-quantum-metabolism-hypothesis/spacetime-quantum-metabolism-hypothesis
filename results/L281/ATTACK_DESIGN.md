# L281 — BB vs smooth full marginalized evidence

## 8인 공격
A1: Fixed-θ ΔlnZ vs marginalized ΔlnZ — Occam penalty 정확?
A2: Nested sampling (dynesty) implementation.
A3: Smooth quadratic 5 params vs BB 3 params — dimensionality penalty.
A4: Prior volume ratio.
A5: Bayes factor robustness.
A6: Stopping criterion convergence.
A7: Multimodal posterior mode count.
A8: ln Z 1-σ uncertainty.

## Top 3
A1, A3, A5.

## 권고
Dynesty nested sampling, 1000 live points, BB vs smooth 5-poly. lnZ_BB - lnZ_smooth.
