# L478 — Priori-Derivation Attempt of the L468 Fisher-Information Hypothesis

**Status:** consistency probe, no data fitting.
**Sister sims:** `simulations/L478/run.py` (this session); inputs from
`results/L468/SPECULATION.md`, `paper/02_sqmh_axioms.md`, `paper/base.md`.

**Verdict (one line):** *Priori derivation is **NOT POSSIBLE** within the
SQMH framework as currently formulated; the geometric-mean structure is
a log-symmetry tautology, and the absolute locus R★ ≈ 8.66 Mpc/h is set
by observational anchors (R_lin ≈ 80, R_nl ≈ 1 Mpc/h), not by P1–P6.*

---

## 1. The four questions, separated

| # | Question                                                              | Verdict      | Why                                                                                                                                                                                                                          |
|---|------------------------------------------------------------------------|--------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1 | Can `σ₀(R) ∝ 1/√I_F(R)` be derived from P1–P6?                         | **NO**       | P1–P6 (a1–a6 in `paper/base.md` §2.1) constrain mass-action absorption + Γ₀ generation + holographic σ. They do not specify a *scale-dependent* coupling form. Cramér–Rao saturation is a *consistent* re-reading, not forced. |
| 2 | Can R★ be determined without data input?                                | **NO**       | All a-priori SQMH lengths (c/H₀, c·t_P, holographic combinations) are either Hubble or Planck scale (Probe 3). No combination yields ~Mpc/h without inserting a separate astrophysical anchor.                                |
| 3 | Why does the geometric mean emerge from two anchors?                    | **TAUTOLOGY**| Any kernel that is **symmetric in ln R about the midpoint** places its extremum at `ln R★ = ½(ln R_lo + ln R_hi)` ⇒ R★ = √(R_lo · R_hi). Probe 2 confirms this is the non-trivial assumption.                                |
| 4 | Does the SK foundation (Pillar 1) supply the Fisher metric?             | **NO** (alone)| KMS condition fixes detailed balance and the form of the retarded propagator. The Fisher metric on the SK contour is generically non-degenerate; degeneracy at intermediate R requires extra structure not in P1–P6.         |

---

## 2. Probe results (numerical, `simulations/L478/run.py`)

### Probe 1 — Anchor-pair invariance under log-symmetric (linear) kernel

| (R_lo, R_hi)  | R★(I_F min) | √(R_lo·R_hi) | rel.err |
|---------------|-------------|--------------|---------|
| (1, 80)       | 8.9443      | 8.9443       | < 1e-15 |
| (0.5, 50)     | 5.0000      | 5.0000       | < 1e-15 |
| (2, 200)      | 20.0000     | 20.0000      | < 1e-15 |
| (0.1, 10)     | 1.0000      | 1.0000       | 0.0     |
| (5, 500)      | 50.0000     | 50.0000      | < 1e-15 |

⇒ Geometric mean is **exact** for any anchor pair, *given* the
linear-in-ln R interpolation. This is the log-symmetry theorem.

### Probe 2 — Kernel sensitivity at fixed (1, 80) Mpc/h

| Kernel                    | R★(I_F min) | rel.err vs geo-mean |
|---------------------------|-------------|---------------------|
| linear in ln R            | 8.9443      | ≈ 0                 |
| power p=2 in ln R         | 22.20       | **+148 %**          |
| power p=0.5 in ln R       | 2.99        | **−66.6 %**         |
| logistic (sharp=1, sym.)  | 8.9443      | ≈ 0                 |
| logistic (sharp=4, sym.)  | 8.9443      | ≈ 0                 |

⇒ **Geometric-mean emergence requires log-symmetric kernels.** Asymmetric
power kernels shift R★ off geo-mean by O(1). The "natural emergence"
in L468 is therefore *not* a generic theorem of two-anchor problems —
it is a property of the linear-log ansatz used in
`simulations/L468/run.py`.

### Probe 3 — Candidate priori length scales from SQMH constants alone

| Combination                              | Value (Mpc) |
|------------------------------------------|-------------|
| c/H₀ (Hubble)                            | 4.4 × 10³   |
| c·t_P                                    | 5 × 10⁻⁵⁸   |
| √(σ_holo / H₀)                           | 1.5 × 10⁻⁴⁰ |
| (σ_holo / (c·H₀))^½                      | 8.5 × 10⁻⁴⁵ |
| 1 / (n₀μ · σ_holo)  (mean-free-path)     | 1.7 × 10⁻⁶⁶ |

⇒ No combination of SQMH a-priori constants yields a Mpc-scale length.
The cluster scale R★ ≈ 8.66 Mpc/h is **anchor-induced**.

---

## 3. SK / Wetterich foundation analysis

### 3.1 SK (Pillar 1)

The SK contour Z[J⁺,J⁻] gives a Fisher metric `g_ij = ⟨∂_i ln Z, ∂_j ln Z⟩`
on the response field couplings. KMS fixes the *form* of the retarded
propagator G_R but not its *scale dependence* in the matter density power
P(k,R). For SQMH P1–P6:

- The metabolism rate is `R = σ·n·ρ_m`; this is the bilinear B1 ansatz
  (paper §2.2 derived 1), independent of R.
- A scale-dependent coupling σ(R) is *not* part of axiom 1 (a1).
- The KMS-consistent SK construction at Pillar-1 level therefore yields
  a *flat* (scale-independent) Fisher info, contradicting the L468
  hypothesis of an I_F minimum at intermediate R.

⇒ The L468 information-minimum at R★ requires either (i) an additional
microscopic input (e.g. RG flow injecting scale via β-functions, Pillar
2), or (ii) a phenomenological 2-anchor maxent ansatz which is what
L468 actually uses.

### 3.2 Wetterich FRG (Pillar 2)

A scale-dependent flow `Γ_k[Φ]` would naturally give I_F(k) with extrema
at fixed points. *However*, paper `base.md` lines 807–818 explicitly
state:

> "saddle 위치 자연성 P=0 ... saddle 위치 priori 도출은 영구 불가
>  ... saddle 위치는 외부 anchor (cluster 관측 데이터) 만으로 결정"

i.e. **the paper's own self-audit declares priori derivation of the
intermediate-scale extremum permanently impossible in current RG
truncation**. This is a CRITICAL constraint: any L468-style priori
claim contradicts §3 of the paper.

### 3.3 Holographic dimensional bound (Pillar 3)

σ = 4πG·t_P fixes the *amplitude* of the absorption cross-section, not
its scale dependence. Pillar 3 cannot supply R★.

### 3.4 Z₂ SSB (Pillar 4)

η ≲ 10 MeV is a particle-physics constraint, no astrophysical scale
emerges.

---

## 4. What IS derivable (positive findings)

1. **Geometric-mean theorem** — once two anchors are fixed and the
   maxent ansatz is *log-symmetric*, R★ = √(R_lo·R_hi) is exact.
   (Mathematically trivial; not a physics prediction.)
2. **Width** — H(w) at w=½ has H''=−4, giving FWHM in ln R ≈ √(8 ln 2)/√4 ≈ 1.18
   (note: original L468 cites 1.76 — let’s flag a recheck;
   the analytic value depends on the second-derivative normalisation).
3. **Functional form `σ₀(R) ∝ 1/√I_F(R)`** — this is the Cramér–Rao
   *saturation*; it is *consistent* with SQMH but is one choice among
   many. It is not uniquely forced.
4. **Falsifiable handle** — if R_lin or R_nl shifts with future data
   (e.g. DR3 BAO, DESI σ₈ scale), R★ should track the geometric mean.
   That co-shift is the *only* genuine prediction of L468.

---

## 5. Honest classification

Per paper `base.md` `claims_status` taxonomy:

| Claim                                          | Status                |
|------------------------------------------------|-----------------------|
| L468: σ₀(R) ∝ 1/√I_F(R)                       | **POSTDICTION**       |
| L468: R★ = √(R_lin·R_nl) ≈ 8.94 Mpc/h          | **PARTIAL** (geo-mean theorem; locus inherited from anchors) |
| L468: priori derivation from P1–P6             | **NOT_INHERITED**     |
| L468: shift-tracking of R★ with future R_lin   | **PASS_STRONG-candidate** (genuine falsifier, untested) |

This is consistent with paper §3.4 (POSTDICTION) and §6.5(e)
(NOT_INHERITED for the saddle-position locus). L478 confirms L468 does
*not* upgrade these classifications.

---

## 6. One-line summary

**Priori 도출 불가능.** L468의 geometric-mean 구조는 log-대칭 kernel의
tautology이며, R★의 절대값은 외부 anchor 의존. SK/Wetterich foundation은
scale-dependent I_F(R)을 강제하지 않으며, 논문 §3 자체가 saddle 위치 priori
도출을 영구 불가로 명시함. L468은 phenomenological re-reading(POSTDICTION)
으로 분류 유지, 단 anchor 이동 시 R★ co-shift는 falsifiable 예측으로 살아남음.
