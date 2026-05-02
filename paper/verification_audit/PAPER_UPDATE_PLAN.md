# paper/base.md 업데이트 PLAN (R8 종합 기반)

**작성일**: 2026-05-01
**근거**: R1–R7 audit + R8 synthesis (32 claim, PASS_STRONG 10 / PASS_TRIVIAL 2 / PASS_BY_INHERITANCE 4 / PARTIAL 8 / NOT_INHERITED 8 / FAIL 0)
**원칙**: cherry-pick 금지. PASS_STRONG 만 강조하고 NOT_INHERITED 숨기는 것 금지. 모든 caveat 명시.

---

## 0. 전체 방향

- **§14 (자가검증) 격하**: "32/32 자동 PASS" 식 narrative 폐기 → "PASS_STRONG 10 + 자동상속 6 + 결손 16" 으로 정직 재기술.
- **§6.1 (한계 표) 신설/확장**: NOT_INHERITED 8 + PARTIAL 8 = 16 항목 한계 행 추가.
- **§4.7 (관측 표) 분리**: CMB primary peak vs θ_* shift 분리.
- **§2.5 (5번째 foundation gate)**: GFT 미채택의 *연쇄 결과* 를 명시 (claim 2/9/25/26/27/28 모두 NOT_INHERITED 의 root cause).

---

## 1. PASS_STRONG (10) — 본문 강조 또는 추가

### 1.1 §4 "Lagrangian → Newton" 강조 (claim 4)
- **위치**: §4.3–4.4
- **수정**: ξ=2√(πG)/c² 매칭 사슬을 *Lagrangian-level 자기완결* 로 명시. "paper postulate set 외부 가정 없이 ∇²Φ=4πGρ 가 직접 도출" 한 문장 추가.

### 1.2 §3 "n₀μ = ρ_Planck/(4π) 는 산술 항등식" (claim 29)
- **위치**: §3.4 (Three-regime σ₀(env) 직후 또는 derived 표)
- **수정**: "n₀·μ = 4πG/σ₀² = 1/(4πG·t_P²) = ρ_Planck/(4π) — *예측이 아니라 σ₀=4πG·t_P 의 산술 따름결과*" 명시. 정직성 확보.

### 1.3 §3 "v(r) = g(r)·t_P" 구조 도출 (claim 31)
- **위치**: §3 inflow 해석 박스
- **수정**: 지구 표면 v=5.289×10⁻⁴³ m/s 수치 명시 + 도출 사슬 (σ₀ flux → ∇·v) 한 줄.

### 1.4 §4 "ξ 표기 명시" (claim 32)
- **위치**: §4.3
- **수정**: ξ=2√(πG)/c²=3.222×10⁻²² SI 명시. 03_background_derivation.md §3.1 와 등가성 한 줄.

### 1.5 §2.4 pillar 3 (Holographic) 강조 (claim 15, 16)
- **위치**: §2.4 foundation 3
- **수정**: "S_BH=k_B A/(4 l_P²) 와 Bekenstein bound 2π k_B E R/(ℏc) 의 Schwarzschild saturation 이 σ₀=4πG·t_P 에서 직접 따라옴" 명시.

### 1.6 §2.4 pillar 1 (Schwinger-Keldysh) 강조 (claim 14)
- **위치**: §2.4 foundation 1
- **수정**: "SK doubled-contour + retarded G_R 해석성 → CPTP map → H-theorem (min ΔS ≥ 0)" 한 줄 추가.

### 1.7 §4.7 dark-only EP 명시 (claim 11)
- **위치**: §4.7 (PPN/EP 표)
- **수정**: "β_b ≡ 0 (dark-only embedding) ⇒ η = 2β_b² = 0 *구조적*" 명시. MICROSCOPE 10⁻¹⁵ 와 비교.

### 1.8 §4.7 Cassini 박스 reword (claim 18) — **CRITICAL**
- **위치**: §4.7 PPN γ 박스
- **수정 전**: "T_photon=0 → γ=1 EXACT"
- **수정 후**: "T_photon=0 은 photon 직접 결합 차단; |γ−1| 의 정량 한계는 **β_eff = Λ_UV/M_Pl ≈ 7.4×10⁻²¹** 작음에서 옴 (∼2β_eff² ≈ 1.1×10⁻⁴⁰ ≪ 2.3×10⁻⁵)"

### 1.9 §4.7 BBN 두 보호 메커니즘 (claim 20)
- **위치**: §4.7 BBN 행
- **수정**: "η_Z₂ ≈ 10 MeV ≫ T_BBN ≈ 0.1 MeV (factor 100) + β_eff² ≈ 5.5×10⁻⁴¹ → ΔN_eff ≈ 10⁻⁴⁶ ≪ 0.17. 두 보호 모두 axiom-2 pillar-4 에서 옴."

---

## 2. PASS_TRIVIAL (2) — 정직 명시

### 2.1 GW170817 (claim 19)
- **위치**: §4.7 GW 행
- **수정**: "conformal-only Lagrangian 형태 선택 ⇒ G_{4,X}=0 ⇒ c_T²−1=0. *유도가 아닌 라그랑지안 형태 선택의 귀결*. C11D disformal 후보 부활 시 KILL."

### 2.2 LLR Ġ/G (claim 22)
- **위치**: §4.7 LLR 행
- **수정**: "G axiom-derived constant ⇒ Ġ=0 *by 정의*. 비자명 보정 β_eff²·H₀ ≈ 4×10⁻⁵¹/yr. *axiom 선택의 동어반복*."

---

## 3. PASS_BY_INHERITANCE (4) — "standard QFT inheritance" 정직 명시

### 3.1 §14.3 (또는 §3 표) 분리 표기
- **위치**: §14.3 axiom 정합성 표
- **수정**: A10 (Lorentz/KMS), A12 (uncertainty), A13 (CPT), claim 24 (wavefunction) 모두 **"standard QFT inheritance — paper framework 의 SQMH-shaped win 아님"** 단주 추가.
- **이유**: paper L⁰ = local·Lorentz scalar·Hermitian 만으로 자동 상속. 이를 "SQMH 검증 통과" 로 광고하면 over-claim.

---

## 4. PARTIAL (8) — caveat 명시 위치

### 4.1 claim 1 (1/r² 중력 함수형) — §3
- **위치**: §3 derived 1
- **caveat 추가**: "mass-action `σ·n·ρ_m` 함수형은 a1 (흡수) 단독으로 결정되지 않으며, root §I 가정 2 (bilinear in n, ρ_m) 가 implicit. paper postulate 로 명시 등재 또는 SK vertex 로부터 도출 필요."

### 4.2 claim 3 (4원리 수렴) — §2.4
- **caveat 추가**: "de Sitter symmetry origin 이 a4 (emergent metric) OPEN 에 묶여 있음. a4 5번째 축 미확정 시 weak-PASS."

### 4.3 claim 5 (Padmanabhan) — §6.1 한계 표
- **수정**: "Padmanabhan emergent gravity 와의 구조적 동형은 *motivational analogy* 수준. paper 본문 인용 0회. N_sur−N_bulk 단계별 도출 부재."

### 4.4 claim 7 (Causal Set) — §2.5
- **caveat 추가**: "Causet meso 는 5번째 축 *후보* 로 거론. axiom 1–6 → causal-set growth → δΛ∼1/√N 의 단계별 도출은 미완. derived 2 (n_∞) 의 5.2 circularity 와 결합."

### 4.5 claim 17 (Conservation/ρ_q=ρ_Λ_obs) — §5.2
- **위치**: 이미 §5.2 가 circularity 명시 — **유지**. 단 §14.3 표에서 A17 옆에 "(5.2 circularity: n_∞ ← ρ_Λ_obs input, derivation 아닌 consistency)" 한 줄.

### 4.6 claim 21 (CMB θ_*) — §4.7 — **CRITICAL**
- **위치**: §4.7 CMB 행
- **수정**: 한 행을 두 행으로 분리:
  - "CMB primary peak 진폭/위치: PASS (radiation era T^α_α≈0)"
  - "CMB θ_* 정밀값: matter era φ 진화로 δr_d/r_d ≈ 0.7% shift (Planck σ 의 23×). Phase-2 BAO 와 동일 채널."
- **§14.4 #20 수정**: "5개 자동 통과" → "4개 자동 (Cassini, GW170817, BBN, LLR) + 1개 부분 (CMB θ_* shift)"

### 4.7 claim 23 (Q-parameter) — §14.5 또는 quantum 섹션
- **caveat 추가**: "Q 정의 비유일 (5 dimensionally consistent 후보, Q_macro 38 자릿수 변동). '0 free param' 은 *정의 선택 후*에만 성립. SQMH 가 정의를 a priori 고정하지 않음."

### 4.8 claim 30 (w_eff(z)) — §5.4 (이미 OPEN gate 명시)
- **위치**: §5.4 V(n,t)-확장
- **수정**: 이미 "derivation gate OPEN" 명시 — **유지**. §14.6 표에서 V(n,t) toy 의 진폭 factor ~3 부족 명시.

---

## 5. NOT_INHERITED (8) — §6.1 한계 표 신설/확장

**§6.1 신설 또는 기존 한계 섹션 확장: "paper framework 가 root /base.md §V–§14 에서 상속받지 않은 8 항목"**

| # | 항목 | root 위치 | NOT_INHERITED 사유 | 해결 경로 |
|---|------|----------|---------------------|-----------|
| 2 | 특이점 해소 (Planck 밀도 포화) | §III.6 | discreteness postulate 부재 | a4 5번째 축 (Causet/GFT) 확정 필요 |
| 6 | Volovik 2-fluid analogue | §V.2 | "superfluid/two-fluid" 0 hits | a4 OPEN 또는 trivial 동형 명시 |
| 8 | Jacobson δQ=TdS | §V.4 | KMS ≠ Clausius. derived 1 경로 다름 | 별도 entropic derivation 추가 또는 인용 삭제 |
| 9 | GFT BEC 해밀토니안 | §V.5, §VI | "GFT/Oriti" 0 hits. Z₂ ≠ U(1) | GFT 5번째 foundation 등재 |
| 25 | BEC coherence → 비국소성 | §14.5 | Z₂ 연속 phase 부재 | GFT foundation 추가 또는 §14.5 삭제 |
| 26 | DESI DR2 ξ_q joint fit | §10.5 | w_a 부호 불일치 + r_d 미요구 + ξ_q 미정의 | V(n,t) derivation gate 닫기 |
| 27 | 3자 정합성 (BBN/CMB/late DE) | §14.6 | #26 의존 + r_d 이동과 BBN/CMB consistency 텐션 | #26 해결 후 재평가 |
| 28 | GFT BEC 해밀토니안 정합 | §VI | paper 4 축에 GFT 부재 | GFT foundation 등재 |

**§6.1 추가 문구**:
> "위 8 항목은 root /base.md 가 §V (구조 일치), §VI (양자), §10.5 (DESI ξ_q joint), §14.6 (시뮬) 에서 도달한 결과지만, paper framework (axioms 1–6 + 4 micro pillars + Causet 5번째 축 후보) 안에서는 외부 입력 없이 도달할 수 없다. 8 항목 중 5건 (#9, #25, #26, #27, #28) 이 GFT/BEC 미상속에서 발생하며, 이는 a4 의 5번째 foundation 결정 (Causet vs GFT 등) 이 critical decision point 임을 보여준다."

---

## 6. §14 (자가검증) 전면 격하

### 6.1 §14 표제 수정
- **수정 전**: "32/32 자동 PASS"
- **수정 후**: "**PASS_STRONG 10 (31.3%) + PASS_TRIVIAL/INHERITANCE 6 (18.8%) + PARTIAL 8 (25.0%) + NOT_INHERITED 8 (25.0%) + FAIL 0**"

### 6.2 §14.1 (수학 도출 4)
- 4/4 → "1 PASS_STRONG (Newton 극한) + 2 PARTIAL (1/r² 함수형, 4원리 수렴) + 1 NOT_INHERITED (특이점 해소)"

### 6.3 §14.2 (구조 일치 5)
- 5/5 → "0 PASS + 2 PARTIAL (Padmanabhan, Causet) + 3 NOT_INHERITED (Volovik, Jacobson, GFT)"

### 6.4 §14.3 (공리 8)
- 8/8 → "4 PASS_STRONG (A11/14/15/16) + 3 PASS_BY_INHERITANCE (A10/12/13) + 1 PARTIAL (A17 circularity)"

### 6.5 §14.4 (관측 5)
- 5/5 → "2 PASS_STRONG (Cassini β_eff, BBN 두 보호) + 2 PASS_TRIVIAL (GW170817, LLR) + 1 PARTIAL (CMB θ_* δr_d ≈ 0.7%)"

### 6.6 §14.5 (양자 3)
- 3/3 → "0 PASS_STRONG + 1 PARTIAL (Q-param 정의 비유일) + 1 PASS_BY_INHERITANCE (wavefunction) + 1 NOT_INHERITED (BEC nonlocality)"

### 6.7 §14.6 (시뮬 3)
- 3/3 → "**0 PASS — 3 NOT_INHERITED 모두**. ξ_q joint fit·r_d=149.8·GFT 해밀토니안 모두 paper framework 외부."

### 6.8 §14.7 (추가 4)
- 4/4 → "3 PASS_STRONG (n₀μ 곱, v=g·t_P, ξ 대수) + 1 PARTIAL (w_eff V(n,t) gate OPEN). n₀μ 개별값은 framework 가 인정한 대로 SI 자기무모순 FAIL."

---

## 7. 우선순위 및 작업 순서

### Phase A — CRITICAL (over-claim 즉시 수정)
1. §4.7 Cassini 박스 reword (PASS_STRONG 의 mechanism 정확히 명시)
2. §4.7 CMB 행 분리 (primary peak / θ_* shift)
3. §14.4 "5/5 자동" → "2 nontrivial + 2 trivial + 1 partial"
4. §14 표제 전면 격하 (32/32 → 10 PASS_STRONG + …)

### Phase B — 본문 강조/추가 (PASS_STRONG)
5. §3 n₀μ 산술 항등식 명시 (claim 29)
6. §3 v=g·t_P 도출 사슬 (claim 31)
7. §4 ξ 표기 명시 (claim 32)
8. §2.4 pillar 1/3 강조 (claim 14, 15, 16)
9. §4.7 dark-only EP 강조 (claim 11)

### Phase C — caveat 명시 (PARTIAL)
10. §3 derived 1 mass-action 함수형 caveat
11. §2.4–2.5 4원리 수렴 + Causet 후보 caveat
12. §14.5 Q-param 정의 비유일 caveat

### Phase D — 한계 표 (NOT_INHERITED)
13. §6.1 한계 표 신설/확장 (8 항목)
14. §6.1 GFT 미채택 연쇄 결과 명시

### Phase E — 정직 표기 (TRIVIAL/INHERITANCE)
15. §14.3 / §14.4 "standard QFT inheritance" / "Lagrangian 형태 선택의 귀결" 단주

---

## 8. 학계 reviewer 대비 — 예상 비판과 대응

| reviewer 비판 | 대응 |
|---------------|------|
| "32/32 PASS 과주장" | Phase A 4개 + §14 격하 (Phase A.4) |
| "Padmanabhan/Volovik/Jacobson/GFT 인용 0회인데 §V 동형 주장?" | Phase D §6.1 한계 표 + §V 본문에 "motivational analogy" 명기 |
| "5/5 관측 자동 통과는 over-claim" | Phase A.1–A.3 |
| "BEC nonlocality 는 paper Z₂ 와 모순" | Phase D claim 25 한계 표 + §14.5 삭제 또는 GFT foundation 등재 |
| "DESI ξ_q joint fit 결과를 paper 결과로 인용 못 한다" | Phase D claim 26/27/28 한계 표 + §10.5 ↔ §14.6 separation |
| "n₀μ '예측' 인가 항등식인가" | Phase B.5 산술 항등식 명시 |
| "Cassini γ=1 EXACT 단독 mechanism 주장" | Phase A.1 Cassini 박스 reword |
| "Q-param 0 free param" | Phase C.12 Q 정의 비유일 caveat |

---

## 9. 정직 한 줄 (PLAN)

> paper/base.md 는 (a) Phase A 의 4개 over-claim 을 즉시 격하하고, (b) Phase B 의 PASS_STRONG 10 을 본문에 정직 강조 (특히 σ₀ holographic 항등식 6건의 "예측이 아닌 따름결과" 표기), (c) Phase D §6.1 한계 표에 NOT_INHERITED 8 항목을 GFT 미채택 연쇄 결과로 묶어 명시, (d) §14 자가검증 표제를 "32/32" 에서 "PASS_STRONG 10 + 자동상속 6 + 결손 16" 로 재기술해야 학계 reviewer 의 가장 냉철한 시선에서 살아남는다.
