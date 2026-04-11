# base.l13.todo.md -- L13 WBS Checklist

> Date: 2026-04-11. L13 5-round execution complete.

---

## Phase Setup (DONE)

- [x] refs/l13_kill_criteria.md (K81-K86, Q81-Q86 frozen before execution)
- [x] simulations/l13/ directory structure created (ode/, amplitude/, wwa/, gamma0/, uniqueness/, dr3/)

---

## L13-O: ODE vs A01 (DONE)

- [x] l13_ode_compare.py: LCDM, A01, full ODE chi2 comparison
- [x] l13_ode_gammascan.py: G0 scan [0.1, 15] (Round 2)
- [x] refs/l13_ode_derivation.md: 8-person discussion
- [x] Key finding: ODE always chi2~21.7 for any G0; A01 chi2=11.6 (NF-35)

---

## L13-A: Amplitude Derivation (DONE)

- [x] l13_amplitude_derivation.py: analytical derivation
- [x] refs/l13_amplitude_derivation.md: 8-person discussion
- [x] Key finding: A_amp from ODE = -2.58 (wrong sign vs Om=0.31); K82 triggered

---

## L13-W: wa Correction (DONE)

- [x] l13_wwa_correction.py: 5 channels (A01, exact ODE, non-equil, radiation, G0 scan)
- [x] refs/l13_wwa_derivation.md: 8-person discussion
- [x] Key finding: Channels 2-5 are CPL artifacts; reliable correction ~0; K83 triggered

---

## L13-Gamma: Gamma0/sigma Origin (DONE)

- [x] l13_gamma0_origin.py: 5 angles (Hawking, dimensional, Penrose, holographic, range)
- [x] l13_gamma0_r5_penrose.py: Penrose identity deep dive (Round 5)
- [x] refs/l13_gamma0_derivation.md: 8-person discussion
- [x] Key finding: NF-34 confirmed -- sigma*rho_P = 4*pi/t_P (algebraic proof)

---

## L13-U: Uniqueness (DONE)

- [x] l13_uniqueness.py: A01 vs free-A AIC/BIC comparison
- [x] l13_uniqueness_r3.py: 6 functional forms (Round 3)
- [x] refs/l13_uniqueness_derivation.md: 8-person discussion
- [x] Key finding: Free-A (A=3.4) is AIC best; A01 ranks 3rd (NF-36)

---

## L13-D: DR3 Prediction (DONE)

- [x] l13_dr3_prediction.py: 7-bin prediction table (R1)
- [x] l13_dr3_r4_combined.py: combined Fisher at fixed Om,h (Round 4)
- [x] refs/l13_dr3_prediction.md: prediction table with DR3 errors
- [x] Key finding: DR3 max per-bin SNR=1.85 (K85); combined 4.5sigma at fixed Om,h (NF-37)

---

## L13-I: Integration (DONE)

- [x] refs/l13_integration_verdict.md: all 5 rounds verdict
- [x] refs/l13_rounds_2to5.md: Rounds 2-5 detailed analysis
- [x] base.l13.result.md: final results
- [x] base.l13.todo.md: this file

---

## New Findings Registered

- [x] NF-34: sigma*rho_P = 4*pi/t_P (Penrose rate identity)
- [x] NF-35: Exact SQMH ODE disconnected from A01 (structural)
- [x] NF-36: A01 not AIC-optimal (free A=3.4 preferred)
- [x] NF-37: DR3 pure perturbation signal 4.5sigma (diagonal, fixed Om,h)

---

## Outstanding Issues for L14 (if applicable)

- [ ] Why is A01 disconnected from exact SQMH ODE? Find functional form that is both ODE-derived AND DESI-compatible.
- [ ] V(phi) quintessence dynamics for wa gap closure (requires Phase 3 CLASS)
- [ ] Full covariance matrix for DR3 combined SNR (marginalized)
- [ ] NF-34 Penrose interpretation: formal connection to Penrose's framework
- [ ] Can ODE with variable Gamma0(z) reproduce A01? (non-constant rate)
