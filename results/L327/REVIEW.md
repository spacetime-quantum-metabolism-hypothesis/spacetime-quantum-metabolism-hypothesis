# L327 — 8인 review (systematic σ inflation)

## 결과 요약 (results/L327/report.json)

| factor f (anchor σ × f) | ΔAICc |
|---|---|
| 1 | 97.46 |
| 2 | 19.75 |
| 5 | −2.00 |
| 10 | −5.11 |

임계 인플레이션:
- f_crit (ΔAICc=10) ≈ **2.53**
- f_crit (ΔAICc=2) ≈ 3.57
- f_crit (ΔAICc=0) ≈ 4.11

Robust statistics (residuals z ≈ {1, 10.05, 1}):
- Huber (k=1.345) ΔAICc ≈ **21.08** (cluster outlier 캡)
- Tukey biweight ΔAICc ≈ **4.85** (cluster outlier 완전 제거)

## 8인 평가

**P (proponent)**: f=2 인플레이션 (anchor σ 두 배)에서도 ΔAICc≈20 — 학계 강한 신호 유지.
σ underestimation 이 factor 2 미만이면 결론 영향 없음.

**N (skeptic)**: f=5 에서 BB 가 LCDM 대비 *불리*. 이는 *anchor σ 가 5배 underestimate
되어 있을 가능성*이 결과를 뒤집을 수 있음을 의미. cluster anchor (A1689) 단일
포인트가 χ²의 98% 제공 — *single-source dominance* risk.

**O (orthogonal)**: Tukey biweight (cluster outlier 제거) ΔAICc=4.85 — 학계
"strong" 컷(=10) 미달. 즉 cluster 한 포인트를 outlier 로 간주하면 BB 우위 *실질
무너짐*. Huber 는 캡만 하므로 21 유지 — robust stats 선택이 결론 좌우.

**H (honest)**:
- f=2 까지는 견고 (학계 typical σ underestimation factor 1.5–2 이하).
- f=5 면 죽지만, σ 5배 underestimation 은 비현실적 (anchor 측정의 systematic
  budget 통상 30–50%).
- 단, **cluster anchor 단일 포인트 의존**은 진짜 weakness — single-source
  dominance 는 reviewer 가 즉시 지적할 사안.

**M (methodologist)**: SPARC σ inflation 은 ΔAICc invariant (공통 분자 cancel) —
정직하게 보고. 실질 위협은 anchor 만.

**S (statistician)**: Robust 결과 split (Huber PASS / Tukey FAIL) 자체가
*전 분석이 cluster anchor 1개에 hinge* 한다는 증거. ΔAICc 99 의 진짜 정보 함량은
"cluster regime 이 SPARC universal a0 와 incompatible 하다"는 1-bit.

**B (bayesian)**: 3-anchor 시스템에서 1개 anchor 가 evidence 의 100% 제공이면
*posterior 는 사실상 1D*. ΔAICc 99 → effective ΔAICc ~ {Huber:21, Tukey:5}
범위가 진짜 evidence band.

**E (experimentalist)**: 추가 cluster anchor (Coma, Perseus, Virgo) 가 정직성
회복의 유일한 길. 단일 cluster 결과 인용은 위험.

## 정직 결론
- **σ × 2 robust**: PASS (ΔAICc=19.75, conventional cutoff 10 초과).
- **σ × 5/10**: FAIL — but unrealistic inflation.
- **Cluster outlier sensitivity**: Tukey 에서 ΔAICc=4.85 → **single-anchor
  dominance 가 진짜 약점**. L208 caveat ("by-construction") + L327 추가
  caveat ("cluster-driven") 둘 다 논문 명시 필요.
- **Net**: 인플레이션 자체로는 BB 우위 죽지 않음. 그러나 robust stats 와
  single-source dominance 가 ΔAICc 99 → effective 5–21 로 *재조정*.
