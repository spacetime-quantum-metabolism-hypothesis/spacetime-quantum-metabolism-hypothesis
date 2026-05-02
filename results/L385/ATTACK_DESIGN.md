# L385 ATTACK DESIGN — Holographic n field upper bound (numerical)

## Goal
Compare the SQT-predicted asymptotic n-field value (n_∞) against the
Cohen–Kaplan–Nelson (CKN) holographic upper bound (n_max) on the
energy/quantum-state density of an effective field theory in a region
of size L. Report the saturation ratio r = n_∞ / n_max as the headline
falsifiable number.

## Direction (no formulas given to derivation team)
- Topic: holographic IR/UV mixing bound on effective DOF.
- Physics keywords: black-hole entropy bound (Bekenstein–Hawking),
  CKN bound (Cohen, Kaplan, Nelson 1999), de Sitter horizon,
  vacuum energy density saturation.
- Math keywords: dimensional analysis, Planck units, horizon area,
  asymptotic limits.
- The eight-person team must independently derive both n_max(L) for a
  causal region of size L and the SQT prediction n_∞ from the SQT
  asymptotic state. No equations are pre-supplied.

## Quantities to compute (numerically)
- n_max(L) for L ∈ {laboratory ~1 m, AU, kpc, Hubble radius R_H}.
- n_∞ from the SQT asymptotic limit (team-derived).
- Saturation ratio r(L) = n_∞ / n_max(L) at each scale, with focus on
  L = R_H = c / H_0 using H_0 = 67.4 km/s/Mpc baseline.
- Planck density rho_P and CKN-implied vacuum density rho_Λ^CKN(L).

## Falsifiability criteria
- K_holo_1: r(R_H) finite and within [10^-2, 10^2] → SQT consistent
  with CKN saturation at the cosmological scale.
- K_holo_2: r(R_H) ≪ 10^-3 or ≫ 10^3 → tension with holography;
  flag for L386 follow-up.
- K_holo_3: scale dependence d ln r / d ln L matches expected CKN
  scaling exponent (team derives from horizon-area argument).

## Constants (SI, CODATA 2018)
- c = 2.99792458e8 m/s
- ℏ = 1.054571817e-34 J·s
- G = 6.67430e-11 m^3 kg^-1 s^-2
- H_0 = 67.4 km/s/Mpc = 2.184e-18 s^-1 (baseline)
- t_P = sqrt(ℏ G / c^5)
- l_P = sqrt(ℏ G / c^3)
- rho_P = c^5 / (ℏ G^2)

## Honesty
- This is an order-of-magnitude saturation test, not a precision fit.
- Any agreement at one decade is interpreted as "structurally
  consistent", not as a derivation of Λ.
- No tuning of n_∞ to hit n_max — n_∞ comes only from the team's
  independent SQT derivation.
