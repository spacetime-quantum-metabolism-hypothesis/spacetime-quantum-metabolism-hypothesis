# L350 REVIEW

## CLAUDE.md 정합성 점검
- [최우선-1] 방향만 제공 — ATTACK_DESIGN/NEXT_STEP 에 수식·파라미터 값 0건. PASS.
- [최우선-2] 이론/분석은 8인 팀 독립 도출 — 역할 사전 지정 없음. PASS.
- 시뮬레이션 병렬 실행 원칙 명시. PASS.
- 비공식 추정값 금지 명시. PASS.
- 시뮬레이션 실패 시 코드 버그 우선 의심 명시. PASS.
- AICc 패널티 명시. PASS.

## 잠재 위험
- PSZ2 vs lensing 표본 질량·redshift overlap 좁을 가능성 → 통계력 부족 위험. 팀이 사전 검토 필요.
- Hydrostatic mass bias (1−b) 의 prior 가 σ 측정에 직접 들어감 → marginalization 필요.
- Lensing 표본 자체의 selection (orientation bias, projection effects) 도 별도 점검 필요.
- SZ-flux Malmquist 효과를 단순 cut 으로 처리하면 잔차 bias 잔존.

## 정직 한국어 한 줄
PSZ2 와 lensing-selected 표본이 σ_cluster 에서 일관한지 아직 모르며, 본 L350 은 selection 효과를 정직하게 분리 보고하는 것이 목표지 LCDM 또는 SQMH 어느 한쪽을 옹호하는 것이 아니다.
