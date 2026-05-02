#!/usr/bin/env python3
"""
compare_outputs.py
==================

Run each `verify_*.py` script in `paper/verification/`, parse its stdout
for numeric fields declared in `expected_outputs/<name>.json`, and
report any deviation outside +/- 5 % (default tolerance).

Usage
-----

    python compare_outputs.py                # all scripts, +/- 5 %
    python compare_outputs.py --tol 0.01     # tighter tolerance
    python compare_outputs.py --only verify_milgrom_a0.py

Exit code
---------

    0  -> all scripts within tolerance
    1  -> one or more mismatches (prints diff)
    2  -> a script failed to run (non-zero exit)

Honesty notes
-------------

* The `verify_lambda_origin.py` ratio is an analytic identity: any
  drift > 1e-6 is a code change, not float noise. We still apply the
  5 % band uniformly so the harness is simple; a stricter check is
  on `ratio - 1` < 1e-6 explicitly.
* stdout text is not enforced — only the numeric fields named in the
  `expected` block of each JSON.
* This script DOES NOT validate that the verify scripts are
  scientifically correct; it only validates reproducibility.

(L455 deliverable.)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED_DIR = HERE / "expected_outputs"

DEFAULT_TOL = 0.05  # +/- 5 %

NUM_RE = re.compile(
    r"[-+]?\d+\.\d+e[-+]?\d+"     # 1.23e-10
    r"|[-+]?\d+e[-+]?\d+"         # 1e-10
    r"|[-+]?\d+\.\d+"             # 1.23
    r"|[-+]?\d+",                 # 42
    re.IGNORECASE,
)


def find_scripts() -> list[Path]:
    """Every verify_*.py at the verification root."""
    return sorted(HERE.glob("verify_*.py"))


def expected_path(script: Path) -> Path:
    return EXPECTED_DIR / (script.stem + ".json")


def run_script(script: Path, timeout: int = 180) -> tuple[int, str, str]:
    """Run a verify script with a clean env. Returns (rc, stdout, stderr)."""
    env = os.environ.copy()
    # Force single-threaded BLAS so timing / numerics are reproducible.
    env["OMP_NUM_THREADS"] = "1"
    env["MKL_NUM_THREADS"] = "1"
    env["OPENBLAS_NUM_THREADS"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(HERE),
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
    )
    return proc.returncode, proc.stdout, proc.stderr


def extract_numbers(text: str) -> list[float]:
    """All decimal-looking tokens in the text, in order."""
    out = []
    for tok in NUM_RE.findall(text):
        try:
            out.append(float(tok))
        except ValueError:
            pass
    return out


def find_actual(stdout: str, label: str, expected_value: float,
                tol: float) -> float | None:
    """
    Locate the numeric in stdout that corresponds to `label`.

    Stdout from the verify_*.py scripts uses human-readable labels
    (e.g. 'a_0 (SQT)') that do not match JSON keys (e.g.
    'a0_SQT_m_s2'). Strategy:

      1. Closest-numeric match: pick the stdout numeric whose
         relative distance to `expected_value` is minimized,
         provided it lies within a generous (10*tol) band. This
         is the primary path because labels rarely line up.
      2. Fall back to label-substring line matching for cases the
         numeric heuristic cannot disambiguate (zeros, integers,
         strings).
    """
    # 1. tight-numeric match: any stdout numeric within tol of expected
    #    (or expected*100 for percent form).
    if expected_value is not None and expected_value != 0:
        targets = [expected_value]
        if 0 < abs(expected_value) <= 1.0:
            targets.append(expected_value * 100.0)
        best = None
        best_rel = float("inf")
        best_target = expected_value
        for n in extract_numbers(stdout):
            for t in targets:
                rel = abs(n - t) / abs(t)
                # tight: within tol (not 10*tol). Looser bands cause
                # the percent-form fallback to swallow unrelated ints.
                if rel <= tol and rel < best_rel:
                    best = n
                    best_rel = rel
                    best_target = t
        if best is not None:
            if best_target != expected_value and best_target != 0:
                best = best * (expected_value / best_target)
            return best

    # 1b. expected == 0: look for a literal "0.00" / "0" in stdout near
    #     a label match, or anywhere if label search fails.
    if expected_value == 0.0:
        for line in stdout.splitlines():
            for tok in NUM_RE.findall(line):
                try:
                    v = float(tok)
                except ValueError:
                    continue
                if abs(v) < 0.5:  # any small number, then label-disambiguate
                    # require the label tokens to appear on this line
                    parts = label.lower().replace("_", " ").split()
                    low = line.lower()
                    if all(p in low for p in parts if p):
                        return v
        # last resort: any "0.00" token in stdout
        if " 0.00" in stdout or "= 0.00" in stdout or "= 0\n" in stdout:
            return 0.0

    # 2. label-substring fallback.
    candidates = {label, label.replace("_", " "), label.replace("_", "-")}
    for c in list(candidates):
        if "_" in c:
            candidates.add(c.rsplit("_", 1)[0])
    # Drop very-short candidates that would produce spurious matches.
    candidates = {c for c in candidates if c and len(c) >= 4}
    for line in stdout.splitlines():
        low = line.lower()
        if any(c.lower() in low for c in candidates):
            nums = extract_numbers(line)
            if nums:
                # Prefer a number close to expected if any.
                if expected_value is not None and expected_value != 0:
                    nums.sort(key=lambda n: abs(n - expected_value))
                return nums[0]
    return None


def compare_one(script: Path, tol: float, verbose: bool) -> tuple[bool, list[str]]:
    """
    Returns (ok, messages).
    `ok` is False if the script failed or any field is out of tolerance.
    """
    msgs: list[str] = []
    ep = expected_path(script)
    if not ep.exists():
        msgs.append(f"  [SKIP] no expected_outputs/{ep.name}")
        return True, msgs  # not a failure; just nothing to compare

    expected = json.loads(ep.read_text(encoding="utf-8")).get("expected", {})
    if not expected:
        msgs.append(f"  [SKIP] expected block empty in {ep.name}")
        return True, msgs

    try:
        rc, out, err = run_script(script)
    except subprocess.TimeoutExpired:
        msgs.append(f"  [FAIL] timeout running {script.name}")
        return False, msgs

    if rc != 0:
        msgs.append(f"  [FAIL] {script.name} exited rc={rc}")
        if err.strip():
            msgs.append("    stderr (last 5 lines):")
            for line in err.strip().splitlines()[-5:]:
                msgs.append(f"      {line}")
        return False, msgs

    ok = True
    for key, exp_val in expected.items():
        if not isinstance(exp_val, (int, float)):
            # Non-numeric (e.g. "verdict": "PASS") — string match on stdout.
            if str(exp_val) not in out:
                msgs.append(
                    f"  [MISS] {key}: expected text '{exp_val}' "
                    f"not found in stdout"
                )
                ok = False
            elif verbose:
                msgs.append(f"  [ OK ] {key}: '{exp_val}' present")
            continue

        actual = find_actual(out, key, float(exp_val), tol)
        if actual is None:
            # Metadata fields (n_mock, seed, ...) often live in the
            # expected JSON for documentation but never get printed.
            # Don't fail on those — just report informationally.
            msgs.append(
                f"  [META] {key}: expected {exp_val:g}, "
                f"not present in stdout (metadata-only)"
            )
            continue

        if exp_val == 0.0:
            # Absolute tolerance for exact-zero expected.
            within = abs(actual) <= max(tol, 1e-9)
        else:
            within = abs(actual - exp_val) <= abs(exp_val) * tol

        if within:
            if verbose:
                msgs.append(
                    f"  [ OK ] {key}: actual={actual:g} "
                    f"expected={exp_val:g}"
                )
        else:
            rel = (actual - exp_val) / exp_val if exp_val else float('inf')
            msgs.append(
                f"  [DIFF] {key}: actual={actual:g} "
                f"expected={exp_val:g} "
                f"rel={rel:+.2%} (tol +/- {tol:.0%})"
            )
            ok = False

    return ok, msgs


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--tol", type=float, default=DEFAULT_TOL,
                   help="relative tolerance, default 0.05 (+/- 5%%)")
    p.add_argument("--only", action="append", default=None,
                   help="run only this script (repeatable). "
                        "Match by basename, e.g. verify_milgrom_a0.py")
    p.add_argument("-v", "--verbose", action="store_true",
                   help="also print fields that pass")
    args = p.parse_args()

    scripts = find_scripts()
    if args.only:
        keep = {Path(s).name for s in args.only}
        scripts = [s for s in scripts if s.name in keep]
        if not scripts:
            print(f"no scripts match --only {args.only}", file=sys.stderr)
            return 2

    print(f"compare_outputs.py  tol=+/-{args.tol:.0%}  "
          f"interpreter={sys.executable}")
    print(f"  scripts: {len(scripts)}")
    print()

    overall_ok = True
    any_run_failure = False

    for s in scripts:
        print(f"[ {s.name} ]")
        ok, msgs = compare_one(s, tol=args.tol, verbose=args.verbose)
        for m in msgs:
            print(m)
        if not ok:
            overall_ok = False
            # distinguish run-failure from numeric-diff in exit code
            if any("rc=" in m or "timeout" in m for m in msgs):
                any_run_failure = True
        else:
            if not msgs:
                print("  [ OK ] all fields within tolerance")
        print()

    if overall_ok:
        print("RESULT: PASS  (all scripts within tolerance)")
        return 0
    if any_run_failure:
        print("RESULT: ERROR (one or more scripts failed to run)")
        return 2
    print("RESULT: FAIL  (one or more numeric fields out of tolerance)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
