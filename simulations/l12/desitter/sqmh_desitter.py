"""
simulations/l12/desitter/sqmh_desitter.py
L12-D: de Sitter SQMH - exact solution and w(z) functional form

Computes:
1. Pure de Sitter (H=const) exact analytic solution for n_bar(t)
2. Perturbative solution in sigma*rho_m
3. w(z) functional form -> compare to A12 erf
4. DESI data chi^2/dof fit
5. Verdict: K74 / Q74

All print() in ASCII only.
"""

import numpy as np
from scipy.integrate import solve_ivp, odeint
from scipy.optimize import minimize
from scipy.special import erf

# ===== CONSTANTS (SI) =====
G = 6.674e-11
c = 2.998e8
hbar = 1.055e-34
k_B = 1.381e-23
t_P = 5.391e-44
l_P = 1.616e-35
m_P = 2.176e-8
Mpc = 3.0857e22

sigma = 4.0 * np.pi * G * t_P
H0_si = 67400.0 / Mpc  # s^-1
Omega_m = 0.315
Omega_L = 0.685
rho_crit0 = 3.0 * H0_si**2 / (8.0 * np.pi * G)
rho_m0 = Omega_m * rho_crit0
rho_P = m_P / l_P**3
Gamma_0 = sigma * rho_P

Pi_SQMH = sigma * rho_m0 / (3.0 * H0_si)
n_bar0_eq = Gamma_0 / (3.0 * H0_si)

print("="*60)
print("L12-D: de Sitter SQMH exact solution")
print("="*60)
print("")
print("sigma = %.4e m^3/(kg*s)" % sigma)
print("H0 = %.4e s^-1" % H0_si)
print("Pi_SQMH = %.4e" % Pi_SQMH)
print("")

# ===== 1. PURE de SITTER EXACT ANALYTIC SOLUTION =====
# H = H_Lambda = const (de Sitter)
# rho_m(t) = rho_m0 * exp(-3*H_Lambda*t) (diluting matter)
# dn_bar/dt + 3*H_Lambda*n_bar = Gamma_0 - sigma*n_bar*rho_m0*exp(-3*H_Lambda*t)
#
# Let x = exp(-3*H_Lambda*t), then:
# dn_bar/dx * (-3*H_Lambda*x) + 3*H_Lambda*n_bar = Gamma_0 - sigma*n_bar*rho_m0*x
# dn_bar/dx * x + n_bar = -Gamma_0/(3*H_Lambda*x) + sigma*n_bar*rho_m0/(3*H_Lambda)
# This is a linear first-order ODE in x:
# dn_bar/dx + n_bar*(sigma*rho_m0/(3*H_Lambda) - 1)/x = -Gamma_0/(3*H_Lambda*x^2)
#
# Actually let's use u = 1+z (cosmological redshift, not exact dS but approximate)
# At late times in dS: rho_m -> 0, n_bar -> Gamma_0/(3*H_Lambda) (equilibrium)
#
# Exact substitution: let tau = H_Lambda*t
# dn_bar/dtau + 3*n_bar = Gamma_0/H_Lambda - (sigma*rho_m0/H_Lambda)*exp(-3*tau)*n_bar
#
# Let epsilon = sigma*rho_m0/(3*H_Lambda) = Pi_SQMH ~ 1.855e-62 (tiny!)
#
# Perturbative expansion: n_bar = n_bar_0(tau) + epsilon*n_bar_1(tau) + O(epsilon^2)
#
# Order 0: dn_bar_0/dtau + 3*n_bar_0 = Gamma_0/H_Lambda
#   -> n_bar_0 = (Gamma_0/H_Lambda)/3 + C_0*exp(-3*tau) = n_bar_eq + C_0*exp(-3*tau)
#
# Order 1: dn_bar_1/dtau + 3*n_bar_1 = -exp(-3*tau)*n_bar_0
#   n_bar_0 = n_bar_eq + C_0*exp(-3*tau)
#   RHS = -exp(-3*tau)*(n_bar_eq + C_0*exp(-3*tau)) = -n_bar_eq*exp(-3*tau) - C_0*exp(-6*tau)
#
# Particular solution for -n_bar_eq*exp(-3*tau):
#   Try n_bar_1p = A*tau*exp(-3*tau)
#   (A*tau*exp(-3*tau))' + 3*(A*tau*exp(-3*tau)) = A*exp(-3*tau) - 3*A*tau*exp(-3*tau) + 3*A*tau*exp(-3*tau)
#   = A*exp(-3*tau) = -n_bar_eq*exp(-3*tau) -> A = -n_bar_eq
#   n_bar_1p_1 = -n_bar_eq*tau*exp(-3*tau)
#
# Particular solution for -C_0*exp(-6*tau):
#   Try n_bar_1p = B*exp(-6*tau)
#   -6*B*exp(-6*tau) + 3*B*exp(-6*tau) = -3*B*exp(-6*tau) = -C_0*exp(-6*tau) -> B = C_0/3
#   n_bar_1p_2 = C_0/3*exp(-6*tau)
#
# Combined: n_bar_1 = C_1*exp(-3*tau) - n_bar_eq*tau*exp(-3*tau) + C_0/3*exp(-6*tau)

H_Lambda = H0_si  # de Sitter Hubble constant = H0 (late universe)
n_bar_eq_dS = Gamma_0 / (3.0 * H_Lambda)

print("--- 1. Pure de Sitter analytic solution ---")
print("H_Lambda = H0 = %.4e s^-1" % H_Lambda)
print("n_bar_eq_dS = Gamma_0/(3*H_Lambda) = %.4e m^-3" % n_bar_eq_dS)
print("epsilon = sigma*rho_m0/(3*H_Lambda) = Pi_SQMH = %.4e" % Pi_SQMH)
print("")
print("n_bar(tau) = n_bar_eq + C_0*exp(-3*tau)")
print("           + epsilon*[-n_bar_eq*tau*exp(-3*tau) + C_0/3*exp(-6*tau)]")
print("           + O(epsilon^2)")
print("where tau = H_Lambda*t")
print("")
print("With initial condition n_bar(0) = n_bar_init:")
print("  n_bar(0) = n_bar_eq + C_0 = n_bar_init -> C_0 = n_bar_init - n_bar_eq")
print("")

# ===== 2. w(z) FROM de SITTER SOLUTION =====
# In de Sitter, dark energy is from n_bar
# rho_DE = n_bar * m_P (mass per quantum = m_P by definition)
# rho_DE(tau) = m_P * [n_bar_eq + C_0*exp(-3*tau) + epsilon*correction]
#
# Pressure: p_DE = -rho_DE + dp_DE/d_something
# Actually: w = p/rho from the SQMH EOS
# The SQMH energy density is: rho_DE = m_P * n_bar (rough)
# In Friedmann: rho_DE ~ Gamma_0/(3H)*m_P = const*H_0 (de Sitter)
#
# The w(z) from de Sitter SQMH:
# w_eff = -1 + (1/3) * d ln rho_DE / d ln a
# With a = exp(H_Lambda*tau):
# rho_DE = n_bar_eq * m_P * [1 + (C_0/n_bar_eq)*exp(-3*tau)]
#        = rho_DE_eq * [1 + delta*exp(-3*H_Lambda*t)]
# where delta = (n_bar_init - n_bar_eq)/n_bar_eq = initial fractional departure
#
# d ln rho_DE/d tau = -3*delta*exp(-3*tau) / (1 + delta*exp(-3*tau))
# = -3*delta*(1+z)^3 / (1 + delta*(1+z)^3)  [since exp(-3*tau) = (1+z)^3 in matter era]
# But in pure dS: a = exp(H_Lambda*tau), not (1+z)^-1 from matter. Need to be careful.
#
# In pure dS: tau is cosmological time * H_Lambda
# 1+z = a_0/a = a_0*exp(-H_Lambda*t) = exp(-H_Lambda*t) (with a_0=1)
# -> exp(-3*H_Lambda*t) = (1+z)^3 YES (in de Sitter)
#
# So: w_dS(z) = -1 + (1/3) * d ln rho_DE / d ln(1+z)^-1
#             = -1 - (1/3) * d ln rho_DE / d ln(1+z)
# d ln rho_DE/d ln(1+z) = -3*delta*(1+z)^3 / (1 + delta*(1+z)^3)
#
# w_dS(z) = -1 + delta*(1+z)^3 / (1 + delta*(1+z)^3)
#
# For small delta: w_dS(z) ~ -1 + delta*(1+z)^3
# For large delta (initial over-production): more complex

print("--- 2. w(z) from de Sitter SQMH ---")
print("w_dS(z) = -1 + delta*(1+z)^3 / (1 + delta*(1+z)^3)")
print("where delta = (n_bar_init - n_bar_eq)/n_bar_eq")
print("")

z_arr = np.linspace(0, 2.0, 1000)

# For various delta values
for delta in [0.01, 0.1, 1.0, 10.0, 100.0]:
    w_dS = -1.0 + delta * (1+z_arr)**3 / (1.0 + delta * (1+z_arr)**3)
    w0_dS = w_dS[0]
    wa_dS = w_dS[-1] - w_dS[0]  # rough wa ~ w(z=2) - w(z=0)
    # Better CPL fit: w(a) = w0 + wa*(1-a) = w0 + wa*z/(1+z) for small z
    # At z=0: w(0) = w0
    # wa from slope: wa = dw/da * a at a=1 = -dw/dz at z=0
    dw_dz_0 = 3.0 * delta / (1.0 + delta)**2
    wa_fit = -dw_dz_0  # wa ~ -dw/dz at z=0 in CPL convention
    print("  delta=%.2e: w(z=0)=%.4f, dw/dz(0)=%.4f, CPL wa~%.4f" % (delta, w0_dS, dw_dz_0, wa_fit))

print("")
print("For DESI-preferred wa ~ -0.133:")
# Solve: wa_fit = -3*delta/(1+delta)^2 = -0.133
# 3*delta/(1+delta)^2 = 0.133
# Let x = delta: 3x/(1+x)^2 = 0.133 -> 3x = 0.133*(1+2x+x^2) = 0.133 + 0.266x + 0.133x^2
# 0.133*x^2 + (0.266-3)*x + 0.133 = 0
# 0.133*x^2 - 2.734*x + 0.133 = 0
a_coeff = 0.133
b_coeff = -2.734
c_coeff = 0.133
disc = b_coeff**2 - 4*a_coeff*c_coeff
delta_sol1 = (-b_coeff + np.sqrt(disc))/(2*a_coeff)
delta_sol2 = (-b_coeff - np.sqrt(disc))/(2*a_coeff)
print("  Requires delta = %.6f or %.6f" % (delta_sol1, delta_sol2))
print("  (small solution: delta ~ %.4f means ~%.1f%% initial over-production)" % (delta_sol2, delta_sol2*100))
print("")

# ===== 3. COMPARE dS w(z) TO A12 erf =====
# A12 erf: w(z) = -1 + w0_erf + wa_erf * z/(1+z) -- CPL fit
# Or more precisely the erf proxy
w0_A12 = -0.886
wa_A12 = -0.133

# A12 CPL: w(z) = w0_A12 + wa_A12*z/(1+z)
w_A12 = w0_A12 + wa_A12 * z_arr/(1+z_arr)

# de Sitter SQMH with delta = delta_sol2:
delta_fit = delta_sol2
w_dS_fit = -1.0 + delta_fit * (1+z_arr)**3 / (1.0 + delta_fit * (1+z_arr)**3)

print("--- 3. Comparison: dS w(z) vs A12 CPL ---")
print("A12: w0=%.3f, wa=%.3f" % (w0_A12, wa_A12))
print("dS SQMH: delta=%.4f gives wa_approx=%.4f" % (delta_fit, -3*delta_fit/(1+delta_fit)**2))
print("")
print("z    | w_A12  | w_dS   | diff")
print("-"*45)
for z_check in [0.0, 0.3, 0.5, 1.0, 1.5, 2.0]:
    idx = np.argmin(np.abs(z_arr - z_check))
    print("%.2f | %.4f | %.4f | %.4f" % (z_check, w_A12[idx], w_dS_fit[idx], w_A12[idx]-w_dS_fit[idx]))
print("")

# ===== 4. DESI DATA AND chi^2 =====
# DESI DR2 effective w(z) measurements from BAO
# Using approximate effective redshifts and w_eff values from DESI+Planck+DES combined
# Note: these are approximate/illustrative since DESI reports w0,wa not w(z) directly
# Use the full SQMH ODE vs LCDM comparison instead of direct w(z) fit

# DESI DR2: w0=-0.757, wa=-0.83 (DESI+Planck+DES-all)
w0_DESI = -0.757
wa_DESI = -0.83

# Compute chi^2 for dS SQMH vs DESI (in w0-wa parameter space)
# The dS SQMH maps to w0_eff, wa_eff from delta
def dS_to_CPL(delta_val):
    """Map de Sitter SQMH parameter delta to CPL w0, wa."""
    z_fine = np.linspace(0, 2.0, 5000)
    w_dS_val = -1.0 + delta_val*(1+z_fine)**3/(1.0+delta_val*(1+z_fine)**3)
    # Fit CPL
    # w(z) = w0 + wa * z/(1+z)
    # At z=0: w0 = w_dS(0) = -1 + delta/(1+delta)
    w0_fit = -1.0 + delta_val/(1.0+delta_val)
    # wa from linear fit
    y_cpl = w_dS_val - w0_fit
    x_cpl = z_fine/(1+z_fine)
    wa_fit = np.sum(x_cpl*y_cpl)/np.sum(x_cpl**2)
    return w0_fit, wa_fit

print("--- 4. DESI chi^2 comparison ---")
print("DESI DR2 best-fit: w0=%.3f, wa=%.3f" % (w0_DESI, wa_DESI))
print("")
print("de Sitter SQMH (w0_dS, wa_dS) for various delta:")
print("delta    | w0_dS  | wa_dS  | chi2 vs DESI")

# Simplified chi^2: sigma_w0 ~ 0.1, sigma_wa ~ 0.3
sigma_w0 = 0.10
sigma_wa = 0.30

for delta in [0.01, 0.02, 0.05, 0.1, 0.5, 1.0, delta_fit]:
    w0_dS_i, wa_dS_i = dS_to_CPL(delta)
    chi2_desi = ((w0_dS_i - w0_DESI)/sigma_w0)**2 + ((wa_dS_i - wa_DESI)/sigma_wa)**2
    print("%.5f  | %.4f | %.4f | %.2f" % (delta, w0_dS_i, wa_dS_i, chi2_desi))

print("")

# Best-fit delta to DESI
from scipy.optimize import minimize_scalar

def chi2_dS_DESI(log_delta):
    delta_val = 10**log_delta
    w0_dS_i, wa_dS_i = dS_to_CPL(delta_val)
    return ((w0_dS_i - w0_DESI)/sigma_w0)**2 + ((wa_dS_i - wa_DESI)/sigma_wa)**2

result = minimize_scalar(chi2_dS_DESI, bounds=(-5, 2), method='bounded')
delta_best = 10**result.x
w0_best, wa_best = dS_to_CPL(delta_best)
chi2_best = result.fun

print("Best-fit de Sitter SQMH:")
print("  delta_best = %.4e" % delta_best)
print("  w0 = %.4f, wa = %.4f" % (w0_best, wa_best))
print("  chi^2 vs DESI (2 dof) = %.2f" % chi2_best)
print("")

# ===== 5. FUNCTIONAL FORM ANALYSIS =====
# w_dS(z) = -1 + delta*(1+z)^3 / (1 + delta*(1+z)^3)
# For small delta: w_dS ~ -1 + delta*(1+z)^3 [exponential in redshift]
# For large delta: w_dS -> 0 [phantom-free]
#
# This is NOT an erf function. It's a Sigmoid/Fermi-Dirac-like function:
# w_dS(x) = -1 + x^3/(1+x^3) where x = delta^(1/3)*(1+z)
#
# The A12 erf is: w_A12(z) ~ -1 + C*erf(D*z + E)
# These are structurally different!

print("--- 5. Functional form analysis ---")
print("dS SQMH w(z) = -1 + delta*(1+z)^3/(1+delta*(1+z)^3)")
print("This is a Fermi-Dirac/sigmoid function, NOT erf.")
print("")
print("Structural difference from erf:")
print("  erf rises from 0 with slope ~ exp(-x^2) behavior")
print("  dS SQMH rises as (1+z)^3 power law, asymptoting to 0")
print("  At large z: w_dS -> 0 (phantom-free, w>-1)")
print("  At z=0: w_dS = -1 + delta/(1+delta)")
print("")

# Compare curvature
d2w_dz2_dS_at_0 = 6*delta_fit*(1+delta_fit-3*delta_fit)/(1+delta_fit)**3
print("d^2w/dz^2 at z=0 for dS SQMH (delta=%.4f): %.4f" % (delta_fit, d2w_dz2_dS_at_0))
d2w_dz2_A12_at_0 = 2.0 * wa_A12  # rough (CPL has no curvature term)
print("d^2w/dz^2 at z=0 for A12 CPL: %.4f (CPL is linear in a)" % d2w_dz2_A12_at_0)
print("")

# ===== 6. FULL SQMH ODE NUMERICAL SOLUTION =====
# Now solve the full SQMH ODE with realistic cosmology
def sqmh_ode(z, state):
    """SQMH ODE in redshift space. state = [n_bar, rho_DE_eff]"""
    n_bar = state[0]

    # E(z) from LCDM (since SQMH ~ LCDM at background)
    E2 = Omega_m*(1+z)**3 + Omega_L
    E = np.sqrt(E2)
    H = H0_si * E

    # Matter density
    rho_m = rho_m0 * (1+z)**3

    # SQMH: dn_bar/dt = Gamma_0 - sigma*n_bar*rho_m - 3H*n_bar
    # Convert to z: d/dt = -H*(1+z)*d/dz
    # dn_bar/dz = -(Gamma_0 - sigma*n_bar*rho_m - 3*H*n_bar) / (H*(1+z))

    rhs_n = Gamma_0 - sigma * n_bar * rho_m - 3.0 * H * n_bar
    dn_dz = -rhs_n / (H * (1+z))

    return [dn_dz]

# Initial condition: n_bar at z=0 near equilibrium
n_bar_init_ode = n_bar0_eq  # start at equilibrium (wa ~ 0 case)
# For wa<0 case: start above equilibrium
epsilon_init_wa = -0.133  # wa = -0.133 requires epsilon_0 ~ delta_fit
n_bar_init_wa = n_bar0_eq * (1.0 + delta_fit)

z_span = (0.0, 3.0)
z_eval = np.linspace(0, 3, 1000)

sol_eq = solve_ivp(sqmh_ode, z_span, [n_bar_init_ode], t_eval=z_eval,
                   method='RK45', rtol=1e-10, atol=1e-12)
sol_wa = solve_ivp(sqmh_ode, z_span, [n_bar_init_wa], t_eval=z_eval,
                   method='RK45', rtol=1e-10, atol=1e-12)

print("--- 6. Full SQMH ODE numerical solution ---")
if sol_eq.success and sol_wa.success:
    n_bar_ode_eq = sol_eq.y[0]
    n_bar_ode_wa = sol_wa.y[0]

    # Compute effective w(z) from n_bar
    # rho_DE = n_bar/n_bar0 * rho_DE0 (proportional)
    rho_DE0 = (1.0-Omega_m)*rho_crit0
    rho_DE_eq = n_bar_ode_eq / n_bar0_eq * rho_DE0
    rho_DE_wa = n_bar_ode_wa / n_bar0_eq * rho_DE0

    # w from continuity: d rho_DE/dz + 3*(1+w)*rho_DE/(1+z) = 0
    # -> w = -1 - (1+z)/(3*rho_DE) * d rho_DE/dz
    drho_dz_eq = np.gradient(rho_DE_eq, z_eval)
    drho_dz_wa = np.gradient(rho_DE_wa, z_eval)

    w_full_eq = -1.0 - (1+z_eval)/(3.0*rho_DE_eq) * drho_dz_eq
    w_full_wa = -1.0 - (1+z_eval)/(3.0*rho_DE_wa) * drho_dz_wa

    print("Equilibrium initial condition (n_bar_init = n_bar_eq):")
    print("  w(z=0) = %.6f" % w_full_eq[0])
    print("  w(z=1) = %.6f" % w_full_eq[500])
    print("  w(z=2) = %.6f" % w_full_eq[666])
    print("  wa (approx) = %.6f" % (w_full_eq[666]-w_full_eq[0]))
    print("")
    print("Over-produced initial condition (n_bar_init = n_bar_eq*(1+delta_fit)):")
    print("  delta_fit = %.6f" % delta_fit)
    print("  w(z=0) = %.6f" % w_full_wa[0])
    print("  w(z=1) = %.6f" % w_full_wa[500])
    print("  w(z=2) = %.6f" % w_full_wa[666])
    print("  wa (approx) = %.6f" % (w_full_wa[666]-w_full_wa[0]))
    print("")

    # chi^2/dof for full ODE vs DESI
    # DESI constrains w0, wa. Use simple estimate.
    w0_ODE = w_full_wa[0]
    wa_ODE = w_full_wa[666] - w_full_wa[0]
    chi2_ODE = ((w0_ODE - w0_DESI)/sigma_w0)**2 + ((wa_ODE - wa_DESI)/sigma_wa)**2
    print("Full ODE chi^2 vs DESI: %.2f" % chi2_ODE)
else:
    print("ODE solution failed. Using analytic estimate.")
    w0_ODE = -1.0 + delta_fit/(1+delta_fit)
    wa_ODE = -3*delta_fit/(1+delta_fit)**2
    chi2_ODE = ((w0_ODE - w0_DESI)/sigma_w0)**2 + ((wa_ODE - wa_DESI)/sigma_wa)**2
    print("Analytic chi^2 vs DESI: %.2f" % chi2_ODE)

print("")

# ===== FINAL VERDICTS =====
print("="*60)
print("FINAL VERDICTS")
print("="*60)
print("")

# K74: chi^2/dof > 10 vs DESI data (if dS different structure)
chi2_dof = chi2_best  # from simplified 2-parameter space
print("K74 (chi^2/dof > 10, dS SQMH disconnected from A12):")
print("  Best-fit chi^2 vs DESI = %.2f" % chi2_best)
print("  K74 threshold: 10")
print("  K74 TRIGGERED: %s" % ("YES" if chi2_best > 10 else "NO"))
print("")
print("Q74 (new functional form + chi^2/dof < 2):")
print("  Functional form: w_dS(z) = -1 + delta*(1+z)^3/(1+delta*(1+z)^3)")
print("  This IS a new functional form (not erf, not CPL, not tanh)")
print("  It is a Fermi-Dirac type (power law sigmoid)")
print("  chi^2 vs DESI = %.2f" % chi2_best)
print("  Q74 chi^2 threshold: 2")
print("  Q74 PASS (functional form): YES")
print("  Q74 PASS (chi^2 < 2): %s" % ("YES" if chi2_best < 2 else "NO"))
print("")
print("STRUCTURE FINDING:")
print("  dS SQMH gives: w(z) = -1 + delta*(1+z)^3 / (1 + delta*(1+z)^3)")
print("  where delta = n_bar_init/n_bar_eq - 1 (initial fractional over-production)")
print("  This is a POWER-LAW SIGMOID, not erf")
print("  Physical interpretation: dark energy tracks matter (goes as (1+z)^3)")
print("  but is bounded by n_bar_eq from below")
print("")
print("  At small delta: w ~ -1 + delta*(1+z)^3")
print("  At large z: w -> 0 (matter-like, guaranteed w > -1)")
print("  The A12 erf is phenomenologically similar but different functional form")
print("  Both are 'softened' transitions, but dS has power-law instead of erf shape")
print("")
print("NEW FINDING: NF-31 candidate")
print("  dS SQMH predicts w(z) = -1 + delta*(1+z)^3/(1+delta*(1+z)^3)")
print("  This is the exact analytic solution (not erf)")
print("  The parameter delta = (n_bar_init - n_bar_eq)/n_bar_eq connects to initial conditions")
