"""L506 — Cassini PPN |gamma-1| cross-form robustness audit.

L491 cross-form audited the L482 RAR a0 PASS_STRONG claim and graded it
GLOBAL_PARTIAL (median within 0.04 dex of SQT but full spread 0.37 dex).

This script applies the *same* logic to the Cassini PPN PASS_STRONG result
(paper base.md:874): "|gamma-1| ~ 1.1e-40 << 2.3e-5 -- PASS_STRONG via
beta_eff = Lambda_UV / M_Pl ~ 7.4e-21".

Question: is |gamma-1| ~ 10^-40 a *global* prediction of the SQMH axioms,
or does it depend on a specific derivation channel?  If alternative
derivations of |gamma-1| yield wildly different magnitudes (some still
PASS, some FAIL), the PASS_STRONG verdict is global only in the sense
that it is "PASS in every reasonable channel" -- *not* "10^-40 in every
channel".  The 40-orders-of-magnitude headline number is then a
form-specific artefact.

Channels enumerated (each is a distinct, literature-justified mapping
from SQMH structure to the post-Newtonian gamma):

  (1) beta_eff^2 portal  (paper choice)
        |gamma-1| = 2 beta^2 / (1+beta^2),  beta = Lambda_UV / M_Pl,
        Lambda_UV ~ 18 MeV  ->  beta ~ 7.4e-21  ->  |g-1| ~ 1.1e-40.
        Damour-Esposito-Farese 1992 universal-conformal-coupling form.

  (2) Universal baryon coupling, beta_b = beta_eff
        Same algebra, but *beta acts on baryons too* (no dark-only
        embedding).  Gives |gamma-1| = 1.1e-40 still.

  (3) Universal baryon coupling at Phase-3 posterior beta ~ 0.1
        L4 universal-IDE: beta ~ 0.107 (BAO+SN+CMB+RSD posterior).
        |gamma-1| = 2*0.107^2/(1+0.107^2) ~ 2.26e-2 -- HARD FAIL.
        This is the failure mode that forced the dark-only embedding.

  (4) Dark-only structural (paper's *actual* PASS reason, per audit_*)
        beta_b = 0 by construction (matter sector decoupled from phi).
        |gamma-1| = 0 EXACT (to all orders in beta_d).
        Cassini bound saturated at noise floor only.

  (5) Brans-Dicke equivalent (Will 2014 review eq 3.22)
        |gamma-1| = 1 / (1 + omega_BD).
        Cassini -> omega_BD > 4.0e4; SQMH has no fixed omega_BD,
        but if we identify omega_BD ~ 1/(2 beta^2) for a single conformal
        scalar, beta = 7.4e-21 -> omega_BD ~ 9.1e39 -> |g-1| ~ 1.1e-40.
        Same headline as (1) -- not independent.

  (6) Pure disformal (A'=0) limit, ZKB 2013
        Schwarzschild static metric is an exact solution; gamma = 1
        exactly, independent of any coupling strength.  |gamma-1| = 0.

  (7) Vainshtein-screened cubic Galileon (Babichev-Deffayet-Ziour 2010)
        Inside Vainshtein radius r_V ~ (r_S * r_C^2)^{1/3},
        |gamma-1| ~ beta^2 * (r/r_V)^{3/2}.
        For Saturn distance ~9.5 AU, M_sun, r_C ~ H0^-1, r_V ~ 100 pc.
        With beta ~ 0.1 (Phase-3): (r/r_V)^{3/2} ~ (9.5 AU / 100 pc)^{3/2}
        ~ 1.5e-9 * (10^something).  Computed below.

  (8) Chameleon/symmetron screening (Khoury-Weltman 2004)
        |gamma-1| ~ epsilon^2 * (1 - M_screen/M_source) where M_screen
        depends on density.  We use a literature ceiling
        |g-1| < 1e-7 (Cassini-attainable for thin-shell screening).

K-criteria for the cross-form audit:
  - K_C1_PASS: every channel passes Cassini |g-1| < 2.3e-5
  - K_C2_HEADLINE: every channel reproduces |g-1| ~ 10^-40 within
                    1 order of magnitude (the paper's stated number)
  - K_C3_SPREAD: cross-form log10|g-1| spread <= 5 dex
  - K_C4_DEPENDENCE: if one channel HARD-FAILS at the Phase-3 posterior
                    beta, the PASS rests on choice of channel ==>
                    PASS_STRONG is global (4/4) only because
                    SQMH *selects* the dark-only or screened channel.

Output
------
  results/L506/CASSINI_ROBUSTNESS.md
  results/L506/L506_results.json
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "L506"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Constants (PDG 2024).
# ---------------------------------------------------------------------------
GeV = 1.0e9              # eV per GeV
MeV = 1.0e6              # eV per MeV
M_PL = 1.221e19 * GeV    # full Planck mass [eV]
M_PL_RED = 2.435e18 * GeV
LAMBDA_UV = 18.0 * MeV   # paper-quoted UV scale
H0_SI = 67.4 * 1.0e3 / (3.0857e22)   # Planck H0 in s^-1
C = 2.998e8                          # m/s

CASSINI_LIMIT = 2.3e-5    # |gamma-1| < this  (Cassini 2003 / Bertotti et al)

# ---------------------------------------------------------------------------
# Channel 1: paper beta_eff^2 portal (Damour-Esposito-Farese conformal)
# ---------------------------------------------------------------------------
def channel_beta_eff_paper():
    beta = LAMBDA_UV / M_PL
    g_m1 = 2.0 * beta**2 / (1.0 + beta**2)
    return dict(
        tag="beta_eff_paper",
        desc="2 beta^2/(1+beta^2), beta=Lambda_UV/M_Pl, Lambda_UV=18MeV",
        beta=float(beta),
        gamma_minus_1=float(g_m1),
        passes=bool(g_m1 < CASSINI_LIMIT),
        cassini_margin=float(CASSINI_LIMIT / max(g_m1, 1e-300)),
        notes="Paper headline. Lambda_UV stipulated, not derived from axioms.",
    )


# ---------------------------------------------------------------------------
# Channel 2: universal baryon coupling at the same beta_eff (no dark-only)
# ---------------------------------------------------------------------------
def channel_universal_at_beta_eff():
    beta = LAMBDA_UV / M_PL
    g_m1 = 2.0 * beta**2 / (1.0 + beta**2)
    return dict(
        tag="universal_at_beta_eff",
        desc="Universal coupling (no dark-only) at the same beta_eff",
        beta=float(beta),
        gamma_minus_1=float(g_m1),
        passes=bool(g_m1 < CASSINI_LIMIT),
        cassini_margin=float(CASSINI_LIMIT / max(g_m1, 1e-300)),
        notes="Same arithmetic as (1). Channel name distinguishes the *embedding*: "
              "if baryons couple, beta=7.4e-21 still passes -- but only because "
              "Lambda_UV was tuned to MeV scale.",
    )


# ---------------------------------------------------------------------------
# Channel 3: universal coupling at Phase-3 posterior beta ~ 0.107
# ---------------------------------------------------------------------------
def channel_universal_phase3():
    beta = 0.107   # L4 BAO+SN+CMB+RSD posterior central
    g_m1 = 2.0 * beta**2 / (1.0 + beta**2)
    return dict(
        tag="universal_phase3",
        desc="Universal coupling at Phase-3 cosmology posterior beta=0.107",
        beta=float(beta),
        gamma_minus_1=float(g_m1),
        passes=bool(g_m1 < CASSINI_LIMIT),
        cassini_margin=float(CASSINI_LIMIT / max(g_m1, 1e-300)),
        notes="HARD FAIL: |gamma-1|~2.3e-2 vs limit 2.3e-5 (1000x violation). "
              "Forces the dark-only embedding choice.",
    )


# ---------------------------------------------------------------------------
# Channel 4: dark-only structural (paper's *actual* PASS mechanism)
# ---------------------------------------------------------------------------
def channel_dark_only():
    return dict(
        tag="dark_only_structural",
        desc="Sector-selective coupling: matter sector decoupled, beta_b=0",
        beta=0.0,
        gamma_minus_1=0.0,
        passes=True,
        cassini_margin=float('inf'),
        notes="STRUCTURAL gamma=1 exact. Identical to PASS_TRIVIAL: any theory "
              "with beta_b=0 trivially passes. Dark-only embedding is an "
              "axiom-level *choice* (Foundation 5), not a derivation.",
    )


# ---------------------------------------------------------------------------
# Channel 5: Brans-Dicke equivalent (Will 2014 eq 3.22)
# ---------------------------------------------------------------------------
def channel_brans_dicke():
    beta = LAMBDA_UV / M_PL
    # omega_BD ~ 1/(2 beta^2) for single conformal scalar
    omega_BD = 1.0 / (2.0 * beta**2)
    g_m1 = 1.0 / (1.0 + omega_BD)
    return dict(
        tag="brans_dicke",
        desc="|g-1| = 1/(1+omega_BD), omega_BD = 1/(2 beta^2)",
        beta=float(beta),
        omega_BD=float(omega_BD),
        gamma_minus_1=float(g_m1),
        passes=bool(g_m1 < CASSINI_LIMIT),
        cassini_margin=float(CASSINI_LIMIT / max(g_m1, 1e-300)),
        notes="Reduces to (1) algebraically -- not an independent prediction.",
    )


# ---------------------------------------------------------------------------
# Channel 6: pure disformal (A'=0) limit (ZKB 2013)
# ---------------------------------------------------------------------------
def channel_pure_disformal():
    return dict(
        tag="pure_disformal",
        desc="Pure disformal coupling: g~ = g + B d_phi d_phi, A'=0",
        beta=None,
        gamma_minus_1=0.0,
        passes=True,
        cassini_margin=float('inf'),
        notes="STRUCTURAL gamma=1 exact (Zumalacarregui-Koivisto-Bellini 2013). "
              "Schwarzschild solves the modified equations with auxiliary "
              "field frozen. Independent of beta. PASS_TRIVIAL.",
    )


# ---------------------------------------------------------------------------
# Channel 7: Vainshtein-screened cubic Galileon
# ---------------------------------------------------------------------------
def channel_vainshtein():
    # Saturn distance ~ 9.5 AU = 1.42e12 m
    r_saturn = 9.5 * 1.496e11   # m
    # Schwarzschild radius of Sun
    r_S = 2.953e3   # m
    # Crossover scale r_C ~ M_Pl / Lambda^2 ~ H0^-1 for cubic Galileon
    r_C = C / H0_SI    # m, ~ 4.4e26 m
    # Vainshtein radius: r_V = (r_S * r_C^2)^{1/3}
    r_V = (r_S * r_C**2) ** (1.0/3.0)
    beta = 0.107   # Phase-3 posterior
    # Inside Vainshtein: |gamma-1| ~ beta^2 (r/r_V)^{3/2}
    suppression = (r_saturn / r_V) ** 1.5
    g_m1 = 2.0 * beta**2 * suppression
    return dict(
        tag="vainshtein_screened",
        desc="Cubic Galileon Vainshtein: |g-1| ~ 2 beta^2 (r/r_V)^{3/2}",
        beta=float(beta),
        r_saturn_m=float(r_saturn),
        r_V_m=float(r_V),
        suppression=float(suppression),
        gamma_minus_1=float(g_m1),
        passes=bool(g_m1 < CASSINI_LIMIT),
        cassini_margin=float(CASSINI_LIMIT / max(g_m1, 1e-300)),
        notes="Phase-3 posterior beta survives Cassini *if* Vainshtein screening "
              "active. Adds a screening axiom (cubic Galileon), not currently "
              "in SQMH foundations.",
    )


# ---------------------------------------------------------------------------
# Channel 8: Chameleon thin-shell ceiling
# ---------------------------------------------------------------------------
def channel_chameleon():
    # Khoury-Weltman 2004: thin-shell suppression gives |g-1| ~ 1e-7 ceiling
    g_m1 = 1.0e-7   # literature ceiling for chameleon screening near Sun
    return dict(
        tag="chameleon_screened",
        desc="Chameleon thin-shell screening, KW 2004 ceiling",
        beta=None,
        gamma_minus_1=float(g_m1),
        passes=bool(g_m1 < CASSINI_LIMIT),
        cassini_margin=float(CASSINI_LIMIT / max(g_m1, 1e-300)),
        notes="Literature ceiling from thin-shell argument. Adds a chameleon "
              "potential axiom not in SQMH foundations.",
    )


# ---------------------------------------------------------------------------
CHANNELS = [
    channel_beta_eff_paper,
    channel_universal_at_beta_eff,
    channel_universal_phase3,
    channel_dark_only,
    channel_brans_dicke,
    channel_pure_disformal,
    channel_vainshtein,
    channel_chameleon,
]


def _safe_log10(x):
    if x is None or x <= 0:
        return None
    return math.log10(x)


def main():
    results = []
    for fn in CHANNELS:
        results.append(fn())

    # Statistics across channels (only those with a finite, positive |g-1|).
    finite_log = [_safe_log10(r['gamma_minus_1']) for r in results
                  if r['gamma_minus_1'] is not None and r['gamma_minus_1'] > 0]
    n_pass = sum(1 for r in results if r['passes'])
    n_fail = sum(1 for r in results if not r['passes'])
    n_struct_zero = sum(1 for r in results if r['gamma_minus_1'] == 0.0)

    if finite_log:
        log_min = min(finite_log)
        log_max = max(finite_log)
        spread = log_max - log_min
        median = sorted(finite_log)[len(finite_log) // 2]
    else:
        log_min = log_max = spread = median = None

    log_paper = math.log10(results[0]['gamma_minus_1'])  # channel 1 = paper

    # K-criteria
    K_C1_all_pass = all(r['passes'] for r in results)
    # K_C2: how many finite channels are within 1 dex of paper headline?
    if finite_log:
        n_within_1dex = sum(1 for L in finite_log if abs(L - log_paper) <= 1.0)
    else:
        n_within_1dex = 0
    K_C2_headline = bool(n_within_1dex == len(finite_log))
    K_C3_spread = bool((spread is not None) and spread <= 5.0)
    # K_C4: if any channel HARD-FAILS, PASS depends on channel selection.
    K_C4_independence = bool(n_fail == 0)

    # Verdict
    if K_C1_all_pass and K_C2_headline and K_C3_spread:
        verdict = "GLOBAL_PASS"
    elif K_C1_all_pass and K_C3_spread:
        verdict = "GLOBAL_PARTIAL"
    elif n_fail == 0 and not K_C3_spread:
        verdict = "PASS_BUT_UNSTABLE"   # all pass, but huge magnitude variance
    elif n_fail > 0:
        verdict = "CHANNEL_DEPENDENT"
    else:
        verdict = "INCONCLUSIVE"

    summary = dict(
        cassini_limit=CASSINI_LIMIT,
        n_channels=len(results),
        n_pass=n_pass,
        n_fail=n_fail,
        n_structural_zero=n_struct_zero,
        log10_min=log_min,
        log10_max=log_max,
        log10_median=median,
        log10_paper_headline=log_paper,
        spread_dex=spread,
        n_within_1dex_of_paper=n_within_1dex,
        K_C1_all_pass=K_C1_all_pass,
        K_C2_headline_within_1dex=K_C2_headline,
        K_C3_spread_le_5dex=K_C3_spread,
        K_C4_no_hard_fails=K_C4_independence,
        verdict=verdict,
    )

    out = dict(channels=results, summary=summary)
    (OUT / "L506_results.json").write_text(json.dumps(out, indent=2, default=float))

    # Markdown report
    md = []
    md.append("# L506 - Cassini PPN |gamma-1| Cross-Form Robustness Audit\n\n")
    md.append("**Goal**: test whether the paper's PASS_STRONG result\n")
    md.append("(|gamma-1| ~ 1.1e-40 << 2.3e-5) is a *global* SQMH prediction\n")
    md.append("or a derivation-channel-specific number.\n\n")
    md.append("Same logic as L491 (RAR a_0 cross-form), applied to PPN gamma.\n\n")
    md.append(f"**Cassini bound**: |gamma-1| < {CASSINI_LIMIT:.2e} (Bertotti+ 2003)\n")
    md.append(f"**Paper headline**: |gamma-1| ~ 1.1e-40 via beta_eff = Lambda_UV/M_Pl ~ 7.4e-21\n\n")

    md.append("## Channels and predictions\n\n")
    md.append("| # | Channel | beta | |gamma-1| | log10 | Pass? | Margin |\n")
    md.append("|--:|---------|-----:|---------:|------:|:-----:|------:|\n")
    for i, r in enumerate(results, 1):
        b_str = "n/a" if r['beta'] is None else f"{r['beta']:.2e}"
        g = r['gamma_minus_1']
        g_str = "0 (structural)" if g == 0.0 else f"{g:.2e}"
        L = _safe_log10(g)
        L_str = "-inf" if L is None else f"{L:+.1f}"
        m = r['cassini_margin']
        m_str = "inf" if math.isinf(m) else f"{m:.1e}"
        md.append(f"| {i} | {r['tag']} | {b_str} | {g_str} | {L_str} | "
                  f"{'YES' if r['passes'] else 'NO'} | {m_str} |\n")
    md.append("\n")

    md.append("## Channel notes\n\n")
    for i, r in enumerate(results, 1):
        md.append(f"**({i}) {r['tag']}**  -- {r['desc']}\n\n")
        md.append(f"  - {r['notes']}\n\n")

    md.append("## Cross-form distribution (finite, positive |g-1|)\n\n")
    md.append(f"- N channels (finite)         : {len(finite_log)} of {len(results)}\n")
    md.append(f"- N structural-zero           : {n_struct_zero}\n")
    if finite_log:
        md.append(f"- log10|g-1| min              : {log_min:+.2f}\n")
        md.append(f"- log10|g-1| max              : {log_max:+.2f}\n")
        md.append(f"- spread                      : {spread:.2f} dex\n")
        md.append(f"- median                      : {median:+.2f}\n")
        md.append(f"- log10|g-1| paper headline   : {log_paper:+.2f}\n")
        md.append(f"- channels within 1 dex of paper: "
                  f"{n_within_1dex} / {len(finite_log)}\n")
    md.append(f"\n## Hypothesis-sensitivity decomposition\n\n")
    md.append("| Channel | Depends on |\n|---|---|\n")
    md.append("| (1)/(2)/(5) beta_eff family | Lambda_UV ~ 18 MeV stipulation |\n")
    md.append("| (3) universal at Phase-3 beta | beta=0.107 from BAO+SN+CMB+RSD posterior |\n")
    md.append("| (4) dark-only | sector-selective embedding axiom (Foundation 5) |\n")
    md.append("| (6) pure disformal | A'=0 disformal-only Lagrangian choice |\n")
    md.append("| (7) Vainshtein | cubic Galileon screening axiom (extra) |\n")
    md.append("| (8) chameleon | KW 2004 thin-shell potential axiom (extra) |\n\n")

    md.append("## K-criteria\n\n")
    md.append(f"- K_C1 all channels PASS Cassini   : "
              f"{'PASS' if K_C1_all_pass else 'FAIL'} ({n_pass}/{len(results)})\n")
    md.append(f"- K_C2 every channel within 1 dex of 10^-40 : "
              f"{'PASS' if K_C2_headline else 'FAIL'} "
              f"({n_within_1dex}/{len(finite_log)})\n")
    md.append(f"- K_C3 cross-form spread <= 5 dex  : "
              f"{'PASS' if K_C3_spread else 'FAIL'} "
              f"({spread:.2f} dex)\n" if spread is not None else
              f"- K_C3 cross-form spread <= 5 dex  : N/A\n")
    md.append(f"- K_C4 no hard fails (channel-indep): "
              f"{'PASS' if K_C4_independence else 'FAIL'} "
              f"({n_fail} hard fails)\n\n")

    md.append(f"## Verdict: **{verdict}**\n\n")
    if verdict == "GLOBAL_PASS":
        md.append("All channels predict |gamma-1| ~ 10^-40 within 1 dex.  "
                  "Headline number is form-independent.\n")
    elif verdict == "GLOBAL_PARTIAL":
        md.append("All channels PASS Cassini, but the headline magnitude\n"
                  "varies across channels.  PASS is global; the *number*\n"
                  "10^-40 is channel-specific.\n")
    elif verdict == "PASS_BUT_UNSTABLE":
        md.append("Every channel passes the bound but predicted magnitudes\n"
                  "span >5 orders of magnitude.  PASS_STRONG label survives,\n"
                  "but the 40-orders-of-magnitude headline is unstable.\n")
    elif verdict == "CHANNEL_DEPENDENT":
        md.append("Some natural channels (e.g. universal coupling at Phase-3\n"
                  "posterior beta) HARD-FAIL Cassini.  PASS_STRONG is global\n"
                  "*only because SQMH selects* the dark-only / screened\n"
                  "channel.  This is the failure mode the dark-only\n"
                  "embedding axiom was introduced to repair (L4 universal\n"
                  "fluid-IDE Cassini violation).\n")
    md.append("\n## One-line honesty\n\n")
    if verdict == "GLOBAL_PASS":
        line = ("GLOBAL PASS_STRONG -- Cassini |g-1|~10^-40 reproduced "
                "across all derivation channels.")
    elif verdict == "GLOBAL_PARTIAL":
        line = ("GLOBAL PARTIAL -- every channel passes Cassini but the "
                "10^-40 headline is form-specific.")
    elif verdict == "PASS_BUT_UNSTABLE":
        line = (f"PASS_STRONG global / cross-form unstable: "
                f"{spread:.1f} dex spread, headline 10^-40 not reproduced.")
    elif verdict == "CHANNEL_DEPENDENT":
        line = ("PASS_STRONG channel-dependent -- universal coupling at "
                "Phase-3 beta HARD FAILS; PASS rests on dark-only / screening "
                "axiom selection.")
    else:
        line = "INCONCLUSIVE."
    md.append(f"> {line}\n")

    (OUT / "CASSINI_ROBUSTNESS.md").write_text("".join(md))
    print(f"[L506] verdict: {verdict}")
    print(f"[L506] {line}")
    print(f"[L506] wrote {OUT/'CASSINI_ROBUSTNESS.md'}")
    print(f"[L506] wrote {OUT/'L506_results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
