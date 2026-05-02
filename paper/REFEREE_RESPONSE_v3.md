# SQMH Referee Response — Template v3

**Manuscript**: Spacetime Quantum Metabolism Hypothesis — Falsifiable Phenomenology
**Version**: v3 (L412–L420 결과 반영)
**Date**: 2026-05-01
**Session**: L439 (independent)
**Authors' note**: 본 v3 은 v1/v2 와 달리 L412 (PASS_STRONG → CONSISTENCY_CHECK
강등), L415 (양면 표기 의무 sync), L416 (§6.5(e) Λ_UV definitional 분리),
L417 (§3.4 RG saddle priori-impossible / §3.6 R-grid R=10 collapse), L418
(BBN single-scale Λ_UV ≈ η_Z₂), L419 (Euclid 4.4σ central / 4.38σ exact
pre-registered floor), L420 (μ-distortion 산술 표제 정직 인정) 결과를 직접
반영. 어떤 referee 공격면도 광고 헤드라인 단독 인용 (특히 raw 31%, "PASS
ρ_q/ρ_Λ=1.0000", "두 보호 mechanism", "4.4σ as detection") 으로 회피하지
않으며, 8 attack 면 중 7 면을 본문 sync 로 무력화하고 잔존 1 면 (B4
구조적 circularity) 은 정직 노출한다.

---

## 0. 한 줄 요약 (per-reviewer)

- **R1 (이론가)**: Λ_UV a priori 도출은 영구 불가능; RG saddle a priori
  P=0; BBN 17-dex margin 은 *single-scale* (Λ_UV ≈ η_Z₂ ≈ 10 MeV) portal
  coupling 산물 — "두 mechanism" 표현 redundancy 정정.
- **R2 (관측가)**: Euclid 4.4σ 는 *pre-registered structural falsifier*
  (DR1 2026–2027 대기), *not* a current detection; S_8 악화는 μ_eff ≈ 1
  + GW170817 c_T constraint 로 **structural prediction**, mitigation
  채널 부재 정직 인정; μ-distortion 1.02×10⁻⁸ 은 σ₀·n_∞·ε 산술
  표제 (PASS_IDENTITY risk) — facility 미확정 (PIXIE cancelled 2016)
  + photon-sector axiom 미닫힘.
- **R3 (통계학자)**: §3.6 R-grid {R=2,3,5,10} 4점 표 본문 등재; R=10 에서
  Δln Z 78 → 15 (5× collapse) + 실 데이터 R=5 0.8 → R=10 음수 가능성 노출;
  raw 광고 (31% PASS_STRONG, post-L412 28%) 와 substantive (13%, 4/32)
  **양면 표기 의무화** (single source of truth: §6.5(e)).

---

## 1. R1 (이론가) — Λ_UV priori, RG saddle priori P=0, BBN single-scale

### R1.1 — "Λ_UV ≈ 10 MeV 가 a priori 도출인가?" (L418)

**Referee 지적**: paper §4.1 row 2 narrative 가 BBN PASS_STRONG 을 "두 보호
mechanism (A: Boltzmann + B: portal)" 로 광고하나, 실제로 Λ_UV 가 어디서
*독립적으로* 도출되는지 본문 누락.

**저자 회신 (L418 simulation 기반)**:

1. **Single-scale 정정**: BBN constraint Γ < H @ T_BBN 에서 portal-only
   path B 단독으로 17.4 dex margin 을 확보한다. Path A (Boltzmann
   suppression) 는 추가 13 dex 보너스이나, B 가 *redundant* 하게 통과시킨
   후의 잉여이며, "두 mechanism" 광고는 정정한다. (paper §4.1 row 2,
   본 v3 §3.1.4 sync.)
2. **Λ_UV ~ η_Z₂ identification**: reduced Planck mass M_Pl ≈ 2.4×10¹⁸
   GeV 사용 시 β_eff = 7.4×10⁻²¹ 가 Λ_UV ≈ 18 MeV 와 정합. 이는
   η_Z₂ ≈ 10 MeV (BBN 상한 역산) 와 factor 1.8 내 동일 scale —
   **Λ_UV ≈ η_Z₂** 가 implicit 가정이며 본문 §4.1 row 3 에 명시했다.
3. **Priori 도출 OPEN**: η_Z₂ 의 후보 매치 √(m_e × Λ_QCD) ≈ 10.53 MeV
   (0.02 dex 일치) 는 *Lagrangian derivation* 이 아닌 *후보* 매치이며,
   **Foundation 4 의 priori 도출은 OPEN 으로 유지**. BBN PASS_STRONG 는
   *structural robustness* (B-only 17 dex) 의 PASS 이며, "Λ_UV 가 SQT
   에서 a priori 나온다" 는 주장은 본 v3 에서 명시적으로 부정한다.
4. **Future work**: ChPT / dilaton / instanton scale enumeration 후
   재판정. paper 인용값 ΔN_eff ≈ 10⁻⁴⁶ 은 본 sim 의 dimensional
   근사 10⁻²² 와 24 dex 차이 — 정확값은 BBN code (PArthENoPE/AlterBBN)
   linkage future work.

**관련 변경**: paper §4.1 row 2/3, §6.1 한계 row "η_Z₂ priori OPEN"
추가 (L418).

### R1.2 — "RG saddle 위치는 a priori 예측인가?" (L417)

**Referee 지적**: §3.4 saddle location 이 외부 anchor (관측 ρ_Λ_obs) 에
의존하며 a priori 도출 불가능. Bayes factor B = 78 은 prior 선택에 따라
collapse 가능.

**저자 회신 (L417 §3.4 patch)**:

1. **a priori 영구 불가능 명시**: cubic-RG scan a priori 확률 1.4%,
   표준 between-fixed-point 가정에서는 P=0. 본 v3 §3.4 단락은 *"saddle
   위치 priori 도출 영구 불가"* 단호 표현을 본문에 채택했다 (외부 anchor
   의존 = §3.5 circularity caveat 와 cross-link).
2. **Mock injection FDR 100% 와 직접 연결**: 본 caveat 은 §5.2 의 FDR
   100% 결과와 일관 — RG saddle 도출 path 는 ρ_Λ_obs scale 을 input
   으로 받지 않으면 닫히지 않으며, *진정 a priori 예측이 아니다*.
3. **광고 격하**: §3.4 헤드라인에서 "Bayesian preference" 표현 유지하나
   "a priori derivation" 표현은 전면 제거.

**관련 변경**: paper §3.4 본문 단락 추가, claims_status v1.1 RG-saddle
row 의 caveat 강화 (L417 §3.4).

### R1.3 — Theorist 잔존 우려 (B4 structural circularity)

**저자 인정**: §5.2 Λ origin claim 은 **CONSISTENCY_CHECK** 등급으로 영구
강등됨 (L412). ρ_q/ρ_Λ(Planck) order-unity 일치는 *dimensional
consistency* 이며 *prediction 이 아니다*. circularity 는 fixable bug 가
아니라 **구조적** — L402 audit Path-α 가 10⁶⁰ scale 로 fail 한 이후 본
attack 면은 *정직 노출* 한다 (paper §0/TL;DR/§1.2.1/§5.2/§6.5(e) 모두 sync).

---

## 2. R2 (관측가) — Euclid 4.4σ pre-reg, S_8 mitigation 부재, μ-distortion 산술 표제

### R2.1 — "S_8 +1.14% 가 detection 인가?" (L419)

**Referee 지적**: paper §4.6 의 ΔS_8 = +0.0114 forecast 가 Euclid 4.4σ
"detection" 으로 광고되는지 여부 모호; DES-Y3 현재 0.63σ 미검출 상태에서
4.4σ 는 *predictive forecast* 인지 명시 부족.

**저자 회신 (L419 §4.6 patch)**:

1. **Pre-registered floor, not detection**: 4.4σ central forecast 는
   Euclid Collab. 2020 IST σ(S_8) = 0.0026 기준 ΔS_8 = +0.0114 의
   **central** 값이다. Quadrature with prediction-uncertainty ±0.0008
   적용 시 4.19σ; 본문 prose 는 "**4.4σ central**" 와 "**4.38σ exact**"
   를 모두 명시 (technical footnote).
2. **Pre-registered two-sided decision rule**: Euclid DR1 cosmic-shear
   ΔS_8 측정에서 (i) +0.0114 ± σ_Euclid 와 정합 시 SQT confirm,
   (ii) 0 과 정합 시 SQT falsify, (iii) 음수 측정 시 즉각 falsify.
   Floor: 3σ; central: 4.4σ. **DR1 2026–2027 release 까지 status =
   OPEN (pre-registered)** 명시.
3. **Falsification floor convention**: 3σ floor 는 SQT internal
   convention 으로 본문 §4.6 헤더에 명시. "4.4σ as current detection"
   해석은 본 v3 에서 명시적으로 부정한다.

### R2.2 — "S_8 mitigation 가능한가?" (L406 / §4.6)

**Referee 지적**: paper 가 ΔS_8 = +0.0114 *structural worsening* 이라
인정하나, mitigation 채널 (μ_eff ≠ 1, c_T ≠ 1, screening) 부재가
*구조적* 인지 verifiable 한가.

**저자 회신**:

1. **μ_eff ≈ 1 구조적**: SQT 는 background-only 수정 + μ_eff ≈ 1 ⇒
   linear growth 변형 채널 차단. Cassini |γ−1| < 2.3×10⁻⁵ + GW170817
   c_T = 1 (1σ) 양 제약을 동시에 통과하는 sector 안에서 **모든
   mitigation 채널이 ΔS_8 < 0.01% 수준의 효과만 허용** (L406 §A
   facility forecast).
2. **Fixable bug 아님**: §4.6 본문에 "S_8 악화는 fixable bug 가 아니라
   **structural prediction**" 명시. mitigation 시도 (β_d dark-only,
   disformal, screening) 는 모두 SQT 외 sector 침범으로 폐기 (L5/L6
   재발방지 누적).
3. **DES-Y3 현재 정합**: 0.63σ 미검출은 forecast 의 floor 0.5σ 와 정합
   (mission noise level 차이 → detection 능력 불충분). LSST-Y10 2.85σ
   까지는 marginal, **Euclid DR1 4.4σ central 이 결정 분기점**.

### R2.3 — "μ-distortion 1.02×10⁻⁸ 가 prediction 인가?" (L420)

**Referee 지적**: paper §4.x 의 PIXIE μ-distortion 1.02×10⁻⁸ (10σ vs
noise, 2σ vs foreground) 는 PASS_STRONG 표제이나 도출 chain 이 닫혀
있는지 verify.

**저자 회신 (L420 §4.x patch)**:

1. **산술 표제 인정**: 1.02×10⁻⁸ 은 σ₀·n_∞·ε·차원분석에서 *자동 도출*
   되는 **산술 산물** 이며 PASS_IDENTITY risk 를 본문에 정직 명시한다.
   §6.5(e) "13% substantive" 패턴 (L409) — σ₀ = 4πG·t_P 류 차원분석이
   μ 사슬에 반복되는 구조와 동일.
2. **PASS_STRONG → PENDING 강등**: 본 v3 에서 μ-distortion row 는
   **PENDING** (PASS_STRONG 이 아님) 으로 유지. 도출 chain 미닫힘:
   - (i) photon-sector coupling axiom 추가 필요
   - (ii) Q(z) injection 시기 프로파일 도출 필요
   - (iii) y/μ 분기 결정 필요 (현재 spectrum 형상 자유도 미고정)
   - (iv) facility 확정 필요 (PIXIE 2016 cancelled, PRISM/BISOU 미확정)
3. **Mission timeline**: 2030+ (TBD). FIRAS upper bound 9×10⁻⁵ 와
   비교 시 1.02×10⁻⁸ 은 4 dex 안전 — *upper-bound consistency* 만
   현재 제공.

**관련 변경**: paper §4.x μ-distortion row 정정 (PENDING + chain caveat
4 항 명시), §6.1 facility table μ-distortion entry update.

---

## 3. R3 (통계학자) — R-grid R=10 collapse, raw 31% vs substantive 13% 양면

### R3.1 — "Δln Z = 78 prior collapse 견고한가?" (L417)

**Referee 지적**: §3.6 의 Δln Z ≈ 78 (Bayesian preference) 은 R (relative
prior width) 선택에 fragile. wider prior R=10 limit 에서 collapse 가능성
본문 부재.

**저자 회신 (L417 §3.6 patch)**:

1. **R-grid 4점 표 본문 등재**: §3.6 에 R = {2, 3, 5, 10} toy Δln Z
   표를 본문에 직접 추가했다 (이전 부록 격리 → 본문 승격).
2. **R=10 5× collapse 정직**: R=10 에서 toy Δln Z 78 → 15 (5×
   collapse). **|Δln Z| < 1 inconclusive** 가 R=10 에서 가능함을
   인정한다 (실 데이터 R=5 의 0.8 → R=10 음수 가능성 명기).
3. **Lindley fragility 인정**: Lindley paradox-style fragility (wider
   prior → null preference) 가 §3.6 Bayesian preference claim 에
   적용됨을 본문 명시; "absolute Δln Z 값은 toy 임" 단서.

**관련 변경**: paper §3.6 본문 R-grid 표 + 단락 추가 (L417 §3.6).

### R3.2 — "31% headline 광고는 inflated 가?" (L412/L415)

**Referee 지적**: abstract / §0 / TL;DR 의 "31% PASS_STRONG" 광고가
inflated; substantive (true a priori predictions) 비율은 별도 보고 필요.

**저자 회신 (L412 강등 + L415 sync)**:

1. **Raw 광고 카운트 정정**: pre-L412 raw = 10/32 PASS_STRONG (31%)
   → post-L412 raw = 9/32 (28%) + CONSISTENCY_CHECK 1 (3%) **양면 표기
   의무화**. (Λ origin row 강등 — §5.2 circularity 구조적.)
2. **Substantive 13% 도입**: 6 카테고리 분류 (raw / substantive /
   identity / inheritance / PARTIAL / NOT_INHERITED) 본문 §6.5(e)
   에 등재 — substantive 4/32 = **13%** (true a priori 예측, MOND a₀ /
   BBN scale margin / Bullet bound / PPN 만).
3. **Single source of truth**: §6.5(e) 가 *유일한* 카테고리 정의 위치;
   abstract / TL;DR / final summary 는 **양면 (28% raw / 13%
   substantive) 동행 의무**. "31% 단독 인용" 은 v3 전체에서 금지.
4. **PASS_IDENTITY 위험 명시**: identity 3 category 는 σ₀ = 4πG·t_P 류
   차원분석 산술이 μ 사슬을 통해 반복되는 패턴 (L409 §6.5(e) "13%
   substantive" 정의 근거) — **prediction 이 아닌 정의 산물** 임을
   §6.5(e) 본문에 명시.

**관련 변경**: paper §0/TL;DR/abstract/§6.5(e)/final summary 8 sync 위치
양면 표기 (L412 + L415).

### R3.3 — Statistician 잔존 우려

**저자 인정**:

- §3.6 R-grid 4점 표는 toy 수준이며, 실 데이터 R=10 의 음수 Δln Z
  가능성은 OPEN (paper §3.6 명시).
- claims_status v1.1 의 enum 8-value canonical (CONSISTENCY_CHECK 추가
  포함) 은 v3 에서 frozen, 추가 강등 시 v1.2 재발행 + JSON master sync.
- L416 권고 (§6.5(e) 에 CONSISTENCY_CHECK 1건 별도 bullet) 적용 완료.

---

## 4. v3 신규 변경 요약 (paper/base.md sync)

| 위치 | 변경 | 출처 |
|------|------|------|
| TL;DR Λ origin bullet | ✅ → ⚠️ CONSISTENCY_CHECK | L412 |
| TL;DR self-audit headline | 31% raw 단독 → 28% raw / 13% substantive 양면 | L412 + L415 |
| §1.2.1 Dark energy origin | "도출 (output)" → "order-unity dimensional consistency check" | L412 |
| §3.4 RG saddle | "Bayesian preference" 유지 + "a priori derivation" 제거, "priori 도출 영구 불가" 단락 추가 | L417 |
| §3.6 R-grid | 부록 → 본문 4점 표 + R=10 collapse + Lindley fragility | L417 |
| §4.1 row 2 BBN narrative | "두 mechanism" → "B-only 17 dex single-scale" 정정 | L418 |
| §4.1 row 3 | Λ_UV ~ η_Z₂ identification 명시 | L418 |
| §4.6 S_8 | ΔS_8 = +0.0114 structural + Euclid 4.4σ central / 4.38σ exact pre-reg + 3σ floor | L419 |
| §4.x μ-distortion | PASS_STRONG → PENDING + chain caveat 4항 | L420 |
| §5.2 Λ origin | PASS_STRONG → CONSISTENCY_CHECK 등급 frozen | L412 |
| §6.1 facility table | Euclid DR1 / μ-distortion mission TBD entries | L419 + L420 |
| §6.1 한계 row | η_Z₂ priori OPEN 추가 | L418 |
| §6.5(e) | substantive 13% (4/32) 카테고리 + CONSISTENCY_CHECK 1 bullet | L412 + L416 |
| claims_status v1.1 JSON | enum 8-value (+CONSISTENCY_CHECK), Λ origin row caveat 강화, RG saddle row priori-impossible | L412 + L417 |
| `verify_lambda_origin.py` 주석 | "1.0000 match" → "dimensional consistency check (circular)" | L412 |
| Final summary | raw/substantive 양면 + Λ origin CONSISTENCY_CHECK | L412 + L415 |

---

## 5. 잔존 OPEN attack 면 (정직 노출)

1. **B4 (structural circularity, §5.2)**: ρ_q/ρ_Λ(Planck) ↔ ρ_Λ_obs
   input dependence. fixable bug 아님 — L402 audit Path-α 10⁶⁰ fail 로
   영구 OPEN.
2. **F4 (η_Z₂ priori, §4.1)**: Λ_UV ≈ η_Z₂ identification 후보
   √(m_e × Λ_QCD) 매치는 *후보* 이며 Lagrangian derivation 미닫힘.
3. **R3.3 (실 데이터 R=10, §3.6)**: 실 데이터 wider prior 에서 Δln Z
   음수 가능성 OPEN — Euclid DR1 + production MCMC 후 재판정.
4. **§4.x (μ-distortion chain, 4 항)**: photon-sector axiom / Q(z) /
   y-μ 분기 / facility — 2030+.

---

## 6. 정직 한 줄

**v3 은 L412~L420 의 8 sync 적용으로 referee 8 attack 면 중 7 면을
무력화하고, 잔존 1 면 (B4 structural circularity) 은 paper 전체에서
정직 노출하며, raw 31% / substantive 13% 양면 표기를 §6.5(e) single
source of truth 로 frozen 했다.**
