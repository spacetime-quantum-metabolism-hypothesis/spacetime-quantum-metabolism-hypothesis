# SQMH Verification Reproducibility Image
# Build:  docker build -t sqmh-verify -f paper/verification/Dockerfile .
# Run:    docker run --rm -v "$PWD":/work -w /work/paper/verification sqmh-verify \
#             python verify_lambda_origin.py
#
# All five verify_*.py scripts are deterministic and should reproduce the
# numbers under paper/verification/expected_outputs/ exactly.

FROM python:3.11-slim-bookworm

# System packages required for numpy/scipy wheels and basic build hygiene
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        git \
    && rm -rf /var/lib/apt/lists/*

# Pin BLAS thread count to 1 — matches the project rule that worker
# processes never spawn nested threads (CLAUDE.md: 시뮬레이션 최우선 실행 원칙).
ENV OMP_NUM_THREADS=1 \
    MKL_NUM_THREADS=1 \
    OPENBLAS_NUM_THREADS=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /work

# Install Python deps first for layer caching
COPY paper/verification/requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

# Copy verification scripts (full repo can be bind-mounted at runtime)
COPY paper/verification /work/paper/verification

WORKDIR /work/paper/verification

# Default: print Python + library versions used for the published numbers
CMD ["python", "-c", "import sys, numpy, scipy; print('python', sys.version.split()[0]); print('numpy ', numpy.__version__); print('scipy ', scipy.__version__)"]
