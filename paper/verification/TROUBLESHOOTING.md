# SQMH Verification — TROUBLESHOOTING

Common issues encountered when reproducing the five `verify_*.py`
scripts in `paper/verification/` on a fresh machine. If your symptom is
not listed, run `python compare_outputs.py` and attach the diff to the
issue tracker.

---

## 0. Quick triage flowchart

```
script fails to import           -> Section 1 (install / env)
script runs, but numbers differ  -> Section 2 (version mismatch)
script prints garbled characters -> Section 3 (encoding / OS)
script hangs / very slow         -> Section 4 (BLAS / threads)
compare_outputs.py mismatch      -> Section 5 (tolerance / seed)
```

---

## 1. Install / environment

### 1.1 `ModuleNotFoundError: No module named 'numpy'`

```bash
pip install -r requirements.txt
```

Use the same Python interpreter you will run the scripts with.
Verify with:

```bash
which python         # macOS / Linux
where python         # Windows
python -c "import numpy, scipy; print(numpy.__version__, scipy.__version__)"
```

### 1.2 `pip` installs into the wrong Python

Symptom: `pip install` succeeds, but `python verify_*.py` still raises
`ModuleNotFoundError`.

Fix: invoke `pip` through the target interpreter explicitly.

```bash
python -m pip install -r requirements.txt
```

On macOS systems where the default `python` command does not exist
(common on Apple Silicon), use `python3` everywhere — including in
shell scripts. (Recorded in `CLAUDE.md` re-occurrence rule.)

### 1.3 `pip install` fails behind a corporate proxy

```
WARNING: Retrying ... after connection broken
```

Set `HTTPS_PROXY` / `HTTP_PROXY` or use an offline wheelhouse:

```bash
pip install --no-index --find-links /path/to/wheels -r requirements.txt
```

### 1.4 Virtual-env recommended

To isolate from system numpy / scipy:

```bash
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
.venv\Scripts\activate             # Windows (cmd)
.venv\Scripts\Activate.ps1         # Windows (PowerShell)
pip install -r requirements.txt
```

---

## 2. Version mismatch

### 2.1 `AttributeError: module 'numpy' has no attribute 'trapezoid'`

You have numpy < 2.0. The scripts use the numpy 2.x name.

```bash
python -c "import numpy; print(numpy.__version__)"
```

If `< 2.0`, upgrade:

```bash
pip install --upgrade "numpy>=2.0"
```

Note: a bare `from numpy import trapz` does **not** work as a
fallback — call `np.trapezoid` directly. (CLAUDE.md rule.)

### 2.2 `AttributeError: module 'numpy' has no attribute 'float_'` / `bool_`

Some downstream tools (emcee, older corner) emit `np.float_` /
`np.bool_`, which were removed in numpy 2.x. The five core
`verify_*.py` scripts do **not** depend on these, but a stale
notebook or extra plot helper may. Pin numpy < 2 in that helper, or
shim:

```python
import numpy as np
if not hasattr(np, 'float_'): np.float_ = np.float64
if not hasattr(np, 'bool_'):  np.bool_  = np.bool_ if hasattr(np, 'bool_') else bool
```

### 2.3 scipy < 1.10 — `ImportError: cannot import name 'cumulative_trapezoid'`

```bash
pip install --upgrade "scipy>=1.10"
```

### 2.4 Python < 3.10

`match` / `|`-typed unions are not used in the verify scripts, but
some optional dependencies of the broader project require 3.10+.
Tested on 3.11 and 3.13.

---

## 3. OS-specific

### 3.1 Windows: `UnicodeEncodeError: 'cp949' codec ... 'µ'`

The paper's broader codebase has had a recurring class of
`cp949` failures from non-ASCII characters in `print(...)` (for
example `ν`, `µ`, `³`). The five verify scripts in
this folder use ASCII-only stdout, so they should not hit this. If
you do hit it (e.g. after editing a script), force UTF-8:

```bash
set PYTHONIOENCODING=utf-8       # cmd
$env:PYTHONIOENCODING = "utf-8"  # PowerShell
chcp 65001                       # console code page -> UTF-8
```

The `cp949` failure mode is recorded in `CLAUDE.md`:
*matplotlib labels can carry unicode; `print()` must stay ASCII*.

### 3.2 macOS Apple Silicon: `python` not found

Use `python3` (and `pip3`) everywhere, or alias in `~/.zshrc`:

```bash
alias python=python3
alias pip='python3 -m pip'
```

### 3.3 macOS: scipy wheel install fails (Accelerate / OpenBLAS clash)

```bash
pip install --upgrade pip setuptools wheel
pip install --no-cache-dir --force-reinstall "scipy>=1.10"
```

If still failing, install via conda-forge:

```bash
conda install -c conda-forge "numpy>=2" "scipy>=1.10"
```

### 3.4 Windows: silent OpenMP death

Symptom: `verify_*.py` exits with code 0 but produces no output
(rare; mostly a hazard for the heavier MCMC scripts elsewhere in
the project). Force single-threaded BLAS:

```bash
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
```

(Same workaround codified in `CLAUDE.md` for L4 emcee runs.)

### 3.5 Linux: no display, matplotlib import error

The five verify scripts do **not** import matplotlib. If you have
added a plotting helper, set the backend **before** any
matplotlib-using import:

```python
import matplotlib
matplotlib.use('Agg')   # MUST be before `import corner` etc.
import matplotlib.pyplot as plt
```

---

## 4. Performance / threads

All five scripts run in `< 1 minute` on a laptop. If a script
appears to hang:

1. The slowest is `verify_mock_false_detection.py` (~1 min, 200
   mock LCDM rotation curves x 175 galaxies).
2. Set `OMP/MKL/OPENBLAS_NUM_THREADS=1` (Section 3.4) — over-
   subscription on cloud VMs can be pathologically slow.
3. Confirm you are not running under a debugger / profiler.

---

## 5. `compare_outputs.py` mismatch

### 5.1 Numeric drift > 5 %

The default tolerance is **+/- 5 %** on every numeric field in
`expected_outputs/*.json`. If `compare_outputs.py` reports a
mismatch larger than that:

- Check numpy / scipy versions (Section 2). Float-summation order
  changes in numpy 2.x have produced sub-percent drifts on some
  platforms; the 5 % band absorbs these.
- The `verify_lambda_origin.py` ratio is **exact** (analytic
  identity), so any drift > 1e-6 indicates a code change, not a
  float-precision issue.
- For `verify_mock_false_detection.py`, ensure the script's
  internal `np.random.default_rng(42)` is intact. Different seeds
  legitimately move the rate by a few percent.

### 5.2 stdout line mismatch

`compare_outputs.py` only diffs JSON numeric fields, not stdout
text. If you want stdout-level diffing, redirect and `diff` by
hand:

```bash
python verify_lambda_origin.py > out.txt
diff out.txt expected_lambda_origin.stdout
```

The `expected_outputs/*.json` files include a `stdout_lines` array
for reference but it is not enforced.

### 5.3 "verdict": PASS vs FAIL flip

Only `verify_milgrom_a0.py` emits a verdict. If it flips to FAIL,
the deviation has exceeded `2 sigma`. The expected sigma is
~0.71 — a flip indicates either a code edit or a major numpy
ABI change. Investigate before accepting.

---

## 6. When all else fails

1. `git status` — ensure no uncommitted edits to the `verify_*.py`
   scripts.
2. `git log --oneline paper/verification/` — confirm you are on
   the published verification commit.
3. Re-run in a clean venv (Section 1.4).
4. Capture `python --version`, `pip freeze`, OS, and the output of
   `python compare_outputs.py` in your bug report.

The five scripts are **deliberately minimal** (numpy + scipy
only, < 200 lines each). If reproduction fails after the steps
above, the most likely cause is a numpy / scipy ABI change we
have not yet pinned — please file an issue with the version
triple and the `compare_outputs.py` diff.
