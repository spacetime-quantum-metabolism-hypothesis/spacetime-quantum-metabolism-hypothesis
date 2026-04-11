# base_2.md — SQMH 최종 결론 (Path F)

> base.md 원본 가설서의 정정·철회·유보 통합본. Phase 1–4 결과 기반 최종 결론만.
> 마지막 갱신: 2026-04-10.

---

## 0. 최종 판정

**Path F (No-Go).** 배경 수준 SQMH coupled quintessence (`V_mass`/`V_RP`/`V_exp`
+ universal β)는 DESI DR2 BAO + DESY5 SN + compressed Planck CMB + RSD
(N=1853) 에 대해 4-gate Decision 전부 실패. 네거티브 결과 논문
(`paper/negative_result.md`) 으로 마무리.

| Gate | 기준 | 결과 |
|---|---|---|
| D1.1 ΔAIC ≤ −6 | CPL −9.43 ✓ / V_RP +4.22 ✗ / V_exp +4.54 ✗ | 부분 |
| D1.2 ΔBIC ≤ 0 | CPL +1.62 ✗ / V_RP +15.27 ✗ / V_exp +15.59 ✗ | **전부 실패** |
| D1.3 Cassini `|γ−1| < 2.3e−5` | Vainshtein 하 1.75e−10 ✓ | 조건부 PASS |
| D1.4 r_d within 3σ Planck | LCDM 2.63σ / **V_RP 3.13σ ✗** / V_exp 2.82σ | V_RP 실패 |

AND gate: **fail → No-Go**.

---

## 1. base.md 원문에 대한 정정표

| 원본 주장 (base.md) | 상태 | 최종 결론 |
|---|---|---|
| §IV 자유 매개변수 0개 | **조건부 철회** | `ξ`는 무자유. `V(φ)` family 선택은 이론적 자유도. `V_mass`/`V_RP`/`V_exp` family 내부 자유도 1~2개. |
| §XV #6 `w_a < 0` 예측 | **철회** | `V_mass` 선도차수 2체 결합은 `w_a > 0` 만 산출. `V_exp` (forward-shooting, λ>0.3) 는 `w_a < 0` 구조적으로 가능하나, joint data 에서 λ≈0.155 로 LCDM limit 수렴. SQMH 고유 예측으로 제시 불가. |
| §XVI Cassini 자동 통과 | **유보 → 조건부 복원** | Unscreened β=0.107 → `|γ−1|=2.26e−2` (Cassini 984× 위반). Cubic Galileon `K(X)=X+γX²/M⁴`, `M⁴~M_Pl²H_0²` 가정 시 r_V(Sun)=124 pc, Cassini 8AU 에서 억제 1.75e−10 → 10⁷ 여유 PASS. 단 nonlinear kinetic term 은 base.md §4.1 에 없으며 GFT-level derivation 필요. |
| H_0 tension 완화 | **악화** | `V_RP` best-fit h=0.6717 vs LCDM 0.6781 → SH0ES(0.7304)와 더 멀어짐. 완화 효과 없음. |
| §X.5 `r_d ≈ 149.8 Mpc` 필요 | **재진술** | r_d 자유 MCMC 에서 세 family 모두 r_d ≈ 148.6 Mpc 로 수렴. Planck 147.09±0.30 대비 **V_RP 3.13σ TENSION**, LCDM/V_exp 경계선. |
| §IV universal `ξφT^α_α` coupling | **L2 재설계 필수** | Universal coupling 은 Cassini 984× 자동 위반. Sector-selective dark-only (C10k) 또는 disformal `g̃=Ag+B∂φ∂φ` (C11D) 만 C1–C4 통과. 단 C10k 는 S_8 tension 악화(+6.6 χ²). |
| §X.5 `ξ_q > 0` BAO 정합성 | **유지** | BAO-only 영역에서 성립. joint fit 에서는 β, n, λ 모두 LCDM 경계로 수렴. |
| §II 공리, §III–VI 이론 구조, §V 5개 프로그램 연결, §VII 대칭, §X.1–3 타임라인 | **유지** | 수정 불필요. 이론 유산으로 방어 가능. |

---

## 2. 최종 수치 (N=1853, emcee MCMC, seed 42)

### 2.1 r_d 고정 (EH98)

| Model | Ω_m | h | β | 2nd | χ²_min | ΔAIC | ΔBIC |
|---|---|---|---|---|---|---|---|
| LCDM (k=4) | 0.3129±0.003 | 0.6781±0.002 | — | — | 1683.11 | 0 | 0 |
| V_RP (k=6) | 0.3222±0.004 | 0.6717±0.004 | 0.107±0.05 | n=0.096±0.04 | 1681.73 | +2.62 | +13.67 |
| V_exp (k=6) | 0.3224±0.004 | 0.6712±0.004 | 0.102±0.05 | λ=0.090±0.04 | 1681.81 | +2.71 | +13.76 |

### 2.2 r_d 자유 (flat prior [130, 165] Mpc)

| Model | r_d [Mpc] | Δ vs Planck 147.09±0.30 | χ²_min | ΔAIC | ΔBIC |
|---|---|---|---|---|---|
| LCDM (k=5) | 148.69 +0.53/−0.49 | +2.63σ (PASS) | 1666.78 | 0 | 0 |
| **V_RP** (k=7) | 148.62 +0.34/−0.39 | **+3.13σ (FAIL)** | 1667.00 | +4.22 | +15.27 |
| V_exp (k=7) | 148.56 +0.42/−0.41 | +2.82σ (PASS) | 1667.32 | +4.54 | +15.59 |

r_d 자유화 효과: Δχ² ≈ −16 (LCDM). 데이터가 Planck 보다 ~1.5 Mpc 높은 r_d 선호.

### 2.3 CPL Fisher forecast 상한 (w0, wa marginalised)

(Om, h, ω_b) marginalised 최적점 `(w0*, wa*) = (−0.8646, −0.9822)`.
- Δχ²_min = −13.43
- ΔAIC = −9.43 ✓ (D1.1)
- ΔBIC = +1.62 ✗ (D1.2)
- DESI headline `(−0.757, −0.83)` 에서 Δχ² = +26.16 (우리 dataset 은 DESI headline 비선호)

### 2.4 k-essence forward shooting (exp-V)

| λ | w0 | wa | Ω_φ(0) |
|---|---|---|---|
| 0.30 | −0.987 | −0.018 | 0.685 |
| 0.50 | −0.964 | −0.051 | 0.685 |
| 1.00 | −0.850 | −0.210 | 0.685 |
| 1.50 | −0.634 | −0.487 | 0.685 |

λ>0.3 → w_a<0 구조적 허용. DESI headline 재현에는 λ≈1.5 필요하나 joint MCMC 는 λ≈0.155 로 수렴.

---

## 3. 이론 경로 판정

| 경로 | 상태 |
|---|---|
| A. Ratra-Peebles `V(φ)` | **기각** (BIC very strong) |
| B. Axion-like oscillating | 보류, 우선순위 낮음 |
| C. Linear IDE (`Q∝ρ_DE`) | **금지** (SQMH 2체 반응 충돌) |
| D. Kinetic dominance | 보류, 단독 불충분 |
| E. Backreaction/비균질성 | **폐기** (효과 O(10⁻⁵)) |
| F. 반증 인정 | **채택** |

남은 이론 경로 (모두 Phase 4 이상, 본 논문 범위 밖):
- Perturbation-level `ξφT^α_α` 재유도 (GFT matching, linear 섭동 G_eff/c_s²/anisotropic stress)
- 비-tracker `w(z)` effective Lagrangian
- L2 sector-selective (C10k) 또는 disformal (C11D) 재설계

---

## 4. Caveat (Phase 4 에서 해소 예정)

1. Compressed CMB (θ*, ω_b, ω_c) 만 사용. Planck full TT/EE/lensing 미사용.
2. r_d 는 EH98 fit (Boltzmann 대비 ~1% bias).
3. 성장 ODE 배경은 LCDM 해석식 대체 (coupled backward ODE `φ_N→√6` 폭주 회피). `φ_N` slow-roll `≈ √(2/3)·β·Ω_m(a)` 사용, `|β|<0.4` 에서 factor ~2.
4. 고z bridge (z>2.5) 는 pure LCDM tail, rescale 금지.
5. BOSS DR12 RSD off-diagonal ρ=(0.24, 0.10, 0.26) 근사.
6. Fluid IDE 는 Phase 3 MCMC 제외 (Phase 2 에서 `ξ_q=0` 경계 수렴).
7. 20 walkers × 800 steps, 1σ tail 정확도 부족.

---

## 5. 산출물 포인터

| 파일 | 역할 |
|---|---|
| `simulations/quintessence.py` | Amendola coupled quintessence 배경 ODE |
| `simulations/desi_fitting.py` | BAO 13pt + V(φ) 3종, β≥0 강제 |
| `simulations/phase2/*.py` | joint χ² (BAO+SN+CMB+RSD) |
| `simulations/phase3/mcmc_phase3.py` | 6D/4D MCMC (r_d 고정) |
| `simulations/phase3/mcmc_rdfree.py` | 7D/5D MCMC (r_d 자유) |
| `simulations/phase3/r_d_tension.md` | A3 tension 수치 |
| `simulations/screening.py` | Cassini/LLR/MICROSCOPE likelihood |
| `simulations/vainshtein.py` | cubic Galileon r_V 계산 |
| `simulations/kessence.py` | k-essence `L₂` forward shooting (CLW variables) |
| `simulations/phase4/fisher_kessence.py` | CPL Fisher |
| `paper/negative_result.md` | 네거티브 결과 논문 draft (8 섹션, ~330 lines) |
| `figures/11_desi_dr2_fit.png` | Phase 1 BAO-only |
| `figures/12_phase2_joint.png` | Phase 2 joint |
| `figures/13_phase3_mcmc.png` | Phase 3 V_RP 6D corner |
| `figures/14_phase3_vexp.png` | V_exp corner |
| `figures/14_cassini.png` | Vainshtein pass/fail |

공식 데이터 출처:
- DESI DR2 BAO 13pt + cov: arXiv:2503.14738 (github.com/CobayaSampler/bao_data)
- DESY5 SN: Vincenzi 2024 (github.com/CobayaSampler/sn_data/DESY5, zHD 규약)
- Planck θ*, ω_b, ω_c: arXiv:1807.06209 Table 2
- RSD fσ_8 8pt: Beutler+2012, Howlett+2015, Alam+2017, Bautista/de Mattia/Hou+2021

---

## 6. 한 줄 요약

> 배경 + sub-horizon SQMH (`ξφT^α_α`, `V(φ)`=RP/exp/mass) 는 DESI DR2 + DESY5
> + compressed Planck + RSD 에 대해 4-gate Decision 전부 실패. `w_a<0` 예측
> 철회, Cassini 자동 통과 철회 (Vainshtein 조건부 복원), H_0 tension 악화,
> `V_RP` r_d 3.13σ TENSION. Path F 선언, 네거티브 결과 논문으로 마무리.
> L2 sector-selective/disformal 재설계는 Phase 5 에서 재시도.

---

## 7. Alt-20 현상론 확장 — 참고 기록 (중요도 낮음)

> 이 섹션은 L5 Phase B 에서 탐색한 20개 closed-form ρ_DE(a) 변형 중
> 상위 4개 후보의 MCMC 결과를 보관한다.
> **이론적 도출 근거 없음. SQMH 예측으로 인용 금지.**
> DESI DR3 비교 참고용으로만 보존.

### 7.1 배경: Alt-20 구조

모든 Alt-20 후보의 형태:

```
ρ_DE(a) = ΩΛ × f(a; Ωm)
```

진짜 SQMH ODE를 적분하는 것이 아니라, ODE 해의
1차 근사(A01) 또는 다른 수학 함수 형태(A02~A20)를
ρ_DE에 직접 대입한 closed-form 근사.

amplitude = Ωm으로 고정 (Amplitude Locking).
자유 파라미터: (Ωm, h) 만. 모델 고유 파라미터 없음.

### 7.2 상위 4개 MCMC 결과 (DESI DR2 + DESY5 + CMB + RSD, N=1853)

| 모델 | 형태 f(a, m) | chi² | Δchi² vs ΛCDM | SQMH 도출 가능 여부 |
|---|---|---|---|---|
| ΛCDM (기준) | 1.0 | 1676.89 | 0 | — |
| **A01** (순수 SQMH) | 1 + m×(1−a) | 1655.78 | **−21.12** | ✓ ODE 1차 근사 |
| A17 (단열 펄스) | 1 + m×(1−a)×exp(−(1−a)²) | 1655.64 | −21.26 | ✗ |
| A12 (erf 확산) | 1 + erf(m×(1−a)) | 1655.28 | −21.62 | ✗ NF-14 위반 |
| A05 (sqrt 이완) | sqrt(1+2m×(1−a)) | 1655.87 | −21.03 | ✗ |

MCMC 수렴: 48 walkers × 2000 steps, R̂ < 1.02 (K13 PASS).

### 7.3 핵심 관찰

**A01과 A12의 chi² 차이: 0.50**

→ 통계적으로 구분 불가 수준.
→ A01(순수 SQMH 이론)이 A12(erf 현상론)와 실질적으로 동등한 DESI 설명력 보유.

**모든 후보가 ΛCDM보다 Δchi²≈21 개선.**

→ 개선의 원인: SQMH 구조 (Ωm으로 진폭 고정된 ρ_DE 진화)
→ 특정 함수 형태(erf vs 선형 vs sqrt)에 크게 의존하지 않음.

### 7.4 NF-14: erf 불가능 정리

A12의 erf 형태는 SQMH ODE에서 이론적으로 도출 불가.

- SQMH = 이류(advection): ∂n/∂t + ∇·(nv) = 소스
- erf = 확산(diffusion): ∂n/∂t = D∇²n 의 해

구조적으로 다른 방정식. "stochastic SQMH" 동기부여는 있으나
NF-14에 의해 정식 도출 경로 닫힘.

### 7.5 논문 기재 방침

- **본문**: A01 (순수 SQMH, 이론 직접 도출) 만 주요 결과로 기재
- **부록**: "20개 closed-form 변형 중 선형~erf 범위에서 Δchi²≈21 일관 달성"
  → 결과의 robust성 근거로만 인용
- **A12를 SQMH 예측으로 호칭 금지**

### 7.6 파일 포인터

| 파일 | 내용 |
|---|---|
| `simulations/l4_alt/runner.py` | Alt-20 전체 20개 정의 (ALT dict) |
| `simulations/l5/A01/mcmc_production.json` | A01 MCMC 결과 (R̂=1.008) |
| `simulations/l5/A12/mcmc_production.json` | A12 MCMC 결과 (R̂=1.010) |
| `simulations/l5/A05/mcmc_production.json` | A05 MCMC 결과 |
| `simulations/l5/A17/mcmc_production.json` | A17 MCMC 결과 |
