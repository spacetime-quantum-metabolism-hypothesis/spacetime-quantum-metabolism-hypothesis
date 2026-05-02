# L452 — Verification Reproducibility Artifacts

**Date:** 2026-05-01
**Scope:** `paper/verification/Dockerfile` + `paper/verification/conda_env.yml`
**Author:** L452 single-agent task

## Deliverables

| Path | Purpose |
|---|---|
| `paper/verification/Dockerfile` | Pinned `python:3.11-slim-bookworm` image, `numpy>=2.0`, `scipy>=1.10`, single-thread BLAS env, copies `paper/verification/`, default CMD prints versions. |
| `paper/verification/conda_env.yml` | `sqmh-verify` env, `python=3.11`, `numpy>=2.0`, `scipy>=1.10`, OpenBLAS pin, `OMP/MKL/OPENBLAS_NUM_THREADS=1` env vars, includes `requirements.txt` via pip block. |

## Design notes

- Both files import `paper/verification/requirements.txt` as the single source
  of truth for Python deps (currently `numpy>=2.0`, `scipy>=1.10`).
- Single-thread BLAS enforced in both environments — matches CLAUDE.md
  "워커당 스레드 고정" rule and guarantees deterministic floating-point
  reductions across hosts.
- `python:3.11-slim` chosen over 3.10 to match conda env and to satisfy
  "Python 3.10+" requirement; numpy 2.x wheels are first-class on 3.11.
- `verify_*.py` scripts in this repo are deterministic (no RNG, no MCMC,
  no parallelism), so `expected_outputs/` should be reproduced exactly
  given matching numpy/scipy minor versions; the env files pin the
  major/minor floor.
- conda env adds `libblas=*=*openblas` so Linux/macOS/Windows all use the
  same BLAS family — silences a known source of last-bit drift in
  `scipy.linalg` operations used by `verify_cosmic_shear.py`.
- Docker default CMD prints versions only; users invoke specific
  `verify_*.py` via `docker run ... python verify_<name>.py` per
  README.md instructions.

## Honest one-line

수식·이론 변경 없이 검증 환경 파일 2개와 본 리뷰만 생성했고 실제 빌드/실행 검증은 수행하지 않았다.
