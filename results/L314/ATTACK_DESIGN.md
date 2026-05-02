# L314 — Paper Section 4 (Predictions) Finalization
## 8인 Attack Design

**Loop**: L314 single, paper Section 4 finalization.
**Goal**: 14 original + 5 new + 2 LSST/CMB-lensing + 3 추가 confront 예측의 ranking, framing, honesty audit.

---

### A1. Falsifier Inventory (전체 22개 후 정리)
- **Original (P1–P14)**: 11 truly SQT-specific per L205 audit. P1–P11만 본문 유지. P12–P14 (degenerate w/ LCDM) → 부록.
- **New (P15–P19)**: μ-distortion (PIXIE-class), GW scalar polarization (LISA), DESI DR3 wₐ, redshift drift (ELT 20yr), Euclid f σ_8(z).
- **Extension (P21–P22)**: LSST 5σ falsifier (cluster mass function tail), CMB lensing κ amplitude.
- **Consistency (P25–P27)**: 21cm EoR, BTFR slope, Bullet cluster offset.
- **Dropped (L287/L288)**: P23/P24 weak, removed.

### A2. Risky vs Safe Ranking (8인 합의 분류)
- **Tier-S (Risky, near-term, decisive)**: P19 (Euclid fσ_8), P21 (LSST cluster tail), P15 (DESI DR3 wₐ).
- **Tier-A (Risky, mid-term)**: P16 (μ-distortion PIXIE/PRISTINE), P17 (LISA scalar GW), P22 (CMB lensing).
- **Tier-B (Safe consistency, not decisive alone)**: P25 (21cm EoR), P26 (BTFR), P27 (Bullet).
- **Tier-C (Currently unfavorable to SQT)**: P19 σ_8 — LCDM marginally better; **must report honestly**.

### A3. Head-to-head LCDM Comparison Table (Sec 4.2 핵심)
| Pred | LCDM | SQT | Δχ²-equiv | Status |
|------|------|-----|-----------|--------|
| P15 wₐ | wₐ=0 | wₐ<0 | DESI DR2 +SN: SQT 선호 ~2.5σ | Active |
| P19 fσ_8 | match RSD | slight excess | -0.6 | Marginal |
| **P19 S_8** | **match** | **+0.5–1.2% high** | **disfavored** | **HONEST FAIL** |
| P21 LSST tail | smooth | suppressed | TBD DR1 | Pending |
| P27 Bullet | requires DM | natural offset | qualitative WIN | PASS vs MOND |

### A4. Bullet Cluster (P27) 강조 전략
- L291: Bullet cluster offset reproduced **without** particle DM, via spacetime-metabolism baryon-curvature decoupling.
- **MOND-class theories FAIL Bullet**; SQT PASS — major differentiator, Sec 4.3에 전면 배치.
- 단, weak lensing peak amplitude는 ΛCDM+CDM과 정량적으로 동일한지 미해결 → 부록 명시.

### A5. σ_8 Worsening — Honest Disclosure Plan (가장 중요)
- L286 P19: SQT predicts σ_8(z=0) ≈ 0.83–0.84 vs Planck/KiDS preferred 0.81±0.013. LCDM ≈ 0.811.
- **SQT는 S_8 tension을 *악화*시킨다**. 본문 Sec 4.4 전면 인정.
- "Background-only modification + μ_eff≈1 ⇒ structure level identical to LCDM modulo Ω_m shift" (L6 재발방지 노트와 일치).
- Trade: w(z) 개선 ↔ σ_8 악화. 향후 perturbation-level 채널 (L6 Q15 미해결) 필수.

### A6. Sensitivity Charts (Figures plan)
- **Fig 4.1**: w₀–wₐ contour, SQT trajectory vs DESI+SN+CMB ellipse (L205 figure 재활용).
- **Fig 4.2**: σ_8 vs Ω_m, SQT vs LCDM vs KiDS/DES — 정직 비교 (SQT 살짝 위쪽).
- **Fig 4.3**: Falsifier timeline (2026 DESI DR3 → 2027 Euclid DR1 → 2030 LSST Y3 → 2035 LISA → 2040 ELT redshift drift).
- **Fig 4.4**: Bullet cluster schematic (qualitative, MOND vs SQT vs ΛCDM).

### A7. Near-term vs Long-term Falsifier Calendar
- **2026 Q4**: DESI DR3 → P15 (wₐ < 0 confirm/refute, primary).
- **2027–2028**: Euclid DR1 fσ_8 → P19.
- **2028+**: LSST Y3 cluster mass function → P21 (5σ falsifier).
- **2030+**: PIXIE/PRISTINE μ-distortion → P16.
- **2035+**: LISA scalar polarization upper limit → P17.
- **2040+**: ELT redshift drift → P18.

### A8. Section 4 구조 합의 (8인)
- 4.1 Inventory (22 → 11 SQT-specific summary)
- 4.2 Head-to-head LCDM comparison (table + Fig 4.1)
- 4.3 Bullet cluster qualitative WIN (Fig 4.4)
- 4.4 **σ_8 honest disclosure** (Fig 4.2) — 본문에서 정직하게 인정, 회피 금지
- 4.5 Falsifier timeline (Fig 4.3)
- 4.6 Risky/Safe tier 분류 + 5σ falsifier 강조 (P21 LSST)

### A9. Honesty Constraints (CLAUDE.md 정합)
- L286 σ_8 worsening 명시 (감추지 않음).
- L287/L288 P23/P24 dropped — paper에서 절대 언급 금지.
- L291 Bullet PASS는 *qualitative* 표시, *quantitative WL amplitude*는 미해결로 분리.
- L6 Q15 (S_8 tension 해결 불가) 정직 명시 — "SQT solves H₀ + wₐ but **not** S_8".
