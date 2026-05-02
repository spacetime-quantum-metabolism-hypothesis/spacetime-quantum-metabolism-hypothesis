"""
L527 Path-alpha toy: Gamma_0(t) time-dependent metabolism rate framework.

PURPOSE
-------
Acceptance-ceiling sensitivity scan for Path-alpha (R8 conservative axiom
modification: axiom 3 -> axiom 3' with time-dependent Gamma_0(t)).

CRITICAL CLAUDE.md COMPLIANCE
-----------------------------
- This toy does NOT prescribe a specific functional form for Gamma_0(t).
- It treats Gamma_0(t) as a generic monotonic function, parameterised only
  by:
    * an ASYMPTOTIC PAST/FUTURE RATIO  R = Gamma_0(t->past) / Gamma_0(t0)
    * a TIMESCALE EXPONENT             p (purely indexing strength of
                                          time dependence; not a physical
                                          parameter to be locked).
- The 8-person team must INDEPENDENTLY derive the actual functional form
  in a downstream Rule-A round. This script then becomes the *consumer*
  of that derivation.
- No new equations from L1-L33 forbidden topics. No values of Gamma_0,
  n_inf, mu, rho_q are computed or hardcoded. Only DIMENSIONLESS sensitivity
  ratios are scanned.

WHAT THIS DOES
--------------
1. AICc penalty accounting for axiom 3 -> axiom 3' (added DOF).
2. Path-alpha acceptance-ceiling sensitivity to (R, p) over a wide grid.
3. Marginalised acceptance histogram (R, p uniform priors).
4. Reports JCAP-acceptance ceiling + N1 prediction-channel survival rate.

OUTPUT
------
- stdout summary table.
- results/L527/path_alpha_scan.json (acceptance grid).

USAGE
-----
    python3 simulations/L527/run.py
"""

from __future__ import annotations

import json
import os
import sys
from itertools import product
from pathlib import Path

import numpy as np

# ---- environment hardening (CLAUDE.md sim rules) ----
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = REPO_ROOT / "results" / "L527"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================================
# Acceptance-ceiling model (phenomenological, derived from L526_R8 §5.1
# trajectory + L527 PATH_ALPHA.md §5.2 mechanism decomposition).
#
# The function below does NOT compute physics; it merely composes the
# qualitative bookkeeping the meta-audit already established, so we can
# see how (R, p) sensitivity propagates to the JCAP-acceptance ceiling.
# =====================================================================

# baseline (R8 Son+ correct, pre-Path-alpha) -- midpoint
ACCEPT_BASELINE = 0.05  # 5%

# component sensitivities (from PATH_ALPHA.md §5.2)
HONESTY_BONUS = 0.015          # axiom 3' explicit declaration
LAMBDA_CIRC_RELIEF = 0.020     # derived 4' partial relief
N1_PREDICTION_OPTIMIST = 0.015 # N1 channel survival upside
AICC_PENALTY_PER_DOF = 0.010   # CLAUDE.md AICc rule
POSTHOC_PENALTY_MAX = 0.015    # archetype-A theorist panel
POSTHOC_PENALTY_MIN = 0.005


def axiom3_dof_count(p_strength: float) -> float:
    """Effective DOF added by axiom 3 -> axiom 3'.

    p_strength in [0, 1]:
        0   -> Gamma_0(t) ~ const  (no real DOF, equiv to old axiom 3)
        1   -> full free monotonic functional (effectively +2 DOF)

    Single-parameter monotonic family ~ +1 DOF; richer family ~ +2.
    """
    return 1.0 + p_strength  # 1.0 .. 2.0


def n1_channel_survival(R: float, p: float) -> float:
    """Probability the N1 (a_0(z)) prediction survives degeneracy with
    Son+ corrected DESI DR3.

    R > 1  (past Gamma_0 larger): late-time signature stronger -> better
    survival. R close to 1: degenerate with LCDM, low survival.
    p high: stronger time evolution -> easier to discriminate but also
    higher post-hoc penalty.
    """
    # smooth saturating function in log(R), modulated by p
    log_strength = np.log10(max(R, 1e-3))
    discriminability = 1.0 - np.exp(-2.0 * abs(log_strength))  # 0..1
    p_modulation = 0.4 + 0.6 * p  # 0.4..1.0
    return float(np.clip(discriminability * p_modulation, 0.0, 1.0))


def posthoc_penalty(p_strength: float, single_param_family: bool) -> float:
    """Archetype-A theorist panel penalty for post-hoc patch suspicion."""
    base = POSTHOC_PENALTY_MIN if single_param_family else POSTHOC_PENALTY_MAX
    # stronger time-dependence -> more suspicion
    return float(base + (POSTHOC_PENALTY_MAX - POSTHOC_PENALTY_MIN) * p_strength)


def acceptance(R: float, p: float, single_param_family: bool = True) -> dict:
    """Compute Path-alpha acceptance for a given (R, p) point.

    Parameters
    ----------
    R : float
        Asymptotic ratio Gamma_0(t->past) / Gamma_0(t0). R=1 -> LCDM-like.
    p : float
        Strength of time dependence in [0, 1].
    single_param_family : bool
        Whether the team derives a single-parameter monotonic family
        (low post-hoc penalty) or a multi-parameter free fit.

    Returns
    -------
    dict with components and total.
    """
    dof = axiom3_dof_count(p)
    aicc_pen = AICC_PENALTY_PER_DOF * dof
    n1_surv = n1_channel_survival(R, p)
    n1_bonus = N1_PREDICTION_OPTIMIST * n1_surv
    ph_pen = posthoc_penalty(p, single_param_family)

    total = (
        ACCEPT_BASELINE
        + HONESTY_BONUS
        + LAMBDA_CIRC_RELIEF
        + n1_bonus
        - aicc_pen
        - ph_pen
    )
    total = float(np.clip(total, 0.0, 1.0))
    return {
        "R": R,
        "p": p,
        "single_param_family": single_param_family,
        "dof_added": dof,
        "aicc_penalty": aicc_pen,
        "n1_survival": n1_surv,
        "n1_bonus": n1_bonus,
        "posthoc_penalty": ph_pen,
        "acceptance": total,
    }


def scan(R_grid, p_grid, family_options=(True, False)):
    rows = []
    for R, p, fam in product(R_grid, p_grid, family_options):
        rows.append(acceptance(R, p, fam))
    return rows


def summarise(rows):
    arr = np.array([r["acceptance"] for r in rows])
    sp = np.array([r["single_param_family"] for r in rows])
    arr_sp = arr[sp]
    arr_mp = arr[~sp]
    return {
        "n_grid": int(arr.size),
        "all": {
            "min": float(arr.min()),
            "median": float(np.median(arr)),
            "max": float(arr.max()),
            "mean": float(arr.mean()),
        },
        "single_param_family": {
            "n": int(arr_sp.size),
            "min": float(arr_sp.min()),
            "median": float(np.median(arr_sp)),
            "max": float(arr_sp.max()),
        },
        "multi_param_family": {
            "n": int(arr_mp.size),
            "min": float(arr_mp.min()),
            "median": float(np.median(arr_mp)),
            "max": float(arr_mp.max()),
        },
    }


def main():
    # R: ratio Gamma_0(past)/Gamma_0(now) -- include LCDM-degenerate (1)
    # and modest evolution (up to 10x).
    R_grid = np.array([0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 3.0, 5.0, 10.0])
    # p: strength of time dependence
    p_grid = np.linspace(0.0, 1.0, 11)

    rows = scan(R_grid, p_grid)
    summary = summarise(rows)

    print("=" * 70)
    print("L527 Path-alpha acceptance-ceiling scan")
    print("=" * 70)
    print(f"grid points  : {summary['n_grid']}")
    print(f"R values     : {list(R_grid)}")
    print(f"p values     : {len(p_grid)} from 0 to 1")
    print()
    print(f"all families        median={summary['all']['median']*100:5.2f}%  "
          f"min={summary['all']['min']*100:5.2f}%  "
          f"max={summary['all']['max']*100:5.2f}%")
    print(f"single-param family median={summary['single_param_family']['median']*100:5.2f}%  "
          f"min={summary['single_param_family']['min']*100:5.2f}%  "
          f"max={summary['single_param_family']['max']*100:5.2f}%")
    print(f"multi-param family  median={summary['multi_param_family']['median']*100:5.2f}%  "
          f"min={summary['multi_param_family']['min']*100:5.2f}%  "
          f"max={summary['multi_param_family']['max']*100:5.2f}%")
    print()

    # show a few representative anchor points
    print("Representative anchors (single-parameter family):")
    print(f"  {'R':>6} {'p':>5} {'N1surv':>7} {'AICcPen':>8} "
          f"{'PostPen':>8} {'Accept':>8}")
    for R in [1.0, 1.5, 3.0, 10.0]:
        for p in [0.0, 0.3, 0.7, 1.0]:
            r = acceptance(R, p, single_param_family=True)
            print(f"  {R:6.2f} {p:5.2f} {r['n1_survival']:7.3f} "
                  f"{r['aicc_penalty']*100:7.2f}% "
                  f"{r['posthoc_penalty']*100:7.2f}% "
                  f"{r['acceptance']*100:7.2f}%")
    print()

    # ceiling under most favourable (single-param family)
    sp_rows = [r for r in rows if r["single_param_family"]]
    best = max(sp_rows, key=lambda r: r["acceptance"])
    print(f"BEST (single-param): R={best['R']}, p={best['p']:.2f} -> "
          f"acceptance {best['acceptance']*100:.2f}%")
    print(f"  PATH_ALPHA.md predicted ceiling: 12% (optimistic)")
    print(f"  PATH_ALPHA.md predicted floor  :  9% (pessimistic)")

    # save grid
    out = {
        "summary": summary,
        "grid": rows,
        "anchors": {
            "R8_baseline_pct": ACCEPT_BASELINE * 100,
            "honesty_bonus_pct": HONESTY_BONUS * 100,
            "lambda_circ_relief_pct": LAMBDA_CIRC_RELIEF * 100,
            "n1_optimist_pct": N1_PREDICTION_OPTIMIST * 100,
            "aicc_penalty_per_dof_pct": AICC_PENALTY_PER_DOF * 100,
            "posthoc_penalty_pct_min_max": [
                POSTHOC_PENALTY_MIN * 100,
                POSTHOC_PENALTY_MAX * 100,
            ],
        },
        "notes": [
            "Gamma_0(t) functional form NOT prescribed; only sensitivity to",
            "asymptotic ratio R and time-dependence strength p.",
            "8-person team must independently derive the functional form",
            "in a downstream Rule-A round; this script is a consumer of",
            "that derivation.",
            "CLAUDE.md [topmost-1] / [topmost-2] compliance: no equations,",
            "no physical parameter values, no theory map.",
        ],
    }
    out_path = RESULTS_DIR / "path_alpha_scan.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print()
    print(f"saved: {out_path}")
    return out


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
