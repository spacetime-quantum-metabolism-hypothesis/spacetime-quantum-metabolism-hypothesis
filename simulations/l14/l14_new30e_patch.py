# -*- coding: utf-8 -*-
"""Patch: run remaining LG3, HB1, HB2, HB3 and merge into l14_new30e_results.json"""
import os, json, sys
import numpy as np
from scipy.optimize import minimize, curve_fit
from scipy.interpolate import interp1d

os.environ.setdefault('OMP_NUM_THREADS', '1')
np.seterr(all='ignore')

_THIS = os.path.dirname(os.path.abspath(__file__))

c_SI=2.998e8; Mpc_m=3.086e22; OMEGA_R=9.1e-5; rs_drag=147.09
H0_KMS=67.7; H0_SI=H0_KMS*1e3/Mpc_m
DESI_Z=np.array([0.295,0.510,0.706,0.930,1.317,1.491,2.330])
DESI_OBS=np.array([7.93,13.62,16.85,21.71,27.79,30.21,39.71])
DESI_ERR=np.array([0.15,0.17,0.22,0.22,0.55,0.49,0.94])
N_Z=3000; Z_MAX=6.0; Z_ARR=np.linspace(0.0,Z_MAX,N_Z)

def chi2_from_ode(z_arr,ode_arr,Om):
    E2=OMEGA_R*(1+z_arr)**4+Om*(1+z_arr)**3+np.maximum(ode_arr,0)
    E_arr=np.sqrt(np.maximum(E2,1e-15))
    E_interp=interp1d(z_arr,E_arr,kind='cubic',fill_value='extrapolate',bounds_error=False)
    z_int=np.linspace(0,Z_MAX*0.99,5000)
    inv_E=1.0/np.maximum(E_interp(z_int),1e-10)
    dz=np.diff(z_int); cum=np.zeros(len(z_int))
    for i in range(1,len(z_int)):
        cum[i]=cum[i-1]+0.5*(inv_E[i-1]+inv_E[i])*dz[i-1]
    chi_func=interp1d(z_int,cum,kind='cubic',fill_value='extrapolate',bounds_error=False)
    fac=c_SI/(H0_SI*Mpc_m); pred=np.zeros(7)
    DM0=fac*chi_func(DESI_Z[0]); DH0=fac/E_interp(DESI_Z[0])
    DV0=(DESI_Z[0]*DM0**2*DH0)**(1.0/3.0); pred[0]=DV0/rs_drag
    for k,z in enumerate(DESI_Z[1:],1):
        pred[k]=fac*chi_func(z)/rs_drag
    resid=pred-DESI_OBS; c2=float(np.sum((resid/DESI_ERR)**2))
    return c2 if np.isfinite(c2) and c2<1e8 else 1e8

def fit_cpl(z_arr,ode_arr):
    z_fit=np.linspace(0.01,1.5,300); dz=1e-4
    ode_i=interp1d(z_arr,ode_arr,kind='cubic',fill_value='extrapolate',bounds_error=False)
    u=np.array([float(ode_i(z)) for z in z_fit])
    u_p=np.array([float(ode_i(z+dz)) for z in z_fit])
    u_m=np.array([float(ode_i(max(z-dz,1e-5))) for z in z_fit])
    dlnu=(u_p-u_m)/(2*dz*np.maximum(u,1e-20))
    w_z=(1+z_fit)*dlnu/3.0-1.0
    def w_cpl(z,w0,wa): return w0+wa*(1-1/(1+z))
    try:
        popt,_=curve_fit(w_cpl,z_fit,w_z,p0=[-0.95,-0.2],bounds=([-3.0,-10.0],[0.5,5.0]),maxfev=5000)
        return float(popt[0]),float(popt[1])
    except: return float('nan'),float('nan')

def fit_model(make_fn,starts):
    best=(1e9,None)
    for p0 in starts:
        def obj(p):
            Om=p[0]
            if Om<0.28 or Om>0.36: return 1e8
            try:
                arr=make_fn(p)
                if arr is None: return 1e8
                return chi2_from_ode(Z_ARR,arr,Om)
            except: return 1e8
        res=minimize(obj,p0,method='Nelder-Mead',options={'xatol':1e-6,'fatol':1e-6,'maxiter':5000})
        if res.fun<best[0]: best=(res.fun,res.x)
    if best[1] is None: return None
    p=best[1]; Om=float(np.clip(p[0],0.28,0.36))
    arr=make_fn(p)
    if arr is None: return None
    chi2=chi2_from_ode(Z_ARR,arr,Om)
    w0,wa=fit_cpl(Z_ARR,arr)
    return {'chi2':chi2,'w0':w0,'wa':wa,'p':[float(x) for x in p]}

def _E_LCDM(Om,z_arr):
    return np.sqrt(OMEGA_R*(1+z_arr)**4+Om*(1+z_arr)**3+(1-Om-OMEGA_R))

def make_LG3(p):
    Om=p[0]; A=p[1]
    OL0=1.0-Om-OMEGA_R
    if OL0<0.01: return None
    E=_E_LCDM(Om,Z_ARR); x=E-1.0
    return OL0*np.exp(-A*x**2)

def make_HB1(p):
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0<0.01: return None
    E=_E_LCDM(Om,Z_ARR); x=E-1.0
    return OL0*(1.0+A*x*np.exp(-B*np.maximum(x**3,-20)))

def make_HB2(p):
    Om=p[0]; A=max(p[1],0.0); B=max(p[2],0.0)
    OL0=1.0-Om-OMEGA_R
    if OL0<0.01: return None
    v_z=(1+Z_ARR)**2
    f_z=np.exp(-A*(v_z-1.0))*(1.0+B*v_z)
    f_0=np.exp(0.0)*(1.0+B)
    if abs(f_0)<1e-10: return None
    return OL0*f_z/f_0

def make_HB3(p):
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0<0.01: return None
    x_z=Om*(1+Z_ARR)**3; x_0=Om
    f_z=x_z**2/(B**2+x_z**2)**2
    f_0=x_0**2/(B**2+x_0**2)**2
    return OL0*(1.0+A*(f_z-f_0))

PATCH_MODELS=[
    ('LG3-LGGauss', make_LG3, [[0.28,-0.5],[0.30,-1.0],[0.28,0.5],[0.28,-2.0]]),
    ('HB1-N3cubic',  make_HB1, [[0.28,1.0,0.3],[0.30,0.5,0.5],[0.28,2.0,0.1],[0.28,3.0,0.05]]),
    ('HB2-ST1quad',  make_HB2, [[0.28,0.1,0.3],[0.30,0.05,0.5],[0.28,0.2,0.1]]),
    ('HB3-Q3high',   make_HB3, [[0.28,5.0,0.3],[0.30,3.0,0.5],[0.28,10.0,0.1]]),
]

patch={}
for label,fn,starts in PATCH_MODELS:
    r=fit_model(fn,starts)
    if r:
        chi2=r['chi2']; w0=round(r['w0'],3); wa=round(r['wa'],3)
        print(f"{label:<14} chi2={chi2:.3f}  w0={w0}  wa={wa}")
        patch[label]=r
    else:
        print(f"{label:<14} FAILED")

# Merge with existing results
out=os.path.join(_THIS,'l14_new30e_results.json')
existing={}
if os.path.exists(out):
    with open(out) as f: existing=json.load(f)
existing.update(patch)
def _j(v):
    if isinstance(v,(np.floating,np.float64,np.float32)): return float(v)
    if isinstance(v,(np.integer,)): return int(v)
    if isinstance(v,list): return [_j(x) for x in v]
    return v
save={k:{kk:_j(vv) for kk,vv in val.items()} for k,val in existing.items()}
with open(out,'w') as f: json.dump(save,f,indent=2)
print(f"Merged -> {out}")
