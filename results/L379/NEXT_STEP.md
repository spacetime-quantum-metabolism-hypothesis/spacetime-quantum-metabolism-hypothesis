# L379 NEXT_STEP — Causet meso 후속 단계

날짜: 2026-05-01

---

## 1. 정직 한국어 한 줄

L379 가 Causet 를 meso pillar 후보로 4/5 조건부 PASS 시켰지만 K2 (BDG action 의 meso 환원성) 가 8인 4:4 로 미결이므로, 다음 세션은 K2 단일 과제 또는 비어버린 micro pillar 자리의 후보 1종 ATTACK 중 하나로 분기한다.

---

## 2. 분기 트리

### 분기 α — K2 단일 과제 (조건부 PASS → 정식 채택 경로)
- α1. BDG action 의 사슬 카운팅이 coarse-grained 평균량으로 *명시 작용* 형태를 유지하는지 단일 검증.
- α2. 결과가 "유지" 면 Causet meso pillar 정식 채택. "약화" 면 K2 FAIL → meso 도 폐기, 분기 β 강제.
- α3. 본 분기는 이론적 검증이며 코드 산출물 없음. 8인 리뷰 (Rule-A) 단일 세션.

### 분기 β — micro pillar 공백 채움 (Causet 폐기 가정)
- β1. 후보군: LQG spin network, Group Field Theory, Wolfram hypergraph rewriting, Cortês–Smolin energetic causal set, set/order-theoretic graph.
- β2. 후보별 독립 세션, 각각 L379 동일 양식 (ATTACK_DESIGN/REVIEW/NEXT_STEP, 8인 자율 토의, 게이트 5종).
- β3. round-robin 또는 사용자 우선순위 지정.

### 분기 γ — meso 가설 추가 강화 (K2 PASS 가정 후)
- γ1. Λ swerves 진폭이 coarse-graining 평균화로 얼마나 억제되는지 토이 시뮬 (Python, multiprocessing spawn pool, ≥4 워커, OMP/MKL/OPENBLAS=1).
- γ2. 관측 가능 채널 (DESI w(z) 변동) 과 비교 가능한 임계 진폭 추정.
- γ3. 본 분기는 코드 산출물 발생 → 4인 코드 리뷰 (Rule-B) 필수.

---

## 3. 즉시 후속 (어느 분기든 공통)

- L379 REVIEW 결론을 base.fix.md 또는 동급 정직 로그에 기록. "거의 채택됨" 류 회색 표현 금지. **조건부 PASS 4/5, K2 미결** 명시.
- L364 KILL-soft, L366 prior 1위, L379 meso 4/5 의 세 결론을 "층별 정합" 으로 명시 (micro KILL / meso 조건부 PASS).
- 본 세션은 L46~L363, L365, L367~L378 미참조. 다음 세션도 동일 독립성 유지 가능.

---

## 4. 데이터 / 시뮬 요구

- 분기 α: 데이터 fitting 불요. 이론 검증.
- 분기 β: 후보별 첫 세션은 이론 매핑 단계 → 데이터 fitting 불요.
- 분기 γ: sprinkling 토이 코드 (Python, multiprocessing.get_context('spawn').Pool, ≥4 워커, 워커당 OMP/MKL/OPENBLAS_NUM_THREADS=1, 모델별 worker 분리, 전역 singleton 금지). 데이터는 DESI w(z) 공식 채널 사용 (CobayaSampler bao_data) — 임의 추정값 금지.

---

## 5. 시간 예산

- 분기 α (K2 단일): 1 세션.
- 분기 β (micro 후보 round-robin): 후보당 1 세션, 5 세션 총.
- 분기 γ (swerves 시뮬): 1~2 세션 + 4인 코드 리뷰.

---

## 6. 리뷰 정책

- 분기 α, β: 이론 클레임 → 8인 리뷰 (Rule-A).
- 분기 γ: 코드 + 이론 → 8인 리뷰 + 4인 코드 리뷰 동시.
- 어느 분기든 역할 사전 지정 금지, 자율 분담만 인정.

---

## 7. 권장 우선순위 (정직)

1. **분기 α** 우선. K2 가 미결인 채로 분기 β/γ 로 진행하면 micro/meso 양쪽이 동시에 흔들려 결론 추적 불가.
2. K2 PASS 시 분기 γ 진입.
3. K2 FAIL 시 분기 β 강제 (Causet meso 도 폐기).
