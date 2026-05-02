# L409 — ATTACK DESIGN (8인팀 reviewer 공격 설계)

날짜: 2026-05-01
범위: PASS_STRONG 10/32 (31%) advertised → 6 건이 σ₀ = 4πG·t_P holographic 항등식의 *산술 따름결과* 라는 audit 결과를 reviewer 가 공격할 경로 설계.

---

## 0. 광고 vs. 실체

- 현재 광고 (README §0, base.md §0): "Self-audit 31% PASS_STRONG (10/32)".
- audit 실체 (base.md §6.5(e)): 10건 중 **6건은 σ₀=4πG·t_P 산술 따름결과** — "예측 아님" 이미 명시.
- 광고는 31% 숫자만 부각, "6건 산술" 단서는 본문 §6.5(e) 한 줄에만 존재. README/§0 TL;DR 에는 흐려져 있음.
- **노출 격차** 가 reviewer 공격 진입점.

## 1. 8인팀 공격 시나리오 (reviewer persona 별)

### A1 — 통계 referee (frequentist)
> "PASS_STRONG 10건 중 6건이 단일 항등식 σ₀=4πG·t_P 의 산술 따름이라면, 이는 **자유도 1**의 결과를 6번 카운트한 것. effective n_PASS_STRONG = 4 + 1 = 5, 즉 **15.6%** 가 정직한 숫자. 31% 광고는 N-fold double-counting."

공격 강도: ★★★★★ (정량적, 수정 강제력 큼)
방어 가능성: 낮음 — audit 자체가 "산술 따름결과" 인정. SVD participation ratio 같은 collinearity 지표를 보고하지 않으면 31% 는 inflated.

### A2 — Bayesian referee
> "Δ ln Z 계산에서 6건의 산술 항등식은 데이터로부터 정보 (likelihood 기여) 를 받지 않음 — prior 에서 결정됨. PASS 카운트에 포함시키면 evidence inflation."

공격 강도: ★★★★
방어: "PASS = consistency check" 로 재정의 가능하나, 그러면 *prediction* 카운트와 분리 표기 필수.

### A3 — 이론 referee (high-energy)
> "n₀μ = ρ_Planck/(4π), v=g·t_P, ξ scaling, BH entropy, Bekenstein bound, Λ-theorem — 이 6 건은 모두 σ₀ = 4πG·t_P 의 차원 분석에서 자동으로 따라옴. SQMH 공리 1–6 의 *unique* 귀결이 아니라, holographic 단위계의 standard recombination."

공격 강도: ★★★★★ (이론적으로 가장 치명적)
방어: 일부 항목은 비자명 implication 포함 — 본 분류가 핵심 (NEXT_STEP 참조).

### A4 — Adversarial generalist
> "31% 헤드라인은 marketing. 본문 §6.5(e) 한 줄에만 6/10 항등식 단서. 이는 **buried disclosure** — 신뢰 위반."

공격 강도: ★★★ (서지/투명성 측면)
방어: README/abstract 동기화 필수.

### A5 — Falsifiability referee (Popper line)
> "6건이 항등식이라면 SQMH 가 *틀릴* 길이 없음 — 그 6건은 어떤 데이터로도 falsify 불가. 자유도 0 결과를 PASS 로 카운트하는 것 자체가 falsifiability 위반."

공격 강도: ★★★★
방어: PASS_STRONG → "PASS_IDENTITY" 별도 enum 분리 필요.

### A6 — Skeptical co-author (내부)
> "진짜 substantive PASS_STRONG 4건 (Newton 회복, BBN ΔN_eff, Cassini β_eff, EP η=0) 은 강하다. 그 4건만 부각해도 충분. 6 항등식을 *추가* 카운트하는 인센티브가 보고서 톤을 약화."

공격 강도: ★★★ (전략적, 자기반성)
방어: 같은 결론.

### A7 — Editor-level
> "광고 vs 본문 disclosure 격차는 PRD/JCAP editor desk-reject 사유 가능."

공격 강도: ★★★★
방어: 사전 self-disclose 으로 차단.

### A8 — Community blog/critic
> "31% 가 SNS·Twitter 헤드라인이 되면, 후속 검증자가 '항등식 6개' 사실 발견 시 이론 신뢰도 한 번에 붕괴."

공격 강도: ★★★★
방어: 첫 광고에서부터 "31% 광고 / 13% substantive" 양쪽 명시.

---

## 2. 공격 종합 — 정직 disclosure 요구

| 메트릭 | 현재 광고 | 실체 (audit-honest) |
|---|---|---|
| PASS_STRONG count | 10/32 = **31%** | 10/32 = 31% (raw) |
| PASS_STRONG (substantive, 항등식 차감 후) | (미보고) | **4/32 = 13%** |
| PASS_IDENTITY (산술 항등식) | (PASS_STRONG 에 합산) | 6/32 = 19% (별도 카테고리 권장) |
| effective independent PASS | (미보고) | 4 + 1 (항등식 cluster 자유도) = **5/32 ≈ 16%** |

**8인팀 합의 권고**: README/§0/abstract 모두에 "31% PASS_STRONG, 그 중 13% substantive (4건), 19% σ₀ 항등식 따름결과 (6건)" 양쪽 동시 표기. 31% 단독 광고 즉시 폐기.

## 3. 공격 회피 전략 (3-pronged)

1. **Reframing (이 세션 NEXT_STEP/REVIEW)** — §6.5(e) 를 PASS_IDENTITY 분리 + 6 항등식 *비자명 implication* 별도 명시로 격상.
2. **Substantive 4건 강화** — Newton/BBN/Cassini/EP 의 *비자명성* 본문 §3.4–§4.1 강조 (각 항목이 왜 항등식이 아니라 *예측* 인지 한 줄씩).
3. **광고 동기화** — README TL;DR + abstract: "31% (raw) / 13% (substantive)" 병기.
