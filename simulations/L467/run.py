"""L467 — Wetterich-style RG flow numerics for SQMH metabolic coupling sigma.

자유 추측 (free speculation) — 클러스터 dip 의 원인을 cubic beta 함수의
saddle 고정점 근처 unstable 분기로 가정한다.

목적
----
1. cubic beta(sigma) = a*sigma + b*sigma^2 + c*sigma^3 의 saddle FP 위치 deep dive.
2. UV (high k) <-> IR (low k) interpolation 곡선.
3. saddle 근처 *temperature-like* 매개변수 T_eff 도입 가능성 (느린 흐름 시간).
4. Wetterich-type 단일루프 flow d sigma / d ln k 수치 적분.

원칙: 어떤 외부 데이터 fit 도 시도하지 않는다. 순수 RG 흐름의 정성적 구조만 본다.
"""

from __future__ import annotations

import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

OUT = Path(__file__).resolve().parent
RES = OUT.parent.parent / "results" / "L467"
RES.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# 1. cubic beta function family
# ---------------------------------------------------------------------------

def beta(sigma: np.ndarray, a: float, b: float, c: float) -> np.ndarray:
    """Cubic beta function. d sigma / d ln k = beta(sigma).

    Sigma is clipped to a safe range to avoid overflow during stiff integration
    near runaway directions of the cubic.
    """
    s = np.clip(sigma, -50.0, 50.0)
    return a * s + b * s * s + c * s * s * s


def beta_prime(sigma: float, a: float, b: float, c: float) -> float:
    """Stability exponent at FP: omega = -beta'(sigma_*)."""
    return a + 2.0 * b * sigma + 3.0 * c * sigma**2


def find_fixed_points(a: float, b: float, c: float) -> list[tuple[float, float, str]]:
    """Return list of (sigma*, beta'(sigma*), classification).

    classification: 'UV' (beta' > 0, IR-repulsive ⇒ UV-attractive),
                    'IR' (beta' < 0, IR-attractive),
                    'saddle' (zero crossing with d^2 beta non-trivial).

    cubic 의 1D RG 에서 saddle 은 본래 없지만, 2D embedding 또는
    coupling 의 다중 채널에서 saddle 행렬 고유치 부호 혼합으로 등장한다.
    여기서는 1D 에서 'saddle-like' 를 beta'≈0 (이중근 근처) 로 정의한다.
    """
    # roots of c x^3 + b x^2 + a x = x*(c x^2 + b x + a)
    roots = [0.0]
    if abs(c) > 1e-15:
        disc = b * b - 4 * a * c
        if disc >= 0:
            r1 = (-b + np.sqrt(disc)) / (2 * c)
            r2 = (-b - np.sqrt(disc)) / (2 * c)
            roots += [r1, r2]
    elif abs(b) > 1e-15:
        roots.append(-a / b)

    out = []
    for r in roots:
        bp = beta_prime(r, a, b, c)
        if abs(bp) < 1e-6:
            cls = "saddle"
        elif bp > 0:
            cls = "UV"  # repulsive in IR direction (k decreasing)
        else:
            cls = "IR"  # attractive in IR direction
        out.append((float(r), float(bp), cls))
    # dedup
    uniq = []
    for r, bp, cls in out:
        if not any(abs(r - rr) < 1e-9 for rr, _, _ in uniq):
            uniq.append((r, bp, cls))
    return uniq


# ---------------------------------------------------------------------------
# 2. saddle deep dive: tune (a,b,c) so two FPs collide (double root)
# ---------------------------------------------------------------------------

def saddle_locus(b: float, c: float) -> tuple[float, float]:
    """Given (b, c), find a* such that b^2 - 4 a c = 0 (double non-trivial root).

    At the saddle: sigma_s = -b/(2c), a_s = b^2/(4c).
    """
    a_s = b * b / (4.0 * c)
    sigma_s = -b / (2.0 * c)
    return a_s, sigma_s


# ---------------------------------------------------------------------------
# 3. UV <-> IR interpolation (flow trajectory)
# ---------------------------------------------------------------------------

def flow_trajectory(
    sigma_uv: float,
    a: float,
    b: float,
    c: float,
    t_span: tuple[float, float] = (0.0, -30.0),
    n_pts: int = 600,
) -> dict:
    """Integrate d sigma / dt = beta(sigma), t = ln k.

    Negative t direction = IR (k -> 0). Positive t = UV.
    """
    t_eval = np.linspace(t_span[0], t_span[1], n_pts)

    def rhs(t, y):
        return [beta(y[0], a, b, c)]

    sol = solve_ivp(
        rhs,
        t_span,
        [sigma_uv],
        t_eval=t_eval,
        method="LSODA",
        rtol=1e-9,
        atol=1e-12,
    )
    return {
        "t": sol.t.tolist(),
        "sigma": sol.y[0].tolist(),
        "success": bool(sol.success),
    }


# ---------------------------------------------------------------------------
# 4. temperature-like parameter near saddle
# ---------------------------------------------------------------------------

def saddle_dwell_time(
    a: float,
    b: float,
    c: float,
    sigma_init: float,
    eps: float = 1e-2,
) -> float:
    """Time spent within ±eps of saddle sigma_s.

    For a true saddle (beta'≈0) the linear theory diverges (∞ dwell time).
    Slightly detuned (a = a_s + delta) gives finite dwell ~ pi / sqrt(|delta|*4c).
    This 'dwell time' is the temperature-like parameter T_eff ≡ 1 / dwell.
    """
    sigma_s = -b / (2.0 * c)

    def rhs(t, y):
        return [beta(y[0], a, b, c)]

    t_arr = np.linspace(0.0, -200.0, 5000)
    try:
        sol = solve_ivp(
            rhs,
            (0.0, -200.0),
            [sigma_init],
            t_eval=t_arr,
            method="RK45",
            rtol=1e-8,
            atol=1e-11,
            max_step=1.0,
        )
        if not sol.success or sol.y.shape[1] < 2:
            return 0.0
        t_arr = sol.t
        s_arr = sol.y[0]
    except Exception:
        return 0.0
    mask = np.abs(s_arr - sigma_s) < eps
    if not mask.any():
        return 0.0
    idx = np.where(mask)[0]
    return float(abs(t_arr[idx[-1]] - t_arr[idx[0]]))


def temperature_scan(
    b: float,
    c: float,
    delta_grid: np.ndarray,
) -> dict:
    """Scan detuning delta = a - a_s, measure dwell time -> T_eff = 1/dwell."""
    a_s, sigma_s = saddle_locus(b, c)
    dwells = []
    for d in delta_grid:
        a = a_s + d
        # start a bit above saddle in unstable direction
        sig0 = sigma_s + 0.05
        tau = saddle_dwell_time(a, b, c, sig0, eps=2e-2)
        dwells.append(tau)
    dwells = np.array(dwells)
    T_eff = np.where(dwells > 1e-6, 1.0 / dwells, np.inf)
    return {
        "delta": delta_grid.tolist(),
        "dwell": dwells.tolist(),
        "T_eff": T_eff.tolist(),
        "a_saddle": float(a_s),
        "sigma_saddle": float(sigma_s),
    }


# ---------------------------------------------------------------------------
# 5. Wetterich-type single-loop flow (toy)
# ---------------------------------------------------------------------------

def wetterich_beta(sigma: float, k: float, lam: float = 1.0, eta: float = 0.0) -> float:
    """Toy Wetterich flow with optimised (Litim) cutoff.

    d sigma / d ln k = (lam - eta) * sigma - sigma^2 * I(k)
    where I(k) is the threshold function. We absorb k-dependence into a slow
    drift so the structure remains cubic-like via expansion.

    Here we keep it minimal: a flowing anomalous dimension eta(sigma) = nu*sigma
    generates a cubic term effectively.
    """
    eta_s = 0.4 * sigma  # toy: anomalous dim grows with coupling
    return (lam - eta_s) * sigma - 0.5 * sigma * sigma + 0.05 * sigma**3


def wetterich_trajectory(
    sigma_uv: float,
    lam: float = 0.1,
    t_span: tuple[float, float] = (0.0, -25.0),
    n_pts: int = 400,
) -> dict:
    t_eval = np.linspace(t_span[0], t_span[1], n_pts)

    def rhs(t, y):
        k = np.exp(t)
        return [wetterich_beta(y[0], k, lam=lam)]

    sol = solve_ivp(
        rhs, t_span, [sigma_uv], t_eval=t_eval,
        method="LSODA", rtol=1e-9, atol=1e-12,
    )
    return {
        "t": sol.t.tolist(),
        "sigma": sol.y[0].tolist(),
        "lam": lam,
        "success": bool(sol.success),
    }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> None:
    rng = np.random.default_rng(42)

    # (1) cubic FP catalogue across (a,b,c)
    cases = []
    for (a, b, c) in [
        (-0.05, 0.30, -0.20),   # generic: 3 real FPs
        (+0.10, 0.30, -0.20),   # only 1 real FP (origin)
        (0.225, 0.60, -0.40),   # near saddle (b^2 = 4ac → degenerate)
        (-0.20, 0.10, -0.30),
    ]:
        fps = find_fixed_points(a, b, c)
        cases.append({"a": a, "b": b, "c": c, "fps": fps})

    # (2) saddle locus: tune a to b^2/(4c)
    b, c = 0.60, -0.40
    a_s, sigma_s = saddle_locus(b, c)
    fps_at_saddle = find_fixed_points(a_s, b, c)

    # (3) UV→IR trajectory near saddle (3 initial conditions: above, at, below)
    trajectories = []
    for sig0 in [sigma_s + 0.05, sigma_s, sigma_s - 0.05]:
        traj = flow_trajectory(sig0, a_s, b, c, t_span=(0.0, -30.0))
        trajectories.append({"sigma_uv": sig0, **traj})

    # also slightly detuned
    a_det_plus = a_s + 0.01
    a_det_minus = a_s - 0.01
    detuned = {
        "above_saddle_a": flow_trajectory(sigma_s + 0.05, a_det_plus, b, c, t_span=(0.0, -50.0)),
        "below_saddle_a": flow_trajectory(sigma_s + 0.05, a_det_minus, b, c, t_span=(0.0, -50.0)),
    }

    # (4) temperature-like scan
    delta_grid = np.linspace(-0.05, 0.05, 21)
    T_scan = temperature_scan(b, c, delta_grid)

    # (5) Wetterich toy flow
    wett = []
    for s0 in [0.05, 0.20, 0.50, 1.0, 1.5]:
        wett.append({"sigma_uv": s0, **wetterich_trajectory(s0)})

    out = {
        "L": "L467",
        "title": "RG saddle-FP unstable branch as cluster-dip origin (speculation)",
        "cubic_FP_catalogue": cases,
        "saddle_locus": {
            "b": b, "c": c, "a_saddle": a_s, "sigma_saddle": sigma_s,
            "fps": fps_at_saddle,
        },
        "trajectories_at_saddle": trajectories,
        "detuned_trajectories": detuned,
        "temperature_scan": T_scan,
        "wetterich_toy": wett,
        "notes": [
            "saddle 정의: cubic 에서 b^2=4ac 인 두 비자명 FP 합류점.",
            "T_eff = 1/dwell 은 saddle 근방 머무름 시간의 역수.",
            "delta -> 0 에서 dwell -> infty, T_eff -> 0 (cold passage).",
            "detuning 부호가 IR 도달 sigma 의 분기를 결정.",
        ],
    }

    out_path = RES / "rg_flow_results.json"
    with out_path.open("w") as f:
        json.dump(out, f, indent=2, default=float)
    print(f"[L467] wrote {out_path}")

    # quick textual summary
    print("\n=== cubic FP catalogue ===")
    for case in cases:
        print(f"  a={case['a']:+.3f} b={case['b']:+.3f} c={case['c']:+.3f}: "
              f"{[(round(r,4), round(bp,4), cls) for r,bp,cls in case['fps']]}")
    print(f"\n=== saddle ===  a*={a_s:.4f}  sigma*={sigma_s:.4f}")
    print(f"  FPs at saddle tuning: {fps_at_saddle}")
    print("\n=== T_eff scan ===")
    for d, dw, Te in zip(T_scan["delta"], T_scan["dwell"], T_scan["T_eff"]):
        print(f"  delta={d:+.3f}  dwell={dw:8.3f}  T_eff={Te:.4f}")


if __name__ == "__main__":
    main()
