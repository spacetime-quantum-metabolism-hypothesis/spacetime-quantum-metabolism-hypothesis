"""
L9-E Diagnostic: C28 gamma0 scan - diagnose wa=-3 issue and
understand wa vs gamma0 relationship.

The issue: at gamma0 in L6 range [0.0011, 0.0019], the ODE gives
wa hitting the -3 lower bound. This indicates either:
1. The rho_DE(z) is extremely rapidly varying (phantom-like)
2. The normalization is off (E2(a=1) != 1 before normalizing)
3. The CPL fit is failing

This diagnostic:
- Plots rho_DE(z) and E2(z) for selected gamma0 values
- Tries a direct wa estimate from rho_DE slope
- Checks the E2_today normalization
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import curve_fit, brentq
import json, os

Omega_m0 = 0.315
Omega_r0 = 9.0e-5

def rr_ode_rhs(N, y, gamma0):
    U, U1, V, V1 = y
    a = np.exp(N)
    E2_matter = Omega_m0*a**(-3) + Omega_r0*a**(-4)
    dE2_matter_dN = -3.0*Omega_m0*a**(-3) - 4.0*Omega_r0*a**(-4)
    nonlocal_term = 2.0*U - V1**2 + 3.0*V*V1
    E2_nl = (gamma0/4.0)*nonlocal_term
    E2 = E2_matter + E2_nl
    if E2 <= 1e-10:
        return [U1, 0.0, V1, 0.0]
    xi_matter = dE2_matter_dN/(2.0*E2)
    dV1_pred = -(3.0+xi_matter)*V1 + U
    d_nl_dN = 2.0*U1 + 3.0*V1**2 + (3.0*V - 2.0*V1)*dV1_pred
    dE2_dN = dE2_matter_dN + (gamma0/4.0)*d_nl_dN
    xi = dE2_dN/(2.0*E2)
    S_U = 6.0*(2.0+xi)
    return [U1, -(3.0+xi)*U1+S_U, V1, -(3.0+xi)*V1+U]

def get_ic(N_ini):
    U_ini = 2.0*abs(N_ini)
    U1_ini = 2.0
    V_ini = (2.0/3.0)*N_ini**2
    V1_ini = (4.0/3.0)*abs(N_ini)
    return [U_ini, U1_ini, V_ini, V1_ini]

def run_rr(gamma0, N_ini=-7.0, n_pts=5000):
    sol = solve_ivp(lambda N, y: rr_ode_rhs(N, y, gamma0),
                    [N_ini, 0.0], get_ic(N_ini),
                    t_eval=np.linspace(N_ini, 0.0, n_pts),
                    method='RK45', rtol=1e-8, atol=1e-10, max_step=0.01)
    return sol if sol.success else None

# Diagnostic for several gamma0 values
test_g0 = [0.0005, 0.00058, 0.001, 0.0015, 0.002]
print("=== Diagnostic: E2 and rho_DE at z=0,0.5,1 ===")
print("gamma0      E2(z=0)   E2(z=0.5)   rho_DE(0)  rho_DE(0.5)  rho_DE(1)")
print("-"*75)

for g0 in test_g0:
    sol = run_rr(g0)
    if sol is None:
        print("  {:.5f}: ODE failed".format(g0))
        continue
    N_arr = sol.t
    a_arr = np.exp(N_arr)
    z_arr = 1.0/a_arr - 1.0
    U = sol.y[0]; V = sol.y[2]; V1 = sol.y[3]
    nl = 2.0*U - V1**2 + 3.0*V*V1
    rho_DE = (g0/4.0)*nl
    E2_matter = Omega_m0*a_arr**(-3) + Omega_r0*a_arr**(-4)
    E2 = E2_matter + rho_DE

    idx0 = -1
    idx_half = np.argmin(np.abs(z_arr - 0.5))
    idx1 = np.argmin(np.abs(z_arr - 1.0))

    print("  {:.5f}   {:.4f}    {:.4f}      {:.4f}     {:.4f}      {:.4f}".format(
        g0, E2[idx0], E2[idx_half], rho_DE[idx0], rho_DE[idx_half], rho_DE[idx1]))

print()

# Check the nonlinear: rho_DE(z) / rho_DE(0) for g0=0.0015
print("=== rho_DE(z)/rho_DE(0) for gamma0=0.0015 ===")
sol15 = run_rr(0.0015)
if sol15 is not None:
    N_arr = sol15.t
    a_arr = np.exp(N_arr)
    z_arr = 1.0/a_arr - 1.0
    U = sol15.y[0]; V = sol15.y[2]; V1 = sol15.y[3]
    nl = 2.0*U - V1**2 + 3.0*V*V1
    rho_DE = (0.0015/4.0)*nl

    idx0 = -1
    for z_target in [0.0, 0.1, 0.3, 0.5, 1.0, 2.0]:
        idxt = np.argmin(np.abs(z_arr - z_target))
        if abs(rho_DE[idx0]) > 1e-10:
            ratio = rho_DE[idxt]/rho_DE[idx0]
        else:
            ratio = np.nan
        print("  z={:.1f}: rho_DE={:.4f}, ratio={:.4f}".format(z_target, rho_DE[idxt], ratio))

print()

# Try manual wa extraction for g0=0.0015 (no curve_fit bounds at -3)
print("=== Manual wa extraction for g0=0.0015 ===")
sol15 = run_rr(0.0015)
if sol15 is not None:
    N_arr = sol15.t
    a_arr = np.exp(N_arr)
    z_arr = 1.0/a_arr - 1.0
    U = sol15.y[0]; V = sol15.y[2]; V1 = sol15.y[3]
    nl = 2.0*U - V1**2 + 3.0*V*V1
    rho_DE = (0.0015/4.0)*nl
    E2_matter = Omega_m0*a_arr**(-3) + Omega_r0*a_arr**(-4)
    E2 = E2_matter + rho_DE

    # Normalize
    E2_norm = E2 / E2[-1]
    rho_DE_norm = rho_DE / E2[-1]

    print("E2_today =", E2[-1])
    print("rho_DE_today =", rho_DE[-1])
    print("rho_DE_today / E2_today =", rho_DE[-1]/E2[-1])

    # Compute w(z) = -1 - (1/3)*d(ln rho_DE)/d(ln a)
    # Use finite differences
    valid = rho_DE_norm > 0.0001
    if np.any(valid):
        # Get z indices where rho_DE > 0
        z_pos = z_arr[valid]
        lnrho_pos = np.log(rho_DE_norm[valid])
        lna_pos = N_arr[valid]

        # Compute d(ln rho)/d(ln a) = d(ln rho)/dN
        dlnrho_dN = np.gradient(lnrho_pos, lna_pos)
        w_arr = -1.0 - dlnrho_dN/3.0

        # CPL form: w(a) = w0 + wa*(1-a)
        # At z=0 (a=1): w0 ~ w_arr[-1]
        # At z=1 (a=0.5): w ~ w0 + wa/2
        idx_z0 = 0  # lowest z in valid array
        idx_z1 = np.argmin(np.abs(z_pos - 1.0))
        print("w(z~0) =", w_arr[-1] if len(w_arr) > 0 else "NA")
        if idx_z1 < len(w_arr):
            print("w(z~1) =", w_arr[idx_z1])
            # w(z=1) = w0 + wa*(1 - 0.5) = w0 + wa/2
            # w(z=0) = w0
            w0_est = w_arr[-1]
            wa_est = 2.0*(w_arr[idx_z1] - w0_est)
            print("wa_est (two-point) =", wa_est)

# Key structural analysis
print()
print("=== Structural Analysis: Why wa hits -3 in L6 range ===")
print()
print("The issue: at gamma0 in [0.0011, 0.0019]:")
print("  - rho_DE grows rapidly with z (rho_DE >> at high z)")
print("  - This corresponds to w << -1 (phantom)")
print("  - CPL bound at wa=-3 is model constraint, not physical")
print()
print("Physical explanation:")
print("  The RR nonlocal contribution 2U - V1^2 + 3*V*V1 at z>0:")
print("  - U ~ 2*|N| grows with redshift")
print("  - At early times, nonlocal_term >> today value")
print("  - So rho_DE(z) >> rho_DE(0): strong phantom behavior")
print()
print("The Dirian 2015 wa ~ -0.19 result uses:")
print("  1. Proper E2(a=1)=1 normalization via m^2 fitting")
print("  2. The m ~ 0.5*H0 scale, NOT gamma0=0.0015")
print("  3. Full self-consistent CPL fit in their framework")
print()
print("Conclusion: gamma0=0.0015 in L9 convention does NOT correspond")
print("to the Dirian 2015 best-fit model. The conventions differ.")
print("The Q45 assessment must rely on the literature value wa=-0.19")
print("at the Dirian 2015 best-fit (their gamma0 is different).")
print()
print("For the L6 posterior gamma0 range [0.0011, 0.0019]:")
print("  These are likely the SQMH-C28 coupling parameter posterior values,")
print("  not the Dirian 2015 non-local mass parameter m^2/H0^2.")
print("  The wa_C28 in L6 was determined via full Bayesian fit, not ODE.")
print()
print("Q45 FINAL VERDICT: INDETERMINATE")
print("  - Numerical ODE at gamma0=0.0015 (L9 convention) gives")
print("    phantom wa hitting lower bound")
print("  - Literature wa=-0.19 at Dirian 2015 gamma0 convention")
print("  - L6 posterior gamma0 [0.0011, 0.0019] is a different convention")
print("  - Cannot verify Q45 numerically without resolving convention")
print("  - Anti-falsification: Q45 FAIL (cannot demonstrate |wa-A12|<0.03")
print("    within L6 posterior range under any verified convention)")
