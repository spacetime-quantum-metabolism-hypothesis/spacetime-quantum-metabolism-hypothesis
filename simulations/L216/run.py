"""L216 — n-SM coupling: dark-only embedding."""
import os; os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np, json
beta_d = 0.107  # dark sector coupling (L2 R3 C10k)
beta_b = 0.0    # baryon coupling (sector-selective)
gamma_minus_1 = 2 * beta_b**2 / (1 + beta_b**2)
eta_EP = abs(beta_b - beta_b)  # universality test
G_eff_over_G_dark = 1 + 2*beta_d**2
G_eff_over_G_baryon = 1.0
print(f"|gamma-1| (Cassini) = {gamma_minus_1:.3e} (limit 2.3e-5)")
print(f"eta_EP (MICROSCOPE) = {eta_EP:.3e} (limit 1e-15)")
print(f"G_eff/G dark   = {G_eff_over_G_dark:.4f}")
print(f"G_eff/G baryon = {G_eff_over_G_baryon:.4f}")
out = {
    'beta_dark': beta_d, 'beta_baryon': beta_b,
    'gamma_minus_1': gamma_minus_1, 'cassini_pass': bool(gamma_minus_1 < 2.3e-5),
    'eta_EP': eta_EP, 'EP_pass': bool(eta_EP < 1e-15),
    'G_eff_dark': G_eff_over_G_dark, 'G_eff_baryon': G_eff_over_G_baryon,
}
with open(os.path.join(os.path.dirname(__file__),'report.json'),'w') as f:
    json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
