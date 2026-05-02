"""L465 toy: 3-state Potts model phase diagram (free speculation).

Goal: explore whether a Z_3 internal symmetry of the metabolism field n
can produce three vacua (low / intermediate / high) and whether the
"intermediate" phase could correspond to the cluster-scale dip seen in
SQMH phenomenology.

This is a toy Monte Carlo on a 2D square lattice. No cosmological data
is used here -- this is purely structural exploration of universality
classes (Z_2 Ising vs Z_3 Potts vs 3-state clock).

Run:  python3 simulations/L465/run.py
Outputs: results/L465/potts_scan.csv, potts_phase.png
"""
from __future__ import annotations

import csv
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results" / "L465"
RESULTS.mkdir(parents=True, exist_ok=True)


def potts_step(state: np.ndarray, beta: float, q: int, rng: np.random.Generator) -> None:
    """Single sweep of Metropolis updates for q-state Potts on a 2D lattice."""
    L = state.shape[0]
    # Random sweep order
    xs = rng.integers(0, L, size=L * L)
    ys = rng.integers(0, L, size=L * L)
    new_vals = rng.integers(0, q, size=L * L)
    rs = rng.random(size=L * L)
    for k in range(L * L):
        x, y = xs[k], ys[k]
        s_old = state[x, y]
        s_new = new_vals[k]
        if s_old == s_new:
            continue
        # Neighbour energy: -J * sum_<ij> delta(s_i, s_j) ; J=1
        nbrs = (
            state[(x + 1) % L, y],
            state[(x - 1) % L, y],
            state[x, (y + 1) % L],
            state[x, (y - 1) % L],
        )
        e_old = -sum(1 for n in nbrs if n == s_old)
        e_new = -sum(1 for n in nbrs if n == s_new)
        dE = e_new - e_old
        if dE <= 0 or rs[k] < np.exp(-beta * dE):
            state[x, y] = s_new


def magnetisation_q(state: np.ndarray, q: int) -> float:
    """Order parameter for q-state Potts: m = (q * f_max - 1) / (q - 1)."""
    counts = np.bincount(state.ravel(), minlength=q)
    f_max = counts.max() / state.size
    return (q * f_max - 1.0) / (q - 1.0)


def run_scan(q: int, L: int = 24, n_eq: int = 200, n_meas: int = 200,
             betas: np.ndarray | None = None, seed: int = 0) -> list[dict]:
    if betas is None:
        # Exact T_c (Potts on 2D square): beta_c = ln(1 + sqrt(q))
        bc = np.log(1.0 + np.sqrt(q))
        betas = np.linspace(0.5 * bc, 1.5 * bc, 21)
    rng = np.random.default_rng(seed)
    rows = []
    for beta in betas:
        state = rng.integers(0, q, size=(L, L)).astype(np.int8)
        for _ in range(n_eq):
            potts_step(state, beta, q, rng)
        ms = []
        for _ in range(n_meas):
            potts_step(state, beta, q, rng)
            ms.append(magnetisation_q(state, q))
        ms = np.array(ms)
        rows.append({
            "q": q,
            "beta": float(beta),
            "beta_over_betac": float(beta / np.log(1 + np.sqrt(q))),
            "m_mean": float(ms.mean()),
            "m_var": float(ms.var()),
            "chi": float(L * L * ms.var()),
        })
        print(f"  q={q} beta={beta:.3f} <m>={ms.mean():.3f} chi={L*L*ms.var():.2f}", flush=True)
    return rows


def main() -> int:
    out_csv = RESULTS / "potts_scan.csv"
    all_rows: list[dict] = []
    for q in (2, 3):
        print(f"=== q={q} (Z_{q} symmetry) ===", flush=True)
        all_rows.extend(run_scan(q=q, L=24, n_eq=150, n_meas=150, seed=42 + q))

    with out_csv.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(all_rows[0].keys()))
        w.writeheader()
        w.writerows(all_rows)
    print(f"Wrote {out_csv}")

    # Optional plot
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:
        print(f"matplotlib unavailable: {e}")
        return 0

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for q in (2, 3):
        rows = [r for r in all_rows if r["q"] == q]
        x = [r["beta_over_betac"] for r in rows]
        m = [r["m_mean"] for r in rows]
        chi = [r["chi"] for r in rows]
        axes[0].plot(x, m, "o-", label=f"q={q}")
        axes[1].plot(x, chi, "s-", label=f"q={q}")
    axes[0].set_xlabel(r"$\beta / \beta_c$")
    axes[0].set_ylabel("order parameter <m>")
    axes[0].axvline(1.0, color="k", ls="--", alpha=0.4)
    axes[0].legend()
    axes[1].set_xlabel(r"$\beta / \beta_c$")
    axes[1].set_ylabel(r"susceptibility $\chi$")
    axes[1].axvline(1.0, color="k", ls="--", alpha=0.4)
    axes[1].legend()
    fig.suptitle("L465 toy: Z_2 vs Z_3 Potts on 2D lattice (24x24)")
    fig.tight_layout()
    fig.savefig(RESULTS / "potts_phase.png", dpi=120)
    print(f"Wrote {RESULTS / 'potts_phase.png'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
