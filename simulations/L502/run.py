#!/usr/bin/env python3
"""
L502 — Hidden DOF AICc Penalty Quantification.

Per L495 hidden DOF audit (results/L495/HIDDEN_DOF_AUDIT.md):
  Conservative count: k_hidden = 9
    +1 functional form (M16 / simple-nu / standard-mu / Bekenstein)
    +3 anchor pick (cosmic 8.37 / cluster 7.75 / galactic 9.56)
    +1 Y_star (SPARC canonical Y_disk=0.5, Y_bul=0.7)
    +1 B1 bilinear ansatz
    +2 sigma_0(env) three-regime structure (carrier + saddle position)
    +1 axiom-scale stipulation (eta_Z2, Lambda_UV, dark-only embedding)
  Expanded count: k_hidden = 13 (each axiom-scale fully unpacked).

For each PASS candidate we compute:
  AICc_naive    = chi2_min + 2 k_naive   + 2 k(k+1)/(N-k-1)
  AICc_honest   = chi2_min + 2 (k_naive + k_hidden) + ...
  delta         = AICc_honest - AICc_naive
  delta_vs_LCDM = AICc_honest_SQT - AICc_LCDM_baseline

Falsifies the "0 free parameter" advertisement on a per-claim basis.

CLAUDE.md compliance:
- 0 new physics formulae (only AICc bookkeeping).
- No theory derivation.
- Honest disclosure of penalty against L482 advertised dAICc=+0.70.
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = ROOT / "results" / "L502"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def aicc(chi2: float, k: int, n: int) -> float:
    """Standard AICc with safe fallback to AIC when n-k-1 <= 0.

    For the substantive PASS_STRONG bound-checks (Newton, BBN, Cassini, EP)
    the channel is N=1 (single inequality satisfied), so AICc small-sample
    correction diverges and we fall back to plain AIC = chi^2 + 2k.  This is
    the correct behaviour: the *capacity* penalty (2k) is the only meaningful
    information criterion at N=1, and it matches the user's request
    (e.g. dAIC = +9*2 = +18 for the conservative full-stack penalty).
    """
    denom = n - k - 1
    if denom <= 0:
        # Fall back to AIC (no small-sample correction); honest at N=1.
        return chi2 + 2.0 * k
    return chi2 + 2.0 * k + (2.0 * k * (k + 1)) / denom


# Hidden DOF breakdown (conservative; see L495)
HIDDEN_DOF_BREAKDOWN = {
    "functional_form": 1,   # M16 / simple-nu / standard-mu / Bekenstein
    "anchor_picks": 3,      # cosmic 8.37 / cluster 7.75 / galactic 9.56
    "Upsilon_star": 1,      # SPARC canonical Y_disk/Y_bul
    "B1_bilinear": 1,       # R = sigma * n * rho_m ansatz
    "three_regime": 2,      # carrier shape + saddle position
    "axiom_scales": 1,      # eta_Z2, Lambda_UV, dark-only (collapsed)
}
K_HIDDEN_CONSERVATIVE = sum(HIDDEN_DOF_BREAKDOWN.values())  # = 9
K_HIDDEN_EXPANDED = K_HIDDEN_CONSERVATIVE + 4  # axiom_scales fully unpacked = 13


@dataclass
class Candidate:
    """A PASS_STRONG / PASS_MODERATE candidate with audit-relevant numbers."""
    claim_id: str
    label: str
    advertised_status: str          # PASS_STRONG / PASS_MODERATE / etc.
    chi2_sqt: float                 # SQT-locked chi^2 against the channel data
    chi2_lcdm_or_free: float        # baseline chi^2 (free fit or LCDM/Newton/MOND-free)
    n_data: int                     # number of independent data points
    k_naive: int                    # advertised free parameters (usually 0)
    k_baseline: int                 # baseline model's free parameters
    # Subset of hidden DOF that materially apply to *this* candidate.
    hidden_dof_subset: dict
    notes: str

    @property
    def k_hidden_applicable(self) -> int:
        return sum(self.hidden_dof_subset.values())

    def aicc_table(self) -> dict:
        n = self.n_data
        # Naive (paper advertisement)
        aicc_sqt_naive = aicc(self.chi2_sqt, self.k_naive, n)
        aicc_base_naive = aicc(self.chi2_lcdm_or_free, self.k_baseline, n)
        d_naive = aicc_sqt_naive - aicc_base_naive

        # Honest: conservative
        k_sqt_h = self.k_naive + self.k_hidden_applicable
        aicc_sqt_honest = aicc(self.chi2_sqt, k_sqt_h, n)
        d_honest = aicc_sqt_honest - aicc_base_naive

        # Honest: expanded (axiom_scales unpacked when applicable)
        # Only inflate if axiom_scales is in the subset.
        expand_extra = 4 if self.hidden_dof_subset.get("axiom_scales", 0) > 0 else 0
        k_sqt_e = self.k_naive + self.k_hidden_applicable + expand_extra
        aicc_sqt_expanded = aicc(self.chi2_sqt, k_sqt_e, n)
        d_expanded = aicc_sqt_expanded - aicc_base_naive

        # Worst-case: apply the *full* k_hidden = 9 (conservative) regardless
        # of which subset materially applies.  This implements the user's
        # specific test "L482 RAR dAICc=+0.70 -> +9*2 = +18 -> LCDM wins?".
        k_sqt_full = self.k_naive + K_HIDDEN_CONSERVATIVE
        aicc_sqt_full = aicc(self.chi2_sqt, k_sqt_full, n)
        d_full = aicc_sqt_full - aicc_base_naive

        return {
            "aicc_sqt_naive": aicc_sqt_naive,
            "aicc_baseline_naive": aicc_base_naive,
            "delta_aicc_naive": d_naive,
            "k_sqt_honest_conservative": k_sqt_h,
            "aicc_sqt_honest_conservative": aicc_sqt_honest,
            "delta_aicc_honest_conservative": d_honest,
            "k_sqt_honest_expanded": k_sqt_e,
            "aicc_sqt_honest_expanded": aicc_sqt_expanded,
            "delta_aicc_honest_expanded": d_expanded,
            "k_sqt_full_kh9": k_sqt_full,
            "aicc_sqt_full_kh9": aicc_sqt_full,
            "delta_aicc_full_kh9": d_full,
        }


# -----------------------------------------------------------------------------
# PASS candidates.  Numbers sourced from:
#   - results/L482/L482_results.json    (RAR a0)
#   - paper/base.md self-audit row 1.2.2 + 4.1                    (other 4)
#   - results/L495/HIDDEN_DOF_AUDIT.md                            (subset map)
# For substantive PASS_STRONG (Newton/BBN/Cassini/EP) the underlying chi^2
# is not a fitted-data chi^2 but a single-point consistency check against an
# upper bound.  We treat them as 1 data point each with chi2=0 (ad hoc null
# bound) and the AICc penalty becomes a *capacity* penalty: 2*k_hidden alone.
# This matches the L495 convention "axiom-scale stipulation = +1 hidden DOF".
# -----------------------------------------------------------------------------
CANDIDATES = [
    # === The single global-peak candidate (L482) ===
    Candidate(
        claim_id="rar_a0_l482",
        label="L482 SPARC RAR (a0 = c H0 / 2pi)",
        advertised_status="PASS_STRONG (candidate, 5/5 K)",
        chi2_sqt=4387.168577979597,            # SQT-locked Planck H0
        chi2_lcdm_or_free=4384.4642839662665,  # 1-param free fit
        n_data=3389,                           # 175 galaxies x ~19.4 radii
        k_naive=0,
        k_baseline=1,
        hidden_dof_subset={
            "functional_form": 1,   # M16 carrier choice
            "Upsilon_star": 1,      # SPARC Y_disk/Y_bul convention
            "B1_bilinear": 0,       # not applicable to RAR channel
            "anchor_picks": 0,      # only galactic anchor used here
            "three_regime": 0,      # RAR is single-regime
            "axiom_scales": 0,
        },
        notes="L482 advertised dAICc(SQT-free) = +0.70; honest penalty inflates this.",
    ),

    # === Substantive PASS_STRONG 4 (paper §6.5(e); base.md row 1045) ===
    Candidate(
        claim_id="newton_recovery",
        label="Newton 1/r^2 recovery (derived 1)",
        advertised_status="PASS_STRONG (substantive)",
        chi2_sqt=0.0,           # consistency check vs Planck-scale derivation
        chi2_lcdm_or_free=0.0,  # Newton itself is the baseline -> tautology
        n_data=1,
        k_naive=0,
        k_baseline=0,
        hidden_dof_subset={
            "B1_bilinear": 1,    # R = sigma n rho_m ansatz (paper §2.2.1)
            "axiom_scales": 1,   # dimensional reduction channel pick
        },
        notes="N=1 consistency-check; AICc_honest = 2*k_hidden = capacity penalty only.",
    ),
    Candidate(
        claim_id="bbn_dN_eff",
        label="BBN Delta N_eff < 0.17",
        advertised_status="PASS_STRONG (substantive)",
        chi2_sqt=0.0,
        chi2_lcdm_or_free=0.0,
        n_data=1,
        k_naive=0,
        k_baseline=0,
        hidden_dof_subset={
            "axiom_scales": 1,    # eta_Z2 ~ 10 MeV stipulation
        },
        notes="Single-bound consistency check. eta_Z2 scale is not derived.",
    ),
    Candidate(
        claim_id="cassini_ppn",
        label="Cassini |gamma-1| < 2.3e-5",
        advertised_status="PASS_STRONG (substantive)",
        chi2_sqt=0.0,
        chi2_lcdm_or_free=0.0,
        n_data=1,
        k_naive=0,
        k_baseline=0,
        hidden_dof_subset={
            "axiom_scales": 1,    # Lambda_UV / M_Pl stipulation
        },
        notes="beta_eff = Lambda_UV/M_Pl chosen ~Planck order; not derived.",
    ),
    Candidate(
        claim_id="ep_eta",
        label="EP |eta| < 1e-15 (MICROSCOPE)",
        advertised_status="PASS_STRONG (substantive)",
        chi2_sqt=0.0,
        chi2_lcdm_or_free=0.0,
        n_data=1,
        k_naive=0,
        k_baseline=0,
        hidden_dof_subset={
            "axiom_scales": 1,    # dark-only sector embedding choice
        },
        notes="C10k embedding choice (vs universal IDE which fails Cassini).",
    ),

    # === Bullet cluster (raw PASS_STRONG, qualitative) ===
    Candidate(
        claim_id="bullet_cluster",
        label="Bullet cluster lensing-vs-gas offset (qualitative)",
        advertised_status="PASS_STRONG (qualitative)",
        chi2_sqt=0.0,
        chi2_lcdm_or_free=0.0,
        n_data=1,
        k_naive=0,
        k_baseline=0,
        hidden_dof_subset={
            # depletion-zone formalism is qualitative; gas ram-pressure is input
            "axiom_scales": 1,
            "B1_bilinear": 1,
        },
        notes="L417 caveat: 150 kpc offset is gas-input echo, not independent prediction.",
    ),

    # === PARTIAL / POSTDICTION (PASS_MODERATE-tier) ===
    Candidate(
        claim_id="three_regime_sigma0",
        label="Three-regime sigma_0(env) parameterisation",
        advertised_status="POSTDICTION (PASS_MODERATE-tier)",
        chi2_sqt=0.0,                 # placeholder, paper uses Delta chi^2 ~ 288 vs single-sigma_0
        chi2_lcdm_or_free=288.0,      # Delta chi^2 vs single universal sigma_0 (base.md §3.4)
        n_data=11,                    # 11 anchor scales used in three-regime fit
        k_naive=0,
        k_baseline=0,
        hidden_dof_subset={
            "anchor_picks": 3,        # cosmic / cluster / galactic
            "three_regime": 2,        # carrier + saddle
            "B1_bilinear": 1,
        },
        notes=("3-regime structure dominates the apparent fit improvement. "
               "Delta chi^2 = 288 (17 sigma) is *postdictive*; mock-injection FDR 100%."),
    ),

    # === CMB theta_* (PARTIAL) ===
    Candidate(
        claim_id="cmb_theta_star",
        label="CMB theta_* shift (partial, ~0.7%)",
        advertised_status="PARTIAL",
        chi2_sqt=23.0**2,             # Planck sigma * 23 (paper §4.1 row 8) -> chi^2~529
        chi2_lcdm_or_free=0.0,        # LCDM sits at theta_* observed
        n_data=1,
        k_naive=0,
        k_baseline=0,
        hidden_dof_subset={
            "B1_bilinear": 1,         # matter-era phi evolution depends on B1
            "anchor_picks": 1,        # cosmic anchor only
        },
        notes="Same channel as Phase-2 BAO; not an independent PASS.",
    ),
]


def main() -> None:
    payload = {
        "hidden_dof_breakdown": HIDDEN_DOF_BREAKDOWN,
        "k_hidden_conservative": K_HIDDEN_CONSERVATIVE,
        "k_hidden_expanded": K_HIDDEN_EXPANDED,
        "candidates": [],
    }

    print(f"L502 Hidden DOF AICc penalty audit (k_hidden = {K_HIDDEN_CONSERVATIVE} conservative, {K_HIDDEN_EXPANDED} expanded)")
    print("=" * 110)
    header = (
        f"{'claim':<28} {'k_naive':>7} {'k_hid':>6} {'dAICc_naive':>13} "
        f"{'dAICc_honest':>14} {'dAICc_expanded':>16} {'dAICc_kh9':>11} {'verdict':<22}"
    )
    print(header)
    print("-" * 122)

    for cand in CANDIDATES:
        tab = cand.aicc_table()
        # Heuristic verdict: PASS retained if dAICc_honest <= +2; otherwise demoted.
        d_h = tab["delta_aicc_honest_conservative"]
        if d_h <= 2.0:
            verdict = "RETAINED (k_h ok)"
        elif d_h <= 6.0:
            verdict = "DEMOTED -> MODERATE"
        elif d_h <= 10.0:
            verdict = "DEMOTED -> WEAK"
        else:
            verdict = "FAILS (LCDM wins)"

        row = {
            "claim_id": cand.claim_id,
            "label": cand.label,
            "advertised_status": cand.advertised_status,
            "n_data": cand.n_data,
            "k_naive": cand.k_naive,
            "k_hidden_applicable": cand.k_hidden_applicable,
            "hidden_dof_subset": cand.hidden_dof_subset,
            "chi2_sqt": cand.chi2_sqt,
            "chi2_baseline": cand.chi2_lcdm_or_free,
            "k_baseline": cand.k_baseline,
            "aicc": tab,
            "verdict_after_penalty": verdict,
            "notes": cand.notes,
        }
        payload["candidates"].append(row)

        print(
            f"{cand.claim_id:<28} {cand.k_naive:>7d} {cand.k_hidden_applicable:>6d} "
            f"{tab['delta_aicc_naive']:>13.3f} {tab['delta_aicc_honest_conservative']:>14.3f} "
            f"{tab['delta_aicc_honest_expanded']:>16.3f} {tab['delta_aicc_full_kh9']:>11.3f} "
            f"{verdict:<22}"
        )

    print("=" * 122)
    print()
    print("Honest one-liner:")
    rar = next(c for c in payload["candidates"] if c["claim_id"] == "rar_a0_l482")
    print(
        "  L482 RAR advertised dAICc(SQT-free) = +{:.3f};".format(rar["aicc"]["delta_aicc_naive"])
        + " with k_hidden_applicable={} -> dAICc_honest = {:+.3f}".format(
            rar["k_hidden_applicable"],
            rar["aicc"]["delta_aicc_honest_conservative"],
        )
        + "; with full k_hidden=9 -> dAICc = {:+.3f} (LCDM/free wins iff > 2).".format(
            rar["aicc"]["delta_aicc_full_kh9"],
        )
    )

    out_json = RESULTS_DIR / "l502_results.json"
    with out_json.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"\nWrote {out_json}")


if __name__ == "__main__":
    # CLAUDE.md: enforce per-worker single-thread (this is a non-parallel
    # bookkeeping script but we still set the env vars defensively).
    for var in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
        os.environ.setdefault(var, "1")
    sys.exit(main())
