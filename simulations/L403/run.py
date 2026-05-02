"""
L403 — Q parameter (quantum-classical transition) canonical definition scan.

Independent session. CLAUDE.md compliance:
  [최우선-1] 방향만, 지도 금지 — this script lists *named directions* only:
      A) action over hbar               (Bohr correspondence direction)
      B) mass-localisation              (Penrose-Diosi gravitational direction)
      C) decoherence rate over obs time (Joos-Zeh / Zurek direction)
      D) phase-space cell count         (Wigner / Liouville direction)
      E) entropy / level-count          (information-theoretic direction)
  No numerical coefficients are pre-fixed: each definition uses *only*
  fundamental constants (hbar, c, G, k_B) plus the system's own
  m, L, T_obs, T_kelvin. No tuning parameters.

  [최우선-2] team derives independently — this file only computes
  five named indicators on a grid and reports their *classification
  accuracy* against a benchmark labelling drawn from textbook examples.
  No "winner" is hard-coded.

Method
------
1. Build a benchmark set of physical systems with consensus
   classical/quantum status (electron in atom, C60 fullerene
   interferometry, viral capsid, dust grain, ..., apple, planet).
2. Compute Q_A..Q_E for each system from m, L, T_obs, T_K.
3. For each definition, scan threshold tau and find best
   classification accuracy (tau* maximises true labels recovered).
4. Report (i) accuracy, (ii) tau*, (iii) Q_macro / Q_micro span,
   (iv) hidden-DOF count = number of free dimensional choices
   (m, L, T_obs, T_K) the user must supply that are *not*
   determined by SQT axioms alone.

OUTPUT
------
results/L403/scan_table.csv  — per-system Q values
results/L403/scan_summary.json — accuracy + tau* + span per defn
"""

import json
import os
import math
import csv

# ----- fundamental constants (SI) -----
HBAR = 1.054571817e-34
C    = 2.99792458e8
G    = 6.67430e-11
KB   = 1.380649e-23

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "results", "L403")
os.makedirs(OUT_DIR, exist_ok=True)

# ----- benchmark set: (name, m_kg, L_m, T_obs_s, T_K, label)
# label: 0 = quantum, 1 = classical
# Sources: standard QM textbooks + matter-wave interferometry literature.
# Values are order-of-magnitude consensus, no fine-tuning.
SYSTEMS = [
    # quantum regime
    ("electron_in_atom",     9.109e-31, 5.29e-11, 1e-16, 300.0, 0),
    ("hydrogen_atom",        1.673e-27, 5.29e-11, 1e-15, 300.0, 0),
    ("cold_atom_BEC_Rb",     1.443e-25, 1e-5,    1e-2,   1e-7, 0),
    ("C60_fullerene",        1.196e-24, 1e-9,    1e-3,   900.0, 0),
    ("oligopeptide_2000amu", 3.32e-24,  1e-9,    1e-3,   500.0, 0),
    ("phthalocyanine",       8.51e-25,  1e-9,    1e-3,   500.0, 0),
    # borderline / target of mesoscopic experiments
    ("nanoparticle_1e7amu",  1.66e-20,  1e-7,    1e-2,   1e-3, 0),
    # classical regime
    ("virus_capsid_TMV",     6.6e-23,   3e-7,    1.0,    300.0, 1),
    ("bacterium_E_coli",     1e-15,     1e-6,    1.0,    300.0, 1),
    ("dust_grain_1um",       1e-15,     1e-6,    1.0,    300.0, 1),
    ("pollen_grain",         1e-11,     2e-5,    1.0,    300.0, 1),
    ("apple",                0.1,       0.05,    1.0,    300.0, 1),
    ("human",                70.0,      1.7,     1.0,    310.0, 1),
    ("car",                  1500.0,    4.0,     1.0,    300.0, 1),
    ("Earth_orbit",          5.972e24,  1.496e11,3.15e7, 300.0, 1),
]

# ----- 5 candidate Q definitions (named directions only, no coefficients) -----

def Q_A(m, L, T_obs, T_K):
    """Action-over-hbar direction. Use kinetic action of thermal motion."""
    p_th = math.sqrt(2.0 * m * KB * T_K)
    S = p_th * L
    return S / HBAR

def Q_B(m, L, T_obs, T_K):
    """Mass-localisation / Penrose-Diosi gravitational direction."""
    # decoherence time tau_PD = hbar / E_G, E_G ~ G m^2 / L
    E_G = G * m * m / L
    tau_PD = HBAR / max(E_G, 1e-300)
    return T_obs / tau_PD

def Q_C(m, L, T_obs, T_K):
    """Joos-Zeh / Zurek decoherence-rate-over-obs-time direction.
    Localisation rate by thermal photons: Lambda ~ a^2 (k_B T)^9 / ...
    We use scattering decoherence on thermal blackbody photons at T_K,
    Joos-Zeh form Lambda = (k_B T)^9 a^6 / hbar^9 c^6  (omitting numeric prefactor)
    with a = L/2.  prefactor is set to 1 (no tuning)."""
    a = 0.5 * L
    Lambda = (KB * T_K) ** 9 * a ** 6 / (HBAR ** 9 * C ** 6 + 1e-300)
    return Lambda * T_obs

def Q_D(m, L, T_obs, T_K):
    """Phase-space cell count direction (Wigner/Liouville).
    N_cell ~ (m * v_th * L)^3 / hbar^3, with v_th = sqrt(kT/m).
    """
    v_th = math.sqrt(KB * T_K / m)
    return (m * v_th * L) ** 3 / HBAR ** 3

def Q_E(m, L, T_obs, T_K):
    """Information-theoretic direction.
    Number of accessible energy levels ~ thermal energy / level spacing,
    level spacing ~ hbar^2 / (m L^2).  Q_E = ln(N_levels)."""
    delta_E = HBAR ** 2 / (m * L * L)
    Eth = KB * T_K
    N_levels = max(Eth / delta_E, 1.0)
    return math.log(N_levels)

DEFINITIONS = {
    "A_action_over_hbar":      Q_A,
    "B_penrose_diosi":         Q_B,
    "C_joos_zeh_decoherence":  Q_C,
    "D_phase_space_cells":     Q_D,
    "E_info_levels":           Q_E,
}

# ----- evaluate -----
rows = []
for name, m, L, T_obs, T_K, label in SYSTEMS:
    row = {"name": name, "m": m, "L": L, "T_obs": T_obs, "T_K": T_K, "label": label}
    for tag, fn in DEFINITIONS.items():
        try:
            row[tag] = fn(m, L, T_obs, T_K)
        except Exception as e:
            row[tag] = float("nan")
    rows.append(row)

# write CSV
csv_path = os.path.join(OUT_DIR, "scan_table.csv")
with open(csv_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    for r in rows:
        w.writerow(r)

# ----- classification accuracy via threshold sweep -----
def best_threshold(values, labels):
    """For Q indicator, sweep threshold tau in log-space; pick tau maximising
    accuracy where classical = (Q > tau)."""
    import numpy as np
    vals = np.array(values, dtype=float)
    labs = np.array(labels, dtype=int)
    finite = np.isfinite(vals)
    if finite.sum() < len(vals):
        return {"accuracy": None, "tau_star": None,
                "n_finite": int(finite.sum()), "n_total": len(vals)}
    log_v = np.log10(np.clip(vals, 1e-300, 1e300))
    candidates = np.unique(log_v)
    best_acc = -1.0
    best_tau = None
    for c in candidates:
        pred = (log_v > c).astype(int)
        acc = (pred == labs).mean()
        if acc > best_acc:
            best_acc = float(acc)
            best_tau = float(10.0 ** c)
    # also try midpoint between consecutive sorted unique values
    sv = np.sort(candidates)
    for i in range(len(sv) - 1):
        c = 0.5 * (sv[i] + sv[i + 1])
        pred = (log_v > c).astype(int)
        acc = (pred == labs).mean()
        if acc > best_acc:
            best_acc = float(acc)
            best_tau = float(10.0 ** c)
    return {"accuracy": best_acc, "tau_star": best_tau,
            "log10_min": float(log_v.min()),
            "log10_max": float(log_v.max()),
            "span_decades": float(log_v.max() - log_v.min())}

summary = {"n_systems": len(SYSTEMS),
           "n_quantum": sum(1 for s in SYSTEMS if s[5] == 0),
           "n_classical": sum(1 for s in SYSTEMS if s[5] == 1),
           "definitions": {}}

labels = [s[5] for s in SYSTEMS]
for tag in DEFINITIONS:
    vals = [r[tag] for r in rows]
    res = best_threshold(vals, labels)
    summary["definitions"][tag] = res

# rank by accuracy then by smaller span (parsimony)
ranked = sorted(summary["definitions"].items(),
                key=lambda kv: (-(kv[1].get("accuracy") or -1),
                                 kv[1].get("span_decades") or 1e9))
summary["ranking_accuracy_then_parsimony"] = [t for t, _ in ranked]

json_path = os.path.join(OUT_DIR, "scan_summary.json")
with open(json_path, "w") as f:
    json.dump(summary, f, indent=2)

# console report (ASCII only — cp949 safe)
print("=" * 60)
print("L403 Q-parameter canonical definition scan")
print("=" * 60)
print(f"systems: {summary['n_systems']} "
      f"(quantum {summary['n_quantum']}, classical {summary['n_classical']})")
print()
print(f"{'definition':30s} {'acc':>6s} {'tau*':>14s} {'span_dec':>10s}")
for tag, res in summary["definitions"].items():
    acc = res.get("accuracy")
    tau = res.get("tau_star")
    sp  = res.get("span_decades")
    acc_s = f"{acc:.3f}" if acc is not None else "  n/a"
    tau_s = f"{tau:.3e}" if tau is not None else "      n/a"
    sp_s  = f"{sp:.1f}"  if sp is not None else "  n/a"
    print(f"{tag:30s} {acc_s:>6s} {tau_s:>14s} {sp_s:>10s}")
print()
print("ranking (accuracy desc, span asc):")
for i, t in enumerate(summary["ranking_accuracy_then_parsimony"], 1):
    print(f"  {i}. {t}")
print()
print(f"CSV : {csv_path}")
print(f"JSON: {json_path}")
