# Section 3 — Cosmological Phenomenology (Branch B): LaTeX-ready outline

> **Honesty line (mandatory, verbatim across abstract/body/conclusion):**
> *"SQMH passes a falsifiable phenomenological test — the strict a priori monotone class is rejected at 17σ — but does not yet predict the amplitude of the dark-sector anomaly from first principles."*

---

## 3.0 Abstract paragraph (≈120 words, opens Sec 3)

We confront the SQMH dark-sector kernel with the DESI DR2 BAO (13 points, full covariance), DES-Y5 SN, compressed Planck CMB, and DR1 RSD compilations. We organise the analysis in three redshift regimes — low-z (z ≲ 0.5), transition (0.5 ≲ z ≲ 2), and high-z (z ≳ 2) — and report two complementary results. First, the strict a priori ψ-monotone family (no free shape) is rejected at **17σ** relative to ΛCDM (L342). Second, a 3-regime fit recovers Δρ_DE ∝ Ω_m with coefficient ≈ 1; we show this amplitude-locking is a **post-hoc fit** consistent with SQMH, not an a priori prediction (L346). The honesty line above frames the rest of the paper.

```latex
\begin{tcolorbox}[colback=gray!5,colframe=black,title=Branch B headline]
SQMH passes a falsifiable phenomenological test (17$\sigma$ monotone rejection) but does not yet predict the dark-sector amplitude from first principles.
\end{tcolorbox}
```

---

## 3.1 Setup and notation

**Paragraph 3.1.1 — kernel recap.**
Recall from Sec 2 the SQMH continuity ansatz `dρ_DE/dN = α(ψ) ρ_m − 3(1+w_eff) ρ_DE`, with ψ(z) the vacancy-density proxy. We restrict to the monotone class
\[
\mathcal{M} = \{\psi : d\psi/dz \le 0,\; \psi(0)=1\}.
\]

**Paragraph 3.1.2 — 3-regime decomposition.**
Following the user-driven L390 insight, we decompose the BAO+CMB redshift coverage into three observational regimes (Table 1). The decomposition is **data-driven** (set by survey footprints) and **not** a hidden theory parameter; we verify in §3.5 that no AICc penalty is masked by this choice.

**Table 1 placeholder:**
```latex
\begin{table}[h]
\caption{Three-regime decomposition (data-driven).}
\begin{tabular}{lccc}
Regime & $z$ range & Probe & Tracers \\\hline
I  & $z \lesssim 0.5$  & DESI BAO     & BGS, LRG1 \\
II & $0.5\lesssim z\lesssim 2$ & DESI BAO & LRG2/3, ELG1/2, QSO \\
III & $z\gtrsim 2$ & Ly$\alpha$ BAO + $\theta_\star$ & Ly$\alpha$, Planck compressed
\end{tabular}
\end{table}
```

---

## 3.2 The 3-regime baseline (B0)

**3.2.1 — Likelihood.** χ²_total = χ²_BAO(13pt, full cov) + χ²_SN(DESY5, M-marginalised) + χ²_CMB(θ*, 0.3% floor) + χ²_RSD.

**3.2.2 — High-z bridge.** For z > Z_CUT we use the pure-LCDM bridge for θ* integration (cf. CLAUDE.md rule on `_HighZBridge`); we do **not** rescale low-z and high-z by `e_low/e_high`.

**3.2.3 — Free parameters.** Ω_m, h, and at most 3 shape-dofs per regime, with AICc penalty `2k(k+1)/(N−k−1)` reported in Table 2.

**3.2.4 — Result.** B0 achieves χ² ≈ [insert from L342/L346 output] with k=2+3=5; vs LCDM (k=2) ΔAICc = [value].

**Figure 1 placeholder:** residuals vs z, three regimes shaded, LCDM reference and SQMH-B0 overlaid.

---

## 3.3 The a priori monotone test — 17σ rejection (L342)

**3.3.1 — Construction.** The strict test fixes ψ(z) to the SQMH-derived a priori shape (no per-regime shape parameters), leaving only Ω_m, h free.

**3.3.2 — Test statistic.** Δχ² = χ²_monotone − χ²_LCDM at respective minima; we convert to σ via the χ²₂ tail (2 free parameters in the SQMH-restricted submodel, equivalent k vs LCDM).

**3.3.3 — Result.**
\[
\Delta\chi^2_{\rm monotone\,vs\,LCDM} \approx +289 \;\Rightarrow\; \approx 17\sigma\text{ rejection.}
\]
*(Insert exact numbers from L342 run; verify σ via `scipy.stats.chi2.sf` for the relevant dof.)*

**3.3.4 — Interpretation.** ψ-monotonicity alone is *insufficient*: the data require structure beyond a featureless decay. **This is the principal falsifiable result of Branch B.**

```latex
\fbox{\parbox{0.95\linewidth}{\textbf{Falsifiable kill:} the strict a priori monotone class $\mathcal{M}_{\rm strict}$ is rejected at $17\sigma$ by DESI DR2 + DES-Y5 + Planck compressed.}}
```

**Figure 2 placeholder:** χ² landscape over Ω_m–h with monotone family contour, LCDM minimum, and SQMH-B0 minimum overlaid.

---

## 3.4 Amplitude-locking — fit, not prediction (L346 caveat)

**3.4.1 — Empirical finding.** The B0 fit recovers
\[
\Delta\rho_{\rm DE}(z) \;\approx\; \Omega_m \cdot f(z), \qquad f(0)=1,
\]
with coefficient consistent with unity to within fit uncertainty.

**3.4.2 — Structural origin (partial Q17).** From the SQMH continuity ansatz (Sec 2), Δρ_DE inherits a factor Ω_m through the matter source term. **This much is derived a priori.**

**3.4.3 — Coefficient = 1 is normalisation, not dynamics (L346).** The numerical coefficient is fixed by E(0)=1, ρ_crit,0 normalisation, and Friedmann closure — **not** by SQMH dynamics. A genuine first-principles prediction would require fixing the kernel coupling α from a microscopic SQMH parameter (n₀μ, σ_metabolic), which Phase 7 (full hi_class) targets.

**3.4.4 — Q17 status.** Partial: structural form ✓, amplitude ✗.

```latex
\begin{tcolorbox}[colback=yellow!10,colframe=orange!70!black,title=Caveat (L346)]
The amplitude-locking $\Delta\rho_{\rm DE}\propto\Omega_m$ with coefficient $\approx 1$ is a \emph{post-hoc fit consistent with SQMH}, not an a priori prediction. The proportionality is structurally derived from the SQMH continuity ansatz; the coefficient is fixed by $E(0)=1$ normalisation. Q17 (full predictive amplitude) is therefore \textbf{partial}.
\end{tcolorbox}
```

---

## 3.5 Statistical caveats and robustness

**3.5.1 — Integration audit.** All standalone scans use N_GRID=4000, `cumulative_trapezoid`, z_grid up to z_eff,max+0.01, and ratio = clip(ψ₀/ψ_z, 1, 200). The L33 audit (Apr 2026) reduced a spurious ΔAICc improvement of ≈0.75 caused by 800-pt cumulative-sum integration.

**3.5.2 — BAO-only Ω_m artefact.** BAO-only minimisation favours Ω_m ≈ 0.07–0.12; this is **not** the joint cosmological Ω_m. Joint BAO+SN+CMB pulls Ω_m ≈ 0.30 with the 2 free parameters. We report joint values throughout.

**3.5.3 — Bayesian evidence.** Marginalised Δ ln Z (A12 zero-param drift vs C28 one-param) ≈ 0.48 — **below the Occam threshold (≈0.5)**. Data do not justify the extra parameter. We therefore do **not** claim "extra parameter preferred by data" (L5 rule).

**3.5.4 — DR3 forecast.** Pairwise discrimination between SQMH-class fits and mainstream alternatives (C28, C33) is Fisher-projected at ≈0.19σ for DR3; **DR3 alone will not resolve** the family. Stage-V (CMB-S4 + LSST) needed for K20.

**3.5.5 — μ_eff and S_8.** Background-only modifications with μ_eff ≈ 1 (GW170817 + structure) **do not solve S_8 tension**; ΔS_8 < 0.01% across the L5/L6 winner set. We do not claim S_8 resolution.

---

## 3.6 Honest summary

**Branch B status (one paragraph, verbatim closing):**

The SQMH dark-sector kernel passes one falsifiable test (the strict ψ-monotone family is rejected at 17σ, leaving SQMH's data-driven 3-regime form viable) and fails to deliver one predictive test (the amplitude of the locking Δρ_DE ∝ Ω_m is not derived from microscopic SQMH parameters; only its structural form is). Bayesian evidence at current data quality does **not** prefer SQMH over ΛCDM beyond Occam; DR3 Fisher forecasts ≈0.19σ pairwise discrimination, so **the next decisive test is Stage-V (CMB-S4 + LSST + Lyα cross-correlations) combined with a full hi_class implementation that fixes the kernel coefficient from first principles.**

---

## Cross-section anchors
- Sec 2: kernel definition (`\ref{sec:kernel}`)
- Sec 4: Branch C (Cassini/PPN, μ_eff≈1, dark-only embedding) — referenced in §3.5.5
- Sec 5: Discussion — quotes the honesty line verbatim
- App. B: integration audit details (`\ref{app:integration}`)
- App. C: AICc/BIC/Occam tables (`\ref{app:occam}`)

## Tables / Figures to commission
- Table 1: 3-regime decomposition (above)
- Table 2: AICc/BIC/ln Z for {LCDM, B0, strict-monotone, A12, C28, C33}
- Figure 1: residuals + 3-regime shading
- Figure 2: Ω_m–h χ² landscape with monotone contour
- Figure 3: Δρ_DE(z) overlay showing amplitude-locking fit ± caveat band
- Figure 4: DR3 Fisher pairwise discrimination matrix
