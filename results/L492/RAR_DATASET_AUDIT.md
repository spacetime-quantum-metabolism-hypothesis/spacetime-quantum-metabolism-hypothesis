# L492 — RAR Cross-Dataset Stability Audit

**Verdict (one line, honest):** RAR `a₀` is **단일 dataset 한정 SQT 일치** — SPARC 175 전체에서만 a₀ ≈ c H₀/(2π) 이고, Q=1 / dwarf / bright 등 모든 부분 표본에서 0.077 ~ 0.353 dex (19 ~ 125 %) 흔들려 K_X1·K_X2·K_X3 모두 FAIL (1/4).

---

## 1. 입력
- 데이터: SPARC 175 (Lelli et al. 2016 AJ 152 157) 회전곡선 + Q/Vflat catalog.
- 함수형: McGaugh 2016 (M16) 만 — L489에서 함수형 의존성은 별도 audit 됨.
- Υ_disk = 0.5, Υ_bul = 0.7 고정 (SPARC convention).
- σ_log floor = 0.13 dex.
- a₀_SQT(Planck H₀=67.4) = 1.0422 × 10⁻¹⁰ m/s².

## 2. Subset 정의

| Key | 정의 | n_galaxies | n_points |
|---|---|---|---|
| D1_full | SPARC 175 전체 (L482 baseline) | 175 | 3389 |
| D2_Q1 | Q=1 high-quality (Lelli+16 best-resolved) | 99 | 2132 |
| D3_Q12 | Q ∈ {1,2}, Q=3 제거 | 163 | 3269 |
| D4_dwarf_LT_proxy | V_flat ≤ 60 km/s **AND** T ≥ 8 (Sdm/Im/BCD) — LITTLE THINGS scale proxy | 17 | 242 |
| D5_bright | V_flat ≥ 150 km/s | 54 | 1605 |

Cluster RAR (Tian-Ko 2016 / Pradel 2014 / Eckert+22) 은 **on-disk 데이터 없음 → 본 audit 에서 재분석 안 함**. 문헌상 a₀_cluster ~ (5–10) × a₀_SPARC (MOND missing-baryon problem). 단일 a₀ 보편성은 cluster scale 에서 구조적으로 실패하며 SQT 도 동일 한계를 공유 — sec. 5 참조.

## 3. Per-subset M16 fit 결과

| Subset | a₀ (×10⁻¹⁰) | σ(log a₀) [stat] | χ²/dof (SQT-locked) | Δlog vs SQT |
|---|---|---|---|---|
| **D1_full** | **1.069** | 0.006 | 1.295 | **+0.011** |
| D2_Q1 | 1.246 | 0.008 | 1.011 | +0.077 |
| D3_Q12 | 1.123 | 0.006 | 1.126 | +0.032 |
| **D4_dwarf_LT_proxy** | **0.463** | 0.024 | **2.510** | **−0.353** |
| D5_bright | 1.256 | 0.010 | 0.856 | +0.081 |

핵심 관찰:
- **D1 의 SQT 일치 (Δlog = +0.011) 는 부분 표본 평균에 대한 우연**. D2 (high-quality Q=1, McGaugh 의 원래 cut 과 가장 가까움) 은 a₀ = 1.25 × 10⁻¹⁰ 로 McGaugh 1.20 쪽으로 회귀 → SQT 와 0.077 dex (19%) 차이.
- **D4 (dwarf, LITTLE THINGS scale)** 가 가장 큰 외부값: a₀ = 0.46 × 10⁻¹⁰ — SQT 보다 2.3 배 낮고 χ²/dof 가 2.5 로 SQT-lock 시 fit 자체가 불량. dwarf scale RAR 은 M16 + 단일 a₀ 로 잘 안 맞는다는 Lelli+17 / Iorio+17 결과와 정합.
- D5 (bright) 도 D2 와 비슷한 1.26 × 10⁻¹⁰ — bright disk 가 RAR 통계를 끌어올리는 쪽.

## 4. Cross-dataset 통계

- spread_dex = std(log₁₀ a₀_subset) = **0.163 dex** (≈ 46 %)
- max |log₁₀(a₀_sub / a₀_SQT)| = **0.353 dex** (D4)
- drift signs: [+, +, +, **−**, +] — D4 만 반대 방향, K_X4 만 PASS.

| K | 정의 | 결과 |
|---|---|---|
| K_X1 | spread_dex ≤ 0.05 | **FAIL** (0.163) |
| K_X2 | max_dev ≤ 0.10 | **FAIL** (0.353) |
| K_X3 | 모든 subset SQT-locked χ²/dof ≤ 1.6 | **FAIL** (D4: 2.51) |
| K_X4 | drift 부호가 한 방향만 아닐 것 | PASS (D4 가 반대) |

**PASS: 1 / 4**

K_X4 만 통과한 것은 "SQT 가 D2/D3/D5 에서는 *과소*, D4 에서는 *과대*" 를 의미 — 즉 SQT 가 단일 a₀ 로 sample-averaged 일치를 하지만 sample-resolved 에서는 양방향 편차. McGaugh 1.20 도 동일한 sample-resolved spread 를 갖지만, 본 audit 는 **SQT 의 sample-stability** 만 판정.

## 5. Cluster scale (재분석 없음, 문헌만 인용)

| Reference | 시스템 | 보고된 a₀_eff |
|---|---|---|
| Tian & Ko 2016, ApJ 818 32 | X-ray groups+clusters | a₀ ≈ 4 × a₀_SPARC |
| Pradel et al. 2014 (toy reanalysis) | groups | a₀ enhanced 5–10× |
| Eckert et al. 2022, A&A 662 A123 | XMM-Newton stacked | RAR 중력 결손 cluster scale |

**구조적 한계**: 단일 a₀ 보편성을 가정하는 어떤 모델 (MOND, SQT 동일 형태) 도 SPARC RAR 와 cluster RAR 를 *동시에* 맞추지 못함. SQT 가 cH₀/(2π) 만으로 a₀ 를 고정한다면 cluster failure 는 자동 — 본 L492 는 이 한계를 SQT 의 cross-system 약점으로 명시한다 (재분석은 별도 LXX).

## 6. 한 줄 결론

**SPARC 175 전체에서의 SQT-RAR 일치는 cross-dataset 안정성을 갖지 못한다 — 단일 dataset 일치이며, 부분 표본 (특히 dwarf LITTLE THINGS proxy) 에서 0.35 dex (×2.3) 어긋난다. PASS 1/4.**

## 7. 산출물
- `simulations/L492/run.py` — 본 audit 코드.
- `results/L492/L492_results.json` — 모든 subset fit 수치.
- `results/L492/RAR_DATASET_AUDIT.md` — 본 보고서.
