"""L425 — NS saturation sigma_0 mock forecast.

Goal: forecast Delta lnZ (3-regime SQT vs 2-regime baseline) when a P11-style
NS saturation anchor is added to the pool, marginalised over an EOS family.

Design (per ATTACK_DESIGN A1-A8):
  - EOS family: APR, SLy4, BSk21, BSk22, MPA1 (chiral-EFT compatible).
    Each EOS contributes (M_max, R_1.4, central density rho_c) with literature
    fiducial values + intrinsic measurement scatter.
  - SQT 3-regime model: an extra high-psi curvature parameter gamma_hi induces
    a saturation shift Delta sigma_0(rho_c, gamma_hi).
  - 2-regime baseline: gamma_hi = 0 fixed (one fewer free parameter).
  - Mock data: NICER + GW170817 + universal relation channel, marginalised
    over EOS prior. Generate N_mock = 500 realisations.
  - Compute ln evidence by Laplace approximation around best-fit.
  - Report: ΔlnZ distribution under EOS-marginalised vs EOS-fixed prescriptions.

Parallelism: multiprocessing spawn pool, OMP/MKL/OPENBLAS threads = 1.
"""

from __future__ import annotations
import os, json, time
# Pin BLAS threads BEFORE numpy import.
for _v in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"

import numpy as np
import multiprocessing as mp
from pathlib import Path

# ----------------------------- EOS family -----------------------------------
# Literature fiducials (chiral-EFT-compatible nucleonic EOS).
# Each entry: M_max [Msun], R_1.4 [km], rho_c at M_max [fm^-3], Lambda_1.4.
EOS_TABLE = {
    "APR":   dict(M_max=2.20, R14=11.34, rho_c=1.10, Lam14=246.0),
    "SLy4":  dict(M_max=2.05, R14=11.74, rho_c=1.20, Lam14=297.0),
    "BSk21": dict(M_max=2.28, R14=12.59, rho_c=0.96, Lam14=521.0),
    "BSk22": dict(M_max=2.26, R14=13.04, rho_c=0.94, Lam14=629.0),
    "MPA1":  dict(M_max=2.46, R14=12.47, rho_c=1.05, Lam14=487.0),
}
EOS_NAMES = list(EOS_TABLE.keys())

# Observational sigma (NICER + GW170817 anchored channels)
SIG_MMAX = 0.10   # Msun, J0740 mass measurement scale
SIG_R14  = 0.80   # km, NICER R(1.4) effective uncertainty
SIG_LAM  = 130.0  # Lambda_1.4 effective from GW170817 (post-anchor)

# True (injected) SQT 3-regime parameter scaling.
# gamma_hi is an a priori O(0.05) high-psi curvature index drawn from the
# 3-regime fit posterior (representative).
GAMMA_HI_TRUE = 0.04

# SQT 3-regime correction model (phenomenological forward map).
# Delta M_max = +A_M * gamma_hi * (rho_c - rho_ref), in Msun
# Delta R_14 = -A_R * gamma_hi * (rho_c - rho_ref), in km
# Delta Lam14 = -A_L * gamma_hi * (rho_c - rho_ref) * Lam14
# Coefficients chosen so that |effect| ~ NICER/GW170817 noise floor (A4 caveat).
A_M = 0.85
A_R = 1.20
A_L = 0.40
RHO_REF = 1.05  # fm^-3, family centre

def forward(eos_name: str, gamma_hi: float) -> dict:
    e = EOS_TABLE[eos_name]
    drho = e["rho_c"] - RHO_REF
    return dict(
        M_max = e["M_max"] + A_M*gamma_hi*drho,
        R14   = e["R14"]   - A_R*gamma_hi*drho,
        Lam14 = e["Lam14"] * (1.0 - A_L*gamma_hi*drho),
        rho_c = e["rho_c"],
    )

def chi2(obs: dict, pred: dict) -> float:
    return ((obs["M_max"]-pred["M_max"])/SIG_MMAX)**2 \
         + ((obs["R14"] -pred["R14"]) /SIG_R14 )**2 \
         + ((obs["Lam14"]-pred["Lam14"])/SIG_LAM)**2

# ---------------------- Evidence (Laplace approx) ---------------------------
# 2-regime: gamma_hi = 0, only EOS choice marginalised.
# 3-regime: gamma_hi free, Gaussian prior N(0, sigma_g_pr); EOS marginalised.
SIG_G_PRIOR = 0.05   # SQT a priori prior width on gamma_hi (from L322 posterior)

def lnL_eos_marg(obs: dict, gamma_hi: float, eos_subset: list[str]) -> float:
    """Marginalise over flat EOS prior within subset by log-sum-exp."""
    chis = np.array([chi2(obs, forward(name, gamma_hi)) for name in eos_subset])
    # log mean exp(-chi/2)
    half = -0.5*chis
    M = half.max()
    return M + np.log(np.exp(half-M).mean())

def ln_evidence_2reg(obs, eos_subset):
    """gamma_hi = 0 fixed."""
    return lnL_eos_marg(obs, 0.0, eos_subset)

def ln_evidence_3reg(obs, eos_subset, n_grid=129):
    """Numerical 1-D integration over gamma_hi with Gaussian prior."""
    g = np.linspace(-4*SIG_G_PRIOR, 4*SIG_G_PRIOR, n_grid)
    lpr = -0.5*(g/SIG_G_PRIOR)**2 - 0.5*np.log(2*np.pi*SIG_G_PRIOR**2)
    lL  = np.array([lnL_eos_marg(obs, gv, eos_subset) for gv in g])
    integrand = lL + lpr
    M = integrand.max()
    return M + np.log(np.trapezoid(np.exp(integrand-M), g))

# ----------------------------- Mock generator -------------------------------
def generate_mock(rng: np.random.Generator, eos_truth: str,
                  gamma_truth: float) -> dict:
    pred = forward(eos_truth, gamma_truth)
    return dict(
        M_max = pred["M_max"] + rng.normal(0.0, SIG_MMAX),
        R14   = pred["R14"]   + rng.normal(0.0, SIG_R14 ),
        Lam14 = pred["Lam14"] + rng.normal(0.0, SIG_LAM ),
    )

# ----------------------------- Worker ---------------------------------------
def worker(seed: int) -> dict:
    rng = np.random.default_rng(seed)
    # EOS truth uniformly drawn from family
    eos_truth = EOS_NAMES[rng.integers(len(EOS_NAMES))]
    # Gamma_hi truth: half mocks at injected value, half at zero (null).
    inject = bool(seed & 1)
    g_true = GAMMA_HI_TRUE if inject else 0.0
    obs = generate_mock(rng, eos_truth, g_true)

    # Two prescriptions:
    # (a) EOS-marginalised over the full family
    # (b) EOS-fixed at the truth (best-case, gives optimistic ΔlnZ ceiling)
    lnZ2_marg = ln_evidence_2reg(obs, EOS_NAMES)
    lnZ3_marg = ln_evidence_3reg(obs, EOS_NAMES)
    lnZ2_fix  = ln_evidence_2reg(obs, [eos_truth])
    lnZ3_fix  = ln_evidence_3reg(obs, [eos_truth])

    return dict(
        seed=seed, eos_truth=eos_truth, inject=inject,
        dlnZ_marg = lnZ3_marg - lnZ2_marg,
        dlnZ_fix  = lnZ3_fix  - lnZ2_fix,
    )

# ----------------------------- Driver ---------------------------------------
def main(n_mock: int = 500, n_workers: int = 9, out_dir: str | None = None):
    out_dir = out_dir or str(Path(__file__).resolve().parents[2]
                             / "results" / "L425")
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    seeds = list(range(1, n_mock+1))
    t0 = time.time()
    ctx = mp.get_context("spawn")
    with ctx.Pool(n_workers) as pool:
        results = pool.map(worker, seeds, chunksize=8)
    dt = time.time() - t0

    arr_marg_inj   = np.array([r["dlnZ_marg"] for r in results if r["inject"]])
    arr_marg_null  = np.array([r["dlnZ_marg"] for r in results if not r["inject"]])
    arr_fix_inj    = np.array([r["dlnZ_fix"]  for r in results if r["inject"]])
    arr_fix_null   = np.array([r["dlnZ_fix"]  for r in results if not r["inject"]])

    summary = dict(
        n_mock=n_mock, n_workers=n_workers, runtime_sec=dt,
        gamma_hi_true=GAMMA_HI_TRUE, sig_g_prior=SIG_G_PRIOR,
        eos_family=EOS_NAMES,
        injected = dict(
            marg=dict(mean=float(arr_marg_inj.mean()),
                      median=float(np.median(arr_marg_inj)),
                      std=float(arr_marg_inj.std()),
                      frac_gt1=float((arr_marg_inj>1).mean()),
                      frac_gt3=float((arr_marg_inj>3).mean())),
            fix =dict(mean=float(arr_fix_inj.mean()),
                      median=float(np.median(arr_fix_inj)),
                      std=float(arr_fix_inj.std()),
                      frac_gt1=float((arr_fix_inj>1).mean()),
                      frac_gt3=float((arr_fix_inj>3).mean())),
        ),
        null = dict(
            marg=dict(mean=float(arr_marg_null.mean()),
                      median=float(np.median(arr_marg_null)),
                      std=float(arr_marg_null.std()),
                      frac_gt1=float((arr_marg_null>1).mean()),
                      frac_gt3=float((arr_marg_null>3).mean())),
            fix =dict(mean=float(arr_fix_null.mean()),
                      median=float(np.median(arr_fix_null)),
                      std=float(arr_fix_null.std()),
                      frac_gt1=float((arr_fix_null>1).mean()),
                      frac_gt3=float((arr_fix_null>3).mean())),
        ),
        # A8 kill switch verdict
        verdict = None,
    )
    m = summary["injected"]["marg"]["median"]
    if m < 1.0:
        summary["verdict"] = "KILL: P11 not worth adding (EOS-marg dlnZ < +1)"
    elif m > 3.0:
        summary["verdict"] = "PROMOTE: 3-regime baseline justified by P11"
    else:
        summary["verdict"] = "RESERVE: keep as conditional anchor (1<=median<=3)"

    out_path = Path(out_dir) / "forecast_summary.json"
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"[L425] wrote {out_path} (runtime {dt:.1f}s, n_mock={n_mock})")
    print(f"[L425] verdict: {summary['verdict']}")
    print(f"[L425] EOS-marg dlnZ (injected): "
          f"median={m:+.3f}, mean={summary['injected']['marg']['mean']:+.3f}, "
          f"std={summary['injected']['marg']['std']:.3f}")
    print(f"[L425] EOS-fix  dlnZ (injected): "
          f"median={summary['injected']['fix']['median']:+.3f}")
    return summary

if __name__ == "__main__":
    main()
