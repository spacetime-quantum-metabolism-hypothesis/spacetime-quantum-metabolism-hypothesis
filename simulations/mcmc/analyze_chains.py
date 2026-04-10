# -*- coding: utf-8 -*-
"""
analyze_chains.py

Post-process Cobaya MCMC chains: corner plots, constraint tables, AIC/BIC.
STUB: runs after Phase 3 MCMC completes.
"""
import sys


def analyze(chain_root):
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

    # Best-fit
    try:
        bf_chi2 = -2 * samples.getLikeStats().logLike_sample
        print(f"\nBest-fit -2*logL = {bf_chi2:.2f}")
    except Exception:
        pass

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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_chains.py <chain_root>")
        print("Example: python analyze_chains.py chains/sqmh_planck_desi_RP")
        sys.exit(1)
    analyze(sys.argv[1])
