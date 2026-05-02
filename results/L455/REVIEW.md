# L455 — verification harness deliverables

Date: 2026-05-01
Scope: TROUBLESHOOTING.md + compare_outputs.py for paper/verification/

## Deliverables produced

- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/paper/verification/TROUBLESHOOTING.md`
  - 6 sections: install/env, version mismatch, OS-specific (Windows
    cp949, macOS Apple Silicon, Linux headless), perf/threads,
    compare_outputs mismatch, last-resort.
  - Cross-references existing CLAUDE.md re-occurrence rules
    (numpy 2.x trapezoid, cp949 unicode, OMP threading,
    matplotlib backend ordering, python vs python3).

- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/paper/verification/compare_outputs.py`
  - Runs every `verify_*.py`, parses stdout, diffs vs
    `expected_outputs/<name>.json` numeric fields.
  - Default tolerance +/- 5 % (configurable via `--tol`).
  - Handles: percent-form unit drift (fraction <-> %), exact-zero
    expected, string verdicts (e.g. "PASS"), metadata-only fields
    (n_mock, n_gal, seed) that never appear in stdout.
  - Forces single-threaded BLAS + UTF-8 IO for reproducibility.
  - Exit codes: 0 PASS, 1 numeric FAIL, 2 run-error.

## Self-test result (this machine, Python 3.x, numpy/scipy installed)

```
[verify_cosmic_shear.py]          OK
[verify_lambda_origin.py]         OK
[verify_milgrom_a0.py]            OK
[verify_mock_false_detection.py]  OK (3 metadata-only fields flagged)
[verify_monotonic_rejection.py]   OK
[verify_Q_parameter.py]           SKIP (no expected JSON)
[verify_S8_forecast.py]           SKIP (no expected JSON)
RESULT: PASS
```

## Honest one-liner

compare_outputs.py achieves PASS for the 5 paper-canonical scripts
within +/- 5 %; n_mock/n_gal/seed are correctly flagged as
metadata-only, but the matcher relies on numeric proximity rather
than label semantics, so a future stdout reformat that changes a
printed value into a different decade could be silently swallowed
by the percent-form fallback.

## Open items not addressed (out of L455 scope)

- `verify_Q_parameter.py` and `verify_S8_forecast.py` have no
  `expected_outputs/*.json`; harness skips them. Adding those JSONs
  is a separate task.
- No CI workflow added (`.github/workflows/verify.yml` still TODO
  per README).
- TROUBLESHOOTING.md is reviewer-facing English only; no Korean
  parallel.
