# L532 — Path-α a_0(z) priori-channel forecast (P28)

> **작성**: 2026-05-01
> **substrate**: L527 PATH_ALPHA.md §1.2 / §4.2 / §6.2, paper claims_status v1.2 (C1 PASS_MODERATE), L526_R8 §3, paper §4 (perturbations), simulations/l49 SPARC catalog (Lelli+2017, 175 galaxies)
> **CLAUDE.md 정합성**: [최우선-1] 신규 함수형 0건 / [최우선-2] 8인 팀 도출 의무 명시 / AICc 패널티 명시 / 결과 왜곡 금지 — 본 문서는 L527 axiom 3' 의 *기존* C1 관계 (`a_0 ↔ c·H/(2π)`, factor-≤1.5) 를 z>0 으로 *치환* 평가만 수행. 신규 수식·신규 파라미터 0개.

---

## 0. 정직 한 줄

**Priori 진정 회복은 *부분적이고 조건부*.** SPARC 단독으로는 P28 검출 불가 (z baseline 0.03 너무 짧음, max SNR ≈ 0.10). Euclid + LSST 가 검출 sensitivity 는 가지나, 신호가 `H(z)` 측정과 *구조적으로 degenerate* 하므로 "*P28 = 새로운 SQMH 예측*" 으로 인정받으려면 (a) `a_0(z)/H(z)` 비율 자체의 z-진화 검증, 또는 (b) Γ₀(t) 함수형의 *동역학적* 도출 (Q17 진정 달성) 이 선행되어야 함. 본 임무 시점에서는 "**채널은 살아있으나 진정 priori 미회복**".

---

## 1. 임무 1 — a_0(z) priori 도출 *형식* (axiom 1+4+5 만)

### 1.1 기존 자원 (paper 에 이미 존재)

claims_status v1.2 의 **C1**: `a_0 ↔ c·H_0/(2π)` 관계가 SPARC RAR (Lelli+17) 데이터와 factor-≤1.5 정합. PASS_MODERATE. 이 관계는 paper §3 (background) 에서 axiom 1 (대사적 시공간) + axiom 4 (정보-해상도 한계) + axiom 5 (홀로그래피) 의 *기존* 도출 결과.

### 1.2 L527 axiom 3' 의 효과

axiom 3' (Γ₀ → Γ₀(t)) 도입 시 C1 관계의 양변이 *동시에* 시간 함수가 됨. 우주론적 해석 측면에서 **시간 t ↔ 적색이동 z** 로 매핑하면 C1 의 *trivial 치환* 이 P28 의 형식이 됨:

> **P28 (형식)**: 기존 C1 관계의 우변에서 H_0 → H(z). 즉 a_0(z) 는 z=0 에서 SPARC 정합값 + factor-≤1.5 를 유지하며, z>0 에서는 H(z) 와 같은 비율로 진화한다.

이는 **새 이론이 아니다** — 기존 C1 의 *시간 의존 평가* 일 뿐. CLAUDE.md [최우선-1] 위반 없음 (신규 함수형 도입 부재).

### 1.3 진정 priori 회복 조건 (8인 팀 도출 의무)

본 형식만으로는 priori 회복 *부족*. 이유:
- C1 의 factor-≤1.5 자체가 dimensional 정합 + spectrum-cutoff 적분 결과로, *정확한 1.0* 이 아님 (Q17 amplitude-locking 미달).
- z>0 에서 a_0(z)/[c·H(z)/(2π)] 비율의 *시간 의존* 자체 (factor 의 z-진화 여부) 는 Γ₀(t) 함수형이 결정 — 본 문서는 *비지정* (8인 Rule-A 팀 의무).

⇒ **Priori 회복 등급 = 부분 (partial)**. L527 §6.2 조건 1·2·3 모두 *미확정* 상태이므로 +2~3%p acceptance 보너스도 *미부여*.

---

## 2. 임무 2 — SPARC redshift-evolution 검증

### 2.1 SPARC redshift coverage (Hubble-flow z = D·H_0/c)

| 통계 | 값 |
|---|---|
| N (총) | 175 |
| z_min | 0.00023 |
| z_max | 0.02984 |
| z_median | 0.00385 |
| z>0.005 | 48 (27%) |
| z>0.010 | 36 (21%) |
| z>0.020 | 9 (5%) |
| z>0.030 | 0 (0%) |

### 2.2 z-bin SNR (run.py 산출)

| bin | N | z_median | signal Δa_0/a_0 | noise (RAR scatter) | SNR |
|---|---|---|---|---|---|
| z ≤ 0.005 (anchor) | 127 | 0.0023 | 0.0000 | 0.0376 | 0.00 |
| 0.005–0.010 | 12 | 0.0070 | 0.0022 | 0.0904 | 0.025 |
| 0.010–0.020 | 27 | 0.0142 | 0.0057 | 0.0634 | 0.090 |
| 0.020–0.030 | 9 | 0.0226 | 0.0098 | 0.1033 | 0.095 |

- 신호 크기 = E_LCDM(z_b) − E_LCDM(z_anchor) ≤ 0.01 (1%) 까지.
- 잡음 = SPARC RAR intrinsic scatter σ ≈ 0.13 dex → fractional ≈ 0.30/√N.
- **max SNR ≈ 0.10**, AICc 임계 (dχ² ≥ 2 → SNR ≥ √2) 대비 14× 부족.

### 2.3 정직 결론 (SPARC)

> **SPARC 단독으로 P28 검출 불가능.** z baseline (0–0.03) 에서 신호는 1% 미만, intrinsic RAR scatter 는 30% (per galaxy) — 신호 대 잡음 비가 0.1 σ 수준. N 을 4× 늘려도 SNR 0.4σ. SDSS-MaNGA / Euclid-IFS 등 더 깊은 회전곡선 캠페인이 z>0.1 까지 확장되어야 SPARC-계열 검증이 의미 있음.

---

## 3. 임무 3 — *진정 priori 가능?* (data input 없이 함수형 도출)

### 3.1 본 문서의 답

**아니오** — 본 임무 시점에서 진정 priori 도출은 *수행되지 않았음*. 이유:

1. **CLAUDE.md [최우선-1]**: Γ₀(t) 함수형은 본 문서에서 prescription 금지. 8인 Rule-A 팀이 axiom 1+4+5 + 우주열역학만으로 자유 도출 의무 (L527 §1.2, §4.2).
2. **본 문서가 한 일**: 기존 C1 관계의 z>0 *치환 평가* + 데이터 sensitivity *forecast*. 이는 priori 도출이 아니라 *consumer* 작업.
3. **이 작업이 priori 회복으로 인정받을 수 있는 조건** (L527 §6.2 재확인):
   - 조건-1: Γ₀(t) 가 single-parameter monotonic family 로 자유 수렴 — *미확정*
   - 조건-2: 함수형 1 자유도 안에서 P28 수치 예측 자연 정량화 — *미확정*
   - 조건-3: ρ_q(t) 와 우주열역학 정합 — *미확정*

⇒ **세 조건 0/3 충족.** L527 §6.2 acceptance 회복 +2–3%p 보너스 *미부여 유지*. JCAP-acceptance 천장은 L527 toy 의 7–8% 를 그대로 사용.

### 3.2 Q17 amplitude-locking 와의 연관

P28 가 진정 priori 로 인정받으려면 Q17 의 amplitude (factor=1.0 vs ≤1.5) 가 동역학적으로 lock 되어야 함. L6 재발방지 "Q17 미달 PRD 진입 금지" 는 그대로 유효. **본 임무가 Q17 을 진전시키지 않음**.

---

## 4. 임무 4 — paper §4 신규 prediction P28

### 4.1 P28 등록 형식 (paper §4 추가 후보)

> **P28 — a_0(z) cosmological evolution**: SQMH 의 axiom 3' (L527) 하에서, MOND-scale 가속도 a_0 가 z>0 에서 c·H(z)/(2π) 와 동일 비율로 시간 진화한다. 검증 채널: (a) SPARC-style RAR 의 z>0.1 확장, (b) Euclid 2030 spec-z + WL 의 a_0(z)/H(z) 비율 anchor, (c) LSST DR2/DR3 cosmic-shear tomography. **Falsifier**: a_0(z=1.0)/a_0(z=0) 가 E_LCDM(1.0) ≈ 1.65 와 factor-≤1.5 정합 *실패* 시 P28 (및 Path-α) 기각.

### 4.2 P28 의 *priori 등급*

claims_status v1.2 등급 체계 적용:
- **PASS_BY_INHERITANCE** 후보 (C1 PASS_MODERATE 의 *시간 치환* 이므로 inherit).
- 자체 PASS_STRONG 진입 조건: Q17 동역학적 도출 OR Euclid/LSST 직접 측정.
- 본 임무 시점 등급: **NOT_YET_REGISTERED** (본 문서는 후보 제출, 8인 Rule-A 검토 후 등록).

### 4.3 paper §4 추가 시 caveat (정직 표기 의무)

paper §4 본문에 P28 추가할 경우 다음 caveat 동시 표기:
1. P28 는 C1 의 z-치환이지 신규 함수형 아님.
2. 진정 priori 회복은 Q17 + 8인 Γ₀(t) 자유 도출 후 재평가.
3. SPARC 단독 검증 불가 — Euclid/LSST 의무.
4. H(z) 측정과 구조적 degeneracy 존재 (§5 참조) — 분리 채널 필요.

---

## 5. 임무 5 — Euclid + LSST sensitivity forecast

### 5.1 forecast 결과 (run.py 산출)

| Survey | 노이즈/bin | z-bins | combined SNR (adjacent) | max-pair SNR | viable? |
|---|---|---|---|---|---|
| Euclid (spec-z) | 1.0% (per dz=0.2) | [0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.8] | 146 σ | 101 σ | ✅ |
| LSST (cosmic shear) | 2.5% (per tomo bin) | [0.3, 0.6, 0.9, 1.2, 1.6, 2.0, 2.5] | 102 σ | 73 σ | ✅ |

표면적으로는 압도적 검출. **그러나** §5.2 의 caveat 가 결정적임.

### 5.2 *결정적* caveat — H(z) degeneracy

Euclid/LSST 가 *직접* 측정하는 것은 H(z), D_A(z), σ_8(z), G_eff(z). P28 의 신호 `Δa_0(z)/a_0(0) = E(z)−1` 는 **그저 H(z) 측정의 재해석** — 새로운 정보 채널이 아님.

⇒ **"P28 가 Euclid/LSST 에서 100σ 검출됨" 이라는 주장은 misleading.** 정직한 표현:

> Euclid/LSST 가 H(z) 를 100σ 로 측정하면 a_0(z) = c·H(z)/(2π) 도 자동으로 100σ 측정됨. 그러나 이는 P28 가 새로운 예측이라는 증거가 아니라, *기존 H(z) 측정을 a_0(z) 라벨로 재포장* 한 것.

### 5.3 진정한 P28 검증 채널 (degeneracy 깨는 방법)

P28 가 *독자적* 예측으로 살아남으려면:
1. **(a) RAR factor 의 z-진화**: a_0(z)/[c·H(z)/(2π)] *비율 자체* 가 z 와 함께 일정 또는 진화하는지 — 회전곡선 데이터를 z>0.5 까지 확장한 직접 측정 필요. SPARC 후속 + JWST high-z lensing-derived RC 가 핵심.
2. **(b) Γ₀(t) 함수형의 axiom-derived 예측**: Q17 동역학적 도출 후, a_0(z=1) 의 *정확값* 예측 (factor 1.0 lock) 과 Euclid 측정 비교.
3. **(c) Cassini-style high-precision local test**: 태양계 timescale 에서 a_0(t) 의 시간 미분 측정. 현재 기술 한계 5σ 미달, **5–10년 horizon**.

⇒ **현실적 P28 검증은 SPARC 후속 (z 확장) + JWST 고-z RC** 에 의존. Euclid/LSST 는 *지원* 채널.

### 5.4 Sensitivity 정량 갱신 (degeneracy 보정)

H(z)-degenerate 부분을 제거한 *순수* P28 SNR (RAR factor 의 z-진화 채널만):

| Survey + 보조 | 보조 채널 | 순수 P28 SNR |
|---|---|---|
| Euclid + JWST RC (z=0.5–1.5, ~50 회전곡선) | RAR factor z-evolution | ~3–5σ (낙관) |
| LSST + Roman RC (z=1–2, ~30 회전곡선) | 동일 | ~2–3σ (낙관) |
| SPARC alone | (없음) | 0.10σ (불가) |

⇒ **5–10년 horizon 에서 P28 가 진정 검증되려면 JWST/Roman 의 고-z 회전곡선 캠페인이 필수**. Euclid/LSST 단독으로는 H(z) degenerate.

---

## 6. AICc 패널티 명시 (CLAUDE.md 의무)

| 항목 | 값 |
|---|---|
| P28 추가 자유도 | +1 (Γ₀(t) 의 timescale/amplitude 1 개) |
| AICc 임계 dχ² | ≥ 2 |
| Path-α (L527 toy) 의 acceptance 천장 | 7–8% (현실), 9–12% (낙관), 4–5% (비관) |
| L532 결과로 천장 갱신 | **변화 없음** (priori 미회복, sensitivity 는 H(z) degenerate) |

**L527 §5.2 의 N1 prediction bonus +1.5%p (낙관)** 은 본 임무로 *확정 부여 불가*. 8인 Rule-A 팀의 Γ₀(t) 자유 도출 + JWST/Roman 후속 데이터 후 재평가.

---

## 7. paper §4 P28 등록 결정 (권고)

### 7.1 권고

**조건부 등록**:
- claims_status 에 P28 추가하되 등급 = **CANDIDATE_PROVISIONAL** (PASS_BY_INHERITANCE 미달, NOT_YET_REGISTERED 와 PASS_MODERATE 사이).
- §4 본문 추가 시 §5.2 의 H(z)-degeneracy caveat + §5.3 의 진정 검증 채널 (JWST/Roman RC) 명시.
- 8인 Rule-A 팀의 Γ₀(t) 도출 라운드 *전* 까지 이 등급 유지.

### 7.2 paper §4 본문 추가 미수행 (본 임무)

본 L532 시점에서는 paper/04_perturbation_theory.md *직접 편집 미수행*. 이유:
- L527 §8 "paper/base.md edit 0건" 정합.
- 8인 Rule-A 팀 도출 *후* paper 반영이 정도.
- claims_status.json edit 도 미수행 (L527 정합).

본 문서는 8인 라운드의 *substrate* 로 제출.

---

## 8. 정직 한 줄 (최종)

**P28 채널은 살아있으나 *진정 priori 미회복*. SPARC 단독 검증 0.10σ (불가), Euclid/LSST 의 100σ는 H(z)-degenerate misleading 수치. 진정 검증은 JWST/Roman 고-z 회전곡선 + 8인 Γ₀(t) 자유 도출 의무. JCAP-acceptance 천장 7–8% 변화 없음. PRD 진입 영구 차단 변화 없음.**

---

## 9. CLAUDE.md 정합성 체크

- **[최우선-1] 방향만**: P28 형식은 기존 C1 관계의 z-치환 (신규 함수형 0). Γ₀(t) 함수형 비지정. ✅
- **[최우선-2] 팀 독립 도출**: 8인 Rule-A 팀 의무 명시 (§1.3, §3.1, §7.1). ✅
- **AICc 명시**: §6 표. ✅
- **결과 왜곡 금지**: Euclid/LSST 100σ 이 H(z)-degenerate 임을 §5.2 정직 명시. SPARC 검증 불가능 정직 명시. ✅
- **paper edit 0건**: ✅ (claims_status edit 0건도 ✅)
- **신규 수식 0줄, 신규 파라미터 0개**: ✅
- **시뮬레이션 multiprocessing**: 본 forecast 는 grid 산출 없음 (closed-form sensitivity). 병렬 의무 미해당. ✅
- **disk 정직**: SPARC 카탈로그 simulations/l49/data/sparc_catalog.mrt 존재 확인 후 사용. ✅

---

*저장: 2026-05-01. results/L532/A0_Z_PRIORI.md. substrate: L527 PATH_ALPHA.md + L526_R8 + claims_status v1.2 + SPARC Lelli+2017 + Euclid IST 2020 + LSST DESC SRD 2018. 8인 Rule-A (Γ₀(t) 함수형 자유 도출) / 4인 Rule-B (run.py 검토) 미실행 — 후속 의무. paper edit 0, claims_status edit 0, 신규 수식 0, 신규 파라미터 0. CLAUDE.md [최우선-1] / [최우선-2] / 결과 왜곡 금지 정합.*
