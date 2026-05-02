# L346 REVIEW — 비단조 σ_0(z) theory-prior 진단 결과

8인 팀 자율 분담. 역할 사전 지정 없음. CLAUDE.md 최우선-1 (방향만, 지도 금지) 준수.

---

## 자료 기반 사실 (논쟁 불가)

### F1. 비단조성의 *역사적 등장 시점* (git/results 추적)
- L67 REVIEW (results/L67/REVIEW.md): σ_0 evidence 의 **비단조** 패턴이
  **데이터 fit 결과** 로 처음 보고. 인용:
  - "σ_0 와 밀도 관계가 비단조"
  - "σ_0 비단조 패턴은 *부분적으로 fit artifact* 일 가능성"
  - "본 이론을 살리려면 (A) 비단조 σ_0(env) 메커니즘 ..."
- L68 REVIEW: "남은 ~1 dex 잔차는 진짜 물리적 비단조성".
- L67 시점은 4-pillar 정식화(a4 emergent metric pillar 도입은 L337 에서
  *5번째 pillar 로 OPEN* 상태)보다 **이전**.

→ **시간선 사실**: 데이터에서 비단조 발견이 먼저, "비단조를 살릴 메커니즘 탐색"
이 그 다음. 이는 fit-driven discovery 의 정의에 부합.

### F2. SQT 4 pillar 의 명시적 비단조 예측 부재
results/L334 (RG b,c priori 도출 불가, pillar 4 ★★ 격하), L337 (micro 80% 상한,
a4 5번째 pillar OPEN), L338 (P17 Tier B V(n,t) derivation gate **미완**)
어디에도 "4 pillar → σ_0(z) 비단조 + 극값 위치 z_*" 형태의 *데이터 보기 전*
유도가 기록되어 있지 않다.

### F3. L345 와의 상호 참조
L345 (proper ln Z 비교) 는 "비단조 선호" 가 Akaike artifact 일 수 있음을
이미 인정 (A2). 즉 *통계적* 차원에서도 비단조 우세는 robust 하지 않다.

---

## 8 axis 평가 (자율 분담 결과 종합)

| Axis | 항목 | 등급 | 근거 |
|------|------|------|------|
| A1 | RG saddle pillar → 비단조 강제? | **L (Low)** | saddle 자체는 부호변화 *허용* 하나 *강제* 안 함. 단조 해 다수 공존. |
| A1 | Holographic pillar → 비단조 강제? | **0** | boundary entropy bound 는 σ_0 monotonicity 에 sign 미부여. |
| A1 | Z_2 pillar → 비단조 강제? | **L** | z-반사 대칭은 sym point 주변 even-fn 만 요구, 부호 변화 강제 아님. |
| A1 | a4 / 4번째 scaling pillar | **0 (OPEN)** | L337 에서 a4 micro origin OPEN. 비단조 예측 불가. |
| A2 | Prior vs Posterior timeline | **Posterior** | F1 의 git/results 자료. L67(데이터) → L68(잔차) → 메커니즘 탐색 순. |
| A3 | Counterfactual pillar 제거 | **약한 prior** | 어느 1 pillar 제거해도 비단조 *제거되지 않음* (즉 4 pillar 가 비단조의 원인이 아님). 정성 판정. |
| A4 | Bayesian theory-prior strength P(non-mono \| 4 pillars) | **L (≪ 0.5 정성)** | 4 pillar 만으로 비단조에 유의 prior 못 부여. 단조도 동등 허용. |
| A5 | P17 pre-registration 명시 여부 | **부분 명시 / Tier B 미완** | L338 P17 Tier B (V(n,t) derivation gate) 미완. Tier A 는 비단조 *형상 자체* 가 아니라 진폭/극값 *추정* 만 lock. |
| A6 | Alt-20 14-cluster drift 1자유도와 동일? | **부분 동일 가능성** | L5 SVD n_eff=1 의 1자유도가 비단조 형상의 한 표현일 수 있음. 독립 prediction 가치 약화. |
| A7 | Falsifier 강도 (DR3) | **M (medium)** | DR3 단조 관측 시 SQT 비단조 prior 위반은 가능. 단 prior 자체가 약하므로 "예측 falsified" 강도 낮음. |

전체 등급 합계: **L 5 / 0 2 / M 1 / Posterior 1**.

---

## Pillar 별 정성 prediction 등급 (요약 표)

| Pillar | σ_0(z) 비단조 *부호 변화* 강제 | 극값 위치 z_* 예측 | 종합 |
|---|---|---|---|
| 1. RG saddle | 허용하나 강제 X | 미예측 | L |
| 2. Holographic | sign 미부여 | 미예측 | 0 |
| 3. Z_2 | 대칭점 주변 even, 부호변화 X | 미예측 | L |
| 4. a4 / scaling (OPEN) | 미정 | 미정 | 0 |

→ 4 pillar 합산도 비단조의 **부호 변화** 를 강제하지 못한다.
극값 위치 z_*≈O(0.5) 는 *어느 pillar 에서도 a priori* 도출되지 않는다.

---

## 핵심 판정

### J1. 비단조성은 *prediction* 인가 *fit* 인가?
**대부분 fit, 부분적으로 retro-rationalized prediction.**

근거 종합:
- F1 시간선: 데이터 → 발견 → 메커니즘 탐색.
- A1 4 pillar 정성 평가: 비단조 *강제력* 어느 pillar 에도 없음.
- A4 Bayesian prior strength: 4 pillar 단독 prior 로는 비단조에 유의 가중치 못 부여.
- A5 P17 Tier B 미완: 비단조 형상 자체가 pre-reg lock 되어 있지 않음.
- L345 (독립 검증): proper ln Z 가 Akaike weight 의 비단조 우세를 무력화 가능.

### J2. SQT 의 등급 영향 (L346 한정 평가)
ATTACK_DESIGN A2 의 (c) 시나리오 ("post-hoc fit 확정") 에 가까움.
다만 *부분 prediction* 여지 (RG saddle 의 *허용*) 가 있어 완전한 (c) 는 아님.

L346 은 *진단* loop 이므로 본 round 에서 등급 확정 변경은 미수행.
다음 SYNTHESIS round 에서 다음 둘 중 하나 권고:
- 보수: 등급 -0.005 ~ -0.010 (pillar 4 ★★ 추가 격하 위험 인정).
- 적극: pillar 4 ★★→★ 격하 명문화, 등급 -0.015.

### J3. Paper / 저널 함의
- Sec 3 본문에서 "SQT 4 pillar 가 비단조성을 *예측한다*" 류 표현은
  **모두 약화 또는 삭제** 필요. 수용 표현:
  - "비단조성은 데이터에서 관측된 패턴이며, SQT 4 pillar 와 *모순되지 않는다*."
  - "비단조성을 falsifiable prediction 으로 lock 하기 위해서는 P17 Tier B
    (V(n,t) full derivation) 완료가 선행되어야 한다."
- PRL/PRD Letter 진입 조건 (L6 의 "Q17 완전 달성 OR Q13+Q14 동시 달성")
  여전히 **미달**. JCAP phenomenology 상한 유지.
- JCAP 영향: 본 round 정직 진단으로 +0~+1% 회복 가능. -1~-2% 위험은
  reviewer 가 비단조 prediction 주장을 의심할 때만 발생.

---

## 정직 한국어 한 줄

> **비단조 σ_0(z) 는 SQT 4 pillar 의 a priori 예측이 아니라 데이터에서 발견된 fit 이며, 4 pillar 는 그것을 강제하지 않고 단지 모순되지 않을 뿐이다.**

---

## 본 round 신뢰도 한계
- L67/L68 의 "비단조" 는 σ_0(env) 환경 의존성 차원. σ_0(z) 적색이동
  의존성과 *완전히 동치* 인지는 별도 mapping 검증 필요 (Next Step 참조).
- pillar 별 등급은 *정성* 판정. 수치적 P(non-mono | pillars) 계산은
  본 round 범위 밖 (수식 도출 금지 원칙 준수).
- 본 결론은 현재 git/results 상태 한정. P17 Tier B 가 추후 완수되어
  V(n,t) 로부터 비단조 z_* 가 *데이터 사용 없이* 도출되면 J1 재판정.
