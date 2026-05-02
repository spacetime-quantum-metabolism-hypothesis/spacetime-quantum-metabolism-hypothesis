# L420 ATTACK_DESIGN — 8인팀 reviewer 공격 설계

**주제**: paper/base.md §4.1 Cassini PASS_STRONG 의 β_eff = Λ_UV/M_Pl ≈ 7.4×10⁻²¹ 도출 정합성.
**목표**: Λ_UV ≈ 18 MeV 의 *왜 그 값?* 에 대한 reviewer 비판 시뮬레이션.
**방법**: 8인 자율 토의 (Rule-A). 역할 사전 지정 없음. 자연 분담된 비판 채널 8개 정리.

---

## 8인팀 자율 발생 비판 채널

### 비판 #1 — Definitional caveat 자체 인정
paper/base.md L857 "한계 #13: Λ_UV definitional, RG-유도 아님 / ACK / UV completion".
**저자가 이미 인정한 한계** 를 PASS_STRONG 4건 중 하나로 카운트하는 것은 자체 모순.
PASS_STRONG (substantive) 는 "σ₀ 항등식 *외* 추가 axiom 입력 필요" 로 정의되어 있고 (L896),
Λ_UV 를 추가 axiom 으로 인정해 PASS_STRONG 자격을 유지하지만, 이 경우 *예측력 = 0*.
β_eff 가 작다는 결론을 위해 18 MeV scale 을 손으로 넣은 후 18 MeV 이 작아서 통과한다고 주장하는 순환.

### 비판 #2 — 5/5 over-claim 의 잔재
L903 "5/5 자동 통과 over-claim 격하" 가 README 단계에서는 수정되었지만,
β_eff 의 출처가 axiom 이 아니라 *관측 mass scale* 인 한, Cassini 통과는 **postdiction** 이지 prediction 이 아님.
"|γ-1| ≈ 10⁻⁴⁰ ≪ 2.3×10⁻⁵" 의 40 자리수 여유는 β_eff 임의 입력에서 자동 발생.

### 비판 #3 — η_Z₂ vs Λ_UV 이중 scale
BBN 보호 (η_Z₂ ≈ 10 MeV, L755) 와 Cassini 보호 (Λ_UV ≈ 18 MeV, L756) 가 *별도 scale 입력*.
Z₂ SSB scale 과 UV completion scale 이 **왜 같은 자리수에서 분리** 되는지 설명 부재.
독립 입력 2개로 PASS_STRONG 2건 → axiom 경제성 페널티.

### 비판 #4 — 실제 mechanism 은 PASS_TRIVIAL 일 가능성
L756 "T_photon=0 단독 mechanism *아님*" 단서는 photon-darkforce 분리 (dark-only embedding)
가 자동으로 |γ-1|=0 을 주는 PASS_TRIVIAL 채널과 구별 불능.
β_eff 항을 제거하고 dark-only 만 남겨도 Cassini 통과 → β_eff 항 자체가 *redundant*.

### 비판 #5 — RG 비유도성의 구조적 의미
"RG-유도 아님" 은 단순 미완성이 아니라 SQMH 가 EFT cutoff 구조를 갖지 못한다는 의미.
정상적 EFT 는 Λ_UV 를 *β-function 폐쇄점* 또는 *new physics threshold* 로 정의.
SQMH 의 "공간 BEC 응집체" axiom (L0–L3) 에는 RG 흐름 정의가 부재 → Λ_UV 는 외부 차용.

### 비판 #6 — Z₂ SSB scale 의 임의성
L692 "Z₂ spontaneous symmetry breaking, η ≲ 10 MeV 제약" 자체가 BBN 관측 *상한* 에서 역산.
즉 η_Z₂ 도 prediction 이 아닌 BBN-fit. 두 scale 모두 데이터에서 빌려옴.

### 비판 #7 — 18 MeV 의 우연 일치 위험
18 MeV ≈ 2 × η_Z₂ (10 MeV) 또는 ≈ (Λ_DE² M_Pl)^(1/3) (24.6 MeV) 등
손쉬운 numerical coincidence 가 존재하지만, 어느 것도 SQMH axiom 에서 도출되지 않음.
사후 일치는 reviewer 가 "fine-tuning to fit caveat" 로 거부.

### 비판 #8 — Falsifiability 약화
β_eff 가 임의 입력이면 "어떤 관측이 SQMH 의 Cassini 통과를 falsify 할 수 있는가?" 답이 없음.
|γ-1| 측정이 향상되어도 Λ_UV 를 미세조정해 통과 가능. 따라서 PASS_STRONG 등급은 *epistemically* PARTIAL 에 가까움.

---

## 8인팀 합의 결론

- Cassini PASS_STRONG 은 *데이터-독립 prediction* 이 아니라 *axiom 외부 scale 입력에 의존하는 conditional pass*.
- 등급 유지 가능 조건: §6.1 row #13 caveat 을 명시적으로 동반할 것.
- "Λ_UV 의 a priori 도출" 이 가능하면 PASS_STRONG → PASS_STRONG_PRIMARY 로 격상.
- 도출 실패 시 caveat 강화 (현재보다 더 명시적 표현) 가 정직 권고.
