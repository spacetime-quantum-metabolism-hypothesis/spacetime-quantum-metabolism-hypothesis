# L451 REVIEW — 4인팀 실행 결과

**임무**: 8인팀 ATTACK + 4인팀 NEXT_STEP 의 mock injection-recovery (N=200)
실행. anchor pool 8 (baseline) ↔ 13 (+5 dSph) 의 ΔlnZ(three_regime − lcdm)
분포를 truth 2 (LCDM null / SQT pre-fit) × mapping 2 (LG outer / galactic
internal) = 4 셀 매트릭스로 측정.

**방법**: 4인 자율 분담 (CLAUDE.md Rule-B). multiprocessing.spawn Pool(8),
OMP/MKL/OPENBLAS=1, mock 단위 분할. R=5.0 fixed. 사전등록 판정 기준
(B7) (a)/(b)/(c) 그대로 적용.

**소요**: 14.1 s (200 mock × 4 cell × 2 pool = 1600 Laplace fit + 200 truth-
prefit). 사전등록 budget 내 완료.

---

## (1) SQT pre-fit truth (T1b)

base8 anchor 에 three-regime, R=5 MAP fit 수행:

```
θ_SQT = [s_h=0.980, s_m=0.385, s_l=1.091, t1=3.000, t2=0.500]
```

baseline log_rho 위치에서 truth 예측값:
`[+0.98, +0.98, +0.385, +0.385, +0.385, +1.091, +1.091, +1.091]` —
즉 V-shape (high-ρ 0.98, mid-ρ 0.385, low-ρ 1.09) 구조 그대로.

---

## (2) Per-cell ΔlnZ(three_regime − lcdm) 분포

200 mock × 8 cell:

| truth | mapping | pool | n_ok | mean | std | p05 | p50 | p95 |
|-------|---------|------|------|------|------|------|------|------|
| lcdm | LG | base8 | 125 | -14.28 | 7.22 | -35.5 | -12.9 | -5.9 |
| lcdm | LG | base13 | 138 | -13.75 | 8.48 | -21.4 | -13.0 | -5.1 |
| lcdm | INT | base8 | 122 | -14.29 | 6.91 | -35.2 | -13.2 | -6.2 |
| lcdm | INT | base13 | 138 | -16.84 | 23.96 | -38.1 | -13.4 | -9.8 |
| sqt  | LG | base8 | 193 | +73.04 | 22.44 | +24.7 | +76.1 | +105.2 |
| sqt  | LG | base13 | 191 | +93.85 | 28.92 | +41.1 | +100.1 | +130.0 |
| sqt  | INT | base8 | 196 | +76.34 | 22.69 | +32.8 | +78.4 | +107.2 |
| sqt  | INT | base13 | 196 | +82.72 | 24.65 | +30.7 | +87.1 | +114.9 |

**핵심 관찰 (ΔlnZ 절대값)**:
1. LCDM null truth 에서 ΔlnZ 평균은 모든 셀에서 *음수* (~-14): three-regime
   가 자유도 5 패널티로 lcdm 에 패배 — 정상.
2. SQT truth 에서 ΔlnZ 평균은 +73 ~ +94: V-shape 진짜 truth 일 때 강한
   detection. 폭(std) 22 ~ 29 — 단일 mock 의 우연 변동도 ±50 범위.
3. Laplace 성공률: LCDM null 에서 60–69%, SQT truth 에서 ≥95%. lcdm-truth
   mock 에서 three-regime 의 Hessian 이 자주 특이 (예측대로).
4. lcdm__INT__base13 의 std 23.96 (다른 셀 6–9 의 3 배) — galactic-internal
   매핑이 *같은 LCDM truth* 에 대해서도 outlier 분산을 만듦. ATTACK B3 의
   "regime 양다리" 가 mock 분포 폭에서 직접 발현.

---

## (3) ΔΔlnZ (13-pool − 8-pool) 분포 — *핵심 측정량*

쌍대 mock realisation 에서 같은 noise seed 로 8-pool ↔ 13-pool 비교:

| truth | mapping | n_ok | mean | std | [p05, p50, p95] |
|-------|---------|------|------|------|------|
| lcdm | LG  | 86  | **+1.64**  | 10.69 | [-11.1, +0.05, +24.3] |
| lcdm | INT | 81  | **-1.87**  |  9.90 | [-23.9, -0.22, +8.4]  |
| sqt  | LG  | 184 | **+21.46** | 39.98 | [-46.4, +22.8, +88.3] |
| sqt  | INT | 192 | **+5.91**  | 33.84 | [-52.8, +8.2,  +59.0] |

**해석**:
- **LCDM null** 에서 ΔΔlnZ 평균이 ±2 (~0) — dSph 5점 추가 자체가 자유도
  패널티 + 정보 균형으로 *거의 0 이동*. 부호는 매핑에 의존 (+1.6 vs -1.9).
- **SQT truth** 에서 ΔΔlnZ 평균이 +21 (LG), +5.9 (INT). 같은 V-shape truth
  에 dSph 추가 → 매핑별로 *4 배 차이*. ATTACK B3 의 매핑 자유도가 13-pool
  ΔΔlnZ 부호 강도에 직접 영향.
- 분포 폭 σ 가 10 (lcdm) ~ 40 (sqt) — L424 가 보고한 ±34 변동이 *single-
  realisation noise 폭 안* 에 들어옴. 즉 L424 의 −22 ~ +34 범위는 mock
  통계로는 "1σ noise" 와 구분되지 않음 (특히 SQT truth 에서).

---

## (4) B7 anti-cherry-pick 판정 (사전등록 기준)

| 셀 | (a) mean<0 | (b) std<5 |
|---|---|---|
| lcdm__LG | False | False |
| lcdm__INT | True | False |
| sqt__LG | False | False |
| sqt__INT | False | False |

| 매핑 차 | mean_diff | pooled_std | (c) within 1σ |
|---|---|---|---|
| lcdm (LG vs INT) | 3.51 | 10.30 | **True** |
| sqt  (LG vs INT) | 15.54 | 37.03 | **True** |

**Tally**:
- (a) mean < 0      : 1/4 셀  → FAIL (LCDM-INT 만 통과, 셋은 양수)
- (b) std < 5       : 0/4 셀  → FAIL (모든 분포가 cherry-pick 폭 ±34 와 비슷)
- (c) mapping 차 < 1σ_pooled: **2/2 truth** → PASS

**판정**: **PASS-C** — 매핑 자유도(LG vs INT) 는 mock realisation 변동
안에 흡수된다. 즉 L424 가 발견한 "매핑 선택만으로 ΔlnZ 부호 반전" 은 실제
구조적 자유도 라기보다 *single-realisation outlier* 와 같은 크기.
PASS-A, PASS-B 미충족: Bayes factor 가 평균값을 0 으로 끌어내리지 *않으며*,
분포 폭도 cherry-pick 우려 폭과 *동일 크기*.

---

## (5) 4인팀 종합

**핵심 발견**:
1. L424 의 ΔlnZ ±34 변동은 200-mock 분포의 std 와 *동일 크기*. 즉 시나리오
   × 매핑 그리드를 자유롭게 골라잡으면 "구조적 신호" 처럼 보이지만, 실제로는
   noise realisation 한 표본의 폭과 구분 불가.
2. 매핑 자유도 (LG vs INT) 자체는 mock 변동 안에 흡수 (PASS-C). 이는 *나쁜
   소식이자 좋은 소식*: dSph 매핑 사전등록 의무는 약화되지만, 동시에 매핑
   선택으로 얻을 수 있는 신호도 제한적.
3. SQT truth + 13-pool 셀에서 ΔΔlnZ 분포 std 가 34 ~ 40 — 만약 SQT 가 진짜
   진실이라도, 단일 실측으로 +20 같은 값이 나와도 *통계적 우연 한계 안*.
4. LCDM null 에서 ΔΔlnZ 평균 ≈ 0 (PASS-(a) 부분 충족: -1.87) — Bayes factor
   가 "null 일 때는 anchor 추가가 평균 0" 을 어느 정도 지킴. 하지만 폭이
   여전히 std 10 으로 cherry-pick 면역은 아님.

**Bayes factor anti-cherry-pick 운영 정의**:
- 본 toy 에서 Bayes factor 는 *부분적* anti-cherry-pick — null 평균 보존
  (a) 일부 통과 + 매핑 자유도 흡수 (c) 통과. 그러나 분포 폭 (b) 미충족.
- "single ΔlnZ 값 인용" 은 위험 — 반드시 200-mock 분포 std 동반 필요.
- L424 의 ±34 변동은 "cherry-pick 위험" 의 직접 증거가 *아니라* "noise
  realisation 폭" 의 직접 증거. 하지만 *어느 쪽이든* paper 본문에 단일
  ΔlnZ 인용은 부적절.

---

## (6) 정직 권고 — paper §6.1 row #5 추가 기록 안

**제안 추가 표현**:
> | 5b | (L451 mock injection-recovery) ΔΔlnZ(13−8) 분포 측정: LCDM null
> 평균 ±2, std 10; SQT truth 평균 +21 (LG) / +6 (INT), std 34–40. L424 의
> ΔlnZ −22~+34 변동은 *single-realisation noise* 와 동일 크기. ρ_env
> 매핑(LG vs INT) 차는 1σ_pooled 안에 흡수 (PASS-C). 단일 ΔlnZ 인용은
> 분포 std 동반 필수. | INFO | 175-point mock + 사전등록 falsifier 임계 |

---

## 결과 파일
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L451/ATTACK_DESIGN.md`
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L451/NEXT_STEP.md`
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L451/REVIEW.md`
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L451/run_log.txt`
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L451/report.json`
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/simulations/L451/run.py`

## 정직 한 줄
**L424 의 ΔlnZ ±34 변동은 cherry-pick 자유도와 mock noise 폭 (std 10–40) 의 합으로 발생하며, Bayes factor 는 매핑 자유도 흡수 (PASS-C) 만 통과하고 평균-0/폭<5 기준 (PASS-A/B) 은 미충족 — anti-cherry-pick 으로 부분만 작동한다.**
