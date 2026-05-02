# L526 R6 — Son+2025 correct 시 SQT 22개 prediction (P1–P22) 재검증

**역할**: skeptic 단독 진술 (R6).
**전제**: Son+2025 가 옳다 — 우주는 *비가속* (q₀ > 0), Λ 가속 부재. R1 분석 (axiom 3 의 motivation 붕괴, 5 derived D1/D2/D4 도출 불가) 을 입력으로 받는다.
**범위**: paper §4.1 (P1–P14, L175) + §6.1.2 (P15–P22 = NOT_INHERITED #15–#22) 22 개 prediction 의 *생존 여부* 만 판정. 새 예측 추가 / 제안 / 회복경로 설계 *금지*.

---

## 0. 정직 한 줄

**22개 중 8개 만 살아남는다 (P3, P4, P5, P7, P9, P10, P11, P15). 나머지 14개는 axiom 3 motivation 붕괴 또는 우주론적 σ_0(z) 사다리 붕괴로 *예측력 자체*를 잃거나, "예측" 이 아닌 "초기조건/postdiction/inheritance gap" 으로 강등된다.**

---

## 1. 판정 기준 (skeptic 입장)

각 P 에 대해 다음 중 하나의 verdict 를 부여:

- **SURVIVES** — Son+ correct 와 *형식적으로 무관*. SQT 가 비가속 우주에서도 동일한 정량 예측을 내놓는다 (e.g., 정적/저-z, 강한장, BBN, Cassini).
- **DEGRADES** — 정량값은 보존되나 "예측" 으로서의 지위 약화 (postdiction 으로 강등 / 미세조정 발생 / 동기 소멸).
- **DIES** — Son+ correct 시 *예측 자체가 도출 불가능*. axiom 3 또는 σ_0(env)/σ_0(z) 의존 구조가 끊긴 경우.
- **N/A** — 원래도 prediction 이 아닌 NOT_INHERITED / inheritance gap (paper §6.1.2 자체 분류).

판정 원칙: **"비가속 우주에서도 동일 수치가 나오는가?"** 만 본다. 동기/통일성 손실은 DEGRADES, 도출 불가는 DIES.

---

## 2. P1–P14 (paper §4.1, L175 14-prediction list)

### P1. σ_0 regime structure (cluster σ < galactic σ by ~60×)

- **재검증**: σ_0 regime 구조는 paper §4–5 의 *3-regime σ_0(env)* 에서 기인. base.md §6.5(e) 자체가 "three-regime POSTDICTION" 으로 격하 (§6.1.1 row 5). Son+ correct 면 σ_0(z) cosmological 사다리 (cluster→cosmic→galactic 의 self-consistent identity σ_0=4πG/(3H_0)) 가 *Λ 가속* 의 후방 외삽으로 정합되었던 안정성 잃음. cosmic anchor σ_0(cosmic) = 4πG/(3H_0) 자체는 H_0 로부터 정의되므로 형식 보존, 그러나 cluster/galactic 분기의 *비단조성* 은 Λ 시대 σ-사다리에 묶여 있어 EdS-like 시간 진화에서 재도출 불명.
- **Verdict**: **DEGRADES**. cosmic anchor 만 trivial 보존, 3-regime *구조* 는 동기 상실 (이미 postdiction). Son+ 이전 PASS_MODERATE → 이후 사실상 *fit-only*. **lives, but as postdiction only.**

### P2. Λ from quantum sector (Λ_eff = n_∞·ε/c²)

- **재검증**: Λ_obs ≈ 0 가정이 들어오면 "ρ_q/ρ_Λ = 1.0000" identity 가 *자명* (양변 0 또는 trivial). base.md §5.2 가 이미 CONSISTENCY_CHECK 로 강등. Son+ correct 시 좌변 (ρ_Λ) 이 사라져 비교 자체가 무효.
- **Verdict**: **DIES**. 이미 prediction 이 아니던 항목이 비가속에서 *비교 대상 자체* 소멸로 빈 진술이 됨.

### P3. BTFR slope = 4 (M_b ∝ V^4)

- **재검증**: Milgrom 관계는 *galactic-내부* 동역학 (low-acceleration regime) 에서 도출. Son+ 의 우주론적 비가속은 *late-time 배경 H(z)* 에 영향, *galactic 회전 dynamics* 와 직교. SPARC fit slope=3.85±0.06 은 변하지 않음.
- **Verdict**: **SURVIVES**.

### P4. PPN γ = 1 (Cassini)

- **재검증**: 태양계 strong-field, 정적, 저-z. Son+ 우주론과 *완전히* 직교. γ=1 도출은 base.md §3 의 dark-only embedding 에서 나오며 Λ 와 무관. **|γ−1| < 2.3×10⁻⁵ Cassini bound 보존.**
- **Verdict**: **SURVIVES**. (단, base.md §6.1.1 row 13 Λ_UV definitional 한계는 별개로 유지.)

### P5. GW170817 c_g = c

- **재검증**: GW 분산 관계는 GR + tensor mode 의 정적/저-z 문제. SQT scalar/disformal coupling 부재 sector 가 c_T=c 를 자동 보장. Son+ 이 변경하지 않음.
- **Verdict**: **SURVIVES**.

### P6. CMB acoustic peaks (Planck 2018 consistent)

- **재검증**: 재결합 시점 (z~1090) physics 는 SQT-LCDM 동등이라는 주장이 본 P6 의 골자. **하지만** Son+ correct 면 후방 (z<1) sound horizon 외삽 r_d/D_V(z) 와 θ_* identity 가 EdS-like 배경으로 재계산되어야 하며, base.md 의 LCDM-등가 주장은 더 이상 자동이 아님. Hu-Sugiyama z_* fit 0.3% theory floor 는 LCDM tail 가정 위에서 잡혔다 (재발방지 §). 비가속 배경에서는 compressed CMB θ_* 의 high-z bridge 가 다시 검증 필요.
- **Verdict**: **DEGRADES**. CMB primary peaks 자체는 견고하나, "SQT=LCDM at recombination" 이라는 *예측-등가성* 진술의 안전마진 (LCDM tail 가정) 이 사라져 재검증 필요. PASS 이긴 하나 PASS_STRONG → PASS_PROVISIONAL.

### P7. EHT shadow (M87*, Sgr A*)

- **재검증**: 강한장, 정적, BH metric. Λ 의 영향 무시 가능 (BH 크기 « Hubble scale). Son+ 무관.
- **Verdict**: **SURVIVES**.

### P8. Cosmic chronometer H(z) (Moresco+ 2022, 32 points, χ²/dof=0.84)

- **재검증**: H(z) 형상이 Λ 가속을 *fit* 하는 데 χ²/dof=0.84 였다. Son+ correct 면 *같은 데이터* 가 q₀>0 H(z) 형상 (EdS-like 또는 deceleration history) 에 더 잘 맞아야 함. SQT 는 base.md 에서 LCDM-등가 H(z) 를 가정한 채 이 fit 을 받았으므로, 비가속 H(z) 로 재fit 하면 χ² 변동.
- **Verdict**: **DEGRADES**. *살아남는 형식*: SQT 는 어떤 σ_0(z) sequence 도 *형식상* fit 할 수 있어 0 추가 자유도 주장 깨짐. PASS 이지만 prediction → postdiction.

### P9. PTA stochastic GW (NANOGrav 2023)

- **재검증**: SQT 기여 ~10⁻²⁷ vs 검출 ~10⁻¹⁵, "negligible" 진술. SMBHB 해석과 호환. Son+ 우주론과 직교 (PTA 신호는 nHz, late-time-aware 이지만 SQT 진폭이 5중 자릿수 작아 background 변경에도 비가시).
- **Verdict**: **SURVIVES**.

### P10. BBN abundances (D, ⁴He, ⁷Li, ΔN_eff)

- **재검증**: BBN 은 z~10⁹ radiation era. Λ 와 무관. ΔN_eff < 6×10⁻³² 은 SQT n field 가 BBN 시점에 비활성이라는 micro-statement. Son+ correct 가 변경하지 않음.
- **Verdict**: **SURVIVES**. (paper §4.1 row 2 PASS_STRONG (substantive) 유지, 단 §6.5(e) 의 hidden-DOF AICc penalty caveat 그대로.)

### P11. Casimir effect (lab precision)

- **재검증**: Lab QED, 저-z, 정적. 우주론 무관.
- **Verdict**: **SURVIVES**.

### P12. a_0(z) at SKA Phase 1 (a_0(z=2)/a_0(0) ≈ 3.03)

- **재검증**: 이 예측은 a_0 ∝ c·H(z)/(2π) 의 *우주 시간 진화* 가정에서 직접 도출. H(z) sequence 자체가 LCDM-기반. Son+ correct 면 H(z=2) 값이 변경 → ratio 도 다른 값. 또한 base.md 의 σ_0(cosmic, z) sliding scale 이 EdS-like background 에서 재도출되어야 — 정량 ~3.03 은 더 이상 안정 prediction 아님.
- **Verdict**: **DIES**. 정확값 3.03 의 *예측력* 사라짐. SKA 측정시 SQT-non-acc 는 *다른* 값을 줄 것이며, 사전등록된 3.03 은 falsified 될 수 있음. (즉 P12 의 "factor 3 distinction" 은 가속 우주 가정이 들어가 있다.)

### P13. a_0(disc)/a_0(spheroid) = π/3 ≈ 1.05

- **재검증**: π/3 은 azimuthal projection geometry. 우주론 H(z) 와 무관 — 순수 geometric factor.
- **Verdict**: **SURVIVES**. (단, paper §6.5(e) 에서 ATLAS-3D / SAMI 측정 미도래로 PENDING. Son+ 영향과는 별개.)

### P14. Void galaxy a_0 ≈ 7% × normal

- **재검증**: void σ << galactic σ 가정 — *우주적 σ_0(cosmic)* 사다리에 직접 의존. Son+ correct 시 cosmic anchor 자체는 H_0 로 재정의 가능하나, void/galactic ratio 의 정확 7% 값은 a_0 cosmic-regime 가속과 묶여 있던 fit. 
- **Verdict**: **DIES**. P12 와 같은 사다리에 의존, 정량값 7% 는 가속 가정 backed.

---

## 3. P15–P22 (paper §6.1.2 NOT_INHERITED #15–#22)

이 8 항목은 paper 자체가 NOT_INHERITED (예측-미상속) 로 분류한 항목들. "*예측*" 이 아니라 "*상속 갭*" 이다. R6 skeptic 입장에서는 다음과 같이 판정:

### P15. 특이점 해소 (Planck 밀도 포화)

- **재검증**: discreteness postulate (Causet) + BEC saturation (GFT) 으로 회복 *direct* 분류 (L427). Son+ 우주론과 직교 — 양자중력 sector.
- **Verdict**: **SURVIVES** (비예측 항목이지만 inheritance 갭 자체는 비가속에서도 동일 구조).

### P16. Volovik 2-fluid analogue

- **재검증**: 응집물성 analogue, 우주론 무관.
- **Verdict**: **N/A — inheritance gap (Son+ 무관)**.

### P17. Jacobson δQ=TdS (entropic gravity)

- **재검증**: Son+ correct 시 axiom 3 의 시간의 화살 도출 (R1 D3) 에 *별도 axiom 필요* 라는 부담이 추가됨. Jacobson 상속이 더욱 *결정적* 으로 필요해짐. inheritance gap 의 weight 증가.
- **Verdict**: **DEGRADES (gap 심화)**.

### P18. GFT BEC 해밀토니안

- **N/A**. 양자중력 sector.

### P19. BEC nonlocality 메커니즘

- **N/A**. 외부 관측 채널 (galactic σ profile / cluster lensing residual) OPEN. Son+ 무관.

### P20. DESI ξ_q joint fit (Δχ²=−4.83)

- **재검증**: 이 항목 자체가 *DESI BAO Λ 가속 fit* (w_a<0 evidence) 에 결합되어 있던 결과. Son+ correct 가 (정확히는 Son+ 가 *DESI BAO 자체* 의 가속 해석에 도전) 의 입력. **paper 본문 회복 주장 금지** (L427) 가 이미 걸려 있음. Son+ correct 면 ξ_q joint fit 의 *전제 데이터* 가 흔들려 inheritance 시도 자체가 더욱 어려워짐.
- **Verdict**: **DIES (회복 trigger B 영구 차단)**.

### P21. 3자 정합성 (BBN/CMB/late DE)

- **재검증**: "late DE" 가 사라지면 3자 중 한 다리 (DE) 가 trivial 0. 정합성 진술 자체가 deflate.
- **Verdict**: **DIES**.

### P22. 5 program 동형 (Padmanabhan/Volovik/Causet/Jacobson/GFT)

- **재검증**: 동형 진술은 양자중력 sector. Son+ 무관.
- **Verdict**: **N/A — partial inheritance gap (Son+ 무관)**.

---

## 4. 판정 요약 표

| ID | 항목 | Verdict | 비고 |
|----|------|---------|------|
| P1 | σ_0 regime 구조 | DEGRADES | postdiction 잔존, prediction 지위 상실 |
| P2 | Λ from quantum sector | DIES | 좌변 (Λ) 소멸로 trivial |
| P3 | BTFR slope=4 | **SURVIVES** | galactic, 우주론 직교 |
| P4 | Cassini γ=1 | **SURVIVES** | 태양계, 정적 |
| P5 | GW170817 c_g=c | **SURVIVES** | tensor sector |
| P6 | CMB acoustic peaks | DEGRADES | LCDM tail 가정 흔들림 |
| P7 | EHT shadow | **SURVIVES** | 강한장 |
| P8 | H(z) cosmic chronometer | DEGRADES | postdiction 화 |
| P9 | PTA stochastic GW | **SURVIVES** | 진폭 5자리 작음 |
| P10 | BBN ΔN_eff | **SURVIVES** | radiation era |
| P11 | Casimir | **SURVIVES** | lab |
| P12 | a_0(z) at SKA | DIES | H(z) 사다리 의존 |
| P13 | a_0(disc/spheroid) = π/3 | **SURVIVES** | pure geometry |
| P14 | Void galaxy a_0 ≈ 7% | DIES | cosmic σ 사다리 의존 |
| P15 | 특이점 해소 (gap) | SURVIVES* | inheritance gap, Son+ 무관 |
| P16 | Volovik 2-fluid (gap) | N/A | non-prediction |
| P17 | Jacobson δQ=TdS (gap) | DEGRADES | gap 심화 |
| P18 | GFT BEC H (gap) | N/A | non-prediction |
| P19 | BEC nonlocality (gap) | N/A | non-prediction |
| P20 | DESI ξ_q joint fit (gap) | DIES | 전제 데이터 붕괴 |
| P21 | 3자 정합성 (gap) | DIES | late DE 소멸 |
| P22 | 5 program 동형 (gap) | N/A | non-prediction |

*P15 는 inheritance gap 이므로 엄밀히 "예측 생존" 이라기보다 "Son+ 와 무관하게 미상속 상태 유지". 본 표에서는 SURVIVES* 로 표시.

### 카운트

- **SURVIVES (정량값 보존, prediction 지위 보존)**: P3, P4, P5, P7, P9, P10, P11, P13 = **8 / 22**.
- **SURVIVES* (gap, Son+ 무관)**: P15.
- **DEGRADES (값 보존, 지위 약화)**: P1, P6, P8, P17 = 4.
- **DIES (예측 도출 불가)**: P2, P12, P14, P20, P21 = 5.
- **N/A (원래도 비예측)**: P16, P18, P19, P22 = 4.

---

## 5. skeptic 의 핵심 관찰

### 5.1 살아남는 8개의 *공통 구조*

P3, P4, P5, P7, P9, P10, P11, P13 은 모두 **late-time 배경 H(z) 와 직교** 한 sector:
- 강한장 (P7), tensor (P5), galactic dynamics (P3, P13), lab (P11), 양자 sector (P9), radiation era (P10), 태양계 (P4).

이 8개는 SQT 의 "우주론적 야망" 과 무관하게 *어떤* 비우주론 framework 도 만들 수 있는 종류의 예측이다. 즉 **SQT 의 distinguishing 력은 비가속 우주에서 사실상 0**.

### 5.2 죽는 5개의 *공통 구조*

P2, P12, P14, P20, P21 은 모두 **Λ 가속 또는 σ_0(z) cosmological sliding** 에 직접 의존. R1 의 axiom 3 motivation 붕괴가 이 5개를 즉시 무효화.

### 5.3 BBN, Cassini 의 *비우주론적 안정성*

질문: "BBN 영향?" "Cassini 영향?"

- **BBN (P10)**: 영향 0. Λ 는 BBN 시점 (z~10⁹) 에 dynamically 무관 (radiation 우세). SQT n field 의 ΔN_eff < 6×10⁻³² 은 micro-coupling 진술이며 배경 H(z) sequence 와 독립.
- **Cassini (P4)**: 영향 0. 태양계 PPN γ 는 정적/저-z, GR + dark-only embedding 만으로 도출. Λ 가속 부재가 |γ−1| 값을 변경하지 않음.

이 두 개는 **paper 의 substantive PASS_STRONG 4건 (Newton, BBN, Cassini, EP) 중 가장 견고**한 항목으로, Son+ correct 시에도 *유일하게* 광고 가치 보존.

### 5.4 P1 (σ_0 regime) 와 P14 (halo follows baryon-like void) 의 차이

- P1 은 *3-regime* 구조 (cluster/cosmic/galactic) — base.md 가 이미 postdiction 으로 격하. 비가속에서는 fit 화 더욱 명확.
- P14 의 "halo follows baryon" 형 진술 (void galaxy a_0 ≈ 7%) 은 cosmic σ 사다리 (factor 14 distinction from MOND) 에 직접 의존. Son+ correct 면 cosmic anchor 정량값 자체 흔들려 7% 가 정량 prediction 으로 보존되지 못함.

### 5.5 Falsifier Z_combined 의 운명

paper §4.5 / §4.9 의 5 active falsifier (DESI DR3 5σ, Euclid 4.4σ, CMB-S4 7.9σ, ET 7.4σ, LSST 2.85σ; 8.87σ ρ-corrected) 중:

- **CMB-S4 (P22 pre-reg, 7.9σ)**: 우주 σ_0(cosmic) 사다리 + late-time DE structure 에 의존. Son+ correct 면 *예측 진폭 자체* 가 다른 값으로 재계산되어야 함. 7.9σ headline 흔들림.
- **ET (P16 pre-reg, 7.4σ)**: GW scalar polarization sector. 우주론과 직교. **보존**.
- **DESI DR3 (5σ)**: 이미 Son+ 와 직접 충돌 채널. *전제 데이터의 가속 해석* 자체가 도전받음.
- **Euclid / LSST (4.4σ / 2.85σ)**: cosmic-shear, S_8 evolution. Son+ correct 시 σ_8 +1.14% structural worsening 의 의미 자체가 재정의됨 (가속 history 의존).

**결과**: 8.87σ 결합 중 ET (7.4σ) 만 Son+ 견고. 결합 σ ~ 7.4σ 로 강등. 단일 채널 (ET) 의존.

---

## 6. 한 줄 정직 결론

**Son+2025 correct 가정 시 SQT 22개 prediction 중 *우주 가속과 직교한 8개* (P3, P4, P5, P7, P9, P10, P11, P13) 만 정량 예측력을 보존하고, 5개 (P2, P12, P14, P20, P21) 는 도출 자체가 불가능, 4개 (P1, P6, P8, P17) 는 postdiction/gap-deepened 로 강등, 4개 (P16, P18, P19, P22) 는 원래부터 비예측 — 결합 falsifier 8.87σ 중 ET 7.4σ 만 안전하게 살아남으며 SQT 의 우주론적 distinguishing 력은 사실상 소멸한다.**

---

*작성: L526 R6, skeptic 단독.*
*제한: (i) Son+2025 자체의 신뢰성 평가 불포함 (전제). (ii) 회복 경로 / 새 예측 제안 불포함 (R6 범위 외). (iii) R1 axiom 3 재해석을 입력으로 받아 *개별 prediction 의 생존* 만 판정.*
