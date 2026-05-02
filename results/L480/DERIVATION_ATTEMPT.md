# L480 — Derivation Attempt: Matter–DE Crossover (deepening L466)

> **Status: derivation *attempt*, not a derivation.** Sections 1–3 follow
> from explicit field-theory ansätze; section 4 is an honest naturalness
> audit and section 5 is the cluster-scale numerical check. Where the
> derivation fails I say so.

정직 한 줄: **B/A = Ω_m/Ω_Λ 는 가정이 아니라 정의 — 우주 평균에서 σ_eff=0
을 *강제*하면 자동으로 따라온다. 따라서 "추가 free parameter 1개" 가 아니라
"closure condition 1개" 다. 그러나 이 closure 는 cluster-scale crossover
를 *trivialise* 한다 (NFW+2-halo 에서 r* 가 사라짐). 자연성 점수: 부분적.**

---

## 1. Lagrangian-level sketch for axiom 1 (absorption) + axiom 3 (generation)

SQMH 의 두 source 는 단일 metabolism scalar χ (the "lattice quantum count
density") 의 연속방정식

```
∇_μ J^μ_χ  =  Γ_abs(x)  −  Γ_gen(x)
```

으로 표현된다. 가장 단순한 (가장 일반적이면서 EFT 차원이 가장 낮은) 결합은

```
L_int  =  −α χ^2 T^μ_μ^(matter)   (axiom 1)
        −β χ^2 ρ_Λ                (axiom 3)
```

여기서 T^μ_μ^(matter) ≈ −ρ_m (비상대론적 더스트 한도), ρ_Λ 는 진공 에너지
밀도. χ 가 (linearly response field) 로 적분되면 source rate 는

```
Γ_abs  =  α' · ρ_m,         Γ_gen  =  β' · ρ_Λ.
```

(α', β' 는 χ 정상상태 응답에서 α, β 와 χ_eq 로 묶임 — 이번 단계에서 두 결합
상수의 *비율* 만 관측 가능.)

따라서 net source 는

```
σ_eff(x)  =  Γ_abs − Γ_gen  =  A · ρ_m(x)  −  B · ρ_Λ,        A := α',  B := β'.
```

이것이 L466 의 phenomenological 출발점에 해당하는 *Lagrangian-level* 동기다.

### 1.1 무엇이 *진짜* 도출되었나

- 선형 항 `A ρ_m − B ρ_Λ` 형태: ✅ EFT 최저 차원 결합에서 자동.
- A, B 부호 (둘 다 양수): ✅ axiom 1 은 흡수 (positive loss), axiom 3 는
  생성 (positive source) → 적분하면 둘 다 양 결합.
- A, B 절대값: ❌ Lagrangian 만으로는 결정 안 됨 — UV 결합 (α, β) 와 χ_eq
  값에 묶임.
- 비율 B/A: ❌ Lagrangian 에서 자유. **다음 절의 closure 가 필요.**

### 1.2 무엇이 *도출되지 않았나*

- 비선형 항 (예: ρ_m^2, ρ_m·ρ_Λ): EFT 차원으로 가능하지만 본 toy 에서는
  무시 (다음 라운드 과제).
- 시간 의존: ρ_Λ ≈ const 가정. 만약 ρ_Λ 가 진정한 진공이 아니라 동역학적
  암흑에너지라면 B(z) 시간 의존 등장.

---

## 2. Closure condition: B/A = Ω_m / Ω_Λ?

### 2.1 어디서 오는가

L466 의 제안: 우주 평균에서 net source = 0 (background steady state).

```
<σ_eff>  =  A·<ρ_m> − B·ρ_Λ  =  A·Ω_m·ρ_crit − B·Ω_Λ·ρ_crit  =  0
        ⇒   B/A  =  Ω_m / Ω_Λ  ≈  0.460.
```

이 한 줄로 자유 parameter 가 사라진다. **단, 가정 1 개 추가:** "우주적
평균 metabolism 은 정확히 정상상태" — 이것이 이론적 *공리* 인지 (예: SQMH
가 처음부터 평균 정상상태를 요구하는 구조), 아니면 *fitting* 인지가 핵심.

### 2.2 정직 평가: 1개 free parameter 추가 vs 자연

| 입장 | 주장 | 평가 |
|---|---|---|
| 자연 (closure) | "우주 평균 정상상태" 는 SQMH 의 추가 공리이며 이로부터 B/A 가 *유도됨* | 가정을 한 단계 더 깊게 미는 것 (parameter → axiom). technically zero free parameter, but morally one extra assumption. |
| 자유 (1 param) | B/A 는 두 결합 비율이고 데이터로 결정 | 정직하지만 예측력 낮음. |

**본 보고서의 입장: 자연-1/2.** Closure 는 free parameter 를 0 개로
줄이지만, 그 *비용* 으로 새 공리 ("cosmic-mean steady state") 를 도입한다.
순 정보량은 보존된다 (Occam-neutral).

---

## 3. Cancellation 반경의 클러스터 스케일 emergence

### 3.1 NFW (1-halo) 단독의 경우

Without 2-halo floor: ρ_m(r)/ρ_crit,0 단조 감소 → 0. 따라서 σ_eff=0 의 해
는 *항상* 어떤 r 에서 존재. closure 값 BA=0.46 → r*/r_vir 는 NFW 한정으로
잘 정의됨. cluster outskirt scale 자연 emergence 에 해당.

### 3.2 NFW + 2-halo floor (cosmic mean) 의 경우

ρ_m 는 r→∞ 에서 0 이 아니라 Ω_m·ρ_crit,0 로 floor 됨. 그러면

```
σ_eff  =  ρ_m(r) − (Ω_m/Ω_Λ)·ρ_Λ
       =  ρ_m(r) − Ω_m·ρ_crit
       ≥  0   for all r   (등호는 r→∞).
```

**즉 closure B/A=0.46 에서는 cancellation 반경이 r→∞ 로 밀려 사라진다.**
이는 산출물 (`scan_results.json`) 에서 직접 확인:

- BA = 0.46 (closure): r*/r_vir = `null` (해 없음, 모든 c 에서 동일).
- BA = 0.5: r*/r_vir = 13.5 (이미 cluster 너머 LSS 영역).
- BA = 0.7: r*/r_vir = 7.4 (splashback 외곽).
- **BA = 1.0: r*/r_vir = 5.6 (cluster outskirt — L466 결과 재현).**
- BA = 2.0: r*/r_vir = 3.9.

### 3.3 해석

L466 의 "B/A=1 → cluster 외곽" 은 NFW 단독 (또는 매우 약한 floor) 가정의
산물이었다. 우주적 평균을 진지하게 더하면 closure 값 (0.46) 은 **cancellation
없음** 으로 흐른다. Cluster outskirt cancellation 은 BA ~ 1 영역 (closure
와 다름!) 에서만 자연.

따라서:

- **closure 자연성** (B/A 자유도 제거) ↔ **cluster crossover 존재** 는
  *상호 배타*. 둘 다 가질 수 없다.
- L466 의 "natural B/A=O(1) → cluster 외곽 자연" 그림은 closure 미도입
  한정으로만 성립.

### 3.4 Cluster-scale invariance (mass dependence)

BA=1 에서 M_vir 를 1e13 → 1e15 M_⊙ 로 스캔 (산출물 참고): r*/r_vir = 5.60
**모든 질량에서 동일** (rho_m/ρ_crit,0 는 r/r_vir 의 함수이며 ρ_crit,0 는
보편 상수이므로). 물리 단위로는 r* = 2.55 → 11.84 Mpc 로 r_vir ∝ M^{1/3}
스케일링. 이는 stacked cluster outskirt 분석의 자연 스케일과 일치.

또한 농도 c ∈ [3, 10] 변화에서 BA=1 r*/r_vir 는 5.0–6.5 사이 (별도 항목
요약). c-의존성 약함 → 실제 cluster ensemble 에서도 robust.

---

## 4. B/A 자연성 정량 audit

### 4.1 log-grid 측도

`scan_results.json -> fraction_of_log_BA_grid_giving_r_star_in_outskirt_band_1_to_10_rvir = 0.502`.

즉 B/A 를 10^{-2} ~ 10^{1.5} 범위에서 log-uniform 으로 잡으면 *절반* 의
경우 cancellation 이 cluster outskirt 에 떨어진다. "운 좋은 fine-tuning" 은
아니지만, "공짜로 cluster 가 튀어나온다" 도 아님. 상한 BA ≈ 0.46 (closure
경계) 미만에서는 해 없음, BA ≳ 0.46 에서만 cluster 영역에 등장.

### 4.2 결론 표

| 질문 | 답 |
|---|---|
| Lagrangian level 동기 (선형, A>0, B>0)? | ✅ |
| B/A 절대값을 이론에서 예측? | ❌ |
| Closure (Ω_m/Ω_Λ) 가 자유도 제거? | △ (공리 1개와 거래) |
| Closure 값에서 cluster crossover 존재? | ❌ (NFW+2-halo floor) |
| Cluster outskirt crossover 의 자연 영역? | BA ≈ 0.7 ~ 2 |
| Cluster mass invariance? | ✅ (r/r_vir 보편) |

---

## 5. 최종 정직 한 줄

**B/A 는 Lagrangian 에서 자유다. 우주적 정상상태 closure 로 0 free
parameter 처럼 만들 수 있지만, 그 closure 자체가 cluster 외곽 cancellation
을 무력화한다. L466 의 "자연 cluster dip" 은 BA ≈ 1 의 별도 가정에서만
성립하며, 이는 closure 와 양립하지 않는다.**

## 6. Outputs (이 라운드)

- `results/L480/scan_results.json` — B/A grid scan + cluster mass scan + c sensitivity
- `results/L480/ba_curve.npz` — dense B/A → r*(B/A) curve
- `simulations/L480/run.py` — 재현용 스크립트

## 7. Next (만약 계속한다면)

- 비선형 결합 (`A·ρ_m^α − B·ρ_Λ^β`) 추가: closure 경계가 sharp 해질 가능성.
- ρ_Λ 시간 의존 (quintessence): closure → time-dependent B/A → high-z
  proto-cluster 에서 dip 위치 이동 예측 (관측가능한 falsifier).
- "cluster dip" 의 관측 채널 확정 (splashback ρ_gas, RSD 잔차, lensing
  amplitude 잔차) — 어느 채널이 σ_eff(r) 에 가장 직접 결합하는지 modelling 필요.
