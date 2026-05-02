# L582 — Mass Path 1 (kinetic ρ) 8인 회의적 검증

작성일: 2026-05-02
대상: L575 §2 후보 A (path 1, kinetic energy density 재정의) — Round 11 등재 가부
규약: [최우선-1] 절대 준수 / 좋은 점 생략 / 회의 일변 / 분산 8인 라운드 의무
세션 형식: single-session skeptical reviewer — 결정 권한 없음, 권고만.
선행: L579 가 path 7 자동 박탈, "path 1 명확히 안전, 단 (B) Round 11 사전회의 의무" 잠정 결론. 본 L582 는 path 1 도 동등한 압박.

---

## R1 — kinetic energy density 의 외부 framework 위험

회의자: framework 회계 검열관.

kinetic energy density 정의 자체는 단순하지 않다. 비상대론 한계 (½ρv²) 와 상대론 한계 (T^{00} of perfect fluid) 가 다르고, 두 사이를 잇는 path 가 *Special Relativity 의 4-momentum 형식주의* 에 의존. SR 은 SQT 4-pillar (SK, Wetterich, Holographic, Z_2) 어디에도 명시 import 되어 있지 않다. axiom 1 의 scalar number density n(x,t) 와 axiom 2 의 sink term 은 *Galilean-Newtonian* 운동학으로도 일관되게 쓸 수 있고, paper §2 의 continuity equation 도 SR 가정 없이 진술된다.

kinetic ρ 채택 = 다음 중 하나 강제:
- (a) SR 4-momentum 을 axiom 0' 로 silent import → hidden axiom +1
- (b) 비상대론 ½ρv² 한정 → cosmic regime (relativistic radiation, Λ vacuum) 정합 즉시 붕괴
- (c) general T_{μν} 의 timelike 성분 → GR import → hidden framework +1 (path 5 ADM 와 같은 비용)

L575 §1 의 "A 비용 = 2 (frame 선택 + rest mass 처리)" 는 SR/GR import 비용을 누락한 회계. 실제는 **A ≥ 3** (frame + rest 처리 + 운동학 framework).

**판정 R1**: SR 또는 GR 의 silent import 없이는 kinetic ρ 가 3-regime universal 정의 불가. 외부 framework 위험은 path 7 의 causal-set import 와 동급, *낮음* 평가는 과소평가.

## R2 — axiom 2 자연 확장 vs 변경

회의자: axiom 텍스트 변경 검열관.

paper/02_sqmh_axioms.md L7: "spacetime quanta with individual rest mass μ. The product nμ has..." — 명시적으로 **rest mass μ**. axiom 2 의 sink term ρ_m 는 macroscopic mass density 이지만, axiom 1 가 *rest mass* 단위에 의존하므로 ρ 의 어휘론적 jurisdiction 은 rest mass 영역.

path 1 의 kinetic ρ 채택 = axiom 2 의 ρ 를 axiom 1 의 μ (rest mass) 와 *일관성 없게* 정의. 두 옵션:
- (i) axiom 1 의 μ 를 kinetic mass 로 동시 재정의 → axiom 1 본문 수정, 단어 수준 변경 아님
- (ii) axiom 1 rest, axiom 2 kinetic 으로 분리 → 두 axiom 사이 dimensional 결합부 (n₀μ = ρ_Planck/(4π)) 의 의미 붕괴

L579 가 path 7 에 대해 "axiom 1 본문 수정 = [최우선-1] 영역 진입" 으로 박탈했다. path 1 은 axiom 2 만 손대는 것처럼 보이지만 실제로는 axiom 1 의 μ 정의도 동시 수정 강제 → 동일한 위반 영역.

**판정 R2**: path 1 도 axiom 1 본문에 손이 닿는다. "axiom 2 의 단어 수준 명시" 라는 reframing 은 자기기만. path 7 와 동일 박탈 트리거.

## R3 — Higgs sector 우회 진정성

회의자: zero-parameter slogan 검열관.

kinetic energy = (γ-1)mc² (상대론) 또는 ½mv² (비상대론). 양쪽 다 **rest mass m 이 명시적으로 등장**. Higgs sector 가 결정하는 양은 m 자체 (Yukawa·v_H) 이므로, kinetic energy density ρ_kin = Σ_i n_i (γ_i - 1) m_i c² 의 m_i 안에 13 Yukawa DOF 가 *그대로 살아 있다*.

L575 §1 의 "B 회수 R3 (QCD/Higgs 모호) 해소" 는 잘못. kinetic 으로 바꾸면 Higgs 가 사라지는 것이 아니라 *추가* 자유도 (속도 분포 v_i, occupation n_i) 가 더해진다. 회피가 아니라 *증식*. proton 의 kinetic energy 는 99% QCD binding + 1% Yukawa 구성도 *그대로 잔존* (m_proton 자체에 들어 있음).

L574 가 옵션 (A) 를 +10 으로 거부한 핵심은 13 Yukawa DOF — kinetic 재정의는 이 13 을 0 으로 만들지 않는다.

**판정 R3**: Higgs disclosure 의무 100% 잔존. path 7 의 R3 판정 ("한 단계 깊이 숨김") 보다 더 직접적인 노출 — kinetic ρ 정의식에 m 이 드러나 있다. 회피 효과 0.

## R4 — 3-regime universality

회의자: regime universality 검열관.

세 regime 의 운동학 상태:
- galactic: 비상대론 (v << c). kinetic ≈ ½ρv². rest mass 가 dominant 에너지.
- cluster: 부분 상대론 (galaxy peculiar velocity ~ 10⁻³c). kinetic 작은 보정.
- cosmic: relativistic radiation (T^{00}_γ = ρ_γc²) + Λ (kinetic 정의 자체 부적합 — vacuum 은 운동 없음).

galactic regime: kinetic ρ ≈ ρ_rest · v²/2c² ≈ 10⁻⁶ × ρ_rest. 즉 mass-action sink 의 ρ_kin = 10⁻⁶ × ρ_total → σ 가 10⁶ 배 커야 같은 sink rate. 그러면 cosmic regime 에서 sink rate 폭주.

cosmic regime: Λ 의 kinetic energy density = 0 (정의상). path 1 채택 시 dark energy 의 self-coupling 이 0 → axiom 2 sink term 의 우주론적 한계 자체가 무의미해짐.

비상대론 한계에서 kinetic mass ≈ rest mass *동치* 라는 일반적 직관은 **틀렸다**: 동치는 *총 에너지* (rest+kinetic) 한계이지 *kinetic 만* 의 한계가 아니다. galactic 에서 kinetic 만 쓰면 6 자릿수 부족.

**판정 R4**: 3-regime universality 자동 *파괴*. L575 가 "B 회수 R5 부분 해소" 라 본 것은 정반대 — path 1 은 R5 universality 를 즉각 깬다. 이 한 축만으로도 자동 박탈 후보.

## R5 — 관측 anchor cross-check

회의자: cross-anchor 정합 검열관.

세 anchor 의 운동학 상태:
- RAR (a₀ ≈ 1.2×10⁻¹⁰ m/s²): SPARC galactic baryon, **비상대론**. kinetic ρ ≈ 10⁻⁶ × M_*/L 기반 mass density
- BBN (η_b ≈ 6×10⁻¹⁰): 우주 z~10⁹, T~10⁹ K, baryon kinetic ≈ kT, **부분 상대론**. kinetic/rest ≈ 10⁻³
- Cassini (|γ-1|<2.3×10⁻⁵): Solar system, Sun **비상대론** (내부 thermal kinetic ~ 10⁻⁶ × M_⊙)

세 anchor 의 kinetic/rest ratio 가 **각각 다른 자릿수**. 단일 σ 가 세 anchor 모두 정합하려면 σ 가 anchor 별로 4~6 자릿수 다른 값 필요 → σ = 4πG·t_P universality 즉시 위반. 또는 anchor 별 hidden mapping 상수 3 개 (각 anchor 의 v² 분포) → hidden DOF +3.

L579 R5 (path 7) 는 "cross-anchor 검증 부재" 였다. path 1 은 *부재* 가 아니라 *명시적 불일치 예측*. 더 나쁘다.

**판정 R5**: kinetic ρ 는 cross-anchor σ universality 를 산술적으로 깬다. silent assumption 이 아니라 명시적 충돌. [자동 박탈 사유 후보 1].

## R6 — kinetic ρ 측정 가능성

회의자: 관측 가능성 검열관.

kinetic energy density 의 직접 측정:
- 천체물리: 직접 측정 불가. mass density 측정 (luminous, dynamical, lensing) 후 velocity dispersion 곱해서 *추론*
- velocity dispersion 측정 자체가 mass 를 거침 (virial theorem, Doppler line width × stellar mass)
- 즉 ρ_kin 측정 path = ρ_rest 측정 → v 측정 → 곱. **모든 측정 channel 이 rest mass 를 거친다**

path 7 의 valence 가 *원리상* 측정 불가능했던 것 (R6 박탈) 에 비해 path 1 은 측정 가능하지만 **항상 rest mass 측정의 후속**. 즉 kinetic ρ 는 독립 관측량이 아니라 ρ_rest × ⟨v²/c²⟩ 의 derived quantity. axiom 2 ρ 를 derived quantity 로 정의하면 axiom 의 자율성 자체가 깨진다 (axiom 은 primary 가 아니라 derived 가 됨).

**판정 R6**: 측정 path 가 Higgs sector 경유 (rest mass) → R3 의 "회피 효과 0" 을 측정 채널에서 재확인. path 7 R6 와 다른 형태이지만 동일 결론: 회수된 DOF 는 형식적.

## R7 — 4-pillar 정합

회의자: pillar 충돌 검열관.

- **SK (Sakharov)** / σ = 4πG·t_P: t_P 는 ℏ/(m_P c²) 의 형태 — m_P 는 *Planck rest mass*. σ 정의에 rest mass 가 명시. axiom 2 ρ 만 kinetic 으로 바꾸면 sink term 의 σρ 결합에서 두 mass 정의가 *섞임* (σ 분모 rest, ρ kinetic). 차원 일관성은 살아도 *물리적 의미* 가 분열.
- **Wetterich**: quintessence scalar 의 kinetic + potential 분리는 Lagrangian 에서 자연. 그러나 axiom 2 의 ρ_m sink 는 matter density (입자 다체) — Wetterich kinetic term 과 path 1 kinetic ρ 는 *서로 다른 kinetic*. 두 kinetic 어휘 충돌 시 paper §3 (Wetterich 정합 논의) 전면 재작성 필요.
- **Holographic** σ scaling: holographic bound 은 *총 에너지* 기반 (Bekenstein, t'Hooft-Susskind). kinetic 만 쓰면 holographic saturation 조건이 다른 자릿수 → 4-pillar 중 holographic 부적합.
- **Z_2 대칭**: kinetic energy 는 v² 짝수, Z_2 자동 정합. 이 한 pillar 만 OK.

4 pillar 중 3 (SK/Wetterich/Holographic) 와 정합 의문. CLAUDE.md 규약상 1 pillar 충돌 = 자동 박탈 후보. path 7 는 2 pillar 충돌 risk (R7) 였다. path 1 은 **3 pillar**.

**판정 R7**: 4-pillar 정합 더 나쁨. [자동 박탈 사유 후보 2].

## R8 — Round 11 의무

회의자: 절차 준수 검열관.

L575 §3 가 path 1 도 "frame (CMB rest frame) 을 axiom 0 으로 명시화" 권한 활용을 언급. 이는 axiom set 에 *새 axiom* 추가 — 단어 수준 정의 명시 아니라 신규 axiom 도입. [최우선-1] "단어 수준" 의 어휘 jurisdiction 명백 초과.

또한 R2 결론 (axiom 1 의 μ 도 동시 수정 강제) 는 axiom 1 본문 수정. L579 가 path 7 에 대해 동일 사유로 (B) 권고 / (C) 박탈 후보로 둔 것과 동일 적용 의무.

본 L582 는 single-session reviewer — Round 11 권고만 가능, 결정 권한 없음. 분산 8인 라운드 (각 reviewer 가 kinetic ρ 의 4-pillar 재도출 + 3-regime cross-check 독립 시도) 가 절대 의무. *수식 0줄, 유도 경로 0건*.

**판정 R8**: 절차상 Round 11 사전회의 의무. 본 세션 단독 결정 금지.

---

## §최종판정

**(C) 자동 박탈** (트리거: R3 회피 효과 0, R4 3-regime universality 산술 파괴, R5 cross-anchor 4~6 자릿수 불일치, R7 4-pillar 중 3 충돌 — 4개 트리거 중복 발동)

부판정: 만약 (C) 를 보류하고 절차상 진행을 강행한다면 **(B) Round 11 사전회의 의무** — 본 세션은 채택 결정 권한 없으며 사전회의 없이 (A) 직진 절대 금지. 권고하지 않음.

(A) Round 11 본회의 직접 등재는 강하게 비권고. R4/R5 의 산술 충돌만으로도 SQMH 의 σ universality slogan 과 직접 충돌 — falsifiability 가 아니라 *이미 falsified*.

---

## §Path 7 박탈 후 Path 1 가 진정 잔존 path 인가

**아니다 — path 1 도 박탈 권고. mass redef 의 7 path 모두 폐기.**

L579 표 (path 1 vs path 7 비교) 에서 path 1 우월 항목들의 본 회의적 재검토:

| 축 | L579 의 path 1 평가 | L582 재평가 |
|---|---|---|
| 외부 framework import | 없음 | SR/GR silent import (R1) — path 7 와 동급 |
| axiom 1 ontology 변경 | 없음 ("n 의 해석만") | μ rest mass 와 충돌 → axiom 1 본문 수정 강제 (R2) |
| Higgs 13 DOF 처리 | mapping 층 잔존 | kinetic 정의식에 m 명시 — 잔존 정도 *더 직접* (R3) |
| 3-regime universality | 가정 잔존 | 산술적 파괴 (10⁶ 부족, R4) — 잔존이 아니라 *깨짐* |
| 측정 가능성 | 운동에너지 측정 가능 | 항상 rest mass 측정 후속 (R6) — 독립 관측량 아님 |
| 4-pillar 정합 | scalar field 유지로 자동 | SK/Wetterich/Holographic 3 충돌 (R7) — path 7 보다 *나쁨* |
| [최우선-1] 위반 risk | 낮음 | axiom 1 본문 수정 강제, frame axiom 추가 → 중간~높음 (R2/R8) |

**L575/L579 의 path 1 우월 평가는 본 회의적 재검토 후 *전면 역전*.** path 1 은 path 7 보다 더 많은 박탈 트리거 (4 vs 3) 발동.

mass redefinition 7 path 평가 (회의적 재집계):
- path 1: 본 L582 → 박탈 권고 (4 트리거)
- path 2 (Higgs 내부 도출): L575 자체 폐기 (+12)
- path 3 (dark-only): L575 net 0~+1, [최우선-1] 중간 risk
- path 4 (Planck normalize): L575 net 0, dimensional 복원 자유도 hidden
- path 5 (ADM/Komar): L575 net +1, FLRW 부적합
- path 6 (Nambu-Goto): L575 net +2, framework lock-in 권고 안 함
- path 7: L579 박탈 권고 (3 트리거)

Top-2 (path 1, path 7) 모두 박탈 권고. 차순위 (path 4, path 3) 는 net 0~+1 — Higgs 13 DOF 흡수 비용 (옵션 A 의 +10) 보다 작지만 *zero-parameter slogan* 회복 분량 (목표 net ≤ -1) 미달.

**잠정 결론**: mass redef 으로 13 DOF 회피 시도는 7 path 어느 것도 net 음수 회복 불가. **mass redef 영구 종결** 권고. paper §6 limitations 의 13 DOF disclosure 유지가 가장 정직한 대응 (L574 옵션 C 의 어휘 명시판).

단 본 결론은 single-session reviewer 의견. 분산 8인 Round 11 사전회의의 독립 합의 없이는 mass redef 영구 종결 결정 권한 없음.

---

## §정직 한 줄

본 L582 single-session reviewer 의 회의적 검증은 path 1 의 자동 박탈 트리거 4 개 (R3/R4/R5/R7) 식별까지가 정합 범위. L575/L579 의 "path 1 명확히 안전" 평가가 본 재검토 후 역전된 것은 회의적 압박 강도의 차이이며, 어느 쪽이 옳은지의 최종 판정은 분산 8인 Round 11 사전회의의 독립 합의 의무. 본 세션은 권고만 가능.
