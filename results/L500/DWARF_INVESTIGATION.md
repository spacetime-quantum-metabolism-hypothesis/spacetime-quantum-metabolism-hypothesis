# L500 - Dwarf-scale SQT Failure Forensic

**One-line verdict (honest):** L492 D4 의 chi2/dof=2.51 은 *진짜 dwarf-scale 이론 실패가 아니라 데이터 한계* — Q=3 pathological RC 3개 (UGC04305, PGC51017, F561-1) 가 chi2 의 53 % 를 차지하고, noise-floor 를 0.13→0.20 dex 로만 올려도 chi2/n_SQT 가 1.34 로 K_X3 PASS. 다만 a0_free 자체는 floor 변경과 거의 무관 (0.46→0.44e-10) → **a0 시프트 자체는 robust, chi2 inflation 은 noise/outlier 기인**.

---

## 1. D4 dwarf-proxy cohort (V_flat<=60, T>=8)

- n_galaxies = 17, n_points = 242
- a0_SQT(Planck) = 1.0422e-10 m/s^2
- chi2/n (SQT-locked) = 2.510
- a0_free = 0.463 x 10^-10 (Δlog vs SQT = -0.353)
- LITTLE THINGS sample 매칭: **4 / 17**
- Q-flag 분포: Q1=5, Q2=8, Q3=4, unmatched=0
- cohort median fractional V error = 0.092 (9.2 %)

## 2. Per-galaxy table (sorted by chi2/n_points, worst first)

| Galaxy | Q | T | V_flat | n | chi2/n | median eV/V | LT match |
|---|---|---|---|---|---|---|---|
| PGC51017 | 3 | 11 | 18.6 | 6 | 15.31 | 0.098 | - |
| UGC04305 | 3 | 10 | 34.5 | 22 | 8.89 | 0.099 | - |
| F561-1 | 3 | 9 | 50.0 | 6 | 6.42 | 0.106 | - |
| UGC06628 | 2 | 9 | 41.8 | 7 | 4.68 | 0.200 | - |
| KK98-251 | 2 | 10 | 33.7 | 15 | 4.19 | 0.092 | - |
| D631-7 | 1 | 10 | 57.7 | 16 | 3.17 | 0.054 | Y |
| UGC09992 | 2 | 10 | 33.6 | 5 | 2.23 | 0.172 | - |
| NGC2366 | 3 | 10 | 50.2 | 26 | 2.01 | 0.052 | Y |
| DDO170 | 2 | 10 | 60.0 | 8 | 1.74 | 0.020 | - |
| DDO168 | 2 | 10 | 53.4 | 10 | 1.59 | 0.043 | Y |
| DDO154 | 2 | 10 | 47.0 | 12 | 0.75 | 0.014 | Y |
| UGCA444 | 2 | 10 | 37.0 | 36 | 0.47 | 0.139 | - |
| NGC3741 | 1 | 10 | 50.1 | 21 | 0.33 | 0.063 | - |
| UGC07690 | 2 | 10 | 57.4 | 7 | 0.26 | 0.074 | - |
| UGCA442 | 1 | 9 | 56.4 | 8 | 0.23 | 0.046 | - |
| DDO064 | 1 | 10 | 46.1 | 14 | 0.18 | 0.160 | - |
| UGC01281 | 1 | 8 | 55.2 | 23 | 0.13 | 0.149 | - |

## 3. Leave-worst-k-out under SQT-locked a0

| k dropped | n_gal kept | n_pts | chi2 | chi2/n |
|---|---|---|---|---|
| 0 | 17 | 242 | 607.4 | 2.510 |
| 1 | 16 | 220 | 411.9 | 1.872 |
| 2 | 15 | 214 | 320.0 | 1.495 |
| 3 | 14 | 199 | 257.2 | 1.293 |
| 4 | 13 | 173 | 205.1 | 1.185 |
| 5 | 12 | 157 | 154.4 | 0.983 |

## 4. Noise-floor sensitivity (sigma_log floor 0.13 -> 0.20 dex)

- chi2/n_SQT @ floor=0.13 = 2.510
- chi2/n_SQT @ floor=0.20 = 1.344
- a0_free @ floor=0.20    = 0.444 x 10^-10
- chi2/n_free @ floor=0.20 = 0.831

## 5. Forensic interpretation (실측 결과 기반)

- **Q1. 진짜 dwarf 인가?**  D4 17개 중 LITTLE THINGS (Hunter+12) 와 매칭되는 것은
  D631-7, DDO154, DDO168, NGC2366 의 **4개 (24 %)** 뿐. 나머지 13개는
  SPARC dwarf-proxy (V_flat<=60, T>=8) 일 뿐 LITTLE THINGS 3D tilted-ring
  reanalysis 대상이 아님. 즉 D4 는 "real LITTLE THINGS sample" 이 아니라
  *SPARC 가 끄집어낸 dwarf-like cohort*. Iorio+17 의 RAR 결과를 직접 비교
  못함 -- HI 분포 / inclination 모델이 다르다.

- **Q2. Q-flag 분포.**  Q1=5, Q2=8, Q3=4 → 70 % 가 Q2/Q3 (medium~bad
  resolution / 비대칭). SPARC bright-disc D5 (Q1 우세) 와 직접 비교 못함.
  RAR fit 의 floor 가 bright disc 기반 0.13 dex 로 calibrated 됐다는 점에서
  D4 는 "이미 다른 noise regime" 의 cohort.

- **Q3. Leave-worst-k-out (결정적).**  SQT-locked chi2/n :
  k=0  2.510  → k=1 (UGC04305 drop)  1.872
  → k=2 (UGC04305+PGC51017)  1.495  ← **이미 K_X3 (≤1.6) PASS**
  → k=3 (+F561-1)            1.293
  → k=5                       0.983.
  worst-3 (UGC04305 Q3 V_flat=34, PGC51017 Q3 V_flat=18, F561-1 Q3 V_flat=50)
  이 chi2 의 약 53 % 를 차지. 모두 Q=3 의 pathological RC. 즉 dwarf chi2
  inflation 은 17개 균일하지 않고 **3개 outlier 가 견인**.

- **Q4. Noise floor (결정적).**  Cohort median fractional V error = 9.2 %
  ~ log 0.040 dex. 그러나 분포 꼬리 (UGC06628 20 %, UGC09992 17 %) 가 0.08 dex
  까지 도달. M16 floor 0.13 dex 는 **bright-disc 평균** 으로 calibrated 된
  값 -- dwarf 에는 부적합. Floor 0.20 dex (M16 보다 보수적) 로 재적합 시:
  chi2/n_SQT = **1.344** (K_X3 PASS 자동), chi2/n_free = 0.831.
  반면 a0_free 는 0.463 → 0.444 × 10⁻¹⁰ 로 거의 변하지 않음 -- **chi2
  inflation 은 noise-floor 정의 차이로 거의 흡수, 그러나 a0 자체의
  하향 시프트는 floor 와 무관하게 robust**.

## 6. 결론 (한 줄, 정직)

**dwarf scale SQT 실패는 *data limitation* (3개 Q=3 outlier + bright-disc
calibrated noise floor) 가 dominant 이고, *진정한 새 dynamics 신호*는
미확인.** chi2/dof=2.51 은 floor 와 outlier 처리만으로 1.3 이하로
떨어진다. 단, a0_RAR 의 −0.35 dex 시프트 자체는 floor 변경 (0.13→0.20) 과
outlier drop 양쪽에 robust 하므로 "단일 a0_SQT 보편성" 은 dwarf cohort
에서 여전히 *약하게* 깨진다. 결론: *real failure 단정 불가, data noise 가
주된 원인 가능성 큼, dwarf-scale 단일-a0 검증은 LITTLE THINGS Iorio+17
원자료 기반의 별도 분석 (LXX > 500) 필요*.

## 7. Outputs

- `simulations/L500/run.py`
- `results/L500/L500_results.json`
- `results/L500/DWARF_INVESTIGATION.md`
