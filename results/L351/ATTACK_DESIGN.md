# L351 ATTACK_DESIGN — Bullet (P27 PASS) ↔ Abell 520 (train wreck) 일관성

## 목표
SQT (Spacetime Quantum metabolism Theory) 의 "depletion zone follows baryons" 그림이
- (a) Bullet cluster (1E0657-558): lensing peak 가 가스(X-ray)와 분리되어 별 군집 (galaxies) 따라감 — P27 PASS 로 분류됨,
- (b) Abell 520 ("train wreck" / "dark core"): lensing peak 가 X-ray 가스와 동행하나 별빛(galaxies)과는 분리 — DM-particle 모델에도 곤혹스러운 anomaly,
양쪽을 동시에 모순 없이 설명 가능한지 정직하게 검증한다.

## 배경 / 동기 (방향만)
- L291 / L314 에서 Bullet 은 "차원적/정성적 PASS" 로 보고됨. 정량 fit 은 미실시.
- Abell 520 (Mahdavi+2007, Jee+2012, Clowe+2012, Jee+2014) 는 lensing 핵이 collisionless 별 군집과 분리.
  CDM 단순 충돌 시뮬레이션은 자연 재현 실패. MOND-class 도 곤란.
- SQT 의 "depletion zone" / "대사공동" 이 baryon (gas + stars) 분포를 따라간다는 1차 직관이라면,
  Bullet 에서 stars-tracking 과 Abell 520 에서 gas-tracking 은 표면적으로 모순.
- 둘을 살리는 길은 (방향만) ① 충돌 단계 (collision phase / time-since-pericenter) 에 따른
  baryon-component 별 가중 차이, ② 가스/별 비율과 국소 ρ_b 에 대한 비선형 응답,
  ③ depletion zone 의 "기억" 시간상수 (relaxation) — 구조 자율 도출.

## 핵심 질문
Q1. SQT 의 baryon-coupled depletion 은 "gas vs star" 어떤 baryon 성분에 더 강하게 응답하는가?
   해석/유도는 팀 자율. 이 결정이 Bullet 과 Abell 520 의 lensing 분포를 동시 결정.
Q2. Abell 520 의 dark core (X-ray 동행) 가 SQT 에서 (i) 자연 예측, (ii) 허용되지만 fine-tune,
   (iii) 명시적 위반 — 셋 중 어디인가?
Q3. 단일 σ_cluster (L348 결과) 와 정합한가? σ 가 cluster-level universal 이면 dark core
   amplitude 도 예측 가능해야 한다.

## 입력 데이터
- Bullet 1E0657-558: Clowe+2006 (lensing κ map), Markevitch+2002/2004 (X-ray), 공개 FITS / 표.
- Abell 520: Jee+2014 (HST WL), Clowe+2012 (lensing peak P3 'dark core' 5.5σ), Mahdavi+2007.
- 좌표/거리: 양 cluster z, D_A.
- 형식: 2D κ(x,y) map, gas Σ_gas(x,y) (X-ray 디프로젝션), stellar Σ_★ (광학 luminosity).

## 작업 분담 (6인 자율)
6인 팀이 역할 사전 지정 없이 자율 분담:
- Bullet & Abell 520 lensing/X-ray/광학 데이터 수집·표준화
- SQT depletion-zone 응답 함수 자율 도출 (수식 사전 지정 금지 — CLAUDE.md 최우선-1)
- 두 cluster 동시 fit (공통 파라미터)
- AICc 패널티 명시 (파라미터 추가 시)
- 코드 리뷰 4인 자율 분담 (Rule-B)

## 산출 기준
- 두 cluster 의 lensing peak 위치 χ² (또는 Bayes factor) 동시 보고
- Bullet PASS 가 유지되는가? (퇴행 검사)
- Abell 520 dark core 의 peak amplitude / 위치 SQT 예측 vs 관측 σ
- 단일 σ_cluster (L348 mean) 와의 정합 또는 어긋남 정량

## Stop / Kill
- K-A. Bullet 을 살리는 응답 함수가 Abell 520 dark core 를 ≥3σ 어긋나게 예측 → SQT 도전, 정직 보고.
- K-B. 두 cluster 동시 fit 이 cluster-별 독립 σ 를 요구 (universal σ 위반) → L348 결과와 충돌, 정직 보고.
- K-C. 응답 함수가 자유 파라미터 ≥3 개로 부풀어 AICc Δ < 0 → 모델 단순화 또는 KILL.

## 정직성 규칙
- CLAUDE.md 전면 적용. 결과가 base.md 주장과 다르면 base.fix.md 기록.
- "SQT 가 두 cluster 모두 설명" 결론은 단일 응답 함수 + 단일 σ 로 동시 fit 성공한 경우만 허용.
- 부분 성공 (Bullet PASS, Abell 520 marginal) 은 정직히 분리 표기.
- MOND/CDM 비교는 동일 데이터·동일 metric 으로만.
