# L348 REVIEW — 사전 자가 점검

## 정직 한국어 한 줄
LoCuSS 50 cluster σ_cluster mean ± std 추출은 데이터 접근만 확보되면 즉시 가능하지만, 본 세션에서는 ATTACK_DESIGN/NEXT_STEP 만 수립하고 실측은 다음 세션에서 5인팀 자율 도출로 수행한다.

## 위험 점검
- (R1) Okabe+2016 표 형식이 M_500 단일컬럼 only 일 경우 R<R_500 enclosed-mass profile 부재 → σ_i 적분이 단일 스칼라로 축소. 해석 한계 명시 필요.
- (R2) 50 cluster 의 z 가 0.15-0.30 좁은 구간 → z 의존성 검증 통계력 약함.
- (R3) σ_cluster 정의가 팀 자율 도출이므로 결과 비교를 위한 L300 계열과의 정의 일관성 사전 확정 필요.
- (R4) WL mass uncertainty (~30% per cluster) 가 σ_i 분포 폭에 직접 전파 → intrinsic scatter 와 measurement scatter 분리 (intrinsic σ via maximum-likelihood) 필수.

## CLAUDE.md 위반 검사
- 최우선-1 (수식 금지): ATTACK_DESIGN/NEXT_STEP 모두 수식 0줄 PASS.
- 최우선-2 (팀 독립도출): 역할 사전 배정 금지 → 5인/4인/8인 자율 분담 명시 PASS.

## 수락 기준
- mean ± std 산출 + bootstrap CI + 환경 의존 sanity → 수락.
- N<40 또는 std/mean>1 → 정직 KILL 후 plan B.

## 다음 세션 진입 조건
- `data/L348/locuss50.csv` 확보.
- CLAUDE.md 재확인.
