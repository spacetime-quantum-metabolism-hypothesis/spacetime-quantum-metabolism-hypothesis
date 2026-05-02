"""
L462 자유 추측 toy: cluster 영역 sigma_0 dip 의 두 가지 phenomenological 모양 비교.

목적
----
1. V-shape (절대값 선형) 모양:        sigma0(rho) = a + b * |log10(rho/rho_c)|
2. Critical scaling (universality):  sigma0(rho) = a + b * |1 - rho/rho_c|^nu
   - mean-field:  nu = 1/2
   - 3D Ising:    nu ~ 0.630
   - Heisenberg:  nu ~ 0.711

두 모양이 cluster 영역 (rho ~ 1e-26 .. 1e-24 kg/m^3) 에서 어떻게 다른 dip 형태를
주는지를 시각적으로 비교하고, hypothetical 측정 grid 에서 두 모양 사이의 chi^2
구분 가능성을 어림한다.

주의: 이 코드는 *자유 추측용 toy* 이며, 어떤 SQMH 핵심 예측에도 들어가지 않는다.
파라미터 (a, b, rho_c, nu) 모두 손으로 고른 placeholder. 실제 critical density 의
물리적 값은 microphysical n-field Lagrangian 으로부터 도출되어야 한다.
"""

from __future__ import annotations

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUTDIR = os.path.join(os.path.dirname(__file__))


# ------------------------------------------------------------------
# 1. Phenomenological shapes
# ------------------------------------------------------------------
def shape_vshape(rho: np.ndarray, a: float, b: float, rho_c: float) -> np.ndarray:
    """V-shape in log(rho)."""
    return a + b * np.abs(np.log10(rho / rho_c))


def shape_critical(
    rho: np.ndarray, a: float, b: float, rho_c: float, nu: float
) -> np.ndarray:
    """|1 - rho/rho_c|^nu — critical scaling toy.

    Note: 진짜 universality class 의 order parameter scaling 은 보통
    |T - T_c|^beta 또는 susceptibility |T - T_c|^(-gamma) 형태이지만,
    여기서는 'dip 의 모양' 만 비교하기 위해 generic 한 |x|^nu 사용.
    """
    eps = np.abs(1.0 - rho / rho_c)
    return a - b * np.power(eps + 1e-12, nu)  # 음수 부호: rho_c 에서 dip 이 깊어지게


# ------------------------------------------------------------------
# 2. Dimensional argument: rho_critical 후보 추정
# ------------------------------------------------------------------
def dimensional_estimate():
    """
    cluster 영역 평균 밀도가 ~ 10^-26 kg/m^3 인 것이 *왜* 의미 있을 수 있는지
    여러 후보 dimensional combination 을 dump 해 본다.

    Planck density rho_P = c^5 / (hbar G^2) ~ 5.16e96 kg/m^3.
    Critical cosmological density today rho_crit0 ~ 8.5e-27 kg/m^3.
    Cluster mean overdensity ~ 200 * rho_crit0 ~ 1.7e-24 kg/m^3.
    Cluster outskirts (filament 경계) ~ rho_crit0 ~ 1e-26 kg/m^3.
    """
    G = 6.674e-11
    hbar = 1.055e-34
    c = 2.998e8
    rho_P = c**5 / (hbar * G**2)
    rho_crit0 = 8.5e-27  # kg/m^3, h=0.7 근방
    H0_inv2 = (1.0 / 2.27e-18) ** 2  # (1/H0)^2  [s^2]

    candidates = {
        "rho_P (Planck)": rho_P,
        "rho_crit0 (cosmo)": rho_crit0,
        "200 * rho_crit0 (virial)": 200 * rho_crit0,
        "geometric mean(rho_P, rho_crit0)": np.sqrt(rho_P * rho_crit0),
        "rho_P^(1/3) * rho_crit0^(2/3)": rho_P ** (1 / 3) * rho_crit0 ** (2 / 3),
        "rho_P^(1/4) * rho_crit0^(3/4)": rho_P ** (1 / 4) * rho_crit0 ** (3 / 4),
    }
    return candidates


# ------------------------------------------------------------------
# 3. Distinguishability test
# ------------------------------------------------------------------
def chi2_between_shapes(
    rho_grid: np.ndarray,
    pars_v: tuple,
    pars_c: tuple,
    sigma_meas: float,
) -> float:
    """두 phenomenology 가 같은 grid 의 측정에서 얼마나 구분되는지."""
    yv = shape_vshape(rho_grid, *pars_v)
    yc = shape_critical(rho_grid, *pars_c)
    return float(np.sum(((yv - yc) / sigma_meas) ** 2))


def fit_critical_to_vshape(rho_grid, pars_v, nu_grid):
    """V-shape 의 mock data 를 critical 모양으로 피팅했을 때 best nu."""
    yv = shape_vshape(rho_grid, *pars_v)
    a_v, b_v, rho_c = pars_v
    chi2s = []
    for nu in nu_grid:
        # least-squares for (a, b) at fixed nu, rho_c
        eps = np.abs(1.0 - rho_grid / rho_c) + 1e-12
        X = np.power(eps, nu)
        # yv ≈ a - b*X  →  fit linear
        A = np.vstack([np.ones_like(X), -X]).T
        coef, *_ = np.linalg.lstsq(A, yv, rcond=None)
        a_hat, b_hat = coef
        pred = a_hat - b_hat * X
        chi2s.append(float(np.sum((yv - pred) ** 2)))
    return np.array(chi2s)


# ------------------------------------------------------------------
# 4. Main
# ------------------------------------------------------------------
def main():
    print("=" * 70)
    print("L462 toy: cluster sigma_0 dip — V-shape vs critical scaling")
    print("=" * 70)

    print("\n[Dimensional rho_c candidates]")
    for k, v in dimensional_estimate().items():
        print(f"  {k:42s} = {v: .3e} kg/m^3")

    # placeholder fit-quality parameters
    rho_c = 1.0e-26  # kg/m^3 (cluster outskirts)
    a, b = 1.0, 0.20
    pars_v = (a, b, rho_c)

    rho_grid = np.logspace(-30, -22, 400)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    # left: shape comparison
    ax = axes[0]
    ax.plot(
        rho_grid,
        shape_vshape(rho_grid, *pars_v),
        "k-",
        lw=2,
        label="V-shape: a+b|log10(rho/rho_c)|",
    )
    for nu, color, name in [
        (0.5, "tab:blue", "mean-field nu=0.5"),
        (0.630, "tab:orange", "3D Ising nu=0.630"),
        (0.711, "tab:green", "Heisenberg nu=0.711"),
        (1.0, "tab:red", "linear nu=1.0"),
    ]:
        # match amplitude at rho = 1e-30 (far from rho_c) for visual fairness
        eps_ref = abs(1.0 - 1e-30 / rho_c)
        b_c = (b * abs(np.log10(1e-30 / rho_c))) / (eps_ref**nu)
        ax.plot(
            rho_grid,
            shape_critical(rho_grid, a, b_c, rho_c, nu),
            color=color,
            lw=1.4,
            label=name,
        )
    ax.axvline(rho_c, color="gray", ls=":", lw=1)
    ax.set_xscale("log")
    ax.set_xlabel(r"$\rho$  [kg/m$^3$]")
    ax.set_ylabel(r"$\sigma_0$ (toy units)")
    ax.set_title("dip shape comparison")
    ax.legend(fontsize=8, loc="lower left")
    ax.grid(alpha=0.3)

    # right: nu fit landscape (V-shape data → critical fit)
    rho_meas = np.logspace(-28, -24, 9)  # 9 hypothetical measurements across cluster band
    nu_grid = np.linspace(0.2, 1.4, 80)
    chi2s = fit_critical_to_vshape(rho_meas, pars_v, nu_grid)
    ax2 = axes[1]
    ax2.plot(nu_grid, chi2s - chi2s.min(), "b-")
    for nu_ref, name in [(0.5, "MF"), (0.630, "Ising"), (0.711, "Heis"), (1.0, "linear")]:
        ax2.axvline(nu_ref, color="gray", ls=":", lw=1)
        ax2.text(
            nu_ref,
            ax2.get_ylim()[1] * 0.8 if False else 0.1,
            name,
            rotation=90,
            fontsize=8,
        )
    ax2.set_xlabel(r"trial $\nu$")
    ax2.set_ylabel(r"$\Delta \chi^2$ (V-shape data → critical fit)")
    ax2.set_title("which universality best mimics V-shape?")
    ax2.grid(alpha=0.3)

    nu_best = nu_grid[np.argmin(chi2s)]
    print(f"\n[V-shape ↔ critical fit]  best mimicking nu = {nu_best:.3f}")
    print(f"  (means: V-shape data is closest to nu={nu_best:.2f} critical scaling)")

    fig.tight_layout()
    out_png = os.path.join(OUTDIR, "shape_compare.png")
    fig.savefig(out_png, dpi=130)
    print(f"\nSaved: {out_png}")

    # distinguishability between mean-field and Ising (for fixed amplitude match)
    pars_c_mf = (a, b * abs(np.log10(1e-30 / rho_c)) / (abs(1 - 1e-30 / rho_c) ** 0.5),
                 rho_c, 0.5)
    pars_c_is = (a, b * abs(np.log10(1e-30 / rho_c)) / (abs(1 - 1e-30 / rho_c) ** 0.630),
                 rho_c, 0.630)
    sigma_meas = 0.02  # toy 2% per point
    chi2_mf_is = chi2_between_shapes(
        rho_meas, (pars_c_mf[0], pars_c_mf[1], pars_c_mf[2]), pars_c_is, sigma_meas
    )
    # NB: 위 함수는 V vs C 비교용이라 (a,b,rho_c) 만 받음. 따로:
    yv = shape_critical(rho_meas, *pars_c_mf)
    yc = shape_critical(rho_meas, *pars_c_is)
    chi2_mf_is = float(np.sum(((yv - yc) / sigma_meas) ** 2))
    print(f"\n[Pairwise 2% measurement discrim, 9 points]")
    print(f"  mean-field vs 3D-Ising  chi^2 = {chi2_mf_is:.2f}  "
          f"(sqrt = {np.sqrt(chi2_mf_is):.2f} sigma)")


if __name__ == "__main__":
    main()
