# base.l8.todo.md — L8 Phase-8 WBS

## Phase L8-0 Infrastructure
- [x] refs/l8_kill_criteria.md — K31-K35, Q31-Q35 고정 (2026-04-11)
- [x] base.l8.todo.md WBS 작성
- [x] simulations/l8/ 디렉터리 생성 (a12/, c11d/, c28/, integration/)

## Phase L8-A A12 역유도 (8인팀)
- [x] L8-A 8인 순차 검토 → refs/l8_a12_derivation.md (2026-04-11)
- [x] L8-A 수치: simulations/l8/a12/sqmh_ode_vs_erf.py (2026-04-11)
  - chi²/dof(SQMH vs A12) = 7.63, Q31 FAIL, K31 미발동
  - 핵심: σ·ρ_m/(3H₀) = 1.83e-62 → SQMH bg = LCDM
- [x] Q31 판정 확정: FAIL (7.63 > 1.0)

## Phase L8-C C11D 역유도 (8인팀) ← 최우선
- [x] L8-C 8인 순차 검토 → refs/l8_c11d_derivation.md (2026-04-11)
- [x] L8-C 수치: simulations/l8/c11d/clw_vs_sqmh.py (2026-04-11)
  - Shooting: y_ini=1.637e-6 → Om_phi(a=1)=0.6905 ✓
  - σ_need = 8.23e8, σ_SQMH = 4.52e-53 → 61차수 갭
  - σ_eff < 0 전체 구간 (두 후보 모두)
- [x] Q32 판정 확정: FAIL, K32 TRIGGERED

## Phase L8-R C28 역유도 (8인팀)
- [x] L8-R 8인 순차 검토 → refs/l8_c28_derivation.md (2026-04-11)
- [x] L8-R 수치: simulations/l8/c28/rr_vs_sqmh.py (2026-04-11)
  - U(a=1)=-12.41, E²_RR(a=1)=0.31 (단순화 ODE 한계)
  - 잔차 100% → Q33 FAIL
- [x] Q33 판정 확정: FAIL, K33 TRIGGERED

## Phase L8-N 수치 통합 검증 (Rule-B 4인 리뷰)
- [x] simulations/l8/integration/l8_comparison.py (2026-04-11)
- [x] simulations/l8/integration/l8_comparison.json (2026-04-11)
- [x] K31-K33 수치 판정 확정:
  - K31 미발동, K32 TRIGGERED, K33 TRIGGERED
  - Q31/Q32/Q33 전원 FAIL

## Phase L8-I 통합 판정 (8인팀)
- [x] refs/l8_integration_verdict.md (2026-04-11) — 8인 합의 완료
- [x] base.l8.result.md (2026-04-11)
- [ ] 논문 §8 역유도 섹션 반영 (paper 작업 시 처리)

## 최종 산출
- [x] base.l8.result.md — 완료 (2026-04-11)

## L8 결론
**PRD Letter 조건 미달** (Q32 FAIL)  
**JCAP 포지셔닝 확정**: A12 현상론 proxy, C11D/C28 독립 이론  
**핵심 발견**: σ = 4πGt_P는 배경 우주론에서 62차수 무시가능  
