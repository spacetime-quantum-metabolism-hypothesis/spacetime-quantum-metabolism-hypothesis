# L337 — ATTACK DESIGN (5 gaps × 4 pillar closure 시도)

## 목표
L330 micro completeness B (~70%) 의 5 잔여 gap 에 대해 4 pillar
(SK + Wetterich RG + Holographic + Z_2) 도구로 *closure 시도*.
각 gap 를 closed / partial / OPEN 으로 분류.

> 본 단계는 **방향 매핑** 이며 수식 유도는 후속 L 단계에서 팀 자율.
> CLAUDE.md 최우선-1/2 준수: 수식·계수 미지정.

## 5 gaps (L330 발췌 + 본 세션 정의)

- **gap_1**: a2 (에너지 보존) micro 기원
- **gap_2**: a3 (cosmic creation Γ_0 magnitude ≈ H_0) micro 기원
- **gap_3**: a4 (emergent metric) micro 기원
- **gap_5**: D5 (Milgrom a_0 = cH_0/(2π)) 의 2π geometric factor 미도출
- **gap_6** (추가): D3 (τ_q time-scale) first-principle 기원
  (gap_5 와 root cause 동일 — *시간 스케일* 의 micro origin)

## Pillar 별 매핑 후보 (방향만)

### Pillar A — Schwinger-Keldysh (L292)
- 제공 가능: real-time response (G_R), fluctuation (G_K), KMS T_eff,
  out-of-eq Keldysh source 구조
- 미제공: 시공간 곡률 emergence, RG flow 계수

### Pillar B — Wetterich Functional RG (L293, L301)
- 제공 가능: 3-regime fixed point 구조 (IR/saddle/UV), β-function,
  scale 의존성 (k → physical scale)
- 미제공: 2-loop coefficients, dimensional pre-factors

### Pillar C — Holographic / area-law (L294)
- 제공 가능: σ_0 ∝ G·t_P 차원 유일성, horizon 4π factor,
  Bekenstein/CKN bound 일관성
- 미제공: bulk dynamics, full Verlinde-style metric reconstruction

### Pillar D — Z_2 spontaneous breaking (L295)
- 제공 가능: ⟨n⟩ 진공 기댓값 scale, domain-wall surface tension dilution,
  Goldstone/pseudo-Goldstone 채널
- 미제공: 비평형 wall network 통계, exact tension coefficient

## Gap × Pillar 공격 매트릭스

| gap | 1차 pillar | 보조 pillar | 공격 노선 (방향) | 예상 등급 |
|---|---|---|---|---|
| gap_1 (a2 energy cons.) | SK | Z_2 | KMS 구조 + 시간 평행이동 Noether 채널 결합 | partial |
| gap_2 (a3 Γ_0 ≈ H_0) | RG | SK | IR fixed point scale 매칭 + Keldysh source 정상 흐름 | partial |
| gap_3 (a4 emergent metric) | Holo | Z_2 | area-law backbone + Goldstone 모드의 graviton 매핑 | OPEN |
| gap_5 (D5 2π factor) | Holo | RG | causal patch ring topology vs horizon disk (2π vs 4π 인자 비율) | partial |
| gap_6 (D3 τ_q origin) | RG | Holo | UV→IR flow time vs horizon crossing time 매칭 | partial |

## 1차 closure 가설 (8인 팀 도출 대상, 본 문서는 *방향 명명*만)

- **gap_1**: SK contour 의 KMS 조건은 시간 평행이동 invariance 의 결과 →
  열적 ensemble 에서 a2 가 *axiom 이 아닌 정리* 로 강등될 가능성.
  단, 비평형 (Γ_0 ≠ 0) 영역에서는 broken — partial closure.

- **gap_2**: RG IR fixed point 에서 σ_cosmic 이 정의되며,
  Γ_0 는 Keldysh source 로 IR FP 의 dissipation rate 에 매핑.
  scale 매칭 (k_IR ↔ H_0) 가 자연스럽다면 partial.
  단, 매칭의 *uniqueness* 가 미해결.

- **gap_3**: Holographic area-law 가 G 의 차원을 고정하나,
  metric *자체* 가 emergent 한다는 구조적 도출은
  현재 4 pillar 모두 부족. Verlinde-style entropic gravity
  또는 tensor network 채널이 필요 — 본 4 pillar 만으로는 OPEN.

- **gap_5**: Milgrom 의 a_0 = c·H_0/(2π) 의 2π 는
  causal patch 의 *원주* (1D ring) vs horizon area 의 *면적* (2D disk)
  factor ratio 와 정합 가능. Holo 의 4π (sphere area) → 2π (great circle)
  reduction 이 RG saddle FP 와 매칭되면 partial.

- **gap_6**: τ_q 는 RG flow time (UV→IR running 의 e-folding 수) 와
  holographic radial coordinate 의 시간 환산을 통해 매핑 시도.
  기본 차원 분석 ( τ_q ~ 1/√(G·n_∞·ε/c²) 류) 은 axiom 순환 위험 →
  pillar 독립 도출 시도 partial.

## 수락 기준 (각 gap)

- **closed**: pillar 도구만으로 axiom 의존 *없이* 도출 + 검산 (수치 자릿수)
- **partial**: 부분 도출 + 잔여 자유 파라미터 1 개 (계수 또는 scale)
- **OPEN**: 4 pillar 만으로 도달 불가, 5번째 채널 필요

## 후속 L 후보

- L338: gap_1 + gap_2 (SK + RG 결합) 집중 도출
- L339: gap_5 + gap_6 (시간 스케일 root cause) 결합 도출
- L340: gap_3 (emergent metric) — Verlinde 또는 tensor network 5번째 pillar 도입
