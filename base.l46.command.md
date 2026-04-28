# L46 Command: 3-Axiom SQT + A3 4-State Full Exploration

## 배경
L45에서 Model UB (2공리 A1+A2) ΔAICc=-55 vs ΛCDM 달성. 그러나 그래프 분석 결과:
- UB 변종들 w₀, wa 방향이 Son et al. CPL과 반대
- 사실상 "ΛCDM + 약한 phantom 섭동" 수준
- 진짜 부활 아님, 부분 개선

사용자 새 통찰: SQT는 3공리 체계여야 함:
- **A1**: 물질 닿으면 ψ 소멸 (유지)
- **A2**: 우주 내부 모든 곳에서 ψ 생성 (재정의)
- **A3**: 경계에서 ψ 이벤트 (유입/유출)

A3 4 상태: Influx / Outflux / Bidirectional / Switch

L46은 3공리 체계 + A3 4 상태 + L45 축 전체 조합으로 Son et al. 방향 정합 모델 탐색.
18-27시간 철저 실행.

## 이론 핵심

### 공리 (3개)

**A1**: 물질과 닿으면 ψ 소멸 → Γ_A1 = σ · ρ_m · ψ

**A2**: 우주 내부 모든 곳에서 ψ 생성 + 팽창 희석
```
dψ/dt|_A2 = κ_2 - 3H·ψ
```
(팽창 희석 필수 포함)

**A3**: 경계에서 ψ 이벤트 (외부 우주 교환)
```
Γ_A3(t) = 3·[J+(t) - J-(t)] / R(t)
```

**완전 ODE**:
```
dψ/dt = κ_2 - 3Hψ - σρ_m·ψ + 3[J+(t) - J-(t)]/R(t)
```

**ρ_DE 정의**:
```
ρ_DE(z) = α · <ψ>_path(z)  [or <ψ>_vol]
```
α는 관측 정규화 (OL0).

## 테스트 축 전체 (8축)

| 축 | 옵션 |
|---|---|
| A3 시간 의존 | Const, Decay, HProp, Tanh |
| A3 부호 | I, O, B+, B- |
| 경계 | H (Hubble), P (Particle), E (Event) |
| 공간 전파 | BAL, FIC, DEC |
| 공간 평균 | PATH, VOL, HYB |
| ρ_DE 결합 | LIN, POW, MIX, LOG |
| A2 팽창 처리 | Dil, NoDil |
| 초기 조건 | Zero (ψ=0 at z_max) |

## Tier 1: 32 핵심 모델

고정 축: 경계=H, 전파=BAL, 평균=PATH, 결합=LIN, 초기=Zero

| # | 이름 | a3_time | a3_sign | J+ | J- | k | A2 |
|---|---|---|---|---|---|---|---|
| 1 | M-CI.Dil | Const | I | J_0 | 0 | 3 | Dil |
| 2 | M-CI.NoDil | Const | I | J_0 | 0 | 3 | NoDil |
| 3 | M-CO.Dil | Const | O | 0 | J_0 | 3 | Dil |
| 4 | M-CO.NoDil | Const | O | 0 | J_0 | 3 | NoDil |
| 5 | M-CBp.Dil | Const | B+ | J_0 | eps*J_0 | 4 | Dil |
| 6 | M-CBp.NoDil | Const | B+ | J_0 | eps*J_0 | 4 | NoDil |
| 7 | M-CBm.Dil | Const | B- | eps*J_0 | J_0 | 4 | Dil |
| 8 | M-CBm.NoDil | Const | B- | eps*J_0 | J_0 | 4 | NoDil |
| 9 | M-DI.Dil | Decay | I | J_0·e^{-t/τ} | 0 | 4 | Dil |
| 10 | M-DI.NoDil | Decay | I | J_0·e^{-t/τ} | 0 | 4 | NoDil |
| 11 | M-DO.Dil | Decay | O | 0 | J_0·e^{-t/τ} | 4 | Dil |
| 12 | M-DO.NoDil | Decay | O | 0 | J_0·e^{-t/τ} | 4 | NoDil |
| 13 | M-DB.Dil | Decay | B | J_0·e^{-t/τ} | J_0·(1-e^{-t/τ}) | 5 | Dil |
| 14 | M-DB.NoDil | Decay | B | J_0·e^{-t/τ} | J_0·(1-e^{-t/τ}) | 5 | NoDil |
| 15 | M-DS.Dil | Decay | S | J_0·(1-e^{-t/τ}) | J_0·e^{-t/τ} | 5 | Dil |
| 16 | M-DS.NoDil | Decay | S | J_0·(1-e^{-t/τ}) | J_0·e^{-t/τ} | 5 | NoDil |
| 17 | M-HI.Dil | HProp | I | J_0·H/H_0 | 0 | 3 | Dil |
| 18 | M-HI.NoDil | HProp | I | J_0·H/H_0 | 0 | 3 | NoDil |
| 19 | M-HO.Dil | HProp | O | 0 | J_0·H/H_0 | 3 | Dil |
| 20 | M-HO.NoDil | HProp | O | 0 | J_0·H/H_0 | 3 | NoDil |
| 21 | M-HB.Dil | HProp | B | J_0·H/H_0 | eps·J_0·H/H_0 | 4 | Dil |
| 22 | M-HB.NoDil | HProp | B | J_0·H/H_0 | eps·J_0·H/H_0 | 4 | NoDil |
| 23 | M-TIO.Dil | Tanh | IO | — | — | 5 | Dil |
| 24 | M-TIO.NoDil | Tanh | IO | — | — | 5 | NoDil |
| 25 | M-TOI.Dil | Tanh | OI | — | — | 5 | Dil |
| 26 | M-TOI.NoDil | Tanh | OI | — | — | 5 | NoDil |
| 27 | M-TIF.Dil | Tanh | IF | — | — | 5 | Dil |
| 28 | M-TIF.NoDil | Tanh | IF | — | — | 5 | NoDil |
| 29 | M-TOF.Dil | Tanh | OF | — | — | 5 | Dil |
| 30 | M-TOF.NoDil | Tanh | OF | — | — | 5 | NoDil |
| 31 | M-A2Only.Dil | — | A2Only | 0 | 0 | 2 | Dil |
| 32 | M-A2Only.NoDil | — | A2Only | 0 | 0 | 2 | NoDil |

### Tanh net flux 정의
- IO: j_net = J_0·tanh((t̃-t̃_0)/τ̃)
- OI: j_net = -J_0·tanh((t̃-t̃_0)/τ̃)
- IF: j_net = J_0·(1+tanh((t̃-t̃_0)/τ̃))/2
- OF: j_net = -J_0·(1-tanh((t̃-t̃_0)/τ̃))/2

### 자유 매개변수 범위
- Om ∈ [0.15, 0.50]
- H0 ∈ [55, 80]
- J_0 ∈ [0, 5]
- τ̃ = H₀τ ∈ [0.05, 5.0]
- t̃_0 ∈ [0, 1.5] (fraction of t̃_today)
- eps ∈ [0, 0.98]

### ODE → z domain (κ_2=1, σ=0 흡수)

Dil: ψ(z) = ∫_z^{z_max} (1+z')²·[1+3·j_eff(z')]/E(z') dz' / (1+z)³

NoDil: ψ(z) = ∫_z^{z_max} [1+3·j_eff(z')] / [(1+z')·E(z')] dz'

ρ_DE(z) = OL0 · ψ(z)/ψ(0)  [LIN coupling, Tier 1]

## Tier 2: 45 모델 (Tier 1 Top-5 × 9 축 변화)

각 Top-5에 대해 9 변종 (30 starts 각):
1. bnd: H → P (particle horizon)
2. bnd: H → E (event horizon)
3. prop: BAL → FIC
4. prop: BAL → DEC
5. avg: PATH → VOL
6. avg: PATH → HYB
7. cpl: LIN → POW (+ n_pow free, k+1)
8. cpl: LIN → MIX (+ eps_mix free, k+1)
9. cpl: LIN → LOG (+ beta_log free, k+1)

prop 변화시 mR 자유 파라미터 추가 (k+1).

## Tier 3: 20 모델 (Tier 2 Top-5 × 4 결합)

결합 축 전체: LIN, POW, MIX, LOG × Top-5 = 20 모델 (20 starts 각)

## Pre-Task (5개)

PT1: ODE 수치 안정성 — 수렴 확인 (rtol=1e-8)
PT2: BBN 안전 (z=10⁹) — ρ_DE/ρ_total < 10⁻⁵
PT3: 재결합 안전 (z=1090) — ρ_DE/ρ_crit < 10⁻³
PT4: 현재 정규화 (z=0) — E(0)=1, ρ_DE(0)=OL0 ± 0.1%
PT5: 미래 거동 (z→-0.99) — 유한성 확인

## 판정 기준 (4중 조건)

| 등급 | 조건 |
|---|---|
| Q95 VICTORY | ΔAICc<-50, w₀∈[-0.5,-0.2], wa∈[-2.5,-1.0], q₀>0, k≤4 |
| Q94 STRONG | ΔAICc<-30, w₀ or wa Son+25 2σ 이내, k≤5 |
| Q93 PARTIAL | ΔAICc<-15, 방향 정합 (부호) |
| Q92 WEAK | ΔAICc<0, 방향 일부 정합 |
| Q91 MARGINAL | ΔAICc≈0 (±5) |
| K90 FAIL | ΔAICc≥5 |
| K91 WRONG | ΔAICc<0 but 방향 반대 (L45 UB 같은 경우) |
| K92 INVALID | 경계 도달, 수치 문제 |

Son+25 기준: w₀=-0.34 ± 0.12 (2σ), wa=-1.9 ± 0.5 (2σ), q₀>0

## 실행 계획

- Tier 1: 32 × 30 = 960 fits
- Tier 2: 45 × 20 = 900 fits
- Tier 3: 20 × 20 = 400 fits
- Bootstrap Top-10: 10 × 200 = 2000 fits
- 총: ~4260 fits
- 예상 실행 시간: 18-27시간

## 인프라

- 8-worker spawn Pool
- Son et al. 2025 age-bias 보정 (L43 검증)
- L43/L45 LCDM 기준: AICc=1759.93
- L45 UB 최우수 기준: dAICc=-55.49
