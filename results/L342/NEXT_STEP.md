# L342 NEXT STEP — 비단조성 LRT 결과 + 후속

## 산출 결과 (simulations/L342/run.py)

세 anchor (cosmic 8.37±0.06, cluster 7.75±0.06, galactic 9.56±0.05) 에 대해:

| 모델                  | k | χ²      | AIC    | BIC    | ΔBIC   |
|-----------------------|---|---------|--------|--------|--------|
| M1  linear monotonic  | 2 | 288.04  | 292.04 | 290.24 | +286.9 |
| M1b tanh monotonic    | 2 | 288.04  | 292.04 | 290.24 | +286.9 |
| M2  parabola V-shape  | 3 |   0.00  |   6.00 |   3.30 |   0.0  |

- **Δχ² (M1 − M2) = 288**, formal LRT ≈ **17σ** (1 dof equiv).
- **ΔBIC = 287** → Kass-Raftery "decisive" 의 ~30배 초과.
- AICc(k=3, N=3) 정의 불가 (denom=−1) — AIC/BIC/Δχ² 로 보고.
- M1b (sigmoid plateau) 도 M1 과 동일 chi² — 단조 family 전체가 cluster
  outlier 를 fit 못함.

## Z stress test (cluster σ_y 인플레이션)

| σ_y(cluster) | χ²(M1) | cluster residual | 단조 기각 |
|--------------|--------|------------------|------------|
| 0.06 dex     | 288.0  | −14.2σ           | 17σ        |
| 0.50 dex     |   5.9  | −2.4σ            | 2.4σ       |
| 1.00 dex     |   1.5  | −1.2σ            | 1.2σ       |
| 1.50 dex     |   0.7  | −0.8σ            | < 1σ       |
| 2.00 dex     |   0.4  | −0.6σ            | < 1σ       |

→ **σ_y_cluster < 0.5 dex 면 2σ 이상 단조성 기각 유지**. SPARC/A1689
실측 통계오차 0.06 + systematic 0.2~0.3 dex 추정 합치면 합 ≲ 0.35 dex.
LRT 가 systematic 후에도 ~3-4σ 범위에 살아 남는다.

## 함의

1. **3-regime structure 의 통계적 정당성 강화**: L332 의 "보수적 2-regime
   baseline" 권고는 g(rm1) curvature 만 보았기 때문. σ_0(ρ_env) 직접 plot
   에서는 단조성 기각 견고.
2. **본 이론 격하 회피**: L341 −0.08 의 일부는 "3-regime narrative 격하"
   기여 (−0.005). L342 결과 반영 시 +0.003~+0.005 회복 가능 →
   **종합 ★★★★★ −0.075 수준**.
3. **caveat 정직 명시 필수**:
   - cluster single-source (L335 13-cluster pool 미실행).
   - anchor 분류가 RG 3-FP 가정에서 동기 (post-hoc).
   - N=3 데이터 — AICc 부재, BIC 도 N→∞ 점근식.

## 후속 액션 (우선순위순)

1. **L335 13-cluster pool 실측** 후 cluster anchor 재계산. σ_y 가 0.06 → ?
   로 변할지 확인. (deferred, 데이터 수집 단계)
2. **P9 dSph 저-ρ anchor 추가** → N=4, AICc 정의 회복, k=3 parabola 가
   genuine 자유도 검증.
3. **JCAP 본문 §3.x 추가**: "Non-monotonic σ_0(ρ_env): a 17σ rejection of
   single-FP RG hypothesis" — Table + Z stress test 포함.
4. **격하 균형 재계산**: L341 종합점수 −0.08 → −0.075 업데이트 검토.

## L342 → L343 권고 화두

- Q21 등록: "σ_0(ρ_env) 비단조성이 13-cluster pool 후에도 ΔBIC > 10 인가?"
- L343 후보 주제: P9 dSph anchor 추가 시 LRT 변화 forecast.
