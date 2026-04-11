# -*- coding: utf-8 -*-
"""
Phase 3.6 — B1. Fifth-force / Cassini / LLR / EP likelihood.

Coupled quintessence with Amendola coupling `beta` produces a long-range scalar
force between matter particles. In the unscreened limit, the PPN parameter
gamma picks up

    gamma - 1 = - 2 beta^2 / (1 + beta^2)                                [1]

(see Amendola & Tsujikawa, "Dark Energy" 2010 eq 9.56; Esposito-Farese 2004).
For small beta this reduces to |gamma - 1| ~ 2 beta^2.

Observational bounds used here (post-2015 consensus):
  Cassini:      |gamma - 1| < 2.3e-5          (Bertotti+ 2003)
  LLR:          |beta_PPN - 1| < 1.1e-4       (Williams+ 2012)
  MICROSCOPE:   eta_EP < 1e-15                (Touboul+ 2017)

For the leading two-body coupling, beta_PPN = 1 + O(beta^4), so LLR is weaker
than Cassini. MICROSCOPE constrains the composition dependence of the fifth
force: eta ~ (Delta beta / beta)^2 which for universal coupling vanishes and
thus gives no bound in the simplest SQMH ansatz (universal coupling on the
stress-energy trace).

Output:
  - chi2_fifth_force(beta): single-number penalty
  - summary table with Phase 3 posterior beta from base.fix.class.md
"""
import numpy as np


GAMMA_CASSINI_LIMIT = 2.3e-5      # Bertotti, Iess, Tortora 2003
BETA_PPN_LLR_LIMIT = 1.1e-4        # Williams, Turyshev, Boggs 2012
ETA_EP_MICROSCOPE = 1.0e-15        # Touboul+ 2017


def gamma_minus_one(beta):
    """PPN gamma - 1 from Amendola coupling beta (universal)."""
    return -2.0 * beta**2 / (1.0 + beta**2)


def beta_ppn_minus_one(beta):
    """PPN beta_PPN - 1, leading order in coupling (universal ansatz)."""
    # For a canonical scalar with universal coupling to T^a_a the PPN beta
    # receives no O(beta^2) correction (Damour-Esposito-Farese 1992). We
    # return the beta^4 leading term for completeness.
    return 0.5 * beta**4 / (1.0 + beta**2)**2


def cassini_chi2(beta):
    """One-sided Cassini chi^2: (|gamma-1| / limit)^2 if over, else 0."""
    g = abs(gamma_minus_one(beta))
    if g <= GAMMA_CASSINI_LIMIT:
        return 0.0
    return (g / GAMMA_CASSINI_LIMIT)**2


def llr_chi2(beta):
    b = abs(beta_ppn_minus_one(beta))
    if b <= BETA_PPN_LLR_LIMIT:
        return 0.0
    return (b / BETA_PPN_LLR_LIMIT)**2


def fifth_force_chi2(beta):
    """Total solar-system chi^2 penalty for coupled quintessence."""
    return cassini_chi2(beta) + llr_chi2(beta)


def max_allowed_beta(limit=GAMMA_CASSINI_LIMIT):
    """Inverse: largest |beta| that satisfies |gamma-1| <= limit."""
    # 2 b^2 / (1 + b^2) = limit => b^2 = limit / (2 - limit)
    return float(np.sqrt(limit / (2.0 - limit)))


def report():
    print("=" * 72)
    print("Phase 3.6 B1 -- Fifth-force / Cassini likelihood")
    print("=" * 72)

    b_max = max_allowed_beta()
    print(f"\nAllowed |beta| from Cassini |gamma-1| < {GAMMA_CASSINI_LIMIT:.1e}:")
    print(f"   |beta| < {b_max:.3e}")
    print(f"   |beta| < {b_max*1e3:.3f} x 10^-3")

    print("\nPhase 3 posterior (base.fix.class.md sec 2.2):")
    for label, b in [("V_RP median", 0.107),
                     ("V_RP +1sigma", 0.107 + 0.060),
                     ("V_RP -1sigma", 0.107 - 0.043)]:
        g = abs(gamma_minus_one(b))
        ratio = g / GAMMA_CASSINI_LIMIT
        status = "PASS" if g < GAMMA_CASSINI_LIMIT else "FAIL"
        print(f"   {label:<14}  beta={b:.4f}  |gamma-1|={g:.3e}  "
              f"ratio/limit={ratio:.2e}  [{status}]")

    print("\n--> Unscreened coupled quintessence with beta ~ 0.1 violates")
    print("    Cassini by ~4 orders of magnitude. Screening (Vainshtein or")
    print("    chameleon) is REQUIRED for SQMH to be viable.")
    print("\nchi2 penalty at Phase 3 median:")
    print(f"   fifth_force_chi2(0.107) = {fifth_force_chi2(0.107):.3e}")
    print(f"   (= contribution to Phase 3 total chi^2 without screening)")


if __name__ == "__main__":
    report()
