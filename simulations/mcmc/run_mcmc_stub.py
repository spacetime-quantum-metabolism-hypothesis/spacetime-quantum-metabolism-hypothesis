# -*- coding: utf-8 -*-
"""
run_mcmc_stub.py

Phase 3 MCMC entry point.
STUB: activates once Phase 2 CLASS patch is applied.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CLASS_DIR = os.path.abspath(os.path.join(HERE, '..', 'class_patch', 'class_sqmh'))
YAML = os.path.join(HERE, 'sqmh_planck_desi.yaml')


def check_prerequisites():
    """Verify Phase 2 artifacts + Python deps exist before running MCMC."""
    if not os.path.isdir(CLASS_DIR):
        return False, f"CLASS-SQMH not found at {CLASS_DIR}. Run Phase 2 first."

    try:
        import cobaya  # noqa: F401
    except ImportError:
        return False, "Cobaya not installed. pip install cobaya getdist"

    try:
        import clik  # noqa: F401  (Planck 2018 likelihood C library)
    except ImportError:
        return False, ("clik (Planck 2018 likelihood) not importable. "
                       "Install from https://github.com/benabed/clik and set "
                       "CLIK_PATH / LD_LIBRARY_PATH.")

    try:
        import classy  # noqa: F401
    except ImportError:
        return False, ("classy not importable. Build CLASS-SQMH Python "
                       f"binding: cd {CLASS_DIR} && make classy")

    if not os.path.exists(YAML):
        return False, f"Missing yaml config: {YAML}"

    return True, "OK"


def main():
    ok, msg = check_prerequisites()
    if not ok:
        print(f"[PREREQUISITE FAIL] {msg}")
        sys.exit(1)

    n_chains = int(os.environ.get('SQMH_NCHAINS', '4'))
    print("Prerequisites OK. Launching Cobaya MCMC...")
    print(f"  config : {YAML}")
    print(f"  chains : {n_chains}")
    print("  target : R-1 < 0.05")
    print(f"  cwd    : {HERE}")
    print()

    # Run from the yaml's own directory so relative `path: ../class_patch/...`
    # resolves correctly.
    rc = subprocess.call(
        ['cobaya-run', os.path.basename(YAML),
         '-r', str(n_chains), '--resume'],
        cwd=HERE,
    )
    sys.exit(rc)


if __name__ == "__main__":
    main()
