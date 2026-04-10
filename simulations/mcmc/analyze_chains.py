# -*- coding: utf-8 -*-
"""
analyze_chains.py

Post-process Cobaya MCMC chains: corner plots, constraint tables, AIC/BIC,
Delta chi^2 vs LCDM baseline.

Usage:
  python analyze_chains.py <chain_root> [--lcdm <lcdm_chain_root>]

STUB: runs after Phase 3 MCMC completes.
"""
import argparse
import os
import sys


# Number of free params for AIC/BIC. SQMH adds xi + V_param_n to LCDM baseline.
K_SQMH_EXTRA = 2   # SQMH_xi, SQMH_V_param_n
# Approximate effective data points for BIC penalty. Planck TTTEEE + lowl +
# lensing + DESI DR2 (13) + DESY5 (~1700). Use conservative round number.
N_DATA_APPROX = 3000


def _best_fit_chi2(samples):
    """Return -2 ln L_max from a getdist MCSamples object.

    getdist.getLikeStats().logLike_sample is the -ln L value at the best-fit
    sample (NOT +ln L). So -2 ln L_max = 2 * logLike_sample.  Double-negating
    (as an earlier stub did) gives the WRONG sign and thus a nonsense chi^2.
    """
    ls = samples.getLikeStats()
    if ls is None:
        return None
    return 2.0 * ls.logLike_sample


def analyze(chain_root, lcdm_root=None):
    try:
        from getdist import loadMCSamples, plots
    except ImportError:
        print("getdist not installed. pip install getdist")
        sys.exit(1)

    print(f"Loading chains from {chain_root}...")
    samples = loadMCSamples(chain_root)

    # 1D marginalized constraints
    params = ['SQMH_xi', 'SQMH_V_param_n', 'H0', 'omega_m', 'sigma8', 'S8']
    print("\nMarginalized 68% CL:")
    for p in params:
        try:
            mean = samples.mean(p)
            std = samples.std(p)
            print(f"  {p:20s}: {mean:+.4f} +/- {std:.4f}")
        except Exception as e:
            print(f"  {p:20s}: n/a ({e})")

    # Best-fit chi^2 (sign-correct)
    chi2_sqmh = _best_fit_chi2(samples)
    if chi2_sqmh is not None:
        k_sqmh = K_SQMH_EXTRA  # relative to LCDM
        aic_sqmh = chi2_sqmh + 2 * k_sqmh
        import math
        bic_sqmh = chi2_sqmh + k_sqmh * math.log(N_DATA_APPROX)
        print(f"\nBest-fit -2 ln L (SQMH)  : {chi2_sqmh:.2f}")
        print(f"AIC contribution (2k)    : +{2*k_sqmh}")
        print(f"BIC contribution (k lnN) : +{k_sqmh*math.log(N_DATA_APPROX):.2f}")

        if lcdm_root:
            print(f"\nLoading LCDM reference chain from {lcdm_root}...")
            lcdm = loadMCSamples(lcdm_root)
            chi2_lcdm = _best_fit_chi2(lcdm)
            if chi2_lcdm is not None:
                d_chi2 = chi2_sqmh - chi2_lcdm
                d_aic = d_chi2 + 2 * k_sqmh
                d_bic = d_chi2 + k_sqmh * math.log(N_DATA_APPROX)
                print(f"LCDM -2 ln L            : {chi2_lcdm:.2f}")
                print(f"Delta chi^2 (SQMH-LCDM) : {d_chi2:+.2f}")
                print(f"Delta AIC               : {d_aic:+.2f}")
                print(f"Delta BIC               : {d_bic:+.2f}")
                verdict = ("Path A success" if d_aic < -6 else
                           "need full joint" if d_aic < -2 else
                           "Path F (reject)")
                print(f"Phase-3 verdict         : {verdict}")

    # Corner plot
    g = plots.get_subplot_plotter()
    g.triangle_plot(samples, params, filled=True)
    g.export(f'{chain_root}_corner.png')
    print(f"\nCorner plot saved: {chain_root}_corner.png")

    # w0-wa plane (if derived params present)
    try:
        g2 = plots.get_single_plotter()
        g2.plot_2d(samples, ['w0_eff', 'wa_eff'], filled=True)
        g2.export(f'{chain_root}_w0wa.png')
        print(f"w0-wa plane saved: {chain_root}_w0wa.png")
    except Exception:
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('chain_root')
    ap.add_argument('--lcdm', dest='lcdm', default=None,
                    help='LCDM reference chain root for Delta chi^2 / AIC / BIC')
    args = ap.parse_args()

    if not os.path.exists(args.chain_root + '.1.txt') and \
       not os.path.exists(args.chain_root):
        print(f"No chain files found at {args.chain_root}")
        sys.exit(1)
    analyze(args.chain_root, lcdm_root=args.lcdm)


if __name__ == "__main__":
    main()
