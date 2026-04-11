# refs/l13_integration_verdict.md -- L13 Integration Verdict (5 Rounds)

> Date: 2026-04-11. Covers all 5 rounds.
> 8-person team consensus + Rule-B 4-person code review.

---

## Round 1: Baseline Execution (All 6 Phases)

### Kill/Keep Verdicts Summary

| ID  | Status | Numerical Result | Notes |
|-----|--------|-----------------|-------|
| K81 | NOT TRIGGERED | |ODE-A01|=10.1 >> 0.5 | ODE with G0=3*Om is DIFFERENT model, not approximation |
| K82 | PARTIAL | A_amp from ODE=-2.58 ≠ Om=0.31 | Amplitude motivated but not derived |
| K83 | TRIGGERED | True wa correction ~0 (artifacts in channels 2-5) | CPL extraction fails for high-z ODE blow-up |
| K84 | TRIGGERED | Range=62 orders >> 20 | Penrose interpretation partial |
| K85 | TRIGGERED (per-bin) | Max single-bin DR3 SNR=1.85 < 2 | Combined=3.49 sigma |
| K86 | PARTIAL | AIC favors A01 but best-fit A=2.0 ≠ Om | Parsimonious but not uniquely predicted |
| Q81 | FAIL | ODE worse than A01 by 10.1 chi2 | |
| Q82 | FAIL | Exact A=Om not derived | Structurally motivated only |
| Q83 | FAIL | Reliable wa correction ~0 | Channel 2-5 artifacts |
| Q84 | PARTIAL | Penrose interpretation for sigma (NF-34) | Not a derivation |
| Q85 | NEARLY TRIGGERED | Combined SNR=3.49 > 3sigma | Requires combined analysis |
| Q86 | FAIL | Best-fit A=2 ≠ Om | |

---

## Round 1 Key Findings

### New Finding NF-34 (Round 1):
sigma * rho_P = 4*pi/t_P exactly (Penrose collapse rate identity).
Physical interpretation: SQMH fiducial rate = Penrose collapse rate scaled by
matter density fraction of Planck density.
Classification: INTERPRETATION (not derivation). Paper §2 addition.

### Critical Structural Finding (ODE Analysis):
A01 and the exact SQMH ODE with G0=3*Om are ENTIRELY DIFFERENT models.
- A01: phenomenological form OL0*(1+Om*(1-a)) empirically fitted.
- Exact ODE: omega_de = G0*Om*(1+z)^3/6 + C*(1+z)^(-3), which grows at high z.
- Gamma0 required to match A01's slope: ~7.36, not 3*Om.
- A01 is NOT a first-order approximation to the exact ODE.

This is a critical weakness for SQMH: the phenomenological form A01 that 
fits DESI data is NOT the literal solution to the SQMH birth-death ODE.

### Uniqueness Finding:
A01 is preferred by AIC/BIC over the free-A class (delta=-0.14 AIC).
But best-fit A=2.0 >> Om=0.31. SQMH does not uniquely predict the DESI-optimal amplitude.

---

## Round 2: ODE Form Deep Dive

**Focus**: If A01 is not the exact ODE solution, what IS the exact ODE solution?
Can the exact ODE with Gamma0=7.36 (A01-matching) fit DESI?

### Analysis:

The exact ODE with Gamma0 to match A01's linear slope:
  Gamma0_match = OL0*(3+Om)/Om = 7.36

omega_de(a) = 7.36*0.31/(6*a^3) + C*a^3
where C = OL0 - 7.36*0.31/6 = 0.685 - 0.380 = 0.305

This function:
- At a=1 (z=0): 0.380 + 0.305 = 0.685 = OL0. Check.
- Linear slope at a=1: -(3*0.380) + 3*0.305 = -0.225 vs A01 slope = -OL0*Om = -0.213.
  Close but not exact.

The exact ODE still has an a^(-3) term which makes it grow at high z.
At z=2: omega_de = 7.36*0.31/(6*125) + 0.305*(1/27) = 0.00189 + 0.0113 = 0.013
vs A01: OL0*(1+Om*2) = 0.685*(1+0.62) = 1.11

So even with Gamma0=7.36, the exact ODE gives rho_DE ~ 0.013 at z=2,
while A01 gives ~1.11. The ODE under-produces DE at high z.

This means: A01 OVER-PRODUCES dark energy at high z compared to ODE.
A01 is effectively a "dark energy was much more in the past" model,
while the exact ODE has a more standard behavior.

Round 2 conclusion: The A01 phenomenological form produces MORE dark energy
at high z than the exact SQMH ODE permits. A01 is physically "beyond" the ODE.
This is a key weak point: A01 is phenomenologically motivated but theoretically
disconnected from the ODE.

---

## Round 3: Uniqueness Deep Dive

**Focus**: A scan showed best-fit A~1.5-2.0 >> Om. Is there a physical reason?

### A-scan interpretation:

The chi2 vs A scan shows:
- A=0 (LCDM): chi2=12.14
- A=0.31 (Om, A01): chi2=11.58
- A=1.5: chi2=10.13
- A=2.0: chi2=9.77 (bound)

The likelihood MONOTONICALLY increases with A (higher A always better fit).
This means: "more dark energy in the past" is always preferred by DESI data.
A01 with A=Om is at the LOW END of what DESI prefers.

This is a critical finding:
- DESI data prefers A >> Om.
- SQMH predicts A=Om.
- The SQMH prediction is DISFAVORED by the data relative to the phenomenological class.

The reason A=Om fits well at all (chi2=11.58) is that LCDM already fits
reasonably (chi2=12.14), and A01 gives a modest improvement.
But a free A would give chi2=9.77 -- a further improvement of 1.8.

AIC/BIC favor A01 only because the extra parameter (free A) is penalized by 2/ln(7)=1.9.
The chi2 gain from free A (1.8) barely exceeds the BIC penalty (1.9 for N=7).
This is a marginal win for A01, not a strong one.

Round 3 conclusion: SQMH predicts the data prefers A~Om, but actually A~2 is preferred.
SQMH's A=Om prediction misses the optimal amplitude by a factor of ~5-7.
This is a genuine weakness: K86 is partially triggered.

---

## Round 4: DR3 Combined Analysis

**Focus**: Combined SNR=3.49 sigma from DR3. What does this mean for K85/Q85?

The L13-D analysis shows:
- No single z-bin reaches 3sigma in DR3 (max=1.85 at z=0.93).
- Combined 7-bin: 3.49 sigma -- exceeds the Q85 threshold if combined analysis used.

Interpretation of "specific z-bin SNR >= 3sigma" (Q85):
Reading 1 (strict per-bin): Q85 FAILS. No bin reaches 3sigma.
Reading 2 (combined Fisher): Q85 PASSES. 3.49 sigma combined.

The L13 command specifies "특정 z-bin" (specific z-bin), suggesting per-bin.
By strict reading: K85 TRIGGERED.

However, the combined signal IS meaningful. With DR3:
- A proper covariance-weighted analysis would give ~3.5 sigma.
- This is a GENUINE discrimination capability.
- Reporting both is honest: per-bin K85, combined Q85-near.

Round 4 conclusion: DR3 can discriminate A01 from LCDM at ~3.5 sigma
if the full 7-bin data vector with covariance is used. Per-bin K85.

---

## Round 5: wa Gap -- Alternative Approach

**Focus**: Can SQMH produce wa ~ -0.64 through any mechanism?

From L13-W analysis:
- A01 gives wa ~ -0.11 to -0.13 reliably.
- The exact ODE (G0=3*Om or G0=7.36) gives CPL artifacts (w0 at bounds).
- Non-equilibrium initial conditions give artifacts.

Alternative: Is wa=-0.64 within 2sigma of A01's prediction?

DESI DR2 uncertainty on wa: sigma(wa) = (+0.24/-0.21) from arXiv:2404.03002.
A01 wa = -0.133, DESI center = -0.83 (full: w0=-0.757, wa=-0.83).
  |wa_A01 - wa_DESI| = |-0.133 - (-0.83)| = 0.697
  sigma(wa) = 0.22 (average)
  Tension = 0.697/0.22 = 3.2 sigma!

Wait -- this is more serious than reported. Let me recalculate carefully.
DESI 2024 values: w0=-0.827, wa=-0.75 (BAO+CMB+SN, from arXiv:2404.03002 Table 4)
With sigma(wa) ~ 0.29. Tension = |(-0.133) - (-0.75)| / 0.29 = 2.1 sigma.
Or for the more extreme case w0=-0.757, wa=-0.83: tension = 2.4 sigma.

So A01's wa is at 2-2.5 sigma tension with DESI's wa measurement.
This is not ruled out (2sigma is standard), but it's uncomfortable.

Within SQMH, achieving wa ~ -0.5 would require either:
1. V(phi) quintessence rolling (full CLASS-level treatment)
2. A different functional form for rho_DE(a) altogether
3. Non-trivial initial conditions (but these cause CPL artifacts)

Round 5 conclusion: K83 remains triggered. The wa gap is ~2-2.5 sigma.
This is SQMH's biggest tension with data. V(phi) dynamics needed.

---

## Final 5-Round Verdicts

| ID  | Final Status | Evidence |
|-----|-------------|---------|
| K81 | NOT TRIGGERED | A01 ≠ exact ODE (structural difference, not approximation error) |
| K82 | TRIGGERED (weak) | A=Om not derived; structural motivation exists |
| K83 | TRIGGERED | wa gap = 2-2.5 sigma; ~0 reliable correction available |
| K84 | TRIGGERED | Range 62 orders; Penrose interpretation only partial |
| K85 | TRIGGERED (per-bin) | Max SNR=1.85; combined=3.49 (near Q85) |
| K86 | TRIGGERED (partial) | Best-fit A=2.0 ≠ Om; AIC marginal win |
| Q81 | FAIL | ODE worse than A01 |
| Q82 | FAIL | Exact amplitude not derived |
| Q83 | FAIL | No reliable wa correction |
| Q84 | PARTIAL | Penrose interpretation (NF-34) |
| Q85 | NEARLY | Combined 3.49 sigma |
| Q86 | FAIL | Best-fit A ≠ Om |

---

## Paper Impact (Post-L13)

### Include in paper:
1. **NF-34 (§2)**: sigma = 4*pi*G*t_P corresponds to Penrose objective collapse rate.
   "SQMH fiducial rate Gamma0 = 4*pi/t_P equals the Penrose collapse rate for Planck-mass quanta."

2. **DR3 prediction (§5)**: Combined 7-bin discrimination SNR=3.5 sigma in DR3.
   "DESI DR3, combining the 7 BAO bins, provides ~3.5 sigma discrimination between A01 and LCDM."

3. **Honest K83 (§3)**: "The wa gap (0.7) between A01 (~-0.13) and DESI (~-0.83) represents
   2-2.5 sigma tension. Within background-level SQMH, this gap cannot be closed."

4. **Honest K86 (§4)**: "The phenomenologically optimal amplitude A~1.5 differs from
   SQMH's theory prediction A=Om by factor ~5. Information criteria (AIC, BIC) favor
   A=Om due to parsimony, but the data prefers higher amplitudes."

### Critical weakness to address (future):
- A01 is NOT the exact SQMH ODE solution (structural disconnect).
- The exact ODE requires Gamma0~7 to match DESI, not the theoretically motivated Gamma0=3*Om.
- This is the deepest problem: SQMH theory and A01 phenomenology are disconnected at ODE level.

---

## Game-Changer Assessment

No game-changers achieved in L13. The Penrose interpretation (Q84 partial) is
the most significant new finding (NF-34). It provides physical motivation for
sigma without being circular, but does not constitute a derivation.

**Recommendation**: L14 (if planned) should focus on:
1. Finding the SQMH ODE that NATURALLY produces A01-like behavior (resolve K82/Q86).
2. Or V(phi) quintessence dynamics for wa (resolve K83).
3. The fundamental disconnect between the ODE and A01 form.
