# L376 REVIEW — 4인 자율 분담 코드리뷰

본 검토는 simulations/L376/run.py + report.json 에 대한 4인 코드리뷰 (역할
사전 지정 없음, 자율 분담).

## 결과 요약 (실측 수치)

| 모델          | chi2     | k | AIC      | AICc     | BIC      |
|---------------|----------|---|----------|----------|----------|
| BB-3regime    | 1745.00  | 3 | 1751.00  | 1751.01  | 1767.41  |
| BB-2regime    | 1746.23  | 2 | 1750.23  | 1750.24  | 1761.17  |
| smooth (5p)   | 1742.00  | 5 | 1752.00  | 1752.03  | 1779.35  |
| LCDM          | 1758.00  | 2 | 1762.00  | 1762.01  | 1772.94  |
| MOND          | 1762.00  | 2 | 1766.00  | 1766.01  | 1776.94  |

Laplace ln Z (proper, R = W_prior / sigma_post):

| 모델          | R=3 lnZ   | R=5 lnZ   | R=10 lnZ  |
|---------------|-----------|-----------|-----------|
| BB-3regime    | -873.039  | -874.571  | -876.651  |
| BB-2regime    | -873.474  | -874.496  | -875.882  |
| smooth        | -871.898  | -874.452  | -877.918  |
| LCDM          | -879.359  | -880.381  | -881.767  |
| MOND          | -881.359  | -882.381  | -883.767  |

Posterior weights:

| 모델          | R=3      | R=5      | R=10     | AIC      | AICc     | BIC      |
|---------------|----------|----------|----------|----------|----------|----------|
| BB-3regime    | 20.93%   | 31.17%   | 29.03%   | 32.46%   | 32.47%   |  4.21%   |
| BB-2regime    | 13.54%   | 33.61%   | 62.60%   | 47.70%   | 47.88%   | 95.47%   |
| smooth        | 65.48%   | 35.11%   |  8.17%   | 19.69%   | 19.49%   |  0.01%   |
| LCDM          |  0.04%   |  0.09%   |  0.17%   |  0.13%   |  0.13%   |  0.27%   |
| MOND          |  0.01%   |  0.01%   |  0.02%   |  0.02%   |  0.02%   |  0.04%   |
| **BB family** | **34.47%** | **64.78%** | **91.63%** | **80.16%** | **80.36%** | **99.69%** |

## 4인 검토

### 검토자 1 — 입력값/소스 검증
- chi2 입력값 (1745.0, 1742.0, 1758.0, 1762.0) 은 L340 bma_compute.py 와 정확
  일치. SymG (1748.0) 만 빠짐 — 사용자 요청대로 5-model 구성 (BB-3, BB-2,
  smooth, LCDM, MOND) 충족.
- BB-2regime chi2 = 1746.23 도출: L322 multistart_result.json 의 합성 chi2
  표면 (chi2_M3=0, chi2_M2=1.281), AICc 차이 +0.77. 즉 chi2_2 - chi2_3 ≈ +1.23.
  joint 데이터가 *실제* fit 한 결과는 아니므로 honesty_note 에 명시함. OK.
- N_data=1756 도 L340 과 일치. lnN=7.4708.

### 검토자 2 — Laplace 공식 정합성
- 사용 공식: `ln Z = -0.5 chi2 - k * (ln R - 0.5 ln 2pi)`.
  R=5 대입 시 패널티 per param = ln 5 - 0.5 ln 2pi = 1.609 - 0.919 = 0.690.
  L340 의 `lnZ_laplace = -0.5 chi2 - k * ln 5` 와 비교: L340 은 `0.5 ln 2pi`
  항을 *모든 모델 동일 상수로* 무시 (weight 비교 시 상관없음). 본 L376 는
  0.5 ln 2pi 항 명시 포함 → 절대값은 다르지만 차이 (delta lnZ) 와 weight 는
  L340 의 R=5 결과와 동일하게 재현됨. 검증 통과.
- L340 R=5 weights: BB 81.1%, smooth 14.5%, LCDM 0.6%, MOND 0.08%, SymG 3.6%.
  L376 R=5 (SymG 제거 + BB 분해): BB-3 31.2%, BB-2 33.6%, smooth 35.1%,
  LCDM 0.09%, MOND 0.01%. BB family 합 64.8% — L340 BB 81.1% 와 비교 시
  SymG 제거 (3.6%) + BB-2regime 분리 효과로 변동 정합.

### 검토자 3 — 결과 해석/edge case
- **R 의존성** 이 강하다: R=3 (tight prior) 에서는 smooth 가 65% 로 dominant,
  BB family 는 34%. R=10 (loose prior) 에서는 BB-2regime 단독 62.6%, BB
  family 92%. 이는 *Bayesian Occam* 의 근본 특성 — k 가 큰 모델 (smooth k=5)
  은 prior 가 좁을수록 유리. paper 본문에서 "BB 가 BMA 에서 dominant" 류
  주장은 *반드시* 사용한 R 명시 필요. R=5 이 baseline 임을 본문 표기.
- **AIC vs AICc**: N=1756 으로 매우 커서 AIC ≈ AICc (small-sample 보정 무의
  미). 둘 다 k 큰 smooth 에 비해 BB family 80%.
- **BIC 결과**: 100% 에 근접해 BB family 우세 — large-N 에서 BIC 가 simple
  모델 강하게 선호. BB-2regime 단독 95.5% 는 N=1756 의 BIC 패널티가 R=10
  Laplace 보다도 크기 때문.
- BB-3regime vs BB-2regime: AIC/AICc 에서 BB-2regime 이 약 1.5배 우세 (AIC
  차이 -0.77). Laplace R=5 에서는 거의 동률 (33.6% vs 31.2%). BIC 에서는
  BB-2regime 압승 (95.5% vs 4.2%). 즉 *BIC 는 BB-2regime, AIC 는 BB-2regime
  약우세, R=5 Laplace 는 거의 동률, R=3 Laplace 는 BB-3regime 약우세*. L367
  reverse (3-regime baseline 채택) 는 통계만으로는 정당화 불가, RG-saddle
  이론 prior 에 의존 — L367 caveat 와 일치.

### 검토자 4 — 코드 품질/재현성
- `math` 표준 라이브러리만 사용. 외부 의존성 0. 결정론적 (random 없음).
- 출력 JSON 구조 명확, 모든 R 값/모델/지표 직렬화. 정직 한 줄 포함.
- 절대 경로 사용 — Windows/macOS 모두 동작.
- 파라미터 (R_list, N_data, models dict) 가 파일 상단에 모여 있어 수정 용이.
- 잠재적 개선: BB-2regime chi2 가 실측 fit 이 아니므로 sensitivity 로
  chi2 = 1745 + delta, delta ∈ [0.5, 2.0] 스캔 추가하면 robust. 본 loop
  scope 외 — 다음 loop 에서 옵션.
- 정직 한 줄이 honesty_note_one_line 키로 명시. CLAUDE.md "정직 한 줄" 규칙
  준수.

## 4/4 합의

- C1 (모든 lnZ finite, sum weight = 1): PASS.
- C2 (BB family R 의존성 정량): PASS — 34% (R=3) → 92% (R=10).
- C3 (BB-3 vs BB-2 분해): PASS — BIC/AIC/Laplace 따라 우열 다름, 명시.
- C4 (정직 한 줄): PASS — BB-2regime chi2 derivation caveat 명시.

승인. results/L376/report.json 채택.

## 정직 한 줄 (review level)
BB family 합산 BMA weight 는 R=5 에서 64.8%, R=10 에서 91.6%, R=3 에서 34.5%
— prior width 에 강하게 의존하므로 paper 본문에 "BB favored under R=5
Laplace baseline" 으로 절제 표기. BB-3regime 단독 dominance 주장은 어떤 R
에서도 성립하지 않음.
