# L348 ATTACK_DESIGN — LoCuSS σ_cluster 분포 추출

## 목표
LoCuSS (Local Cluster Substructure Survey) Smith+2016 / Okabe+2016 50+ cluster sample 에서
SQT 우주적 대사 표면밀도 σ_cluster 의 분포를 정량 (mean ± std) 한다.

## 배경 / 동기 (방향만)
- L300 계열에서 단일/소수 클러스터 (Coma, A1689 등) σ_cluster 단편 측정 누적.
- 50개 규모 균질 sample 에서 mean ± std 가 나와야 "σ_cluster 가 universal constant 인가, 환경 의존인가" 의
  통계적 1차 답이 가능.
- LoCuSS 는 0.15 < z < 0.30 X-ray-selected 50 cluster, Subaru weak-lensing M(<r) profile 균질 공개.

## 입력 데이터
- 1차 소스: Okabe & Smith 2016 (MNRAS 461, 3794) 50 cluster WL mass profile 표.
- 보조: Smith+2016 LoCuSS overview, Martino+2014 X-ray.
- 형식: cluster id, z, M_500, R_500, M(<R_2500), M(<R_500), M(<R_vir) 추출.

## 정의 (방향)
- σ_cluster := SQT 표면밀도 정의 (n0 μ-product, plank scale, surface density 차원).
- 방법: 각 cluster 의 enclosed-mass profile 로부터 SQT 차원맞춤으로 σ_i 계산.
- 수식 결정은 팀 자율 (CLAUDE.md 최우선-1: 수식 사전 지정 금지).

## 작업 분담 (5인 자율)
- 5인 팀이 자율적으로:
  1. LoCuSS 표 디지털화 / CSV
  2. σ_i 계산 코드
  3. 분포 통계 (mean, std, median, MAD)
  4. 환경 의존성 sanity check (M_500, z 와의 상관)
  5. 코드 리뷰

## 산출 기준
- N ≥ 50 cluster
- σ_cluster mean ± std (1σ)
- histogram + scatter (σ vs M_500, σ vs z)
- 외곽치 (>3σ) 분리 보고

## Stop / Kill
- N < 40 cluster 데이터 확보 실패 → 정직 KILL, 보조 sample (CLASH 25, HSC-SSP) 로 plan B.
- σ_i 의 std/mean > 1 (분포가 너무 넓어 universal constant 해석 불가) → 환경 의존 모델 분기.

## 정직성 규칙
- CLAUDE.md 따른다. 수식 결과가 base.md 와 다르면 base.fix.md 에 기록.
- 50 cluster 중 일부 누락 시 누락 사유 명시.
