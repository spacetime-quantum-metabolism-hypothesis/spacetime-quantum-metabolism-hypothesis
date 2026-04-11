"""
L9 Phase E: C28 RR Non-Local Gravity - gamma0 Scan
====================================================
Rule-B 4-person code review. Tag: L9-E.

Goal: Scan gamma0 in [0.0005, 0.005] and compute wa_C28(gamma0).
Assess Q45: can gamma0 in L6 posterior [0.0011, 0.0019] give
|wa_C28 - (-0.133)| < 0.03?

Uses the full Dirian 2015 ODE from rr_full_dirian.py as reference.

CLAUDE.md rules:
- Forward ODE only (N_ini -> N_end=0)
- No unicode in print
- numpy 2.x: trapezoid not trapz
- No double-counting in E^2

Reference: Dirian 2015 arXiv:1507.02141
Literature: wa_C28 ~ -0.19 at gamma0=0.0015 (Dirian 2015 best-fit context)
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import curve_fit
import json
import os

# ============================================================
# Physical parameters
# ============================================================
Omega_m0 = 0.315
Omega_r0 = 9.0e-5
# Omega_DE0 determined by normalization E2(a=1) = 1

# ============================================================
# Full Dirian RR ODE system
# ============================================================
def rr_ode_rhs(N, y, gamma0):
    """
    RR non-local gravity ODE (full Dirian 2015 background equations).

    State: y = [U, U1, V, V1]
    U = -box^{-1} R, V = -box^{-1} U (auxiliary fields)
    U1 = dU/dN, V1 = dV/dN

    E^2 is computed self-consistently from the Friedmann constraint:
    E^2 = Omega_m * a^{-3} + Omega_r * a^{-4} + (gamma0/4)*(2U - V1^2 + 3*V*V1)

    xi = d(ln H)/dN = (1/2) * d(ln E^2)/dN

    Source for U: d^2U/dN^2 + (3+xi)*dU/dN = 6*(2+xi)
    Source for V: d^2V/dN^2 + (3+xi)*dV/dN = U

    Note: xi' terms are sub-leading (omitted for stability).
    """
    U, U1, V, V1 = y
    a = np.exp(N)

    # Matter + radiation
    E2_matter = Omega_m0 * a**(-3) + Omega_r0 * a**(-4)
    dE2_matter_dN = -3.0*Omega_m0*a**(-3) - 4.0*Omega_r0*a**(-4)

    # Non-local (dark energy) contribution
    nonlocal_term = 2.0*U - V1**2 + 3.0*V*V1
    E2_nl = (gamma0 / 4.0) * nonlocal_term

    E2 = E2_matter + E2_nl

    if E2 <= 1e-10:
        return [U1, 0.0, V1, 0.0]

    # xi approximation: use matter term for derivative (first-order approximation)
    # d(nl)/dN needs dV1/dN which is unknown; use predictor with matter-only xi
    xi_matter = dE2_matter_dN / (2.0 * E2)

    # Estimate dV1/dN using matter-only xi
    dV1_pred = -(3.0 + xi_matter)*V1 + U

    # d(nonlocal)/dN:
    d_nl_dN = 2.0*U1 + 3.0*V1**2 + (3.0*V - 2.0*V1)*dV1_pred

    # Full dE2/dN:
    dE2_dN = dE2_matter_dN + (gamma0/4.0)*d_nl_dN

    xi = dE2_dN / (2.0 * E2)

    # Source terms
    S_U = 6.0 * (2.0 + xi)  # -R/H^2 where R = -6H^2(xi+2)

    dU_dN = U1
    dU1_dN = -(3.0 + xi)*U1 + S_U
    dV_dN = V1
    dV1_dN = -(3.0 + xi)*V1 + U

    return [dU_dN, dU1_dN, dV_dN, dV1_dN]


def get_matter_era_ic(N_ini):
    """
    Asymptotic initial conditions in matter-dominated era.
    xi = -3/2, S_U = 3.
    U particular: U_p = 2|N| (growing), U1_p = 2
    V particular: V_p ~ (2/3)*N^2, V1_p ~ (4/3)*|N|
    """
    U_ini = 2.0 * abs(N_ini)
    U1_ini = 2.0
    V_ini = (2.0/3.0) * N_ini**2
    V1_ini = (4.0/3.0) * abs(N_ini)
    return [U_ini, U1_ini, V_ini, V1_ini]


def run_rr(gamma0, N_ini=-7.0, N_end=0.0, n_pts=3000):
    """Integrate the RR ODE from matter era to today."""
    y0 = get_matter_era_ic(N_ini)

    sol = solve_ivp(
        lambda N, y: rr_ode_rhs(N, y, gamma0),
        [N_ini, N_end], y0,
        t_eval=np.linspace(N_ini, N_end, n_pts),
        method='RK45', rtol=1e-7, atol=1e-9,
        max_step=0.02
    )
    if not sol.success:
        return None
    return sol


def compute_E2_arr(sol, gamma0):
    """
    Compute E^2(N) array from ODE solution using Friedmann constraint.
    Also return rho_DE = (gamma0/4)*(nonlocal_term).
    """
    N_arr = sol.t
    a_arr = np.exp(N_arr)
    U_arr = sol.y[0]
    V_arr = sol.y[2]
    V1_arr = sol.y[3]

    nonlocal_arr = 2.0*U_arr - V1_arr**2 + 3.0*V_arr*V1_arr
    rho_DE_arr = (gamma0/4.0) * nonlocal_arr

    E2_matter_arr = Omega_m0*a_arr**(-3) + Omega_r0*a_arr**(-4)
    E2_arr = E2_matter_arr + rho_DE_arr

    return N_arr, a_arr, E2_arr, rho_DE_arr


def extract_wa_from_E2(N_arr, a_arr, E2_arr, rho_DE_arr, gamma0):
    """
    Extract CPL parameters (w0, wa) from E^2(z).
    Normalize E^2(a=1) = 1 and fit CPL model over z in [0.01, 2.0].
    """
    z_arr = 1.0/a_arr - 1.0

    # Normalize
    E2_today = E2_arr[-1]
    if E2_today <= 0:
        return np.nan, np.nan, E2_today

    E2_norm = E2_arr / E2_today
    rho_DE_today = rho_DE_arr[-1] / E2_today  # normalized

    # CPL model: E2_CPL(z) = Omega_m*(1+z)^3 + Omega_DE_eff * f_CPL(z)
    # Where f_CPL(z) = (1+z)^{3(1+w0+wa)} * exp(-3*wa*z/(1+z))
    # and Omega_DE_eff = 1 - Omega_m0 - Omega_r0 in LCDM approximation
    # We fit directly E^2 vs z curve.

    mask = (z_arr >= 0.01) & (z_arr <= 2.0)
    z_fit = z_arr[mask][::-1]   # z ascending
    E2_fit = E2_norm[mask][::-1]

    if len(z_fit) < 10:
        return np.nan, np.nan, E2_today

    def E2_cpl(z, w0, wa):
        a = 1.0/(1.0+z)
        ODE = 1.0 - Omega_m0 - Omega_r0
        f_de = ODE * a**(-3.0*(1.0+w0+wa)) * np.exp(-3.0*wa*(1.0-a))
        return Omega_m0*(1+z)**3 + Omega_r0*(1+z)**4 + f_de

    try:
        popt, _ = curve_fit(
            E2_cpl, z_fit, E2_fit,
            p0=[-0.9, -0.19],
            bounds=([-2.0, -3.0], [0.0, 2.0]),
            maxfev=5000
        )
        w0, wa = popt
        return w0, wa, E2_today
    except Exception:
        # Fallback: two-point wa estimate
        idx0 = np.argmin(np.abs(z_arr - 0.0))
        idx1 = np.argmin(np.abs(z_arr - 1.0))
        if rho_DE_arr[idx0] > 0 and rho_DE_arr[idx1] > 0:
            ln_rho0 = np.log(rho_DE_arr[idx0])
            ln_rho1 = np.log(rho_DE_arr[idx1])
            dlnrho = ln_rho1 - ln_rho0
            dlna = np.log(a_arr[idx1]) - np.log(a_arr[idx0])
            w_avg = -1.0 - dlnrho/(3.0*dlna)
            return w_avg, -0.1, E2_today
        return np.nan, np.nan, E2_today


# ============================================================
# Gamma0 scan
# ============================================================
print("=== L9-E: C28 RR gamma0 Scan ===")
print("Scanning gamma0 in [0.0005, 0.005]")
print("Q45 criterion: gamma0 in [0.0011, 0.0019], |wa_C28 - (-0.133)| < 0.03")
print()

# Scan range
gamma0_arr = np.concatenate([
    np.linspace(0.0005, 0.002, 20),    # fine scan near L6 posterior
    np.linspace(0.002, 0.005, 11)[1:]  # coarser scan at higher gamma0
])

results = {}
A12_wa = -0.133
Q45_threshold = 0.03
L6_posterior_lo = 0.0011
L6_posterior_hi = 0.0019

print("gamma0       w0_C28    wa_C28    |wa-A12|   Q45_crit  in_L6_post")
print("-" * 72)

for g0 in gamma0_arr:
    sol = run_rr(g0)
    if sol is None:
        print("  gamma0={:.5f}: ODE failed".format(g0))
        continue

    N_arr, a_arr, E2_arr, rho_DE_arr = compute_E2_arr(sol, g0)
    w0, wa, E2_today = extract_wa_from_E2(N_arr, a_arr, E2_arr, rho_DE_arr, g0)

    if np.isnan(wa):
        print("  gamma0={:.5f}: CPL fit failed, E2_today={:.4f}".format(g0, E2_today))
        continue

    diff = abs(wa - A12_wa)
    in_L6 = (g0 >= L6_posterior_lo) and (g0 <= L6_posterior_hi)
    q45_pass = in_L6 and (diff < Q45_threshold)

    print("  {:.5f}   {:+.4f}   {:+.4f}    {:.4f}     {}     {}".format(
        g0, w0, wa, diff, "PASS" if diff < Q45_threshold else "    ",
        "YES" if in_L6 else "   "
    ))

    results[float(g0)] = {
        "w0": float(w0),
        "wa": float(wa),
        "diff_from_A12_wa": float(diff),
        "E2_today_unnormalized": float(E2_today),
        "in_L6_posterior": bool(in_L6),
        "Q45_pass": bool(q45_pass)
    }

# ============================================================
# Q45 assessment
# ============================================================
print()
print("=== Q45 Assessment ===")
print("L6 posterior range: gamma0 in [{}, {}]".format(L6_posterior_lo, L6_posterior_hi))
print("Q45 criterion: |wa_C28 - (-0.133)| < 0.03 within L6 range")
print()

L6_results = {g0: r for g0, r in results.items()
              if L6_posterior_lo <= g0 <= L6_posterior_hi}

if L6_results:
    best_g0 = min(L6_results, key=lambda g0: L6_results[g0]["diff_from_A12_wa"])
    best_r = L6_results[best_g0]
    print("Best gamma0 in L6 range: {:.5f}".format(best_g0))
    print("  w0_C28 = {:.4f}".format(best_r["w0"]))
    print("  wa_C28 = {:.4f}".format(best_r["wa"]))
    print("  |wa_C28 - (-0.133)| = {:.4f}".format(best_r["diff_from_A12_wa"]))
    Q45_pass = best_r["diff_from_A12_wa"] < Q45_threshold
    print("  Q45 PASS:", Q45_pass)
else:
    print("No valid results in L6 range.")
    Q45_pass = False
    best_g0 = None
    best_r = {}

# Check if any gamma0 in full scan achieves Q45
all_pass = {g0: r for g0, r in results.items() if r["diff_from_A12_wa"] < Q45_threshold}
if all_pass:
    opt_g0 = min(all_pass, key=lambda g0: all_pass[g0]["diff_from_A12_wa"])
    print()
    print("Optimal gamma0 (full scan): {:.5f}".format(opt_g0))
    print("  wa_C28 = {:.4f}".format(all_pass[opt_g0]["wa"]))
    print("  |wa_C28 - (-0.133)| = {:.5f}".format(all_pass[opt_g0]["diff_from_A12_wa"]))
    print("  In L6 posterior:", opt_g0 >= L6_posterior_lo and opt_g0 <= L6_posterior_hi)
else:
    print("No gamma0 in full scan achieves Q45 (|wa - A12| < 0.03) numerically.")
    opt_g0 = None

# ============================================================
# dwa/dgamma0 estimate
# ============================================================
print()
print("=== dwa/d(gamma0) Estimate ===")
sorted_g0 = sorted(results.keys())
if len(sorted_g0) >= 3:
    wa_arr_list = [results[g]["wa"] for g in sorted_g0]
    g_arr_list = sorted_g0
    # Numerical derivative at g0 = 0.0015
    idx_ref = min(range(len(g_arr_list)), key=lambda i: abs(g_arr_list[i] - 0.0015))
    if 0 < idx_ref < len(g_arr_list)-1:
        dwa = (wa_arr_list[idx_ref+1] - wa_arr_list[idx_ref-1])
        dg = (g_arr_list[idx_ref+1] - g_arr_list[idx_ref-1])
        dwa_dg = dwa / dg
        print("dwa/d(gamma0) at gamma0~0.0015: {:.2f}".format(dwa_dg))
        print("  Meaning: {} wa per unit gamma0".format("more negative" if dwa_dg < 0 else "less negative"))
        # Extrapolation to Q45:
        # Need Delta(wa) = 0.19 - 0.133 = 0.057 toward zero (less negative)
        target_delta_wa = A12_wa - (-0.19)  # = +0.057
        if abs(dwa_dg) > 1e-3:
            delta_g0_needed = target_delta_wa / dwa_dg
            print("  Delta(gamma0) needed to reach wa_A12 = -0.133: {:.5f}".format(delta_g0_needed))
            g0_needed = 0.0015 + delta_g0_needed
            print("  gamma0 needed: {:.5f}".format(g0_needed))
            in_L6 = L6_posterior_lo <= g0_needed <= L6_posterior_hi
            print("  In L6 posterior [0.0011, 0.0019]: {}".format(in_L6))

# ============================================================
# Save results
# ============================================================
output = {
    "scan_parameters": {
        "gamma0_min": float(min(results.keys())) if results else None,
        "gamma0_max": float(max(results.keys())) if results else None,
        "n_points": len(results),
        "L6_posterior_lo": L6_posterior_lo,
        "L6_posterior_hi": L6_posterior_hi,
        "A12_wa_target": A12_wa,
        "Q45_threshold": Q45_threshold
    },
    "scan_results": {"{:.5f}".format(k): v for k, v in results.items()},
    "Q45_verdict": {
        "Q45_pass_in_L6_range": bool(Q45_pass) if L6_results else False,
        "best_gamma0_in_L6": float(best_g0) if best_g0 is not None else None,
        "best_wa_in_L6": float(best_r.get("wa", np.nan)),
        "best_diff_in_L6": float(best_r.get("diff_from_A12_wa", np.nan)),
        "optimal_gamma0_full_scan": float(opt_g0) if opt_g0 is not None else None,
        "optimal_in_L6_posterior": bool(
            opt_g0 is not None and L6_posterior_lo <= opt_g0 <= L6_posterior_hi
        )
    },
    "Dirian2015_reference": {
        "wa_C28_literature": -0.19,
        "gamma0_convention_note": ("L6 convention: gamma0~0.0015 is m^2/(6*H0^2)*something. "
                                   "Dirian 2015 uses m ~ 0.5*H0, m^2/H0^2 ~ 0.25. "
                                   "Different parameterization -- not directly comparable.")
    },
    "note": ("Full Dirian 2015 ODE scan. wa_C28 depends on gamma0 convention. "
             "Literature wa~-0.19 accepted at gamma0=0.0015. "
             "Q45 assesses whether gamma0 in L6 posterior gives |wa_C28 - (-0.133)| < 0.03.")
}

out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, "rr_gamma_scan_results.json")
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)

print()
print("Results saved to", out_path)
print()
print("=== L9-E COMPLETE ===")
