"""L507 — BBN cross-experiment robustness for SQT.

Tests whether SQT's predicted ΔN_eff (from L83/L149: ~10^-32 to 10^-47, taking
characteristic 10^-46 conservative value) is *simultaneously* consistent with:
  (1) Planck CMB ΔN_eff <= 0.17 (Planck 2018 + ACT/SPT, 95% CL)
  (2) Primordial He-4 mass fraction Y_p = 0.245 +/- 0.003 (Aver+2021),
      which constrains |ΔN_eff| <= 0.20.
  (3) Primordial D/H = (2.527 +/- 0.030) x 10^-5 (Cooke+2018),
      which constrains |ΔN_eff| <= 0.15 (most stringent).
  (4) EMPRESS 2022 anomalous low He-4 (Y_p = 0.2370 +/- 0.0034) which
      *prefers* ΔN_eff ~ -0.5 (negative tension with standard).
  (5) Li-7 problem: standard BBN predicts (Li/H)_p ~ 5e-10, observation ~1.6e-10.

For each experimental constraint we compute SQT's margin (constraint / prediction)
and a binary PASS/FAIL.  Robustness = PASS across all *non-anomalous* channels.
EMPRESS and Li-7 are reported separately as anomaly cross-checks.
"""

import json
import os
import sys

# SQT prediction baselines (from L83 / L149 simulations in this repo)
DELTA_NEFF_SQT_L83 = 5.96e-32   # constant Γ_0, baseline
DELTA_NEFF_SQT_L149 = 1.14e-47  # full V(n,t) extension
# Use the *characteristic* value quoted in the task brief
DELTA_NEFF_SQT_CHAR = 1.0e-46

# Experimental upper bounds on |ΔN_eff| (95% CL)
BOUNDS = {
    # Planck 2018 TT,TE,EE+lowE+lensing: N_eff = 2.99 +/- 0.17 -> |ΔN_eff| <= 0.17
    "Planck18_CMB":        {"limit": 0.17, "ref": "Planck 2018 VI, A&A 641 A6"},
    # PArthENoPE/PRIMAT He-4: Aver+2021 Y_p=0.2453+/-0.0034 -> |ΔN_eff|<=0.20
    "He4_Aver2021":        {"limit": 0.20, "ref": "Aver+2021 JCAP 03 027"},
    # D/H Cooke+2018 PRECISION: (2.527 +/- 0.030)e-5 -> |ΔN_eff|<=0.15 (tightest)
    "DH_Cooke2018":        {"limit": 0.15, "ref": "Cooke+2018 ApJ 855 102"},
    # Combined BBN (Pitrou+2018): |ΔN_eff|<=0.16
    "BBN_combined_Pitrou": {"limit": 0.16, "ref": "Pitrou+2018 Phys Rep 754 1"},
}

# Anomaly channels — preferred *non-zero* ΔN_eff (sign matters)
ANOMALIES = {
    # EMPRESS 2022: Y_p = 0.2370 +/- 0.0034 prefers ΔN_eff ~ -0.5 to -1.0
    # (Matsumoto+2022 ApJ 941 167; Yeh+2023 reanalysis allows ~0)
    "EMPRESS_He4_2022": {"preferred_dNeff": -0.5,
                         "sigma": 0.5,
                         "ref": "Matsumoto+2022 ApJ 941 167"},
    # Li-7 problem: 3-5x discrepancy. Effective ΔN_eff to fix is ~ -0.4
    # (but no consensus this is BBN; likely stellar depletion).
    "Li7_problem": {"preferred_dNeff": -0.4,
                    "sigma": 0.5,
                    "ref": "Fields 2011 Annu Rev Nucl Part Sci 61 47; Pitrou+2018"},
}


def evaluate(dNeff_sqt: float):
    out = {"sqt_delta_Neff": dNeff_sqt, "constraints": {}, "anomalies": {}}
    all_pass = True
    for name, info in BOUNDS.items():
        margin = info["limit"] / max(abs(dNeff_sqt), 1e-300)
        passed = abs(dNeff_sqt) <= info["limit"]
        all_pass &= passed
        out["constraints"][name] = {
            "limit": info["limit"],
            "margin_orders_of_magnitude": float(f"{margin:.3e}".split("e")[1]) if margin > 0 else None,
            "margin": margin,
            "pass": bool(passed),
            "ref": info["ref"],
        }
    out["all_standard_constraints_pass"] = bool(all_pass)

    # Anomalies: SQT prediction is so tiny it cannot *explain* a non-zero anomaly.
    # We report compatibility = "SQT consistent with anomaly within its sigma?"
    # i.e. is 0 (which is essentially SQT's prediction) within ~3 sigma of preferred?
    for name, info in ANOMALIES.items():
        pref = info["preferred_dNeff"]
        sig = info["sigma"]
        z_score = abs(0.0 - pref) / sig  # SQT ≈ 0 vs preferred non-zero
        out["anomalies"][name] = {
            "preferred_dNeff": pref,
            "sigma": sig,
            "sqt_distance_in_sigma": z_score,
            "sqt_can_explain": False,  # 10^-46 cannot generate ΔNeff ~ -0.5
            "ref": info["ref"],
        }

    out["robust_cross_experiment"] = bool(all_pass)
    out["explains_empress_anomaly"] = False
    out["explains_li7_problem"] = False

    return out


def main():
    results = {
        "sqt_predictions": {
            "L83_constant_Gamma0":  DELTA_NEFF_SQT_L83,
            "L149_V_n_t":            DELTA_NEFF_SQT_L149,
            "L507_characteristic":   DELTA_NEFF_SQT_CHAR,
        },
        "evaluation_at_characteristic": evaluate(DELTA_NEFF_SQT_CHAR),
        "evaluation_at_L83":           evaluate(DELTA_NEFF_SQT_L83),
        "evaluation_at_L149":          evaluate(DELTA_NEFF_SQT_L149),
    }

    out_dir = os.path.join(os.path.dirname(__file__), "..", "..",
                           "results", "L507")
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "cross_exp_report.json"), "w",
              encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # console summary (ASCII only, per CLAUDE.md cp949 rule)
    e = results["evaluation_at_characteristic"]
    print("=" * 60)
    print("L507 BBN CROSS-EXPERIMENT ROBUSTNESS")
    print("=" * 60)
    print(f"SQT prediction (characteristic): dNeff = {DELTA_NEFF_SQT_CHAR:.2e}")
    print()
    print("Standard constraints (PASS = |dNeff_SQT| <= limit):")
    for name, c in e["constraints"].items():
        verdict = "PASS" if c["pass"] else "FAIL"
        print(f"  {name:25s}  limit={c['limit']:.3f}  "
              f"margin={c['margin']:.2e}x  [{verdict}]")
    print()
    print(f"All standard constraints: "
          f"{'PASS' if e['all_standard_constraints_pass'] else 'FAIL'}")
    print()
    print("Anomalies (SQT cannot explain non-zero shifts):")
    for name, a in e["anomalies"].items():
        print(f"  {name:25s}  preferred={a['preferred_dNeff']:+.2f}  "
              f"sqt_dist={a['sqt_distance_in_sigma']:.1f}sigma  "
              f"explains={a['sqt_can_explain']}")
    print()
    print(f"ROBUST CROSS-EXPERIMENT: {e['robust_cross_experiment']}")
    print(f"Explains EMPRESS anomaly: {e['explains_empress_anomaly']}")
    print(f"Explains Li-7 problem:    {e['explains_li7_problem']}")
    print(f"\nReport written: {out_dir}/cross_exp_report.json")


if __name__ == "__main__":
    main()
