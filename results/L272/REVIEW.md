# L272 — 4인 review (mock injection) — CRITICAL FINDING

시뮬 simulations/L272/run.py: N=200 mock LCDM realisations, BB(3 regime) vs universal.

## 결과
- **False BB detection rate (ΔAICc>10): 100%** (200/200)
- median ΔAICc = 132.95
- BB 우위 가 *data-driven tertile split* 인해 자동 발생

## 4인 정직 평가
- P: "anchor 가 *physical* 이면 false rate 다를 것" — 그러나 본 mock 은 unphysical split 으로 BB 의 worst-case overfitting 노출.
- N: 시뮬은 BB 가 *flexibility* 만으로 LCDM 데이터에 100% 우위를 줌을 정량 증명 — overfitting 강력 증거.
- O: L208 ΔAICc=99 (real data) 는 본 결과와 일관 — 진정 신호 vs 자유도 효과 분리 불가.
- H: σ_0 anchors 가 *theory-prior* 가 아니라 *data-fit* 이면 BB 의 모든 우위 의심.

## 정직 결론 (CRITICAL)
**Branch B 의 ΔAICc 우위는 overfitting artefact 가능성 정량 확인.**
완화 조건: σ_0 3 regime 를 *데이터 보기 전* theory-prior 로 고정.
논문에 "anchor predetermined, not fitted" 명시 필수.

→ 등급 -0.02 격하 위험. paper 에 별도 box 필요.
