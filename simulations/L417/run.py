"""
L417 — Bullet cluster offset quantitative toy.

4인 팀 자율 분담 실행.

Goal: produce SQT-predicted lensing-peak vs gas-peak offset and compare to Clowe 2006 (~150 kpc).

Approach (toy, transparent):
  - Two subclusters (main + bullet) in 1D collision axis.
  - Galaxies (collisionless): tracked by Plummer profile centered on subcluster center post-collision.
  - Gas (collisional): offset toward collision midpoint by ram-pressure stripping (observed).
  - SQT depletion-zone density rho_dep(x) = baryon-tracking with finite re-equilibration
    lag tau_q vs collision crossing time tau_cross. lag --> spatial offset epsilon.
  - Lensing convergence kappa(x) ~ projected total surface density:
        Sigma_eff = Sigma_galaxies + Sigma_gas + Sigma_dep
    Bullet observation: kappa peak - gas peak = 150 +/- 30 kpc.

Critical: NO theoretical "map". 4인 팀 자율 도출 결과물 형태로 단순 mass-tracking
proxy + tau_q sweep. Output: predicted offset in kpc as function of tau_q/tau_cross.

PASS criterion (pre-registered in NEXT_STEP.md):
  offset_pred in [120, 180] kpc --> PASS_STRONG_QUANTITATIVE
  offset_pred in [50, 250] kpc  --> PASS (broad)
  else                          --> caveat strengthen
"""

import os
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import json
import numpy as np

# =============================================================
# Bullet cluster geometry (Clowe 2006 + Markevitch 2002/2004)
# =============================================================
# Post-collision separation between subclusters: ~720 kpc
# Subcluster mass: main M1 ~ 1.5e15 Msun, bullet M2 ~ 1.5e14 Msun
# Collision velocity: v ~ 4700 km/s relative (Mastropietro & Burkert 2008
#   simulation; observed shock 4500-4700 km/s).
# Time since pericenter: t_since ~ 0.1-0.2 Gyr.
# Lensing-gas offset (observed, main subcluster region): ~150 kpc; total
#   weak-lensing mass peak vs X-ray peak.

# Geometry inputs (kpc, km/s, Gyr)
SEP_SUBCL = 720.0          # post-collision center separation [kpc]
V_REL = 4700.0             # relative velocity [km/s]
T_SINCE = 0.15             # time since pericenter [Gyr]
R_SCALE_GAL = 250.0        # Plummer scale of galaxy/DM-effective profile [kpc]
R_SCALE_GAS = 200.0        # gas profile scale [kpc]
GAS_RAMP_OFFSET = 150.0    # observed: gas lags galaxies by ~150 kpc per side
                            # (Markevitch shock front + ram-pressure stripping)
                            # We treat this as observation, not prediction.

# Observed offset (Clowe 2006, Bradac 2006): mass peak vs gas peak
OBS_OFFSET = 150.0
OBS_OFFSET_ERR = 30.0

# ============================================================
# 1D coordinate grid along collision axis
# ============================================================
x = np.linspace(-1500.0, 1500.0, 6001)  # kpc, 0.5 kpc resolution
dx = x[1] - x[0]

# Subcluster centers (galaxies/collisionless): symmetric about origin
xc1 = -SEP_SUBCL / 2.0   # main subcluster (galaxies)
xc2 = +SEP_SUBCL / 2.0   # bullet subcluster (galaxies)

# Mass weights (relative; absolute irrelevant for peak position)
M1, M2 = 10.0, 1.0   # main : bullet ~ 10:1

def plummer_1d(x, xc, a):
    # 1D projected Plummer-like surface density (proxy)
    return (1.0 + ((x - xc) / a) ** 2) ** (-1.5)

# Galaxies (collisionless) profiles
Sigma_gal1 = M1 * plummer_1d(x, xc1, R_SCALE_GAL)
Sigma_gal2 = M2 * plummer_1d(x, xc2, R_SCALE_GAL)
Sigma_gal = Sigma_gal1 + Sigma_gal2

# Gas: shifted toward collision midpoint by GAS_RAMP_OFFSET (ram pressure)
# Gas peak for main subcluster sits at xc1 + GAS_RAMP_OFFSET (toward center).
xg1 = xc1 + GAS_RAMP_OFFSET   # main gas pulled toward bullet
xg2 = xc2 - GAS_RAMP_OFFSET   # bullet gas pulled toward main
# Gas mass fraction (relative to galaxies; cluster gas-to-stellar ~5-10x)
GAS_FRAC = 6.0
Sigma_gas1 = GAS_FRAC * M1 * plummer_1d(x, xg1, R_SCALE_GAS)
Sigma_gas2 = GAS_FRAC * M2 * plummer_1d(x, xg2, R_SCALE_GAS)
Sigma_gas = Sigma_gas1 + Sigma_gas2

# ===================================================================
# SQT depletion zone Sigma_dep(x): tracks galaxies with finite lag eps
# ===================================================================
# Channel (i): tau_q (depletion-zone re-equilibration) vs tau_cross.
# Crossing time tau_cross ~ R_SCALE_GAL / v_rel
KPC_PER_KMS_GYR = 1.022   # 1 km/s * 1 Gyr ~ 1.022 kpc
v_kpc_per_Gyr = V_REL * KPC_PER_KMS_GYR     # ~4803 kpc/Gyr
tau_cross_Gyr = (2 * R_SCALE_GAL) / v_kpc_per_Gyr   # ~0.104 Gyr

# Channel (ii) parameterization: dynamic sigma_0 modulation by collision.
# Toy proxy: depletion zone mass weight = MASS_RATIO * galaxy mass.
# In SQT depletion-zone effective surface density tracks baryons (P14 axiom),
# but ratio depends on environment. Here we set ratio so that, in absence of
# lag, Sigma_dep_peak == lensing peak (i.e. depletion zone dominates lensing).
DEP_RATIO = 5.0   # depletion-zone effective Sigma / galaxy Sigma (SQT toy)

def offset_for_tauq(tau_q_Gyr):
    """Spatial lag epsilon of depletion zone behind galaxies, given tau_q."""
    # Galaxies move with subcluster velocity; depletion zone re-equilibrates
    # with timescale tau_q. Lag length = v * tau_q (lower bound).
    # If tau_q = 0  ==> perfect tracking, no lag.
    # If tau_q > tau_cross ==> depletion zone effectively static between
    #   subclusters (worst case, lag ~ separation/2).
    eps = min(v_kpc_per_Gyr * tau_q_Gyr, SEP_SUBCL / 2.0)
    return eps

def sigma_dep(x, eps):
    # Depletion zone displaced *backward* along motion: each subcluster's
    # depletion zone lags toward original (pre-collision) position.
    # Main subcluster moved toward +x post-collision; depletion zone lags --> shifted toward -x.
    xd1 = xc1 - eps   # main subcluster: dep zone lags behind motion (toward -x)
    xd2 = xc2 + eps   # bullet subcluster: lags behind motion (toward +x)
    # Wait: define motion direction. Bullet impacts main coming from +x to -x
    # historically; post-collision bullet ends up at +x ~360 kpc (moving +x), main at -x.
    # So main subcluster motion is -x direction. Lag of main dep zone = +x (behind).
    # Re-do correctly: main's dep zone lags toward +x (where main came from);
    # bullet's dep zone lags toward -x. Use that convention.
    xd1 = xc1 + eps    # main dep lags behind (toward +x)
    xd2 = xc2 - eps    # bullet dep lags behind (toward -x)
    Sd1 = DEP_RATIO * M1 * plummer_1d(x, xd1, R_SCALE_GAL)
    Sd2 = DEP_RATIO * M2 * plummer_1d(x, xd2, R_SCALE_GAL)
    return Sd1 + Sd2

def lensing_peak_offset(tau_q_Gyr):
    """Predicted offset between SQT lensing peak and gas peak (main side)."""
    eps = offset_for_tauq(tau_q_Gyr)
    Sigma_dep = sigma_dep(x, eps)
    Sigma_total = Sigma_gal + Sigma_dep   # lensing source: collisionless + dep
    # restrict to main-subcluster side: x in [-1500, 0]
    mask_main = x < 0
    # peak of lensing convergence proxy (max Sigma_total on main side)
    i_lens = np.argmax(Sigma_total * mask_main)
    x_lens = x[i_lens]
    # peak of gas on main side
    i_gas = np.argmax(Sigma_gas * mask_main)
    x_gas = x[i_gas]
    # observed offset = lensing peak - gas peak (sign: lensing leads motion)
    # main moves in -x direction post-collision; lensing at xc1=-360, gas at xg1 = -360+150 = -210
    # offset (kpc) = |x_lens - x_gas|
    offset = abs(x_lens - x_gas)
    return offset, x_lens, x_gas, eps

# ============================================================
# Sweep tau_q / tau_cross
# ============================================================
ratios = np.array([0.0, 0.1, 0.3, 0.5, 1.0, 1.5, 2.0, 3.0])
results = []
for r in ratios:
    tauq = r * tau_cross_Gyr
    off, xl, xg, eps = lensing_peak_offset(tauq)
    results.append({
        'tau_q_over_tau_cross': float(r),
        'tau_q_Gyr': float(tauq),
        'eps_kpc': float(eps),
        'x_lens_kpc': float(xl),
        'x_gas_kpc': float(xg),
        'offset_kpc': float(off),
    })

# Best-estimate band: SQT P14 axiom-level — re-equilibration is "fast" since
# depletion zone is microscopic spacetime-quantum process (per axiom). 4인팀
# 자율 도출: tau_q << tau_cross.
# Range tau_q/tau_cross in [0, 0.3] is the SQT-natural regime.
sqt_band = [r for r in results if r['tau_q_over_tau_cross'] <= 0.3]
sqt_offsets = [r['offset_kpc'] for r in sqt_band]
sqt_min, sqt_max = min(sqt_offsets), max(sqt_offsets)

# ============================================================
# Decision logic
# ============================================================
def classify(off):
    if 120.0 <= off <= 180.0:
        return 'PASS_STRONG_QUANTITATIVE'
    if 50.0 <= off <= 250.0:
        return 'PASS_BROAD'
    return 'TENSION_OR_CAVEAT'

# Single fiducial: tau_q = 0 (axiom-level fast re-equilibration)
fid = lensing_peak_offset(0.0)
fid_offset = fid[0]
verdict = classify(fid_offset)

# Honest framing: at tau_q=0 the predicted offset equals GAS_RAMP_OFFSET (gas
# ram-pressure offset) by construction, since dep zone exactly tracks galaxies.
# So "offset = 150 kpc" recovery here is *not* an independent SQT prediction;
# it is inherited from the observed gas-ram-pressure displacement.
# The genuine SQT-specific prediction is: dep zone == galaxy distribution
# (peak collocation), which is what Clowe 2006 actually observed.

# Compute pure SQT-specific quantity: |peak_lens - peak_galaxy|
i_lens_main = np.argmax((Sigma_gal + sigma_dep(x, 0.0)) * (x < 0))
i_gal_main = np.argmax(Sigma_gal * (x < 0))
sqt_specific_offset = abs(x[i_lens_main] - x[i_gal_main])  # should be ~0 at tau_q=0

# What SQT genuinely predicts vs gas peak:
# offset_predicted = |peak_lens - peak_gas| = |peak_galaxy - peak_gas|
#                  = GAS_RAMP_OFFSET (input from observation)
# This is *consistent* but *not independent* — the prediction is actually the
# qualitative statement "lensing tracks galaxies, not gas".

summary = {
    'sep_subcluster_kpc': SEP_SUBCL,
    'v_rel_km_s': V_REL,
    'tau_cross_Gyr': float(tau_cross_Gyr),
    'gas_ram_offset_input_kpc': GAS_RAMP_OFFSET,
    'observed_offset_kpc': OBS_OFFSET,
    'observed_err_kpc': OBS_OFFSET_ERR,
    'sweep': results,
    'sqt_natural_band_tau_q_lt_0p3_tau_cross': {
        'offset_min_kpc': float(sqt_min),
        'offset_max_kpc': float(sqt_max),
    },
    'fiducial_tau_q_zero': {
        'predicted_offset_vs_gas_kpc': float(fid_offset),
        'sqt_specific_lens_vs_galaxy_offset_kpc': float(sqt_specific_offset),
        'classification': verdict,
    },
    'honest_caveat': (
        'The recovered ~150 kpc lens-vs-gas offset at tau_q->0 is dominated by '
        'the *input* gas ram-pressure offset, not an independent SQT prediction. '
        'SQT genuinely predicts |peak_lens - peak_galaxy|~0; the gas-vs-galaxy '
        'separation is set by collisional gas dynamics (input). Quantitative '
        'PASS therefore requires SQT to additionally predict the magnitude of '
        'gas ram-pressure stripping, which is outside the depletion-zone '
        'formalism. Conclusion: PASS remains qualitative.'
    ),
    'final_verdict': (
        'PASS_QUALITATIVE_ONLY (no genuine quantitative upgrade). '
        'tau_q << tau_cross is satisfied at axiom level (P14), so '
        'depletion zone tracks galaxies — consistent with Clowe 2006 — '
        'but the 150 kpc magnitude is inherited from gas dynamics, '
        'not derived from SQT.'
    ),
}

out_path = os.path.join(os.path.dirname(__file__), 'L417_results.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2)

# ASCII-only print (cp949 safe)
print('=== L417 Bullet cluster quantitative attempt ===')
print(f'tau_cross = {tau_cross_Gyr:.4f} Gyr  (R_scale={R_SCALE_GAL} kpc, v={V_REL} km/s)')
print(f'Observed offset (Clowe 2006): {OBS_OFFSET} +/- {OBS_OFFSET_ERR} kpc')
print('--- sweep tau_q/tau_cross ---')
for r in results:
    print(f"  ratio={r['tau_q_over_tau_cross']:.2f}  eps={r['eps_kpc']:7.2f} kpc  offset={r['offset_kpc']:7.2f} kpc")
print(f"SQT natural band offset: [{sqt_min:.1f}, {sqt_max:.1f}] kpc")
print(f"Fiducial (tau_q=0) offset_lens_vs_gas: {fid_offset:.2f} kpc -> {verdict}")
print(f"SQT-specific (lens vs galaxy) offset: {sqt_specific_offset:.4f} kpc (should be ~0)")
print('FINAL VERDICT:')
print('  ' + summary['final_verdict'])
print(f'JSON saved: {out_path}')
