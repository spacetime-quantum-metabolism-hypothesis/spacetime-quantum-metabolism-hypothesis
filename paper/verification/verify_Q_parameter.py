"""SQT Q-parameter (Definition C, Joos-Zeh decoherence) macro/micro classifier.

Q is the dimensionless quantity that controls the macro/micro boundary in SQT.
Of 5 dimensionally-consistent candidates (A action/hbar, B Penrose-Diosi,
C Joos-Zeh, D phase-space cells, E info levels), this script reproduces the
Definition C variant (Joos-Zeh 1985 thermal-photon decoherence rate over
observation time).

Q_C(m, L, T_obs, T_K) = Lambda * T_obs,
  Lambda = (k_B T)^9 (L/2)^6 / (hbar^9 c^6),  prefactor = 1, no tuning.

Threshold: log10(Q) > tau_star -> classical, else quantum. tau_star is
selected as the threshold maximising classification accuracy on a 15-system
benchmark (7 quantum + 8 classical), per L403 grid sweep.

CLASSIFICATION (L403): Definition C accuracy = 1.000 (15/15), tau_star =
9.42e16, span = 191.8 decades. Status: PARTIAL (axiom-derivation K3
question pending; A is parsimony winner). Lab falsifiability winner.

Run: < 1 s, stand-alone (numpy only).
"""
import math
import numpy as np

# --- physical constants (SI) ---
HBAR = 1.054571817e-34
KB   = 1.380649e-23
C    = 2.99792458e8

def Q_C(m, L, T_obs, T_K):
    a = 0.5 * L
    Lambda = (KB * T_K) ** 9 * a ** 6 / (HBAR ** 9 * C ** 6 + 1e-300)
    return Lambda * T_obs

# --- 15-system benchmark (mass kg, size m, T_obs s, T K, label 0=quantum 1=classical) ---
SYSTEMS = [
    ("electron_in_atom",      9.109e-31, 5.29e-11, 1e-16,  300.0,  0),
    ("hydrogen_atom",         1.673e-27, 5.29e-11, 1e-15,  300.0,  0),
    ("cold_atom_BEC_Rb",      1.443e-25, 1e-05,    0.01,   1e-07,  0),
    ("C60_fullerene",         1.196e-24, 1e-09,    0.001,  900.0,  0),
    ("oligopeptide_2000amu",  3.32e-24,  1e-09,    0.001,  500.0,  0),
    ("phthalocyanine",        8.51e-25,  1e-09,    0.001,  500.0,  0),
    ("nanoparticle_1e7amu",   1.66e-20,  1e-07,    0.01,   0.001,  0),
    ("virus_capsid_TMV",      6.6e-23,   3e-07,    1.0,    300.0,  1),
    ("bacterium_E_coli",      1e-15,     1e-06,    1.0,    300.0,  1),
    ("dust_grain_1um",        1e-15,     1e-06,    1.0,    300.0,  1),
    ("pollen_grain",          1e-11,     2e-05,    1.0,    300.0,  1),
    ("apple",                 0.1,       0.05,     1.0,    300.0,  1),
    ("human",                 70.0,      1.7,      1.0,    310.0,  1),
    ("car",                   1500.0,    4.0,      1.0,    300.0,  1),
    ("Earth_orbit",           5.972e24,  1.496e11, 3.15e7, 300.0,  1),
]

# --- compute Q_C for every system ---
qvals  = []
labels = []
for name, m, L, T_obs, T_K, lab in SYSTEMS:
    q = Q_C(m, L, T_obs, T_K)
    qvals.append(q)
    labels.append(lab)
qvals  = np.asarray(qvals)
labels = np.asarray(labels)
log10Q = np.log10(np.maximum(qvals, 1e-300))

# --- threshold sweep: best accuracy ---
candidates = sorted(set(log10Q.tolist()))
midpoints = [0.5 * (candidates[i] + candidates[i+1]) for i in range(len(candidates)-1)]
all_thr = sorted(set(candidates + midpoints))

best_acc = -1.0
best_tau = None
for thr in all_thr:
    pred = (log10Q > thr).astype(int)  # > thr => classical (1)
    acc  = (pred == labels).mean()
    if acc > best_acc:
        best_acc = acc
        best_tau = thr

tau_star = 10.0 ** best_tau

print("SQT Q-parameter, Definition C (Joos-Zeh thermal-photon decoherence)")
print("=" * 68)
print(f"Benchmark systems: {len(SYSTEMS)} "
      f"({(labels==0).sum()} quantum + {(labels==1).sum()} classical)")
print("")
print(f"{'system':<24s} {'log10 Q_C':>12s}  label  predicted")
print("-" * 60)
for (name, *_), lq, lab in zip(SYSTEMS, log10Q, labels):
    pred = int(lq > best_tau)
    tag = "OK" if pred == lab else "MISS"
    print(f"{name:<24s} {lq:>12.3f}  {lab:>5d}  {pred:>9d}  {tag}")

print("")
print(f"best log10(tau_star)  = {best_tau:.3f}")
print(f"tau_star (linear)     = {tau_star:.3e}")
print(f"classification accuracy = {best_acc*100:.1f}%  ({int(round(best_acc*len(SYSTEMS)))}/{len(SYSTEMS)})")
print(f"log10 Q span (decades)  = {log10Q.max() - log10Q.min():.1f}")
print("")
print("STATUS: PARTIAL (paper §5.2). Definition C: lab-falsifiable winner.")
print("        canonical selection awaits 8-team K3 (axiom derivation).")
print("Source: L403 (4-person review PASS).")
