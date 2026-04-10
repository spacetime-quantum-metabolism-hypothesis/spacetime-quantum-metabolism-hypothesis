# -*- coding: utf-8 -*-
"""
verify_background.py

Cross-check: Phase 1 quintessence.py ODE vs CLASS-SQMH patched background.
Runs identical (V_family, beta, params) through both and compares E(z), w(z).

Canonical V_family: strings "mass"|"RP"|"exp" (see patch_template.py).
Pass criterion: max relative deviation |Delta E / E| < 0.1% over 0 < z < 3.
 (README §"Phase 1 -> Phase 2 cross-check" mandates 0.1% precision; 1% would
  hide O(%) integration-scheme errors that matter for CMB-level fits.)

Stub: populated once CLASS patch is applied.
"""
import os
import sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import quintessence as qn

TOL = 1e-3  # 0.1% max relative deviation


def run_phase1(V_family, beta, extra_params):
    """Run Phase 1 Python module."""
    E = qn.E_quintessence(V_family, beta, extra_params)
    if not E.ok:
        return None
    z_arr = np.linspace(0, 3.0, 61)
    return z_arr, np.array([E(z) for z in z_arr])


def run_class_sqmh(V_family, beta, extra_params):
    """
    Run CLASS-SQMH patched version.

    TODO: implement after CLASS patch is complete.
    Python side passes the canonical STRING ('mass'|'RP'|'exp'); the classy
    wrapper (or C input parser) translates to the integer enum in
    include/background.h via the _TO_CODE map in patch_template.py.

    Pseudo-code:
      from classy import Class
      cosmo = Class()
      cosmo.set({
          'SQMH_enabled': 1,
          'SQMH_V_family': V_family,  # canonical string
          'SQMH_xi': beta,
          'SQMH_V_params': extra_params,
          ...Planck baseline...
      })
      cosmo.compute()
      z_arr = np.linspace(0, 3.0, 61)
      E_arr = np.array([cosmo.Hubble(z) / cosmo.Hubble(0) for z in z_arr])
      return z_arr, E_arr
    """
    raise NotImplementedError("CLASS patch not yet applied")


def compare(V_family, beta, extra_params):
    r1 = run_phase1(V_family, beta, extra_params)
    if r1 is None:
        print(f"{V_family}: Phase 1 integration failed")
        return False

    try:
        r2 = run_class_sqmh(V_family, beta, extra_params)
    except NotImplementedError as e:
        print(f"{V_family}: CLASS stub ({e})")
        return None

    z1, E1 = r1
    z2, E2 = r2
    E2_interp = np.interp(z1, z2, E2)
    rel_err = np.abs(E1 - E2_interp) / E1
    max_err = float(np.max(rel_err))
    ok = max_err < TOL
    print(f"{V_family}: max|dE/E|={max_err:.3%} "
          f"{'PASS' if ok else 'FAIL'} (tol={TOL:.1%})")
    return ok


if __name__ == "__main__":
    print("Cross-validating Phase 1 (Python) vs Phase 2 (CLASS-SQMH)")
    print("=" * 60)
    # Best-fit points from desi_fitting.py Phase 1 run (see
    # figures/11_desi_dr2_fit.png.md). Update when results change.
    compare("RP", 0.352, (0.348,))
    compare("exp", 0.355, (0.345,))
    compare("mass", 0.0, ())  # LCDM-like sanity check
