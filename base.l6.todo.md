# base.l6.todo.md — L6 Phase-6 WBS

## Phase L6-0 Infrastructure
- [x] refs/l6_kill_criteria.md — K17-K20, Q13-Q17 고정 (2026-04-11)
- [x] base.l6.todo.md WBS 작성
- [x] simulations/l6/ 디렉터리 생성 (evidence/, growth/, class/, dr3/)
- [x] Python 환경 확인: dynesty 3.0.0 ✓, emcee 3.1.6 ✓, classy ✗, hi_class ✗

## Phase L6-T Theory Upgrade (8인팀 필수)
- [x] L6-T3: 이론 포지셔닝 문서 (8인팀) → refs/l6_theory_positioning.md — "정직한 falsifiable phenomenology", JCAP 타깃
- [x] L6-T1: Amplitude-locking 유도 시도 (8인팀) → refs/l6_amplitude_lock_analysis.md — Q17 부분 달성 (이론 동기, 완전 유도 아님)
- [x] L6-T2: C11D 일반 disformal PPN 분석 (8인팀) → refs/l6_c11d_general_disformal.md — GW170817 강제, K20 미해당

## Phase L6-E Full Marginalized Evidence (4인 코드리뷰 필수)
- [x] L6-E1: C28 완전 3D marginalized (Om, h, gamma0), nlive=800 → Δ ln Z = +8.633 K17 PASS (26.8분)
- [x] L6-E2: C11D 3D marginalized 재실행 nlive=1000 → Δ ln Z = +8.771 K17 PASS (84.3분)
- [x] L6-E3: Occam 분석 통합 → 실측 결과: A12(10.769) > C28(8.633), gap=-2.14 nats, net=-3.52 nats
- [x] L6-E-hires: Alt 모델 7종 nlive=800 재실행 → A12/A17/A01/A05/A06/A08/A09 전원 K17 PASS
- [x] L6-E-hires: LCDM hires 기준치 → ln Z = -843.538 (L5 대비 +0.15 nats)

## Phase L6-G Growth Sector μ(a,k) (8인+4인 필수)
- [x] L6-G1: SQMH 섭동 방정식 도출 (이론) → mu_eff_profiles.py docstring + 8인팀 이론 분석 완료
- [x] L6-G2: μ_eff 수치 계산 + S_8 보정 (4인 코드리뷰) → mu_eff.json + s8_mu_correction.json 완료
- [x] L6-G3: CLASS 근사 (4인 리뷰) → cmb_chi2.json 완료 (C11D K19 provisional PASS, Δchi2=−6.33)

## Phase L6-D DESI DR3 재실행 준비
- [x] L6-D1: 재실행 스크립트 (4인 코드리뷰) → simulations/l6/dr3/run_dr3.sh 완료
- [x] L6-D2: DR3 해석 시나리오 α~ε (8인팀) → refs/l6_dr3_scenarios.md 완료

## Phase L6-P Paper v2
- [x] L6-P1: §7.5 Occam + §7.6 μ_eff + §8.5 K13 실결과 + §8.9 8인팀 포지셔닝 추가
- [x] L6-P2: 저널 타깃 결정 → JCAP 확정 (8인팀 합의, L6-T3)

## 최종 산출
- [x] base.l6.result.md — 시나리오 B 판정 + 8인/4인 완료 확인
