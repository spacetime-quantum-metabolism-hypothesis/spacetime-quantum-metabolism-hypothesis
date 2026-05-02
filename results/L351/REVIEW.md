# L351 REVIEW — 사전 비판 (pre-mortem)

## 핵심 위험: Abell 520 가 SQT 도전이 될 가능성

### 1. 표면적 모순
- Bullet (P27 PASS, L291): lensing peak 가 가스(X-ray)와 분리, 별/galaxies 동행.
  → "depletion zone follows baryons" 그림에서 baryon = stars 우세 응답.
- Abell 520 dark core (Clowe+2012, Jee+2014): lensing peak P3 가 X-ray gas 동행,
  별빛(galaxies) 과는 분리.
  → 같은 그림에서 baryon = gas 우세 응답.
- 단일 응답 함수로 양쪽을 동시에 살리려면 **충돌 동역학 의존성** (시간, 속도, 가스 thermal 상태)
  이 함수 안에 들어와야 함. 자유도 증가 → AICc 패널티 위험.

### 2. CDM/MOND 와의 비교 — SQT 만의 위험은 아님
- 표준 collisionless CDM 도 Abell 520 dark core 자연 재현 실패 (Jee+2012/2014).
- MOND/TeVeS 는 Bullet 에서 이미 알려진 곤란.
- 따라서 "Abell 520 = SQT 만의 도전" 은 아니다. 그러나 SQT 가 "baryon-following" 으로 Bullet 을
  단순 PASS 했다면, Abell 520 에서는 그 그림이 직접 깨진다는 점은 SQT 에 더 구조적 부담.

### 3. P27 PASS 등급 재검토 필요성
- L291 / L314 의 P27 PASS 는 정성/차원적 PASS 였다 (정량 fit 미실시).
- L351 동시 fit 에서 Bullet 자체 χ² 가 나빠지면, P27 등급 자체가 "정성 PASS → 정량 marginal"
  로 강등될 수 있음. 정직히 기록.

### 4. σ_cluster universality (L348) 와의 충돌 가능성
- Abell 520 dark core 의 amplitude 가 단일 σ 와 정합하지 않으면, L348 의
  "σ universal" 1차 결론이 흔들림. 두 결과 동시 정합 또는 동시 수정.

### 5. 데이터 자체의 불확실성
- Abell 520 P3 peak 의 유의도는 분석마다 다름 (Clowe+2012 5.5σ vs Jee+2012 보수적).
- κ map 의 source-redshift 분포 가정에 민감.
- "관측 자체가 robust 한가" 를 fit 결과 해석 전 확정해야 한다.

## 권장 정직성 가드
- G1. Bullet single-cluster fit 을 먼저 완성 → P27 정량 등급 확정 후 Abell 520 추가.
- G2. "동시 fit 성공" 주장은 단일 응답 함수 + 단일 σ + AICc 개선 모두 충족 시에만.
- G3. 응답 함수가 충돌-단계 의존성을 도입하면 그 단계 변수 (e.g. time-since-pericenter) 가
     관측에서 독립 추정 가능한가 (X-ray bow shock, radio relic) 명시.
- G4. 부분 성공 / 부분 실패는 base.fix.md 에 분리 기록. 결과 왜곡 금지.
- G5. "SQT 가 Abell 520 도 자연 설명" 결론은 5+ cluster (L352) 까지 reproducibility 확인 후에만.

## 사전 결론 (실행 전)
- Abell 520 는 "SQT 의 결정적 KILL" 도, "자동 PASS" 도 아니다.
- 단순한 baryon-following 그림은 위험. 충돌 동역학 의존 응답이 필요할 가능성 ≥ 50%.
- 결과가 나오기 전에 "SQT 가 Bullet + Abell 520 둘 다 푼다" 라고 외부에 주장 금지.

## 정직 한국어 한 줄
Abell 520 의 dark core 는 단순한 baryon-추종 SQT 그림에 정면 도전이며, Bullet PASS 와 동시에 살리려면 충돌 동역학에 의존하는 응답 함수가 필요할 가능성이 높고, 그 결과는 실행 전에는 PASS 도 KILL 도 아니다.
