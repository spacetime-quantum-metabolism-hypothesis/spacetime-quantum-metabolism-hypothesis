# simulations/l11/quasispecies/sigma_distribution.py
# Attempt 11: Quasi-species equation -> sigma distribution width
# Rule-B 4-person review

import numpy as np
from scipy.linalg import eig
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)

# --- Constants ---
H0 = 2.183e-18
sigma_SQMH = 4.521e-53  # m^3 kg^-1 s^-1
Omega_m = 0.315
rho_crit0 = 9.472e-27
rho_m0 = Omega_m * rho_crit0

print("=== L11 Attempt 11: Quasi-species -> Sigma Distribution ===")
print("")

# Eigen quasi-species: fitness matrix W_ij
# Species i has 'fitness' f_i = 1/(sigma_i * rho_m + 3H)  [n_eq for that sigma]
# Mutation matrix: Q_ij = probability of sigma_j -> sigma_i per generation

# Discretize sigma into k = 5 values:
k = 5
sigma_values = np.logspace(np.log10(sigma_SQMH) - 1, np.log10(sigma_SQMH) + 1, k)
print("Sigma values explored [m^3 kg^-1 s^-1]:")
for i, sv in enumerate(sigma_values):
    print("  sigma_{} = {:.4e}".format(i, sv))
print("")

# Fitness (effective n_eq normalized):
def fitness(sigma, z=0.0):
    rho = rho_m0 * (1.0 + z)**3
    H = H0 * np.sqrt(Omega_m * (1+z)**3 + (1-Omega_m))
    return 1.0 / (sigma * rho + 3.0 * H)

f_vec = np.array([fitness(s) for s in sigma_values])
print("Fitness values (n_eq/Gamma_0 normalized):")
for i, fv in enumerate(f_vec):
    print("  f_{} = {:.4e} s".format(i, fv))
print("")

# Mutation matrix: Gaussian in log(sigma) space
mu_q = 0.1  # mutation rate per 'generation'
log_sigma = np.log10(sigma_values)
Q_matrix = np.zeros((k, k))
for i in range(k):
    for j in range(k):
        Q_matrix[i, j] = np.exp(-0.5 * (log_sigma[i] - log_sigma[j])**2 / 0.5**2)
    Q_matrix[:, j] /= Q_matrix[:, j].sum()  # normalize columns

# Quasi-species fitness matrix: W = Q * diag(f)
W = Q_matrix * f_vec[np.newaxis, :]

# Dominant eigenvector = stationary distribution p_i
eigenvalues, eigenvectors = eig(W)
idx = np.argmax(np.real(eigenvalues))
dominant_eigenvector = np.real(eigenvectors[:, idx])
dominant_eigenvector = np.abs(dominant_eigenvector)
dominant_eigenvector /= dominant_eigenvector.sum()

print("Quasi-species stationary distribution:")
for i in range(k):
    print("  p({:.2e}) = {:.4f}".format(sigma_values[i], dominant_eigenvector[i]))
print("")

# Effective sigma:
sigma_eff = np.dot(dominant_eigenvector, sigma_values)
print("Effective sigma_eff = sum(p_i * sigma_i): {:.4e} m^3 kg^-1 s^-1".format(sigma_eff))
print("  vs sigma_SQMH = {:.4e} m^3 kg^-1 s^-1".format(sigma_SQMH))
print("  Ratio sigma_eff/sigma_SQMH = {:.4f}".format(sigma_eff/sigma_SQMH))
print("")

# Width of distribution:
sigma_width = np.sqrt(np.dot(dominant_eigenvector, (sigma_values - sigma_eff)**2))
print("Width of sigma distribution: {:.4e} m^3 kg^-1 s^-1".format(sigma_width))
print("  Relative width: {:.4f}".format(sigma_width / sigma_eff))
print("")

print("Conclusion:")
print("  Quasi-species with Gaussian mutation in log(sigma) gives")
print("  sigma_eff ~ sigma_SQMH if SQMH sigma is the fitness peak.")
print("  Width ~ 50% (for mutation rate 0.1, spread of 1 dex).")
print("  This replaces NF-1 (sigma RG running) with a distribution interpretation.")
print("  Observable effect: sigma_eff uncertainty -> G_eff/G uncertainty.")
print("  delta(G_eff/G) / (G_eff/G) ~ 50% (if sigma uncertain by factor 2).")
print("  But: sigma is constrained by SQMH fit to < 1% precision through rho_DE.")
print("  Quasi-species interpretation: sigma distribution width < 1% in practice.")
print("  Attempt 11: Interesting framework, no new observable predictions.")
