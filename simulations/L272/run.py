#!/usr/bin/env python3
"""L272 — Mock LCDM injection, BB false-detection rate."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L272"); OUT.mkdir(exist_ok=True, parents=True)

rng = np.random.default_rng(42)
N_MOCK = 200
N_GAL = 175
sigma_truth_universal = 9.0  # log
err = 0.10

false_detect = 0
delta_aiccs = []
for i in range(N_MOCK):
    # mock LCDM: all galaxies same sigma + noise
    obs = rng.normal(sigma_truth_universal, err, N_GAL)
    # universal model fit: 1 param
    mu_uni = obs.mean()
    chi2_uni = np.sum((obs - mu_uni)**2 / err**2)
    # BB 3-regime: split by tertile
    sorted_obs = np.sort(obs)
    t1, t2 = N_GAL//3, 2*N_GAL//3
    g1, g2, g3 = sorted_obs[:t1], sorted_obs[t1:t2], sorted_obs[t2:]
    chi2_bb = sum(np.sum((g - g.mean())**2 / err**2) for g in [g1,g2,g3])
    k_bb, k_uni = 3, 1
    aicc_bb = chi2_bb + 2*k_bb + 2*k_bb*(k_bb+1)/(N_GAL-k_bb-1)
    aicc_uni = chi2_uni + 2*k_uni + 2*k_uni*(k_uni+1)/(N_GAL-k_uni-1)
    d = aicc_uni - aicc_bb
    delta_aiccs.append(float(d))
    if d > 10: false_detect += 1

rate = false_detect/N_MOCK
print(f"  N_MOCK={N_MOCK}, false_rate={rate:.3f}")
print(f"  median ΔAICc={np.median(delta_aiccs):.2f}, max={np.max(delta_aiccs):.2f}")
verdict = f"BB false-detection rate on LCDM mock: {rate:.1%}. Threshold 5% — {'PASS' if rate<0.05 else 'FAIL'}."
print(verdict)
with open(OUT/'report.json','w') as f:
    json.dump(dict(N_mock=N_MOCK, false_rate=rate, median_dAICc=float(np.median(delta_aiccs)),
                   max_dAICc=float(np.max(delta_aiccs)), verdict=verdict), f, indent=2)
