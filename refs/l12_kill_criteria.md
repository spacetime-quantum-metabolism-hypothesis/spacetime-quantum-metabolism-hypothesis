# refs/l12_kill_criteria.md -- L12 Kill/Keep Criteria (Fixed Before Execution)

> Date: 2026-04-11
> Fixed before Round 1 execution begins. These criteria do NOT change after runs.
> Language standard inherited from L7-L11.

---

## L12 Context

L12 strategy shift: instead of directly measuring sigma = 4*pi*G*t_P
(blocked by 62-order gap), we seek theoretical determination or
entirely new observational channels.

Key constants:
- sigma = 4*pi*G*t_P = 4.52e-53 m^3/(kg*s)
- t_P = 5.391e-44 s
- G = 6.674e-11 m^3/(kg*s^2)
- l_P = 1.616e-35 m
- m_P = 2.176e-8 kg
- Pi_SQMH = sigma*rho_m0/(3*H0) = 1.855e-62
- Gamma_0/sigma = n0*mu ~ rho_Planck = 5.155e96 kg/m^3

---

## KILL Conditions (all fixed before execution)

| ID  | Condition                                                                 | Consequence if triggered                          |
|-----|---------------------------------------------------------------------------|---------------------------------------------------|
| K71 | Lindblad quantum correction: delta_w_quantum < 1e-60                     | Quantum SQMH cosmologically irrelevant. Confirmed. |
| K72 | Bekenstein cannot constrain Gamma_0: allowed range spans > 62 orders     | Gamma_0 is not theory-determinable. Confirmed.    |
| K73 | Verlinde cannot derive sigma: intermediate steps require G independently  | sigma = 4*pi*G*t_P is purely phenomenological.   |
| K74 | dS SQMH w(z) structurally differs from A12 erf: chi^2/dof > 10          | dS limit disconnected from A12. Path terminated.  |
| K75 | Quantum Darwinism adds no new contribution to wa: same as NF-11/NF-29   | Decoherence channel irrelevant.                   |

---

## KEEP Conditions (game-changers)

| ID  | Condition                                                                        | Consequence if triggered                                   |
|-----|----------------------------------------------------------------------------------|-------------------------------------------------------------|
| Q71 | Lindblad quantum correction: delta_w_quantum > 1e-30 (32+ orders improvement)  | Quantum SQMH new channel. Add quantum correction section.   |
| Q72 | Bekenstein constrains Gamma_0 to within 10 orders of magnitude                 | First theoretical lower bound on Gamma_0. Strengthen paper. |
| Q73 | Verlinde yields sigma = 4*pi*G*t_P * C where C = O(1)                          | UV completion new path. PRD Letter review triggered.        |
| Q74 | dS SQMH w(z) = new functional form (non-erf) + chi^2/dof < 2 vs DESI data     | New phenomenological proxy for A12. Novel result.          |
| Q75 | Decoherence rate sigma*rho_m contributes independently to wa<0 (not NF-11)     | Third independent explanation of wa<0.                     |

---

## Game-Changer Protocol

If Q72 achieved (Bekenstein constrains Gamma_0 to 10 orders):
-> First theoretical naturality explanation of Gamma_0
-> Partial resolution of cosmological constant hierarchy problem
-> Triggers: paper Section 2 expansion + PRD Letter consideration

If Q73 achieved (Verlinde sigma = 4*pi*G*t_P * C, C=O(1)):
-> sigma = 4*pi*G*t_P emerges from entropic gravity naturally
-> UV completion new path. K56 partially overturned.
-> Triggers: PRD Letter review. Rounds 6-10 deep investigation.

If Q72 + Q73 simultaneously:
-> Both sigma and Gamma_0 theory-determined
-> SQMH fundamental parameters no longer free
-> PRD Letter entry + entirely new level of theory

---

## Verdict Protocol

Each round reports:
- K71-K75: TRIGGERED / NOT TRIGGERED / PENDING
- Q71-Q75: PASS / FAIL / PARTIAL / PENDING
- Overall: KILL (any K triggered) / KEEP (any Q passed) / UNCERTAIN

---

*Fixed: 2026-04-11. Not modifiable after Round 1 starts.*
