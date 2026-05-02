# L350 NEXT_STEP

## 즉시 단계
1. PSZ2 공식 카탈로그 다운로드 경로 확정 (Planck Legacy Archive). 비공식 mirror 금지.
2. Lensing-selected 비교 카탈로그 후보 리스트업 후 8인 팀 토의로 1개 또는 2개 선정.
3. 질량·redshift overlap 영역 정의 — 팀 자율 도출.
4. selection 함수 (PSZ2 completeness map, lensing S/N) 문서 수집.

## 코드 단계
5. 데이터 로더 작성 (병렬 multiprocessing spawn, OMP/MKL/OPENBLAS_NUM_THREADS=1).
6. σ_cluster 추정 파이프라인 — 8인 팀이 방법 자율 선택.
7. 일관성 통계 + selection-corrected 비교.
8. 4인 코드리뷰 자율 분담.

## 산출
9. 결과를 results/L350/ 하위에 기록. 기대와 다르면 base.fix.md.
10. AICc/BIC 패널티 명시. 단순 모델 우선.

## 금지
- 수식·계수·임계값 사전 제공 금지.
- 역할 사전 배정 금지.
- 비공식 데이터 추정값 금지.
