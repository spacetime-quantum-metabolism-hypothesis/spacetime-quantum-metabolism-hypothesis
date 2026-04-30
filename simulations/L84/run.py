#!/usr/bin/env python3
"""L84 — Sakharov conditions vs SQT for baryogenesis."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L84"); OUT.mkdir(parents=True,exist_ok=True)

print("L84 — Sakharov conditions for baryogenesis from SQT")
sakharov = {
  "1. Baryon number violation":
     "SQT axioms a1-a6 silent on baryon number. Standard model preserves B at perturbative level. SQT Γ_0 creates 'spacetime quanta', not baryons. → SQT does NOT provide B violation directly.",
  "2. C and CP violation":
     "SQT axioms a1-a6 are CP-symmetric (real-valued, no chiral structure). L80 confirmed C, P preserved. → SQT does NOT provide CP violation.",
  "3. Out-of-equilibrium":
     "SQT Γ_0 cosmic creation is INHERENTLY non-equilibrium (energy non-conservation, L74 A4). → SQT NATURALLY satisfies Sakharov 3rd condition.",
}
for k, v in sakharov.items():
    print(f"\n  {k}:")
    print(f"    {v}")

print("\n  CONCLUSION: SQT provides Sakharov 3 (out-of-equilibrium) NATURALLY.")
print("              SQT does NOT provide Sakharov 1 (B violation) or 2 (CPV).")
print("              These must come from STANDARD MODEL extensions or coupling.")
print("              SQT is COMPLEMENTARY to baryogenesis, not the source.")

verdict = ("SQT satisfies Sakharov 3 (out-of-equilibrium via Γ_0). "
           "B-violation and CPV must come from SM extensions. "
           "SQT NEUTRAL on baryogenesis — neither helps nor hurts.")

fig, ax = plt.subplots(figsize=(10,6))
labels = list(sakharov.keys())
status = [0, 0, 1]   # only #3 satisfied
ax.barh([l[:30] for l in labels], status, color=['red','red','green'], alpha=0.7)
ax.set_xlim(0, 1.2)
ax.set_xlabel('SQT satisfies (1) or not (0)')
ax.set_title('L84 — SQT vs Sakharov conditions')
plt.tight_layout(); plt.savefig(OUT/'L84.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(sakharov=sakharov, verdict=verdict,
                   sqt_satisfies=[False, False, True]), f, indent=2)
print("L84 DONE")
