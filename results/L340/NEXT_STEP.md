# L340 — NEXT_STEP

## 결정
- **paper narrative 유지** (BB 81–93% across BIC/Laplace).
- "BB Akaike weight 100%" 표현 영구 폐기. 본문 표/문장 모두 수정.
- model-averaged σ_8 = 0.812, H_0 = 67.8 BMA 보고 (단일 BB 값과 같은 자리수).

## L341 후보
1. **dynesty nested sampling** 으로 BB / smooth / LCDM lnZ 직접 계산 — Laplace 근사 검증.
   - 1000 live points, BB 3-param, smooth 5-param, LCDM 2-param.
   - BIC 와 dynesty lnZ gap 비교. > 1 차이면 Laplace 부적합 영역.
2. **MOND/SymG full posterior** — 본 BMA 에서 사용된 chi² 값은 family-level 추정. proper joint MCMC 한 번씩 돌려 chi²_min 갱신.
3. **prior sensitivity**: Laplace 에서 prior width 5σ → 3σ / 10σ 변화 시 BB weight 변동 곡선.

## 우선순위
- L341 = dynesty (BB vs smooth) lnZ 직접 측정. L281 Laplace ΔlnZ=+0.8 vs L340 BIC ΔlnZ=+5.97 의 큰 격차 — 둘 중 하나는 부정확. 진실 확인.

## 코드 산출물
- `results/L340/bma_compute.py` — BIC + Laplace + AIC 세 척도 비교, 5-모델.
- `results/L340/bma_report.json` — 정량 결과 dump.

## 정직 메모
- L196→L340 에서 BB 표시 weight 가 99.9998% → 81–93% 로 떨어진 것은 **공격이 아니라 분석 정직성 향상**.
  - 4-모델 → 5-모델
  - AIC → BIC/Laplace (Occam penalty 강화)
  - fixed-θ → marginalized
- 등급 변화 없음. BB 우위는 5-모델 확장 후에도 robust.
