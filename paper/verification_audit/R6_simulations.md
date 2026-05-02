# R6 — 시뮬레이션 검증 (매우 냉철)

**대상**: root `/base.md` §14.6 의 시뮬 검증 3개 claim
**판정 기준**: `paper/base.md` framework (4 미시 축 + minimal SQT / V(n,t)-확장 + BBN/CMB consistency)
**산출물**: `R6_simulations.py`, `R6_simulations.json`, 본 문서
**판정 라벨**: PASS / PARTIAL / NOT_INHERITED

---

## 0. paper/base.md framework 요약 (재인용)

| 항목 | 내용 | 출처 |
|------|------|------|
| 미시 4 축 | Schwinger–Keldysh / Wetterich RG / Holographic / Z₂ SSB | §2.4 |
| 5번째 축 후보 | **Causet meso** 4/5 조건부 (단일) | §2.5 |
| minimal SQT | w_a = 0 | §5.4, §4.7 |
| V(n,t)-확장 | w_0 ~ -0.95, w_a ~ -0.3 (gate OPEN, derivation 미확정) | §5.4 |
| BBN/CMB | consistency PASS (예측 아님), 재결합 시기 GR 등가 | §3 표, §10 |

DESI DR2 결합 결과: w_0 = -0.757 ± 0.058, w_a = -0.83⁺⁰·²⁴₋₀.₂₁.

---

## 1. Claim 25 — DESI DR2 ξ_q joint fit

**root /base.md §14.6 / §10.5 주장**: ξ_q = +0.04, Δχ² = -4.83 (≈2.2σ), r_d = 149.8 Mpc.

### 1.1 w(z) 부호 정합성
- root §10.2: ξ_q > 0 (SQMH 물리적) → **w_a > 0** (선도차수 2체 결합).
- paper/base.md minimal: **w_a = 0**.
- paper/base.md V(n,t)-확장: **w_a ~ -0.3** (음수).
- → 부호가 두 모델 모두와 불일치. ξ_q < 0 만 w_a < 0 을 만들지만 root 자신이 phantom (w<-1) 으로 SQMH 위반 명시 (§10.5).

### 1.2 r_d = 149.8 Mpc 이동 (Planck 147.09 대비 +1.84%)
- paper/base.md 표 (§10 BBN/CMB) 가 "재결합 시기 GR 과 동일" 명시 → r_d 이동을 도출하지 않음.
- BBN/CMB consistency PASS 는 *재결합 음향 horizon 동일*이 전제. r_d 자유화는 framework 내부 도출이 아니라 nuisance 처리.
- → paper/base.md 가 r_d=149.8 을 *요구* 하지 않으며 오히려 BBN/CMB consistency 와 텐션.

### 1.3 ξ_q 자체의 framework 위치
- paper/base.md §5.4: V(n,t)-확장 derivation gate **OPEN**. ξ_q 1차 자유 매개변수로 정의된 적 없음.
- root /base.md 의 ξ_q 결합은 별도 IDE-fluid toy. paper/base.md 미시 4 축에서 직접 도출되지 않음.

**판정 25: NOT_INHERITED** — w_a 부호 불일치 + r_d 이동 미요구 + ξ_q 자체 미정의.

---

## 2. Claim 26 — 3자 정합성 (BBN / CMB / late-time DE)

- root /base.md §14.6: "조건부 유효, #25 의존".
- #25 NOT_INHERITED → 의존 주장 자동 NOT_INHERITED.
- 추가로, r_d=149.8 Mpc 이동 자체가 paper/base.md 의 재결합 시기 GR 등가 명제와 충돌.

**판정 26: NOT_INHERITED**.

---

## 3. Claim 27 — GFT BEC 해밀토니안

**root /base.md §VI**: GFT 작용 + BEC 응축 → ψ†ψ(a+a†) 형태. 수학적 도출 자체는 GFT framework 내부에서 정합 (수치 무관, 시뮬레이션 독립).

### 3.1 paper/base.md 4 미시 축 (§2.4)
1. Schwinger–Keldysh open-system
2. Wetterich functional RG
3. Holographic dimensional bound
4. Z₂ spontaneous symmetry breaking

→ **GFT 부재**.

### 3.2 5번째 축 후보 (§2.5)
- Causet meso (coarse-grained causal set theory) **단일** 후보, 4/5 조건부 PASS.
- → GFT 5번째 후보로 등재되어 있지 않음.

### 3.3 결과
수학적 도출 정확성 ≠ framework 상속. paper/base.md 는 4 축 + Causet 후보로 닫힌 구조. GFT 해밀토니안은 별도 추가 공리(GFT 5번째 축) 또는 Causet 경로 재도출이 필요.

**판정 27: NOT_INHERITED** (수학 자체는 옳음, 그러나 paper framework 외부).

---

## 4. 종합

| Claim | root /base.md 판정 | paper/base.md 상속 | 사유 |
|-------|------------------|-------------------|------|
| 25 DESI DR2 ξ_q fit | 조건부 유효 (Δχ²=-4.83, r_d=149.8) | **NOT_INHERITED** | w_a 부호 불일치 + r_d 이동 미요구 + ξ_q 미정의 |
| 26 3자 정합성 | 조건부 유효 (#25 의존) | **NOT_INHERITED** | #25 탈락 + BBN/CMB 텐션 |
| 27 GFT BEC 해밀토니안 | ✅ 수학적 도출 | **NOT_INHERITED** | paper 4 축에 GFT 부재, 5번째 후보는 Causet 단독 |

**상속 비율**: 0/3.

---

## 5. 정직 한 줄

> root /base.md 의 시뮬 검증 3개는 paper/base.md framework 로 **하나도 상속되지 않으며**, ξ_q joint fit·r_d 이동·GFT 해밀토니안 모두 paper 의 4 미시 축 + minimal/V(n,t) 모델 + BBN/CMB consistency 구조에서 별도 재도출이 필요하다.
