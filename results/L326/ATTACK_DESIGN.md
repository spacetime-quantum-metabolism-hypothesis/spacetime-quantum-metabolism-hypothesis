# L326 — Falsification Attack Design

**Date:** 2026-05-01
**Loop:** 236 (cumulative)
**Frame:** Information-theoretic ranking of 8 SQT falsifiers (P15-P19, P21, P22, P27)
**Method:** KL divergence between SQT-predicted and LCDM-baseline observable distributions; cost-benefit per falsifier; risky/safe split.
**8-person independent ideation; no equation-level guidance from prior loops.**

---

## 1. Framework

For each falsifier i with predicted signal offset Δ_i and observational uncertainty σ_i (Gaussian approximation, two competing point hypotheses SQT vs LCDM):

```
D_KL,i = (Δ_i / σ_i)² / 2          [nats]
N_σ,i  = √(2 · D_KL,i) = |Δ_i|/σ_i [detection significance]
```

For multi-parameter falsifiers (P21 cosmic shear, P15 spectrum), Δ/σ uses the projected dominant principal component of the residual.

**Decisiveness metric** = D_KL × P(experiment delivers within timeline) × (1 / cost_units).
**Pre-registration value** = D_KL × prior_betting_market_disagreement.

This is *honest* phenomenology: numbers are SQT team's order-of-magnitude estimates from L282–L291, not externally validated forecasts.

---

## 2. Per-falsifier KL table

| ID | Channel | Δ (SQT−LCDM) | σ_obs (forecast) | D_KL [nats] | N_σ | Timeline | Cost |
|----|---------|--------------|-------------------|-------------|-----|----------|------|
| **P21** | LSST Y10 cosmic shear S_8 | +1.14% (SQT *worse*) | 0.4% | ~4.1 | ~2.85 | 2030+ | $$$$ (built) |
| **P17** | DESI DR3 w_a (V(n,t) ext) | −0.5 to −0.8 | 0.15 | ~5.6–14.2 | ~3.3–5.3 | 2025–2026 | $ (data drop) |
| **P19** | Euclid f·σ_8(z) | structural mismatch | ~1.5% | ~2.2 | ~2.1 | 2026–2028 | $$$ (built) |
| **P15** | PIXIE/PRISM μ-distortion | (2–3)·μ_LCDM | 0.5·μ_LCDM (FG-limited) | ~2.0 | ~2.0 | 2030+ mission | $$$$ (mission) |
| **P16** | ET scalar GW polarisation | ≪ 1 (Z_2-suppressed) | LIGO++ noise | <0.5 | <1 | 2035+ | $$$$$ |
| **P22** | BTFR slope MOND-regime | matches MOND 3.5–4.0 | 0.1 | ~0.5 | ~1 | now (PASS) | $ |
| **P27** | Bullet 1E0657 σ-offset | matches GR | 0.2 (post-hoc PASS) | 0 forward | 0 | done | done |
| ~~P18~~ | ELT z-drift | 50× below sensitivity | — | <0.001 | <0.05 | drop | drop |

---

## 3. Ranking (decisiveness, forward information)

```
1. P17  DESI DR3 w_a            5.6–14.2 nats   IMMEDIATE ★★★★★
2. P21  LSST Y10 S_8            4.1   nats     2030+      ★★★★
3. P19  Euclid f·σ_8            2.2   nats     2026–28    ★★★½
4. P15  PIXIE μ-distortion      2.0   nats     2030+      ★★★
5. P16  ET scalar GW            <0.5  nats     2035+      ★★
6. P22  BTFR (PASS)             0.5   nats     done       ★★
7. P27  Bullet (PASS)           0     forward  done       ★
   P18  z-drift                 drop                       —
```

**Cumulative D_KL of top-3 (P17+P21+P19) ≈ 12 nats** ⇒ joint detection / falsification ~5σ if all three converge — exceeds individual PRD threshold.

---

## 4. Risky vs safe split

**Risky (high D_KL, high failure probability):**
- **P21 LSST S_8** — SQT structurally *predicts the wrong direction* (L286). High prior probability of falsifying SQT → if it survives, +++ evidence; if it falsifies, theory wounded. Pre-registration value MAX.
- **P19 Euclid f·σ_8** — same structural issue, earlier timeline.

**Safe (high D_KL, theory-favorable):**
- **P17 DR3 w_a** — SQT's strongest prediction; w_a < 0 already preferred by DR2. Less risky for theory but most decisive overall because timeline is *now*.

**Neutral / completed:**
- P22, P27 — PASS, no forward information.

**Drop:**
- P18 (sensitivity 50× short), P16 (D_KL < 0.5 even at 2035 ET).

---

## 5. Cost-benefit

| Falsifier | D_KL/$cost | Pre-reg value | Recommended priority |
|-----------|------------|---------------|----------------------|
| P17       | **HIGHEST** (data already taken, just await release) | high | **#1** |
| P19       | medium-high | medium-high | **#2** |
| P21       | medium (built, await Y10) | **HIGHEST** (risky) | **#3** |
| P15       | low (mission not approved) | medium | #4 |
| P16       | very low | low | drop active focus |

---

## 6. Pre-registration recommendation

Lock in **before DR3 release** (estimated 2026 mid-late):
1. **P17 sign+amplitude band**: −1.0 < w_a < −0.4 PASS, w_a > −0.2 or w_a < −1.5 FAIL. 5σ if |w_a| > 0.6.
2. **P19 S_8 prediction**: SQT predicts +1.14% above LCDM Planck — explicit FAIL band.
3. **P21 Y10 S_8 prediction**: same +1.14% structural offset; if Y10 measures −1% offset, SQT falsified at >3σ.

Lock these in arXiv preprint **timestamped before** DR3 unblinding to claim genuine pre-registration.

---

## 7. 8-person independent verdict

| Persona | Vote |
|---------|------|
| Information-theorist | P17 #1 (max D_KL/cost), P21 #2 |
| Experimentalist | P17 (data exists), P19 (next earliest) |
| Bayesian | P21 (pre-reg value), P17 (Occam test) |
| Risk officer | P21 risky/honest split essential |
| Phenomenologist | P17 + P19 amplitude-locked, treat as one channel |
| Theorist | P15 most diagnostic of axiom L2 (μ-distortion ↔ creation rate) |
| Reviewer simulator | P17 will be PRD/JCAP-decisive in 2026 |
| Honest broker | drop P18; downgrade P16; P22/P27 are completed PASS |

**Consensus: P17 > P21 > P19 > P15 ≫ rest.**

---

## 8. Honest caveats

- KL numbers are forecast-grade, not measured. PIXIE/LSST σ are mission-document values; actual will likely be 1.3–2× larger (FG residuals, systematics).
- "P17 ext V(n,t)" requires SQT extension not yet derived (L284). If extension fails, P17 drops to ~LCDM equivalence and D_KL collapses.
- Pre-registration before DR3 only valid if submitted publicly *before* unblinding. Internal documents do not count.
- σ_8 +1.14% (P19/P21) is *structural*, not parameter-tunable (L286, L321 limitation #1). This is a genuine risky prediction, not flexibility.
