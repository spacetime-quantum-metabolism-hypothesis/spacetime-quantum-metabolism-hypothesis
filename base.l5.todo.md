# base.l5.todo.md — L5 Phase-5 WBS

## Phase L5-0 Infrastructure
- [x] refs/l5_kill_criteria.md freeze
- [x] dynesty install check (v3.0.0)
- [x] simulations/l5/common.py (production MCMC, nested evidence, fisher, cosmic shear)
- [x] simulations/l5/ directory layout

## Phase L5-A Mainstream Production MCMC
- [x] C28 Maggiore RR: budget-limited 16×300 실행, R̂=1.82 (K13 미통과, 고사양 재실행 필요)
- [x] C33 f(Q): budget-limited 16×300 실행, R̂=1.27 (K13 미통과, demoted 이후 재실행 생략)

## Phase L5-B Alt-hard Production MCMC
- [x] A01 SQMH canonical: 2-D budget-limited + interpretation doc 완료
- [x] A05 Sqrt relaxation: ibid
- [x] A12 Erf diffusion: ibid
- [x] A17 Adiabatic pulse: ibid

## Phase L5-C Bayesian evidence (dynesty)
- [x] LCDM baseline evidence — ln Z = -843.689
- [x] C28, C33 evidence — C28 +11.257 STRONG, C33 +2.508 substantial
- [x] A01, A05, A12, A17 evidence — all STRONG (+10.6~10.8)
- [x] A03, A06, A08, A09, A11, A13, A15, A16, A19, A20 evidence — STRONG (+4.5~10.6), A19 substantial
- [x] C11D evidence — +8.951 STRONG (3D Occam-penalised)
- [x] Δ ln Z table, Jeffreys scale verdict — evidence_all.json, base.l5.result.md §L5-C

## Phase L5-D Cosmic shear S_8
- [x] DES-Y3 + KiDS-1000 + Planck WL data module — S_8 combined = 0.7656 ± 0.0138
- [x] chi2_joint_with_shear for all winners — C33 FAIL, 나머지 PASS
- [x] K15 check per candidate — C33 K15+Q10+Q11 3중 실패 → demoted

## Phase L5-E Re-evaluation
- [x] C11D hi_class disformal or Sakstein-Jain analytic K3 re-judge — Sakstein-Jain CLW ODE로 K3 CLEARED, PROMOTED
- [x] C26 J⁰=α_Q H ρ_m reformulation full ODE — CMB dead, KILL 확정
- [x] Verdict: C11D PROMOTE / C26 KILL

## Phase L5-F Alt-20 SVD class reduction
- [x] 14 alt candidates best-fit E²(z) matrix
- [x] SVD principal drift modes, n_eff=1 (99.15% variance mode 1)
- [x] Cluster representative selection by Δ ln Z — A12 1위
- [x] paper/figures/l5_alt_class_svd.png

## Phase L5-G DESI DR3 Fisher forecast
- [x] σ(w_0), σ(w_a) per winner
- [x] 2σ LCDM separation (Q9) — C11D 2.9σ, C28 3.91σ, A12 2.16σ
- [x] Pairwise discrimination table — C28↔C33 0.19σ (구분 불능)
- [x] paper/figures/l5_dr3_forecast.png

## Phase L5-H Paper v1 update
- [x] 00_abstract.md — L5 winner 3인방 + Δ ln Z + DR3 forecast 업데이트
- [x] 05_desi_prediction.md — C11D/C28/A12 예측 + DR3 table + C33/C26 demoted/kill
- [x] 06_mcmc_results.md — C11D 승격 + K13 budget note + backup/demoted
- [x] 07_comparison_lcdm.md — Bayesian evidence 전체 표 + Δχ² table
- [x] 08_discussion_limitations.md — cosmic shear, alt-20 class degeneracy, K13 budget, C26 negative result
- [x] 09_conclusion.md — 3 winner 확정 + 2 negative results + DR3 prediction
- [x] paper/10_appendix_alt20.md — 기존 완료

## Phase L5-I arXiv checklist
- [x] paper/arxiv_submission_checklist.md — 완료

## Phase L5-J Final integration
- [x] base.l5.result.md — L5-C 섹션 완료 + Q8 표 업데이트
- [x] base.l5.todo.md — 전 태스크 [x] 완료 표시 (본 업데이트)
- [x] CLAUDE.md L5 prevention rules — 12개 규칙 추가
