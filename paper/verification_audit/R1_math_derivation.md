# R1 검증 — 수학적 도출 4 claim audit

**검증자**: R1 (이론 수학자, 매우 냉철)
**대상**: root `/base.md` §14.1 의 "수학적 도출 ✅ 4개"
**기준 framework**: `paper/base.md` (6 postulates + 4 foundations)
**검증일**: 2026-05-01

---

## 0. 정직성 선언

`paper/base.md` 는 root `/base.md` 와 **다른 표층 구조**를 가진다.
- root: 가정 1–3 (흡수/소멸/유입) → §III 정상상태 도출 → §IV 라그랑지안.
- paper: postulate a1–a6 (a1=흡수, a2=보존, a3=Γ₀ 균일생성, a4=발현 metric, a5=bound matter, a6=linear maintenance) → derived 1–5 + 4 foundation (Schwinger-Keldysh, Wetterich RG, Holographic σ₀=4πG·t_P, Z₂ SSB) → three-regime σ₀(env).

paper framework 는 derived 1 ("Newton G 회복", a1+a4) 를 *명시*하지만 **유도 sketch 만** 적고, 실제 수학적 단계 (`4πr²n₀v=σn₀M`, `U=-GMm/r` 매칭, `G=n₀μσ²/(4π)`) 는 root §III 에 의존한다. paper 가 **자기완결적 도출 텍스트를 보유하지 않으므로**, 4 claim 의 검증은 다음 두 조건을 모두 요구한다:
1. paper 의 6 postulate + 4 foundation set 이 root §III 도출의 *전제*를 빠짐 없이 cover 하는가
2. paper 가 제거한 root 가정 (예: 가정 2의 mass-action `σ·n·ρ_m`) 이 도출에 *암묵적으로 필요한가*

---

## 1. Verdict 표

| # | Claim | Verdict | 핵심 사유 |
|---|-------|---------|-----------|
| 1 | 1/r² 중력 (정상상태 Poisson 해) | **PARTIAL** | derived 1 sketch 만 존재. paper a1–a6 만으로 `σ·n·ρ_m` mass-action 형태가 유도되지 않음 — root §I 가정 2 가 implicit. holographic foundation σ₀=4πG·t_P 으로 σ 는 회수되나 `n` 의존 형태는 a1 의 *해석*. |
| 2 | 특이점 해소 (이산적 Planck 밀도 포화) | **PARTIAL → FAIL-prone** | postulate-level "discreteness" 진술 부재. root §I 가정 1 ("이산적 양자, 수밀도 n") 이 paper 에서는 GFT (foundation-adjacent) 로 외주됨. Bounce 해소는 root §V.5 에서 *GFT BEC 응축* 인용으로만 등장 — paper 6+4 set 에는 GFT 가 *foundation* 으로 등재되어 있지 않음 (Schwinger-Keldysh / Wetterich / Holographic / Z₂ SSB 4축). |
| 3 | 균일 생성 + 국소 소멸의 필연성 (4원리 수렴) | **PASS-conditional** | a3 (cosmic Γ₀ 균일생성) + a1 (흡수) 이 직접 진술. root §II.2 의 4 원리 (de Sitter/2법칙/QFT/일반공변성) 는 paper 4 foundation 과 *교집합 비공식*: Schwinger-Keldysh 가 QFT 자발방출/유도흡수, Z₂ SSB 가 대칭깨짐 mechanism, Wetterich RG 가 IR universality 를 cover. 단, "de Sitter 대칭" 과 "일반 공변성" 은 paper 의 어느 foundation 에서도 *명시* 도출되지 않음 (a4 발현 metric 의 *결과*로만 가정됨). |
| 4 | 뉴턴 극한에서 Poisson 방정식 복원 | **PASS** | paper §4.4 (root) 의 `□φ + V'(φ) = ξ T^α_α` 비상대론 정적 극한이 `∇²(δφ) = -ξ ρ_m c²` 로 환원, ξ = 2√(πG)/c² (paper §4.3) 매칭으로 `∇²Φ_N = 4πG ρ_m` 자동 회복. 이 사슬은 paper 라그랑지안 (Einstein-Hilbert + canonical kinetic + V(φ) + ξφT + L_m) 만으로 자기완결. PPN γ=1 (paper §4.7) 와 정합. |

**종합 PASS rate**: 1/4 full PASS (claim 4), 1/4 conditional PASS (claim 3), 2/4 PARTIAL (claim 1, 2). 강한 의미의 PASS 는 25%, 약한 의미 (조건부 포함) 는 50%.

---

## 2. Claim별 1단락 분석

### Claim 1 — 1/r² 중력 (PARTIAL)

paper framework 의 derived 1 row 는 "depletion-zone gradient → 1/r²" 한 줄 sketch 를 제공할 뿐 실제 도출은 root §III.1 의 **flux conservation** `4πr²·n₀·v(r) = σ·n₀·M` 에 의존한다. 이 식의 우변 `σ·n₀·M` 은 **root 가정 2**의 mass-action `σ·n·ρ_m` 적분 (질량 M 안에서 `ρ_m` 적분) 형태이며, paper 의 a1 ("matter absorbs spacetime quanta") 자체로는 *흡수율의 함수형*이 결정되지 않는다. 즉 a1 은 *흡수가 일어난다*는 정성 진술이고, "비례계수가 σ·n·ρ_m 이다" 는 별도 가정이 필요하다. Holographic foundation 이 σ=4πG·t_P 를 *값* 으로 고정하지만, **함수형** (mass-action vs 다른 reaction kinetics) 은 어디에도 priori 도출되지 않는다.
- *Circularity*: 약함. σ 값과 `1/r²` 표현이 G 정의 자체에 의존하나, root §3.4 가 이미 정직 disclosure ("G 변수 치환에 불과") 를 한 상태.
- *Missing piece*: mass-action kinetics `σ·n·ρ_m` 의 a1 으로부터 도출 또는 별도 postulate 화. Schwinger-Keldysh 가 *interaction vertex* 를 제공할 수 있지만 paper 는 이를 명시하지 않음.
- *추가 가정*: "흡수율 = bilinear in n and ρ_m" 가정 (사실상 root 가정 2).
- *Dimensional*: `[σ·n·ρ_m] = m³kg⁻¹s⁻¹ · m⁻³ · kg/m³ = kg/(m³·s)` (수밀도 변화율 체크 OK).

### Claim 2 — 특이점 해소 (PARTIAL/FAIL-prone)

이산성 (discrete spacetime quanta) 은 root §I 가정 1 의 핵심이지만 paper 의 6 postulate 어디에도 "discrete" 또는 "lattice" 진술이 명시되지 않는다. paper a4 ("발현 metric, 미시 OPEN") 는 의도적으로 *미시 mechanism 을 비워둠* — Causet meso (5번째 축 후보) 와 GFT 가 후보로 거명되나 둘 다 paper 의 confirmed foundation 에 포함되지 않는다. Bounce 해소 자체는 root §V.5 가 GFT BEC 응축으로 수정 Friedmann 을 얻는다는 *외부 인용*에 의존하며, paper 4 foundation (Schwinger-Keldysh, Wetterich, Holographic σ₀, Z₂ SSB) 에서는 직접 도출되지 않는다.
- *Circularity*: 없음.
- *Missing piece*: discreteness postulate (root 가정 1 의 paper 등재) 또는 GFT foundation 의 추가.
- *추가 가정*: "n 에 UV cutoff (Planck 밀도) 가 존재한다" — paper 에는 Holographic dimensional bound 가 *σ₀ uniqueness* 만 보장하고 *밀도 포화* 는 보장하지 않음.
- *Verdict 강화 시*: a4 의 5번째 축 (Causet meso) 가 confirm 되거나 GFT 가 5번째 foundation 으로 추가되면 PASS 로 격상 가능.

### Claim 3 — 균일 생성 + 국소 소멸의 필연성 (PASS-conditional)

a3 (cosmic Γ₀ 균일 생성) + a1 (matter absorbs) 의 조합으로 paper postulate 수준에서 직접 진술된다. root §II.2 의 "4 원리 수렴" 표 — (i) de Sitter symmetry, (ii) 2법칙, (iii) QFT 자발방출/유도흡수, (iv) 일반 공변성 — 중 (iii) 은 Schwinger-Keldysh open-system foundation 에 자연 포함되고 (대칭 깨뜨림은 Z₂ SSB 가 cover), (ii) 와 (iv) 는 paper postulate 보조 진술 (a2 보존 + 일반 공변성 implicit) 에서 회수된다. (i) de Sitter symmetry 는 a4 ("emergent metric") 의 *최대 대칭 vacuum 한계*에서 구현되나 paper 가 명시 도출하지 않음. 따라서 4 원리의 "독립적 수렴" 주장은 paper framework 안에서도 retained 되지만, *de Sitter 대칭의 어디에서 오는가* 가 a4 OPEN 에 묶여 약점이다.
- *Circularity*: 없음. 4 원리 각각이 다른 구조에서 같은 결론에 도달 (over-determination 형 robustness).
- *Missing piece*: de Sitter symmetry 의 a4 로부터의 priori 도출 (현재 axiom 4 5번째 축 후보 OPEN 과 결합).
- *추가 가정*: 없음 — postulate set 자체가 이미 결론을 포함.

### Claim 4 — Newton 극한 Poisson 복원 (PASS)

paper §4 (라그랑지안 장) 가 명시하는 작용
S = ∫√(-g)[c⁴R/(16πG) + ½(∂φ)² - V(φ) + ξφT^α_α + L_m]
에서 metric 변분 → Einstein eq, φ 변분 → `□φ + V'(φ) = ξ T^α_α` 가 직접 도출. 정적/비상대론 극한에서 `T^α_α ≈ -ρ_m c²` (먼지), `□ → -∇²`, V'(φ₀)=0 정상점 조건이면 `∇²(δφ) = -ξ ρ_m c²` 가 그대로 Poisson 형태가 된다. matching 은 ξ = 2√(πG)/c² (paper §4.3 고정값) 를 통해 `∇²Φ_N = 4πG ρ_m` 으로 정합. 이 사슬은 paper postulate set 외부 가정 없이 자기완결.
- *Circularity*: 없음. ξ 가 G 에 묶여 있으나 이는 *normalization choice* (paper §4.6 에서 G 가 상수 status 로 명시) 이며 도출의 input.
- *Missing piece*: 없음 — Lagrangian-level claim.
- *Dimensional 검증*: `[ξφT^α_α] = m^{-1}kg^{1/2}s^{-1} · kg^{1/2}m^{1/2}s^{-1} · kg/(m·s²)` 등 매개변수 단위는 ξ 정의에 의존, ∇²Φ ~ 4πGρ 의 SI 차원 [s⁻²] 일치. `ξ = 2√(πG)/c²` 에서 √(πG) 는 [m^{3/2}kg^{-1/2}s^{-1}], ÷ c² → [m^{-1/2}kg^{-1/2}s] — φ 의 canonical [kg^{1/2}m^{-1/2}s^{-1}] 와 결합하여 ξφ 는 [s/m] · [s⁻¹] = [1/m], T^α_α [kg/(m·s²)] 곱하면 [kg/(m²·s²)] 즉 ∇²φ 의 source dimension 과 정합.

---

## 3. 종합 정직 보고

- 4 claim 중 **claim 4 만이 paper framework 자기완결적 PASS**.
- claim 1 은 *함수형* (mass-action) 이 paper postulate set 에 누락됨. root 가정 2 의 paper 등재 또는 foundation 으로의 도출 작업 필요.
- claim 2 는 paper 가 의도적으로 비운 a4 (emergent metric, 미시 OPEN) 와 직접 충돌. discreteness 가 5번째 축 / 5번째 foundation 으로 추가되지 않으면 paper-only 도출은 FAIL.
- claim 3 은 robust 하나 de Sitter symmetry origin 이 a4 OPEN 에 묶여 weak-PASS.
- root `/base.md` §14.1 의 "수학적 도출 ✅ 4개" 라벨은 root framework (가정 1–3 명시 포함) 에서는 정당하나, paper framework (6 postulate + 4 foundation) 에서는 **2개 PARTIAL + 1개 conditional + 1개 PASS** 로 격하해야 정직.

권고: paper §2.1 표에 (a) discreteness postulate 추가 (또는 GFT 를 5번째 foundation 으로 등재), (b) a1 의 mass-action functional form 을 명시, (c) a4 OPEN status 를 claim 1/2 verdict 에 명시 inheritance.
