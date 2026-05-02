# L342 ATTACK DESIGN — sigma_0(rho_env) 비단조성의 통계적 유의성

**컨텍스트**: L341 종합 ★★★★★ −0.08, JCAP 진입 90–94%. L332 권고("2-regime
baseline 채택, 3-regime 은 P11 NS forecast 후 reserve")는 보수적이다. 사용자
통찰: 3-regime 의 *진정한* 이론적 근거는 g(rm1) 의 두 break 위치가 아니라
**σ_0(ρ_env) 자체의 비단조성** 이다. 단조 σ(ρ) 는 RG β-function 의 단일 FP
구조와 동치 — 비단조 σ(ρ) 는 multi-FP topology 의 *직접 관측 증거*. 이
loop 는 그 비단조성에 likelihood ratio 정량을 부여한다.

---

## 8인 독립 사고

### P (frequentist)
- 데이터: 3 anchor (cosmic 8.37±0.06, cluster 7.75±0.06, galactic 9.56±0.05).
- 가설 H0 = monotonic σ(ρ); H1 = non-monotonic.
- 단순 likelihood ratio: H0 = 직선 (k=2), H1 = parabola/V-shape (k=3).
- N=3, k=3 saturates → AICc 정의 불가 영역. **AIC + BIC + Δχ² 동시 보고** 필수.

### X (model-comparison)
- M1 (linear monotonic, k=2) vs M1b (tanh monotonic, k=2) vs M2 (parabola, k=3).
- M1b 는 sigmoid bound — y 가 plateau 가지만 여전히 monotonic. M1 과 chi² 거의
  동일 예상 (cluster outlier 가 monotonic shape 에 둔감).
- BIC 가 가장 정직한 비교: ΔBIC > 10 → "decisive" (Kass-Raftery).

### Y (Bayesian)
- 평탄 prior 하에서 Bayes factor ≈ exp(−ΔBIC/2). cluster point 가
  outlier 인 한 BF ~ 100 이상 자명.
- 단 이 BF 는 **데이터-내부 통계량** — 미시 이론에서 *왜 V-shape* 인가는
  별개. RG 3-FP 가정과의 **structural prior** 까지 반영하면 BF 더 커진다.

### H (anchor predetermined)
- 본 테스트의 anchor 는 **post-hoc 결정**. cosmic/cluster/galactic 분류 자체가
  RG 3-FP 가정에서 동기. 따라서 LRT 결과는 "given regimes are physical, are
  they non-monotonic?" 에 답할 뿐, "regimes 자체가 실재인가" 는 답 못함.
- L334 priori 한계 (σ_0 만 priori, 위치는 post-hoc) 와 동일 수준.

### Z (systematics)
- σ_y = 0.06 dex 가 *통계* 오차. 시스테매틱 (SPARC sample-selection,
  cluster lensing inversion, IGM rho 추정) 은 별도. cluster point 에 ±0.3 dex
  systematic 가능성 — 그래도 LRT 견고성 확보 필요 (아래 Z stress test).

### B (B-team challenge)
- "cluster value 7.75 가 단순 측정 오류일 가능성" — A1689 single-source.
  L335 13-cluster pool 결과 전 까지 **provisional**. 단일 cluster outlier
  가 LRT 의 99% 를 끌어가는 구조 자체가 위험.
- 대안 H0': cluster 점이 misidentified, 실제는 단조. 이 가설은 데이터 내부에
  서는 분리 불가 — 외부 검증 (P9 dSph 저-rho, NS saturation 고-rho) 필수.

### G (geometric/physics)
- RG flow 가 σ-축에서 3 FP 갖는다면, σ(ρ_env) curve 는 ρ 가 우주 진화/
  수직 채널을 따라 FP 사이를 hopping — **반드시 비단조**. 단조 σ(ρ) 는 RG
  단일 FP (or no-FP) 와 동치.
- σ_0 ∝ G·t_P holographic 은 *anchor scale* 만 priori. 비단조성은 b/c 비율의
  signature.

### W (writer/positioning)
- JCAP 본문 정직 표기: "3 anchor LRT Δχ²=288 (17σ formal); 한계는
  N=3 + cluster single-source. 13-cluster pool (L335) 후 실효 dof 회복".
- 강한 주장 가능: "σ(ρ) 단조성은 17σ 로 기각된다 — 단, anchor *집합* 자체
  의 post-hoc 선택성이 prior odds 에 영향".

---

## 합의 핵심 디자인 (8/8)

1. **세 anchor 점 사용**:
   - cosmic   log10 σ_0 = 8.37 ± 0.06,  log10 ρ_env ≈ −27
   - cluster  log10 σ_0 = 7.75 ± 0.06,  log10 ρ_env ≈ −24
   - galactic log10 σ_0 = 9.56 ± 0.05,  log10 ρ_env ≈ −21
2. **모델**: M1 linear, M1b tanh (둘 다 k=2 monotonic), M2 parabola (k=3
   non-monotonic).
3. **점수**: χ², AIC, BIC, ΔBIC, Δχ² (LRT).  AICc 는 N=3,k=3 에서 정의 불가
   → 정직 표기.
4. **Z stress test**: σ_y_cluster 를 0.06 → 2.0 dex 인플레이션 시 ΔBIC 추적.
5. **외부 의존**: 결과의 cluster-driven 구조를 명시하고, L335 13-cluster
   재-fit 후 재실행 권고.

---

## Q-questions (Q21 추가 candidate)

- **Q21**: "σ_0(ρ_env) 가 ΔBIC > 10 으로 비단조" — 본 loop 가 1-anchor-set
  에서 결정. 13-cluster pool 후 robust 재확인 필요.

종합: 단조성 기각이 통계적으로 매우 강함. 단 anchor 선택성+cluster single-
source 가 해석 caveat.
