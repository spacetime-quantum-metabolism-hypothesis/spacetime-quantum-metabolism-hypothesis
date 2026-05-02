# L466 — Free Speculation: Cluster Dip from matter–Λ Crossover Cancellation

> **Status: speculation only.** No derivation, no parameter fixing. Just a sketch
> consistent with axioms 1 (absorption) + 3 (generation) and the empirical "cluster
> dip" observed in earlier L-series scans. Numbers below come from a toy NFW
> profile in `simulations/L466/run.py`, *not* from theory.

한 줄: 클러스터 평균 밀도가 ρ_Λ 와 같은 자릿수라 흡수와 생성이 부분 상쇄될 수 있다.

---

## 1. Picture

SQMH 의 두 source:

- **axiom 1 (absorption)** — 시공간 격자가 물질 근방에서 양자를 *흡수*. 비율은
  *환경 의존*: 국소 물질 밀도 ρ_m(x) 에 (단조) 의존. 텅 빈 보이드에서는 거의 0,
  깊은 핵심 클러스터에서는 발화.
- **axiom 3 (generation)** — 양자 *생성* 은 진공/Λ 항이 담당. 우주적으로 거의
  *균일* (ρ_Λ ≈ const, 시간 의존만 약함). 환경에 둔감.

대사율 (metabolism rate) 의 부호 있는 net source:

```
sigma_eff(x)  =  sigma_abs(ρ_m(x))  −  sigma_gen(ρ_Λ)
```

선형화하면

```
sigma_eff(x)  ≈  A · ρ_m(x)  −  B · ρ_Λ.
```

A, B 는 두 공리의 결합 상수 (이번 추측에서 자유). 비율 B/A 만 물리적.

## 2. Why a *cluster* dip?

ρ_m(x) 의 두 극한:

| region | ρ_m(x) / ρ_crit,0 | sigma_eff |
|---|---|---|
| void | ≪ Ω_m ≈ 0.3 | 음 (생성 우세) |
| 클러스터 코어 (r ≪ r_vir) | 10²–10⁴ | 양 (흡수 우세) |
| **클러스터 외곽 / splashback / 1→2 halo 전이** | **~ Ω_Λ ≈ 0.7** | **≈ 0 (cancellation)** |

이 마지막 줄이 핵심. NFW + 200 평균 과밀도 정규화로 toy 를 풀면:

- B/A = 1 → 상쇄 반경 r/r_vir ≈ **4.5** (rho_m/rho_crit ≈ 0.685)
- B/A = 0.5 → 5.7
- B/A = 2.0 → 3.6
- B/A = 5.0 → 2.6

즉 **자연스러운 결합 (B/A 가 O(1))** 이면 cancellation 은
"클러스터 안" 이 아니라 **클러스터 외곽 / 2-halo 전이** 에서 일어난다.
이는 stacked cluster + outskirt 분석 (R_p ~ 수 Mpc, r/r_vir ~ 1–10) 에서
대사 신호가 유난히 약해지거나 부호 반전될 가능성을 시사한다.

## 3. Why not other density regimes?

- **Voids**: ρ_m ≪ ρ_Λ → sigma_eff ≈ −B ρ_Λ 일정 음. dip 아니라 *균일 생성 floor*.
- **Field galaxy, halo (ρ_m ~ 50–200 ρ_crit)**: sigma_eff ≫ 0. 흡수 압도, 생성
  무시 가능. dip 없음.
- **Cluster outskirt (ρ_m ~ 0.5–2 ρ_crit)**: 두 항이 동급. **유일한 cancellation
  band.**
- **우주 평균 (ρ_m → Ω_m·ρ_crit ≈ 0.315)**: B/A ≈ Ω_m/Ω_Λ ≈ 0.46 일 때 정확히
  "background null" — 우주 평균에서 net source = 0. 이는 SQMH 의 평균 정상상태
  (steady-state 해석) 와 일치하는 매력적 정합 조건.

## 4. Tightening — what would a derivation look like?

추측 단계에서 멈추되, 다음 방향만 명시:

1. **결합 상수 비** B/A 를 자유 파라미터가 아니라 background steady state
   `<sigma_eff> = 0` 조건으로 묶기 → B/A = Ω_m / Ω_Λ ≈ 0.46.
   그러면 cancellation 반경은 `rho_m(r) = Ω_m · ρ_crit,0`, 즉 **정확히 우주
   평균 밀도** 가 되는 곳. NFW 에서 r/r_vir ≈ 6–7 (2-halo 영역).
2. **environment-dependent vs uniform** 비대칭이 본질. 흡수가 ρ_m 에
   비선형 (예: ρ_m^α) 이면 cancellation band 는 더 좁아져 sharper dip.
3. **시간 의존**: ρ_Λ 는 effectively const 이지만 ρ_m(z) 가 (1+z)³ 로 뜸 →
   고-z 에서는 cancellation 조건이 *cluster 안쪽* 으로 이동. observable:
   high-z proto-cluster 에서는 dip 위치가 안쪽 r_vir.

## 5. Caveats / falsification handles

- B/A ratio 는 free; 우주적 steady-state 조건으로만 묶임. independent
  로 측정할 길 없으면 결정성 없음.
- 선형 추가 `A ρ_m − B ρ_Λ` 자체가 가정. SQMH 의 absorption/generation 이
  실제로 ρ 에 어떤 함수 형태인지 (예: ρ²·t_P², √(ρ·ρ_Λ)) 는 미지.
- "cluster dip" 의 관측적 정의가 필요. 어떤 신호 (RSD, cluster lensing
  amplitude, splashback 강도, ICM scaling) 의 어떤 잔차에서 dip 인지 명시 후
  toy 를 정량 데이터에 매핑.
- 4·π·G·t_P (SI) 단위계 정합성 점검 미수행. dimensional check 는 다음 단계.

## 6. Outputs

- toy curve: `simulations/L466/run.py` → `results/L466/toy_curve.npz`
- 수치 요약: `results/L466/toy_results.json`
- **B/A = 1, NFW c=5: dip 반경 r/r_vir ≈ 4.5; ρ_m/ρ_crit ≈ 0.685 ≈ Ω_Λ.**

## 7. Next (if pursued)

L467+: stack cluster outskirt 의 어떤 SQMH observable 이 r/r_vir ≈ 5 근방에서
부호 반전을 보이는지 specific 데이터 채널 (ACT-DR6 lensing, DESI cluster
RSD, eROSITA cluster-WL stacks) 로 매핑. observable 을 먼저 합의하고,
그 후에 함수형/계수를 정량화.
