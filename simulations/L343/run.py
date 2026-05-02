"""
L343 — RG cubic β-function FP topology scan.

목적
----
3-regime narrative (cosmic / cluster / galactic anchors) 가 RG fixed-point
구조에서 자연스럽게 나오는지 정량 평가.

대상 ansatz (가상 RG flow on a 1D coupling σ ≡ density-like coupling):

    β(σ) = a σ - b σ² + c σ³

이 cubic 은 일반적으로 최대 3개 root 를 가짐: σ=0 (trivial) + 두 비자명 root.
부호 조합 (a, b, c) 에 따라 root 의 안정성 (β'(σ*) 부호) 분포가:
  - 0 / saddle / stable  (또는 그 역)
  - 0 / stable / saddle
  - 모두 stable / 한쪽 complex
  ...

핵심 질문
---------
Q1. (a,b,c) 부호 조합이 만드는 FP 토폴로지 클래스는 몇 개인가?
Q2. σ_cluster 가 saddle FP 와 매핑될 수 있는 비율 (자연성 측정)?
Q3. 비단조 dip (cluster 영역의 mid-σ lump) 이 cubic FP 토폴로지의 기하적
    *필연*인가, 아니면 cubic 폭에 대한 자유 파라미터로 수동 조정한 결과인가?

방법론
------
- (a,b,c) 를 grid 에서 스캔.
- 각 점에서 β(σ) root 와 안정성 (β'(σ*)) 평가.
- 3개의 비자명 패턴 (S, U, Saddle) 분포를 분류.
- σ_cluster anchor 위치 (BAO ratio 단위로 mid 영역) 에 saddle 이 위치할 확률
  (a,b,c) 측정.
- "Saddle 이 cluster 에만 등장" vs "saddle 이 어느 σ 에든 등장 가능" 비교.

주의 (CLAUDE.md 최우선-1, -2)
---------------------------------
이 toy 는 *가상* β-function 의 위상 분류만 시연한다. SQT 미시 Lagrangian
유도가 아니다. (a,b,c) 의 물리적 의미는 **부여하지 않는다.** 결론은
"위상이 자연스러운가 / 부자연스러운가" 의 정성적 판정으로 한정.
"""

from __future__ import annotations
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import json
import numpy as np
from pathlib import Path

OUT = Path(__file__).resolve().parent
RES = Path(__file__).resolve().parents[2] / "results" / "L343"
RES.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Cubic β-function FP analysis
# ---------------------------------------------------------------------------

def fp_analysis(a: float, b: float, c: float):
    """Return list of (sigma_star, beta_prime, kind) for cubic β.

    kind:  'stable'  : β'(σ*) < 0
           'unstable': β'(σ*) > 0
           'marginal': |β'(σ*)| < tol
    """
    # roots of β(σ) = σ (a - b σ + c σ²) = 0
    roots = [0.0]
    if abs(c) > 1e-12:
        disc = b * b - 4.0 * c * a
        if disc >= 0:
            sq = np.sqrt(disc)
            roots.append((b + sq) / (2.0 * c))
            roots.append((b - sq) / (2.0 * c))
    elif abs(b) > 1e-12:
        roots.append(a / b)

    out = []
    for r in roots:
        # β'(σ) = a - 2 b σ + 3 c σ²
        bp = a - 2.0 * b * r + 3.0 * c * r * r
        if abs(bp) < 1e-9:
            kind = "marginal"
        elif bp < 0:
            kind = "stable"
        else:
            kind = "unstable"
        out.append((float(r), float(bp), kind))
    return out


def topology_signature(fps):
    """Return canonical signature for a set of fixed points.

    Sort by σ value, list (kind) tuple. Marginal -> 'm'.
    """
    s = sorted(fps, key=lambda x: x[0])
    code = []
    for r, bp, k in s:
        code.append(k[0])  # 's','u','m'
    return "".join(code), tuple((round(r, 4), k) for r, _, k in s)


# ---------------------------------------------------------------------------
# Grid scan
# ---------------------------------------------------------------------------

def run_scan(n_grid: int = 25, sigma_max: float = 5.0):
    """Scan (a,b,c) on signed grid; classify topology and saddle position."""
    rng = np.linspace(-1.0, 1.0, n_grid)
    rng_b = np.linspace(-2.0, 2.0, n_grid)

    classes: dict[str, int] = {}
    saddle_positions: list[float] = []   # σ of saddle (unstable) FP, when present
    stable_positions: list[float] = []
    cluster_band_hits = 0   # saddle FP in σ ∈ [0.8, 2.5] (toy "cluster" band)
    physical_count = 0      # cases with at least one σ* > 0 in [0, sigma_max]

    total = 0
    for a in rng:
        for b in rng_b:
            for c in rng:
                if abs(c) < 0.05:
                    continue  # keep cubic non-degenerate
                fps = fp_analysis(a, b, c)
                # physically interesting: at least one positive non-trivial FP in band
                pos = [(r, bp, k) for (r, bp, k) in fps
                       if 0.05 < r < sigma_max]
                if not pos:
                    continue
                physical_count += 1
                sig, _ = topology_signature(fps)
                classes[sig] = classes.get(sig, 0) + 1
                # collect saddle (unstable in 1D = "saddle" of RG flow direction)
                for r, bp, k in pos:
                    if k == "unstable":
                        saddle_positions.append(r)
                        if 0.8 <= r <= 2.5:
                            cluster_band_hits += 1
                    elif k == "stable":
                        stable_positions.append(r)
                total += 1

    return {
        "scan_grid": dict(n_grid=n_grid, sigma_max=sigma_max,
                          a_range=[float(rng.min()), float(rng.max())],
                          b_range=[float(rng_b.min()), float(rng_b.max())],
                          c_range=[float(rng.min()), float(rng.max())]),
        "total_evaluated": total,
        "physical_cases": physical_count,
        "topology_classes": classes,
        "saddle_count": len(saddle_positions),
        "stable_count": len(stable_positions),
        "saddle_in_cluster_band": cluster_band_hits,
        "saddle_naturalness_ratio": (cluster_band_hits / max(1, len(saddle_positions))),
        "saddle_pos_quartiles": [float(np.quantile(saddle_positions, q))
                                 for q in (0.25, 0.5, 0.75)] if saddle_positions else [],
        "stable_pos_quartiles": [float(np.quantile(stable_positions, q))
                                 for q in (0.25, 0.5, 0.75)] if stable_positions else [],
    }


# ---------------------------------------------------------------------------
# Non-monotonic dip geometry test
# ---------------------------------------------------------------------------

def dip_geometry_test(n_samples: int = 400, sigma_max: float = 5.0):
    """Among (a,b,c) configs with topology 0/saddle/stable (or 0/stable/saddle),
    measure whether g(σ) ≡ ∫β dσ produces a non-monotonic dip in cluster band."""
    rng = np.random.default_rng(42)
    dip_count = 0
    monotone_count = 0
    examples = []
    for _ in range(n_samples):
        a = rng.uniform(-1, 1)
        b = rng.uniform(-2, 2)
        c = rng.uniform(-1, 1)
        if abs(c) < 0.05:
            continue
        fps = fp_analysis(a, b, c)
        pos = [(r, bp, k) for (r, bp, k) in fps if 0.05 < r < sigma_max]
        if len(pos) < 2:
            continue
        kinds = sorted(k for _, _, k in pos)
        # interesting topology: one stable, one unstable (saddle)
        if not ("stable" in kinds and "unstable" in kinds):
            continue
        sig = np.linspace(0.0, sigma_max, 401)
        beta = a * sig - b * sig ** 2 + c * sig ** 3
        g = np.cumsum(beta) * (sig[1] - sig[0])
        # non-monotonic in cluster band [0.8, 2.5]?
        m = (sig >= 0.8) & (sig <= 2.5)
        gband = g[m]
        dgs = np.diff(gband)
        sign_changes = int(np.sum(np.diff(np.sign(dgs)) != 0))
        if sign_changes >= 1:
            dip_count += 1
            if len(examples) < 3:
                examples.append(dict(a=a, b=b, c=c, sign_changes=sign_changes))
        else:
            monotone_count += 1
    return {
        "n_topology_qualified": dip_count + monotone_count,
        "non_monotonic_dip_count": dip_count,
        "monotone_count": monotone_count,
        "dip_fraction": dip_count / max(1, dip_count + monotone_count),
        "examples": examples,
    }


# ---------------------------------------------------------------------------
def main():
    print("[L343] cubic β-function FP scan ...")
    scan = run_scan(n_grid=25)
    print("  total physical cases:", scan["physical_cases"])
    print("  topology classes:", scan["topology_classes"])
    print("  saddle naturalness in cluster band:",
          f"{scan['saddle_naturalness_ratio']:.3f}")

    print("[L343] non-monotonic dip geometry test ...")
    dip = dip_geometry_test(n_samples=2000)
    print("  dip fraction:", f"{dip['dip_fraction']:.3f}")

    out = dict(scan=scan, dip=dip)
    with open(RES / "scan_results.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("[L343] written:", RES / "scan_results.json")


if __name__ == "__main__":
    main()
