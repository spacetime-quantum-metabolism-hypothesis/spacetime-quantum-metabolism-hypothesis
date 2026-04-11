# refs/l6_dr3_scenarios.md — L6-D2 DR3 해석 시나리오

> 8인팀 사전 합의 (L6-T3 포지셔닝 확장). 작성일: 2026-04-11.
> DR3 전에 "확인될 것" 확언 금지. 예측만.

## 시나리오 정의 (base.l6.command.md §L6-D2)

| 시나리오 | DR3 조건 | SQMH 결론 |
|---------|----------|-----------|
| **α** | w_a < -0.5 강화 + C11D/C28 ≥ 3σ 분리 | PRD Letter 재검토 |
| **β** | w_a < 0 유지 + < 2σ 분리 | JCAP 현상론 유지 |
| **γ** | w_a > 0 역전 | wₐ < 0 부호 예측 falsified |
| **δ** | phantom crossing w < -1 실측 | SQMH L0/L1 falsified |
| **ε** | A04 |w_a| ≈ 0.5 (~8σ 분리) | alt-class 강력 지지 |

## 8인팀 사전 대응 전략

### 시나리오 α (강화): SQMH 최우호

- C11D/C28 ≥ 3σ 분리 → L5 Fisher 예측 (3.9σ, 2.9σ) 실현
- PRD Letter 재검토 조건:
  - L6-E1/E2 marginalized Δ ln Z ≥ +5 (STRONG)
  - amplitude-lock 이론 강화 필요
- 대응: 즉시 PRD Letter 전환 초안 준비

### 시나리오 β (유지): 현재 경로 継続

- JCAP 투고 유지
- §5 DR3 업데이트 + §8.7 데이터 의존성 기록

### 시나리오 γ (역전): wₐ 부호 falsification

- SQMH 배경 수준 wₐ < 0 예측 실패
- 대응 옵션:
  1. arXiv negative result: "L5 evidence는 DR2 신호 과잉 fitting"
  2. Phase 7: wₐ > 0을 허용하는 SQMH 변형 탐색
  3. 포기 (데이터가 LCDM으로 복귀)
- 8인팀 사전 합의: γ 발생 시 Phase 7 없이 honest negative result 투고

### 시나리오 δ (phantom): SQMH L0/L1 falsification

- w < -1 실측 → SQMH 3가정 중 가정 2 (σ > 0 소멸만) 위반
- SQMH 근본 수정 필요 (L0 재설계)
- 8인팀 합의: 포기 결정 전 3개월 재검토

### 시나리오 ε (outlier A04): alt-class 지지

- A04 (volume-cumulative, λ_4=1-a^3) 특이점 지지
- SVD n_eff=1 클래스 단순화가 틀렸음을 의미
- 대응: A04 심층 분석, SQMH 이론 복잡화

## DR3 실행 명령

```bash
bash simulations/l6/dr3/run_dr3.sh
```

출력: simulations/l6/dr3/dr3_vs_l5_diff.json
