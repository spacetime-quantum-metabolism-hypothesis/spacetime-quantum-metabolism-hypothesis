# L404 — NEXT_STEP: Causet vs GFT 채택 시 framework 변화 정량

**Loop**: L404 (independent)
**Date**: 2026-05-01
**Scope**: ATTACK_DESIGN.md 의 D2 / D3 / D6 / D8 공격면에 대한 정량 응답
**정직 한 줄**: 본 단계는 회복 가중치를 ATTACK_DESIGN §2 의 *정성적 방향* (direct/partial/latent/none) 만으로 numeric mapping 한 *후순위 toy* 이며, 가중치 자체는 8인팀의 정성 합의를 1.0/0.5/0.25/0.0 로 *형식적으로 부호화* 한 것이다 — 절대값에 우주론적 의미는 없고 *상대적 ordering* 만 의미를 가진다.

---

## 0. 8인팀 자율 분담

본 단계의 toy 작성과 sensitivity scan 은 8인팀 토의 결과를 정량 표로 옮기는 작업으로, 토의에서 자율 발생한 분업으로 진행. 사전 역할 지정 0건.

---

## 1. 분석 toy 입력

ATTACK_DESIGN.md §2.3 cost-benefit 매트릭스의 *정성 방향* 을 다음 numeric mapping 으로 부호화:

- direct 회복 → 1.00
- partial 회복 → 0.50
- latent 회복 → 0.25
- none → 0.00

NOT_INHERITED 8 row (#15–#22) 별 가중치:

| row | Causet | GFT |
|-----|--------|-----|
| 15 (특이점) | 1.00 | 0.50 |
| 16 (Volovik) | 0.00 | 0.50 |
| 17 (Jacobson) | 0.50 | 0.00 |
| 18 (GFT BEC H) | 0.00 | 1.00 |
| 19 (BEC nonlocality) | 0.00 | 1.00 |
| 20 (DESI ξ_q joint) | 0.00 | 0.25 |
| 21 (3자 정합성) | 0.00 | 0.25 |
| 22 (5 program 동형) | 0.20 | 0.20 |
| **합** | **1.70 / 8.00** | **3.70 / 8.00** |

Framework limitations 중 5번째 축 결정에 직접 묶인 row #10 (micro completeness 80%) 와 #11 (axiom 4 metric 미시 OPEN) 는 두 후보 모두 동일 가중치 (#10=0.50, #11=1.00) 로 부분/완전 close.

GFT 채택의 *axiom-4 군 mismatch cost* 는 ATTACK_DESIGN §2.2 의 8인팀 첫인상에 따라 cost ∈ [0.0, 0.6] 의 sensitivity 변수로 둔다.

---

## 2. 결과 (절대값 의미 없음, 상대 ordering 만)

`simulations/l404/recovery_compare.out` 산출물:

```
Causet: NOT_INHERITED 회복=1.70/8.00, framework=1.50/1.50, axiom-4 cost=0.00, NET=3.20
GFT   : NOT_INHERITED 회복=3.70/8.00, framework=1.50/1.50, axiom-4 cost=0.60, NET=4.60
Dual  : NOT_INHERITED 회복=4.70/8.00, framework=1.50/1.50, overhead=0.40, GFT cost=0.60, NET=5.20

Sensitivity (GFT axiom cost):
  cost=0.6 → GFT=4.60, Dual=5.20, Causet=3.20
  cost=0.4 → GFT=4.80, Dual=5.40, Causet=3.20
  cost=0.2 → GFT=5.00, Dual=5.60, Causet=3.20
  cost=0.0 → GFT=5.20, Dual=5.80, Causet=3.20
```

**Gap |GFT_NET − Causet_NET| = 1.40 > 0.5**

(미리 정한 8인팀 임계 0.5 보다 큼 — single-winner 선호 영역)

---

## 3. 해석 (정직)

### 3.1 ordering

**Dual > GFT > Causet** 가 axiom-4 cost 의 모든 시나리오 (0.0–0.6) 에서 robust.

### 3.2 ordering 의 한계

본 ordering 은 다음 가정에 의존하며, 가정이 깨지면 ordering 도 깨진다:

- (a) 회복 가중치 1.0/0.5/0.25/0.0 는 *형식적* 부호화. 8인팀이 다른 mapping 을 선택하면 NET 절대값과 gap 모두 변함.
- (b) row 별 회복은 *독립 합산* 으로 가정. 실제로는 #18, #19, #20, #21 이 GFT 채택의 *연쇄 회복* 이라 correlation 존재 — 합산이 회복 효과를 *과대* 추정할 가능성.
- (c) axiom-4 군 mismatch cost 0.0–0.6 범위는 8인팀 첫인상이며 정량 도출 아님. cost > 1.0 시 GFT 채택은 framework 자체를 손상시킬 수 있음.
- (d) Dual policy 의 overhead 0.4 는 "본문 §2.5 확장 텍스트 + axiom 4 의 두 SSB 채널 공존 표기" 의 *정성 비용*. 실제 inter-channel consistency 가 깨지면 cost 는 비선형 폭증.
- (e) #15 (특이점) 회복은 두 후보 모두 *부분*. *완전* 회복은 별도 entropic derivation (axiom 외부) 필요 — 어느 단일 후보로도 #15 close 불가.
- (f) #17 (Jacobson δQ=TdS) 는 어느 후보도 단독 회복 못함. 이는 KMS≠Clausius 라는 axiom 1 의 *내재 한계* 로, 5번째 축 결정과 *직교*. paper §6.5(e) 에 별도 분리 명시.

### 3.3 GFT 채택 시 paper 변화 정량

axiom-4 cost = 0.4 (중간 시나리오) 가정 시:

- §6.1.2 NOT_INHERITED 8 row 중 **5 row (#15, #16, #18, #19, #22) 가 PASS/PARTIAL 로 이동**, 3 row (#17, #20, #21 잔존; #20/#21 은 latent → PENDING 격하 가능).
- §6.1.1 row #10 (PARTIAL) + #11 (close).
- §2.4 4 축 표가 5 축으로 확장 — η_Z₂ ≈ 10 MeV 의 군 구조 *재검증* 필요 (paper §2.4 의 PASS_STRONG 1 row 가 PARTIAL 로 격하될 위험).
- §4.1 holographic 항등식 σ₀=4πG·t_P 의 PASS_STRONG 6 row 는 *재도출 필요* 시 PARTIAL 로 격하 가능 — **이것이 GFT 채택의 실질 cost**.

### 3.4 Causet 채택 시 paper 변화 정량

- §6.1.2 NOT_INHERITED 8 row 중 **2 row (#15, #17 부분) 가 PASS/PARTIAL 로 이동**, 6 row 잔존.
- §6.1.1 row #10 (PARTIAL) + #11 (close).
- §2.4 / §4.1 PASS 표 변화 *없음* — axiom 4 의 Z₂ SSB 보존.
- 회복 폭은 좁으나 **paper framework 의 PASS_STRONG row 안정성 보존**.

### 3.5 Dual coexistence 시 paper 변화 정량

- NOT_INHERITED 회복은 union (4.70/8.00) 으로 가장 큼.
- 그러나 §2.5 가 "5번째 축 후보 OPEN" → "5+6번째 축 dual" 로 확장되어 framework completeness 가 *오히려 감소* 할 위험 — paper 가 미시 결정을 *postpone* 한다는 reviewer R3 D4 공격에 정면 노출.
- overhead 0.4 는 toy 추정. 실제 inter-channel consistency 검증 미완 시 cost 는 본문 *부담* 으로 누적.

---

## 4. 의사결정 입력 (REVIEW.md 4인팀에 전달)

본 NEXT_STEP 은 결정을 *내리지 않는다*. 4인팀은 다음 입력으로 권고를 작성:

1. **Robust ordering**: Dual > GFT > Causet (cost 0.0–0.6 모든 시나리오).
2. **Framework 안정성**: Causet > GFT > Dual (PASS_STRONG row 보존 관점).
3. **Reviewer 노출도** (ATTACK_DESIGN D1–D8): Causet 단독 = D2/D8 약, D5/D7 강; GFT 단독 = D6 강, D2/D5 약; Dual = D1/D3/D4 강, D2/D5/D8 약.
4. **#17 (Jacobson) 잔존**: 어느 시나리오도 단독 회복 못함 — paper §6.5(e) 외부 future work 분리 필수 (모든 시나리오 공통).
5. **σ₀=4πG·t_P 항등식 재도출 risk**: GFT/Dual 채택 시 *비제로*. Causet 채택 시 0.

---

## 5. CLAUDE.md 준수 자가 점검

- [최우선-1] 방향만, 지도 금지: 본 toy 는 회복 *방향* 의 형식적 부호화만 수행. 수식·파라미터·유도 경로 도입 0건. 가중치 1.0/0.5/0.25/0.0 는 정성 라벨의 *형식 mapping* 이지 이론 파라미터가 아님.
- [최우선-2] 이론 도출 없음: 5번째 축 후보의 라그랑지안·해밀토니안·작용 등 일절 도입 안 함.
- 역할 사전 지정 금지: 8인팀 자율 분담만 기록.
- 결과 왜곡 금지: §3.2 에서 ordering 의 6 가지 한계 (a)–(f) 정직 기재.
- 과적합 패널티: 본 toy 는 자유 파라미터 (axiom-4 cost ∈ [0, 0.6]) 의 sensitivity 를 명시 보고. AICc 등은 정량 통계 분석이 아니므로 미적용.
- 시뮬레이션 병렬 원칙: 본 toy 는 단일 산술 산출 (10 ms) 이라 병렬화 무의미.
- DR3 스크립트 미실행: 위반 없음.
- print() 유니코드: 산출 텍스트는 ASCII + 기본 라틴 보충만 — cp949 충돌 없음.
