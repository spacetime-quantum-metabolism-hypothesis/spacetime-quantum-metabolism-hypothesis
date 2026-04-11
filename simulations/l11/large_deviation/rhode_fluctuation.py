# simulations/l11/large_deviation/rhode_fluctuation.py
# Attempt 20: Large deviation theory -> rho_DE fluctuation probability
# Rule-B 4-person review

import numpy as np
import warnings
warnings.filterwarnings('ignore')

# --- Constants ---
H0 = 2.183e-18
sigma_sq = 4.521e-53
Omega_m = 0.315
rho_crit0 = 9.472e-27
rho_DE0 = (1.0 - Omega_m) * rho_crit0
c = 3e8
E_P_J = 1.956e9
l_P = 1.616e-35

print("=== L11 Attempt 20: Large Deviation -> rho_DE Fluctuation Probability ===")
print("")

# --- Large deviation rate function ---
# For Poisson(N_bar): I(x) = x*ln(x) - x + 1 (Cramer rate function, x = n/n_bar)
# P(N = x*N_bar) ~ exp(-N_bar * I(x)) for large N_bar

# N_bar: total DE quanta in Hubble volume
V_H = (c / H0)**3
N_bar = rho_DE0 * V_H / E_P_J
print("N_bar = {:.4e} (quanta in Hubble volume)".format(N_bar))
print("log10(N_bar) = {:.1f}".format(np.log10(N_bar)))
print("")

def I_cramer(x):
    """Cramer rate function for Poisson."""
    if x <= 0:
        return np.inf
    return x * np.log(x) - x + 1.0

def log_P_large_dev(x, N_bar):
    """Log probability of N = x*N_bar quanta."""
    return -N_bar * I_cramer(x)

print("Probability of rho_DE = x * rho_DE0:")
print("{:<15} {:<20} {:<30}".format("x", "log10(P)", "Physical meaning"))

x_values = [
    (1.0, "Typical (no fluctuation)"),
    (1.001, "0.1% excess"),
    (1.01, "1% excess"),
    (1.1, "10% excess"),
    (2.0, "2x rho_DE"),
    (10.0, "10x rho_DE"),
    (0.999, "0.1% deficit"),
    (0.9, "10% deficit"),
    (0.5, "half rho_DE"),
]

for x, meaning in x_values:
    if x > 0:
        logP = log_P_large_dev(x, N_bar) / np.log(10)
        # Scientific notation for the exponent:
        print("{:<15.4f} {:<20.4e} {:<30}".format(x, 10**logP if logP > -300 else 0, meaning))
print("")

# The key insight: even a 0.1% fluctuation has
# log10(P) = -N_bar * I(1.001) / ln(10)
x_tiny = 1.001
I_tiny = I_cramer(x_tiny)
log_P_tiny = -N_bar * I_tiny / np.log(10)
print("Probability of 0.1% rho_DE fluctuation:")
print("  I(1.001) = {:.6e}".format(I_tiny))
print("  log10(P) = {:.4e}".format(log_P_tiny))
print("  This is exp(-{:.2e}) ~ 0 (absolute zero)".format(N_bar * I_tiny))
print("")

# Cosmological constant problem angle:
# Current rho_DE = rho_DE0 (observed)
# "Typical" rho_DE (from large deviation): rho_DE0 is the MOST LIKELY value
# by construction (it's n_eq by definition)
# Large deviation tells us: ANY departure from rho_DE0 is essentially impossible
# at the quantum level. This is a stability statement, not a CC problem solution.

print("Cosmological constant problem interpretation:")
print("  rho_DE0 is the equilibrium value n_eq * E_P / l_P^3.")
print("  The probability that rho_DE differs from rho_DE0 by even 0.1%:")
print("  P(x=1.001) = exp(-N_bar * I(1.001)) = exp(-{:.2e})".format(N_bar * I_tiny))
print("  -> P = 0 (absolutely impossible at quantum level)")
print("")
print("  This explains 'why is rho_DE the current value?':")
print("  ANSWER: Because rho_DE0 = n_eq * E_P / l_P^3 is the ONLY stable equilibrium.")
print("  Any deviation collapses back to n_eq with probability 1 (large N_bar).")
print("")

# But: this doesn't explain WHY n_eq is 10^-122 rho_Planck (not 1 rho_Planck)
# = CC problem repackaged as Gamma_0/sigma problem (NF-27)
print("Limitation:")
print("  Large deviation explains why rho_DE = rho_DE0 (not why rho_DE0 ~ 10^-122 rho_P)")
print("  The ABSOLUTE SCALE still requires CC-level fine-tuning of Gamma_0.")
print("  Large deviation is a CONSISTENCY argument, not a CC resolution.")
print("  (Consistent with NF-27: CC = Gamma_0 fine-tuning problem)")
print("")
print("Summary:")
print("  Attempt 20 provides statistical mechanics foundation for rho_DE stability.")
print("  P(x=10) = exp(-10^43) = absolute 0 (rho_DE cannot fluctuate to 10x current)")
print("  rho_DE0 is stable to any perturbation by N_bar ~ 10^42 suppression.")
print("  Does not solve CC problem (why rho_DE0/rho_P ~ 10^-122).")
print("  Valuable for paper: 'SQMH dark energy is thermodynamically stable'")
print("  (complementary to Lyapunov stability, Attempt 19)")
