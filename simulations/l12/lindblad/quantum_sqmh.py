"""
simulations/l12/lindblad/quantum_sqmh.py
L12-L: Lindblad quantum SQMH simulation

Computes:
1. Quantum variance <delta_n^2> from Lindblad master equation
2. Quantum correction delta_w to equation of state
3. CMB f_NL contribution
4. Decoherence timescale

All print() statements use ASCII only (CLAUDE.md rule).
"""

import numpy as np
from scipy.integrate import solve_ivp

# ===== CONSTANTS (SI) =====
G = 6.674e-11          # m^3/(kg*s^2)
c = 2.998e8            # m/s
hbar = 1.055e-34       # J*s
k_B = 1.381e-23        # J/K
t_P = 5.391e-44        # s (Planck time)
l_P = 1.616e-35        # m (Planck length)
m_P = 2.176e-8         # kg (Planck mass)
Mpc = 3.0857e22        # m

# SQMH parameters
sigma = 4.0 * np.pi * G * t_P  # m^3/(kg*s) = 4.52e-53
H0_si = 67400.0 / Mpc          # s^-1 = 2.184e-18 s^-1
Omega_m = 0.315
Omega_L = 0.685

# Derived
rho_crit0 = 3.0 * H0_si**2 / (8.0 * np.pi * G)
rho_m0 = Omega_m * rho_crit0

# SQMH equilibrium n_bar at z=0
# n_bar_eq = Gamma_0 / (3*H + sigma*rho_m)
# Since sigma*rho_m << 3H, n_bar_eq ~ Gamma_0/(3*H)
# Total dark energy quanta in Hubble volume:
# rho_DE = Gamma_0/(3*H) * m_P / V_Hubble ... complex.
# Instead use directly: N_bar = total quanta in Hubble volume
V_Hubble = (c / H0_si)**3
rho_P = m_P / l_P**3  # Planck density ~ 5.155e96 kg/m^3
Gamma_0_over_sigma = rho_P  # Gamma_0/sigma = n0*mu ~ rho_Planck

Gamma_0 = sigma * rho_P  # = 4*pi*G*t_P * rho_P = 4*pi*G*m_P/l_P^3

# n_bar at z=0
n_bar0 = Gamma_0 / (3.0 * H0_si)  # quanta/m^3

# Total quanta in Hubble volume
N_bar = n_bar0 * V_Hubble

Pi_SQMH = sigma * rho_m0 / (3.0 * H0_si)

print("="*60)
print("L12-L: Lindblad Quantum SQMH")
print("="*60)
print("")
print("--- Key constants ---")
print("sigma = %.3e m^3/(kg*s)" % sigma)
print("H0 = %.3e s^-1" % H0_si)
print("rho_m0 = %.3e kg/m^3" % rho_m0)
print("Gamma_0 = %.3e s^-1/m^3 * (some units)" % Gamma_0)
print("n_bar0 = %.3e quanta/m^3" % n_bar0)
print("V_Hubble = %.3e m^3" % V_Hubble)
print("N_bar = %.3e quanta in Hubble vol" % N_bar)
print("Pi_SQMH = sigma*rho_m0/(3*H0) = %.3e" % Pi_SQMH)
print("")

# ===== 1. LINDBLAD QUANTUM VARIANCE =====
# Steady-state quantum variance from Lindblad:
# <delta_n^2>_ss = (Gamma_0 + sigma*rho_m0*n_bar0) / (2*(sigma*rho_m0 + 3*H0))
#                ~ Gamma_0 / (6*H0)  = n_bar0/2 (Poisson)
decay_rate = sigma * rho_m0 + 3.0 * H0_si
var_ss = (Gamma_0 + sigma * rho_m0 * n_bar0) / (2.0 * decay_rate)
var_classical = n_bar0 / 2.0  # Poisson baseline

print("--- 1. Quantum Variance (steady state) ---")
print("Variance_ss = %.3e quanta^2/m^6" % var_ss)
print("Poisson floor = n_bar/2 = %.3e" % var_classical)
print("Ratio var_ss/var_Poisson = %.6f" % (var_ss / var_classical))
print("  -> Quantum variance = Poisson (no enhancement)")
print("")

# ===== 2. QUANTUM CORRECTION TO w =====
# delta_rho_DE/rho_DE ~ sqrt(var_ss)/n_bar0 (per unit volume)
# delta_w_quantum ~ Pi_SQMH * delta_rho_DE/rho_DE
delta_rho_over_rho = np.sqrt(var_ss) / n_bar0
delta_w_quantum = Pi_SQMH * delta_rho_over_rho

print("--- 2. Quantum correction to w ---")
print("delta_rho/rho = sqrt(var)/n_bar = %.3e" % delta_rho_over_rho)
print("delta_w_quantum = Pi_SQMH * delta_rho/rho = %.3e" % delta_w_quantum)
print("K71 threshold: 1e-60")
print("K71 triggered: %s" % ("YES (KILL)" if delta_w_quantum < 1e-60 else "NO (KEEP)"))
print("")

# ===== 3. f_NL CONTRIBUTION =====
# CMB scale: z_CMB = 1100
z_CMB = 1100.0
E_CMB = np.sqrt(Omega_m * (1.0 + z_CMB)**3 + Omega_L)
H_CMB = H0_si * E_CMB
n_bar_CMB = Gamma_0 / (3.0 * H_CMB)

V_Hubble_CMB = (c / H_CMB)**3
N_bar_CMB = n_bar_CMB * V_Hubble_CMB

# delta_zeta_SQMH
delta_zeta_CMB_observed = 5.0e-5  # observed amplitude
delta_zeta_SQMH = Pi_SQMH / np.sqrt(N_bar_CMB)  # rough estimate

# f_NL contribution (order of magnitude)
f_NL_SQMH = delta_zeta_SQMH / delta_zeta_CMB_observed**2

print("--- 3. CMB f_NL contribution ---")
print("At z_CMB = 1100:")
print("  E(1100) = %.3e" % E_CMB)
print("  H(1100) = %.3e s^-1" % H_CMB)
print("  n_bar(1100) = %.3e quanta/m^3" % n_bar_CMB)
print("  N_bar(1100) = %.3e quanta in Hubble vol" % N_bar_CMB)
print("  delta_zeta_SQMH = %.3e" % delta_zeta_SQMH)
print("  f_NL_SQMH = %.3e" % f_NL_SQMH)
print("  Planck limit: |f_NL| < 5")
print("  Euclid target: |f_NL| < 1")
print("  Gap: 1e0/%.3e = %.3e" % (abs(f_NL_SQMH), 1.0/abs(f_NL_SQMH) if abs(f_NL_SQMH) > 0 else np.inf))
print("")

# ===== 4. DECOHERENCE TIMESCALE =====
# Decoherence rate between adjacent Fock states |n> and |n+1>:
# Gamma_deco = (Gamma_0 + sigma*rho_m*n_bar)/(2*n_bar)
# tau_deco = 1/Gamma_deco

Gamma_deco = (Gamma_0 + sigma * rho_m0 * n_bar0) / (2.0 * n_bar0)
tau_deco = 1.0 / Gamma_deco
tau_Hubble = 1.0 / H0_si

print("--- 4. Decoherence timescale ---")
print("Gamma_deco (adjacent Fock) = %.3e s^-1" % Gamma_deco)
print("tau_deco = %.3e s" % tau_deco)
print("tau_Hubble = 1/H0 = %.3e s" % tau_Hubble)
print("tau_deco / tau_Hubble = %.3e" % (tau_deco / tau_Hubble))
print("")

# Key finding (Member 7): decoherence at ~Hubble timescale?
# Gamma_deco ~ Gamma_0/(2*n_bar0) = (3*H0*n_bar0)/(2*n_bar0) = 3*H0/2
Gamma_deco_approx = 3.0 * H0_si / 2.0
tau_deco_approx = 1.0 / Gamma_deco_approx
print("Approximate decoherence rate = 3*H0/2 = %.3e s^-1" % Gamma_deco_approx)
print("tau_deco_approx = 2/(3*H0) = %.3e s" % tau_deco_approx)
print("tau_deco_approx / tau_Hubble = %.3f" % (tau_deco_approx / tau_Hubble))
print("  -> STRUCTURAL RESULT: SQMH quanta decohere on ~Hubble timescale!")
print("  -> Quantum-to-classical transition at cosmological scales.")
print("")

# ===== 5. NON-MARKOVIAN CORRECTION =====
# Memory timescale ~ t_P
gamma_mem = 1.0 / t_P
correction_NM = (H0_si / gamma_mem)**2  # ~ (H0*t_P)^2 ~ Pi_SQMH^2
print("--- 5. Non-Markovian correction ---")
print("Memory timescale = t_P = %.3e s" % t_P)
print("gamma_mem = 1/t_P = %.3e s^-1" % gamma_mem)
print("NM correction ~ (H0*t_P)^2 = %.3e" % correction_NM)
print("Pi_SQMH^2 = %.3e" % Pi_SQMH**2)
print("  -> NM corrections even smaller than Markovian")
print("")

# ===== 6. LINDBLAD DENSITY MATRIX EVOLUTION (truncated Fock space) =====
# Evolve small density matrix in Fock space {|0>, |1>, ..., |N_max>}
# for illustration of quantum dynamics
print("--- 6. Lindblad density matrix evolution (Fock space N_max=10) ---")
N_max = 10
n_bar_toy = 3.0  # toy value for demo

# Gamma_creation and Gamma_annihilation for toy model
# n_bar_toy = Gamma_creation/(Gamma_annihilation) for balance
Gamma_cr = 3.0   # creation rate (s^-1)
Gamma_an = 1.0   # annihilation rate per quantum (s^-1)

def lindblad_rhs(t, rho_flat):
    """Lindblad master equation RHS for truncated Fock space."""
    rho = rho_flat.reshape(N_max+1, N_max+1)
    L = np.zeros_like(rho)

    # L1 = sqrt(Gamma_cr) * a_dagger (creation)
    # L2 = sqrt(Gamma_an) * a (annihilation)
    for n in range(N_max+1):
        for m in range(N_max+1):
            # L1 rho L1^dag term
            if n > 0 and m > 0:
                L[n, m] += Gamma_cr * np.sqrt(n * m) * rho[n-1, m-1]
            # -1/2 (L1^dag L1 rho + rho L1^dag L1) term
            L[n, m] -= 0.5 * Gamma_cr * (n + m) * rho[n, m]  # simplified
            # Wait - L1^dag L1 = Gamma_cr * a a^dag = Gamma_cr * (N+1)
            # The diagonal term should be -Gamma_cr * (n+m+2) / 2 * rho[n,m]
            # But let's do exact:

    # Redo with correct formulas
    L = np.zeros_like(rho)
    for n in range(N_max+1):
        for m in range(N_max+1):
            # Creation: L1 rho L1^dag where L1 = sqrt(Gamma_cr) * a^dag
            # (L1 rho L1^dag)_{nm} = Gamma_cr * sqrt((n+1)*(m+1)) * rho[n,m] ?
            # Actually: L1 = sqrt(Gamma_cr)*a^dag, so (L1)_{n,n-1} = sqrt(Gamma_cr)*sqrt(n)
            # L1 rho L1^dag has elements:
            # sum_{k} (L1)_{nk} rho_{kl} (L1^dag)_{lm} = Gamma_cr * sqrt(n*m) * rho[n-1,m-1]
            if n > 0 and m > 0:
                L[n, m] += Gamma_cr * np.sqrt(float(n * m)) * rho[n-1, m-1]
            # -1/2 L1^dag L1 rho: L1^dag L1 = Gamma_cr * a a^dag = Gamma_cr*(N+1)
            # (L1^dag L1 rho)_{nm} = Gamma_cr*(n+1)*rho[n,m]
            L[n, m] -= 0.5 * Gamma_cr * (n + 1) * rho[n, m]
            # -1/2 rho L1^dag L1: (rho L1^dag L1)_{nm} = Gamma_cr*(m+1)*rho[n,m]
            L[n, m] -= 0.5 * Gamma_cr * (m + 1) * rho[n, m]

            # Annihilation: L2 rho L2^dag where L2 = sqrt(Gamma_an) * a
            # (L2 rho L2^dag)_{nm} = Gamma_an * sqrt((n+1)*(m+1)) * rho[n+1,m+1]
            if n < N_max and m < N_max:
                L[n, m] += Gamma_an * np.sqrt(float((n+1)*(m+1))) * rho[n+1, m+1]
            # -1/2 L2^dag L2 rho: L2^dag L2 = Gamma_an * N
            # (L2^dag L2 rho)_{nm} = Gamma_an*n*rho[n,m]
            L[n, m] -= 0.5 * Gamma_an * n * rho[n, m]
            # -1/2 rho L2^dag L2: = Gamma_an*m*rho[n,m]
            L[n, m] -= 0.5 * Gamma_an * m * rho[n, m]

    return L.flatten()

# Initial state: vacuum |0><0|
rho0 = np.zeros((N_max+1, N_max+1))
rho0[0, 0] = 1.0

# Evolve
t_span = (0.0, 10.0)
t_eval = np.linspace(0, 10, 100)
sol = solve_ivp(lindblad_rhs, t_span, rho0.flatten(), t_eval=t_eval, method='RK45',
                rtol=1e-8, atol=1e-10)

# Extract <n> and <delta_n^2>
n_values = np.arange(N_max+1)
n_mean = []
n_var = []
for i in range(len(t_eval)):
    rho_t = sol.y[:, i].reshape(N_max+1, N_max+1)
    rho_diag = np.real(np.diag(rho_t))
    mean_n = np.sum(n_values * rho_diag)
    mean_n2 = np.sum(n_values**2 * rho_diag)
    n_mean.append(mean_n)
    n_var.append(mean_n2 - mean_n**2)

n_mean = np.array(n_mean)
n_var = np.array(n_var)

# Theoretical steady state
n_bar_th = Gamma_cr / Gamma_an  # steady state mean
var_th = n_bar_th  # Poisson

print("Toy model: Gamma_cr=%.1f, Gamma_an=%.1f" % (Gamma_cr, Gamma_an))
print("Theoretical steady state: n_bar = Gamma_cr/Gamma_an = %.1f" % n_bar_th)
print("Final numerical: <n> = %.4f (at t=10)" % n_mean[-1])
print("Theoretical variance (Poisson) = n_bar = %.1f" % var_th)
print("Final numerical: Var(n) = %.4f (at t=10)" % n_var[-1])
print("Ratio Var(n)/n_bar = %.4f (should be ~1 for Poisson)" % (n_var[-1]/n_bar_th))
print("")

# ===== FINAL VERDICTS =====
print("="*60)
print("FINAL VERDICTS")
print("="*60)
print("")
print("K71 (delta_w_quantum < 1e-60): TRIGGERED")
print("  delta_w_quantum = %.3e << 1e-60" % delta_w_quantum)
print("")
print("Q71 (delta_w_quantum > 1e-30): FAIL")
print("  delta_w_quantum = %.3e << 1e-30" % delta_w_quantum)
print("")
print("STRUCTURAL FINDING (NF-30 candidate):")
print("  tau_deco ~ 2/(3*H0) ~ Hubble time")
print("  SQMH quanta decohere on cosmological timescales")
print("  Quantum-to-classical transition at Hubble scale")
print("  f_NL contribution ~ %.3e" % f_NL_SQMH)
print("")
print("CONCLUSION: Lindblad quantum SQMH is cosmologically irrelevant.")
print("  No quantum enhancement beyond classical Poisson floor.")
print("  K71 triggered. Q71 fails.")
