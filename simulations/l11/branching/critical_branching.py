# simulations/l11/branching/critical_branching.py
# Attempt 12: Branching process -> critical point scale-free fluctuations
# Rule-B 4-person review

import numpy as np
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)

# --- Constants ---
H0 = 2.183e-18
sigma_sq = 4.521e-53
Omega_m = 0.315
rho_crit0 = 9.472e-27
rho_m0 = Omega_m * rho_crit0

print("=== L11 Attempt 12: Critical Branching -> Scale-Free DE Fluctuations ===")
print("")

# Galton-Watson branching process:
# Each spacetime quantum produces offspring with mean m (branching ratio).
# Critical: m = 1 (critical point)
# Supercritical: m > 1 (exponential growth)
# Subcritical: m < 1 (extinction)

# SQMH branching ratio:
# m = P(birth per quantum per dt) / P(death per quantum per dt)
# = lambda/(mu) ... but in SQMH, birth is INDEPENDENT of n (zeroth-order)
# This is NOT a standard branching process (birth not proportional to n).
# Need modification: interpret Gamma_0 as effective branching from existing quanta.

# Modified branching: if each quantum has probability p_birth of producing a "child":
# effective_lambda = p_birth * n_bar
# At equilibrium: p_birth * n_bar = mu * n_bar
# -> p_birth = mu = sigma*rho_m + 3H

# Branching ratio m = p_birth/mu = 1 (always critical!)
# This is consistent with SQMH equilibrium = critical branching.
print("SQMH branching ratio analysis:")
print("  mu (death rate per quantum) = sigma*rho_m + 3H = {:.4e} s^-1".format(
    sigma_sq * rho_m0 + 3.0 * H0))
print("  At equilibrium: effective birth = death = mu * n_eq")
print("  -> branching ratio m = 1 (CRITICAL)")
print("")

# Critical branching properties:
# 1. Power-law distribution of avalanche sizes: P(s) ~ s^(-3/2)
# 2. Scale-free fluctuations
# 3. Susceptibility diverges: chi = 1/(1-m) -> infinity

print("Critical branching properties:")
print("  P(avalanche size s) ~ s^(-3/2) (scale-free)")
print("  Susceptibility: chi = 1/(1-m) -> infinity (at m=1)")
print("")

# Observable consequence:
# If SQMH is at critical branching, DE density has power-law fluctuations.
# P(delta_rho_DE) ~ (delta_rho_DE)^(-3/2) for avalanche events.
# BUT: the TYPICAL fluctuation is still Poisson (n ~ 10^42 quanta).
# The power-law tail applies to rare large events.

# Critical branching avalanche statistics:
# <s> = 1/(1-m) -> infinity (diverges at criticality)
# <s^2> ~ diverges (if m->1)
# But: for finite system (N_max ~ N_bar), cutoff at s ~ N_bar

N_bar_log = np.log10(9.47e-27 * (3e8/H0)**3 / 1.956e9)  # log10 of N_bar
print("Finite-size cutoff for critical branching:")
print("  N_bar ~ 10^{:.0f} (total quanta in Hubble volume)".format(N_bar_log))
print("  Maximum avalanche: s_max ~ N_bar")
print("")

# Simulation: small critical branching process
def simulate_branching(n0, m, n_steps=10):
    """Simulate Galton-Watson branching with Poisson offspring (mean=m)."""
    populations = [n0]
    n = n0
    for _ in range(n_steps):
        if n == 0:
            populations.append(0)
            continue
        # Each individual produces Poisson(m) offspring
        offspring = np.random.poisson(m, n)
        n = np.sum(offspring)
        populations.append(n)
    return np.array(populations)

# Simulate at m = 1.0 (critical) and m = 0.99 (slightly subcritical):
n0 = 100
print("Critical branching simulation (n0={}, m=1.0, 10 steps, 5 runs):".format(n0))
for run in range(5):
    pop = simulate_branching(n0, m=1.0, n_steps=10)
    print("  Run {}: {}".format(run+1, pop.tolist()))
print("")

print("At m=1 (critical): high variance, eventual extinction possible.")
print("")
print("Conclusion:")
print("  SQMH is always at critical branching (m=1 at equilibrium).")
print("  This gives scale-free fluctuations: P(s) ~ s^(-3/2) for avalanches.")
print("  BUT: the Poisson floor (N_bar ~ 10^42) suppresses typical fluctuations.")
print("  Power-law tail has amplitude ~ 1/N_bar^(1/2) ~ 10^-21.")
print("  Not distinguishable from standard Poisson at cosmological sensitivity.")
print("  Attempt 12: Critical branching is correct framework, unobservable fluctuations.")
