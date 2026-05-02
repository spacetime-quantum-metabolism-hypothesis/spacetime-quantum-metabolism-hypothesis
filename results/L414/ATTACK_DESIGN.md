# L414 — ATTACK_DESIGN (8인팀 공격 설계)

날짜: 2026-05-01
주제: PR P0-3 — §6.5(e) Self-audit reframing (raw 31% / substantive 13% / σ₀ identity 9%)
선행 결과: L409 §6.5(e) 양면 reframing 완료, 그러나 §0 / TL;DR / cross-ref 9개 위치 sync 미완.

---

## 8인팀 자율 공격 (역할 사전 지정 없음, 토의 자연 분담)

### A1 — Reviewer 광고 over-claim 공격
- 표적: Abstract / TL;DR 의 "31%" 단독 수치.
- 공격 시나리오: PRD/JCAP 심사위원이 §0 "31% strong-pass" 만 보고 §6.5(e) 까지 안 읽음. 본문 reframing 이 있어도 abstract 가 over-claim 이면 desk reject.
- 위험도: **HIGH**. SQMH 의 가장 큰 평판 리스크.
- 방어: §0 line 614 자체에 "13% substantive + 9% σ₀ identity" 양면 표기.

### A2 — 카운트 산수 일관성 공격
- 표적: 4 + 3 + 8 + 8 + 8 + 0 = 31 ≠ 32 (L409 REVIEW 자체에 1건 미스매치 인정됨, v=g·t_P 위치 결정 미해결).
- 공격: "32 claim 중 분류된 합이 31. 정직 audit 이 카운트도 못 맞추는데 결론을 어떻게 신뢰?"
- 방어: 추가 카테고리 `PASS_CONSISTENCY_CHECK` (1건, Λ origin) 으로 분리하여 합 = 32. line 149 TL;DR 은 이미 이 포맷.

### A3 — enum drift 공격
- 표적: schema enum 9종에 `PASS_IDENTITY` 없음. 본문 §6.5(e) 에는 `PASS_IDENTITY` 사용. JSON 자동화 도구가 unknown enum 에서 실패.
- 방어: schema 의 status enum 에 `PASS_IDENTITY`, `PASS_CONSISTENCY_CHECK` 추가 (총 11종).

### A4 — Cross-ref drift 공격
- 표적: line 614 (§0), line 487 (schema breakdown), line 750 (§6.1 cross-ref) 의 카운트 표기가 서로 다름.
  - line 614: "31% + 19% inherited + 50% caveat/gap"
  - line 487: "PASS_STRONG 10 + PASS_TRIVIAL 2 + PASS_BY_INHERITANCE 4 + PARTIAL 8 + NOT_INHERITED 8"
  - line 902 (§6.5(e)): "13% substantive + 9% identity + 25% inheritance + 25% PARTIAL + 25% NI"
- 공격: 동일 audit 의 3가지 다른 표기 → 어느 것이 canonical?
- 방어: §6.5(e) 를 single source of truth 로 명시. line 614 / 487 / 750 모두 §6.5(e) 참조하도록 sync.

### A5 — "광고 31% 의도 은폐" 공격
- 표적: substantive 13% 가 진짜라면 광고에 substantive 만 쓰면 됨. 31% 를 abstract 에 끌고 가는 것 자체가 inflation 의도?
- 방어: 양면 표기 의무화 + "31% raw 단독 광고 금지" 를 §6.5(e) 본문 정책으로 못박음 (이미 line 902 에 적용). L414 에서는 §0 에도 명시.

### A6 — PASS_IDENTITY 정의 모호성
- 표적: σ₀=4πG·t_P holographic 항등식 따름결과 3건 (n₀μ, ξ scaling, Λ-theorem) 의 "identity" 분류 기준이 ad hoc.
- 방어: PASS_IDENTITY 정의를 schema 에 명시 — *"산술/차원 분석으로 σ₀=4πG·t_P 항등식 + Planck 단위계로부터 자동 도출되는 quantity. 추가 자유도 0. 항등식 자체를 의심하면 자동 무효."*

### A7 — "PASS_CONSISTENCY_CHECK 1건" 필요성 공격
- 표적: TL;DR line 149 "CONSISTENCY_CHECK 3% (1, Λ origin)" 이 §6.5(e) line 902 에 없음.
- 방어: §6.5(e) 에 PASS_CONSISTENCY_CHECK 카테고리 명시 (Λ origin: ρ_q/ρ_Λ = 1.0000, but circularity → identity 도 substantive 도 아닌 dimensional consistency check).

### A8 — schema v1.1 backward-compat 공격
- 표적: 신규 enum 추가 시 v1.0 클라이언트가 unknown enum 만나서 crash.
- 방어: schema version 을 v1.2 로 bump. 신규 enum (`PASS_IDENTITY`, `PASS_CONSISTENCY_CHECK`) 은 v1.2+ 에서만. 외부 인용은 v1.2 명시 권고.

---

## 8인 합의 결론

1. PR P0-3 의 단순 §6.5(e) reframing 으로는 부족 (A1, A4 cover 안 됨).
2. **통합 reframing 필수**: §0 + TL;DR + §6.5(e) + schema enum 4점 동시 수정.
3. PASS_IDENTITY enum + PASS_CONSISTENCY_CHECK enum 추가로 카운트 합 = 32 정확 일치.
4. §6.5(e) 를 single source of truth 로 선언 — 다른 위치는 모두 cross-ref.
5. schema version v1.0 → v1.2 bump (v1.1 i18n + v1.2 신규 enum).

## 정직 한 줄

> "31% over-claim 위험은 abstract 차원의 문제이지 §6.5(e) 본문만 고친다고 사라지지 않는다 — 통합 reframing 필수."
