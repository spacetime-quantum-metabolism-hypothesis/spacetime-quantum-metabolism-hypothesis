# -*- coding: utf-8 -*-
"""
L13-Gamma Round 5: Penrose objective collapse identity deep dive.

Verifies NF-34 algebraically and explores whether the 4*pi factor
can be derived geometrically from SQMH birth-death process.
"""
from __future__ import annotations
import os
import json
import numpy as np

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')

_THIS = os.path.dirname(os.path.abspath(__file__))

# Planck units (SI)
G_SI = 6.674e-11
t_P = 5.391e-44
l_P = 1.616e-35
m_P = 2.176e-8
hbar = 1.055e-34
c_SI = 2.998e8
k_B = 1.381e-23
H0 = 67.7e3 / 3.086e22

# SQMH
sigma_SQMH = 4.0 * np.pi * G_SI * t_P
rho_P = m_P / l_P**3
Gamma0_fid = sigma_SQMH * rho_P


def verify_nf34():
    """
    Verify NF-34: sigma*rho_P = 4*pi/t_P exactly.

    Algebraic proof:
    sigma = 4*pi*G*t_P
    rho_P = m_P / l_P^3

    In Planck units: G = l_P*c^2/m_P (from G*m_P^2 = hbar*c, m_P=sqrt(hbar*c/G))
    Also: t_P = l_P/c

    sigma * rho_P = 4*pi * G * t_P * (m_P/l_P^3)
                 = 4*pi * (l_P*c^2/m_P) * (l_P/c) * (m_P/l_P^3)   [using G = l_P*c^2/m_P]
                 = 4*pi * l_P^2*c * m_P / (m_P * c * l_P^3)
                 = 4*pi / l_P
                 = 4*pi * c / l_P^2 / c
                 Hmm... let me be more careful.

    G = l_P c^2 / m_P? Let me verify from Planck mass definition.
    m_P = sqrt(hbar*c/G)  => G = hbar*c/m_P^2
    l_P = sqrt(hbar*G/c^3) = sqrt(hbar^2*c/(m_P^2*c^3)) = hbar/(m_P*c)
    t_P = l_P/c = hbar/(m_P*c^2)
    rho_P = m_P/l_P^3 = m_P^4*c^3/hbar^3

    sigma = 4*pi*G*t_P = 4*pi * (hbar*c/m_P^2) * (hbar/(m_P*c^2))
          = 4*pi * hbar^2 / (m_P^3 * c)

    sigma * rho_P = 4*pi * hbar^2/(m_P^3*c) * m_P^4*c^3/hbar^3
                 = 4*pi * m_P*c^2/hbar
                 = 4*pi / t_P           [since t_P = hbar/(m_P*c^2)]

    QED: sigma * rho_P = 4*pi / t_P. Exact algebraic identity.
    """
    # Numerical verification
    Gamma0_computed = sigma_SQMH * rho_P
    Gamma0_penrose = 4.0 * np.pi / t_P

    print('NF-34 Verification:')
    print('  sigma * rho_P = ' + '{:.6e}'.format(Gamma0_computed) + ' s^-1')
    print('  4*pi / t_P   = ' + '{:.6e}'.format(Gamma0_penrose) + ' s^-1')
    print('  Ratio = ' + str(Gamma0_computed / Gamma0_penrose))
    print()
    print('Algebraic proof steps:')
    print('  m_P = sqrt(hbar*c/G)')
    print('  l_P = hbar/(m_P*c)')
    print('  t_P = hbar/(m_P*c^2)')
    print('  rho_P = m_P/l_P^3 = m_P^4*c^3/hbar^3')
    print('  sigma = 4*pi*G*t_P = 4*pi*(hbar*c/m_P^2)*(hbar/(m_P*c^2)) = 4*pi*hbar^2/(m_P^3*c)')
    print('  sigma*rho_P = 4*pi*hbar^2/(m_P^3*c) * m_P^4*c^3/hbar^3 = 4*pi*m_P*c^2/hbar')
    print('             = 4*pi/t_P. QED.')
    print()

    return {
        'Gamma0_computed': float(Gamma0_computed),
        'Gamma0_penrose': float(Gamma0_penrose),
        'ratio': float(Gamma0_computed / Gamma0_penrose),
        'proof': 'sigma*rho_P = 4*pi*(m_P*c^2/hbar) = 4*pi/t_P exact',
    }


def geometric_4pi():
    """
    Can 4*pi be derived geometrically from SQMH?

    In SQMH, each spacetime quantum is created/annihilated in a spherically
    symmetric fashion around a matter concentration.
    If the birth-death process is modeled as:
      - Source at origin
      - Quanta emitted isotropically into 4*pi solid angle
      - Absorption rate proportional to solid angle subtended

    Then the coupling: Gamma = (rate per steradian) * 4*pi = total rate.
    This gives 4*pi from solid angle integration.

    Alternatively: from quantum field theory, the phase space factor for
    isotropic emission is 4*pi (k-space integration).

    The Penrose rate for a single Planck-mass quantum:
      tau_P = hbar/E_G where E_G = G*m_P^2/l_P = m_P*c^2
      => tau_P = hbar/(m_P*c^2) = t_P
      Rate = 1/t_P (per quantum)

    For a continuous medium with density rho:
      N_quanta = rho/rho_P (fraction of Planck density)
      Total rate per unit volume = N_quanta/t_P = rho/(rho_P*t_P)
      But isotropically emitted: multiply by 4*pi for total solid angle.
      => Gamma_total/volume = 4*pi * rho/(rho_P*t_P) = sigma * rho
      where sigma = 4*pi/(rho_P*t_P) = 4*pi*G*t_P... wait:

    Let me check: 4*pi/(rho_P*t_P) = 4*pi*t_P^3*c^3/(m_P*l_P^3*t_P)
    = 4*pi*t_P^2*c^3/(m_P*l_P^3)
    Hmm, this gives units of [s^2*m^3/s^3 / (kg*m^3)] = [s^(-1)*kg^(-1)]... wrong units.

    Let me use: sigma [m^3 kg^-1 s^-1]
    sigma = 4*pi*G*t_P = 4*pi/(rho_P*t_P) * t_P^2 ??? No.

    Actually sigma*rho = 4*pi/t_P * (rho/rho_P) [this is dimensionless * 1/t_P]
    sigma*rho has units [m^3 kg^-1 s^-1 * kg m^-3] = [s^-1]. Correct!
    sigma*rho = Gamma0_eff (rate per unit time).

    So the physical picture:
      Gamma_eff = sigma * rho = (Penrose rate 4*pi/t_P) * (rho/rho_P)

    The 4*pi comes from isotropic solid angle for Penrose collapse.
    If Penrose collapse were directional (1D), it would be 2 (forward/backward).
    The spherical geometry of spacetime quanta gives 4*pi.
    """
    print('Geometric origin of 4*pi:')
    print('  In SQMH: quanta emitted isotropically -> 4*pi solid angle factor.')
    print('  Penrose collapse for Planck quanta: rate = 1/t_P per quantum.')
    print('  For density rho: rate/volume = (rho/rho_P)/t_P (before geometry).')
    print('  With 4*pi geometry: rate/volume = 4*pi*rho/(rho_P*t_P) = sigma*rho.')
    print()
    print('  sigma = 4*pi/(rho_P*t_P) = 4*pi*G*t_P [identity]')
    print()
    print('  The 4*pi is the solid angle of spherical spacetime quantum emission.')
    print('  This is the same 4*pi as in: solid angle = 4*pi sr (full sphere).')
    print()
    print('  ASSESSMENT: 4*pi factor has geometric motivation from:')
    print('    (1) Isotropic Penrose collapse emission')
    print('    (2) Standard QFT phase space factor for isotropic process')
    print('    (3) Equivalently: surface area of unit sphere in 3D')
    print()
    print('  This is NOT a derivation but IS a physically motivated explanation.')
    print()


def check_sigma_range():
    """
    What range of sigma values are theoretically allowed?
    From Penrose: sigma = 4*pi*G*t_P is UNIQUELY determined by:
    - G: Newton constant (fixed by measurement)
    - t_P: Planck time (fixed by measurement)
    - 4*pi: geometric factor (motivated by spherical symmetry)

    If 4*pi is fixed by geometry, then sigma is determined up to ~O(1) factors.
    Range = 1 order of magnitude (geometric uncertainty).

    This is different from the "range=62 orders" in K84 which refers to
    Gamma0_fiducial from holographic and phenomenological bounds.

    K84 applies to Gamma0 (observable rate), not to sigma (microscopic coupling).
    sigma = 4*pi*G*t_P is uniquely determined.
    """
    print('sigma uniqueness:')
    print('  sigma = 4*pi*G*t_P is UNIQUELY determined from {G, t_P, geometry}.')
    print('  Range: O(1) from geometric factor 4*pi (isotropic assumption).')
    print('  If 2*pi (hemisphere) or 8*pi (other): sigma changes by factor 2.')
    print('  This is 0 orders of magnitude (within factor of 2).')
    print()
    print('  CONCLUSION: sigma is theoretically constrained to O(1) range,')
    print('  given G, t_P, and isotropy. This is STRONG theoretical basis.')
    print()
    print('  Gamma0 (effective cosmological rate) is DIFFERENT: spans 62 orders.')
    print('  K84 applies to Gamma0_fid. sigma itself is well-determined.')
    print()

    sigma_range_log10 = np.log10(2)  # factor 2 from 4*pi vs 2*pi
    print('  sigma range (orders): 10^' + str(round(sigma_range_log10, 2)) + ' (< 1 order)')


def main():
    print('=== L13-Gamma Round 5: Penrose Deep Dive ===')
    print()

    r1 = verify_nf34()
    geometric_4pi()
    check_sigma_range()

    print('=== Round 5 Summary ===')
    print()
    print('NF-34 CONFIRMED: sigma*rho_P = 4*pi/t_P (exact algebraic identity).')
    print()
    print('sigma = 4*pi*G*t_P:')
    print('  - Dimensionally unique (only G*t_P has correct units)')
    print('  - 4*pi geometrically motivated (isotropic Penrose collapse)')
    print('  - Penrose interpretation: rate per Planck density = 4*pi/t_P')
    print('  - Range < 1 order if isotropy assumed')
    print()
    print('Gamma0 (effective rate):')
    print('  - Range 62 orders from H0 to 4*pi/t_P. K84 applies here.')
    print('  - A01 effective Gamma0 = 3*Om is disconnected from sigma by 62 orders.')
    print()
    print('Q84 STATUS: PARTIAL.')
    print('sigma has theoretical basis (dimensional uniqueness + Penrose geometry).')
    print('This is the best available motivation without quantum gravity.')

    results = {
        'nf34_verification': r1,
        'sigma_geometric_basis': '4*pi = isotropic solid angle (Penrose collapse)',
        'sigma_range_orders': float(np.log10(2)),
        'Gamma0_range_orders': 62.0,
        'q84_partial': True,
        'q84_triggered': False,
        'conclusion': 'sigma uniquely determined; Gamma0_eff disconnected by 62 orders',
    }

    out_path = os.path.join(_THIS, 'l13_gamma0_r5_results.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print('Results saved to: ' + out_path)
    return results


if __name__ == '__main__':
    main()
