# -*- coding: utf-8 -*-
# CODE REVIEW: Bug-v Physics-v Repro-v Rules-v  [2026-04-11]
"""L6: A05 sqrt-relaxation evidence at nlive=800."""
from __future__ import annotations
import json, os, sys, time
os.environ.setdefault('OMP_NUM_THREADS','1'); os.environ.setdefault('MKL_NUM_THREADS','1'); os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np; np.seterr(all='ignore')
_HERE=os.path.dirname(os.path.abspath(__file__)); _L6=os.path.dirname(_HERE); _SIMS=os.path.dirname(_L6)
_L4=os.path.join(_SIMS,'l4'); _L4_ALT=os.path.join(_SIMS,'l4_alt')
for _p in (_SIMS,_L4,_L4_ALT):
    if _p not in sys.path: sys.path.insert(0,_p)
import dynesty
from l4.common import chi2_joint
from l4_alt.runner import ALT, _make_E
_OMEGA_B=0.02237; _LCDM_LOGZ=-843.689
def _jsonify(obj):
    if isinstance(obj,dict): return {k:_jsonify(v) for k,v in obj.items()}
    if isinstance(obj,(list,tuple)): return [_jsonify(v) for v in obj]
    if isinstance(obj,np.ndarray): return obj.tolist()
    if isinstance(obj,np.integer): return int(obj)
    if isinstance(obj,np.floating): return float(obj)
    if isinstance(obj,np.bool_): return bool(obj)
    return obj
_,f_ratio=ALT['A05']; _build=_make_E(f_ratio)
def prior_transform(u): return np.array([0.28+0.08*u[0],0.64+0.07*u[1]])
def log_likelihood(theta):
    Om,h=theta
    omega_c=Om*h*h-_OMEGA_B
    if omega_c<=0: return -1e30
    try:
        E=_build([],Om,h)
        if E is None: return -1e30
        e_hi=float(E(1100.0))
        if not np.isfinite(e_hi) or e_hi<1 or e_hi>1e5: return -1e30
        r=chi2_joint(E,rd=147.09,Omega_m=Om,omega_b=_OMEGA_B,omega_c=omega_c,h=h,H0_km=100.0*h)
        tot=r['total']
        if tot is None or not np.isfinite(tot): return -1e30
        return -0.5*float(tot)
    except Exception: return -1e30
def main():
    t0=time.time()
    print('[L6 A05-hires] nlive=800 seed=42',flush=True)
    rstate=np.random.default_rng(42)
    sampler=dynesty.NestedSampler(log_likelihood,prior_transform,2,nlive=800,rstate=rstate,sample='unif')
    sampler.run_nested(print_progress=False,dlogz=0.05)
    res=sampler.results
    logz=float(res.logz[-1]); logz_err=float(res.logzerr[-1])
    delta_logz=logz-_LCDM_LOGZ; dt=time.time()-t0
    k17=delta_logz>=2.5
    jeffreys='STRONG' if delta_logz>5 else 'substantial' if delta_logz>2.5 else 'weak'
    print('[L6 A05-hires] logZ=%.4f delta=%.4f jeffreys=%s K17=%s dt=%.1fmin'%(logz,delta_logz,jeffreys,k17,dt/60),flush=True)
    result={'ID':'A05','phase':'L6-E-hires','logz':logz,'logz_err':logz_err,'lcdm_logz':_LCDM_LOGZ,'delta_logz':delta_logz,'jeffreys':jeffreys,'k17_pass':k17,'nlive':800,'niter':int(res.niter),'wall_sec':float(dt),'l5_delta_logz':10.581}
    with open(os.path.join(_HERE,'evidence_A05_hires.json'),'w',encoding='utf-8') as f: json.dump(_jsonify(result),f,indent=2)
    print('[L6 A05-hires] done',flush=True)
if __name__=='__main__': main()
