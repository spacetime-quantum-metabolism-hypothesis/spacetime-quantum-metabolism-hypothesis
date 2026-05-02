# L417 Next Step — 8인 팀 정량화 경로 설계

## 원칙 (CLAUDE.md 최우선-1 준수)
- 방향만 제시. 수식/파라미터 값 일체 미제공.
- 8인 팀이 독립 도출.
- 4인 팀 코드 검증 후 채택.

## 정량화 목표
quantitative offset prediction Δx_SQT in kpc → Clowe 2006 의 ~150 kpc 와 비교.

## 탐색 방향 (3 채널, 8인 토의 합의)

### 채널 (i) — Depletion zone dynamic timescale
**방향**: SQT depletion zone 이 baryon 위치를 *얼마나 빠르게 추적*하는가.
- 물리 현상 이름: "absorption zone re-equilibration"
- 비교 timescale: cluster 충돌 통과시간
- 결과 형태: τ_q / τ_cross 부등식 → tracking 정확도 → offset residual

수학 분야: relaxation kinetics, characteristic length scales.
*수식, 계수 일체 사전 제공 금지.* 팀 자율 도출.

### 채널 (ii) — Collision-induced σ₀(t) modification
**방향**: 충돌 중 시공간 양자 흡수 단면적이 *동적으로* 변하는가.
- 물리 현상 이름: shock-induced absorption modulation
- 환경 변수: local baryon density, kinetic energy density
- 결과 형태: Δσ₀/σ₀ 의 spatial map → ρ_eff peak shift

수학 분야: 환경 의존 단면적 functional, perturbation around quiescent σ₀.
*형태 제시 금지.* 팀이 SQT 공리에서 직접 도출.

### 채널 (iii) — Lensing peak vs gas peak quantitative separation
**방향**: weak-lensing convergence κ(x) 와 X-ray surface brightness 의 separation 을 *수치적으로* 예측.
- 입력: Bullet 충돌 기하 (subcluster 위치, 속도, mass), gas mass distribution, galaxy distribution
- 출력: peak_κ (예측) - peak_gas (관측) in kpc
- 비교: Clowe 2006 = 150 ± 30 kpc (8σ)

수학 분야: convergence integral, projected density mapping.

## 통합 path
세 채널 모두 자체적으로 정량 산출 후 — 일관성 검증 — paper/base.md §4.1 격상 결정.

## Falsification 조건 (사전 명시)
- 예측 offset ∈ [120, 180] kpc → **PASS_STRONG_QUANTITATIVE** 격상.
- 예측 offset ∈ [50, 250] kpc 외 → **PASS_QUALITATIVE_ONLY** 정직 강등.
- 예측 부정 (offset < 50 kpc) → **TENSION** 표시 + caveat 강화.
- 예측 도출 불가 (formalism 불완전) → **현재 PASS_STRONG → PASS_QUALITATIVE 강등** + base.md 정직 기록.

## 4인 팀 인계
다음 단계 (REVIEW.md): 4인 팀 자율 분담으로 simulations/L417/run.py 구현 + 검증.
