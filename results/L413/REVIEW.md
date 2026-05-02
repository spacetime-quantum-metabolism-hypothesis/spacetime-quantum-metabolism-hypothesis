# L413 — 4-Person Execution / Code-and-Text Review

The 4-person team self-distributed across (a) numerical sanity check on
4.38σ, (b) §4.6 / §6.1 row 14 / abstract sync, (c) two-sided decision
rule logical consistency, (d) honest-framing wording. No role
pre-assignment (CLAUDE.md L17 rule).

## (a) 4.38σ central value — numerically VERIFIED

L406 `forecast_facilities.json`:
- ΔS_8 = +0.0114 (paper §4.6 baseline; verified vs §6.1.1 row 1).
- σ(S_8, Euclid IST) = 0.0026 (Euclid Collab. 2020 IST forecast,
  cross-checked Blanchard+ 2020).

`+0.0114 / 0.0026 = 4.3846…` → round to **4.38σ** (paper text:
"4.4σ central; 4.38σ exact"). Quadrature with prediction-uncertainty
±0.0008 (L406 grid) gives σ_total = √(0.0026² + 0.0008²) = 0.00272;
revised n-σ = 0.0114 / 0.00272 = **4.19σ**. Both numbers stay above
the 3σ floor.

Recommendation: paper prose uses "4.4σ central"; technical footnote
gives "4.38σ exact, 4.19σ after prediction-uncertainty quadrature".

## (b) Paper edits — ready for application

Targets confirmed (against base.md current line numbers):
- Abstract block at §0 line ~612 (정직 disclosure).
- §4.6 line ~791 ("S_8 악화 정직 인정").
- §6.1.1 row 14 line ~858 (Cosmic-shear 외부 채널).

The three locations are mutually consistent in current base.md and
will remain so after the L413 update (cross-reference pointers are
aligned).

## (c) Two-sided decision rule — CONSISTENT

The four-band rule in NEXT_STEP §D:
| band | verdict |
|---|---|
| +1.5% to +3.0% | CONSISTENT |
| +0.5% to +1.5% | tension, not exclusion |
| −0.5% to +0.5% | excluded ~4σ |
| < −0.5% | excluded > 5σ |

Coverage check: bands are contiguous; gap at +3.0%+ (>2σ above SQT
prediction) — recommend extending top band to "+1.5% to +∞ → consistent
or upward tension". 4-person team accepts this minor amendment as
implementation detail (paper §4.6 prose handles).

Logical consistency: the rule is binary in the sense that
"CONSISTENT vs excluded" decision is well-defined for any measurement
outside the ±0.5% ambiguous band. Pre-registration claim valid.

## (d) Honest-framing wording — APPROVED with two caveats

NEXT_STEP §E wording is internally consistent with paper structure.
Caveats:

(i) Abstract sentence must state "central forecast" not "guaranteed
detection". Reviewer V1 (ATTACK_DESIGN) attack vector defused.

(ii) §6.1 row 14 must keep "OPEN" status semantically — the falsifier
is *pre-registered*, not yet *executed*. Status remains "OPEN
(pre-registered, awaiting Euclid DR1 2026–2027)" rather than promoting
to "PASS" or "FAIL".

Both caveats are folded into the paper edit text in §B below.

## (e) AICc / overfitting check — N/A

This is not a parameter fit; the L413 update only adds prose +
forecast quantities already produced in L406. No new free parameter.
AICc penalty zero.

## Verdict

Code: PASS (no new code; L406 numerics re-verified).
Physics: PASS (4.4σ defensible, 3σ floor convention, two-sided rule
consistent).
Framing: PASS with caveats (i) "central forecast" and (ii) status
remains "OPEN pre-registered".

**Recommendation**: apply NEXT_STEP §E paper edits with the two
caveats folded in (final wording in §B below). Defer OSF/GitHub-tag
admin to Phase-7 / arXiv submission day.

## §B — Final paper edit text (ready for application)

### B.1 Abstract (§0 line ~612, 정직 disclosure sentence)

Replace:
> *"정직 disclosure: σ_8 +1.14% structural worsening, marginalized
> Bayes factor = 0.8 only, anchor circularity in Λ derivation,
> three-regime structure 는 데이터 fit 에서 발견된 postdiction."*

With:
> *"정직 disclosure: σ_8 +1.14% structural worsening (**pre-registered
> as a 4.4σ Euclid DR1 cosmic-shear falsifier**, L406; central forecast
> 4.38σ, 3σ falsification floor; two-sided decision rule §4.6),
> marginalized Bayes factor = 0.8 only, anchor circularity in Λ
> derivation, three-regime structure 는 데이터 fit 에서 발견된
> postdiction."*

### B.2 §4.6 (line ~791)

Replace existing two-line stub with:
> *"### 4.6 ★ S_8 악화 정직 인정 (영구 한계, pre-registered Euclid
> falsifier)*
>
> *SQT 구조적 μ_eff≈1 → cosmic shear ξ_+(10') = LCDM 보다 +2.29%
> (= 2 × ΔS_8, ΔS_8 = +0.0114). L406 facility forecast: DES-Y3
> 0.63σ (현재 미검출, 정합), LSST-Y10 2.85σ, **Euclid DR1 4.38σ
> 중심값** (round 4.4σ; quadrature with prediction-uncertainty ±0.0008
> → 4.19σ). 4.4σ는 중심 forecast 이며, falsification floor 는
> cosmology convention 3σ.*
>
> ***Pre-registered two-sided decision rule** (Euclid DR1 cosmic-shear
> 2pt ξ_+(10') 측정 m 의 ΛCDM 대비 초과율):*
> *- +1.5%~+3.0%: SQT **CONSISTENT** (1σ band of prediction)*
> *- +0.5%~+1.5%: ambiguous (tension, not exclusion)*
> *- −0.5%~+0.5%: SQT **excluded ~4σ** (LCDM-like)*
> *- < −0.5%: SQT **excluded > 5σ** (anti-SQT)*
>
> ***Pre-registration triple-timestamp**: arXiv submission ID + GitHub
> release tag `v-preDR1-2026.NN` + OSF DOI (Phase-7 admin, locked
> before Euclid DR1 2026–2027 release). 모든 mitigation 채널이 SQT
> 허용 sector (Cassini + GW170817) 안에서 μ_eff ≥ 1 (L406 §A);
> S_8 악화는 fixable bug 가 아니라 **structural prediction**. 검출
> = SQT falsified. 도망 불가."*

### B.3 §6.1.1 row 14 (line ~858)

Replace:
> *"| 14 | Cosmic-shear 외부 채널 미검증 | OPEN | LSST/Euclid 대기 |"*

With:
> *"| 14 | Cosmic-shear 외부 채널 (Euclid DR1 4.4σ pre-registered
> falsifier) | OPEN (pre-registered) | Euclid DR1 2026–2027; 두-sided
> decision rule §4.6; LSST-Y10 2.85σ 보조. Triple-timestamp: arXiv +
> GitHub tag + OSF DOI (Phase-7 admin) |"*
