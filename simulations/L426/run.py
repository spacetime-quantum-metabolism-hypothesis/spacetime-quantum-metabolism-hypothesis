"""L426 — Halo concentration-mass relation: SQT vs LCDM.

Channel (Path ii from NEXT_STEP.md):
  background H(z) shift  ->  D(z)  ->  sigma(M, z)  ->  nu(M, z)  ->  c(M, z)

LCDM baseline:  Diemer-Kravtsov 2015 (DK15) style c(nu, n_eff).
SQT shift:      modified H(z) from a phenomenological w(z) (CPL),
                using L48-class SQT background hint values
                (w0~-0.95, wa~-0.10) and a LCDM-equivalent control (w0=-1, wa=0).

For both backgrounds we recompute D(z), sigma(M,z), peak height nu, and
plug into the same DK15 c(nu) mapping. Difference between the two outputs
quantifies the SQT depletion-zone contribution to c(M) under the
"D(z) -> nu(M) -> c" path. This is a *minimum-axiom* test: depletion-zone
itself does not enter halo interior; only the background growth shift does.

Outputs:
  results/L426/cM_compare.json
  results/L426/cM_plot.png

Parallelism: multiprocessing spawn pool over (mass, z) grid evaluations of
sigma(M,z). Per CLAUDE.md: spawn context, OMP/MKL/OPENBLAS=1, max 9 workers.
"""

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import json
import multiprocessing as mp
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import quad, odeint

# ---------------------------------------------------------------------------
# Cosmology / constants
# ---------------------------------------------------------------------------
H0 = 67.4                      # km/s/Mpc (Planck 2018)
h = H0 / 100.0
OM = 0.315                     # matter density today
OB = 0.0493
NS = 0.965
SIGMA8 = 0.811
DELTA_C = 1.686                # spherical collapse threshold
RHO_CRIT_0 = 2.775e11 * h * h  # Msun / Mpc^3

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "results" / "L426"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Background E(z) for arbitrary CPL (w0, wa)
# ---------------------------------------------------------------------------
def E_of_z(z, w0=-1.0, wa=0.0, Om=OM):
    a = 1.0 / (1.0 + z)
    Ode = 1.0 - Om
    # CPL Omega_DE evolution: f_DE(a) = a^(-3(1+w0+wa)) * exp(-3 wa (1-a))
    fde = a ** (-3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * (1.0 - a))
    return np.sqrt(Om * (1.0 + z) ** 3 + Ode * fde)


# ---------------------------------------------------------------------------
# Linear growth D(z) via standard 2nd-order ODE in ln a
# ---------------------------------------------------------------------------
def growth_D(z_arr, w0=-1.0, wa=0.0, Om=OM):
    """Returns D(z) normalized to D(z=0)=1."""
    a_arr = np.linspace(1e-3, 1.0, 4000)

    def Om_a(a):
        z = 1.0 / a - 1.0
        return Om * (1.0 + z) ** 3 / E_of_z(z, w0, wa, Om) ** 2

    def dlnE_dlna(a):
        eps = 1e-4
        z1, z2 = 1.0 / (a * (1 + eps)) - 1.0, 1.0 / (a * (1 - eps)) - 1.0
        lnE1 = np.log(E_of_z(z1, w0, wa, Om))
        lnE2 = np.log(E_of_z(z2, w0, wa, Om))
        return (lnE1 - lnE2) / (2.0 * eps)

    def deriv(y, lna):
        D, dD = y
        a = np.exp(lna)
        Oma = Om_a(a)
        dlnE = dlnE_dlna(a)
        d2D = -(2.0 + dlnE) * dD + 1.5 * Oma * D
        return [dD, d2D]

    lna = np.log(a_arr)
    y0 = [a_arr[0], a_arr[0]]    # matter-dominated initial: D ~ a
    sol = odeint(deriv, y0, lna, full_output=False)
    D = sol[:, 0]
    D = D / D[-1]                # normalize D(a=1)=1
    z_grid = 1.0 / a_arr - 1.0
    # interpolate to requested z (input is decreasing in z_arr but a is increasing)
    return np.interp(z_arr[::-1], z_grid[::-1], D[::-1])[::-1]


# ---------------------------------------------------------------------------
# Eisenstein-Hu 1998 BBKS-like transfer (no-wiggle) for sigma(M)
# ---------------------------------------------------------------------------
def T_EH98_nowiggle(k, Om=OM, Ob=OB, h_=h):
    """k in h/Mpc. Eisenstein-Hu 1998 fitting (no-wiggle, eq. 26-31)."""
    om_m = Om * h_ * h_
    om_b = Ob * h_ * h_
    f_b = Ob / Om
    s = 44.5 * np.log(9.83 / om_m) / np.sqrt(1.0 + 10.0 * om_b ** 0.75)  # Mpc
    alpha_gamma = (
        1.0 - 0.328 * np.log(431.0 * om_m) * f_b
        + 0.38 * np.log(22.3 * om_m) * f_b ** 2
    )
    k_phys = k * h_  # 1/Mpc
    gamma_eff = Om * h_ * (
        alpha_gamma + (1.0 - alpha_gamma) / (1.0 + (0.43 * k_phys * s) ** 4)
    )
    q = k_phys * (2.728 / 2.7) ** 2 / gamma_eff
    L = np.log(2.0 * np.e + 1.8 * q)
    C = 14.2 + 731.0 / (1.0 + 62.5 * q)
    return L / (L + C * q ** 2)


def P_lin(k, Om=OM, Ob=OB, ns=NS, h_=h):
    """Linear matter power spectrum at z=0, normalized later via sigma8."""
    T = T_EH98_nowiggle(k, Om, Ob, h_)
    return k ** ns * T ** 2


def sigma_R(R, Om=OM, Ob=OB, ns=NS, h_=h):
    """Top-hat sigma at radius R (Mpc/h), z=0, *unnormalized* (no sigma8 yet)."""
    def integrand(lnk):
        k = np.exp(lnk)
        x = k * R
        W = 3.0 * (np.sin(x) - x * np.cos(x)) / x ** 3 if x > 1e-3 else 1.0 - x * x / 10.0
        return k ** 3 * P_lin(k, Om, Ob, ns, h_) * W * W / (2.0 * np.pi ** 2)

    val, _ = quad(integrand, np.log(1e-4), np.log(1e3), limit=200)
    return np.sqrt(val)


def normalize_sigma8(Om=OM, Ob=OB, ns=NS, h_=h, sigma8=SIGMA8):
    s8_unnorm = sigma_R(8.0, Om, Ob, ns, h_)
    return sigma8 / s8_unnorm


def M_to_R(M):
    """Lagrangian radius (Mpc/h) for halo mass M (Msun/h)."""
    return (3.0 * M / (4.0 * np.pi * RHO_CRIT_0 * OM)) ** (1.0 / 3.0)


def n_eff_at_R(R, Om=OM, Ob=OB, ns=NS, h_=h, dlnR=0.02):
    """Effective slope n_eff = -3 - d ln sigma^2 / d ln R (DK15 def, approx)."""
    s_lo = sigma_R(R * np.exp(-dlnR), Om, Ob, ns, h_)
    s_hi = sigma_R(R * np.exp(+dlnR), Om, Ob, ns, h_)
    return -3.0 - (np.log(s_hi ** 2) - np.log(s_lo ** 2)) / (2.0 * dlnR)


# ---------------------------------------------------------------------------
# DK15 c(nu, n_eff) fitting (Diemer-Kravtsov 2015, median NFW concentration)
# ---------------------------------------------------------------------------
DK15 = dict(phi0=6.58, phi1=1.37, eta0=6.82, eta1=1.42, alpha=1.12, beta=1.69)


def c_DK15(nu, n_eff):
    p = DK15
    cmin = p["phi0"] + p["phi1"] * n_eff
    nu_min = p["eta0"] + p["eta1"] * n_eff
    return 0.5 * cmin * ((nu_min / nu) ** p["alpha"] + (nu / nu_min) ** p["beta"])


# ---------------------------------------------------------------------------
# Worker: compute sigma_M, n_eff, nu, c for a batch of masses at z=0
# ---------------------------------------------------------------------------
def _eval_mass(args):
    M, sigma_norm, Om, Ob, ns, h_ = args
    R = M_to_R(M)                                 # Mpc/h Lagrangian
    sM = sigma_norm * sigma_R(R, Om, Ob, ns, h_)  # sigma(M, z=0)
    neff = n_eff_at_R(R, Om, Ob, ns, h_)
    return M, sM, neff


def compute_cM(masses, w0, wa, redshifts):
    """Return dict with sigma(M,z), nu(M,z), c(M,z) for each z in redshifts."""
    sigma_norm = normalize_sigma8()
    args = [(M, sigma_norm, OM, OB, NS, h) for M in masses]
    nproc = max(1, min(9, mp.cpu_count() - 1))
    ctx = mp.get_context("spawn")
    with ctx.Pool(nproc) as pool:
        results = pool.map(_eval_mass, args)
    results.sort(key=lambda r: r[0])
    Mout = np.array([r[0] for r in results])
    sM0 = np.array([r[1] for r in results])
    neff = np.array([r[2] for r in results])

    Dz = growth_D(np.array(redshifts), w0=w0, wa=wa)
    out = {"M": Mout.tolist(), "n_eff": neff.tolist(), "z": list(redshifts), "Dz": Dz.tolist()}
    out["sigma"] = {}
    out["nu"] = {}
    out["c"] = {}
    for zi, Di in zip(redshifts, Dz):
        sMz = sM0 * Di
        nu = DELTA_C / sMz
        c = c_DK15(nu, neff)
        out["sigma"][f"{zi:.2f}"] = sMz.tolist()
        out["nu"][f"{zi:.2f}"] = nu.tolist()
        out["c"][f"{zi:.2f}"] = c.tolist()
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    masses = np.logspace(11.5, 15.5, 21)  # Msun/h
    redshifts = [0.0, 0.5, 1.0]

    print("[L426] LCDM baseline (w0=-1, wa=0) ...")
    lcdm = compute_cM(masses, w0=-1.0, wa=0.0, redshifts=redshifts)

    # SQT phenomenological background: prior SQMH SQT runs (L48 family) point
    # toward mild dynamical-DE preference; we use representative shift only.
    print("[L426] SQT background (CPL phenomenological, w0=-0.95, wa=-0.10) ...")
    sqt = compute_cM(masses, w0=-0.95, wa=-0.10, redshifts=redshifts)

    # Differences
    diff = {"M": lcdm["M"], "z": redshifts, "delta_c_over_c": {}, "delta_sigma_over_sigma": {}}
    for zi in redshifts:
        key = f"{zi:.2f}"
        cL = np.array(lcdm["c"][key])
        cS = np.array(sqt["c"][key])
        sL = np.array(lcdm["sigma"][key])
        sS = np.array(sqt["sigma"][key])
        diff["delta_c_over_c"][key] = ((cS - cL) / cL).tolist()
        diff["delta_sigma_over_sigma"][key] = ((sS - sL) / sL).tolist()

    # Headline numbers
    summary = {
        "max_abs_delta_c_pct": float(
            100.0 * max(np.max(np.abs(diff["delta_c_over_c"][f"{z:.2f}"])) for z in redshifts)
        ),
        "Dz_LCDM": lcdm["Dz"],
        "Dz_SQT": sqt["Dz"],
        "interpretation": (
            "If max|Delta c/c| < 1% -> PASS_TRIVIAL (LCDM-indistinguishable). "
            "Cluster c(M) observational scatter ~0.1 dex (~25%) far exceeds this."
        ),
    }

    full = {"lcdm": lcdm, "sqt": sqt, "diff": diff, "summary": summary,
            "params": {"w0_sqt": -0.95, "wa_sqt": -0.10,
                       "Om": OM, "Ob": OB, "ns": NS, "sigma8": SIGMA8, "h": h}}

    out_json = OUT_DIR / "cM_compare.json"
    with open(out_json, "w") as f:
        json.dump(full, f, indent=2)
    print(f"[L426] wrote {out_json}")
    print(f"[L426] max |Delta c / c| over z={redshifts}: {summary['max_abs_delta_c_pct']:.3f} %")

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    Mp = np.array(lcdm["M"])
    for zi in redshifts:
        key = f"{zi:.2f}"
        axes[0].plot(Mp, lcdm["c"][key], "--", label=f"LCDM z={zi}")
        axes[0].plot(Mp, sqt["c"][key], "-", label=f"SQT z={zi}")
        axes[1].plot(Mp, 100.0 * np.array(diff["delta_c_over_c"][key]), label=f"z={zi}")
    axes[0].set_xscale("log"); axes[0].set_yscale("log")
    axes[0].set_xlabel(r"M [$M_\odot/h$]"); axes[0].set_ylabel("c (DK15)")
    axes[0].legend(fontsize=8); axes[0].set_title("c(M) — LCDM vs SQT (Path-ii)")
    axes[1].set_xscale("log")
    axes[1].set_xlabel(r"M [$M_\odot/h$]"); axes[1].set_ylabel(r"$\Delta c / c$ [%]")
    axes[1].axhline(0, color="k", lw=0.5)
    axes[1].axhline(+1, color="gray", lw=0.5, ls=":"); axes[1].axhline(-1, color="gray", lw=0.5, ls=":")
    axes[1].legend(fontsize=8); axes[1].set_title("SQT - LCDM, percent")
    fig.tight_layout()
    out_png = OUT_DIR / "cM_plot.png"
    fig.savefig(out_png, dpi=130)
    print(f"[L426] wrote {out_png}")


if __name__ == "__main__":
    main()
