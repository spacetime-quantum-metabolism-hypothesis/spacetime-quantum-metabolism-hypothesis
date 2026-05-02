# L348 NEXT_STEP

## 즉시 (D+0)
1. Okabe & Smith 2016 MNRAS 461 3794 의 Table 표 (50 cluster) 다운로드.
   - VizieR cat: J/MNRAS/461/3794
2. CSV 생성: `data/L348/locuss50.csv` (id, z, M_500, R_500, M_2500, M_vir, ref).

## D+1
3. 5인팀 자율 토의 → σ_cluster 추출 식 확정 (CLAUDE.md 최우선-1: 사전 지정 금지).
4. `simulations/L348/sigma_cluster_locuss.py` 작성 + 코드리뷰 (4인 자율 분담).

## D+2
5. 50 cluster σ_i 일괄 계산.
6. 통계: mean, std, median, MAD, skewness.
7. 산점도: σ vs (M_500, z, R_500).
8. histogram + bootstrap 1000 회로 mean 의 신뢰구간.

## D+3
9. REVIEW.md 작성 (8인 자율 리뷰).
10. base.md / base.fix.md 갱신.

## 후속 (L349~)
- L349: CLASH 25 cluster 교차검증.
- L350: HSC-SSP/DES 대량 sample 확장.
- 환경 의존성 발견 시 → SQMH-σ(M_500, z) 모델링 분기.

## 데이터 진입 실패 시 plan B
- Okabe+2016 표 접근 불가 → Umetsu+2020 HSC-SSP cluster catalog (~1900 cluster) 의 M(<r) profile 부분 사용.
- Plan B 시 KILL 보고 후 재설계.
