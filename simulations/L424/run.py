"""
L424 — dSph (dwarf spheroidal) σ₀ saturation P9 anchor forecast (4인팀 실행)

목적: paper §6.1 row #5 "Three-regime 강제성 약함 (anchor 4-5개 필요),
dSph + NS 추가" 의 *dSph 부분* 만 분리해 P9 anchor pool (5 classical
Local Group dSph) 추가 시 BB three-regime 강제력 정량.

핵심 차별점 (vs L405 P9 forecast):
  L405: P9 dSph 1점 toy (-0.3, 0.85, 0.12) 합성치 only.
  L424: 5 dSph (Draco, UMi, Sculptor, Sextans, Carina) archive 매핑,
        환경-only anchor 모드 (σ₀ free) + σ₀-anchor 모드 비교,
        mock false-rate 측정 (강제력 ≠ pool 확대 분리).

CLAUDE.md 준수:
  - 8인팀 합의 (ATTACK/NEXT_STEP) 의 *실행* 단계만 — 새 이론 도출 없음.
  - dSph σ₀ "측정값" 은 archive (McConnachie 2012, Walker 2009, Gaia DR3 RVS)
    의 σ_los → M_dyn → 정규화 (M_dyn / r_half³) 1차 변환 toy. 정확한
    "SQMH σ₀" 변환은 paper §3.4 후속 (ATTACK B4).
  - ρ_env 매핑은 D_LG 거리 기반 1차 근사 — galactic-internal regime
    (별별 자체 밀도) vs Local Group regime (kpc 바깥) 두 매핑 모두 시도.
  - 결과는 *상대 변화* (without dSph → with dSph) 만 신뢰 가능.

산출:
  results/L424/run_log.txt : 콘솔 출력 캡처
  results/L424/report.json : 정량 요약
"""
from __future__ import annotations

import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

RNG_SEED = 4242

# ============================================================================
# 0. Baseline anchor pool (L405 toy synthetic — base.md §3.5/§3.6 calibrated)
# ============================================================================

BASE_ANCHORS = np.array([
    # (log10_rho_env, sigma0_obs, sigma_err)  [unitless toy]
    (+4.5, 1.00, 0.05),  # SPARC core 1     (galactic-internal)
    (+3.7, 0.96, 0.05),  # SPARC core 2
    (+2.8, 0.40, 0.06),  # SPARC mid 1      (regime gap down)
    (+2.0, 0.35, 0.06),  # SPARC mid 2
    (+0.5, 0.42, 0.08),  # SPARC outer
    (-1.0, 0.95, 0.10),  # Cluster A1689    (regime gap up)
    (-2.0, 1.10, 0.07),  # Cosmic 1
    (-2.5, 1.15, 0.07),  # Cosmic 2
])

# ============================================================================
# 1. Local Group dSph archive (McConnachie 2012 + Walker 2009 + Gaia DR3 RVS)
# ============================================================================
# Public archive values (σ_los central velocity dispersion, r_half projected
# half-light, D_LG Local Group barycentric distance, M_dyn dynamical mass).
# References:
#   McConnachie 2012 AJ 144, 4 (arXiv:1204.1562) — Table 2 baseline.
#   Walker et al. 2009 ApJ 704, 1274 — σ profile updates.
#   Gaia DR3 RVS (Vallenari 2023) — RV refinement; values rounded to McC 2012.

DSPH = {
    # name        sigma_los  r_half_pc  D_LG_kpc   M_dyn_1e7Msun
    "Draco":      (9.1,      221.0,      82.0,      2.2),
    "UrsaMinor":  (9.5,      181.0,      78.0,      1.8),
    "Sculptor":   (9.2,      283.0,      86.0,      3.4),
    "Sextans":    (7.9,      695.0,      89.0,      4.1),
    "Carina":     (6.6,      250.0,     106.0,      0.8),
}

def dsph_to_anchor(name, mode="local_group"):
    """
    Convert dSph archive measurement to (log10 rho_env, sigma0_obs, sigma_err).

    mode == "local_group" : ρ_env = M_LG_local / V_LG_local (~ kpc 바깥 환경
            밀도). 1차 근사로 D_LG 의 함수: log10 ρ_env ~ -0.5 ~ 0
            (cluster~cosmic 사이).
    mode == "galactic_internal" : ρ_env = M_dyn / (4/3 π r_half³). dSph
            *내부* 별별 자체 밀도 ~ +3 (galactic-internal regime).

    σ₀_obs 는 σ_los 를 baseline anchor 의 σ₀ scale 로 정규화 (toy proxy).
    SQMH paper 의 σ₀ ↔ σ_los 정확 변환은 paper §3.4 후속 (ATTACK B4).
    여기서는 σ_los / σ_ref 로 unit-less 정규화 + Walker 2009 typical err.
    """
    s_los, r_half_pc, D_LG, M_dyn = DSPH[name]
    # σ₀ proxy: σ_los / σ_ref where σ_ref = 10 km/s ~ classical dSph mean.
    # 정규화 후 baseline anchor 와 같은 스케일 (~0.4 ~ 1.15) 에 들어옴.
    s_ref = 10.0
    sig0 = 0.95 * (s_los / s_ref)  # 9.5 km/s → ~0.90 (cosmic regime 근방)
    sig_err = 0.10 * sig0          # 10% 통계 + systematic
    if mode == "local_group":
        # log10 ρ_env: D_LG 80 kpc 평균 → cluster~cosmic 경계 ~ -1.0 ~ -0.5
        # toy: log10 ρ_env = -0.5 - 0.01 * (D_LG - 80)
        log_rho = -0.5 - 0.01 * (D_LG - 80.0)
    elif mode == "galactic_internal":
        # M_dyn (1e7 Msun) / (4/3 π r_half_pc³) 의 SI 환산 후 log10
        # 1 Msun ≈ 2e30 kg, 1 pc ≈ 3.086e16 m
        Msun_kg = 1.989e30
        pc_m = 3.086e16
        V = (4.0 / 3.0) * math.pi * (r_half_pc * pc_m) ** 3
        M = M_dyn * 1e7 * Msun_kg
        rho = M / V  # kg/m^3
        # ρ_crit ≈ 9.47e-27 kg/m^3 (h=0.7).  log10(ρ/ρ_crit)
        rho_crit = 9.47e-27
        log_rho = math.log10(rho / rho_crit)
    else:
        raise ValueError(mode)
    return (log_rho, sig0, sig_err)

def build_dsph_anchors(mode="local_group"):
    rows = []
    for name in DSPH:
        rows.append(dsph_to_anchor(name, mode))
    return np.array(rows)

# ============================================================================
# 2. Models (L405 와 동일 — three_regime / two_regime / monotonic / lcdm)
# ============================================================================

def model_three_regime(theta, x):
    s_h, s_m, s_l, t1, t2 = theta
    if t1 <= t2:
        return None
    return np.where(x > t1, s_h, np.where(x > t2, s_m, s_l))

def model_two_regime(theta, x):
    s_h, s_l, t1 = theta
    return np.where(x > t1, s_h, s_l)

def model_monotonic(theta, x):
    a, b, x0, w = theta
    return a + b / (1.0 + np.exp(-(x - x0) / w))

def model_lcdm(theta, x):
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

# ============================================================================
# 3. Likelihood / prior / Laplace ln Z (L405 패턴)
# ============================================================================

def make_ll(anchors):
    log_rho = anchors[:, 0]
    sig_obs = anchors[:, 1]
    sig_err = anchors[:, 2]
    def log_likelihood(model_name, theta):
        fn = MODELS[model_name]["fn"]
        pred = fn(theta, log_rho)
        if pred is None:
            return -np.inf
        chi2 = np.sum(((sig_obs - pred) / sig_err) ** 2)
        return -0.5 * chi2
    return log_likelihood

def log_prior(model_name, theta, R):
    mu = PRIOR_CENTRES[model_name]
    s = PRIOR_NATSCALE[model_name] * R
    if len(theta) != len(mu):
        return -np.inf
    diff = (np.asarray(theta) - mu) / s
    return -0.5 * np.sum(diff ** 2) - np.sum(np.log(s * math.sqrt(2 * math.pi)))

def laplace_logz(anchors, model_name, R, restarts=8, rng=None):
    rng = rng or np.random.default_rng(RNG_SEED)
    mu = PRIOR_CENTRES[model_name]
    s = PRIOR_NATSCALE[model_name] * R
    k = len(mu)
    log_likelihood = make_ll(anchors)

    def neg_logp(theta):
        lp = log_prior(model_name, theta, R)
        ll = log_likelihood(model_name, theta)
        if not np.isfinite(lp + ll):
            return 1e8
        return -(lp + ll)

    best = (np.inf, None)
    for _ in range(restarts):
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
    logp_map = -best[0]
    chi2_map = -2.0 * log_likelihood(model_name, theta_map)

    eps = 1e-3 * np.maximum(np.abs(theta_map), 1.0)
    H = np.zeros((k, k))
    for i in range(k):
        for j in range(k):
            if i == j:
                ei = np.zeros(k); ei[i] = eps[i]
                fpp = neg_logp(theta_map + ei)
                fmm = neg_logp(theta_map - ei)
                f0 = -logp_map
                H[i, i] = (fpp - 2 * f0 + fmm) / (eps[i] ** 2)
            else:
                ei = np.zeros(k); ei[i] = eps[i]
                ej = np.zeros(k); ej[j] = eps[j]
                fpp = neg_logp(theta_map + ei + ej)
                fpm = neg_logp(theta_map + ei - ej)
                fmp = neg_logp(theta_map - ei + ej)
                fmm = neg_logp(theta_map - ei - ej)
                H[i, j] = (fpp - fpm - fmp + fmm) / (4 * eps[i] * eps[j])
    H = 0.5 * (H + H.T)
    sign, logdet = np.linalg.slogdet(H)
    if sign <= 0 or not np.isfinite(logdet):
        H_reg = H + 1e-3 * np.eye(k)
        sign, logdet = np.linalg.slogdet(H_reg)
        if sign <= 0:
            return dict(logZ=np.nan, theta_map=theta_map,
                        chi2_map=chi2_map, hess_singular=True)
    logZ = logp_map + 0.5 * k * math.log(2 * math.pi) - 0.5 * logdet
    return dict(logZ=logZ, theta_map=theta_map, chi2_map=chi2_map,
                hess_singular=False)

# ============================================================================
# 4. R-grid sensitivity
# ============================================================================

R_LIST = [2.0, 3.0, 5.0, 10.0]

def r_grid(anchors, label=""):
    rows = []
    for R in R_LIST:
        out = {"R": R}
        for m in MODELS:
            r = laplace_logz(anchors, m, R)
            out[m] = float((r or {}).get("logZ", np.nan))
        rows.append(out)
    return rows

def fmt_grid(rows, label):
    print(f"\n--- ln Z grid [{label}] ---")
    print(f"  R    | {'three_R':>9} | {'two_R':>9} | {'mono':>9} | "
          f"{'lcdm':>9} || ΔlnZ(3R−L) | ΔlnZ(2R−L)")
    print("  " + "-" * 88)
    for r in rows:
        d3 = r["three_regime"] - r["lcdm"]
        d2 = r["two_regime"] - r["lcdm"]
        print(f"  R={r['R']:<3g}| {r['three_regime']:9.3f} | "
              f"{r['two_regime']:9.3f} | {r['monotonic']:9.3f} | "
              f"{r['lcdm']:9.3f} || {d3:+10.3f} | {d2:+10.3f}")

# ============================================================================
# 5. Mock injection false-rate (강제력 ≠ pool 확대 분리 — ATTACK B2 핵심)
# ============================================================================

def mock_false_rate(N_anchors, n_mock=200, seed=0, sig_truth=0.85, err=0.10):
    """
    LCDM null: σ_truth 일정. three-regime fit 이 ΔAICc>10 으로 lcdm 을 이기는
    비율 측정. anchor 갯수 N 의 함수로 false-rate 가 어떻게 변하는지가
    "dSph 추가의 강제력" 진단.
    """
    rng = np.random.default_rng(seed)
    false = 0
    for _ in range(n_mock):
        # 합성 anchor 위치 (baseline 8 + dSph 추가시 +5)
        # log_rho 는 baseline 분포에서 sample
        if N_anchors == 8:
            log_rho = BASE_ANCHORS[:, 0]
        else:
            extra = build_dsph_anchors("local_group")
            log_rho = np.concatenate([BASE_ANCHORS[:, 0], extra[:, 0]])
        sig_obs = rng.normal(sig_truth, err, len(log_rho))
        sig_err_arr = np.full(len(log_rho), err)
        anchors = np.column_stack([log_rho, sig_obs, sig_err_arr])

        log_likelihood = make_ll(anchors)
        # quick chi2 minimisers (no Laplace, just MAP)
        best3, best1 = np.inf, np.inf
        for _ in range(3):
            mu3 = PRIOR_CENTRES["three_regime"]
            s3 = PRIOR_NATSCALE["three_regime"] * 5.0
            x0 = mu3 + 0.3 * s3 * rng.standard_normal(5)
            r = minimize(lambda t: -log_likelihood("three_regime", t),
                         x0, method="Nelder-Mead",
                         options=dict(maxiter=2000, xatol=1e-4, fatol=1e-4))
            if r.fun < best3:
                best3 = r.fun
        for _ in range(2):
            x0 = np.array([sig_truth + 0.05 * rng.standard_normal()])
            r = minimize(lambda t: -log_likelihood("lcdm", t),
                         x0, method="Nelder-Mead",
                         options=dict(maxiter=1000, xatol=1e-5, fatol=1e-5))
            if r.fun < best1:
                best1 = r.fun
        chi2_3 = 2 * best3
        chi2_1 = 2 * best1
        N = len(anchors)
        aicc_3 = chi2_3 + 2 * 5 + (2 * 5 * 6) / max(N - 5 - 1, 1)
        aicc_1 = chi2_1 + 2 * 1 + (2 * 1 * 2) / max(N - 2, 1)
        if (aicc_1 - aicc_3) > 10:
            false += 1
    return false / n_mock

# ============================================================================
# 6. Three forecast scenarios for dSph σ₀ value (B6 부호-결정 임계 사전등록)
# ============================================================================

def dsph_scenario(scenario, mode="local_group"):
    """
    scenario:
      "compat_cosmic"   : σ₀_dSph ≈ cosmic regime (1.05–1.15) → V-shape 강화
      "compat_galactic" : σ₀_dSph ≈ galactic regime (0.95–1.00) → 단조 회복
      "tension_cluster" : σ₀_dSph ≈ cluster regime (0.40–0.50) → V-shape 위치 이동
      "null_archive"    : σ₀_dSph = archive 변환값 그대로
    """
    rows = build_dsph_anchors(mode)  # log_rho 는 mode 의존, σ₀ 는 archive 변환
    overrides = {
        "compat_cosmic":   1.10,
        "compat_galactic": 0.97,
        "tension_cluster": 0.45,
        "null_archive":    None,
    }
    val = overrides.get(scenario)
    if val is not None:
        rows = rows.copy()
        rows[:, 1] = val
    return rows

# ============================================================================
# 7. Main
# ============================================================================

def main():
    print("=" * 80)
    print("L424 — dSph P9 anchor pool forecast (5 classical Local Group dSph)")
    print("=" * 80)

    # archive summary
    print("\n--- 5 dSph archive (McConnachie 2012 + Walker 2009 + Gaia DR3) ---")
    print(f"  {'name':<10s}  σ_los  r_half(pc)  D_LG(kpc)  M_dyn(1e7 Msun)")
    for name, vals in DSPH.items():
        print(f"  {name:<10s}  {vals[0]:5.1f}  {vals[1]:9.0f}  "
              f"{vals[2]:9.1f}  {vals[3]:14.2f}")

    print("\n--- ρ_env mapping (two modes) ---")
    print(f"  {'name':<10s}  log10(ρ/ρ_c)_LG  log10(ρ/ρ_c)_internal  σ₀_proxy  σ_err")
    for name in DSPH:
        a_lg = dsph_to_anchor(name, "local_group")
        a_in = dsph_to_anchor(name, "galactic_internal")
        print(f"  {name:<10s}  {a_lg[0]:+15.2f}  {a_in[0]:+21.2f}  "
              f"{a_lg[1]:8.3f}  {a_lg[2]:5.3f}")

    # baseline (no dSph) ln Z grid
    rows_base = r_grid(BASE_ANCHORS, "baseline 8 anchors (no dSph)")
    fmt_grid(rows_base, "baseline (no dSph)")

    # ----------------------------------------------------------------------
    # Scenario A — Local-Group regime mapping (kpc 바깥, low-ρ_env 추가)
    # ----------------------------------------------------------------------
    print("\n=== Scenario A: dSph mapped to Local-Group regime (kpc-outer) ===")
    by_scenario_LG = {}
    for sc in ("null_archive", "compat_cosmic", "compat_galactic",
               "tension_cluster"):
        ex = dsph_scenario(sc, "local_group")
        anchors = np.vstack([BASE_ANCHORS, ex])
        rows = r_grid(anchors, f"+dSph[LG]/{sc}")
        by_scenario_LG[sc] = rows
        # short summary at R=5
        r5 = next(r for r in rows if abs(r["R"] - 5.0) < 1e-6)
        d3 = r5["three_regime"] - r5["lcdm"]
        d2 = r5["two_regime"] - r5["lcdm"]
        b5 = next(r for r in rows_base if abs(r["R"] - 5.0) < 1e-6)
        b3 = b5["three_regime"] - b5["lcdm"]
        b2 = b5["two_regime"] - b5["lcdm"]
        print(f"  [{sc:18s}] ΔlnZ(3R−L)={d3:+.3f} (Δ vs baseline {d3-b3:+.3f}) "
              f"ΔlnZ(2R−L)={d2:+.3f} (Δ vs baseline {d2-b2:+.3f})")

    # ----------------------------------------------------------------------
    # Scenario B — galactic-internal regime mapping (별별 자체 밀도)
    # ----------------------------------------------------------------------
    print("\n=== Scenario B: dSph mapped to galactic-internal regime ===")
    by_scenario_int = {}
    for sc in ("null_archive", "compat_cosmic", "compat_galactic",
               "tension_cluster"):
        ex = dsph_scenario(sc, "galactic_internal")
        anchors = np.vstack([BASE_ANCHORS, ex])
        rows = r_grid(anchors, f"+dSph[INT]/{sc}")
        by_scenario_int[sc] = rows
        r5 = next(r for r in rows if abs(r["R"] - 5.0) < 1e-6)
        d3 = r5["three_regime"] - r5["lcdm"]
        d2 = r5["two_regime"] - r5["lcdm"]
        b5 = next(r for r in rows_base if abs(r["R"] - 5.0) < 1e-6)
        b3 = b5["three_regime"] - b5["lcdm"]
        b2 = b5["two_regime"] - b5["lcdm"]
        print(f"  [{sc:18s}] ΔlnZ(3R−L)={d3:+.3f} (Δ vs baseline {d3-b3:+.3f}) "
              f"ΔlnZ(2R−L)={d2:+.3f} (Δ vs baseline {d2-b2:+.3f})")

    # ----------------------------------------------------------------------
    # Mock false-rate: 8 anchor (baseline) vs 13 anchor (+dSph LG)
    # ----------------------------------------------------------------------
    print("\n=== Mock injection false-detection rate (LCDM null, n_mock=200) ===")
    rate8 = mock_false_rate(8, n_mock=200, seed=11)
    rate13 = mock_false_rate(13, n_mock=200, seed=11)
    print(f"  N=8  (baseline)        : false rate = {rate8:.1%}")
    print(f"  N=13 (+5 dSph LG)      : false rate = {rate13:.1%}")
    print(f"  Δ false rate (+dSph)   : {(rate13-rate8)*100:+.1f}%-points")
    if rate13 < rate8 - 0.05:
        verdict = "FALSE-RATE 감소 — 강제력 부분 회복 신호"
    elif rate13 > rate8 + 0.05:
        verdict = "FALSE-RATE 증가 — pool 확대 자유도-우위 악화"
    else:
        verdict = "FALSE-RATE ~동일 — dSph 추가 강제력 효과 없음"
    print(f"  판정: {verdict}")

    # ----------------------------------------------------------------------
    # JSON 요약
    # ----------------------------------------------------------------------
    out = dict(
        seed=RNG_SEED,
        n_dsph=len(DSPH),
        dsph_archive={k: list(v) for k, v in DSPH.items()},
        rho_env_mapping={
            name: dict(local_group=dsph_to_anchor(name, "local_group"),
                       galactic_internal=dsph_to_anchor(name, "galactic_internal"))
            for name in DSPH
        },
        baseline_grid=rows_base,
        scenario_LG=by_scenario_LG,
        scenario_internal=by_scenario_int,
        mock_false_rate=dict(N8=rate8, N13=rate13, delta=rate13 - rate8,
                             verdict=verdict),
    )
    out_dir = Path(__file__).resolve().parent.parent.parent / "results" / "L424"
    out_dir.mkdir(parents=True, exist_ok=True)

    def _jsonify(o):
        if isinstance(o, dict):
            return {k: _jsonify(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [_jsonify(v) for v in o]
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        return o

    with (out_dir / "report.json").open("w") as f:
        json.dump(_jsonify(out), f, indent=2)
    print(f"\n[saved] {out_dir / 'report.json'}")
    print("\n=== END L424 run.py ===")

if __name__ == "__main__":
    main()
