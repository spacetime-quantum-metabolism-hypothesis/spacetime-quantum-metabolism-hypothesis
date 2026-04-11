# refs/l7_kill_criteria.md — L7 Kill / Keep 기준 (실행 전 고정)

> **이 파일은 L7 실행 시작 전 고정. 실행 도중 임계값 조정 금지.**
> 작성일: 2026-04-11. 근거: base.l7.command.md §Kill/Keep 기준.

---

## KILL 조건

| ID | 조건 | 결과 |
|----|------|------|
| **K21** | JCAP reject (not major-revision) | 저널 재선택 후 재제출 |
| **K22** | DESI DR3: w_a > 0 (≥ 2σ) | honest negative result 논문 작성 |
| **K23** | classy 정식 CMB: Δχ²_CMB > LCDM+6 | C11D/C28 KILL — A12만 유지 |
| **K24** | UV completion 시도 후 8인팀 "수학적 불가능" 판정 | Theory 채널 포기, 현상론 브랜딩 확정 |
| **K25** | Euclid Y1: μ_eff 측정 μ < 0.95 OR > 1.1 | 성장섹터 falsified |

## KEEP 조건

| ID | 조건 |
|----|------|
| **Q18** | JCAP accept 또는 minor revision |
| **Q19** | DESI DR3: w_a < 0 지속 ≥ 2σ |
| **Q20** | classy 정식 CMB: Δχ²_CMB ≤ LCDM+3 (K19 formal pass) |
| **Q21** | amplitude-locking 완전 유도 성공 (8인팀) |
| **Q22** | 우주론 외 채널 ≥ 1개: GW binary, CMB-S4 ISW, SKAO 21cm |

---

## 기준 근거

- **K23 임계값 +6**: L6 K19와 동일. classy 정식 TT+EE+TE likelihood 사용.
  압축 우도 대비 정밀도 상승. +6 = 2σ 수준.
- **K22 임계값**: DR3에서 w_a > 0 이 2σ 이상이면 SQMH wₐ < 0 예측 falsified.
- **K25**: Euclid Y1 (예상 2026-2027). μ_eff ≈ 1 구조이므로 이 범위면 구조 불일치.

## L6 → L7 출발점

| 후보 | L6 marginalized Δ ln Z | K17 | K19 (현재) |
|------|------------------------|-----|-----------|
| A12  | +10.769 | PASS | provisional (압축) |
| C11D | +8.771  | PASS | provisional (압축) |
| C28  | +8.633  | PASS | provisional (압축) |
