# L328 — Next Step

## 즉시 실행 (코드)
1. `simulations/L328/run.py` 작성:
   - L281 Laplace pipeline 재사용 (BB 3-param, LCDM/smooth baseline).
   - 6 subset (S0 SPARC-only, S1–S3 SPARC+single-anchor, S4 anchors-only, S5 full).
   - 동일 prior box. 각 subset 별 lnZ_BB, lnZ_baseline, ΔlnZ 출력.
2. 4인 코드리뷰 (역할 사전 지정 없음, 자율 분담) — likelihood 일관성, prior box
   동일성, Occam penalty term 분해.
3. L276 LOO 표 재정의 검증: 같은 pipeline 이 ΔAICc 41/56/89 를 재현하는지 확인.
   재현 안 되면 L276 표 표기 수정 (정직 기록).

## 보고 항목 (논문 반영)
- 표: ΔlnZ_subset (S0…S5), 1-σ 불확실도 포함.
- 그림: ΔlnZ vs N_data, log scale. Jeffreys 임계선 (1, 2.5, 5) 표시.
- 본문 수정:
  - "Akaike weight 100%" → 제거 (이미 L281 격하).
  - "ΔlnZ = +0.8 favors BB" → "ΔlnZ_full = +0.8 (full joint, marginalized);
    ΔlnZ_SPARC-only ≈ −12 (Occam-dominated). BB advantage is anchor-driven."
  - L208 anchor caveat 와 cross-reference.

## 미실행 사유
이 thread 는 *독립 사고* 지시. 시뮬레이션은 별도 세션 (4인 코드리뷰 동반)에서
spawn Pool 9 워커로 실행.

## 후속 질문 (L329+ 제안)
- Q1: 새 anchor (P9 dSph, P11 NS) 추가 시 SPARC-only 가 양수 ΔlnZ 영역으로
  진입하는가? L276 의 "anchor 다중성" 명제 정량 검증.
- Q2: anchor 1 개당 ΔlnZ contribution decomposition (additive 가정 검증).
- Q3: smooth baseline 차원 (5 → 4 → 3) 변화 시 Occam penalty scaling 확인.
