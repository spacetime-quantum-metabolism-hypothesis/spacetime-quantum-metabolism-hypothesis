# L382 REVIEW — SK Wightman propagator W_+, W_- explicit (n field, thermal eq.)

**Date**: 2026-05-01
**Lineage**: L382 독립 미시 deepening. SK 형식 위 자유 n 장의 평형 Wightman 함수 정착.

> 정직 한 줄: 본 결과는 자유 스칼라의 잘 알려진 평형 Wightman 함수를 SQMH n 장 표기로 재정리한 것이며, 새로운 물리 예측은 없다. 검증 K1 (analytical KMS) PASS, K2 (positivity) PASS, K4 (numerical KMS far-from-pole) 는 Lorentzian regulator 꼬리에 의한 알려진 실패 — 물리 무효화 아님.

---

## 1. 정의 (SQMH 표기)

n(x) 는 SQMH 의 (선형화된) 대사 밀도 요동 장. 본 세션은 자유 한도 (vertex 무시) 에서 평형 (T = 1/β) 두-점 함수를 다룬다.

Schwinger-Keldysh 윤곽: forward (+) 가지 와 backward (−) 가지. 두 가지 분기 사이의 물리적 양자 평균이 Wightman:

- W_+(x, x') ≡ ⟨n(x) n(x')⟩
- W_-(x, x') ≡ ⟨n(x') n(x)⟩

평형 + 시간 병진 + 공간 병진 → 푸리에 공간에서 ω, k 함수.

분광함수 (spectral function):
ρ(ω, k) ≡ W_+(ω, k) − W_-(ω, k).

## 2. 자유 한도에서의 명시적 형태

분산 ω_k = √(k² + m²), Bose-Einstein 점유 n_B(ω_k) = 1/(e^{βω_k} − 1).

자유 실수 스칼라 (Le Bellac, Thermal Field Theory; Kapusta-Gale §3) 에서:

W_+(ω, k) = 2π [ (1 + n_B(ω_k)) δ(ω − ω_k) + n_B(ω_k) δ(ω + ω_k) ]
W_-(ω, k) = 2π [ n_B(ω_k) δ(ω − ω_k) + (1 + n_B(ω_k)) δ(ω + ω_k) ]
ρ(ω, k)   = 2π [ δ(ω − ω_k) − δ(ω + ω_k) ] · sgn(ω)

각 δ 는 양자 단일 입자/단일 정공 분기의 on-shell 지지를 의미한다.

### 2.1 KMS 관계

양 ω-축 양 (positive-frequency) 분기에서:
W_+ / W_- = (1 + n_B) / n_B = e^{βω_k}.

음 ω-축에서는:
W_+ / W_- = n_B / (1 + n_B) = e^{−βω_k} = e^{βω}|_{ω=−ω_k}.

따라서 두 분기를 종합해 KMS:
**W_+(ω, k) = e^{βω} W_-(ω, k)**
가 양 분기에서 정확히 성립.

### 2.2 분광함수 양수성

ω > 0 에서 ρ ≥ 0, ω < 0 에서 ρ ≤ 0 이므로 sgn(ω)·ρ(ω) ≥ 0. 즉 ρ 는 보즈 측면 정당 분광 함수.

### 2.3 FDR 와의 연결 (preview, L383+)

흩어진 응답함수 G_R = (Re G_F) − i (sgn(ω)/2) ρ 와의 관계로부터 요동-소산 정리:
W_+(ω) + W_-(ω) = (1 + 2 n_B(ω)) ρ(ω) = coth(βω/2) ρ(ω).

본 세션에서는 W_+, W_- 도출까지만. coth FDR 의 SQMH 응용은 후속.

---

## 3. 수치 검증 (simulations/L382/run.py)

격자: β ∈ {0.5, 1.0, 2.0}, m ∈ {0, 0.3, 1.0}, k ∈ {0, 0.5}. δ(ω ∓ ω_k) → Lorentzian (η = 1e-3 또는 5e-3) 으로 정칙화.

### 3.1 K1 — analytical KMS (delta-limit, exact at pole)

각 (β, m, k) 격자에서 W_+/W_- 의 극에서 비율을 정확히 계산:
**max |((1+n_B)/n_B) − e^{βω_k}| / e^{βω_k} = 1.35e−16** (machine zero).
→ **K1 PASS**.

### 3.2 K2 — positivity of sgn(ω)·ρ

모든 격자 점에서 min sgn(ω)·ρ(ω) = 0 (정확히 영, 두 Lorentzian 차에서 음 구역 없음).
→ **K2 PASS**.

### 3.3 K3 — realness

1+1D 자유 자기-사례 (real scalar) 의 ω-공간 Wightman 은 실수. 본 시뮬레이션은 실수 산술만 사용하므로 trivially PASS.
→ **K3 PASS**.

### 3.4 K4 — numerical KMS away from pole (regulator-limited)

W_+(ω)/W_-(ω) 와 e^{βω} 비교를 모든 ω 격자에서 시도하면 max relative residual 이 β = 2 case 에서 약 2e4 까지 폭주. 이는 **Lorentzian 꼬리** 효과: pole 에서 멀어지면 W_± 가 둘 다 1/((ω∓ω_k)² + η²) ~ 1/ω² 처럼 행동해 비율이 1 에 가까워지지만 e^{βω} 는 폭증. δ-한도에서 비율 자체가 정의되지 않는 영역이므로 물리 위반이 아니다.
→ **K4 FAIL (regulator-limited, not physical)**. delta-limit (K1) 이 진정한 KMS 검증임.

## 4. 게이트 종합

| 게이트 | 내용 | 결과 |
|---|---|---|
| K1 | Analytical KMS at pole, all (β,m,k) | PASS (1.3e−16) |
| K2 | sgn(ω)·ρ ≥ 0 | PASS (0.0) |
| K3 | Realness | PASS |
| K4 | Numerical KMS far from pole | FAIL (regulator artifact) |

물리적 결론: KMS, positivity, realness 모두 자유 한도에서 정확히 성립. K4 는 Lorentzian 꼬리에 따른 알려진 인공물.

## 5. 산출물

- 본 파일 (`results/L382/REVIEW.md`)
- 그림: `results/L382/wightman_kms.png` (4-panel: W_±, ρ, KMS log-비교, β-dependence residual)
- 데이터: `results/L382/L382_summary.json`
- 코드: `simulations/L382/run.py`

## 6. 한계 및 다음 단계

- **자유 한도 한정**. SQMH 의 n³ vertex (소멸 항 J_q 미시 origin) 에 따른 self-energy Σ(ω, k) → finite-width quasi-particle / NLO Wightman 은 후속 세션 (L383+).
- **평형 한정**. Keldysh rotation (G_R, G_A 분리) 와 비평형 Kadanoff-Baym 으로의 확장은 후속.
- **공간 차원 일반화**. 본 세션은 fixed-k slice. d=3+1 적분 측도와 IR/UV 정칙화는 후속에 명시.
- **SQMH-specific**: SK 윤곽 위 사라짐 항 (J_q) 가 추가될 때 KMS 가 어떻게 깨지는지 (또는 effective β_eff 가 도입되는지) 가 본 인프라 위에서 진행될 정량 질문.

본 세션은 표준 자유-장 Wightman 의 SQMH 표기 정착 + 수치 인프라 구축의 미시 deepening 단계. 이론 신규성은 다음 단계로 이월.
