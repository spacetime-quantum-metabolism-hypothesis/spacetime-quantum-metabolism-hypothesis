# L404 — ATTACK_DESIGN: 5th micro-axis (Causet vs GFT) decision-point

**Loop**: L404 (independent)
**Date**: 2026-05-01
**Scope**: paper/base.md §2.4 (4 microscopic pillars) + §2.5 (5th axis OPEN) + §6.1.2 (NOT_INHERITED 8 entries, of which 5 chained to GFT/BEC non-adoption)
**Predecessors**: L320, L370, L385, L388, L389, L390, L400, L401
**정직 한 줄**: 본 design 은 "Causet meso vs GFT 등재 결정"을 reviewer 가 *왜 미루느냐*로 공격하는 vector 만 매핑하며, 이론 형태·수식·파라미터 값을 일절 도입하지 않는다 (CLAUDE.md [최우선-1] 준수).

---

## 0. 8인팀 자율 분담 원칙 (CLAUDE.md L17 이후)

본 attack design 은 8인팀의 토의에서 *자연 발생한* 분업의 결과만 기록한다. 사전 역할 지정 없음. 8인은 자유롭게 두 후보 (Causet meso / GFT) 의 axiom 정합성과 NOT_INHERITED 회복 잠재력을 공격면별로 자율 분담하여 검토한다.

---

## 1. Critical decision-point 의 reviewer 공격 가능성

### 1.1 핵심 공격면

paper/base.md §2.5 는 "Causet meso 4/5 조건부 PASS, 후속 검증 필요" 만 기재. §6.1.2.1 은 "axiom 4 의 5번째 축 (Causet vs GFT) 결정이 critical decision point" 라고 명시하면서도, 결정을 *유보* 한다. Reviewer 가 즉시 떠올릴 자연스러운 공격은 다음과 같다.

| ID | 공격 | 채널 |
|----|------|------|
| **D1** | "5번째 축 결정을 *왜* 유보하나? §2.5 가 4/5 조건부 PASS 라고 부르면 이미 Causet 채택해야 하는 것 아닌가, 아니면 PASS 라는 단어가 무력화된 것 아닌가?" | R1 (theorist) |
| **D2** | "GFT 등재 시 NOT_INHERITED 8건 중 5건이 동시 회복된다고 §6.1.2.1 이 *주장*. 그럼 GFT 채택의 cost (axiom 1–6 와의 충돌, Z₂≠U(1) 군 mismatch) 가 정확히 무엇인가? cost-benefit 비교 정량 미제시." | R1 + R3 |
| **D3** | "두 후보 (Causet/GFT) 가 axiom 1–6 에 대해 동일하게 호환적인가? 동일하다면 'critical decision' 이 아니다 — 둘 다 채택하면 된다. 다르다면 어떤 axiom 과 conflict 하는지 명시 부재." | R1 |
| **D4** | "결정 유보 자체가 §6.5(b) iterative model refinement caveat 의 또 다른 사례 아닌가? '결정을 미루어 두 결과를 모두 살릴 수 있는 상태' 는 p-hacking 면역에 어긋난다." | R3 |
| **D5** | "NOT_INHERITED #15 (특이점), #17 (Jacobson δQ=TdS) 는 GFT 등재만으로는 회복되지 않는다 (#17 은 KMS≠Clausius issue). 5번째 축 결정이 회복하는 항목과 *여전히* 회복 못하는 항목을 분리 보고하라." | R1 + R2 |
| **D6** | "4 축은 이미 σ₀=4πG·t_P holographic 항등식을 산술 결과로 가진다. 5번째 축이 추가될 때 이 항등식이 *유지되는가*, *수정되는가*, *재도출되는가*?" | R1 |
| **D7** | "Causet meso 의 4/5 조건부 PASS 의 *조건* 1개가 무엇인지 paper 본문 미명시. Reviewer 가 따라갈 수 없다." | R2 |
| **D8** | "BEC nonlocality (#19) 는 GFT 등재 시 회복 가능하다고 주장. 그러나 BEC nonlocality 가 실제 *관측* 채널 (e.g. galactic σ profile, cluster lensing residual) 에서 *어떻게* 시그너처를 남기는지 정량 미제시. 회복이 'paper 자체 inheritance' 만의 회복이라면 *외부 관측 가치 없음*." | R2 |

### 1.2 공격면 D1–D8 의 reviewer 별 우선순위

- R1 (theorist): D1, D2, D3, D5, D6 — axiom 1–6 정합성 + holographic 항등식 영향
- R2 (observer): D5, D7, D8 — 회복된 claim 의 관측 가치
- R3 (statistician): D2, D4 — cost-benefit / iterative refinement caveat

---

## 2. 두 후보의 axiom 정합성 정성 (★ 수치 미부여, 방향만)

8인팀 토의에서 자율 분담된 정성 검토 결과만 기록. 정량 비교는 NEXT_STEP.md 에서 별도 분석 toy 로 진행.

### 2.1 Causet meso (coarse-grained causal set)

- axiom 정합성 *방향*: discreteness postulate 와 axiom 4 (Z₂ SSB) 의 macro 발현이 결합 가능한지 — 정성적으로 *충돌하지 않는* 것으로 보이나, "조건부 PASS 의 1 미달 조건" 이 본문에 명시되지 않은 채 §2.5 가 인용됨. ★ 본문 정직 기재 필요.
- NOT_INHERITED 회복 *방향*: #15 (특이점 해소) 직접 회복 가능. #17 (Jacobson) 부분 회복 가능 (causal set entropy 채널). #16/#18/#19 (Volovik/GFT/BEC) 회복 *없음*. #20/#21 (DESI ξ_q, 3자 정합) 회복 *없음*.
- 8인팀 첫인상: "5/8 NOT_INHERITED 회복은 GFT 가 더 강할 것" 으로 의견 다수.

### 2.2 GFT (Group Field Theory)

- axiom 정합성 *방향*: BEC 상의 U(1) 연속 phase 가 axiom 4 의 Z₂ SSB 와 *군 mismatch*. 8인팀이 미해결로 분류. paper 채택 시 (a) axiom 4 를 Z₂ → 더 큰 군으로 *확장*, (b) GFT 의 U(1) 상을 Z₂ 부분군으로 *축소*, (c) 두 분리된 SSB 채널로 *공존*, 세 시나리오 분기.
- NOT_INHERITED 회복 *방향*: #18, #19 직접 회복. #16 (Volovik) 부분 회복 (BEC 동형). #20, #21 회복 잠재 (DESI ξ_q joint fit 의 미시 motivation 제공). #15 (특이점) 부분 회복 (BEC saturation 채널). #17 (Jacobson) 회복 *없음*.
- 8인팀 첫인상: NOT_INHERITED 회복은 더 넓으나, axiom 4 의 *군 구조 수정 cost* 가 §2.4 의 핵심 quantitative claim (η_Z₂ ≈ 10 MeV) 을 흔들 위험.

### 2.3 정성적 cost-benefit 매트릭스 (★ 수치 미부여)

| 채널 | Causet | GFT |
|------|--------|-----|
| axiom 1–3 (KMS, Wetterich, holographic) 정합성 | 충돌 없음 (방향) | 충돌 없음 (방향) |
| axiom 4 (Z₂ SSB) 정합성 | 충돌 없음 | **군 mismatch — 확장/축소/공존 분기** |
| axiom 5–6 정합성 | 충돌 없음 | 충돌 없음 |
| #15 회복 | 직접 | 부분 |
| #16 회복 | 없음 | 부분 |
| #17 회복 | 부분 | 없음 |
| #18 회복 | 없음 | 직접 |
| #19 회복 | 없음 | 직접 |
| #20 회복 | 없음 | 잠재 |
| #21 회복 | 없음 | 잠재 |
| #22 회복 (5 program 동형) | Causet PARTIAL → PASS 1/5 | GFT NOT_INHERITED → PASS 1/5 |
| η_Z₂ ≈ 10 MeV 보존 여부 | 보존 | **재검증 필요** |
| holographic 항등식 σ₀=4πG·t_P 영향 | 무관 (방향) | **재도출 필요 가능성** |

★ 8인팀 합의: 두 후보는 *동일 trade-off* 위에 있지 않다 — Causet 은 **보수적 (axiom 보존, 회복 1–2건)**, GFT 은 **공격적 (axiom 4 수정, 회복 5건+)**.

---

## 3. Reviewer 공격에 대한 방어 방향 (★ 결론 미부여)

8인팀이 자율 분담으로 도출한 방어 채널만 기록. 결론 (Causet 채택 / GFT 채택 / 양립 정책) 은 REVIEW.md 에서 4인팀이 권고.

### 3.1 D1 (왜 유보하나?)
- 방향: §2.5 의 "조건부 PASS" 가 *full PASS* 와 다르다는 점, 그리고 "결정 유보 = framework completeness 80% 상한" 이 §6.1.1 #10 에 이미 정직 기재되어 있음을 reviewer 에게 redirect.

### 3.2 D2 (cost-benefit 정량)
- 방향: NEXT_STEP.md 에서 두 후보 각각 채택 시 paper framework 의 22 row 한계 표 변화 정량 (몇 row 가 NOT_INHERITED → PASS/PARTIAL 로 이동하는지). 본 ATTACK_DESIGN 에서는 *공격면이 정당하다* 고 인정.

### 3.3 D3 (axiom 1–6 호환성 차등)
- 방향: 표 2.3 그대로 본문에 §2.5 확장으로 추가. 두 후보의 axiom 4 영향 차이를 명시하면 D3 close.

### 3.4 D4 (iterative refinement caveat)
- 방향: §6.5(b) caveat 에 "5번째 축 결정 유보 자체가 iterative refinement 의 한 사례" 한 문장 추가. p-hacking 면역에 부합하도록 *결정 시 사전 등록* (DR3 timeline 과 무관한 별도 micro-decision register) 도입.

### 3.5 D5 (#17 등 잔존 NOT_INHERITED)
- 방향: 어느 후보도 #17 (Jacobson δQ=TdS) 단독 회복 못 함을 명시. 별도 entropic derivation 채널 (paper 외부 future work) 분리.

### 3.6 D6 (holographic 항등식 영향)
- 방향: GFT 채택 시 σ₀=4πG·t_P 항등식이 *재도출 필요* 인지 *형식 보존* 인지 8인팀 정직 기재. Causet 채택 시 영향 없음을 명시.

### 3.7 D7 (Causet 4/5 조건부 PASS 의 1 미달 조건)
- 방향: 본문 §2.5 에 Causet meso 의 5 조건 명시 + 미달 1 조건의 *방향* (예: dimensionality emergence 의 정량 검증 미완) 만 기재. 수식 도입 없음.

### 3.8 D8 (BEC nonlocality 관측 채널)
- 방향: GFT 채택 시 #19 회복은 *paper-internal* 회복일 뿐이며, 관측 채널 (galactic profile residual / cluster lensing) 에서의 시그너처는 별도 falsifier 로 등재 필요. paper 본문 §4.7 falsifier 표 확장 후보.

---

## 4. CLAUDE.md 준수 자가 점검

- [최우선-1] 방향만, 지도 금지: 본 design 에 수식·파라미터 값·유도 경로 0건. 두 후보 군구조 명칭 (Z₂, U(1)) 은 axiom 4 본문에 이미 등재된 *명칭* 이므로 지도가 아님.
- [최우선-2] 이론은 팀 독립 도출: 본 design 은 reviewer 공격 매핑이며 이론 도출 아님.
- 역할 사전 지정 금지: 8인팀 자율 분담만 기록, 사전 역할 부여 0건.
- 결과 왜곡 금지: 두 후보 모두 단점 (Causet=회복 폭 좁음, GFT=axiom 4 군 mismatch) 정직 기재.
- "fixed-θ" vs "marginalized" 구분: 본 단계 정량 통계 미사용 — 위반 없음.
- DR3 스크립트 미실행 원칙: 본 세션 코드 실행 없음 (NEXT_STEP.md 에서만 분석 toy 1건).
