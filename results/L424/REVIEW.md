# L424 REVIEW — 4인팀 실행 결과

**임무**: 8인팀 NEXT_STEP 의 N1–N4 task 수행. simulations/L424/run.py 로
dSph P9 anchor pool 추가 시 BB three-regime ΔlnZ 변화 + mock false-rate 측정.

**방법**: 4인 자율 분담 (CLAUDE.md Rule-B). 데이터 매핑 / Laplace fit /
mock injection / 해석 자연 분담.

**결과 요약**:
- ΔlnZ 는 dSph 추가로 *시나리오 의존적* 으로 변동 (-21 ~ +34).
- 그러나 mock false-rate 는 **변화 없음 (0% → 0%)** — 강제력 회복 신호 부재.
- ATTACK B2 (강제력 ≠ pool 확대) 의 우려가 실측 결과로 부분 확정.
- 정직 권고: paper §6.1 row #5 ACK_REINFORCED, P9 falsifier 부호-결정 필요.

---

## (1) Archive 측정 + ρ_env 매핑 (N1)

5 classical Local Group dSph (McConnachie 2012 표준값, Gaia DR3 RVS 보강):

| name      | σ_los (km/s) | r_half (pc) | D_LG (kpc) | M_dyn (10⁷ M☉) |
|-----------|--------------|-------------|------------|-----------------|
| Draco     | 9.1          | 221         | 82.0       | 2.20            |
| UrsaMinor | 9.5          | 181         | 78.0       | 1.80            |
| Sculptor  | 9.2          | 283         | 86.0       | 3.40            |
| Sextans   | 7.9          | 695         | 89.0       | 4.10            |
| Carina    | 6.6          | 250         | 106.0      | 0.80            |

ρ_env 매핑 결과:

| name      | log10(ρ/ρ_c)_LG | log10(ρ/ρ_c)_internal | σ₀_proxy | σ_err |
|-----------|-----------------|------------------------|----------|-------|
| Draco     | −0.52           | +6.54                  | 0.864    | 0.086 |
| UrsaMinor | −0.48           | +6.71                  | 0.902    | 0.090 |
| Sculptor  | −0.56           | +6.41                  | 0.874    | 0.087 |
| Sextans   | −0.59           | +5.32                  | 0.750    | 0.075 |
| Carina    | −0.76           | +5.94                  | 0.627    | 0.063 |

**관찰**: ATTACK B3 의 "regime 양다리" 가 실측에서 확인. Local-Group regime
(D_LG 기반) 은 cluster~cosmic 사이 (−0.5 ~ −0.8) 로 anchor pool 의 *gap 채움*
역할. galactic-internal regime (M_dyn / r_half³) 은 +5 ~ +7 로 SPARC core
보다도 *높은* 밀도 — 아예 다른 regime. 어느 매핑 쓸지로 결과 부호 변동.

---

## (2) Baseline ln Z grid (no dSph)

| R   | three_R | two_R | mono | lcdm | ΔlnZ(3R−L) | ΔlnZ(2R−L) |
|-----|---------|-------|------|------|------------|-------------|
| 2   | −19.73  | −84.31| −79.91| −100.85 | +81.12 | +16.54 |
| 3   | −21.35  | −85.27| nan  | −101.25 | +79.90 | +15.98 |
| 5   | −23.39  | −86.67| nan  | −101.77 | +78.37 | +15.09 |
| 10  | −86.26  | −88.70| −83.80| −102.46 | +16.20 | +13.76 |

**관찰**:
- toy anchor (8개, base.md §3.5/§3.6 calibrated) 에서 three-regime 의
  ΔlnZ vs LCDM 은 R=2~5 에서 +78 ~ +81 — *toy 가 V-shape 을 강하게 favour*.
  이는 toy 가 V-shape 재현용으로 구성된 결과이며 실 데이터 0.8 (paper §3.6
  marginalized) 와 *직접 비교 불가* (L405 disclaimer 동일).
- R=10 에서 ΔlnZ(3R−L) 가 +16 으로 급락 — Lindley wide-prior collapse 신호.
  monotonic 모델은 R=3, 5 에서 Hessian 특이 (nan) — 8-point anchor 에 4
  파라미터가 sloppy.

---

## (3) dSph 추가 ΔlnZ 변동 (N2, N3)

### Scenario A: Local-Group regime 매핑 (kpc-outer, low-ρ_env 추가)

| dSph σ₀ scenario   | ΔlnZ(3R−L) @R=5 | Δ vs baseline | ΔlnZ(2R−L) @R=5 | Δ vs baseline |
|--------------------|------------------|----------------|------------------|----------------|
| null_archive       | +62.74           | **−15.63**     | +6.84            | −8.25          |
| compat_cosmic      | +104.56          | +26.18         | +41.26           | +26.16         |
| compat_galactic    | +84.46           | +6.09          | +21.21           | +6.12          |
| tension_cluster    | +112.52          | +34.15         | +33.51           | +18.42         |

### Scenario B: galactic-internal regime 매핑 (별별 자체 밀도)

| dSph σ₀ scenario   | ΔlnZ(3R−L) @R=5 | Δ vs baseline | ΔlnZ(2R−L) @R=5 | Δ vs baseline |
|--------------------|------------------|----------------|------------------|----------------|
| null_archive       | +69.72           | −8.66          | +13.82           | −1.27          |
| compat_cosmic      | +101.84          | +23.47         | +32.14           | +17.05         |
| compat_galactic    | +86.78           | +8.41          | +17.23           | +2.14          |
| tension_cluster    | +56.64           | **−21.73**     | +33.70           | +18.61         |

**관찰**:
- **archive 변환값 (null_archive)** 은 두 매핑 모두에서 ΔlnZ 를 *낮춤*
  (LG: −15.63, INT: −8.66). 즉 Walker 2009/Gaia DR3 표준값을 그대로 변환
  하면 three-regime 모델이 *오히려 약화*.
- compat_cosmic / compat_galactic 시나리오는 ΔlnZ 강화. 하지만 이는
  dSph σ₀ 를 *의도적으로 cosmic 또는 galactic regime 값에 박은* 결과
  — ATTACK B6 의 "부호 미지정 saturation" 이 사후 cherry-pick 로 강화처럼
  *보일 수 있음* 의 직접 증거.
- tension_cluster 매핑이 LG mode 에서는 ΔlnZ 강화 (+34) 인데 INT mode
  에서는 ΔlnZ 약화 (−21.73). 매핑 선택만으로 *부호 반전* — ATTACK B3 의
  "regime 양다리 자유도" 우려를 정량 확인.
- 따라서 dSph anchor 추가의 ΔlnZ 변화는 *prior 사전등록 없이는 강화 주장
  불가*.

---

## (4) Mock false-detection rate (N4) — 핵심 강제력 진단

| anchor pool       | N    | three-regime false-rate (LCDM null mock 200) |
|-------------------|------|----------------------------------------------|
| baseline          | 8    | **0.0%**                                     |
| baseline + dSph(LG)| 13  | **0.0%**                                     |

**관찰**:
- 이 toy 의 false-rate 는 baseline 에서 이미 0% — paper §3.5 의 "100% false-
  detection" 과 *다름*. 이유: 본 toy 의 LCDM null 은 σ_truth = 0.85 단일
  값에 ε_err = 0.10 noise — paper §3.5 의 175-galaxy SPARC 분포보다 노이즈
  구조가 단순. *base.md §3.5 의 100% rate 와 직접 비교 불가*.
- 그러나 **dSph 5점 추가가 false-rate 를 *낮추지도 않음***. 본 toy 에서는
  baseline 도 0% 이므로 "강화" 측정 불가. paper 실측 (175 SPARC + 1 cluster
  + 2 cosmic + 5 dSph = 183) 으로 같은 mock 을 돌려야 ATTACK B2 결판.
- 본 L424 mock 결과는 *necessary not sufficient*: dSph 추가가 false-rate
  를 *악화* 하지 않음을 toy 수준에서 확인. paper §3.5 175-point mock
  재실행은 별도 budget (L425).

---

## (5) 4인팀 종합

**핵심 발견**:
1. dSph σ₀ "saturation prediction" 의 priori 수치 부재 (ATTACK B1) 가 본
   forecast 에서 *부호-결정 자유도* 로 직접 발현. compat_cosmic /
   compat_galactic / tension_cluster 시나리오 어느 쪽도 사전등록 없이는
   재량 선택. ΔlnZ 가 −22 ~ +34 범위에서 시나리오 의존.
2. ρ_env 매핑 (LG outer vs galactic-internal) 만으로 tension_cluster
   시나리오의 ΔlnZ 부호가 반전 (+34 ↔ −22) — ATTACK B3 의 "regime 양다리"
   가 실측 결과 변동성의 직접 source.
3. archive 변환값 (null_archive) 은 두 매핑 모두에서 ΔlnZ 를 *낮춤*.
   이는 dSph σ₀ ≈ 0.6 ~ 0.9 범위가 toy three-regime 의 V-shape 위치 (cosmic
   ~1.1 , cluster ~0.4) 어느 쪽과도 정확히 일치하지 않기 때문.
4. mock false-rate 는 본 toy 에서 baseline 0% — 강제력 회복 측정의 *유의 신호
   부재*. paper §3.5 175-point mock 재실행이 필요.

**Three-regime 강제성 평가**:
- paper §6.1 row #5 "강제성 약함, dSph + NS 추가" 의 *dSph 부분*: 본 L424
  forecast 결과로 "dSph 추가가 자동으로 강제성을 회복하지는 않는다" 가
  정량 확인.
- 강제력 회복 조건: (a) σ₀_dSph 부호-결정 임계 사전등록, (b) ρ_env 매핑
  사전 선택 (LG outer vs internal), (c) σ₀ 변환 prior 명시, (d) paper §3.5
  175-point mock 으로 false-rate Δ 재측정. 4 조건 모두 미해결.

---

## (6) 정직 권고 — paper §6.1 row #5 강화안

현재 (L918):
> | 5 | Three-regime 강제성 약함 (anchor 4-5개 필요) | ACK | dSph + NS 추가 |

**제안 강화 표현**:
> | 5 | Three-regime 강제성 약함. **L424 forecast 결과**: 5 classical Local
> Group dSph (Draco/UMi/Scl/Sextans/Carina) archive 추가 시 ΔlnZ 변동
> −22 ~ +34 (scenario × ρ_env-mapping 의존). archive 변환 그대로 사용 시
> ΔlnZ *감소* (LG: −15.6, INT: −8.7). 강화 주장은 *부호-결정 임계 + ρ_env
> 매핑 + σ₀ 변환 prior + 175-point mock false-rate Δ* 4 조건 사전등록 후만
> 가능. 본 시점에서는 dSph 추가가 강제성을 자동 회복하지 못함. | ACK_REINFORCED
> | 4 조건 사전등록 (L425 GitHub release tag) → 실 SPARC+dSph mock 재실행 |

**P9 falsifier 등급 권고** (paper §4 22-예측 표):
- 현재: P9 dSph σ₀ saturation (low-ρ_env regime 재진입, 정성).
- 제안: **P9 conditional** — 부호 (cosmic / galactic / cluster regime) 사전
  등록 *후* 만 falsifier 기능. 사전등록 없으면 "정성 시사" 등급으로 격하.

---

## 결과 파일
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L424/ATTACK_DESIGN.md`
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L424/NEXT_STEP.md`
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L424/REVIEW.md`
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L424/run_log.txt`
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L424/report.json`
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/simulations/L424/run.py`

## 정직 한 줄
**dSph P9 anchor pool 추가는 BB three-regime 강제력을 자동 회복시키지 못한다 — 부호-결정 임계 + ρ_env 매핑 + σ₀ 변환 prior + 175-point mock false-rate Δ 4 조건 사전등록 후에만 강화 주장 가능.**
