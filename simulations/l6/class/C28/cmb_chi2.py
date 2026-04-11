# -*- coding: utf-8 -*-
# CODE REVIEW: Bug-v Physics-v Repro-v Rules-v  [2026-04-11]
"""L6-G3: CMB chi2 for C28 via chi2_joint compressed Planck likelihood."""
from __future__ import annotations
import json, os, sys, time
os.environ.setdefault('OMP_NUM_THREADS','1'); os.environ.setdefault('MKL_NUM_THREADS','1'); os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np; np.seterr(all='ignore')
_HERE=os.path.dirname(os.path.abspath(__file__)); _L6=os.path.dirname(os.path.dirname(_HERE)); _SIMS=os.path.dirname(_L6)
_L4=os.path.join(_SIMS,'l4'); _C28=os.path.join(_L4,'C28')
for _p in (_SIMS,_L4,_C28):
    if _p not in sys.path: sys.path.insert(0,_p)
from l4.common import chi2_joint, E_lcdm
from l4.C28.background import build_E as _build_E_c28
_OMEGA_B=0.02237
# C28 L4 MAP / MCMC posterior
_OM=0.3081; _H=0.6789; _G0=0.0025; _BS=0.4786; _AT=2.1708
def _jsonify(obj):
    if isinstance(obj,dict): return {k:_jsonify(v) for k,v in obj.items()}
    if isinstance(obj,(list,tuple)): return [_jsonify(v) for v in obj]
    if isinstance(obj,np.ndarray): return obj.tolist()
    if isinstance(obj,np.integer): return int(obj)
    if isinstance(obj,np.floating): return float(obj)
    if isinstance(obj,np.bool_): return bool(obj)
    return obj
def main():
    print('[L6-G3 C28] CMB chi2 via chi2_joint',flush=True)
    Om,h=_OM,_H; omega_c=Om*h*h-_OMEGA_B
    try:
        E=_build_E_c28([_G0,_BS,_AT],Om,h)
        r=chi2_joint(E,rd=147.09,Omega_m=Om,omega_b=_OMEGA_B,omega_c=omega_c,h=h,H0_km=100.0*h)
        cmb_c28=r.get('cmb',float('nan'))
    except Exception as e:
        print('[L6-G3 C28] ERROR: %s'%e,flush=True); cmb_c28=float('nan')
    E_l=E_lcdm(Om,h)
    r_l=chi2_joint(E_l,rd=147.09,Omega_m=Om,omega_b=_OMEGA_B,omega_c=omega_c,h=h,H0_km=100.0*h)
    cmb_lcdm=r_l.get('cmb',float('nan'))
    delta=cmb_c28-cmb_lcdm if (not (cmb_c28!=cmb_c28 or cmb_lcdm!=cmb_lcdm)) else float('nan')
    k19=bool(delta<=6.0) if not (delta!=delta) else None
    print('[L6-G3 C28] CMB chi2 LCDM=%.4f C28=%.4f delta=%.4f K19=%s'%(cmb_lcdm,cmb_c28,delta,k19),flush=True)
    result={'ID':'C28','phase':'L6-G3','cmb_chi2':{'LCDM':float(cmb_lcdm),'C28':float(cmb_c28),'delta':float(delta)},'K19_provisional_pass':k19,'WARNING':'compressed Planck only, hi_class not installed'}
    out=os.path.join(_HERE,'cmb_chi2.json')
    with open(out,'w',encoding='utf-8') as f: json.dump(_jsonify(result),f,indent=2)
    print('[L6-G3 C28] wrote %s'%out,flush=True)
if __name__=='__main__': main()
