# L364 REVIEW — CST ↔ n-field 직접 매핑 판정

날짜: 2026-05-01
세션: L364 (독립). L46~L363 결과 미참조.

---

## 1. 정직 한국어 한 줄

Causal Set Theory 는 SQT n-field 의 micro pillar 가 아니라 meso 후보이며, 직접 매핑(CLAIM-A,B,C 모두)은 인과 순서의 비환원성·차원 불일치·LI 강제 조건 때문에 KILL-soft 판정으로, 매개 coarse-graining 층 없이는 채택 불가하다.

---

## 2. 공격축별 결과

### 축 1 — 차원/의미
- CST element: dimensionless event. n-field: density-like scalar.
- 단위계 변환은 fundamental length scale (CST 의 sprinkling density 역수) 도입 시에만 가능.
- 그 length scale 자체가 새 자유도 → micro 가 아니라 phenomenological 파라미터화.
- 결과: FAIL (직접 매핑 불성립).

### 축 2 — 인과 순서 보존
- partial order 는 2-인자 관계, n(x) 는 1-인자 스칼라. 정보론적으로 후자에서 전자 복원 불가능.
- 카운터 예: 동일 n 분포가 서로 다른 partial order 와 호환 가능 (degeneracy).
- 결과: FAIL-hard. 이 한 축만으로도 직접 매핑 KILL.

### 축 3 — Lorentz invariance
- CST 의 LI 보존은 Poisson sprinkling 의 통계적 LI 에 의존. 균질 격자 n-field 는 격자 방향 선호 → LI 깨짐.
- n-field 를 Poisson 으로 강제하면 SQT 측 가정 변경 필요 → 독립성 훼손.
- 결과: CONDITIONAL FAIL.

### 축 4 — Coarse-graining
- 매개층 (예: n = 국소 element 밀도 평균) 도입 시 매핑 가능성 회복 신호.
- 그러나 정의상 micro pillar 자격 박탈, meso 로 강등.
- 결과: micro 자격 KILL, meso 후보로만 생존.

### 축 5 — Action / dynamics
- BD action 의 사슬 카운팅과 n-field metabolism flux 는 같은 물리량의 두 표현이 아니라 별개 관측가능량.
- 한쪽에서 다른 쪽으로의 환원 경로 미존재 (현재 문헌 + 본 세션 자율 도출 모두).
- 결과: FAIL.

---

## 3. 최종 판정

- CLAIM-A (element=n 격자값): KILL (축 2,5).
- CLAIM-B (sprinkling density=n(x)): KILL-soft (축 1,3,4. coarse-graining 시 부분 부활).
- CLAIM-C (BD action → n 동역학): KILL (축 5).
- 종합: CST 는 SQT n-field 의 micro pillar 아님. 단, coarse-grained meso 층으로는 후속 탐색 가치 있음 (NEXT_STEP 분기 A).

---

## 4. 팀 합의

- 6인 자유 토의 결과: 6/6 합의 "직접 매핑 불성립".
- 분기 A (meso 재분류) 4/6 지지, 분기 B (CST 폐기 후 다른 micro 후보) 2/6 지지.
- 다수 의견대로 다음 세션은 분기 A 또는 분기 B 중 사용자 선택에 따라 진행.

---

## 5. 과적합 방지 점검

- 본 세션은 데이터 피팅 없음. 파라미터 추가 없음. AICc 비검토.
- "거의 매핑된다" 류 회색 표현 회피. KILL-soft 명시.
- L46~L363 결과 미참조 확인 (독립성 유지).

---

## 6. 다음 액션

- NEXT_STEP.md 의 분기 A 또는 B 중 사용자 결정 대기.
- 본 결론은 8인 이론 리뷰 (Rule-A) 권장. 코드 산출물 없으므로 4인 코드 리뷰 불필요.
