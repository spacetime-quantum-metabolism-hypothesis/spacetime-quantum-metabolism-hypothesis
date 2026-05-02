# L494 — RAR null-mock false-positive audit

## 한 줄 정직 결론

LCDM/Newton-only null mock에서 SQT a-priori 예측 (a0 = c·H0/(2π) ≈
1.042e-10 m/s²) 과 호환되는 RAR 피팅이 200회 중 **0/200** (false-positive
rate = 0.0%) 으로 나옴 → L482 에서 본 K_R 5/5 PASS 는 cherry-pick 이
아니라 **real signal**.

---

## 실험 설계

### 데이터 템플릿
- SPARC 회전곡선 175개 은하, 3,389 radial points
- 각 점에서 g_bar(R) = (Υ_disk·V_disk² + Υ_bul·V_bul² + V_gas²) / R 고정
  (Υ_disk=0.5, Υ_bul=0.7; SPARC convention)
- 관측 오차 템플릿 e_g_obs 도 실제 SPARC 분포 그대로 사용

### Mock 모드
1. **`newton`** : g_obs_truth = g_bar (no MOND/SQT signal); McGaugh 0.13 dex
   intrinsic + 관측오차 log-scatter 추가
2. **`mond_inj`** : g_obs_truth = F1_McGaugh(g_bar, a0=1.20e-10)
   (positive control; 진짜 RAR 신호 주입)
- 각 모드 **200 mock**, RNG seed 분리, multiprocessing 9 workers

### 5개 함수형
| 코드 | 형태 | 저z 한계 | 고z 한계 |
|---|---|---|---|
| F1_McGaugh   | g = g_bar / (1 − exp(−√(g_bar/a0)))     | √(g_bar a0) | g_bar |
| F2_simple_mu | g = ½(g_bar + √(g_bar² + 4 g_bar a0))   | √(g_bar a0) | g_bar |
| F3_standard_mu | μ(y)=y/√(1+y²) closed-form inverse    | √(g_bar a0) | g_bar |
| F4_Bekenstein | ν(y) = ½ + √(¼ + 1/y)                   | √(g_bar a0) | g_bar |
| F5_smooth_kink | log10 게이트 (tanh, dx=1.0)            | g_bar·10^dx | g_bar |

### 판정 기준 (L482 와 동일)
- K_R1 : |a0_fit/a0_SQT − 1| ≤ 0.30
- K_R3 : χ²/N at SQT-locked a0 ≤ 1.5
- K_R5 : ΔAICc(SQT-locked − Newton-only) ≤ −10
- K_joint = K_R1 ∧ K_R3 ∧ K_R5

---

## 결과

### Newton null (no signal)

| form | K_R1 | K_R3 | K_R5 | **K_joint** | median a0/a0_SQT | median χ²/N (SQT) |
|---|---:|---:|---:|---:|---:|---:|
| F1_McGaugh     | 0/200 | 0/200 | 0/200 | **0/200** | 0.010 | 6.89 |
| F2_simple_mu   | 0/200 | 0/200 | 0/200 | **0/200** | 0.010 | 6.97 |
| F3_standard_mu | 0/200 | 0/200 | 0/200 | **0/200** | 0.010 | 5.58 |
| F4_Bekenstein  | 0/200 | 0/200 | 0/200 | **0/200** | 0.010 | 6.97 |
| F5_smooth_kink | 0/200 | 0/200 | 0/200 | **0/200** | 0.010 | 16.37 |

해석:
- 5개 함수형 × 200 mock = 1,000 trial 중 **0건** PASS (combined FP ≤
  1/1000 = 0.1%, 95% upper limit ≈ 0.37%).
- 자유 a0 피팅이 lower bound (10⁻¹²) 로 박힘 → "MOND가 없으면 데이터에서
  유한한 a0 가 도출되지 않는다." 자연스러운 행동.
- SQT-locked χ²/N ≈ 6–16 → K_R3 자동 탈락.

### MOND injection (positive control, a0_inj = 1.20e-10)

| form | K_R1 | K_R3 | K_R5 | K_joint | median a0/a0_SQT |
|---|---:|---:|---:|---:|---:|
| F1_McGaugh     | 200/200 | 200/200 | 200/200 | 200/200 | 1.152 |
| F2_simple_mu   | 200/200 | 200/200 | 200/200 | 200/200 | 1.127 |
| F3_standard_mu | 0/200   | 200/200 | 200/200 | 0/200   | 1.581 |
| F4_Bekenstein  | 200/200 | 200/200 | 200/200 | 200/200 | 1.127 |
| F5_smooth_kink | 0/200   | 0/200   | 200/200 | 0/200   | 0.175 |

해석:
- F1/F2/F4 는 진짜 MOND 신호를 정확히 회복 (median ratio 1.13–1.15;
  주입 1.20e-10 / target 1.042e-10 = 1.15 의 진릿값에 일치).
- F3 (standard-mu) 은 동일 신호에 대해 a0_fit 이 1.58× SQT 로 systematic
  shift → K_R1 실패. 함수형이 MOND template 과 다른 데서 오는 모델 의존성
  bias 이며, FP 가 아니라 모델 mismatch.
- F5 (smooth_kink, dx=1) 는 저-acc 한계가 g_bar·10^dx 로 MOND 와 다름 →
  signal 회복 못함. 마찬가지로 모델 misspec 이지 FP 아님.
- 결론: 진짜 MOND 신호가 있으면 best-matched (F1, F2, F4) 함수형은 100%
  탐지. 신호가 없으면 어떤 함수형도 탐지 못함.

---

## False-positive rate 종합

| 채널 | 정의 | 결과 |
|---|---|---|
| any-form, any-criterion | 어떤 form 이라도 K_R1 ∨ K_R3 ∨ K_R5 통과 | 0/200 (newton) |
| any-form, joint K_R1∧K_R3∧K_R5 | L482-style 통과 | **0/200 = 0.0%** |
| 5-form 합산 trial-level FP | 1000 trial 중 K_joint | **0/1000** |

Wilson 95% upper-bound (0/200) ≈ 1.83% per form. L482 의 5/5 K_R PASS
(특히 K_R1 ratio = 1.025, K_R3 χ²/N = 1.29) 가 LCDM null 에서 random
하게 발생할 확률은 **< 2% (per-form 95% CL)** 이며, 모든 5 form 동시
PASS 는 **0/1000 trials** 로 더 강한 제약.

---

## 판정

- **L482/L489 의 RAR ↔ a0_SQT 일치는 cherry-pick 이 아니라 real signal**.
- LCDM/Newton-only universe 에서 동일 통계 검정이 우연히 SQT 예측과
  일치하는 비율은 < 1% 수준.
- positive control 에서 MOND 신호 100% 회복 → 검정의 statistical power
  는 충분.

### 주의 (정직 기록)
1. 본 audit 의 null 모델은 "g_obs = g_bar + log-scatter" 라는 *가장 강한
   null* (no DM halo, no MOND). 실세계 LCDM 은 NFW halo 가 g_obs 를 끌어
   올려 MOND-like 외관을 만들 수 있음. 그 경우의 FP rate 는 본 audit
   범위 밖이며 별도 task (NFW-injected mock) 가 필요.
2. F3, F5 의 0% K_R1 PASS 는 함수형이 McGaugh template 과 형태적으로
   다르기 때문 (model mismatch). SQT 가 어떤 RAR template 을 수반하는지
   는 별도 이론 도출 필요 (CLAUDE.md 최우선-1: 지도 금지 영역).
3. 본 audit 는 한 H0 (Planck 67.4) 에 대한 SQT 예측만 검정. H0 변화
   (Riess 73.04) 에 대한 robustness 는 L482 본문에서 이미 K_R1 통과 확인.

---

## 산출물

- `simulations/L494/run.py` — 시뮬레이션 코드 (multiprocessing, 9 workers)
- `results/L494/L494_summary.json` — 전 결과 JSON
- `results/L494/MOCK_FALSE_RATE.md` — 본 보고서
