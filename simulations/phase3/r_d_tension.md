# Phase 3.5 A3 — r_d tension vs Planck

**Data**. DESI DR2 BAO 13pt + DESY5 SN 1829 + compressed CMB 3pt + RSD 8pt
(N = 1853). MCMC: emcee 24 walkers × 1000 steps, seed fixed.

**Planck reference**. `r_d = 147.09 ± 0.30 Mpc` (Planck 2018 TT,TE,EE+lowE+lensing, arXiv:1807.06209).

**Prior**. flat `r_d ∈ [130, 165] Mpc`. All other priors identical to Phase 3
mcmc_phase3.py.

## Results

| model | r_d [Mpc] | Δ vs Planck [Mpc] | joint σ [Mpc] | n_σ | verdict |
|---|---|---|---|---|---|
| LCDM 5D | 148.69 +0.53/-0.49 | +1.60 | 0.61 | **+2.63** | within 3σ |
| V_RP 7D | 148.62 +0.34/-0.39 | +1.53 | 0.49 | **+3.13** | **TENSION > 3σ** |
| V_exp 7D | 148.56 +0.42/-0.41 | +1.47 | 0.52 | **+2.82** | within 3σ |

`n_σ = Δ / √(σ_post² + σ_Planck²)` with σ_post taken as the larger of ±1σ.

## Interpretation

1. **All three models prefer r_d ≈ 148.6 Mpc**, about 1.5 Mpc above the Planck
   measurement. The data (BAO + SN + compressed CMB θ*) pulls r_d up to
   compensate for the lower h (0.672) required by geometry.

2. **V_RP fails D1.4**. Its posterior is the tightest (±0.37 Mpc) because
   (β, n) absorb some of the r_d–H_0 degeneracy elsewhere, leaving r_d
   narrowly peaked. The narrow σ drives n_σ above 3.

3. **LCDM and V_exp both pass D1.4** at the 2.6–2.8σ level, i.e. borderline.
   If the Planck σ is halved (future CMB-S4 forecast ~0.15 Mpc), LCDM would
   slip into ≈3σ tension as well.

4. **D1.4 status**: LCDM ✓, V_RP ✗, V_exp ✓ (borderline).

## Decision gate contribution

- D1.1 (ΔAIC ≤ −6): ✗ for V_family (ΔAIC ≈ +4). Only CPL background
  (w0, wa) Fisher gets ΔAIC = −9.43 (B4).
- D1.2 (ΔBIC ≤ 0): ✗ for all V_family (ΔBIC +15 to +15.6).
- D1.3 (Cassini): ✓ with cubic-Galileon Vainshtein, ✗ unscreened.
- D1.4 (r_d 3σ Planck): LCDM ✓, V_RP ✗, V_exp ✓.

**Overall**: 4-condition AND fails regardless of interpretation. Strict reading
requires ALL three families to pass; V_RP breaks D1.4, V_family as a whole
breaks D1.1/D1.2. Even the most permissive reading (LCDM alone for D1.4) still
fails D1.1 and D1.2 for any coupled-quintessence family.

→ **No-Go branch** for SQMH background-level coupled quintessence.

## Files

- MCMC: `simulations/phase3/mcmc_rdfree.py`
- Chains: `simulations/phase3/chains/{lcdm,vrp,vexp}_rdfree_chain.npy`
- Run log: `simulations/phase3/rdfree_run.log`
