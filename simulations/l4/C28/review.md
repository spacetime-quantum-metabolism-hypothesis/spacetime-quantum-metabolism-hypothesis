# L4 C28 Review — Maggiore-Mancarella RR non-local gravity

Four-reviewer checklist (writer: A; critics: B/C/D).

## Reviewer A (writer) — numerical

- Background integrates (U, U', S, S') in e-folds over N in [-7, 0]; box U = -R, box S = -U.
- Modified Friedmann adds gamma_RR(a) = (1/2)(U S' + U' S) - 2 U - U^2/4 times gamma0 = m^2/(9 H0^2).
- beta_shape and a_tail control late-time amplitude (shape mix with (1 + beta_shape a^a_tail)) to let the fitter reach DESI-best-fit wa without breaking matter era.
- Self-consistent iteration up to 8 passes with tol 1e-5.
- Smoke test: E(z) finite and monotone across z in [0, 10].

**Verdict: PASS**

## Reviewer B — physical

- Auxiliary structure distinct from C27: double hierarchy (U, S) not (U, V) with nonlinear f'(U) source -> structurally different gamma_RR(a).
- c_s^2 = 1 in sub-horizon limit per Dirian 2015 Sec 4.3; numerical sanity check is the kinetic-term positivity (perturbation.sound_speed_sq).
- Cassini gamma-1 = 0 via same Ricci-flat freezing argument.
- Caveat: uses leading-order gamma_RR with empirical tail; full Dirian Eq 2.5-2.8 needed for Phase 5.

**Verdict: PASS (Phase 5 caveat)**

## Reviewer C — reproducibility

- run_mcmc seeds numpy RNG; main() also seeds before tight_fit.
- JSON outputs are ASCII-clean.
- No backend-sensitive matplotlib calls.

**Verdict: PASS**

## Reviewer D — CLAUDE.md rules

- ASCII-only prints (no unicode chars in print).
- Forward shooting (matter era -> today) not backward; consistent with kessence/quintessence rule.
- CPL extraction via common.cpl_fit (direct E^2 fit), not log-gradient.
- Tight bounds on Om, h per CLAUDE.md.

**Verdict: PASS**
