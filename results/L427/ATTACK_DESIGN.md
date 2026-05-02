# L427 — ATTACK_DESIGN: Dual foundation 명시 등재 시 reviewer 공격 매핑

**Loop**: L427 (independent)
**Date**: 2026-05-01
**Predecessors**: L320, L370, L385, L388, L389, L390, L400, L401, L404 (Dual coexistence 권고)
**Scope**: paper/base.md §2.5 + §6.1.2 가 5번째 axis 후보를 *Causet meso + GFT dual foundation* 으로 명시 등재할 때 reviewer 가 새로 펼 공격면 매핑.
**정직 한 줄**: 본 design 은 L404 권고의 *paper 본문 등재 단계* 에서 reviewer 공격이 어떻게 *이동·증가* 하는지를 추적하며, 이론 형태·수식·파라미터를 일절 도입하지 않는다 (CLAUDE.md [최우선-1] 준수).

---

## 0. 8인팀 자율 분담 원칙 (CLAUDE.md L17)

8인팀은 (i) Dual 명시 등재가 L404 D1–D8 공격면을 어떻게 *변형* 하는지, (ii) Dual 등재로 신규 발생하는 reviewer 공격면 (D9–D12), (iii) NOT_INHERITED 8 항목 중 회복 가능 set 의 정량 경계 — 세 작업을 토의 중 자율 분담. 사전 역할 지정 0건.

---

## 1. L404 D1–D8 의 *post-등재* 변형

L404 ATTACK_DESIGN 은 "결정 유보" 상태의 reviewer 공격을 매핑했고, L404 REVIEW 는 양립 정책을 권고했다. L427 은 *권고가 본문에 반영된 후* 의 attack surface 를 갱신한다.

| ID | L404 공격 (유보 상태) | L427 변형 (Dual 명시 후) | 강도 변화 |
|----|---------------------|-------------------------|----------|
| D1 | "왜 결정을 유보하나?" | "왜 *두 후보 모두* 등재하나? 이는 단순 OR 가 아닌 *프레임워크 확장* 이다" | ↑ 노출도 증가 (본문 noun 으로 등장하므로) |
| D2 | "cost-benefit 정량 부재" | "두 foundation 의 *상호작용* cost (cross-channel consistency) 정량 부재" | ↑ 새 차원 추가 |
| D3 | "axiom 1–6 호환성 차등" | "두 foundation 이 동시 등재될 때 axiom 4 가 *Z₂ 단독* 이 아닌 *Z₂ × U(1)-부분군* 형태로 *해석 변경* 되는 것 아닌가" | ↑↑ 강도 크게 증가 |
| D4 | "결정 유보 = iterative refinement" | "Dual 등재 = *결정 회피의 정당화*. p-hacking 면역 위반 의혹" | = 동일 강도, 채널만 변경 |
| D5 | "#17 (Jacobson) 잔존" | 동일. 어느 시나리오에서도 단독 회복 불가 — Dual 에서도 잔존 | = 동일 |
| D6 | "σ₀=4πG·t_P 항등식 영향" | "GFT branch 가 항등식을 재도출 *해야* 하면, Dual 등재는 항등식이 *두 채널에서 독립 재도출* 되어야 함을 함의" | ↑ 검증 부담 가중 |
| D7 | "Causet 4/5 조건부 1 미달" | 동일 — Causet 부분의 미달 1 조건은 Dual 명시 후에도 잔존 | = 동일 |
| D8 | "BEC nonlocality 관측 채널" | "Dual 등재 시 BEC nonlocality 가 *부분 활성화* (GFT branch). 관측 시그너처가 *분리 가능한* 가" | ↑ 분해능 요구 |

요약: D3 / D6 는 Dual 등재로 *강도 상승*. D1 / D2 는 노출도 증가 (본문 등재 자체가 reviewer 의 첫 진입점). D4 / D5 / D7 / D8 은 동일 또는 채널 변경.

---

## 2. Dual 등재로 신규 발생하는 공격면 (D9–D12)

### 2.1 D9 — "Dual 은 framework 추가 자유도 1 도입"
- 채널: R3 (statistician)
- 공격: Causet 단독 또는 GFT 단독 대비, Dual 은 *어느 branch 가 활성화되는지의 binary choice* 라는 *숨은 자유도 1* 을 도입한다. AICc 패널티 정량 부재 시 model selection 에서 Dual 이 *부당하게 우세* 하게 보일 수 있다.
- 방어 방향: §2.5 본문 등재 시 "Dual 은 cosmological observable 에 영향 미치지 않는 *foundational* layer 이며, derived prediction 자유도는 0 추가" 를 정직 기재. (이론 도출 0건, 명시 정책만)

### 2.2 D10 — "Dual 등재가 §2.4 4 미시 축의 *상호 일관성* 가정 (§2.6 caveat) 을 더 약화"
- 채널: R1 (theorist)
- 공격: §2.6 은 이미 "4 축 상호 일관성 (동일 Lagrangian 도출 가능성) 부분 검증" 을 자가 caveat 으로 인정. 5번째 축이 *2 후보 동시* 라면, "동일 Lagrangian" 가정 자체의 *의미* 가 후퇴한다.
- 방어 방향: §2.6 caveat 를 1 문장 확장 — "5번째 축의 dual 본질은 4 축의 Lagrangian 일관성 가정과 *직교* (foundational layer 분리) 또는 *완화* (joint consistency 약화) 두 해석 모두 OPEN" 명시.

### 2.3 D11 — "양립 정책의 micro-decision register 가 R3 D4 의 *재포장* 에 불과"
- 채널: R3
- 공격: L404 §3 의 micro-decision register Trigger A–D 는 "결정을 미루는 새 메커니즘" 일 뿐, p-hacking 면역에 실질적 추가 보장 없음.
- 방어 방향: register 의 trigger 조건이 *데이터-독립* (axiom 4 군 구조의 외부 QFT/holography 채널, σ₀ 항등식의 별도 dimensional reduction 채널 등) 임을 §6.5(b) 1 문장 추가로 명시.

### 2.4 D12 — "Dual 등재가 paper completeness 80% 상한을 *영구화* 한다"
- 채널: R2 (observer)
- 공격: L404 NEXT_STEP §3.5 / REVIEW Trigger D 는 "어느 trigger 도 발생 안 하면 양립 정책 영구 유지 → 80% 상한 영구 격상" 을 정직 기재. 이는 "완전한 axiom-기반 framework" 라는 §0 abstract 의 implicit 약속을 약화한다.
- 방어 방향: §0 abstract 와 §6.1.1 row #10 모두 "completeness 80% (Dual 등재 후)" 를 *명시적 상수* 로 동기화. JCAP "정직한 falsifiable phenomenology" 포지셔닝과 정합 (PRD Letter 진입 조건 미달성 재확인).

---

## 3. NOT_INHERITED 8 항목 중 회복 가능 set 정량 경계 (D5 의 정직 응답)

L404 NEXT_STEP §1 의 회복 가중치 표를 다시 *정성 mapping* 만으로 (수치 없음, 라벨로만) 정리. 이 매핑은 형식적이며 절대값에 우주론적 의미 없음을 본문 본문에 명시.

| # | row | Causet branch | GFT branch | Dual union | 회복 도달 가능성 (정성) |
|---|-----|---------------|------------|------------|----------------------|
| 15 | 특이점 해소 | direct | partial | direct | high |
| 16 | Volovik 2-fluid | none | partial | partial | medium |
| 17 | Jacobson δQ=TdS | partial | none | partial | medium (둘 다 단독으론 불가) |
| 18 | GFT BEC 해밀토니안 | none | direct | direct | high |
| 19 | BEC nonlocality | none | direct | direct | high (단, 관측 채널 분리 D8 잔존) |
| 20 | DESI ξ_q joint fit | none | latent | latent | low (외부 재현 trigger B 필요) |
| 21 | 3자 정합성 (BBN/CMB/late DE) | none | latent | latent | low (#20 의존) |
| 22 | 5 program 동형 | partial (1/5) | partial (1/5) | partial (2/5) | medium |

요약 (정성):
- **direct 회복**: #15, #18, #19 — Dual 등재의 *직접 이득* (3 항목)
- **partial 회복**: #16, #17, #22 — Dual 에서 부분만 회복, 잔여 future work (3 항목)
- **latent 회복**: #20, #21 — 외부 trigger 의존, paper 본문 회복 *주장 불가* (2 항목)

**정직 경계**: Dual 등재의 NOT_INHERITED 회복 *주장 가능 범위* 는 최대 **direct 3 + partial 3 = 6/8 항목 부분 이상 진행**. #20/#21 는 *paper 본문에서 회복 주장 금지* (latent 만). #17 은 어느 branch 도 단독 회복 불가 — §6.5(e) self-audit footnote 에 별도 분리 필수.

---

## 4. Reviewer 우선순위 (D1–D12)

- R1 (theorist): D1, D3, D6, D10 — axiom-foundational consistency
- R2 (observer): D5, D7, D8, D12 — 회복 주장의 관측 가치 + completeness 약속
- R3 (statistician): D2, D4, D9, D11 — cost-benefit + iterative refinement + 자유도

D3 (axiom 4 해석 변경) 와 D9 (자유도 1) 가 *최고 강도 신규 공격* — paper §2.5 본문 등재 시 직접 응답 텍스트 필수.

---

## 5. CLAUDE.md 준수 자가 점검

- [최우선-1] 방향만, 지도 금지: 본 design 에 수식·파라미터 값·유도 경로 0건. 군 구조 명칭 (Z₂, U(1)) 은 axiom 4 본문 등재 명칭이므로 지도가 아님.
- [최우선-2] 이론 도출 없음: Dual foundation 채택은 *결정 유보의 명시화* 이며 이론 형태 도입 아님. 두 foundation 모두 paper 외부에서 prior 로 인용된 미시 후보들이며, paper 는 *어느 foundation 이 axiom 4 의 미시 origin 인가* 를 *결정하지 않는다*.
- 역할 사전 지정 금지: 8인팀 자율 분담만 기록.
- 결과 왜곡 금지: §2 D9–D12 신규 공격면 정직 명시. §3 회복 set 의 latent 2 항목 (paper 본문 회복 주장 금지) 정직 경계 기재.
- "fixed-θ" vs "marginalized" 구분: 본 단계 정량 통계 미사용 — 위반 없음.
- DR3 스크립트 미실행: 본 세션 코드 실행 0건.
- L6 8인 합의: Dual 등재가 PRD Letter 진입 조건 (Q17 + Q13/Q14) 과 무관 — JCAP 포지셔닝 정합.

---

## 6. NEXT_STEP / REVIEW 에 전달할 입력

1. D9 (자유도 1) / D10 (4 축 일관성 약화) / D11 (register 재포장) / D12 (80% 상한 영구화) 신규 공격면 — 본문 응답 텍스트 후보를 NEXT_STEP §1 에서 정량 매핑.
2. NOT_INHERITED 회복 set 정량 경계 (direct 3 / partial 3 / latent 2) — REVIEW §1 의 paper §6.1.2 본문 *회복 주장 한계* 에 직접 반영.
3. paper §2.5 / §6.1.2 본문 수정의 *최소 텍스트 변경* 경계 — REVIEW §2 에서 4인팀이 직접 §2.5 / §6.1.2 sync 수정 시 위반 없는 변경 폭 확정.
