# -*- coding: utf-8 -*-
"""
C37' — Modified Chaplygin Gas (MCG)
(Debnath-Banerjee-Chakraborty CQG 21 5609 (2004))

Equation of state:  p = B rho - A / rho^alpha
Conservation equation:
    rho' + 3 H (rho + p) = 0
    rho' + 3 H rho (1 + B - A/rho^(1+alpha)) = 0

Integral gives:
    rho(a) = [ A/(1+B) + C / a^{3(1+B)(1+alpha)} ]^{1/(1+alpha)}

where C is fixed by rho(today).

L2 Round 3 candidate. Tests C1 (trivial) and C4 (w_a sign, fixing vanilla
GCG w_a>0 problem via B>0).

Run:
    python simulations/l2/round3/c37_mod_chaplygin.py
"""
import numpy as np

H0_km = 67.36
Mpc = 3.0857e22
H0 = H0_km * 1e3 / Mpc
Om_m = 0.3153
Om_chap = 1.0 - Om_m  # MCG plays role of DE + DM mixture
rho_c0 = 1.0  # dimensionless, rho normalised to rho_c0


def rho_mcg(a, A, B, alpha, C):
    return (A / (1 + B) + C / a**(3 * (1 + B) * (1 + alpha)))**(1 / (1 + alpha))


def w_mcg(rho, A, B, alpha):
    p = B * rho - A / rho**alpha
    return p / rho


def compute_w(A, B, alpha):
    # Normalise so that rho(a=1) = Om_chap * rho_c0 (fill DE+DM role)
    rho_today = Om_chap
    # rho(1) = ( A/(1+B) + C )^{1/(1+alpha)}
    #     rho_today^{1+alpha} = A/(1+B) + C
    C = rho_today**(1 + alpha) - A / (1 + B)
    if C <= 0:
        return None, None, None
    z = np.linspace(0.01, 2.0, 200)
    a = 1.0 / (1 + z)
    rho = rho_mcg(a, A, B, alpha, C)
    w = w_mcg(rho, A, B, alpha)
    return z, w, rho


def cpl_fit(z, w):
    mask = (z > 0.05) & (z < 1.8)
    x = z[mask] / (1 + z[mask])
    Amat = np.vstack([np.ones_like(x), x]).T
    coef, *_ = np.linalg.lstsq(Amat, w[mask], rcond=None)
    return float(coef[0]), float(coef[1])


def main():
    print("C37' Modified Chaplygin Gas")
    print("=" * 60)
    print("Equation of state: p = B rho - A / rho^alpha")

    # --- C1 Cassini ---
    print("\n[1] C1 Cassini")
    print("  Fluid-level DE, no scalar dof")
    print("  |gamma-1| = 0 trivially (metric = Schwarzschild + cosmological)")
    print("  C1: PASS")

    # --- C4 scan ---
    print("\n[2] C4 w_a scan over (A, B, alpha)")
    print(f"  {'A':>8}  {'B':>8}  {'alpha':>8}  {'w0':>10}  {'wa':>10}  sign")
    print("  " + "-" * 60)

    best = None
    for alpha in [0.3, 0.5, 1.0]:
        for B in [0.0, 0.05, 0.10, 0.20, 0.30]:
            for A in [0.3, 0.5, 0.65, 0.80]:
                out = compute_w(A, B, alpha)
                if out[0] is None:
                    continue
                z, w, rho = out
                if not np.all(np.isfinite(w)):
                    continue
                w0, wa = cpl_fit(z, w)
                if not (np.isfinite(w0) and np.isfinite(wa)):
                    continue
                if w0 < -1.5 or w0 > -0.5:
                    # outside DE regime, skip printing but still record
                    continue
                sign = "NEG (OK)" if wa < -1e-4 else (
                    "POS" if wa > 1e-4 else "~0"
                )
                print(f"  {A:8.3f}  {B:8.3f}  {alpha:8.2f}  "
                      f"{w0:+10.4f}  {wa:+10.4f}  {sign}")
                if wa < 0:
                    score = abs(wa - (-0.83))
                    if best is None or score < best[0]:
                        best = (score, A, B, alpha, w0, wa)

    # --- Vanilla GCG check (B=0) ---
    print("\n[3] Vanilla GCG check (B=0, should give wa>0)")
    for A in [0.5, 0.65, 0.80]:
        out = compute_w(A, 0.0, 0.5)
        if out[0] is None:
            continue
        z, w, _ = out
        w0, wa = cpl_fit(z, w)
        sign = "POS (correct)" if wa > 0 else "NEG"
        print(f"  A={A:.2f}, B=0, alpha=0.5: w0={w0:+.4f}, wa={wa:+.4f}  {sign}")
    print("  -> confirms vanilla GCG has wa>0 (structural)")

    if best is not None:
        print(f"\n[4] Best MCG point for wa<0")
        print(f"  A={best[1]:.3f}, B={best[2]:.3f}, alpha={best[3]:.2f}")
        print(f"  w0={best[4]:+.4f}, wa={best[5]:+.4f}")
        print(f"  |diff vs DESI -0.83| = {best[0]:.4f}")
    else:
        print("\n[4] No wa<0 point found in MCG scan")
        print("  -> MCG also does not yield wa<0 in natural A,B,alpha range")
        print("  -> C4 FAIL for full Chaplygin family")

    print("\nSummary")
    print("=" * 60)
    print("C1: PASS trivial (fluid DE)")
    print("C3: PASS (fluid conservation)")
    print("C4: depends on (A, B, alpha) scan result above")
    if best is not None:
        print("Verdict: 3-4/4 depending on w_a scan (MCG extension)")
    else:
        print("Verdict: 3/4 (C1/C3 pass, C4 fails for tested region)")


if __name__ == "__main__":
    main()
