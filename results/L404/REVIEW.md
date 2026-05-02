# L404 — REVIEW: 4인팀 권고 (5번째 축 결정 / 양립 정책)

**Loop**: L404 (independent)
**Date**: 2026-05-01
**Predecessors in this session**: ATTACK_DESIGN.md, NEXT_STEP.md
**정직 한 줄**: 4인팀은 NEXT_STEP toy 의 절대값을 *결정 근거로 신뢰하지 않으며*, 대신 ordering robustness + framework 안정성 + reviewer 노출도의 *세 정성 축* 만을 권고 근거로 채택한다.

---

## 0. 4인팀 자율 분담 (CLAUDE.md L17)

4인팀은 (i) ATTACK_DESIGN 의 8 공격면 D1–D8 검토, (ii) NEXT_STEP toy 의 가정 (a)–(f) 검토, (iii) paper §2.5 / §6.1.2 본문 영향 검토, (iv) 권고문 작성 — 의 4 작업을 토의 중 자율 분담. 사전 역할 지정 0건.

---

## 1. 권고

### 1.1 메인 권고

**명시적 양립 정책 (Dual coexistence with priority)** 을 paper §2.5 본문 정책으로 채택.

구체:

- §2.5 를 "5번째 축 후보 OPEN — Causet meso 4/5 조건부 PASS" 에서 → "**5번째 축 후보 OPEN, 두 후보 (Causet meso, GFT) 모두 본 framework 와 *조건부* 호환** — 우선순위는 axiom 4 보존도 (Causet) > NOT_INHERITED 회복도 (GFT) 의 *순서 결정 미정*. 본 paper 는 결정을 명시적으로 유보하며, DR3 unblinding 과 *분리된* 별도 micro-decision register 로 사후 등록한다." 로 확장.
- 두 후보 채택 시 paper 변화 (NEXT_STEP §3.3, §3.4) 를 §2.5 보조 표로 본문 첨부.
- §6.5(b) iterative refinement caveat 에 "5번째 축 결정 유보 자체가 iterative refinement 의 한 사례 — 결정은 데이터 *불의존* micro-decision register 에 사전 등록한다" 1 문장 추가.
- §6.1.2 NOT_INHERITED 표에 "5번째 축 결정 후 회복 row" 컬럼 추가 (Causet 채택 시 / GFT 채택 시 / 양립 정책 시 의 3 시나리오 row 별 표시).

### 1.2 권고 근거 (3 정성 축)

| 축 | 1순위 | 2순위 | 3순위 |
|----|------|------|------|
| Robust ordering (NEXT_STEP §3.1) | Dual | GFT | Causet |
| Framework 안정성 (NEXT_STEP §3.4) | Causet | GFT | Dual |
| Reviewer 노출도 합 (ATTACK_DESIGN D1–D8) | Dual (D1/D3/D4 노출) | Causet (D2/D8 노출) | GFT (D6 노출, severity 높음) |

세 축의 1순위 가 일치하지 않음 → **단일 후보 결정은 어느 축 하나를 희생** 하므로 4인팀은 *명시적 양립 정책* 을 차선으로 권고. 양립 정책의 reviewer 노출도 (D1/D3/D4) 는 §2.5 본문 확장 + §6.5(b) 1 문장 추가로 *직접 응답* 가능 — 8인팀 토의에서 응답 가능성 합의.

### 1.3 단일 후보 권고를 *하지 않는* 정직한 이유

- **GFT 단독 채택 시**: NEXT_STEP §3.3 의 "σ₀=4πG·t_P 항등식 재도출 risk" 가 비제로. paper §4.1 의 PASS_STRONG 6 row 가 PARTIAL 로 격하될 risk 는 NOT_INHERITED 5 row 회복의 이득을 *paper-internal* 에서는 능가하지 못한다 (PASS_STRONG row 는 외부 관측 채널 보유, NOT_INHERITED row 는 *paper-internal* inheritance 이슈).
- **Causet 단독 채택 시**: NEXT_STEP §3.4 의 회복 폭 (2 row) 이 좁아 NOT_INHERITED 8 row 중 6 row 잔존. R1 D2 ("cost-benefit 정량") 와 R3 D4 ("결정 유보") 에 직접 노출. Reviewer 가 "왜 4/5 조건부 PASS 로 충분한가" 를 재차 공격할 채널을 닫지 못함.

---

## 2. 양립 정책 채택 시 paper 텍스트 영향 체크리스트

8인팀 + 4인팀 합의로 본문에 들어갈 변경 (★ 이론 도출 0건, 정책 텍스트만):

- [ ] §2.5 1 → 2 단락 확장 (Causet/GFT 두 후보 본문 명시 + cost-benefit 정성 표)
- [ ] §2.5 보조 표: NEXT_STEP §3 의 "Causet 채택 시 / GFT 채택 시 / 양립 정책 시" 3 시나리오 row 영향 표
- [ ] §6.1.1 #10, #11 의 "Future plan" 컬럼에 "5번째 축 결정 시 PARTIAL 또는 close" 표기
- [ ] §6.1.2 표에 "5번째 축 결정 후 회복" 컬럼 추가
- [ ] §6.1.2.1 의 "GFT 등재 시 root /base.md §V/§VI 의 5+ claim 동시 회복 가능" 문장을 "*GFT 등재 시* 5 claim 회복 가능 — 단, axiom 4 군 구조 재검증 cost 동반. *Causet meso 등재 시* 1–2 claim 회복 — axiom 보존. 본 paper 는 양립 정책으로 결정 유보" 로 수정
- [ ] §6.5(b) iterative refinement caveat 에 1 문장 추가 (5번째 축 결정 유보 = iterative refinement 사례, micro-decision register 사전 등록)
- [ ] §4.7 falsifier 표 (가능 시) 에 "BEC nonlocality observational signature" 1 row 신규 등재 — GFT 채택 시 활성화, Causet 채택 시 NA. *현 시점 falsifier 등재 효과 0* (양립 정책 하에서) 명시.
- [ ] §6.1.2 #17 (Jacobson δQ=TdS) 는 어느 후보로도 단독 회복 안 됨을 §6.5(e) self-audit 의 별도 footnote 로 분리 (현재 표에 묶여 있어 "GFT 등재만 하면 다 풀린다" 인상 야기 — 정직성 결여).

---

## 3. 양립 정책의 한계와 다음 loop 조건부 trigger

양립 정책은 *유보* 의 명시화이지 결정의 *대체* 가 아니다. 4인팀이 DR3 와 *무관한* 별도 micro-decision register 의 trigger 조건 권고:

- **Trigger A**: paper 외부에서 axiom 4 의 군 구조 (Z₂ vs U(1)) 가 *독립적인* QFT/holography 채널에서 결정되면 — 두 후보 중 하나로 자동 결정.
- **Trigger B**: NOT_INHERITED #20 (DESI ξ_q joint fit) 의 *외부 (다른 그룹) 재현* 이 r_d shift 와 함께 보고되면 — GFT 우선으로 결정 (joint fit 미시 motivation 제공자가 GFT 라면).
- **Trigger C**: σ₀=4πG·t_P holographic 항등식 보존 여부에 *경계 검증* (예: 별도 dimensional reduction 채널) 이 닫히면 — Causet 우선으로 결정 (항등식 재도출 risk 확정 시 GFT 후퇴).
- **Trigger D**: 어느 trigger 도 발생 안 함 → 양립 정책 영구 유지. 이 경우 paper completeness 80% 상한 (§6.1.1 #10) 은 *영구* 한계로 격상.

---

## 4. ATTACK_DESIGN 8 공격면 별 양립 정책 응답

| 공격 | 양립 정책 응답 |
|------|---------------|
| D1 (왜 유보) | §2.5 확장 + §6.5(b) 추가 문장으로 *명시적 유보* 정당화 |
| D2 (cost-benefit) | NEXT_STEP §3 의 3 시나리오 row 영향 표를 §2.5 본문에 첨부 |
| D3 (axiom 1–6 호환성 차등) | §2.5 cost-benefit 표가 직접 응답 |
| D4 (iterative refinement) | §6.5(b) 1 문장 추가 + micro-decision register 명시 |
| D5 (#17 잔존) | §6.5(e) footnote 분리로 정직 명시 |
| D6 (holographic 항등식) | §2.5 보조 표의 "GFT 시 재도출 risk 비제로 / Causet 시 0" row |
| D7 (Causet 4/5 조건부 1 미달) | §2.5 본문 확장 시 Causet 의 미달 1 조건 *방향* 명시 (수식 없이) |
| D8 (BEC nonlocality 관측) | §4.7 falsifier 표에 신규 row 등재 (양립 정책 하 비활성, GFT 채택 시 활성화) |

---

## 5. CLAUDE.md 준수 자가 점검

- [최우선-1] 방향만, 지도 금지: 본 REVIEW 는 정책 권고이며 수식·파라미터·유도 경로 0건.
- [최우선-2] 이론 도출 없음: 양립 정책은 *결정 유보* 의 명시이며 이론 형태 도입 아님.
- 역할 사전 지정 금지: 4인팀 자율 분담만 기록.
- 결과 왜곡 금지: §1.3 에서 단일 후보 권고를 *하지 않는* 이유, §3 에서 양립 정책의 한계 (영구 80% 상한 격상) 정직 기재.
- "fixed-θ" vs "marginalized" 구분: 본 권고는 통계 evidence 비교 미사용 — 위반 없음.
- DR3 스크립트 미실행: 본 세션 코드 실행은 NEXT_STEP toy (10 ms 산술) 1건만, DR3 미공개 데이터 접근 0건.
- L6 8인 합의 (JCAP 타깃, falsifiable phenomenology 포지셔닝): 양립 정책은 *honest framework* 강화이며 PRD Letter 진입 조건 (Q17 + Q13/Q14) 과 무관 — 위반 없음.
- ★ 본 권고가 paper 본문 §2.5 / §6.1 / §6.5 텍스트 변경을 동반하므로, paper 반영 *전* 에 8인팀 Rule-A 순차 리뷰 1회 추가 권고 (CLAUDE.md L6 재발방지 규칙).

---

## 6. 산출물

- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L404/ATTACK_DESIGN.md`
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L404/NEXT_STEP.md`
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L404/REVIEW.md` (본 파일)
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/simulations/l404/recovery_compare.out` (toy 산출)
