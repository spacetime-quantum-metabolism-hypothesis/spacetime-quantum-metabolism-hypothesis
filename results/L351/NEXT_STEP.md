# L351 NEXT_STEP

## 즉시 단계
1. 데이터 확보
   - Bullet (1E0657-558): Clowe+2006 κ map (공개), Markevitch X-ray 표면휘도.
   - Abell 520: Jee+2014 HST κ map, Clowe+2012 peak 표, Mahdavi+2007 X-ray.
   - 두 cluster 모두 동일 grid (arcsec → kpc 변환) 로 재샘플.

2. 응답 함수 자율 도출 (6인 팀, 수식 사전 지정 금지)
   - depletion zone 의 baryon 성분 가중 (gas 대 stars) 자유 도출.
   - 충돌 단계 / 시간상수 / 비선형 응답 여부 자율.
   - 파라미터 수 최소화. AICc 패널티 사전 명시.

3. 동시 fit
   - 단일 σ_cluster (L348 결과) 고정 시도가 1차.
   - 실패 시 σ 자유화 → 단일 σ universality 정합 검사.

4. 비교 baseline
   - LCDM particle DM (단순 collisionless), MOND/TeVeS, ΛCDM + self-interacting DM.
   - 동일 metric 으로만 비교.

## 산출물
- /Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L351/
  - data/ (재샘플 κ, Σ_gas, Σ_★ for 양 cluster)
  - fit_results.json (parameters, χ², AICc, Bayes factor)
  - figures/ (κ overlay, residual map)
  - report.md (정직 결론)

## 후속 분기
- PASS 양쪽: L352 — 5+ merging cluster sample (MACS J0025, A2744, A1758, El Gordo, DLSCL J0916) 확장.
- Bullet PASS / Abell 520 FAIL: SQT 의 "baryon-following depletion" 단순 그림 수정 필요 — base.fix.md 기록.
- 양쪽 marginal: σ universality 재검토 (L348 분포 폭 → 환경 의존 모델로 분기).

## 일정 (제안)
- D1: 데이터 디지털화 / grid 재샘플
- D2: 응답 함수 자율 도출 + 단일 cluster sanity (Bullet 만)
- D3: 동시 fit + AICc + 코드리뷰 4인
- D4: 비교 baseline + 정직 보고서

## 위험 / 사전 점검
- Abell 520 lensing peak P3 의 통계적 유의도는 Clowe+2012 vs Jee+2014 사이 일부 disagreement 존재 — 두 분석 모두 인용.
- κ map 단위 일관성: Σ_crit (z_l, z_s) 정의 통일.
- 별 광도 → stellar mass 변환의 M/L 계열 가정은 자유 파라미터 아님 (Bell+2003 fix), fit 외부에 고정.
