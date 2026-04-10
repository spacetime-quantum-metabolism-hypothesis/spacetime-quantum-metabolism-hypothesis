# -*- coding: utf-8 -*-
"""
run_mcmc_stub.py

Phase 3 MCMC entry point.
STUB: activates once Phase 2 CLASS patch is applied.
"""
import os
import sys


def check_prerequisites():
    """Verify Phase 2 artifacts exist before running MCMC."""
    class_path = os.path.join(os.path.dirname(__file__),
                              '..', 'class_patch', 'class_sqmh')
    if not os.path.isdir(class_path):
        return False, f"CLASS-SQMH not found at {class_path}. Run Phase 2 first."

    try:
        import cobaya  # noqa: F401
    except ImportError:
        return False, "Cobaya not installed. pip install cobaya getdist"

    return True, "OK"


def main():
    ok, msg = check_prerequisites()
    if not ok:
        print(f"[PREREQUISITE FAIL] {msg}")
        sys.exit(1)

    print("Prerequisites OK. Launching Cobaya MCMC...")
    print("  config: sqmh_planck_desi.yaml")
    print("  chains: 4")
    print("  target: R-1 < 0.05")
    print()
    os.system("cobaya-run sqmh_planck_desi.yaml --resume")


if __name__ == "__main__":
    main()
