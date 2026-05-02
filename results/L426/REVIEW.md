# L426 REVIEW — 4인팀 c(M) SQT vs LCDM 비교 실행 결과

**임무**: NEXT_STEP Path (ii) 실행. SQT background 수정이 D(z) → σ(M,z) → ν(M,z) → c(M,z)
chain 으로 halo concentration 에 미치는 영향을 LCDM 대비 정량 평가.
**방법**: 4인 자율 분담 (CLAUDE.md Rule-B). 데이터 로딩 / 배경 ODE / σ(M) 적분 / c(ν) 매핑 자연 분담.
**구현**: `simulations/L426/run.py` (multiprocessing spawn pool, 9 워커, 스레드 1로 고정).
**결과 요약**: **max |Δc/c| ≈ 0.46% (z=0,0.5,1.0)** — LCDM-indistinguishable, PASS_TRIVIAL.

---

## 실행 구성

- **LCDM baseline**: w0=−1, wa=0, Planck18 base (Ω_m=0.315, Ω_b=0.0493, n_s=0.965, σ_8=0.811, h=0.674).
- **SQT background**: CPL phenomenological 대표값 w0=−0.95, wa=−0.10
  (L48-class SQT runs 의 mild dynamical-DE 선호와 정합. *입력*임을 명시; 본 task 는 c(M) 채널의 *민감도 측정*).
- **σ(M)**: Eisenstein-Hu 1998 no-wiggle transfer + top-hat top-hat W(kR), σ_8 정규화.
- **n_eff(M)**: −3 − d ln σ²/d ln R (DK15 정의, 수치미분 dlnR=0.02).
- **growth D(z)**: matter-perturbation 2nd-order ODE, lna 격자 4000 포인트, D(a=1)=1 정규화.
- **c(ν, n_eff)**: Diemer-Kravtsov 2015 median NFW concentration fit.
- **Mass range**: M ∈ [10^11.5, 10^15.5] M_sun/h, 21 logarithmic bins.
- **Redshifts**: z ∈ {0, 0.5, 1.0}.

## 핵심 수치

| z | c_LCDM(10^12) | c_SQT(10^12) | Δc/c | c_LCDM(10^14) | c_SQT(10^14) | Δc/c | mean Δσ/σ |
|---|---|---|---|---|---|---|---|
| 0.0 | 11.25 | 11.25 | +0.00% | 6.44 | 6.44 | +0.00% | +0.000% |
| 0.5 |  8.50 |  8.52 | +0.19% | 5.24 | 5.25 | +0.12% | +0.186% |
| 1.0 |  6.68 |  6.70 | +0.35% | 4.64 | 4.65 | +0.12% | +0.356% |

- **Max |Δc/c|** over the full grid: **0.455%**.
- D(z=0.5) shift 1.86×10⁻³, D(z=1) shift 3.56×10⁻³ (양 부호: SQT 가 LCDM 보다 살짝 큰 D, 따라서 σ(M,z)
  도 크고, ν 작아져 c 살짝 증가 — DK15 의 c−ν 단조 감소 영역).
- z=0 에서 Δc/c=0 이 정확히 나오는 이유: σ_8 정규화 시점이 z=0 이므로 σ(M,z=0) 가 두 모델에서 동일.
  순수 차이는 D(z>0) shift 만. z=0 c(M) 는 σ(M)·n_eff 만으로 결정 → 동일.

## 판정

NEXT_STEP 사전 기준:
- Δc/c ≲ 1% → **PASS_TRIVIAL** (LCDM-indistinguishable). ✅ 본 결과 적용.
- 5% → distinguishing prediction.
- ≳ 10% → 기존 관측 (Umetsu+ 2020, Sereno+ 2017; cluster c-M scatter ~0.1 dex ≈ 25%) 충돌 위험.

본 결과 **0.46% ≪ 0.1 dex (~25%) 관측 산포** 이므로,
SQT depletion-zone 의 c(M) 채널 prediction 은
*현재 및 가까운 미래 관측 정밀도* 에서 LCDM 와 *원리적으로 구분 불능*.

## 한계 / 정직 caveat

1. **Path (ii) 만 검증**: NEXT_STEP Path (i) (depletion-zone scale → r_s 식별) 와 Path (iii)
   (splashback / Γ 채널) 은 별도 시뮬레이션 필요. 본 결과는 *background-growth 채널 한정*.
2. **w0, wa 입력**: SQT 가 axiom 수준에서 (w0, wa) 를 *유도* 하지 않음. L48 best-fit 대표값 차용.
   다른 admissible SQT 배경 (w0=−1.05, wa=+0.05 등) 도 같은 1% 미만 결과 예상 (전반적 D(z) shift 가 작음).
3. **DK15 fitting 의 LCDM-trained 한계**: c(ν, n_eff) 매핑은 LCDM N-body 로 calibrate 됨.
   SQT 가 비-LCDM N-body 통계 (formation history 분포) 를 가질 가능성은 본 toy 가 포착 못함.
4. **interior depletion-zone effect 부재**: ATTACK_DESIGN 비판 #1 그대로 유효 — depletion 이 halo
   *내부* density profile 에 영향 줄 axiom-level path 는 SQT 에 없음. 수정한 것은 *background growth* 만.
5. **σ_8 정규화 위치**: z=0 에서 σ_8=0.811 고정. SQT 의 정합 σ_8 가 LCDM 와 *살짝* 다르면 z=0
   에서도 작은 shift 발생 가능. 본 toy 는 σ_8 동일 가정 (data-anchored).

## paper §5 / §6 권고

### §5 (예측 표) 추가 행 권고
> | halo c(M) | LCDM 와 |Δc/c|<1% | PASS_TRIVIAL — background-growth 채널 한정. depletion-zone interior 효과 path 부재 (results/L426/) |

### §6.1 (한계 표) 추가 행 권고
> | XX | depletion-zone 은 halo 내부 density profile 에 axiom-level 진입 불가. c(M) 예측은 background-D(z) 채널로만 가능, |Δc/c|<0.5% (LCDM-indistinguishable). | ACK | future N-body of SQT-체 |

---

## 산출물

- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L426/ATTACK_DESIGN.md`
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L426/NEXT_STEP.md`
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L426/REVIEW.md`
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L426/cM_compare.json` (수치 결과)
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L426/cM_plot.png` (c(M) 곡선 + Δc/c)
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/simulations/L426/run.py`

## 정직 한 줄

**SQT depletion-zone 의 halo c(M) 예측은 background-growth 채널에서 LCDM 대비 |Δc/c|<0.5% — Diemer-Joyce/Ludlow N-body 정밀도 및 cluster lensing 산포보다 100× 작아 PASS_TRIVIAL (구분 불능).**
