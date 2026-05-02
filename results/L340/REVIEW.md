# L340 — 4인 review (5-모델 proper BMA)

## 결과 요약 (results/L340/bma_report.json)
| Model  | k | chi² | BIC    | ΔlnZ vs BB (BIC) | ΔlnZ vs BB (Laplace, 5σ prior) |
|--------|---|------|--------|------------------|--------------------------------|
| BB     | 3 | 1745.0 | 1767.41 | 0    | 0     |
| smooth | 5 | 1742.0 | 1779.35 | −5.97 | −1.72 |
| LCDM   | 2 | 1758.0 | 1772.94 | −2.76 | −4.89 |
| MOND   | 2 | 1762.0 | 1776.94 | −4.76 | −6.89 |
| SymG   | 4 | 1748.0 | 1777.88 | −5.24 | −3.11 |

### Posterior model weights
- **BIC-based**:     BB 92.64% · LCDM 5.84% · MOND 0.79% · SymG 0.49% · smooth 0.24%
- **Laplace (5σ)**: BB 81.14% · smooth 14.55% · SymG 3.62% · LCDM 0.61% · MOND 0.08%
- **AIC (vgl. L196)**: BB 59.06% · smooth 35.82% · SymG 4.85% · LCDM 0.24% · MOND 0.03%

### Model-averaged predictions
- BIC weights:      σ_8 = 0.8118, H_0 = 67.80
- Laplace weights:  σ_8 = 0.8115, H_0 = 67.83
- AIC weights:      σ_8 = 0.8111, H_0 = 67.85

(예측 spread Δσ_8 < 0.001, ΔH_0 < 0.05 — BMA 안정.)

## L196 vs L281 vs L340 narrative arc
- L196 (4-model, AIC): BB **99.9998%**.
- L281 (BB vs smooth, marginalized Laplace): ΔlnZ = +0.8 → BB ~ 69%.
- L340 (5-model, BIC): BB **92.6%**, (Laplace 5σ prior): BB **81.1%**, (AIC for fair comparison): BB **59.1%**.

→ L196 의 "100%" 는 4-모델 + AIC 패널티 부재의 합작품. proper BMA 에서는 60–93% 사이.

## 4인 자율 분담 review
- **P (proponent)**: BB 가 BIC/Laplace 어느 척도에서도 가장 높은 lnZ. 5-모델 추가에도 dominant 유지.
- **N (nihilist)**: AIC weight 59% 는 "near-coin-flip with smooth (36%)". paper 에서 BIC 단독 강조 시 readers misled. 반드시 두 척도 모두 보고.
- **O (Occam)**: BIC 패널티 (k·ln 1756)/2 ≈ 3.74 per param 이 가장 보수적. Laplace (5σ prior, ln 5 ≈ 1.61 per param) 는 중간. AIC (1 per param) 는 가장 약함. 세 척도가 BB 우위는 일치 — robust.
- **H (honesty)**:
  - L196 의 "BB 100%" 주장은 4-모델 한정 + AIC 한정 결과. **paper 본문에 이 한계 명시 필수**.
  - 5-모델 proper BMA 에서 BB weight = **81.1% (Laplace) / 92.6% (BIC)**. 50% 이상 → narrative 격하 *없음*, 다만 "100%" 표현은 영구 폐기.
  - smooth 가 Laplace 에서 14.5%, AIC 에서 35.8% — 두 번째 후보로 유지. paper 에 "BB strongly preferred but smooth retains nontrivial posterior weight" 명시.

## 정직 판정
- **BB weight (BIC) = 92.64% > 50%** → narrative 유지.
- **BB weight (Laplace 5σ) = 81.14% > 50%** → narrative 유지.
- **단**, AIC weight 59% 는 borderline. paper 본문에 세 척도 모두 보고 — "BB favored across BIC / Laplace / AIC; weight 59–93% depending on Occam strength".
- σ_8, H_0 BMA 예측은 BB 단독 예측에서 1σ 이내 (Δ < 0.001/0.05) → robust.

등급 변화: **0**. (L281 의 −0.005 격하 후, L340 에서 추가 격하 *없음*. 5-모델 확장으로도 BB 우위 보존.)
