# L419 ATTACK_DESIGN — 8인팀 공격 설계

**주제**: BBN PASS_STRONG 강화. paper §4.1 row 2 가 두 보호 mechanism (η_Z₂ ≈ 10 MeV ≫ T_BBN factor 100, β_eff² ≈ 5.5×10⁻⁴¹) 으로 ΔN_eff ≈ 10⁻⁴⁶ < 0.17 통과를 광고. Reviewer 의 가능한 공격면을 8명 시뮬레이션.

**좌표**:
- paper/base.md §2.4 row 4 — Foundation 4 (Z₂ SSB), η ≲ 10 MeV "제약"으로 표기.
- paper/base.md §4.1 row 2 — "η_Z₂ ≈ 10 MeV ≫ T_BBN + β_eff² 두 보호".
- paper/base.md §4.1 row 3 (Cassini) — β_eff = Λ_UV/M_Pl ≈ 7.4×10⁻²¹ 사용.
- paper/base.md §6.5(e) — BBN ΔN_eff 가 substantive PASS_STRONG 4건 중 하나로 등재.

---

## 1. Reviewer 공격 표면 (8인팀 시뮬레이션)

### A1 — BBN nucleosynthesis specialist
> "10 MeV 가 'foundation 4 의 제약' 으로 §2.4 에 기술되어 있을 뿐, 어떤 SSB scalar 의 vev/mass 인지 Lagrangian 수준 정의 부재. paper 가 'η ≲ 10 MeV' 라는 *상한* 만 명시 — 이는 BBN bound 에서 *역으로* 들어온 값일 수 있다 (postdiction risk)."

**Severity**: 결정적. η_Z₂ scale 의 priori 도출 부재 → "BBN bound 으로 η_Z₂ 를 정의해서 다시 BBN bound 을 통과한다" 의 circularity 위험. L419 simulation 으로 *어떤 Standard-Model scale 후보들이 자연 일치하는지* 정량화 필요.

### A2 — EFT/RG reviewer
> "β_eff = Λ_UV/M_Pl 정의에서 Λ_UV 가 무엇인가? §6.1 row 13 가 'Λ_UV definitional, RG-유도 아님' 인정. 7.4×10⁻²¹ × M_Pl ≈ 90 MeV (full Planck) 또는 18 MeV (reduced) — η_Z₂ ≈ 10 MeV 와 같은 order. Λ_UV ≡ η_Z₂ 라는 *implicit identification* 이 진행 중. 이게 명시되어 있나?"

**Severity**: 치명. **L419 simulation 결과**: β_eff = 7.4e-21 ↔ Λ_UV(full) = 90 MeV, Λ_UV(reduced) = 18 MeV. 둘 다 η_Z₂ 와 factor 1.8–9. 즉 **paper 의 두 보호 mechanism 은 *동일 scale* 에서 옴**. Independent 가 아니다.

### A3 — Cosmologist (CMB-degeneracy)
> "ΔN_eff = 10⁻⁴⁶ 은 *임의로 작은* 숫자다. Planck bound 0.17 대비 45 dex 여유. 이런 'over-pass' 는 보통 mechanism 이 *너무 강해* 다른 채널에서 KILL 되는 신호. Z₂ scalar 가 BBN 에 얼마나 결합하는지 vs CMB θ_* (paper §4.1 row 8 PARTIAL) 에 얼마나 결합하는지 정합성 미확인."

**Severity**: 중대. 단 paper §5.6 가 "BBN PASS, 재결합 무영향, neutrino 독립" 분리 명시 — 채널-by-채널 disclosure 존재.

### A4 — Theorist (foundation 4 micro)
> "η_Z₂ ≈ 10 MeV 의 priori 도출 path 가 §2.4 에 없다. 'Z₂ SSB' 만 명시. 어떤 potential V(φ) 에서 vev=10 MeV 가 *예측*되는지? mu² 와 lambda 가 SM 의 어떤 scale 과 결합? **paper 가 priori prediction 으로 분류한 4 건 중 하나가 사실은 BBN 데이터로 fit 한 한계값** 일 가능성."

**Severity**: 결정적. **L419 simulation [3] 결과**: SM 후보 11종 중 **√(m_e × Λ_QCD) ≈ 10.5 MeV 가 0.02 dex 내 일치**. 이는 priori candidate path *후보* 이지 derivation 이 아님. 정직 한계로 §6.1 등재 권고.

### A5 — Statistical reviewer
> "두 mechanism 이 multiplicative 로 보호한다는 narrative — 사실은 둘 다 같은 Λ_UV scale 에서 옴 (A2 지적). 독립 보호 두 개가 아니라 *하나의 scale 의 두 표현*. PASS_STRONG 라벨이 robustness 를 over-state."

**Severity**: 중대. **L419 simulation [2] 결과**: A-only ΔN ≤ 5.2e-5 (Boltzmann), B-only ΔN ≤ 3.8e-18 (포털). **B 가 A 보다 10⁻¹³ 더 강력 — A 는 redundant.** "두 mechanism" narrative 보다 **"β_eff² portal 단독으로 17 dex 여유 + Boltzmann 추가 13 dex 보너스"** 가 더 정확.

### A6 — Phenomenologist (BSM portal)
> "β_eff² = (Λ_UV/M_Pl)² ≈ 5.5e-41 의 portal coupling. 이건 standard scalar portal phenomenology 에서 freeze-in 영역 (never-thermalised). DM 후보로 reinterpret 가능 — Z₂ scalar 가 DM 일부 일 수 있나? paper §5 dark sector 와 연결?"

**Severity**: 중간. 새로운 연결 path 시사 — 하지만 본 task 범위 외.

### A7 — Skeptical referee (PRD-level)
> "paper §6.5(e) 에서 PASS_STRONG (substantive) 4 건 중 하나가 BBN ΔN_eff. 단 mechanism (a) η_Z₂ scale 이 priori 아님 (foundation 4 가 *상한* 명시), (b) β_eff 가 Λ_UV 정의 의존 (§6.1 row 13 ACK). **두 input 모두 paper 가 정직 caveat 한 항목들의 곱** — 이건 'PASS_STRONG' 라벨 보다 'PASS_BY_INPUT' 라벨이 더 정직하지 않은가?"

**Severity**: 결정적. paper 가 §6.5(e) 에서 "η_Z₂ scale, Λ_UV/M_Pl" 을 *추가 axiom 입력* 으로 명시한 것과 일치. 단, 그래도 Cassini 와 같은 등급 (PASS_STRONG) 으로 분류되어 있는 것은 두 입력 모두 OOM 수준에서 SM scale 과 일치하기 때문 — A4 의 √(m_e Λ_QCD) match 가 이를 지지.

### A8 — Honest-broker reviewer
> "결론적으로 BBN bound 통과는 robust. 단 narrative 를 두 가지로 분리할 것: (i) **structural pass** — β_eff² portal 단독 17 dex 여유, η_Z₂ 가 어떤 SM scale (1 MeV ~ 1 GeV) 어디든 PASS, (ii) **priori claim** — η_Z₂ ≈ 10 MeV 자체의 도출은 OPEN. (i) 만 PASS_STRONG, (ii) 는 §6.1 등재."

**Severity**: 권고. 정직 분리 후 PASS_STRONG 는 유지 가능.

---

## 2. 공격 면 종합

| 공격 | 핵심 | 본 작업 (L419 simulation) 답변 |
|------|------|--------------------------------|
| A1, A4 | η_Z₂ priori 도출 부재 | √(m_e Λ_QCD) ≈ 10.5 MeV 0.02 dex match candidate 발견; 단 derivation 아님 (§6.1 OPEN 유지) |
| A2 | β_eff = Λ_UV/M_Pl 의 Λ_UV 정체 | full M_Pl 시 Λ_UV=90 MeV, reduced 시 18 MeV — η_Z₂ 와 동일 scale |
| A5 | 두 mechanism redundancy | B(portal) 단독 ΔN ≤ 3.8e-18; A(Boltzmann) 는 13 dex 추가 보너스. 진짜 보호는 B |
| A7 | input 두 개 모두 caveat 항목 | OOM 수준에서 SM scale 일치 → PASS_STRONG 유지하되 narrative 정직 분리 |
| A3 | CMB 채널 정합성 | §5.6 채널 분리 disclosure 가 이미 답함 |

## 3. 핵심 발견 (정직 한 줄)

> 두 보호 mechanism 은 **독립이 아니라 동일 Λ_UV scale 의 두 표현**이고, β_eff² portal 단독으로 ΔN_eff ≤ 4×10⁻¹⁸ 로 17 dex 여유. PASS_STRONG 는 robust 하나 narrative 는 "**single-scale 17-dex margin**" 로 정정 권고.
