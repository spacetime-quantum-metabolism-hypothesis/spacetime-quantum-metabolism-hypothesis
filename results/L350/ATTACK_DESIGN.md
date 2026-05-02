# L350 ATTACK_DESIGN — PSZ2 cluster σ_cluster selection bias 검증

## 목적
Planck SZ-selected 카탈로그(PSZ2)에서 측정한 σ_cluster 값이 lensing-selected (CLASH, LoCuSS, weak-lensing 카탈로그) 표본에서 측정한 값과 일관한지를 비교하여, SZ 선택 효과(Malmquist-style hot-gas bias, cool-core bias, hydrostatic mass bias)가 σ_cluster 추정에 미치는 영향을 정량화한다.

## 가설
- H0 (null): PSZ2-기반 σ_cluster 와 lensing-기반 σ_cluster 가 통계적 오차 범위 내에서 일관.
- H1: 두 표본 간 유의한 편차 존재 → SZ-selection bias 가 SQMH σ 측정에 영향.

## 데이터 방향 (값 절대 명시 금지)
- Planck PSZ2 공식 카탈로그 (Planck Legacy Archive).
- Lensing-selected 비교 표본: weak-lensing mass-calibrated cluster catalogs (예: CLASH, LoCuSS, HSC, KiDS-cluster) — 어느 것을 쓸지 8인 팀 토의에서 결정.
- 질량-overlap 영역만 매칭 (질량 cut, redshift cut 은 팀이 도출).

## 분석 방향
1. 두 표본의 σ_cluster 분포 추정 (kernel density / hierarchical Bayesian — 팀 자율).
2. 일관성 검증 통계 (KS, Anderson-Darling, hierarchical posterior overlap — 팀 자율).
3. selection 함수 모델링 (PSZ2 completeness, lensing S/N cut) 후 deconvolution.
4. Hydrostatic mass bias (1−b) 의 σ 측정 영향 분리.

## 팀 구성 원칙
- 8인 이론/분석 팀: 역할 사전 지정 금지. 자유 접근.
- 4인 코드리뷰 팀: 데이터 로딩·통계·플로팅·문서 자율 분담.
- 수식·파라미터 값 사전 제공 금지 (CLAUDE.md 최우선-1).

## 통과 기준 (방향만)
- 두 표본 σ_cluster 의 일관성 정량 지표 + uncertainty.
- selection bias 보정 후 잔차 보고.
- AICc/BIC 패널티 명시.

## 실패 시 처리
- 시뮬레이션 실패 → 코딩 버그 우선 의심 → 4인 코드리뷰 → 재실행.
- 결과가 사전 기대와 다르면 정직하게 base.fix.md 에 기록.
