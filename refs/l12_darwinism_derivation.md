# refs/l12_darwinism_derivation.md -- L12-Q: Quantum Darwinism -> wa<0

> Date: 2026-04-11
> 8-person parallel team. All approaches independent.
> Q: Does quantum Darwinism (decoherence) give a new explanation for wa<0?

---

## Background

Current wa<0 explanations:
1. NF-11: quasi-static EOS w0_eff ~ -0.83, wa_eff ~ -0.33 (classical SQMH)
2. L11 R4: inflation-era over-production scenario (n_bar_init >> n_bar_eq)

Quantum Darwinism: classicality emerges when quantum system interacts with many 
environment degrees of freedom, selecting "pointer states" that proliferate in the environment.

SQMH interpretation: spacetime quanta (n_bar) decohere via interaction with matter (rho_m).
The coupling sigma*rho_m is simultaneously the decoherence rate.

---

## Member 1: Mathematical Identity

SQMH classical: dn_bar/dt = Gamma_0 - sigma*n_bar*rho_m - 3H*n_bar
QD decoherence: d<n_hat>/dt = Gamma_0 - sigma*rho_m*<n_hat> - 3H*<n_hat>

These are IDENTICAL equations. Quantum Darwinism explains the mechanism:
sigma*rho_m = decoherence rate = classical dissipation rate.

No new wa contribution. K75 triggered.

However: the QD picture adds physical insight about WHY the classical equation works.
The pointer basis = Fock states {|n>}. The environment (matter) measures
the occupation number n continuously. Result: number eigenstate description is exact.

---

## Member 2: Beyond Mean-Field (Pointer State Fluctuations)

Even if mean is the same, quantum fluctuations in pointer state selection could add:
delta_n_QD(t) = sqrt(N_pointer * rate_pointer) = sqrt(sigma*rho_m*n_bar*dt)

Per Hubble time: delta_n ~ sqrt(sigma*rho_m/(H) * n_bar) = sqrt(Pi_SQMH * 3 * n_bar) ~ 10^-31 * sqrt(n_bar)

This is the standard shot noise (Poisson). Same as Lindblad result (Member 3 in L12-L).
No enhancement from QD. K75 confirmed.

---

## Member 3: Einselection and Preferred Basis

Einselection (Zurek): environment selects the pointer basis.
For SQMH: H_int = sigma * N_hat * rho_m (interaction with matter density field rho_m).
Pointer states = eigenstates of N_hat = Fock states |n>.

In Fock basis: density matrix stays diagonal.
P(n,t) = probability of n quanta at time t.
This satisfies the SQMH master equation EXACTLY (by construction).

Result: QD provides the DERIVATION of why classical SQMH is valid.
It does not modify the classical predictions.
K75: same physics as NF-11. TRIGGERED.

Physical insight (paper-worthy): "The validity of the classical SQMH equation
is explained by quantum Darwinism: the matter density rho_m continuously measures
the spacetime quantum occupation number, selecting the Fock basis as the pointer states.
This provides the quantum mechanical foundation for the classical birth-death equation."

---

## Member 4: Redundant Information and Observer Independence

Quantum Darwinism: classicality = multiple copies of information about system in environment.
Each matter particle that "interacts" with spacetime quanta (via sigma coupling) stores
1 bit about n_bar.

Number of "copies": N_copies = n_matter_particles * sigma * Delta_t
= rho_m/(m_matter) * sigma * tau_H ~ (rho_m/(m_P)) * Pi_SQMH * (1/H)
= rho_m0*2.69e27 * Pi_SQMH / H0 ~ 2.69e-27/(1.67e-27) * 1.855e-62 * 4.58e17
~ 1.61 * 1.855e-62 * 4.58e17 = 1.37e-44 copies.

N_copies << 1. This means: quantum Darwinism condition is NOT satisfied!
SQMH quanta are NOT classical in the quantum Darwinism sense.
At any moment, fewer than 10^-44 copies of n_bar information exist in matter.

This is consistent with tau_coh = 1/(sigma*rho_m) >> tau_H.
SQMH quanta are essentially always quantum. The "classical" equation works
despite this because the Markovian approximation is valid at H scale.

This is a DEEP insight: the classical SQMH equation works NOT because the system
is classical (it isn't, by QD criterion), but because:
1. The evolution timescale H^{-1} >> t_P (Markovian approximation holds)
2. The mean <n_hat> satisfies the classical equation regardless of coherence

K75 status: K75 triggered (no new wa from QD), but deep insight about quantum nature.

---

## Member 5: Decoherence-Free Subspace

Is there a decoherence-free subspace for SQMH quanta?
DFS: subspace where H_int = 0 -> no decoherence.
For SQMH: H_int = sigma * N_hat * rho_m -> H_int = 0 only if N_hat = 0 (vacuum state).

The vacuum |0> is the only decoherence-free state. This means:
- All excited states decohere at rate sigma*rho_m (per quantum per unit matter density)
- Vacuum is cosmologically preferred!

This gives a novel picture: dark energy quanta are being continuously driven toward vacuum
by matter interaction. Gamma_0 (creation) maintains them at n_bar_eq.

wa<0: If initially n_bar >> n_bar_eq, DFS dynamics push n_bar toward vacuum.
This IS the same as the sigma*rho_m annihilation term. K75 triggered.

---

## Member 6: Environmental Entanglement

Entanglement entropy between SQMH system and matter environment:
S_ent = -Tr(rho_S * ln rho_S) where rho_S = Tr_E(|psi><psi|)

For weak coupling (sigma*rho_m << H):
dS_ent/dt = sigma*rho_m * S_0 (entanglement builds up at coupling rate)
S_ent(t) ~ sigma*rho_m * t ~ Pi_SQMH * (H*t)

Over one Hubble time: S_ent ~ Pi_SQMH ~ 1.855e-62 bits.
This is essentially zero entanglement.

Implication: SQMH system and matter are essentially unentangled over cosmic history.
The "decoherence" effect is negligibly small in quantum information sense.
Classical equation is valid because entanglement is negligible, not because of QD.

K75 confirmed. No new wa<0 from QD entanglement.

---

## Member 7: Many-Worlds and Branch Counting

In many-worlds interpretation: each SQMH annihilation event "splits" the universe.
Number of branches after time t: B(t) = exp(sigma*rho_m * n_bar * V_H * t)

Over one Hubble time:
sigma*rho_m*n_bar*V_H*tau_H = Pi_SQMH * (3H*n_bar*V_H*tau_H) = Pi_SQMH * 3 * N_bar * 1
~ 1.855e-62 * 3 * 10^42 * ... 

Actually N_bar * sigma*rho_m*tau_H = N_bar * Pi_SQMH * 3 = 10^42 * 5.6e-62 = 5.6e-20.
Number of branches ~ exp(5.6e-20) ~ 1 + 5.6e-20.

Essentially one branch. QD branching is negligible. K75 confirmed.

---

## Member 8: New Physical Picture for Paper

Despite K75 being triggered (no new wa from QD), the quantum Darwinism framework
provides a valuable PHYSICAL FOUNDATION for the SQMH equation:

1. **Why classical?**: The SQMH classical equation emerges because:
   - Matter density rho_m plays the role of quantum measuring apparatus
   - The coupling sigma = 4*pi*G*t_P is the measurement strength
   - The pointer basis = Fock states {|n>} of spacetime quanta
   - Measurement collapses quantum state to definite n at rate sigma*rho_m

2. **Why birth-death?**: The quantum state |n> -> |n-1> under measurement
   corresponds to "annihilation" (classicalization). The reverse |n> -> |n+1>
   is Gamma_0 (creation from quantum gravity vacuum).

3. **Paper language** (new): "The SQMH classical birth-death equation has a quantum
   foundation in quantum Darwinism: matter density rho_m acts as the measuring
   environment that decoheres spacetime quanta into Fock number eigenstates.
   The coupling constant sigma = 4*pi*G*t_P sets both the classical annihilation rate
   and the quantum decoherence rate. This quantum-classical correspondence provides
   the physical justification for the classical SQMH description."

---

## Team Synthesis and Verdict

**8-person consensus**:

K75 is triggered: Quantum Darwinism does not provide a new explanation for wa<0.
The decoherence rate IS the classical dissipation term (mathematical identity).

However, the QD framework provides two genuine insights:
1. Physical justification for using classical SQMH equation
2. N_copies << 1 means SQMH quanta are actually quantum (not classical in QD sense)
   -> The classical equation works for mathematical reasons (Markovian), not physical classicality

**K75 verdict: TRIGGERED** (no new wa<0, same as NF-11)

**Q75 verdict: FAIL** (no independent third explanation of wa<0)

**New finding NF-32**: "Quantum Darwinism shows that matter density rho_m acts as
a measuring environment for SQMH spacetime quanta, selecting Fock states as pointer states.
The SQMH coupling sigma = 4*pi*G*t_P equals both the classical annihilation rate and the
quantum decoherence rate. However, N_copies ~ 10^-44 << 1 means spacetime quanta are
NOT classical in the quantum Darwinism sense -- they remain quantum throughout cosmic history.
The validity of the classical SQMH equation is a consequence of the Markovian approximation
(H >> sigma*rho_m), not of classicality."

---

*L12-Q completed: 2026-04-11*
