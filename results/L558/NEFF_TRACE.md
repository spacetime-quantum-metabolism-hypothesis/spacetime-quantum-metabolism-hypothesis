# L558 — N_eff = 4.44 vs disk "≈ 4" 통계 base 신뢰성 추적

**Date**: 2026-05-02
**Scope**: 본 세션 메타 분석에서 인용된 falsifier 독립도 `N_eff = 4.44` (8.87σ ρ-corrected)
가 L498 원자료에 실재하는지 vs 메타-분석에서 생성된 hallucination 인지 판정.
**Edits**: 0 (audit-only).

---

## §1. grep 결과 표

### §1.1 `results/L498/` (원자료, source of truth)

| 파일 | 행 | 토큰 | 컨텍스트 |
|---|---:|---|---|
| `l498_results.json` | L149 | `N_eff_CheverudGalwey` | `5.7063492063492065` |
| `l498_results.json` | L150 | `N_eff_ParticipationRatio` | **`4.436619718309859`** ← **4.44 의 정밀치** |
| `l498_results.json` | L151 | `N_eff_LiJi` | `5.0` |
| `l498_results.json` | L153 | `Z_combined_correlation_corrected_all6` | **`8.871817515312959`** ← **8.87 의 정밀치** |
| `FALSIFIER_INDEPENDENCE.md` | L71 | "Estimator | N_eff" 표 헤더 | — |
| `FALSIFIER_INDEPENDENCE.md` | L74 | `Participation ratio` | **`4.44`** (반올림) |
| `FALSIFIER_INDEPENDENCE.md` | L81 | "Best estimate" | `N_eff ≈ 4.4–5.0`, "not 6" |
| `FALSIFIER_INDEPENDENCE.md` | L88 | "All 6, ρ-corrected" | **`8.87 σ`** |
| `FALSIFIER_INDEPENDENCE.md` | L108 | conclusion #1 | "participation-ratio estimate (4.44) is the most conservative" |
| `FALSIFIER_INDEPENDENCE.md` | L117 | replacement wording | "**N_eff ≈ 4.4** independent observable channels" |
| `FALSIFIER_INDEPENDENCE.md` | L126 | TL;DR | "compress to N_eff ≈ 4.44 truly independent channels (participation ratio); … 8.87 σ" |

→ **L498 원자료에 4.44 와 8.87 정확히 명시.** Participation-ratio = 4.4366… 가 round-to-2dp = 4.44.

### §1.2 `paper/base.md`

| 행 | 표기 | 컨텍스트 |
|---:|---|---|
| L149 | `N_eff=4.44, 8.87σ ρ-corrected` | self-audit headline 인용 |
| L618 | `N_eff=4.44 after correlation correction; 8.87σ` | §4.9 (요약) |
| L953 | `L498 N_eff=4.44, 8.87σ ρ-corrected` | abstract-level 카운트 표 |
| L961 | `N_eff=4.44 … 8.87σ … not 11.25σ` | falsifier 정의문 |
| L972 | "participation-ratio 4.44 (most conservative, **adopted as headline**)" + Li–Ji 5.00 / Cheverud–Galwey 5.71 / naive 6.00 4-estimator 표 | N_eff estimator 설명 |
| L1077 | row 24 (verification table): "N_eff = **4.44** (participation-ratio, headline)" + `8.87σ` ρ-corrected all six + 9.95σ active 5 + naive 11.25/12.32 단독 인용 금지 | **canonical row** |

→ paper/base.md 6개 위치, **모두 4.44 정확 표기**, "≈ 4" 표기 **없음**.

### §1.3 `paper/arXiv_PREPRINT_DRAFT.md`

| 행 | 컨텍스트 |
|---:|---|
| L13 (Abstract) | "participation-ratio effective number is N_eff = 4.44, combined ρ-corrected significance 8.87σ" |
| L117 (§5) | "compress to N_eff = 4.44 (participation-ratio; *headline*) … corrected ρ-aware combined is 8.87σ" |
| L128 (§5) | 4-estimator 표: "Participation-ratio 4.44 (headline) … Li–Ji 5.00 … Cheverud–Galwey 5.71 … naive 6.00" |
| L161 | 결론: "compress to N_eff = 4.44, ρ-corrected 8.87σ" |
| L210 | conclusion-tail: "N_eff = 4.44 / 8.87σ ρ-corrected" |

→ arXiv 프리프린트 5개 위치, **모두 4.44 정확 표기**, "≈ 4" 표기 **없음**.

### §1.4 `paper/MNRAS_DRAFT.md`

`grep -nE "4\.44|8\.87|N_eff"` 결과: **0 hit**. (L557 §3.4 가 이미 명시했듯
falsifier 통계는 MNRAS scope 외 — Path-γ galactic-only, cosmology 사항은 companion JCAP.)
MNRAS draft 의 N_eff 인용은 의도적으로 부재.

### §1.5 `claims_status.json` L631 (limitation `L25-N_eff-falsifier-channel-correlation`)

```
future_plan: "… N_eff ≈ 4 (active 5 detection 중) per Cheverud–Galwey. Bonferroni α = 0.05/5 = 0.01 …"
i18n.en.label: "… 6 pre-registered channels collapse to N_eff ≈ 4 active detection …"
i18n.ko.label: "… 6 사전등록 채널이 N_eff ≈ 4 (active 5 중) 로 축소 …"
```

→ claims_status.json 은 **`≈ 4` 표기**, 그리고 estimator 를 **"per Cheverud–Galwey"** (실제 5.71)
이라고 명시. 4.44 (participation-ratio) **0 hit**.

다만 **claims_status.json L1077** (row 24, 별도 verification table) 에는 정확히
**"N_eff = 4.44 (participation-ratio, headline) … 8.87σ ρ-corrected"** 가 적혀 있음.
즉 claims_status.json **내부 자기 충돌**: limitations 항목 (L631) 은 "≈ 4 / Cheverud–Galwey",
verification row 24 (L1077) 는 "4.44 / participation-ratio".

---

## §2. 4.44 의 출처 결정

**(a) L498 원자료에 4.44 명시되어 있는가?** → **YES**.
- `l498_results.json` L150: `N_eff_ParticipationRatio = 4.436619718309859` (정밀치, 4.44 = 2dp 반올림)
- `FALSIFIER_INDEPENDENCE.md` L74, L108, L117, L126: `4.44` 직접 표기
- 8.87 도 동일: `Z_combined_correlation_corrected_all6 = 8.871817515312959`

**(b) 메타 분석 hallucination 가능성** → **NO**. paper/base.md, arXiv 프리프린트, claims_status.json
row 24 의 4.44 인용은 모두 L498 원자료에서 직접 산출된 값.

**(c) 다른 estimator 와 혼동 가능성** → **부분적 YES, 단 paper 인용은 무관**:
- claims_status.json **L631** 의 `"N_eff ≈ 4 per Cheverud–Galwey"` 는 **이중 오류**:
  (i) Cheverud–Galwey 추정량은 실제 5.71 (4 가 아님), (ii) 본문 headline 으로
  채택된 estimator 는 participation-ratio (4.44) 이지 Cheverud–Galwey 가 아님.
  L631 표기가 estimator 를 잘못 인용한 것.
- paper / row 24 / arXiv 의 `4.44` 인용은 estimator 정확 (participation-ratio).

**판정**: **4.44 는 L498 원자료에 정확히 명시된 값** (case a). hallucination 아님.
claims_status.json L631 의 `≈ 4` 표기는 (i) **반올림 (4.44 → 4)** + (ii) **estimator 라벨 오기재
(participation-ratio → Cheverud–Galwey)** 의 보고 단계 drift 이지, paper 본문의 4.44 가
틀린 것이 아님.

---

## §3. 8.87σ 의 base

| 출처 | 값 | 정밀치 |
|---|---|---|
| `l498_results.json` L153 | `Z_combined_correlation_corrected_all6` | **8.871817515312959** |
| `FALSIFIER_INDEPENDENCE.md` L88 | "All 6, ρ-corrected" | **8.87 σ** |

추가로 L498 원자료는 다음을 보고:
- 9.95σ (active 5, ρ-corrected) — paper/base.md L1077 + arXiv 모두 인용
- 11.25σ naive (all 6) / 12.32σ naive (active 5) — *standalone 인용 금지* 라벨 부착

→ **8.87σ 도 L498 원자료에 정확히 존재**. paper / arXiv / row 24 인용 모두 정합.

---

## §4. 4.44 가 만약 hallucination 이었다면 영향 (가상 시나리오)

**(실제 결론은 hallucination 아님이므로 정정 의무 없음.)** 단, 만약 가상으로 4.44 가
fabricated 였다면:

| 채널 | 현재 인용 위치 | 영향 |
|---|---|---|
| Trajectory (L498 → L514 → L516 → L498-cite) | `paper/base.md` L149/L618/L953/L961/L972/L1077 | 본문 6개 위치 4.44 → 정확 estimator (Cheverud–Galwey 5.71 또는 Li–Ji 5.00) 로 정정 + Z 재계산 의무 |
| Acceptance (verification row 24, ACK) | claims_status.json L1077 | row 24 status 재검토 |
| Falsifier disclosure (arXiv §5) | arXiv L13/L117/L128/L161/L210 | 5 위치 정정 |
| MNRAS | (없음) | 무관 |

→ **현재 상태 (case a)**: 4.44 는 L498 원자료에 실재 → **인용 정정 의무 0**.
단 **claims_status.json L631 의 "Cheverud–Galwey" estimator 라벨 오기재**는 별도로
정정 후보 (audit-only 단계, 본 보고서는 edit 0).

---

## §5. 정직 한 줄

`N_eff = 4.44` 는 L498 원자료 `l498_results.json` L150 에 `N_eff_ParticipationRatio =
4.436619718309859` 로 정확히 존재하고 8.87σ 도 `Z_combined_correlation_corrected_all6
= 8.871817…` 로 일치하므로 paper/base.md (6 위치) 와 arXiv 프리프린트 (5 위치) 의
인용은 모두 hallucination 이 아니라 원자료에서 산출된 정밀치이며, claims_status.json
L631 의 `≈ 4` 는 단순 2dp 반올림 + estimator 라벨 오기재 (participation-ratio → Cheverud–Galwey)
의 limitation-row 단계 보고 drift 일 뿐 본문 통계 base 신뢰성에는 영향 없다.
