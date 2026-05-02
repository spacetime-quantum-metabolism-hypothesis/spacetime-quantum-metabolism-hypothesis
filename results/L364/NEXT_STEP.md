# L364 NEXT_STEP — CST ↔ n-field 후속 단계

날짜: 2026-05-01

---

## 1. 정직 한국어 한 줄

CST 직접 매핑이 KILL-soft 로 판정되면, 다음 세션은 "CST coarse-grained density → n-field" 의 meso 경로 탐색 또는 CST 를 버리고 다른 micro 후보 (loop quantum gravity spin network, group field theory, energetic causal set, set-theoretic graph) 로 분기한다.

---

## 2. 분기 트리

### 분기 A — KILL-soft (매개층 필요)
- A1. Meso pillar 후보로 CST 재분류. n(x) = ⟨local element count⟩ 정의 가능성 별도 세션 (L365 후보).
- A2. SQT 측에서 n-field 가 Poisson 분포인지 균질인지 사전 강제 결정 필요. L40 계열 결과 참조 금지(독립).
- A3. Coarse-graining scale 자유도 추가 시 AICc 패널티 견적.

### 분기 B — KILL-hard (인과 순서 비환원)
- B1. CST 폐기, micro 후보 다음 라운드:
  - LQG spin network (이산 면적/부피 → n-field 와의 연결)
  - Group Field Theory (2nd quantised CST)
  - Wolfram hypergraph rewriting
  - Energetic causal set (Cortês-Smolin)
  - Set-theoretic / order-theoretic graph
- B2. 후보별 독립 세션, 각각 L364 와 동일한 ATTACK_DESIGN 양식.

### 분기 C — PASS (직접 매핑 성립, 가능성 낮음)
- C1. BD action 의 n-field 동역학 환원 검증. Phase 5 수준 수치 시뮬 (병렬 ≥4 워커).
- C2. Lorentz invariance 깨지지 않는지 sprinkling 분포 자체 점검.
- C3. SQT 메타볼리즘 flux 가 CST 사슬 카운팅과 일치하는지 토이 모델.

---

## 3. 즉시 후속 (어느 분기든 공통)

- L364 REVIEW 결과를 8인 리뷰 (Rule-A) 에 회부. CST pillar 결론은 이론 클레임이므로 4인 코드 리뷰가 아닌 8인 이론 리뷰.
- 결론은 base.fix.md 에 정직 기록. "거의 매핑됨" 류 회색 표현 금지.
- 다음 라운드는 L365 로 번호 진행. CST 결과를 L46~L363 과 무관하게 독립 평가 유지.

---

## 4. 데이터/시뮬 요구

- 직접 매핑 검증에 데이터 fitting 불요 (이론 매핑 단계).
- 분기 C 진입 시에만 CST sprinkling 토이 코드 (Python, multiprocessing spawn pool, ≥4 워커, OMP/MKL/OPENBLAS=1).

---

## 5. 시간 예산

- 분기 판정: 1 세션 (L364 본).
- 분기 A meso 탐색: 2~3 세션.
- 분기 B 후보 5종 round-robin: 5 세션.
- 분기 C 토이 시뮬: 1~2 세션 + 8인 리뷰.
