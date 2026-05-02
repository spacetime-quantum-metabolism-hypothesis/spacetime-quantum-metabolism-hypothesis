# R4 — 관측 검증 audit (관측가, 매우 냉철)

**대상**: root `base.md` §14.4 의 *5개 관측 자동 PASS* 주장
**기준 framework**: `paper/base.md` (axiom 1–6, 4 micro pillars, σ₀ holographic, Λ_UV ≈ 18 MeV, Z₂ SSB η ≲ 10 MeV)
**스크립트**: `paper/verification_audit/R4_observations.py`
**산출 JSON**: `paper/verification_audit/R4_observations.json`

## 핵심 수치 (paper/base.md framework)

| 양 | 값 | 출처 |
|---|---|---|
| σ₀ = 4πG·t_P | 4.522 × 10⁻⁵³ m³ kg⁻¹ s⁻¹ | derived 1 / pillar 3 |
| Λ_UV | 18 MeV | axiom-2 micro pillar 4 (definitional) |
| η_Z₂ | ≤ 10 MeV | pillar 4 (Z₂ SSB scale) |
| M_Pl (reduced) | 2.435 × 10¹⁸ GeV | – |
| **β_eff = Λ_UV / M_Pl** | **7.39 × 10⁻²¹** | dimensional ratio (5th-force coupling) |

## 5개 관측 — 항목별 판정

| # | 관측 | 제약 | paper/base 주장 | 정량 예측 | 판정 |
|---|---|---|---|---|---|
| 1 | Cassini PPN γ | \|γ−1\| < 2.3×10⁻⁵ | γ = 1 EXACT (Tᵅᵅ=0 photon) | \|γ−1\| ~ 2β_eff² = **1.1×10⁻⁴⁰** | **PASS_NONTRIVIAL** |
| 2 | GW170817 c_GW | \|Δc/c\| < 7×10⁻¹⁶ | c_GW = c (동일 SQ medium) | tree=0 (no disformal); loop ~5.5×10⁻⁴¹ | **PASS_TRIVIAL** |
| 3 | BBN ΔN_eff | < 0.17 | radiation 시대 GR | ΔN_eff ~ β_eff²·(ρ_b/ρ_r) ≈ **1.3×10⁻⁴⁶** | **PASS_NONTRIVIAL** |
| 4 | CMB θ_* | σ/θ ≈ 3×10⁻⁴ | "Planck 일관" | radiation era OK; **matter era δr_d/r_d ~ 0.7%** | **PARTIAL** |
| 5 | LLR Ġ/G | < 10⁻¹³/yr | G 고정 (axiom) | β_eff²·H₀ ≈ **3.8×10⁻⁵¹/yr** | **PASS_TRIVIAL** |

## 항목별 냉철 분석

### 1. Cassini — PASS_NONTRIVIAL
- paper §4.7 주장 *"γ = 1 정확히 (T_photon = 0)"* 은 **필요조건이지 충분조건이 아니다**.
- 광자 자체에 직접 5번째 힘이 안 걸리는 것은 맞다 (Tᵅᵅ=0).
- 그러나 **태양 내부 물질**의 Tᵅᵅ ≈ ρ c² ≠ 0 → φ profile 생성 → 광자 측지선 휨.
- 진정한 PASS 메커니즘은 **β_eff = Λ_UV/M_Pl ≈ 7.4×10⁻²¹** 이 매우 작다는 사실. 이 작음은 axiom-2 pillar-4 (Λ_UV ~ 18 MeV) + Planck 위계에서 자동으로 따라온다.
- 학계 비판 가능: "T_photon=0 만으로 γ=1 EXACT 라는 §4.7 문장은 over-claim; 실제로는 5th-force suppression."
- 권고: §4.7 박스 문장 수정 — "T_photon=0 은 photon 직접 결합을 끄지만, γ=1 정확성은 Λ_UV/M_Pl 작음에서 옴".

### 2. GW170817 — PASS_TRIVIAL
- paper §4.1 라그랑지안은 **순수 conformal** (φ²R + ξφTᵅᵅ); disformal 항 g̃ = Ag + B∂φ∂φ 없음.
- → G_{4,X} = 0 → c_T² − 1 = 0 (tree level).
- 이는 **유도(derive)가 아니라 라그랑지안 형태 선택의 귀결**. PASS_TRIVIAL.
- ★ 위험: L4 R&D layer 에서 C11D (disformal) 후보 부활 시 GW170817 즉시 KILL. CLAUDE.md 의 "C11D disformal 통과" 메모는 PPN γ 한정이지 c_GW 가 아님 — `paper/base.md` 가 disformal 도입하면 이 PASS 가 깨진다.

### 3. BBN — PASS_NONTRIVIAL
- 두 개의 정량적 보호:
  - η_Z₂ = 10 MeV ≫ T_BBN ≈ 0.1 MeV (factor 100): Z₂ 가 BBN 훨씬 이전에 깨져서 vacuum 정적 → SQ 자체로는 추가 복사 자유도 없음.
  - β_eff² ≈ 5.5×10⁻⁴¹ × baryon-to-radiation 비 (5×10⁻⁷) → ΔN_eff ~ 10⁻⁴⁶ ≪ 0.17.
- 두 보호가 모두 axiom-2 pillar-4 (Λ_UV/η_Z₂) 에서 옴 → 진짜 비자명.

### 4. CMB θ_* — PARTIAL ⚠
- paper §4.7 *"CMB 1차 이방성 Planck 일치 (radiation era 불변)"* 은 **부분만 맞다**.
- radiation 시대 (z ≳ 3000) Tᵅᵅ ≈ 0 → φ 정지 → primary peak 진폭/위치 OK.
- 그러나 θ_* 는 **z=1100 → 0 적분량** (D_A) 이고 이 구간은 matter 시대 → φ 진화 → H(z) 수정 → θ_* 이동.
- 실제 BAO 피팅 (root base.md §11) δr_d/r_d ≈ 0.7% (149.8 Mpc vs 148.7 Mpc) — 이 자체가 CMB θ_* 에 동등한 shift.
- Planck σ(100 θ_*) = 0.030% 보다 **23× 큰** 이론 변화.
- 즉 §14.4 "CMB 자동 통과" 는 primary peak 형태 한정; θ_* 정밀값은 자동 PASS 아님.
- 권고: §4.7 표에 CMB 행을 "primary peak 진폭 OK, θ_* 는 Phase-2 BAO 적합 통해 0.7% shift" 로 분리.

### 5. LLR — PASS_TRIVIAL
- G 가 axiom-derived (derived 1) constant → Ġ = 0 by 정의.
- 비자명 보정은 β_eff²·H₀ ~ 4×10⁻⁵¹/yr ≪ 10⁻¹³/yr.
- "axiom 으로 결정" 자체는 검증이 아니라 정의이므로 TRIVIAL.

## 종합 (한 줄, 정직)

> **5/5 자동 PASS 라는 §14.4 주장은 over-claim. 실측은 2 PASS_NONTRIVIAL (Cassini, BBN — Λ_UV/M_Pl 작음에서 비자명 도출) + 2 PASS_TRIVIAL (GW170817, LLR — 라그랑지안/axiom 구조 선택의 귀결) + 1 PARTIAL (CMB θ_* 는 matter-era φ 진화로 0.7% shift 발생, Phase-2 BAO 와 동일 채널). §4.7 박스 문장은 "Tᵅᵅ=0 photon → γ=1 EXACT" 단독 메커니즘 주장이지만 실제 PASS 의 정량적 보호는 β_eff = Λ_UV/M_Pl ≈ 7.4×10⁻²¹ 작음에서 온다 — 문장 보강 필요.**

## 학계 reviewer 가 제기할 비판 (대비)

1. *"§4.7 의 γ=1 EXACT 는 photon 한정 효과; 태양 내부 물질이 φ 를 source 하면 light bending 보정이 있어야 한다."* → β_eff² 작음으로 답변 가능, but §4.7 문구 자체 수정 필수.
2. *"GW170817, LLR 'PASS' 는 라그랑지안/axiom 형태 선택의 동어반복(tautology)."* → 인정. "Lagrangian structurally forbids deviation" 으로 표현 정직화.
3. *"CMB '자동 통과' 는 primary peak 한정. δr_d/r_d ≈ 0.7% 가 θ_* 에 동등 shift 를 줄 텐데 §14.4 표 와 §11 BAO 결과가 충돌한다."* → 가장 위험. §4.7 CMB 행 reword 필수.
4. *"5/5 PASS 가 아니라 2 NONTRIVIAL + 2 TRIVIAL + 1 PARTIAL 로 정직 보고하라."* → 본 audit 권고.

## 권고 — paper/base.md 수정 사항

- §4.7 표 **CMB 행** 분리: "primary peak 진폭 PASS / θ_* 0.7% shift (Phase-2 BAO 와 동일 채널)".
- §4.7 γ=1 박스 문구 보강: "T_photon=0 이 photon 직접 결합을 차단하지만, |γ−1| 의 실제 정량 한계는 β_eff = Λ_UV/M_Pl ≈ 7×10⁻²¹ 작음에서 온다."
- §14.4 #20 *"5개 관측 테스트 자동 통과"* → *"4개 자동 통과 (Cassini, GW170817, BBN, LLR) + 1개 부분 (CMB θ_* 는 Phase-2 BAO 와 같은 채널로 0.7% shift)"*.
