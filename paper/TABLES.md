# SQMH/SQT Paper — Tables T1–T4 (LaTeX-ready)

> Compiled: L444 (2026-05-01).
> Sources: `results/L73/SQT_AXIOMS_FORMAL.md` (axioms a1–a6, D1–D5),
> `results/SQT_PROGRESS_SUMMARY.md` §22–§39 (foundations F1–F4,
> predictions, limitations), `L55_audit_axioms_to_phenomenology.md`,
> `L56_tau_q_unification_decision.md`, `paper/08_discussion_limitations.md`.
>
> All tables paste directly into LaTeX with `\begin{table}` /
> `\begin{tabular}` wrappers. Booktabs (`\toprule`, `\midrule`,
> `\bottomrule`) assumed.

---

## T1 — Axioms a1–a6 (formal statement)

```latex
\begin{table}[t]
\centering
\caption{SQMH axioms a1--a6. Natural-language statement (column~2),
formal mathematical content (column~3), and status (column~4).
Status codes: F = fully formalised, P = partially formalised
(awaiting Lagrangian / UV completion).}
\label{tab:T1_axioms}
\begin{tabular}{llp{0.50\linewidth}c}
\toprule
ID & Name & Formal content & Status \\
\midrule
a1 & Absorption        & $R_{\text{abs}}(x,t) = \sigma_0\,n(x,t)\,\rho_m(x,t)$ with $\sigma_0 \ge 0$, $n,\rho_m \ge 0$. Bilinear mass-action absorption of spacetime quanta by matter. & F \\
a2 & Energy conservation & Per absorption event quantum energy $\varepsilon$ is transferred to matter: $\partial_t(\rho_m c^2)|_{\text{abs}} = +R_{\text{abs}}\varepsilon$, $\partial_t(n\varepsilon)|_{\text{abs}} = -R_{\text{abs}}\varepsilon$, so $d/dt[\rho_m c^2 + n\varepsilon] = 0$ for absorption alone. & F \\
a3 & Cosmic creation   & $\partial_t n|_{\text{creation}} = +\Gamma_0$, with $\Gamma_0 \ge 0$ uniform and isotropic in the cosmic mean ($\nabla\Gamma_0 = 0$). & F \\
a4 & Spacetime as quantum pattern & The macroscopic metric $g_{\mu\nu}$ is emergent from $n(x,t)$: $g_{\mu\nu} \equiv g_{\mu\nu}(n;\varepsilon,\sigma_0)$, with $g \to g_{\text{GR}}$ in the $n \to n_\infty$ limit. & P \\
a5 & Stable matter as bound pattern & Stable particles are self-sustaining bound configurations of $n$: $\int \rho_{m,\text{particle}}\,d^3x = m_{\text{particle}}$, with absorption rate $\ll$ self-binding rate. SM spectrum derivation deferred. & P \\
a6 & Maintenance linear in energy & Pattern maintenance loss rate $dN_{\text{patt}}/dt|_{\text{maint}} = -k_M\,E_{\text{patt}}$ with $k_M > 0$ linear; recovers the absorption cross-section $\propto$ mass. & F \\
\bottomrule
\end{tabular}
\end{table}
```

---

## T2 — Derived relations D1–D5, foundations F1–F4, and dependency

The derived relations follow from the axioms plus the SQMH ODE
system (eqs. 2.1–2.3). The foundations are independent
self-consistency checks executed in L75/L76.

```latex
\begin{table}[t]
\centering
\caption{SQMH derived relations D1--D5 and foundational soundness
checks F1--F4. ``From'' lists the axioms (and prior derived
relations) the result depends on. ``Status'' codes: D = derived,
P = partially derived, V = verified by simulation/analytic check.}
\label{tab:T2_derived_foundations}
\begin{tabular}{llp{0.42\linewidth}lc}
\toprule
ID & Name & Formal content & From & Status \\
\midrule
D1 & Newton constant      & $G = \sigma_0/(4\pi\,\tau_q)$. Gravitational coupling fixed by absorption coefficient and quantum lifetime (cf.\ L92 regime-local $\tau_q(\text{env})$). & a1, a2, a4 & D \\
D2 & Steady-state density & $n_\infty = \Gamma_0\,\tau_q$. Equilibrium between cosmic creation and absorption-driven decay. & a1, a3        & D \\
D3 & Quantum energy       & $\varepsilon = \hbar/\tau_q$ (scenario Y; Heisenberg). Selects the Y-branch among the A/X/Y scenarios. & a2          & D \\
D4 & Dark energy          & $\rho_\Lambda = \Lambda_{\text{eff}} c^2/(8\pi G) = n_\infty\,\varepsilon/c^2$. $\Lambda$ identified with the cosmic quantum sector. & D2, D3 & D \\
D5 & Milgrom relation     & $a_0 = c H_0/(2\pi)$ from $\sigma_0(\text{sc})\,\rho_{\text{crit}}\,c = c H_0/2$ with a $1/\pi$ angular projection (L73 H5). Recovers MOND $a_0$ to 4.9\%. & D1, D2 & P \\
\midrule
F1 & Causality            & Group velocity $v_g(k\to\infty)\to c$ in all Branch~B regimes; Sommerfeld precursor artefact ruled out (L75). & a1--a4    & V \\
F2 & Lorentz invariance   & $\Gamma_0$ is a Lorentz scalar across boosts; cosmic frame $=$ CMB rest is observational, not LV (L75). & a3            & V \\
F3 & Vacuum stability     & $n_\infty$ is an attractor; relaxation time $\tau \sim$ Hubble (cosmic), $0.1$~Gyr (cluster), instantaneous (galactic) (L75). & a1, a3, D2 & V \\
F4 & EFT cutoff           & $\Lambda_{\text{UV}} = \hbar c/d_{\text{inter-quantum}} \approx 18.6$~MeV; SQMH valid at $L > d \approx 0.067$~fm; UV completion via QG (LQG / asymptotic safety) deferred (L76). & a1, D2  & V \\
\bottomrule
\end{tabular}
\end{table}
```

**Dependency graph (text form, for a figure caption or appendix):**

```
a1 (absorption) ─┐
a2 (conservation) ┼─► D1 (G = σ₀/4π τ_q)   ──┐
a4 (emergent g)  ─┘                            │
                                              ├─► D5 (a_0 = c H_0/2π)
a1 ─┐                                         │   [via ρ_crit projection]
a3 ─┴─► D2 (n_∞ = Γ_0 τ_q) ──┐                │
                              ├─► D4 (ρ_Λ = n_∞ ε / c²) ──► (Λ origin)
a2 ────► D3 (ε = ℏ/τ_q) ─────┘

F1 (causality)  ◄─ a1, a2, a4
F2 (Lorentz)    ◄─ a3
F3 (stability)  ◄─ a1, a3, D2
F4 (EFT cutoff) ◄─ a1, D2
```

---

## T3 — 22 predictions of SQMH

Each row: ID, target observable, SQMH prediction, falsifier
threshold, target experiment / data, expected timescale, current
status. P-prefix = SQMH-unique falsifiable predictions
(ranked by L80, L101, L121, L170 cumulative work). T-prefix =
shared-with-others tests where SQMH must not fail.

```latex
\begin{table*}[t]
\centering
\caption{SQMH falsifiable predictions T3.1--T3.22. ``Threshold''
gives the value beyond which the prediction is falsified. ``Status''
codes: O = observed PASS, P = pending experiment, A = ambiguous
(consistent at 2$\sigma$), C = current data conditional, F$^*$ =
acknowledged gap (not yet falsified, but unmodelled).}
\label{tab:T3_predictions}
\small
\begin{tabular}{llp{0.27\linewidth}p{0.16\linewidth}lll}
\toprule
\# & ID & Prediction & Falsifier threshold & Source / probe & Date & Status \\
\midrule
1  & P1  & $\sigma_0$ regime spectrum: cluster $<$ galactic by $1.81$ dex (Branch B) & Single $\sigma_0$ with $\sigma(\log a_0)<0.05$ dex across regimes & SPARC 175, KiDS, DES & current & A \\
2  & P2  & $\Lambda_{\text{eff}} = n_\infty\varepsilon/c^2$ (D4) & Independent measure of $n_\infty$ inconsistent with $\rho_\Lambda$ at $5\sigma$ & Combined $\rho_\Lambda$ + lab quantum & 2030+ & P \\
3  & P3  & Quantum depletion zone near matter, $r_{\text{dep}} \sim (n_\infty/\sigma_0\rho_m)^{1/3}$ & EP violation $\eta > 10^{-17}$ at low ambient density & MICROSCOPE-2 & 2027 & P \\
4  & P4  & GW amplitude attenuation $\propto \exp(-D/D_{\text{abs}})$, $D_{\text{abs}} \sim 1/(\sigma_{\text{GW}} n_\infty)$ & Frequency-dependent dispersion at $> 10^{-15}$ relative & ET, CE, LISA & 2030s & P \\
5  & P5  & BBN constraint: $\Gamma_0\tau_q$ at $z\!\sim\!10^9$ does not perturb $n/p$ & $\Delta N_{\text{eff}} > 0.3$ from SQMH absorption & BBN re-fit, CMB-S4 & current/2030 & O \\
6  & P6  & Galactic intrinsic scatter $\sigma(\log\sigma_0) = 0.567$ dex & Tighter scatter $< 0.1$ dex with 4th covariate & Extended SPARC + LSB & 2027+ & O \\
7  & P7  & $a_0(z)/a_0(0) = c H(z)/c H_0$, predicting $a_0(z\!=\!2)/a_0(0)\!\approx\!3.03$ & $|\Delta a_0(z\!=\!2)/a_0|<0.05$ at $2\sigma$ & SKA Phase 1 & 2028--2030 & P \\
8  & P8  & Milgrom relation $a_0 = c H_0/(2\pi)$ (D5) & Time-dependent or $\pm 10\%$ off measured $a_0$ & cosmic-scale RC & current & O (4.9\%) \\
9  & P9  & dSph intermediate $\sigma_0$ between cluster and galactic & dSph $\sigma_0$ matches galactic regime exactly & dwarf catalogues & 2027+ & P \\
10 & P10 & Regime-local $\tau_q(\text{env})$ with $G$ invariant (L92) & Detected $\dot G/G > 10^{-13}$/yr in cosmic-rest frame & LLR, BBN-CMB combo & current & O \\
11 & P11 & $\sigma_0(\text{NS})$ saturation at $\sigma_{\text{galactic}}$ value (L93) & NS structure incompatible at $> 5\sigma$ & NICER + GW170817 EOS & 2027+ & A \\
12 & P12 & Cosmological constant reframed: $\varepsilon \sim \hbar H_0$ (L100, L116) & Lab-scale measurement of $\varepsilon$ inconsistent & quantum gravity probe & 2030s & P \\
13 & P13 & Void galaxy $a_0 \sim 7\%$ of normal (L104) & Void $a_0$ within $1\%$ of field $a_0$ & DESI/Euclid void galaxies & 2027+ & P \\
14 & P14 & Halo shape $=$ baryon shape (L110), differs from CDM N-body & Stripped/disturbed galaxies show CDM-shape halos at $> 3\sigma$ & weak lensing, stellar streams & 2027+ & P \\
15 & G2  & $a_0(\text{disc})/a_0(\text{spheroid}) = \pi/3$ (or $2$, see L115/L143) & Universal $a_0$ across morphology to $< 5\%$ & ATLAS-3D, SAMI & 2025--2030 & P \\
16 & T17 & Compressed CMB $\theta_*$ (Hu-Sugiyama) consistent with Planck & Recombination shift $> 0.3\%$ from joint fit & Planck 2018 + DESI DR2 & current & C \\
17 & T20 & Linear growth $f\sigma_8(z)$ within $2\sigma$ of RSD (BOSS/eBOSS) & Branch~B violation $> 3\sigma$ & DESI RSD, Euclid & current/2027 & C \\
18 & T22 & SPARC RC fit $\chi^2/\nu \le \Lambda$CDM+NFW after intrinsic scatter & SQMH worse than NFW at $\Delta\chi^2 > 30$ globally & SPARC 175 & current & A \\
19 & T26 & $|c_{\text{gw}} - c|/c < 10^{-15}$ (GW170817) & Frequency dispersion observed & LIGO/Virgo/ET & current & O \\
20 & T35 & EP $\eta < 10^{-15}$ at low ambient density (P3-equivalent) & $\eta > 10^{-17}$ in low-density region & MICROSCOPE-2 & 2027 & P \\
21 & T36 & $a_0(z)$ time evolution (P7-equivalent) probed at $z>1$ & $a_0(z)$ constant to $\pm 5\%$ at $z=2$ & SKA Phase 1 & 2028+ & P \\
22 & TBT & Baryonic Tully-Fisher slope $= 4$ (D5 + L119 derivation) & BTFR slope $\ne 4 \pm 0.1$ in clean baryon-dominated sample & SPARC, MaNGA & current & O \\
\bottomrule
\end{tabular}
\end{table*}
```

---

## T4 — 22 limitations / acknowledged gaps

Honest limitations table compiled from L48–L201. ``Severity''
codes: H = high (publication blocker without acknowledgement),
M = medium (publication-acceptable with limitation note), L =
low (technical caveat).

```latex
\begin{table*}[t]
\centering
\caption{SQMH acknowledged limitations T4.1--T4.22. ``Severity''
H/M/L; ``Origin'' is the L-task where the gap was first
documented; ``Mitigation'' is the path forward (or NONE if
structural).}
\label{tab:T4_limitations}
\small
\begin{tabular}{lp{0.35\linewidth}cp{0.30\linewidth}l}
\toprule
\# & Limitation & Severity & Mitigation / status & Origin \\
\midrule
1  & ``Zero free parameters'' claim is false; 5 free parameters in Branch~B (3 $\sigma_0$ + $\Gamma_0$ + $\varepsilon$). & H & Honest count adopted in §1.3 (post L56). Permanent. & L48--L54, L191 \\
2  & $\tau_q$ used with two incompatible meanings: $t_P$ (micro) vs $1/(3H_0)$ (macro), 60 dex apart. & H & L56 option D: split into $\tau_{\text{micro}}$/$\tau_{\text{macro}}$. Bridge unproven. & L55, L56 \\
3  & Single $\sigma_0$ cosmic unification dead (4-value spread $\ge 1.4$ dex). & H & Branch~B (3 regimes) adopted. Permanent. & L48, L49 \\
4  & A1 (time-invariant $a_0$) violated at $\sigma(\log a_0) = 0.78$ dex. & H & A1 declared dead; D5 + regime structure substitutes. & L49 \\
5  & $\sigma_0(k)$ patch: Lorentzian fails 3D unification ($\chi^2 = 58.24$, PASS = 0/3375). & H & Permanently abandoned. & L50, L53 \\
6  & $\sigma_0(z)$ Model V fails: $\chi^2 = 55.5$, no joint pass. & H & Permanently abandoned. & L54 \\
7  & Hubble tension residual: all winners cluster at $h\!\approx\!0.677$ vs SH0ES $0.732$. SQMH ``solves'' only $\Delta h \approx +0.009$. & M & Acknowledged in §8.2. EDE-like $\Gamma_0(z)$ candidate (L114). & L114, paper §8.2 \\
8  & $S_8$ tension structurally unresolved: $\mu_{\text{eff}} \approx 1$ in all winners. & M & Acknowledged in §8.3. Branch B regimes give partial $S_8$ explanation (L157), not derivation. & L157, paper §8.3 \\
9  & DESI $w_a < 0$ in natural conflict with constant-$\Gamma_0$ SQMH. & M & $\Gamma_0(t)$ extension required; micro origin unproven (L78, L112, L135). & L78, L112 \\
10 & Effective field theory status: candidate families (C11D, C28, A12) are realisations, not first-principles SQMH derivations. & M & Acknowledged §8.1. Phase-6 UV completion goal. & paper §8.1 \\
11 & Lagrangian (action principle) only partial: standard real action cannot encode dissipative absorption. & M & Schwinger-Keldysh / MSR formalism (L79, L118, L146) — partial completion. & L79, L118 \\
12 & $\varepsilon \sim \hbar H_0$ scenario Y is one postulate dressed in 4 framings (Bunch-Davies, holographic, Heisenberg, self-consistency). & M & Acknowledged L185. Honest count: 1 postulate. & L116, L162, L185 \\
13 & 3-regime structure of $\sigma_0$ is empirical, not derived from action principle. & M & Landau-Ginzburg / cubic-RG attempts (L142, L165) are plausibility, not derivation (L183, L184). & L182--L184 \\
14 & C26 Perez-Sudarsky (closest direct SQMH realisation) is CMB-dead at background level. & M & §8.8. Recorded as Phase-5 negative result. & paper §8.8 \\
15 & C28 K13 fails ($\hat R = 1.37$); reliance on fixed-$\theta$ evidence. & M & Bayesian evidence used (Δ ln Z), MCMC unreliable for C28. Acknowledged §8.5. & paper §8.5 \\
16 & Alt-20 14-cluster is one SVD direction (n$_{\text{eff}}$ = 1), not 14 independent theories. & L & A12 used as single representative. & paper §8.6 \\
17 & DESI DR3 may shift $w_a$; current results conditional on DR2. & L & Pre-registered DR3 predictions (L155). & paper §8.7 \\
18 & K3 phantom-crossing kill of C11D was a CPL-template artefact (resolved L4–L5). & L & Resolved; recorded as CLAUDE.md rule. & paper §8.10 \\
19 & D1 (Newton constant) overshoots by factor 31 if $\sigma_{\text{galactic}}$ used in cosmic context. & M & L92 regime-local $\tau_q(\text{env})$ restores $G$ invariance; cross-regime mixing rules unproven. & L89, L92 \\
20 & NS regime ($\rho \sim 10^{17}$): not covered by Branch B 3-regime fit. & M & L93 saturation conjecture: $\sigma_0(\text{NS}) \to \sigma_{\text{galactic}}$. Verification pending NICER+GW. & L90, L93 \\
21 & $1/\pi$ vs $1/(2\pi)$ angular factor in D5: L73 H5 picks $\pi/3$, L115/L143 reanalysis suggests $2$ (factor 2). & L & Disc-vs-spheroid $a_0$ ratio prediction G2 carries the ambiguity; ATLAS-3D will discriminate. & L115, L143 \\
22 & Cluster missing-mass: SQMH alone insufficient; $\sim 20/80$ SQMH/CDM hybrid acknowledged. & M & §L113, L136 honest. Branch~B $\sigma_0$(cluster) covers $\sim 15$--$20\%$ of dynamical mass. & L113, L136, L152 \\
\bottomrule
\end{tabular}
\end{table*}
```

---

## Cross-references inside paper

- T1 cited from §2.1 (axiom statement) and §8.1 (EFT realisations).
- T2 cited from §2.4 (FLRW derivation), §3 (candidate families), §8.4 (foundational checks).
- T3 cited from §5 (DESI prediction), §6 (MCMC results), §7 (LCDM comparison).
- T4 cited from §8 (discussion / limitations) — every row maps to a §8.x subsection or to a recorded L-task in `results/`.

---

## Compile notes

- Booktabs and `\caption` style follow JCAP; for PRD swap to
  `ruled` table style.
- T3 and T4 are wide tables (`table*`) — ensure two-column layout
  in the `\documentclass`.
- All numerical values match the canonical sources at compile
  time (L444, 2026-05-01); revalidate if Branch~B fits change.
