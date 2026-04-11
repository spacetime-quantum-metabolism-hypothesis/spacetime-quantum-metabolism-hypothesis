# -*- coding: utf-8 -*-
"""
L3 unified data loader.

Thin wrapper around the Phase 2/3 likelihood modules to centralise access
for all 11 L2 survivor evaluations. Data sources:

  BAO : DESI DR2 13-point (arXiv:2503.14738) + full cov
        via simulations/desi_data.py  (CobayaSampler-derived)
  SN  : DESY5 (1829 SNe, zHD frame) + systematic cov
        via simulations/phase2/sn_likelihood.py (CobayaSampler/sn_data)
  CMB : compressed (theta*, omega_b, omega_c) + 0.3% theory floor
        via simulations/phase2/compressed_cmb.py (Planck 2018 VI)
  RSD : 8-point fsigma_8 compilation (6dFGS, SDSS MGS, BOSS DR12,
        eBOSS LRG/ELG/QSO)
        via simulations/phase2/rsd_likelihood.py

Everything exposed through a single ``L3Data`` singleton + a single
``chi2_joint(E_func, w_func, **kwargs)`` call so that each candidate script
can do

    from simulations.l3.data_loader import L3_DATA, chi2_joint

    def my_model_E(z): ...

    result = chi2_joint(my_model_E, w_func=my_w, growth='lcdm_like',
                        Omega_m=0.315)

and get the decomposed chi^2 dict back.

No model-specific logic lives here. KILL criteria K1-K8 are applied in
``judge.py`` once chi^2 and ancillary checks are complete.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Callable, Optional

import numpy as np

_THIS = os.path.dirname(os.path.abspath(__file__))
_SIMS = os.path.dirname(_THIS)
_ROOT = os.path.dirname(_SIMS)
for _p in (_SIMS, os.path.join(_SIMS, 'phase2')):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import config  # noqa: E402
import desi_data as dd  # noqa: E402
import desi_fitting as df  # noqa: E402
from phase2 import compressed_cmb as ccmb  # noqa: E402
from phase2 import sn_likelihood as snl  # noqa: E402
from phase2 import rsd_likelihood as rsdl  # noqa: E402


# ---------------------------------------------------------------------------
# Data singleton
# ---------------------------------------------------------------------------

@dataclass
class L3Data:
    # BAO
    bao_points: list
    bao_cov: np.ndarray
    bao_cov_inv: np.ndarray
    # SN
    sn: snl.DESY5SN
    # CMB
    omega_b_fid: float = 0.02237
    omega_c_fid: float = 0.12000
    h_fid: float = 0.6736
    # RSD
    rsd_z: np.ndarray = None
    rsd_fs8: np.ndarray = None
    rsd_sig: np.ndarray = None

    @classmethod
    def build(cls) -> "L3Data":
        return cls(
            bao_points=dd.DESI_DR2,
            bao_cov=dd.DESI_DR2_COV,
            bao_cov_inv=dd.DESI_DR2_COV_INV,
            sn=snl.DESY5SN(),
            rsd_z=rsdl.Z_RSD.copy(),
            rsd_fs8=rsdl.FS8_OBS.copy(),
            rsd_sig=rsdl.FS8_SIG.copy(),
        )


_SINGLETON: Optional[L3Data] = None


def get_data() -> L3Data:
    global _SINGLETON
    if _SINGLETON is None:
        _SINGLETON = L3Data.build()
    return _SINGLETON


# ---------------------------------------------------------------------------
# chi^2 helpers
# ---------------------------------------------------------------------------

def _chi2_bao(E_func: Callable[[float], float], rd: float = 147.09) -> float:
    """BAO chi² via the existing desi_fitting.chi2(E_func, rd) helper.
    Uses DESI DR2 13-point + full 13x13 covariance."""
    return float(df.chi2(E_func, rd))


def _chi2_sn(E_func: Callable[[float], float], H0_km: float = 67.36) -> float:
    """DESY5 SN chi² with marginalised absolute mag."""
    d = get_data()
    return float(d.sn.chi2(E_func, H0_km=H0_km))


def _chi2_cmb(E_func: Callable[[float], float],
              omega_b: float = 0.02237,
              omega_c: float = 0.12000,
              h: float = 0.6736) -> float:
    """Compressed CMB chi² against Planck 2018 TT,TE,EE+lowE."""
    return float(ccmb.chi2_compressed_cmb(omega_b, omega_c, h, E_func))


def _chi2_rsd_lcdm(Om_0: float) -> float:
    """Fallback RSD chi² using LCDM growth with given Omega_m. Conservative
    approximation for models without explicit modified-gravity growth."""
    return float(rsdl.chi2_lcdm(Om_0))


def _chi2_rsd_custom(z_arr: np.ndarray, fs8_th: np.ndarray) -> float:
    """RSD chi² given a model-supplied fs8 prediction at the 8 L3 redshifts."""
    d = get_data()
    assert np.allclose(z_arr, d.rsd_z), "rsd_z mismatch"
    delta = d.rsd_fs8 - fs8_th
    return float(np.sum((delta / d.rsd_sig)**2))


def chi2_joint(
    E_func: Callable[[float], float],
    *,
    rd: float = 147.09,
    Omega_m: float = 0.315,
    omega_b: float = 0.02237,
    omega_c: float = 0.12000,
    h: float = 0.6736,
    H0_km: float = 67.36,
    fs8_theory: Optional[np.ndarray] = None,
) -> dict:
    """Full BAO+SN+CMB+RSD joint chi² decomposition.

    Returns dict with keys ``bao``, ``sn``, ``cmb``, ``rsd``, ``total``.
    If ``fs8_theory`` is None, LCDM growth at ``Omega_m`` is used for RSD.
    """
    c_bao = _chi2_bao(E_func, rd=rd)
    c_sn = _chi2_sn(E_func, H0_km=H0_km)
    c_cmb = _chi2_cmb(E_func, omega_b=omega_b, omega_c=omega_c, h=h)
    if fs8_theory is None:
        c_rsd = _chi2_rsd_lcdm(Omega_m)
    else:
        c_rsd = _chi2_rsd_custom(get_data().rsd_z, np.asarray(fs8_theory))
    return {
        'bao': c_bao,
        'sn': c_sn,
        'cmb': c_cmb,
        'rsd': c_rsd,
        'total': c_bao + c_sn + c_cmb + c_rsd,
    }


if __name__ == "__main__":
    import json
    print("L3 data loader smoke test")
    d = get_data()
    print(f"  BAO points : {len(d.bao_points)}")
    print(f"  SN         : {d.sn.N}")
    print(f"  RSD        : {len(d.rsd_z)}")

    Om = 0.3153
    Or = config.Omega_r
    OL = 1.0 - Om - Or

    def E_lcdm(z):
        return np.sqrt(Or * (1 + z)**4 + Om * (1 + z)**3 + OL)

    res = chi2_joint(E_lcdm, Omega_m=Om)
    print("LCDM reference chi2 decomposition:")
    print(json.dumps(res, indent=2))
