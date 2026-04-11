# -*- coding: utf-8 -*-
"""
L13-A: Omega_m amplitude theoretical origin in SQMH.

Rule-B 4-person code review:
  R1 (ODE structure): derive amplitude from SQMH equation analytically
  R2 (normalization): test if amplitude = Om is normalization artifact
  R3 (comparison): compare ODE-predicted amplitude vs best-fit Om
  R4 (verdict): K82/Q82 judgment

Key question: In A01, rho_DE(a) = OL0 * [1 + Om * (1-a)]
The amplitude of the perturbation is Om. Is this:
  (a) A SQMH theory prediction from the equation structure?
  (b) A normalization artifact (comes purely from rho_DE(0)=OL0 condition)?

Analysis:
SQMH ODE (linearized around LCDM background):
  d(omega_de)/dz = Gamma0 * omega_m0 * (1+z)^2 - 3*omega_de/(1+z)

The general solution is:
  omega_de(z) = C*(1+z)^(-3) + [particular solution]

Particular solution: try omega_de_p = A*(1+z)^3
  3*A*(1+z)^2 = Gamma0*Om*(1+z)^2 - 3*A*(1+z)^2... => wait
  Actually: d/dz[(1+z)^(-3)] = -3*(1+z)^(-4)
  The ODE: dydz = G0*Om*(1+z)^2 - 3y/(1+z)

  d/dz [y*(1+z)^3] = dydz*(1+z)^3 + 3*(1+z)^2*y
                   = [G0*Om*(1+z)^2 - 3y/(1+z)]*(1+z)^3 + 3*(1+z)^2*y
                   = G0*Om*(1+z)^5 - 3y*(1+z)^2 + 3*(1+z)^2*y
                   = G0*Om*(1+z)^5

  => y*(1+z)^3 = G0*Om*(1+z)^6/6 + C
  => y(z) = G0*Om*(1+z)^3/6 + C*(1+z)^(-3)

At z=0: y(0) = OL0 => G0*Om/6 + C = OL0
At z>>1 (matter era): C*(1+z)^(-3) -> 0, so y ~ G0*Om*(1+z)^3/6

For y(z=0) = OL0:
  C = OL0 - G0*Om/6

Amplitude of perturbation from LCDM:
  delta_rho = y(z) - OL0 = G0*Om*(1+z)^3/6 + C*(1+z)^(-3) - OL0
            = G0*Om/6*[(1+z)^3 - 1] + (OL0 - G0*Om/6)*[(1+z)^(-3) - 1]

At 1st order in z:
  delta_rho ~ G0*Om/6 * 3z - (OL0 - G0*Om/6) * 3z
            = z * [G0*Om/2 - 3*OL0 + G0*Om/2]
            = z * [G0*Om - 3*OL0]

But in A01: delta_rho = OL0*Om*(1-a) = OL0*Om*z/(1+z) ~ OL0*Om*z

=> Matching: G0*Om - 3*OL0 = OL0*Om
=> G0 = OL0*(Om + 3)/Om

For Om ~ 0.31, OL0 ~ 0.685:
  G0_theory = 0.685 * (0.31 + 3) / 0.31 = 0.685 * 3.31 / 0.31 ~ 7.31

But A01 uses G0 = 3*Om = 0.93. There is a discrepancy.

The question is: what sets the AMPLITUDE to be Om (not some other value)?

In A01: the amplitude is Om because:
  rho_DE(a) = OL0 * [1 + Om*(1-a)]
  At a=0 (z->inf): rho_DE -> OL0*(1+Om) [radiation era correction]
  Normalization: the "1" in [1+Om*(1-a)] ensures rho_DE(a=1)=OL0

The Om amplitude appears because: Gamma0 = 3*Om (A01 prescription).
  With Gamma0 = 3*Om and linearized solution:
  delta_rho/OL0 = Om*(1-a) [exactly]

So the amplitude Om in A01 is SET by the choice Gamma0 = 3*Om.
The question becomes: is Gamma0 = 3*Om theory-derived or fitted?
"""
from __future__ import annotations
import os
import sys
import json
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize_scalar, minimize

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')

_THIS = os.path.dirname(os.path.abspath(__file__))

# Physical constants
G_SI = 6.674e-11
t_P = 5.391e-44
c_SI = 2.998e8
Mpc_m = 3.086e22
OMEGA_R = 9.1e-5


def analytical_amplitude_derivation():
    """
    Derive the relationship between Gamma0 and the amplitude.

    SQMH birth-death ODE (in terms of rho/rho_crit_0):
      d(omega_de)/dz = Gamma0 * Om * (1+z)^2 - 3*omega_de/(1+z)

    General solution:
      omega_de(z) = Gamma0*Om*(1+z)^3/6 + C*(1+z)^(-3)
    where C = OL0 - Gamma0*Om/6 (from boundary condition at z=0)

    Convert to a(=1/(1+z)) variable:
      omega_de(a) = Gamma0*Om/(6*a^3) + C*a^3

    Expand around a=1 (z=0):
      omega_de(a) ~ OL0 + (terms in (a-1))

    For A01 matching (rho_DE = OL0*(1 + Om*(1-a))):
      The linear term in (1-a) must equal OL0*Om.

    From general solution:
      d(omega_de)/da|_{a=1} = -3*Gamma0*Om/6 - 3*C*1^4 / ...
      Actually d/da[omega_de] at a=1:
        d/da[Gamma0*Om/(6*a^3) + C*a^3]
        = -3*Gamma0*Om/(6*a^4) + 3*C*a^2
        At a=1: = -Gamma0*Om/2 + 3*C
              = -Gamma0*Om/2 + 3*(OL0 - Gamma0*Om/6)
              = -Gamma0*Om/2 + 3*OL0 - Gamma0*Om/2
              = 3*OL0 - Gamma0*Om

    For A01: d(omega_de)/da|_{a=1} = -OL0*Om
    => 3*OL0 - Gamma0*Om = -OL0*Om
    => Gamma0*Om = OL0*(3 + Om)
    => Gamma0 = OL0*(3 + Om)/Om

    With Om=0.31, OL0=0.685:
    => Gamma0_theory = 0.685*(3.31)/0.31 = 7.31

    But A01 sets Gamma0 = 3*Om = 0.93 (NOT the A01-matching value!)
    This means A01 is NOT the exact ODE solution with any Gamma0.
    A01 is a DIFFERENT functional form: OL0*(1 + Om*(1-a))

    The question: is Om*(1-a) the ODE solution?
    From ODE with Gamma0=3*Om:
      omega_de(a) = 3*Om^2/(6*a^3) + C*a^3
                 = Om^2/(2*a^3) + (OL0 - Om^2/2)*a^3

    At a=1: omega_de = Om^2/2 + OL0 - Om^2/2 = OL0. Check!

    omega_de(a)/OL0 = Om^2/(2*OL0*a^3) + (1 - Om^2/(2*OL0))*a^3

    This is NOT the same as 1 + Om*(1-a).

    CONCLUSION: A01 is a phenomenological fit, not exact ODE solution.
    The amplitude Om is set by the fitted form, not derived from Gamma0.
    """
    Om = 0.3102
    OL0 = 1.0 - Om - OMEGA_R
    G0_A01 = 3.0 * Om  # A01 prescription

    # True ODE solution with G0_A01
    # omega_de(a) = G0*Om/(6*a^3) + C*a^3
    G0 = G0_A01
    C_ode = OL0 - G0 * Om / 6.0

    # A01 form
    def rho_A01(a): return OL0 * (1.0 + Om * (1.0 - a))
    def rho_ODE(a):
        return G0 * Om / (6.0 * a**3) + C_ode * a**3

    # Compare at several redshifts
    z_test = np.array([0.0, 0.1, 0.3, 0.5, 1.0, 1.5, 2.0, 3.0])
    a_test = 1.0 / (1.0 + z_test)

    print('=== L13-A: Omega_m Amplitude Derivation ===')
    print()
    print('Om = ' + str(round(Om, 4)) + ', OL0 = ' + str(round(OL0, 4)))
    print('G0_A01 = 3*Om = ' + str(round(G0_A01, 4)))
    print()
    print('z | A01 rho_DE | ODE rho_DE | diff (A01-ODE)')
    print('-' * 55)
    for z, a in zip(z_test, a_test):
        r_a01 = rho_A01(a)
        r_ode = rho_ODE(a)
        print(str(round(z, 1)) + ' | ' + str(round(r_a01, 6)) +
              ' | ' + str(round(r_ode, 6)) +
              ' | ' + str(round(r_a01 - r_ode, 6)))

    print()

    # What Gamma0 would make ODE = A01 (matching at first order)?
    G0_match = OL0 * (3.0 + Om) / Om
    print('Gamma0 to EXACTLY match A01 linear term: ' + str(round(G0_match, 4)))
    print('Gamma0 in A01 (3*Om): ' + str(round(G0_A01, 4)))
    print('Discrepancy factor: ' + str(round(G0_match / G0_A01, 3)))
    print()

    # Check if amplitude = Om is normalization artifact
    # If we parameterize rho_DE = OL0*(1 + A_amp*(1-a)):
    # Normalization rho_DE(a=1)=OL0 is automatically satisfied for ANY A_amp.
    # So A_amp = Om is NOT required by normalization.
    # A_amp = Om is an empirical fitting result.

    # However: can SQMH ODE generate A_amp ~ Om structurally?
    # From ODE with generic G0:
    # d(omega_de)/da|_{a=1} = 3*OL0 - G0*Om = -OL0*A_amp (to match)
    # => A_amp = G0*Om/OL0 - 3
    # With G0 = 3*Om: A_amp = 3*Om^2/OL0 - 3 = 3*(Om^2 - OL0)/OL0
    # For Om=0.31, OL0=0.685: A_amp = 3*(0.096-0.685)/0.685 = -2.58 !! Negative.

    # This means A01 amplitude Om > 0 CANNOT come from G0=3*Om in linear ODE.
    # The A01 form is a separate phenomenological ansatz.

    A_amp_from_G0_A01 = G0_A01 * Om / OL0 - 3.0
    print('A_amp from G0=3*Om in linear ODE: ' + str(round(A_amp_from_G0_A01, 4)))
    print('Expected A01 A_amp (= Om): ' + str(round(Om, 4)))
    print()
    print('VERDICT: A01 amplitude Om is NOT the linear ODE derivative prediction')
    print('A01 is a phenomenological form rho_DE=OL0*(1+Om*(1-a)) fitted to DESI.')
    print('The Om amplitude encodes the SQMH concept (matter-DE coupling)')
    print('but its exact value is not derived from ODE structure alone.')
    print()

    # However: check if Om comes from ANY exact analytical condition
    # In A01: rho_DE(a->0) = OL0*(1+Om) = OL0 + Om*OL0
    #   = OL0 + Om*(1-Om-OMEGA_R)
    # The "extra" DE at high-z ~ Om*OL0, which is fixed by matter content Om.
    # This IS a structural prediction: DE excess = Om * (DE today)
    # This comes from the SQMH birth-death balance: more matter -> more DE production

    # In SQMH equation: Gamma_0 * n_bar_eq * rho_m is the production term.
    # At equilibrium: prod = decay
    # n_bar_eq * Gamma_0 * rho_m = 3*H*n_bar
    # In matter era: rho_m >> rho_DE, so n_bar grows proportional to rho_m.
    # This gives omega_de ~ rho_m ~ Om*(1+z)^3 at high z.
    # The normalization to OL0 today then sets amplitude ~ Om.
    # This IS a structural prediction from SQMH!

    print('STRUCTURAL PREDICTION CHAIN:')
    print('1. SQMH birth rate: dN/dt ~ Gamma0 * rho_m (matter drives DE production)')
    print('2. In matter era: omega_de tracks Om*(1+z)^3')
    print('3. Normalized to OL0 today: amplitude ~ Om/OL0 * OL0 = Om * (geometry)')
    print('4. Therefore: Om amplitude IS structurally predicted by SQMH birth-death')
    print('   IF Gamma0 is set by SQMH equation (not free-fitted)')
    print()
    print('PARTIAL Q82: The Om amplitude is structurally motivated by SQMH birth-death')
    print('coupling. But exact coefficient = Om (not Om/OL0 or 3*Om^2/OL0) requires')
    print('phenomenological fitting of Gamma0. K82 partially triggered.')

    results = {
        'Om': Om,
        'OL0': OL0,
        'G0_A01': G0_A01,
        'G0_for_exact_A01_match': G0_match,
        'A_amp_from_G0_A01': A_amp_from_G0_A01,
        'A_amp_A01_value': Om,
        'amplitude_is_normalization_artifact': False,
        'amplitude_structurally_motivated': True,
        'amplitude_exact_coefficient_derived': False,
        'verdict': 'K82 PARTIAL: structural motivation exists but exact Om coefficient is phenomenological',
        'k82_triggered': True,
        'q82_triggered': False,
        'q82_partial': True,
    }
    return results


def main():
    results = analytical_amplitude_derivation()

    out_path = os.path.join(_THIS, 'l13_amplitude_results.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print()
    print('Results saved to: ' + out_path)
    return results


if __name__ == '__main__':
    main()
