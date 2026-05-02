"""
L405 — BMA Δln Z = 0.8 약점 강화 4인팀 실행

목적: paper §3.6 의 marginalized Δln Z = 0.8 (Jeffreys 'barely worth mentioning')
약점에 대한 정량 sensitivity:
  (i)  prior width R ∈ {2, 3, 5, 10} grid scan
  (ii) extra anchor (P9 dSph, P11 NS) injection forecast
  (iii) dynesty smoke test (full posterior sampler 가용성 확인)

CLAUDE.md 준수:
  - 8인팀 합의 (ATTACK/NEXT_STEP) 의 *실행* 단계만 — 새 이론 도출 없음.
  - σ₀(env) anchor 모델은 toy synthetic (실 SPARC/cluster/cosmic 재현 아님).
    실 데이터 anchor 점 (Q=1 SPARC + A1689 + cosmic) 의 χ² 구조는
    base.md §3.5 (LOO 1-out 41–89, 3-out 0) 와 §3.6 (2-regime ΔAICc=+0.77)
    구조를 *재현하도록 calibrated* 한 toy 임. 실측 재실행은 별도 budget.
  - 결과는 R sensitivity 의 *상대 변화* (Δln Z 의 R 의존성) 만 신뢰 가능.
    절대 Δln Z 값 0.8 자체는 base.md L34x 시리즈 실측 인용.

산출:
  results/L405/run_log.txt : 콘솔 출력 캡처 (이 스크립트 실행 결과)
  stdout                   : R-grid table, anchor forecast, dynesty smoke
"""
from __future__ import annotations

import os
# OpenMP 단일 스레드 강제 (Windows/Mac 안정성)
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

RNG_SEED = 42

# -----------------------------------------------------------------------------
# 0. Toy anchor synthesis — base.md §3.5/§3.6 구조 재현
# -----------------------------------------------------------------------------
# base.md 사실:
#   - 3-regime vs 2-regime ΔAICc = +0.77 (3-regime 약 선호, k 패널티 후 거의 동등)
#   - 3-regime vs 1-regime (단조) Δχ² = 288 (regime-간 gap)
#   - LOO 1-out 41–89 / 3-out 0 (cluster 9% χ² 기여)
#   - marginalized Δln Z (vs LCDM) = 0.8 with R=5 prior
# 본 toy 는 8개 anchor (SPARC galactic mid-bin 5 + cluster 1 + cosmic 2) 합성.
# 실측 산점 대신 base.md 보고된 χ²/Z 구조에 *fit* 한 합성 데이터.

def synthesize_anchors():
    """8 anchor 점 합성. (env_log10[ρ/ρ_crit], σ0_obs, sigma_err)"""
    # log10(rho_env / rho_crit) — galactic core ~+5, halo outskirt ~+2,
    # cluster ~ -1, cosmic ~ -2.5.  σ0(env) [SI m³ kg⁻¹ s] toy units.
    anchors = np.array([
        # (log10_rho_env, sigma0_obs, sigma_err)
        ( +4.5, 1.00,  0.05),  # SPARC core 1
        ( +3.7, 0.96,  0.05),  # SPARC core 2
        ( +2.8, 0.40,  0.06),  # SPARC mid 1   <-- regime gap (down)
        ( +2.0, 0.35,  0.06),  # SPARC mid 2
        ( +0.5, 0.42,  0.08),  # SPARC outer
        ( -1.0, 0.95,  0.10),  # Cluster A1689 <-- regime gap (up)
        ( -2.0, 1.10,  0.07),  # Cosmic 1
        ( -2.5, 1.15,  0.07),  # Cosmic 2
    ])
    return anchors

ANCHORS = synthesize_anchors()
LOG_RHO = ANCHORS[:, 0]
SIG_OBS = ANCHORS[:, 1]
SIG_ERR = ANCHORS[:, 2]

# Extra anchor forecast (P9 dSph low-rho, P11 NS high-rho) — toy
EXTRA_ANCHORS = {
    "P9_dSph":   (-0.3, 0.85, 0.12),  # mid-low env, expected ~0.85
    "P11_NS":    (+6.0, 1.05, 0.08),  # ultra-high env, expected ~1.0
}

# -----------------------------------------------------------------------------
# 1. Models — three-regime BB / 2-regime / 1-regime monotonic / LCDM (flat)
# -----------------------------------------------------------------------------

def model_three_regime(theta, x):
    """3-regime broken-bracket: σ_high, σ_mid, σ_low + 2 thresholds.
    theta = (s_high, s_mid, s_low, t1, t2)  with t1 > t2 (high-env first).
    """
    s_h, s_m, s_l, t1, t2 = theta
    if t1 <= t2:
        return None
    out = np.where(x > t1, s_h,
          np.where(x > t2, s_m, s_l))
    return out

def model_two_regime(theta, x):
    s_h, s_l, t1 = theta
    return np.where(x > t1, s_h, s_l)

def model_monotonic(theta, x):
    """Smooth monotonic σ(env) — sigmoid."""
    a, b, x0, w = theta
    return a + b / (1.0 + np.exp(-(x - x0) / w))

def model_lcdm(theta, x):
    """Constant σ — 1 parameter (LCDM-equivalent: env-independent)."""
    (s0,) = theta
    return np.full_like(x, s0)

MODELS = {
    "three_regime": dict(fn=model_three_regime, k=5,
                         names=["s_h", "s_m", "s_l", "t1", "t2"]),
    "two_regime":   dict(fn=model_two_regime,   k=3,
                         names=["s_h", "s_l", "t1"]),
    "monotonic":    dict(fn=model_monotonic,    k=4,
                         names=["a", "b", "x0", "w"]),
    "lcdm":         dict(fn=model_lcdm,         k=1,
                         names=["s0"]),
}

# -----------------------------------------------------------------------------
# 2. Priors (Gaussian, width R times the natural scale) + likelihood
# -----------------------------------------------------------------------------

# Natural scales (centred so LCDM at posterior peak)
PRIOR_CENTRES = {
    "three_regime": np.array([1.0, 0.4, 1.1, 3.0, 0.5]),
    "two_regime":   np.array([1.0, 0.7, 2.0]),
    "monotonic":    np.array([0.4, 0.7, 1.5, 1.0]),
    "lcdm":         np.array([0.8]),
}
PRIOR_NATSCALE = {
    "three_regime": np.array([0.3, 0.3, 0.3, 1.5, 1.5]),
    "two_regime":   np.array([0.3, 0.3, 1.5]),
    "monotonic":    np.array([0.3, 0.5, 1.5, 1.0]),
    "lcdm":         np.array([0.3]),
}

def log_likelihood(model_name, theta):
    fn = MODELS[model_name]["fn"]
    pred = fn(theta, LOG_RHO)
    if pred is None:
        return -np.inf
    chi2 = np.sum(((SIG_OBS - pred) / SIG_ERR) ** 2)
    return -0.5 * chi2

def log_prior(model_name, theta, R):
    """Gaussian prior, width = R * natural scale (independent dims)."""
    mu = PRIOR_CENTRES[model_name]
    s  = PRIOR_NATSCALE[model_name] * R
    if len(theta) != len(mu):
        return -np.inf
    diff = (np.asarray(theta) - mu) / s
    return -0.5 * np.sum(diff ** 2) - np.sum(np.log(s * math.sqrt(2 * math.pi)))

# -----------------------------------------------------------------------------
# 3. Laplace approximation for ln Z  (analytic, fast — primary tool)
# -----------------------------------------------------------------------------
# Z ≈ L(θ_MAP) * π(θ_MAP) * (2π)^{k/2} * |H|^{-1/2}
# H = -∂² ln(Lπ)/∂θ²  evaluated at MAP.

from scipy.optimize import minimize

def laplace_logz(model_name, R, restarts=8, rng=None):
    """Laplace approximation of ln Z. Returns (logZ, theta_MAP, chi2_MAP)."""
    rng = rng or np.random.default_rng(RNG_SEED)
    mu  = PRIOR_CENTRES[model_name]
    s   = PRIOR_NATSCALE[model_name] * R
    k   = len(mu)

    def neg_logp(theta):
        lp = log_prior(model_name, theta, R)
        ll = log_likelihood(model_name, theta)
        if not np.isfinite(lp + ll):
            return 1e8
        return -(lp + ll)

    best = (np.inf, None)
    for i in range(restarts):
        x0 = mu + 0.3 * s * rng.standard_normal(k)
        try:
            res = minimize(neg_logp, x0, method="Nelder-Mead",
                           options=dict(xatol=1e-5, fatol=1e-5,
                                        maxiter=4000, disp=False))
            if res.fun < best[0]:
                best = (res.fun, res.x)
        except Exception:
            continue
    if best[1] is None:
        return None
    theta_map = best[1]
    logp_map  = -best[0]
    chi2_map  = -2.0 * log_likelihood(model_name, theta_map)

    # Numerical Hessian via central differences (on -log p)
    eps = 1e-3 * np.maximum(np.abs(theta_map), 1.0)
    H = np.zeros((k, k))
    for i in range(k):
        for j in range(k):
            if i == j:
                ei = np.zeros(k); ei[i] = eps[i]
                fpp = neg_logp(theta_map + ei)
                fmm = neg_logp(theta_map - ei)
                f0  = -logp_map
                H[i, i] = (fpp - 2 * f0 + fmm) / (eps[i] ** 2)
            else:
                ei = np.zeros(k); ei[i] = eps[i]
                ej = np.zeros(k); ej[j] = eps[j]
                fpp = neg_logp(theta_map + ei + ej)
                fpm = neg_logp(theta_map + ei - ej)
                fmp = neg_logp(theta_map - ei + ej)
                fmm = neg_logp(theta_map - ei - ej)
                H[i, j] = (fpp - fpm - fmp + fmm) / (4 * eps[i] * eps[j])
    # Symmetrise
    H = 0.5 * (H + H.T)
    sign, logdet = np.linalg.slogdet(H)
    if sign <= 0 or not np.isfinite(logdet):
        # Fallback: regularise
        H_reg = H + 1e-3 * np.eye(k)
        sign, logdet = np.linalg.slogdet(H_reg)
        if sign <= 0:
            return dict(logZ=np.nan, theta_map=theta_map,
                        chi2_map=chi2_map, hess_singular=True)
    logZ = logp_map + 0.5 * k * math.log(2 * math.pi) - 0.5 * logdet
    return dict(logZ=logZ, theta_map=theta_map, chi2_map=chi2_map,
                hess_singular=False)

# -----------------------------------------------------------------------------
# 4. R-grid sensitivity scan (R ∈ {2, 3, 5, 10})
# -----------------------------------------------------------------------------

def r_grid_scan():
    R_LIST = [2.0, 3.0, 5.0, 10.0]
    rows = []
    for R in R_LIST:
        out = {"R": R}
        for mname in MODELS:
            res = laplace_logz(mname, R)
            out[mname] = (res or {}).get("logZ", np.nan)
        rows.append(out)
    return rows

def print_r_grid(rows):
    print("\n=== (i) Prior-width R sensitivity (Laplace ln Z) ===")
    print(f"  R       | {'three_regime':>12} | {'two_regime':>10} | "
          f"{'monotonic':>10} | {'lcdm':>10} || ΔlnZ(3R−LCDM) | ΔlnZ(2R−LCDM)")
    print("  " + "-" * 95)
    for r in rows:
        d3 = r["three_regime"] - r["lcdm"]
        d2 = r["two_regime"] - r["lcdm"]
        print(f"  R={r['R']:<5g}| {r['three_regime']:12.3f} | "
              f"{r['two_regime']:10.3f} | {r['monotonic']:10.3f} | "
              f"{r['lcdm']:10.3f} || {d3:+13.3f} | {d2:+13.3f}")

# -----------------------------------------------------------------------------
# 5. Extra anchor injection forecast (P9 dSph, P11 NS)
# -----------------------------------------------------------------------------
# 두 시나리오:
#   S_compat : 새 anchor 가 three-regime 예측과 일치 (현재 평균값 사용)
#   S_tension: 새 anchor 가 monotonic 쪽으로 쏠림 (regime gap 약화)

def forecast_with_extra(scenario, R=5.0):
    """Re-evaluate Δln Z with extra anchors injected."""
    global LOG_RHO, SIG_OBS, SIG_ERR
    save = (LOG_RHO.copy(), SIG_OBS.copy(), SIG_ERR.copy())
    extras_x = []
    extras_y = []
    extras_e = []
    for name, (x, y_compat, e) in EXTRA_ANCHORS.items():
        extras_x.append(x); extras_e.append(e)
        if scenario == "compat":
            extras_y.append(y_compat)
        elif scenario == "tension":
            # Tension: P9 dSph 가 +0.10 위로 (monotonic 일치),
            # P11 NS 가 -0.15 아래로 (regime gap 와해)
            shift = +0.10 if "dSph" in name else -0.15
            extras_y.append(y_compat + shift)
        else:
            extras_y.append(y_compat)
    LOG_RHO = np.concatenate([save[0], np.array(extras_x)])
    SIG_OBS = np.concatenate([save[1], np.array(extras_y)])
    SIG_ERR = np.concatenate([save[2], np.array(extras_e)])

    # Patch globals into log_likelihood scope by reassignment (used as module globals)
    res = {}
    for mname in MODELS:
        r = laplace_logz(mname, R)
        res[mname] = (r or {}).get("logZ", np.nan)

    # Restore
    LOG_RHO = save[0]; SIG_OBS = save[1]; SIG_ERR = save[2]
    # Push back into module globals (since we shadowed)
    globals()["LOG_RHO"] = LOG_RHO
    globals()["SIG_OBS"] = SIG_OBS
    globals()["SIG_ERR"] = SIG_ERR
    return res

def print_anchor_forecast(R=5.0):
    print("\n=== (ii) Extra-anchor forecast (P9 dSph + P11 NS, R=5 prior) ===")
    base_rows = r_grid_scan()
    base = next(r for r in base_rows if abs(r["R"] - R) < 1e-6)

    for sc in ("compat", "tension"):
        # Need to actually mutate LOG_RHO etc — use module-level helper
        global LOG_RHO, SIG_OBS, SIG_ERR
        save = (LOG_RHO.copy(), SIG_OBS.copy(), SIG_ERR.copy())
        ex_x, ex_y, ex_e = [], [], []
        for name, (x, y_compat, e) in EXTRA_ANCHORS.items():
            ex_x.append(x); ex_e.append(e)
            if sc == "compat":
                ex_y.append(y_compat)
            else:
                shift = +0.10 if "dSph" in name else -0.15
                ex_y.append(y_compat + shift)
        LOG_RHO = np.concatenate([save[0], np.array(ex_x)])
        SIG_OBS = np.concatenate([save[1], np.array(ex_y)])
        SIG_ERR = np.concatenate([save[2], np.array(ex_e)])

        res = {m: laplace_logz(m, R) for m in MODELS}
        d3  = res["three_regime"]["logZ"] - res["lcdm"]["logZ"]
        d2  = res["two_regime"]["logZ"]   - res["lcdm"]["logZ"]
        print(f"  scenario={sc:<8s}  ΔlnZ(3R−LCDM)={d3:+.3f}  "
              f"ΔlnZ(2R−LCDM)={d2:+.3f}  "
              f"(baseline 3R−LCDM={base['three_regime']-base['lcdm']:+.3f})")

        # Restore
        LOG_RHO = save[0]; SIG_OBS = save[1]; SIG_ERR = save[2]

# -----------------------------------------------------------------------------
# 6. dynesty smoke test (full posterior sampler)
# -----------------------------------------------------------------------------

def dynesty_smoke():
    print("\n=== (iii) dynesty smoke test (three_regime, R=5) ===")
    try:
        import dynesty
    except ImportError:
        print("  dynesty 미설치 — skip.")
        return

    R = 5.0
    mname = "three_regime"
    mu = PRIOR_CENTRES[mname]
    s  = PRIOR_NATSCALE[mname] * R
    k  = len(mu)

    def prior_transform(u):
        from scipy.special import ndtri
        # Uniform [0,1]^k → Gaussian(mu, s) via inverse CDF
        return mu + s * ndtri(u)

    def logl(theta):
        return float(log_likelihood(mname, theta))

    rng = np.random.default_rng(RNG_SEED)
    t0 = time.time()
    sampler = dynesty.NestedSampler(
        logl, prior_transform, ndim=k,
        nlive=80, rstate=rng,
    )
    sampler.run_nested(maxiter=2500, dlogz=0.5, print_progress=False)
    res = sampler.results
    dt = time.time() - t0

    logZ      = res.logz[-1]
    logZ_err  = res.logzerr[-1]
    n_iter    = res.niter
    print(f"  nlive=80  niter={n_iter}  wall={dt:.2f}s")
    print(f"  ln Z (dynesty, three_regime) = {logZ:.3f} ± {logZ_err:.3f}")

    # Compare to Laplace for same model
    lap = laplace_logz(mname, R)
    print(f"  ln Z (Laplace,  three_regime) = {lap['logZ']:.3f}")
    print(f"  Δ (dynesty − Laplace)         = {logZ - lap['logZ']:+.3f}")

    # And for LCDM
    def prior_transform_lcdm(u):
        from scipy.special import ndtri
        muL = PRIOR_CENTRES["lcdm"]; sL = PRIOR_NATSCALE["lcdm"] * R
        return muL + sL * ndtri(u)
    def logl_lcdm(theta):
        return float(log_likelihood("lcdm", theta))
    rng2 = np.random.default_rng(RNG_SEED + 1)
    sL = dynesty.NestedSampler(
        logl_lcdm, prior_transform_lcdm, ndim=1, nlive=60, rstate=rng2)
    sL.run_nested(maxiter=2000, dlogz=0.5, print_progress=False)
    rL = sL.results
    logZL = rL.logz[-1]; errL = rL.logzerr[-1]
    print(f"  ln Z (dynesty, lcdm)         = {logZL:.3f} ± {errL:.3f}")
    print(f"  ΔlnZ(3R − LCDM, dynesty)     = {logZ - logZL:+.3f}  "
          f"(quadrature err ≈ {math.hypot(logZ_err, errL):.3f})")

# -----------------------------------------------------------------------------
# 7. Main
# -----------------------------------------------------------------------------

def main():
    print("=" * 78)
    print("L405 — BMA Δln Z=0.8 sensitivity (R-grid + extra-anchor forecast + dynesty)")
    print("=" * 78)
    print(f"anchors N = {len(LOG_RHO)}  (toy synthetic, base.md §3.5/§3.6 calibrated)")
    print(f"models    : {list(MODELS.keys())}")
    print(f"seed      : {RNG_SEED}")

    # Sanity: print χ² at MAP for each model with R=5
    print("\n--- Sanity (R=5, MAP χ²) ---")
    for m in MODELS:
        r = laplace_logz(m, 5.0)
        if r is None:
            print(f"  {m:14s} : optim FAIL")
            continue
        print(f"  {m:14s} : k={MODELS[m]['k']}  χ²={r['chi2_map']:.3f}  "
              f"lnZ={r['logZ']:.3f}  hess_sing={r['hess_singular']}")

    rows = r_grid_scan()
    print_r_grid(rows)
    print_anchor_forecast(R=5.0)
    dynesty_smoke()

    # Save JSON summary
    out = dict(seed=RNG_SEED, n_anchors=int(len(LOG_RHO)),
               r_grid=[{k: float(v) if isinstance(v, (int, float, np.floating))
                        else v for k, v in row.items()} for row in rows])
    out_dir = Path(__file__).resolve().parent.parent.parent / "results" / "L405"
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "report.json").open("w") as f:
        json.dump(out, f, indent=2, default=float)
    print(f"\n[saved] {out_dir / 'report.json'}")
    print("\n=== END L405 run.py ===")

if __name__ == "__main__":
    main()
