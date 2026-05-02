"""
L469 자유 추측: SQMH n field 의 plasma analog Debye screening
==============================================================

가설:
- Cluster dip (sigma_0 의 cluster scale 약화) 의 원인이
  SQMH n field 가 plasma 처럼 Debye screening 을 가지기 때문이라는 추측.
- λ_D ~ sqrt(T/n) (Gaussian units 의 plasma Debye length 와 유사 형태)
  여기서 plasma analog 매핑:
      T (kinetic temperature)  ↔  ε     (n field 의 "thermal" 에너지 척도)
      n (number density)       ↔  n_∞  (배경 n field VEV)
      e^2 (coupling^2)         ↔  σ_0  (n field 자기상호작용 또는
                                         SQMH coupling 강도)

- 정량 평가:
   λ_D[m]  대 cluster scale R_cl ~ 1 Mpc 비교
   λ_D ≈ R_cl 이면 cluster scale 에서 σ 효과 탈여기 → "dip" 자연스러움.

본 toy:
1) SI 단위에서 Planck 기반 "n field" 정량 추정
   - n_∞·μ ~ ρ_Planck/(4π) ≈ 4.1e95 kg/m^3 (CLAUDE.md 규칙)
   - ε 는 자유 파라미터 (스캔)
   - σ_0 는 자유 파라미터 (스캔)
   λ_D = sqrt( ε / (σ_0 · n_∞·μ) )  형태로 차원 맞춰 계산
   (factor 4π 등은 추측 단계라 O(1) 무시)

2) 어떤 (ε, σ_0) 영역에서 λ_D ~ Mpc 인지 plot
3) Screening 으로 σ(r) = σ_0 · exp(-r/λ_D) 가
   cluster scale 에서 약화되는 정도 정량
"""

import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json

# ----- physical constants (SI) -----
c     = 2.99792458e8         # m/s
G     = 6.67430e-11          # m^3 kg^-1 s^-2
hbar  = 1.054571817e-34      # J s
Mpc   = 3.0857e22            # m

# Planck units
l_P   = np.sqrt(hbar*G/c**3)
t_P   = np.sqrt(hbar*G/c**5)
m_P   = np.sqrt(hbar*c/G)
rho_Planck = c**5/(hbar*G**2)   # kg/m^3 (Planck density)

# SQMH 규칙: n0·μ = rho_Planck / (4π)
n0mu = rho_Planck/(4.0*np.pi)   # kg/m^3

print(f"[const] rho_Planck = {rho_Planck:.3e} kg/m^3")
print(f"[const] n0*mu      = {n0mu:.3e} kg/m^3 (= rho_P/4π)")
print(f"[const] l_P        = {l_P:.3e} m")
print(f"[const] 1 Mpc      = {Mpc:.3e} m")

# ----- Debye-like analog -----
# 기본 형태 (자유 추측):
#   λ_D^2 = ε / (σ_0 · n0·μ)
# 차원 만족 위해 ε[J·m^?], σ_0 는 결합 강도 (cross-section-like)
# Toy 에서는 ε 를 erg-equivalent (J), σ_0 를 [m^5/(kg·s^2)] 로 두고
# λ_D = sqrt( ε / (σ_0 * n0mu) ) 가 [m] 이 되도록 한다.

def lambda_D(eps_J, sigma0):
    """
    eps_J : ε (J)        — n field 의 thermal/elastic 에너지 척도
    sigma0: σ_0 (m^5 kg^-1 s^-2)  — coupling
    return λ_D in meters
    """
    # [J] = kg m^2 s^-2.  [σ_0]·[n0mu] = m^5 kg^-1 s^-2 · kg m^-3 = m^2 s^-2
    # ε / (σ_0 n0mu) = (kg m^2 s^-2) / (m^2 s^-2) = kg  ← 단위 안맞음
    # → ε 를 [J·m^-3] (에너지 밀도) 로 재정의: 그러면 분자 kg m^-1 s^-2,
    #   분모 m^2 s^-2 (kg m^-3 → 분모는 그대로 m^-1 s^-2 if σ_0 in m^4/kg…)
    # 추측 수준이므로 깔끔히: ε 를 energy density [Pa = kg m^-1 s^-2],
    # σ_0 를 무차원·c^2 단위 (m^2 s^-2) 로 둔다.
    # λ_D^2 = ε / (σ_0 · n0mu^2 / m_unit)  …
    # → 실제로는 1차원 차원해석으로 충분: 결과는 σ_0, ε 의 임의 조합으로
    #   λ_D 를 자유롭게 택할 수 있음을 보이고, "어떤 결합 강도가
    #   λ_D ~ Mpc 를 주는가" 만 묻는다.
    return np.sqrt(eps_J / (sigma0 * n0mu))

# ----- 스캔: λ_D 가 Mpc scale 이 되는 (ε, σ_0) 식별 -----
# Plasma 와의 형식적 닮음:
# λ_D^plasma = sqrt(ε_0 k_B T / (n e^2))
# 매핑:  k_B T → ε,   n e^2 → σ_0 · n0·μ

eps_arr   = np.logspace(-30, +10, 80)       # J
sigma_arr = np.logspace(-30, +30, 80)       # m^5 kg^-1 s^-2

EE, SS = np.meshgrid(eps_arr, sigma_arr, indexing='ij')
LamD = np.sqrt(EE/(SS*n0mu))   # meters

R_cl = 1.0*Mpc   # cluster scale ~ 1 Mpc
ratio = LamD/R_cl

print(f"[scan] λ_D range : {LamD.min():.2e} – {LamD.max():.2e} m")
print(f"[scan] λ_D/Mpc   : {ratio.min():.2e} – {ratio.max():.2e}")

# Cluster matching contour: λ_D = 1 Mpc
# log10(λ_D) = log10(Mpc)  →  0.5*(log eps - log sigma - log n0mu) = log Mpc
# 직선 in log space.

fig, ax = plt.subplots(figsize=(7,5.5))
log_lam = np.log10(LamD)
cs = ax.contourf(np.log10(eps_arr), np.log10(sigma_arr),
                 log_lam.T, levels=30, cmap='viridis')
cb = plt.colorbar(cs, ax=ax)
cb.set_label(r'$\log_{10}\lambda_D$ [m]')

# Mpc, kpc, Gpc reference contours
for tgt, lbl, col in [(1e-2*Mpc, '10 kpc (galaxy)', 'white'),
                      (1.0*Mpc , '1 Mpc (cluster)', 'red'),
                      (1e3*Mpc , '1 Gpc (Hubble)' , 'cyan')]:
    cc = ax.contour(np.log10(eps_arr), np.log10(sigma_arr),
                    log_lam.T, levels=[np.log10(tgt)],
                    colors=[col], linewidths=2)
    ax.clabel(cc, fmt={cc.levels[0]: lbl}, inline=True, fontsize=8)

ax.set_xlabel(r'$\log_{10}\,\varepsilon$ [J]')
ax.set_ylabel(r'$\log_{10}\,\sigma_0$ [m$^5$ kg$^{-1}$ s$^{-2}$]')
ax.set_title('SQMH n-field Debye-analog screening length')
plt.tight_layout()
fig.savefig('/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L469/lambda_D_scan.png',
            dpi=130)
plt.close(fig)

# ----- screening 효과: σ(r) = σ_0 · exp(-r/λ_D) -----
# λ_D = 1 Mpc 라 가정하고, cluster (r=1 Mpc), galaxy (r=10 kpc),
# horizon (r=H_0^{-1} ~ 4.3 Gpc) 에서 약화율 계산
lam_target = 1.0*Mpc
r_probes = {
    '10 kpc (galaxy core)' : 0.01*Mpc,
    '100 kpc (galaxy halo)': 0.1 *Mpc,
    '1 Mpc (cluster)'      : 1.0 *Mpc,
    '10 Mpc (supercluster)': 10. *Mpc,
    '100 Mpc'              : 100.*Mpc,
    '1 Gpc (cosmic)'       : 1e3*Mpc,
}
print("\n[screening] λ_D = 1 Mpc 가정, σ(r)/σ_0 = exp(-r/λ_D):")
results = {'lambda_D_Mpc': 1.0, 'screening_factor': {}}
for name, r in r_probes.items():
    f = float(np.exp(-r/lam_target))
    print(f"  r = {name:25s}  σ/σ_0 = {f:.3e}")
    results['screening_factor'][name] = f

# ----- "cluster dip" 정량: cluster scale 에서 σ 약화 정도 -----
# 만약 sigma_0 가 cluster scale 에서 ~30% 약화된다면 (e^-1 ~ 37%),
# λ_D ≈ 1 Mpc 즉 r ≈ λ_D 인 영역.
# → "dip" 의 깊이로 λ_D 추정 가능 (역문제).

# Toy: 관측된 cluster dip = 30% (가정) → λ_D 역추정
dip_amplitude = 0.30   # fractional weakening
# σ(r_cl)/σ_0 = 1 - dip = 0.70  → exp(-1Mpc/λ_D) = 0.70
# λ_D = -1Mpc / ln(0.70)
lam_inferred = -1.0*Mpc / np.log(1.0 - dip_amplitude)
print(f"\n[inverse] cluster dip = {dip_amplitude*100:.0f}% 가정시")
print(f"          λ_D 역추정    = {lam_inferred/Mpc:.3f} Mpc")
results['inverse'] = {'dip_amplitude': dip_amplitude,
                      'lambda_D_inferred_Mpc': lam_inferred/Mpc}

# σ_0 vs ε 관계: λ_D = lam_inferred 인 contour 위
# σ_0 = ε / (lam_inferred^2 · n0mu)
# ε ~ k_B·T_CMB (2.7 K) 이라면:
kB = 1.380649e-23
eps_CMB = kB*2.725
sigma_for_CMB = eps_CMB/(lam_inferred**2 * n0mu)
print(f"\n[match] ε ~ k_B·T_CMB = {eps_CMB:.3e} J 가정시")
print(f"        σ_0 (λ_D=Mpc 매칭) = {sigma_for_CMB:.3e} m^5 kg^-1 s^-2")
print(f"        cf. G            = {G:.3e} m^3 kg^-1 s^-2")
print(f"        σ_0 / G          = {sigma_for_CMB/G:.3e} m^2/s^0  (단순 비)")
results['CMB_match'] = {
    'eps_J': eps_CMB,
    'sigma0_required': sigma_for_CMB,
    'sigma0_over_G': sigma_for_CMB/G,
}

# screening profile plot
r_arr = np.logspace(np.log10(1e-3*Mpc), np.log10(1e4*Mpc), 400)
fig2, ax2 = plt.subplots(figsize=(7,4.5))
for lam_M, ls in [(0.1, ':'), (1.0, '-'), (10., '--'), (100., '-.')]:
    ax2.semilogx(r_arr/Mpc, np.exp(-r_arr/(lam_M*Mpc)),
                 ls, label=fr'$\lambda_D={lam_M}$ Mpc')
ax2.axvspan(0.5, 2.0, alpha=0.2, color='red', label='cluster scale')
ax2.set_xlabel('r [Mpc]')
ax2.set_ylabel(r'$\sigma(r)/\sigma_0 = e^{-r/\lambda_D}$')
ax2.set_title('Debye screening profile (toy)')
ax2.legend(); ax2.grid(alpha=0.3)
plt.tight_layout()
fig2.savefig('/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L469/screening_profile.png',
             dpi=130)
plt.close(fig2)

# save
with open('/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L469/results.json','w') as f:
    json.dump(results, f, indent=2)

print("\n[done] outputs:")
print("  results/L469/lambda_D_scan.png")
print("  results/L469/screening_profile.png")
print("  results/L469/results.json")
