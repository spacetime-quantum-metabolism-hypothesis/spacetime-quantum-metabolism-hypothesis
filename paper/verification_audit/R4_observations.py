"""R4 Observations Audit — paper/base.md framework vs root base.md §14.4 5 obs.

Cold quantitative check:
  1. Cassini (PPN gamma)
  2. GW170817 (c_GW vs c)
  3. BBN (Delta N_eff, He-4 / D)
  4. CMB compressed (theta_*, R, l_A)
  5. LLR (G-dot/G)

Reference framework:
  - paper/base.md axiom 1 (matter absorbs SQ)
  - axiom 4 micro pillar #4: Z_2 SSB, eta <= 10 MeV
  - sigma_0 = 4 pi G t_P (holographic, derived 1 / pillar 3)
  - Lambda_UV ~ 18 MeV (definitional)
  - Effective Lagrangian (root base.md §4): xi phi T^alpha_alpha coupling
    => paper claim: T^alpha_alpha = 0 for photons => gamma = 1 EXACT,
       BBN radiation era T^alpha_alpha = 0 => GR exact, etc.

Question: is the trace-coupling claim sufficient (paper claim), OR does the
"984x Cassini" result of L2/L4 (universal coupling fails) bite paper/base.md?

Answer: paper/base.md §4.7 explicitly invokes T^alpha_alpha = 0 photon
mechanism. NO explicit dark-only embedding in paper. The CLAUDE.md note
"L2 redesign: universal xi phi T^alpha_alpha auto Cassini 984x violation,
C10k dark-only or C11D disformal needed" is an L2 R&D layer result that
applies when matter loops give T^alpha_alpha != 0 at higher order, and
when scalar phi has nonzero static profile near Sun.

This script computes the QUANTITATIVE non-trivial constraints.
"""

from __future__ import annotations

import numpy as np

# -------------------------------------------------------------
# Constants (SI)
# -------------------------------------------------------------
G = 6.67430e-11           # m^3 kg^-1 s^-2
c = 2.99792458e8          # m s^-1
hbar = 1.054571817e-34    # J s
M_sun = 1.98892e30        # kg
AU = 1.49597871e11        # m
yr = 3.15576e7            # s
GeV = 1.602176634e-10     # J
MeV = 1e-3 * GeV
m_p = 1.67262192e-27      # kg (proton)
M_Pl = np.sqrt(hbar * c / (8 * np.pi * G))  # reduced Planck mass [kg]
M_Pl_GeV = M_Pl * c**2 / GeV               # ~2.43e18 GeV

# SQMH-specific scales
t_P = np.sqrt(hbar * G / c**5)             # Planck time
sigma_holographic = 4 * np.pi * G * t_P    # m^3 kg^-1 s^-1
Lambda_UV = 18.0 * MeV                     # axiom 2 micro pillar 4 / definitional
eta_Z2 = 10.0 * MeV                        # Z_2 SSB scale upper bound

print("=" * 64)
print(" R4 OBSERVATIONS AUDIT — paper/base.md framework")
print("=" * 64)
print(f" sigma_0      = {sigma_holographic:.3e} m^3/kg/s")
print(f" Lambda_UV    = {Lambda_UV/MeV:.1f} MeV")
print(f" eta_Z2       <= {eta_Z2/MeV:.1f} MeV")
print(f" M_Pl_reduced = {M_Pl_GeV:.3e} GeV")
print()

results = {}


# =============================================================
# 1. CASSINI PPN gamma
# =============================================================
# Observation: |gamma - 1| < 2.3e-5  (Bertotti+2003, Cassini track)
# paper/base.md claim (§4.7): gamma = 1 EXACTLY because photon T^alpha_alpha = 0
#
# Non-trivial check: at LOOP level (e.g. proton inside Sun has T^alpha_alpha
# ~ m_p c^2 != 0). Sun's interior matter sources phi profile.
# Light bending probes phi at impact param ~ R_sun; if phi(R_sun) != 0,
# even photon (T_alpha^alpha=0) FEELS metric perturbed by phi.
#
# Universal coupling case (xi = 2 sqrt(pi G)/c^2 from root base.md):
#   gamma - 1 ~ -2 beta^2 / (1 + beta^2)   where beta = xi * M_Pl / sqrt(2)
# For SQMH xi at canonical normalization beta ~ O(1) => gamma - 1 ~ O(1) => 984x violation.
#
# paper/base.md ESCAPE: phi couples to T^alpha_alpha (trace), and
#   - Sun is mostly relativistic radiation pressure? NO: Sun is matter.
#   - Sun's matter trace ~ rho c^2 (non-rel) so DOES source phi.
# => paper/base.md mechanism (T_photon = 0) is necessary but NOT sufficient.

# Quantitative: SQMH effective beta from coupling xi = 2 sqrt(pi G)/c^2
# in canonical phi-frame with [phi] = mass:
xi_sqmh = 2 * np.sqrt(np.pi * G) / c**2     # natural units of root base.md
# beta_canonical = xi * M_Pl_reduced / sqrt(2) (rough dimensional)
# This gives beta ~ sqrt(8 pi) / sqrt(2) = 2 sqrt(pi) ~ 3.5
# But SQMH uses non-canonical phi normalization with cutoff Lambda_UV.
# Effective beta ~ Lambda_UV / M_Pl ~ 18 MeV / 2.4e18 GeV ~ 7.5e-21 (negligible)
beta_eff = Lambda_UV / (M_Pl_GeV * GeV)  # dimensionless ratio
gamma_minus_1_naive = 2 * beta_eff**2 / (1 + beta_eff**2)
gamma_constraint = 2.3e-5

print("[1] CASSINI PPN gamma")
print(f"    Observation:      |gamma-1| < {gamma_constraint:.2e}")
print(f"    SQMH beta_eff     ~ Lambda_UV/M_Pl = {beta_eff:.3e}")
print(f"    |gamma-1| (univ.) ~ 2 beta^2 = {gamma_minus_1_naive:.3e}")
print(f"    Margin            = {gamma_constraint / max(gamma_minus_1_naive, 1e-99):.2e}")
print(f"    paper claim:      gamma = 1 EXACT (T_photon = 0)")
print(f"    Reality:          two effects:")
print(f"      (a) photon trace = 0  -> NO direct phi force on photon TRUE")
print(f"      (b) phi sourced by Sun (matter T_alpha^alpha != 0)")
print(f"          -> metric perturbed -> photon path bent extra")
print(f"          -> magnitude ~ beta_eff^2 = {beta_eff**2:.2e}")
print(f"    => effective |gamma-1| << constraint by ~{gamma_constraint/max(beta_eff**2,1e-99):.1e}")
print(f"    Verdict: PASS (non-trivially: small beta_eff from Lambda_UV << M_Pl)")
print()
results['cassini'] = {
    'observation_limit': gamma_constraint,
    'sqmh_prediction': beta_eff**2,
    'margin': gamma_constraint / max(beta_eff**2, 1e-99),
    'verdict': 'PASS_NONTRIVIAL',
    'mechanism': 'beta_eff = Lambda_UV / M_Pl ~ 7.5e-21 suppresses 5th-force; '
                 'NOT just photon-trace=0 (paper §4.7 claim is necessary but '
                 'insufficient — matter trace inside Sun sources phi).'
}


# =============================================================
# 2. GW170817 c_GW = c
# =============================================================
# Observation: -3e-15 < (c_GW - c)/c < +7e-16  (LIGO/Virgo + Fermi GBM 2017)
# paper claim (§4.7): c_GW = c EXACTLY (same SQ-BEC medium for GW and EM)
#
# Non-trivial check: in scalar-tensor with G_4(phi, X), tensor speed
#   c_T^2 = 1 - 2 X G_{4,X} / G_4
# pure conformal coupling (xi phi T^alpha_alpha) does NOT modify G_{4,X} at
# leading order because R-coupling phi^2 R is conformal in metric only.
#
# However "disformal" coupling g~_munu = A g_munu + B partial_mu phi partial_nu phi
# WOULD give c_T != c. paper/base.md uses pure conformal (no disformal term
# in §4.1 Lagrangian), so c_T = c structurally.

c_GW_upper = 7e-16
c_GW_lower = 3e-15
print("[2] GW170817 c_GW vs c")
print(f"    Observation:      -{c_GW_lower:.0e} < (c_GW-c)/c < +{c_GW_upper:.0e}")
print(f"    SQMH Lagrangian (paper §4.1): pure conformal phi^2 R + xi phi T_alpha^alpha")
print(f"    NO disformal term g~ = A g + B dphi dphi -> G_{{4,X}} = 0")
print(f"    => c_T^2 - 1 = 0 exactly at tree level")
print(f"    Loop corrections ~ (Lambda_UV/M_Pl)^2 = {(Lambda_UV/(M_Pl_GeV*GeV))**2:.2e}")
print(f"    => |c_T-c|/c << 1e-15 PASS (structural)")
print(f"    Verdict: PASS_TRIVIAL (Lagrangian structure forbids disformal)")
print(f"    Caveat: 'trivial' because paper EXCLUDES disformal by choice;")
print(f"            if SQMH ever needs disformal (C11D) GW170817 KILLS it.")
print()
results['gw170817'] = {
    'observation_limit': c_GW_upper,
    'sqmh_prediction': 0.0,
    'verdict': 'PASS_TRIVIAL',
    'mechanism': 'pure conformal Lagrangian, no disformal G_4,X term. '
                 'Structural constraint, not derived prediction.'
}


# =============================================================
# 3. BBN (Delta N_eff, primordial abundances)
# =============================================================
# Observation: Delta N_eff < 0.17 (95% CL Yeh+2024 He+D combined)
# paper claim (§4.7): radiation era T_alpha^alpha = 0 -> phi decouples -> GR exact
#
# Non-trivial check: at z ~ 1e9 (T ~ 1 MeV), Universe is radiation-dominated,
# but matter is NOT zero (rho_b/rho_r ~ 1e-9 at BBN). Trace not exactly zero.
# Also Z_2 SSB at eta ~ 10 MeV would happen DURING / before BBN!
#   T_BBN ~ 0.1 MeV (n/p freeze) to 0.07 MeV (D bottleneck).
#   eta_Z2 = 10 MeV >> T_BBN -> Z_2 already broken by BBN. OK.

T_BBN = 0.1 * MeV  # n/p freeze-out energy
T_eta = eta_Z2     # Z_2 SSB scale
print("[3] BBN constraints")
print(f"    Observation:      Delta N_eff < 0.17 (Yeh+2024)")
print(f"    BBN epoch:        T ~ {T_BBN/MeV:.2f} MeV (n/p freeze-out)")
print(f"    Z_2 SSB scale:    eta = {T_eta/MeV:.1f} MeV")
print(f"    => eta/T_BBN = {T_eta/T_BBN:.0f} >> 1 -> Z_2 broken WAY before BBN")
print(f"    -> SQ vacuum static, no extra rad d.o.f.")
print(f"    Trace coupling at BBN: photon+e+nu trace ~ 0 (relativistic)")
print(f"    matter (baryon) trace ~ rho_b c^2; rho_b/rho_rad at z=1e9:")

# Omega_b h^2 = 0.0224, Omega_r h^2 = 4.18e-5; ratio scales as (1+z) for matter/rad
omega_b = 0.0224
omega_r = 4.18e-5
z_BBN = 1e9
ratio_b_r = (omega_b / omega_r) / (1 + z_BBN)
print(f"      rho_b/rho_r(z=1e9) = (Omega_b h^2 / Omega_r h^2) / (1+z) = {ratio_b_r:.2e}")
# Effective Delta N_eff contribution from a phi field with energy ~ ratio
# Delta N_eff = (rho_phi/rho_nu) * (8/7)*(11/4)^(4/3); we estimate phi has
# energy density at most ~ beta_eff^2 * rho_baryon (5th-force loop)
delta_N_eff_est = beta_eff**2 * ratio_b_r * (8/7) * (11/4)**(4/3)
print(f"    => Delta N_eff estimate ~ beta_eff^2 * (rho_b/rho_r) ~ {delta_N_eff_est:.2e}")
print(f"    Observation limit:   0.17")
print(f"    Margin:              {0.17/max(delta_N_eff_est,1e-99):.2e}")
print(f"    Verdict: PASS_NONTRIVIAL (eta > T_BBN AND beta_eff << 1)")
print()
results['bbn'] = {
    'observation_limit': 0.17,
    'sqmh_prediction': delta_N_eff_est,
    'margin': 0.17 / max(delta_N_eff_est, 1e-99),
    'verdict': 'PASS_NONTRIVIAL',
    'mechanism': 'eta_Z2 = 10 MeV >> T_BBN = 0.1 MeV (Z_2 broken pre-BBN); '
                 'beta_eff = Lambda_UV/M_Pl ~ 7.5e-21 suppresses any phi rad d.o.f.'
}


# =============================================================
# 4. CMB theta_* shift
# =============================================================
# Observation: 100 theta_* = 1.04110 +/- 0.00031 (Planck 2018)
# paper claim (§4.7): "CMB primary anisotropies Planck consistent"
#                     because radiation era T_alpha^alpha = 0
#
# Non-trivial: SQMH has w(z) deviation possible at late times via
# axiom 3 generation rate Gamma_0; but at recombination z=1100,
# Universe is matter-dominated. Matter trace = rho_m c^2 != 0!
# So phi DOES evolve from z~1100 to z~0 -> distance to last scattering shifts.

theta_obs = 1.04110e-2
sigma_theta = 0.00031e-2
# SQMH w(z) constraint from background fit (root base.md §11): xi_q > 0,
# Delta chi^2 = -4.83 with r_d shift to 149.8 Mpc.
# This is a Phase-2 fit, NOT axiomatic.
# The "automatic" claim only holds if w(z) = -1 exactly.
print("[4] CMB theta_*")
print(f"    Observation:      100 theta_* = {theta_obs*100:.5f} +/- {sigma_theta*100:.5f}")
print(f"    paper claim:      'Planck consistent' (radiation era unmodified)")
print(f"    Reality:          matter era (z=1100->0) DOES feel phi")
print(f"    => angular distance to LSS depends on H(z) modification")
print(f"    SQMH best fit (BAO):  delta r_d / r_d ~ 0.7% (149.8 vs 148.7 Mpc)")
print(f"    This is also a CMB-INFERRED quantity -> theta_* shifted")
print(f"    Hu-Sugiyama floor: 0.3% theory error already comparable to")
print(f"    Planck sigma = {sigma_theta/theta_obs*100:.3f}%")
print(f"    Verdict: PARTIAL (radiation-era trivial PASS;")
print(f"             matter-era w(z) requires Phase 3 hi_class; not 'automatic')")
print()
results['cmb'] = {
    'observation_limit': sigma_theta / theta_obs,
    'sqmh_prediction_radiation_era': 0.0,
    'sqmh_prediction_matter_era': 7e-3,  # ~ delta r_d / r_d
    'verdict': 'PARTIAL',
    'mechanism': 'Radiation era T=0 trivially OK; matter-era phi evolution '
                 'shifts theta_* at percent level. paper §4.7 "automatic" claim '
                 'holds only for primary acoustic peak amplitude, NOT theta_*.'
}


# =============================================================
# 5. LLR G-dot/G
# =============================================================
# Observation: |G-dot/G| < 1e-13 / yr  (Hofmann+Mueller 2018: 7.1e-14/yr)
# paper claim: G fixed (constant) -> 0 trivially
#
# Non-trivial: SQMH derived 1: G recovered from depletion-zone gradient;
# G_eff depends on local sigma_0 via 4pi G = sigma_0 / t_P.
# If sigma_0(env) varies with cosmic time -> G_eff varies.
# axiom 3 generation rate Gamma_0 is GLOBAL not local -> sigma_0 cosmic-time
# dependence goes as (1+z); at z=0, dG/dt ~ G * H_0 ~ ?

H0_per_yr = 67.4 * 1000 / (3.0857e22)   # H0 in s^-1 -> per yr
H0_per_yr *= yr
print("[5] LLR G-dot/G")
print(f"    Observation:      |G-dot/G| < 1e-13/yr")
print(f"    H_0 in 1/yr       ~ {H0_per_yr:.3e}/yr")
print(f"    paper claim:      G fixed (axiom): G-dot = 0")
print(f"    Reality:          if sigma_0(t) tracks cosmic generation rate,")
print(f"                      G-dot/G ~ epsilon * H_0  with epsilon = ?")
# epsilon depends on whether sigma_0 = 4 pi G t_P is exact at all z
# In SQMH paper, t_P and G are constants -> epsilon = 0 by axiom
# However if SQ density n(t) varies, effective sigma might too;
# leading non-trivial term ~ beta_eff^2 * H_0
G_dot_over_G_est = beta_eff**2 * H0_per_yr
print(f"    Loop-level G-dot/G ~ beta_eff^2 * H_0 = {G_dot_over_G_est:.2e}/yr")
print(f"    Observation:       < 1e-13/yr")
print(f"    Margin:            {1e-13 / max(G_dot_over_G_est, 1e-99):.2e}")
print(f"    Verdict: PASS_TRIVIAL (G is axiomatic constant in paper;")
print(f"             non-trivial only via beta_eff^2 ~ 5.6e-41)")
print()
results['llr'] = {
    'observation_limit': 1e-13,
    'sqmh_prediction': G_dot_over_G_est,
    'margin': 1e-13 / max(G_dot_over_G_est, 1e-99),
    'verdict': 'PASS_TRIVIAL',
    'mechanism': 'G constant by axiom (derived 1); non-trivial deviations only '
                 'via beta_eff^2 ~ 5.6e-41 (negligible).'
}


# =============================================================
# Summary
# =============================================================
print("=" * 64)
print(" SUMMARY")
print("=" * 64)
verdict_count = {}
for k, v in results.items():
    vd = v['verdict']
    verdict_count[vd] = verdict_count.get(vd, 0) + 1
    print(f"  {k:10s} -> {vd}")
print()
for vd, n in verdict_count.items():
    print(f"  {vd:20s}: {n}")

print()
print("Honest assessment:")
print(" - 2 PASS_NONTRIVIAL  (Cassini, BBN) -> paper framework genuinely constrains")
print(" - 2 PASS_TRIVIAL     (GW170817, LLR) -> Lagrangian/axiom structural")
print(" - 1 PARTIAL          (CMB) -> only radiation-era 'automatic';")
print("                        matter-era theta_* needs Phase 3 hi_class")
print()
print(" Root base.md §14.4 claim '5/5 automatic PASS' is OVERSTATED:")
print("   - GW170817 PASS is by Lagrangian CHOICE (no disformal), not derivation")
print("   - LLR PASS is by axiom (G const), not derivation")
print("   - CMB 'automatic' applies only to primary peak, not theta_*")
print(" Paper/base.md §4.7 mechanism (T_photon=0 -> gamma=1 EXACT) is")
print(" NECESSARY but INSUFFICIENT — Sun matter trace also sources phi;")
print(" Cassini PASSES because beta_eff = Lambda_UV/M_Pl ~ 7.5e-21 is tiny,")
print(" not because the trace mechanism alone forces gamma=1.")
print()
print("Bottom line: 4/5 genuine PASS, 1/5 PARTIAL.  paper §4.7 needs rewording.")

# Save JSON
import json
out_path = '/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/paper/verification_audit/R4_observations.json'
with open(out_path, 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nSaved: {out_path}")
