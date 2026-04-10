---
name: bigwork-paper
description: SQMH 가설 GitHub 논문 레포 + Python 수치 증명 + DESI DR3 예측
trigger: "/bigwork-paper", "SQMH 논문", "논문 작업"
---

# SQMH Paper Project

SQMH (Spacetime Quantum Metabolism Hypothesis) 논문 프로젝트.
`base.md` → GitHub repo (English paper + Python simulations + DESI prediction).

## Quick Start
1. Read current state: `refs/meta.json`, `refs/test-plan.md`
2. Identify next incomplete checkpoint
3. Execute via generator agent → verify via evaluator
4. Measure KPIs (`refs/define.md`) → record in `refs/adjust.md`

## Key Files
| File | Purpose |
|------|---------|
| `base.md` | Source hypothesis (Korean) |
| `refs/intent.md` | Decisions log |
| `refs/define.md` | KPIs: 7 sims, repo completeness, publication readiness |
| `refs/spec.md` | Repo structure + rules |
| `refs/test-plan.md` | 5 checkpoints with verification criteria |

## Deliverables (Priority Order)
1. **DESI DR3 prediction** — w(z) inflection + no phantom crossing
2. **7 Python simulations** — standalone, reproducible, zero free params
3. **English paper sections** — 9 markdown files in `paper/`
4. **README.md** — clone → install → run → all figures reproduced

## Hard Constraints
- Zero free parameters (σ=4πG from G, Γ₀ from H₀/Ωₘ/ΩΛ)
- All constants centralized in `simulations/config.py`
- Honest about limitations (base.md §10.4, §XVI, §XVII)
