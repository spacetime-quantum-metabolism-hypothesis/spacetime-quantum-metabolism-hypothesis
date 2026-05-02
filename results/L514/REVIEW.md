# L514 — paper/base.md §4 falsifier 통계 정정

**Date:** 2026-05-01
**Scope:** paper/base.md §4 (falsifiers) — apply L498 correlation-corrected statistics.
**Source of truth:** `results/L498/FALSIFIER_INDEPENDENCE.md`, `results/L498/l498_results.json`.

---

## 1. L498 핵심 수치 (정정 대상)

| Quantity | Naive (잘못) | L498 corrected (정답) |
|---|---|---|
| N_falsifiers | 6 (independent) | **6 pre-registered, N_eff = 4.44** (participation-ratio) |
| Combined Z (all 6) | 11.25σ | **8.87σ (ρ-corrected)** |
| Combined Z (active 5, drop SKA) | 12.32σ | **9.95σ (ρ-corrected)** |
| Cost of correlation correction | — | **−2.4σ in headline** |

**Correlated pairs:**
- Euclid × LSST = **0.80** (cosmic shear physics overlap)
- DESI × Euclid = **0.54** (BAO/RSD overlap at z<2)
- DESI × SKA = 0.32 (minor RSD overlap)

**3 load-bearing orthogonal channels:** **CMB-S4 / ET / SKA**. These three alone deliver Z_comb ≈ 10.83σ at full independence and carry the structural falsification weight; the cosmic-shear / BAO bloc (Euclid+LSST+DESI) collapses to ~2.7 effective channels.

---

## 2. base.md 수정 사항

### 2.1 line 618 (TL;DR self-audit bullet)
**Before:**
> 4. 22개 예측, 7개 near/mid-term falsifier — DESI DR3 가 가장 결정적

**After:**
> 4. 22개 예측, 6 pre-registered falsifiers (N_eff=4.44 after correlation correction; 8.87σ combined, ρ-corrected) — DESI DR3 가 가장 결정적; 3 load-bearing orthogonal channels = CMB-S4 / ET / SKA (§4.9, L498)

Rationale: "7개" was the simple sum of §4.3 (3) + §4.5 (4); the canonical pre-registered set per L498 is 6 (DESI / Euclid / CMB-S4 / ET / LSST / SKA-null). Replaced with the corrected count plus N_eff and ρ-corrected combined Z.

### 2.2 New subsection §4.9 — *Falsifier independence — correlation-corrected statistics (L498)*
Inserted between §4.8 (22 prediction summary) and §5 (cosmology implications).

Contents:
- Headline correction: N_eff=4.44; 8.87σ combined (all six, ρ-corrected); 9.95σ active five.
- Explicit prohibition of naive σ multiplication.
- Correlated-pair table (Euclid×LSST = 0.80, DESI×Euclid = 0.54, DESI×SKA = 0.32).
- Three load-bearing orthogonal channels named: **CMB-S4 / ET / SKA-null** (Z_comb ≈ 10.83σ at full independence).
- All N_eff estimators reported (participation 4.44 / Li–Ji 5.00 / Cheverud–Galwey 5.71 / naive 6.00) — participation-ratio adopted as headline (most conservative).
- Bonferroni / Holm passing status retained for the five active channels (LSST passes by ~2× margin only).
- Cross-references: §4.3, §4.5, §6.1 row 14, L406 / L485 / L486 / L487.

### 2.3 정정하지 않은 항목
- §4.3 (3개 near-term) and §4.5 (4개 mid-term) row counts left as-is. These describe the *time-window grouping* (DESI DR3 / PIXIE / LSST early; Euclid / CMB-S4 / ET / 21cm later); the L498 canonical set of 6 (DESI / Euclid / CMB-S4 / ET / LSST / SKA) is a *different* grouping. PIXIE is a near-term consistency channel not in L498's six; SKA is included in L498 as the structural null. Mixing the two would mis-state both. §4.9 explicitly anchors to the L498 canonical six and points back to §4.3 / §4.5 for the time-window view.
- §4.6 Euclid 4.4σ central forecast unchanged — it is a single-channel forecast (L406), independent of the multi-channel combination question L498 addresses.
- "5σ-class combined" / "11.25σ" / "N_eff=6" *verbatim* phrases were not present in base.md; the correction is purely *additive* (new §4.9) plus the line-618 wording fix. No deletion required.

---

## 3. 정직 한 줄

> The six pre-registered SQMH falsifiers compress to N_eff = 4.44 truly independent observable channels (participation-ratio); after Strube-1985 correlation correction the honest combined detection is **8.87σ (all six) / 9.95σ (active five)**, *not* the naive 11.25 / 12.32σ — the three load-bearing orthogonal tests are **CMB-S4, ET, and the SKA null**.

---

## 4. Artifacts

- `paper/base.md` — line 618 wording fix; new §4.9 inserted before §5.
- `results/L498/FALSIFIER_INDEPENDENCE.md` — source audit (unchanged).
- `results/L498/l498_results.json` — N_eff estimators, ρ matrix, Z_comb (unchanged).
