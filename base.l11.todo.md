# base.l11.todo.md -- L11 WBS Checklist

> Date: 2026-04-11
> L11: Boltzmann Birth-Death Isomorphism -> 20 Empirical Formula Derivations
> Rounds 1-5 execution plan

---

## Phase L11-0: Setup [COMPLETE]
- [x] refs/l11_kill_criteria.md (K61-K63, Q61-Q65)
- [x] base.l11.todo.md (this file)
- [x] simulations/l11/ all 21 subdirectories created

## Phase L11-A: Round 1 -- All 20 Attempts [COMPLETE]
- [x] refs/l11_derivation_all20.md (8-person parallel team, all 20 approaches)
- [x] simulations/l11/michaelis/mm_vs_erf.py (Attempt 1)
- [x] simulations/l11/master/master_equation_rhode.py (Attempt 2)
- [x] simulations/l11/first_passage/dark_energy_onset.py (Attempt 3)
- [x] simulations/l11/detailed_balance/wwa_direction.py (Attempt 4)
- [x] simulations/l11/fdt/geff_response.py (Attempt 5)
- [x] simulations/l11/stefan_boltzmann/sb_gamma0.py (Attempt 6)
- [x] simulations/l11/generating_func/dark_energy_cumulants.py (Attempt 7)
- [x] simulations/l11/wkb_action/sqmh_lagrangian.py (Attempt 8)
- [x] simulations/l11/gillespie/stochastic_hz.py (Attempt 9)
- [x] simulations/l11/extinction/dark_energy_fate.py (Attempt 10)
- [x] simulations/l11/quasispecies/sigma_distribution.py (Attempt 11)
- [x] simulations/l11/branching/critical_branching.py (Attempt 12)
- [x] simulations/l11/cme_spectrum/rhode_power_spectrum.py (Attempt 13)
- [x] simulations/l11/kingman/sqmh_coalescent.py (Attempt 14)
- [x] simulations/l11/void_bias/rhode_void_bias.py (Attempt 15)
- [x] simulations/l11/rg_fixed_point/sigma_ir_fixed.py (Attempt 16)
- [x] simulations/l11/entropy_prod/wwa_entropy.py (Attempt 17)
- [x] simulations/l11/turing/sqmh_turing.py (Attempt 18)
- [x] simulations/l11/lyapunov/sqmh_stability.py (Attempt 19)
- [x] simulations/l11/large_deviation/rhode_fluctuation.py (Attempt 20)
- [x] simulations/l11/integration/l11_comparison.py
- [x] refs/l11_integration_verdict.md
- [x] base.l11.result.md

## Phase L11-B: Rounds 2-5 -- Deep Dive [COMPLETE]
- [x] Priority: Attempt 19 (Lyapunov): w(z) = -1 + 0.5*Omega_m(z), wa_bg = +0.34
- [x] Priority: Attempt 15 (void bias): b_DE = -Pi_SQMH (NF-29 confirmed)
- [x] Priority: Attempts 4+17: wa<0 from inflation over-production (n_bar/n_eq ~ 10^83)
- [x] NF-28: Poisson floor bound registered
- [x] NF-29: Dark energy anti-bias registered
- [x] refs/l11_rounds_2to5.md [COMPLETE]

---

## Constants Reference
- sigma = 4.521e-53 m^3/(kg*s)
- Pi_SQMH = 1.855e-62 (= Omega_m * H0 * t_P / (4*pi) ... CHECK)
- Actually Pi_SQMH from base.l10.result.md = 3.709e-62
- A12: w0=-0.886, wa=-0.133, Delta_lnZ=+10.769
- C28: gamma0=0.000624, wa=-0.176, G_eff/G=+2%
- n_bar_eq = Gamma_0/(sigma*rho_m + 3H) at equilibrium
- Omega_m=0.315, H0=67.4 km/s/Mpc = 2.183e-18 s^-1
- t_P = 5.391e-44 s
- l_P = 1.616e-35 m
- rho_Planck = 5.157e96 kg/m^3
- rho_crit0 = 9.472e-27 kg/m^3
- rho_m0 = Omega_m * rho_crit0 = 2.984e-27 kg/m^3
- rho_DE0 = (1-Omega_m) * rho_crit0 = 6.489e-27 kg/m^3

---

*Created: 2026-04-11*
