# refs/l6_kill_criteria.md — L6 Kill / Keep 기준 (실행 전 고정)

> **이 파일은 L6 실행 시작 전 고정. 실행 도중 임계값 조정 금지.**
> 작성일: 2026-04-11. 근거: base.l6.command.md §Kill/Keep 기준.

---

## KILL 조건

| ID | 조건 | 판정 결과 |
|----|------|----------|
| **K17** | Marginalized Δ ln Z < +2.5 (Q8 재검증) | KILL — fixed-theta 아티팩트 확인 |
| **K18** | μ_eff(a=1, k=0.1/Mpc) < 0.8 또는 < 0 (ghost) | KILL — 불안정 섭동 |
| **K19** | CLASS full CMB χ² vs Planck > LCDM + 6 | KILL — CMB 죽음 |
| **K20** | 8인팀 Synthesizer: "반증" 판정 | 해당 이론 주장 폐기 |

## KEEP 조건

| ID | 조건 |
|----|------|
| **Q13** | Marginalized Δ ln Z ≥ +2.5 (4인 코드리뷰 통과 코드로 산출) |
| **Q14** | CLASS Planck CMB χ² ≤ LCDM + 3 |
| **Q15** | μ_eff 유도 가능 + S_8 tension Δ(S_8) ≥ 0.010 개선 |
| **Q16** | DESI DR3 실측 w_a < 0 지속 + C11D/C28 ≥ 2σ 분리 |
| **Q17** | amplitude-locking 수식 유도 성공 (8인팀 합의) |

---

## 기준 근거

- **K17 임계값 +2.5**: Jeffreys' scale "substantial" 하한. L5 fixed-theta 결과
  (C28 +11.26, C11D +8.95, A12 +10.78) 는 완전 marginalized 에서 Occam 패널티
  ~2-4 units 예상. +2.5 미만이면 evidence 아티팩트로 확정.
- **K18 임계값 0.8**: LCDM μ=1 대비 20% 이상 억제는 CMB ISW 등 기존 관측과
  충돌 위험 (Planck 2018 growth 제약 μ=1.01±0.05 @k=0.1/Mpc).
- **K19 임계값 LCDM+6**: 2σ 수준. 현재 Planck 데이터 총 χ²~2500 에서 Δ6은
  3σ 이상 탈락 기준.
- **K20**: 8인팀 최고 권위. 반증 판정은 5인 이상 동의 필요.

## L5 위너 현황 (L6 출발점)

| 후보 | L5 Δ ln Z (fixed-θ) | L5 MCMC K13 | L6 대상 |
|------|---------------------|-------------|---------|
| C11D | +8.951 | ✅ R̂=1.0114 | L6-E2 full evidence |
| C28  | +11.257 | ❌ R̂=1.365  | L6-E1 full evidence |
| A12  | +10.779 | ✅ R̂=1.0095 | L6-E3 Occam 분석 |
