# L513 — §6.5(e) Self-audit Headline 격하 (Hidden DOF AICc penalty 통합)

> **작성일**: 2026-05-01
> **substrate**: L502 (`results/L502/HIDDEN_DOF_AICC.md`) + L495 hidden DOF audit + paper/base.md §6.5(e)
> **CLAUDE.md 정합성**: 신규 물리 수식 0줄, 신규 파라미터 0개. AICc bookkeeping 의 §6.5(e) 반영 한정.
> **타깃 파일**: `paper/base.md` §6.5(e) (L513 항목 신규 추가, line ~1055)

---

## 0. 정직 한 줄

**L502 hidden DOF AICc penalty 적용 시 PASS_STRONG 후보 0 건 유지 — 광고 substantive 13% (4/32) 는 정직 잣대 하에서 *0%* 로 환원된다.**

---

## 1. 임무

L502 발견을 §6.5(e) self-audit headline 에 직접 반영, "substantive 13% / raw 28%" 양면 표기에 *hidden DOF 차감 시 0%* 라는 세 번째 면 (worst-case AICc penalty) 을 명시.

---

## 2. 적용 변경 — paper/base.md §6.5(e)

L513 항목을 §6.5(e) 마지막 sub-bullet 로 추가 (line ~1055, "헤드라인 (정직 양면 표기, L415 sync)" 직후).

추가된 핵심 문장:

- L502 hidden DOF AICc penalty (보수 k_hidden = 9) 적용 시 PASS_STRONG (substantive) 4 건 (Newton / BBN / Cassini / EP) 전부 ΔAICc ≥ +18 로 PASS_MODERATE 이하 강등.
- applicable-only (k_h_app) 차감 시 Newton 은 ΔAICc=+4 로 즉시 강등, BBN/Cassini/EP 는 +2 "RETAINED 경계" — 보수 풀카운트 (k_h=9) 에서는 전원 탈락.
- "substantive 13% (4/32)" 추정도 hidden DOF 차감 시 *0%* (PASS_STRONG 후보 0 건 유지).
- 본 paper 의 PASS_STRONG 카테고리 단독 인용은 (raw / substantive 어느 쪽이든) AICc penalty 미적용 가정 하에서만 성립함을 명시.

---

## 3. L502 표 (참고용 재인용, `results/L502/HIDDEN_DOF_AICC.md` §2)

| Claim | 광고 status | k_h_app | ΔAICc(naive) | ΔAICc(k_h_app) | ΔAICc(k_h=9) | 판정 (k_h=9) |
|-------|-------------|---------|--------------|----------------|--------------|---------------|
| Newton 회복 | PASS_STRONG (substantive) | 2 | 0 | +4.0 | +18.0 | **DEMOTED** |
| BBN ΔN_eff | PASS_STRONG (substantive) | 1 | 0 | +2.0 | +18.0 | **DEMOTED** |
| Cassini \|γ−1\| | PASS_STRONG (substantive) | 1 | 0 | +2.0 | +18.0 | **DEMOTED** |
| EP \|η\|<10⁻¹⁵ | PASS_STRONG (substantive) | 1 | 0 | +2.0 | +18.0 | **DEMOTED** |
| L482 RAR (a₀) | PASS_STRONG candidate | 2 | +0.703 | +4.707 | +18.756 | **DEMOTED** |

> 부호 규약: SQT − 기준선. +2/+6/+10 은 strong-equivalence / 강등 / 탈락 임계값.

PASS_STRONG (substantive 4) + L482 RAR (candidate) 모두 보수 hidden DOF 풀카운트에서 PASS_MODERATE 이하 강등 → **AICc 정직 잣대 하 PASS_STRONG = 0 건**.

---

## 4. 기록 — 정직 양면 표기 → 삼면 표기 확장

기존 (L415 sync):
> "raw 28% PASS_STRONG / 13% substantive (4건) + 9% σ₀ 항등식 + 3% CONSISTENCY_CHECK"

L513 보강:
> "raw 28% PASS_STRONG / 13% substantive (4건) [hidden DOF penalty 차감 시 0%] / 9% σ₀ 항등식 / 3% CONSISTENCY_CHECK"

raw / substantive / AICc-penalised 셋 모두 동시 보고 의무. AICc-penalised 0% 단독 인용도 (반대 방향) 금지 — hidden DOF 카운트 자체가 보수 9 / 확장 13 의 범위를 가지므로 *범위* 표기 필수.

---

## 5. 비-수정 항목 (정직 한계)

- 32-claim 등급 분포 (PASS_STRONG/IDENTITY/INHERITANCE/CONSISTENCY/PARTIAL/NOT_INHERITED) 카운트는 **변동 없음**. AICc penalty 는 *해석 잣대* 의 추가 layer 이지, claim 분류 enum 자체를 바꾸지 않는다.
- §6.1 OBS-FAIL (S_8) 별개 카테고리 유지 — hidden DOF 와 무관.
- README TL;DR / abstract / claims_status.json 동기화는 본 L513 에서는 §6.5(e) 본문만 손대고 미실시 (별도 라운드 필요).

---

## 6. 정직 한 줄 (재진술)

**Hidden DOF AICc penalty 적용 시 PASS_STRONG 후보 0 건 — 광고 substantive 13% 는 정직 잣대 하에서 0%.**
