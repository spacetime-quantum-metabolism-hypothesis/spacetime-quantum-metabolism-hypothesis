"""L381 — Cosmic shear xi_+(theta=10') SQT vs LCDM — Euclid/LSST sensitivity.

Independent computation. L286 follow-up.

Approach:
  - Limber-approx convergence power C_l = integral dz [W(z)^2/chi^2/H(z)] P_m(k=l/chi, z)
  - SQT: dark-only structural (mu_eff=1), background-only effect modeled as
         effective S_8 shift +1.14% (L242/L286 confirmed). Same linear P_m shape,
         normalisation rescaled by (sigma_8_SQT/sigma_8_LCDM)^2 in C_l.
  - xi_+(theta) = (1/2 pi) integral dl l C_l J_0(l theta)
  - Linear matter P(k) via Eisenstein-Hu 1998 transfer (no wiggle is OK at 10'),
    plus halofit Smith 2003 nonlinear extension for theta=10' (l~700 main contribution).
  - Gaussian covariance for xi_+ at single theta bin: shape noise + cosmic variance.
  - Survey specs: Euclid (15000 deg^2, n_eff=30/arcmin^2, sigma_e=0.26),
                  LSST Y10 (18000 deg^2, n_eff=27/arcmin^2, sigma_e=0.26).
  - n(z): Euclid Smail (alpha=2, beta=1.5, z0=0.64); LSST Y10 (z0=0.28, a=0.9, b=2).
"""
import os, json, math
import numpy as np
from scipy.integrate import quad, simpson
from scipy.special import j0
from scipy.interpolate import interp1d

OUT_DIR = "/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L381"
os.makedirs(OUT_DIR, exist_ok=True)

# ----------------------------- cosmology -----------------------------------
H0_KMS = 67.4  # km/s/Mpc
h = H0_KMS / 100.0
Om = 0.315
Ob = 0.0493
ns = 0.965
sigma8_LCDM = 0.811
S8_LCDM = sigma8_LCDM * math.sqrt(Om / 0.3)

# L286/L242 SQT: ΔS_8 = +1.14% (worsens tension)
DELTA_S8_PCT = 1.14
S8_SQT = S8_LCDM * (1.0 + DELTA_S8_PCT / 100.0)
sigma8_SQT = S8_SQT / math.sqrt(Om / 0.3)
# In linear theory (mu_eff=1) full power scales as (sigma_8)^2.
PK_AMP_RATIO = (sigma8_SQT / sigma8_LCDM) ** 2  # ~1.023

C_KMS = 299792.458  # km/s
H0_INV_MPC = H0_KMS / C_KMS  # 1/Mpc

# ----------------------- background distances ------------------------------
def E_LCDM(z):
    return math.sqrt(Om * (1 + z) ** 3 + (1 - Om))

def chi_of_z(z):
    # comoving distance in Mpc (flat)
    val, _ = quad(lambda zp: 1.0 / E_LCDM(zp), 0.0, z, epsabs=1e-8, epsrel=1e-7)
    return (C_KMS / H0_KMS) * val

# Tabulate
Z_TAB = np.linspace(1e-4, 4.0, 400)
CHI_TAB = np.array([chi_of_z(z) for z in Z_TAB])
chi_interp = interp1d(Z_TAB, CHI_TAB, kind="cubic", bounds_error=False, fill_value="extrapolate")
z_of_chi = interp1d(CHI_TAB, Z_TAB, kind="cubic", bounds_error=False, fill_value="extrapolate")
CHI_MAX = CHI_TAB[-1]

# --------------------- Eisenstein-Hu 1998 (no wiggle) ----------------------
def eh98_nowiggle_T(k):
    """k in h/Mpc -> transfer function (Eisenstein-Hu 1998 no-wiggle)."""
    # Use physical params
    om0h2 = Om * h * h
    obh2 = Ob * h * h
    f_b = Ob / Om
    Tcmb = 2.7255
    theta = Tcmb / 2.7
    s = 44.5 * math.log(9.83 / om0h2) / math.sqrt(1.0 + 10.0 * obh2 ** 0.75)  # Mpc
    alpha_gamma = 1 - 0.328 * math.log(431.0 * om0h2) * f_b + 0.38 * math.log(22.3 * om0h2) * f_b ** 2
    # k in 1/Mpc for formula
    k_mpc = k * h
    gamma_eff = Om * h * (alpha_gamma + (1.0 - alpha_gamma) / (1.0 + (0.43 * k_mpc * s) ** 4))
    q = k_mpc * theta * theta / gamma_eff  # k in 1/Mpc, gamma_eff in h/Mpc -> dimensional careful
    # Standard form: q = k(h/Mpc) * theta^2 / gamma_eff
    # gamma_eff is dimensionless * h here; use k in h/Mpc directly:
    q = k * theta * theta / (gamma_eff)
    L = math.log(2 * math.e + 1.8 * q)
    Cq = 14.2 + 731.0 / (1.0 + 62.5 * q)
    return L / (L + Cq * q * q)

def Pk_lin_unnorm(k):
    """Linear matter P(k) [unnormalised], k in h/Mpc."""
    T = eh98_nowiggle_T(k)
    return (k ** ns) * T * T

# Normalise to sigma_8
def sigma_R_unnorm(R):
    def integrand(lnk):
        k = math.exp(lnk)
        x = k * R
        if x < 1e-3:
            W = 1.0 - x * x / 10.0
        else:
            W = 3.0 * (math.sin(x) - x * math.cos(x)) / (x ** 3)
        return k * k * k * Pk_lin_unnorm(k) * W * W / (2 * math.pi ** 2)
    val, _ = quad(integrand, math.log(1e-4), math.log(50.0), epsabs=0, epsrel=1e-5, limit=200)
    return math.sqrt(val)

SIG8_UNNORM = sigma_R_unnorm(8.0)
PK_NORM = (sigma8_LCDM / SIG8_UNNORM) ** 2

def Pk_lin_LCDM(k, z):
    """Linear P_m(k,z) [Mpc/h]^3, k in h/Mpc."""
    # growth factor (LCDM, normalised D(z=0)=1)
    D = growth_D(z)
    return PK_NORM * Pk_lin_unnorm(k) * D * D

# ------------------------- growth factor (LCDM) -----------------------------
def growth_D_unnorm(z):
    a = 1.0 / (1.0 + z)
    def integrand(ap):
        Ez = math.sqrt(Om / ap ** 3 + (1 - Om))
        return 1.0 / (ap * Ez) ** 3
    val, _ = quad(integrand, 1e-6, a, epsabs=0, epsrel=1e-7)
    Ea = math.sqrt(Om / a ** 3 + (1 - Om))
    return 2.5 * Om * Ea * val

D0_NORM = growth_D_unnorm(0.0)
def growth_D(z):
    return growth_D_unnorm(z) / D0_NORM

# ------------------------- halofit (Smith 2003) -----------------------------
def halofit_Pk(k_arr, z):
    """Smith 2003 halofit nonlinear P(k,z). k_arr in h/Mpc."""
    # Find k_sigma (nonlinear scale): sigma^2(R=1/k_sigma; z) = 1
    D = growth_D(z)
    def sig2_gauss(R):
        def integrand(lnk):
            k = math.exp(lnk)
            return k ** 3 * Pk_lin_unnorm(k) * PK_NORM * D * D * math.exp(-(k * R) ** 2) / (2 * math.pi ** 2)
        v, _ = quad(integrand, math.log(1e-4), math.log(100.0), epsabs=0, epsrel=1e-5, limit=200)
        return v
    # bisect for sigma^2(R)=1
    lo, hi = 1e-3, 50.0
    f_lo = sig2_gauss(lo) - 1
    f_hi = sig2_gauss(hi) - 1
    if f_lo * f_hi > 0:
        # linear regime fallback (high z) — return linear
        return PK_NORM * np.array([Pk_lin_unnorm(k) for k in k_arr]) * D * D
    for _ in range(60):
        mid = math.sqrt(lo * hi)
        f_mid = sig2_gauss(mid) - 1
        if f_mid > 0:
            lo = mid
        else:
            hi = mid
    R_nl = 0.5 * (lo + hi)
    k_sigma = 1.0 / R_nl
    # neff and C from derivatives at R_nl
    eps = 1e-3
    s2_p = sig2_gauss(R_nl * (1 + eps))
    s2_m = sig2_gauss(R_nl * (1 - eps))
    s2_0 = sig2_gauss(R_nl)
    dlnsig2_dlnR = (math.log(s2_p) - math.log(s2_m)) / (2 * eps)
    neff = -dlnsig2_dlnR - 3.0
    # second derivative
    s2_pp = sig2_gauss(R_nl * (1 + 2 * eps))
    s2_mm = sig2_gauss(R_nl * (1 - 2 * eps))
    d2lnsig2 = (math.log(s2_pp) - 2 * math.log(s2_0) + math.log(s2_mm)) / ((2 * eps) ** 2)
    Cn = -d2lnsig2

    Omz = Om * (1 + z) ** 3 / E_LCDM(z) ** 2
    Olz = (1 - Om) / E_LCDM(z) ** 2

    # Smith 2003 fits
    an = 10 ** (1.4861 + 1.8369 * neff + 1.6762 * neff ** 2 + 0.7940 * neff ** 3
                + 0.1670 * neff ** 4 - 0.6206 * Cn)
    bn = 10 ** (0.9463 + 0.9466 * neff + 0.3084 * neff ** 2 - 0.9400 * Cn)
    cn = 10 ** (-0.2807 + 0.6669 * neff + 0.3214 * neff ** 2 - 0.0793 * Cn)
    gamma_n = 0.8649 + 0.2989 * neff + 0.1631 * Cn
    alpha_n = 1.3884 + 0.3700 * neff - 0.1452 * neff ** 2
    beta_n = 0.8291 + 0.9854 * neff + 0.3401 * neff ** 2
    mu_n = 10 ** (-3.5442 + 0.1908 * neff)
    nu_n = 10 ** (0.9589 + 1.2857 * neff)

    f1 = Omz ** -0.0307
    f2 = Omz ** -0.0585
    f3 = Omz ** 0.0743

    out = np.zeros_like(k_arr)
    for i, kh in enumerate(k_arr):
        Plin = PK_NORM * Pk_lin_unnorm(kh) * D * D
        Delta2_L = kh ** 3 * Plin / (2 * math.pi ** 2)
        y = kh / k_sigma
        fy = 0.25 * y + 0.125 * y ** 2
        Delta2_Q = Delta2_L * ((1 + Delta2_L) ** beta_n / (1 + alpha_n * Delta2_L)) * math.exp(-fy)
        Delta2_Hp = an * y ** (3 * f1) / (1 + bn * y ** f2 + (cn * f3 * y) ** (3 - gamma_n))
        Delta2_H = Delta2_Hp / (1 + mu_n / y + nu_n / y ** 2)
        Delta2_NL = Delta2_Q + Delta2_H
        out[i] = 2 * math.pi ** 2 * Delta2_NL / kh ** 3
    return out

# ----------------------------- n(z) ----------------------------------------
def nz_smail(z, z0, alpha, beta):
    return (z ** alpha) * np.exp(-((z / z0) ** beta))

def make_nz(z_grid, kind):
    # Euclid: standard Smail (Euclid Coll. forecasts) z_med~0.9
    # LSST Y10: DESC SRD form n(z) ~ z^2 exp(-(z/z0)^a), z0=0.11, a=0.68 -> z_med~0.86
    if kind == "Euclid":
        z0, alpha, beta = 0.64, 2.0, 1.5
    elif kind == "LSST":
        z0, alpha, beta = 0.11, 2.0, 0.68
    else:
        raise ValueError(kind)
    nz = nz_smail(z_grid, z0, alpha, beta)
    norm = simpson(nz, x=z_grid)
    return nz / norm

# ----------------------- lensing kernel (single bin) -----------------------
def lensing_kernel(z_arr, nz_arr):
    """W(chi) = (3/2) Om H0^2 chi/a integral_z^inf dz' n(z') (chi'-chi)/chi'.
    Returns interpolator W(chi) [units: 1/Mpc^2 * Mpc = 1/Mpc].
    Use natural units: H0/c = 1/Mpc, and we keep prefactor explicit.
    """
    chi_arr = np.array([float(chi_interp(z)) for z in z_arr])
    # cumulative tail integral: I(z) = int_z^inf dz' n(z') (chi' - chi(z))/chi'
    Wc = np.zeros_like(chi_arr)
    for i, z in enumerate(z_arr):
        chi_i = chi_arr[i]
        mask = z_arr >= z
        zp = z_arr[mask]
        nzp = nz_arr[mask]
        chip = chi_arr[mask]
        if len(zp) < 2:
            Wc[i] = 0.0
            continue
        integrand = nzp * (chip - chi_i) / np.where(chip > 0, chip, 1.0)
        Wc[i] = simpson(integrand, x=zp)
    a_arr = 1.0 / (1.0 + z_arr)
    pref = 1.5 * Om * (H0_INV_MPC ** 2)
    W = pref * chi_arr / a_arr * Wc  # [1/Mpc]
    return chi_arr, W

# ----------------------- C_l via Limber integration ------------------------
def Cl_kappa(l_arr, chi_arr, W_arr, z_arr, model="LCDM"):
    """C_l = int dchi W(chi)^2/chi^2 P_m(k=l/chi, z(chi))."""
    # Convert to chi grid and interpolate W; integrate over chi.
    Cl = np.zeros_like(l_arr, dtype=float)
    # Build P_m(k,z) interpolator for halofit on a grid (same for both, then rescale).
    z_pk_grid = np.linspace(0.05, 3.5, 12)
    k_grid = np.logspace(-3, 1.5, 80)  # h/Mpc
    Pk_table = np.zeros((len(z_pk_grid), len(k_grid)))
    for iz, zz in enumerate(z_pk_grid):
        Pk_table[iz] = halofit_Pk(k_grid, zz)
    # Convert P from [Mpc/h]^3 to [Mpc]^3 by * h^-3
    Pk_table_mpc = Pk_table / (h ** 3)
    # k in h/Mpc -> k_mpc = k*h
    log_k_mpc = np.log(k_grid * h)
    log_Pk = np.log(Pk_table_mpc)
    # bilinear interp in log
    from scipy.interpolate import RegularGridInterpolator
    log_Pk_interp = RegularGridInterpolator((z_pk_grid, log_k_mpc), log_Pk, bounds_error=False, fill_value=None)

    # chi integration grid (drop endpoints)
    mask = (chi_arr > 10.0) & (z_arr < 3.4)
    chi_int = chi_arr[mask]
    W_int = W_arr[mask]
    z_int = z_arr[mask]

    amp = PK_AMP_RATIO if model == "SQT" else 1.0
    for j, l in enumerate(l_arr):
        k_mpc = l / chi_int  # 1/Mpc
        pts = np.column_stack([z_int, np.log(k_mpc)])
        Pm = np.exp(log_Pk_interp(pts))
        integrand = (W_int ** 2) * Pm / (chi_int ** 2)
        Cl[j] = amp * simpson(integrand, x=chi_int)
    return Cl

# ------------------- xi_+(theta) Hankel transform J_0 ----------------------
def xi_plus(theta_rad, l_arr, Cl):
    """xi_+(theta) = (1/2pi) int dl l C_l J_0(l theta)."""
    # high-l oscillation: use log-spaced l
    integrand = l_arr * Cl * j0(l_arr * theta_rad)
    return simpson(integrand, x=l_arr) / (2 * math.pi)

# ------------------- Gaussian covariance for xi_+(theta) -------------------
def xi_plus_variance(theta_rad, l_arr, Cl, n_eff_arcmin2, sigma_e, f_sky):
    """Approx Gaussian variance for xi_+ at single theta.
    Cov[xi_+(theta), xi_+(theta)] ~ (1/(pi A f_sky)) * int dl l (C_l + N_l)^2 J_0^2(l theta),
    where N_l = sigma_e^2 / n_eff (in steradians). A here = 2 pi (full-sky factor absorbed)."""
    n_eff_sr = n_eff_arcmin2 * (60.0 * 180.0 / math.pi) ** 2
    Nl = sigma_e ** 2 / n_eff_sr
    # var(xi_+) = 1/(2 pi^2 f_sky) * int dl l (C_l+N_l)^2 J_0^2.  (Joachimi 2008 eq A2 simplified)
    integrand = l_arr * (Cl + Nl) ** 2 * j0(l_arr * theta_rad) ** 2
    var = simpson(integrand, x=l_arr) / (2 * math.pi ** 2 * f_sky)
    return var

# ============================== MAIN =======================================
def main():
    print("[L381] Computing xi_+(theta=10') for Euclid + LSST, SQT vs LCDM")

    z_grid = np.linspace(1e-3, 3.5, 200)
    out = {"meta": {
        "S8_LCDM": S8_LCDM, "S8_SQT": S8_SQT, "delta_S8_pct": DELTA_S8_PCT,
        "sigma8_LCDM": sigma8_LCDM, "sigma8_SQT": sigma8_SQT,
        "pk_amp_ratio_SQT_over_LCDM": PK_AMP_RATIO,
        "Om": Om, "h": h, "ns": ns, "Ob": Ob,
        "theta_arcmin": 10.0, "mu_eff": 1.0,
        "L286_assumption": "dark-only structural mu_eff=1, S_8 +1.14% effective shift",
    }, "surveys": {}}

    theta_arcmin = 10.0
    theta_rad = theta_arcmin * math.pi / (60.0 * 180.0)
    l_arr = np.logspace(math.log10(2), math.log10(2e4), 400)

    surveys = {
        "Euclid": {"area_deg2": 15000.0, "n_eff": 30.0, "sigma_e": 0.26, "nz": "Euclid"},
        "LSST_Y10": {"area_deg2": 18000.0, "n_eff": 27.0, "sigma_e": 0.26, "nz": "LSST"},
    }

    for sname, spec in surveys.items():
        print(f"  -- {sname} --")
        f_sky = spec["area_deg2"] / 41252.96
        nz_arr = make_nz(z_grid, spec["nz"])
        chi_arr, W_arr = lensing_kernel(z_grid, nz_arr)

        Cl_LCDM = Cl_kappa(l_arr, chi_arr, W_arr, z_grid, model="LCDM")
        Cl_SQT = Cl_kappa(l_arr, chi_arr, W_arr, z_grid, model="SQT")

        xi_LCDM = xi_plus(theta_rad, l_arr, Cl_LCDM)
        xi_SQT = xi_plus(theta_rad, l_arr, Cl_SQT)

        var_LCDM = xi_plus_variance(theta_rad, l_arr, Cl_LCDM,
                                     spec["n_eff"], spec["sigma_e"], f_sky)
        sigma_xi = math.sqrt(max(var_LCDM, 0.0))

        delta_xi = xi_SQT - xi_LCDM
        rel = delta_xi / xi_LCDM
        snr = abs(delta_xi) / sigma_xi if sigma_xi > 0 else float("inf")

        rec = {
            "f_sky": f_sky,
            "n_eff_arcmin2": spec["n_eff"],
            "sigma_e": spec["sigma_e"],
            "xi_plus_LCDM": xi_LCDM,
            "xi_plus_SQT": xi_SQT,
            "delta_xi_plus": delta_xi,
            "rel_diff_pct": rel * 100.0,
            "sigma_xi_plus": sigma_xi,
            "SNR_sigma": snr,
            "detectable_1sigma": bool(snr > 1.0),
            "detectable_3sigma": bool(snr > 3.0),
        }
        out["surveys"][sname] = rec
        print(f"     xi+_LCDM = {xi_LCDM:.4e}")
        print(f"     xi+_SQT  = {xi_SQT:.4e}")
        print(f"     Delta/xi = {rel*100:+.3f}%")
        print(f"     sigma    = {sigma_xi:.4e}")
        print(f"     SNR      = {snr:.2f}")

    # honest single line
    eu = out["surveys"]["Euclid"]; ls = out["surveys"]["LSST_Y10"]
    out["honest_one_line"] = (
        f"xi_+(10') SQT-LCDM 차이 = {eu['rel_diff_pct']:+.2f}% (S_8 +{DELTA_S8_PCT}% 직접 결과); "
        f"Euclid SNR={eu['SNR_sigma']:.1f}σ, LSST_Y10 SNR={ls['SNR_sigma']:.1f}σ — "
        f"{'양 미션 모두 1σ 검출 가능' if (eu['SNR_sigma']>1 and ls['SNR_sigma']>1) else '검출 한계'}; "
        "단, SQT 는 LCDM 대비 'worsen' 방향 (S_8 tension 악화)이므로 검출 = SQT 기각."
    )
    print()
    print(out["honest_one_line"])

    rep_path = os.path.join(OUT_DIR, "report.json")
    with open(rep_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"  -> {rep_path}")

if __name__ == "__main__":
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    np.seterr(all="ignore")
    main()
