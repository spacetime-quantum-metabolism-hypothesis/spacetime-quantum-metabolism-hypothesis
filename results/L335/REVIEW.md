# L335 — 8인 review (cluster anchor 다중화 forecast)

자율 분담: 데이터 가용성 / probe 결합 / 통계 forecast / honest limitation 4축으로
8인이 자유 접근. 사전 역할 지정 없음.

## 결과 요약 (results/L335/report.json)

### 데이터 가용성
- 후보 pool 13 cluster.
- Equilibrium-clean: 9.
- 3-probe (lensing + X-ray + SZ) 동시 가용: 9.
- 두 조건 교집합 (실효 N_eff 상한): **7** (A1689, A2029, A2142, A2218, A1835,
  A2390, RXJ1347-1145).

### Forecast (3 mode × N ∈ {1,2,4,7,10})

| 모드 | N=1 ΔAICc | N=10 ΔAICc | N=10 Tukey | N=10 PR |
|---|---|---|---|---|
| realistic (cluster-regime 고유, z~3.5) | 94.85 | 218.07 | 129.31 | 0.401 |
| universal (모든 anchor z~10) | 94.85 | 1032.63 | 213.18 | 0.894 |
| pessimistic (A1689 only outlier) | 94.85 | 106.08 | 27.03 | 0.123 |

### σ_cluster 일관성 (std/mean of |z|)
- universal: 0.18 (일관성 강함 — 보편 anchor 가설 PASS criterion)
- realistic: 0.57 (중간)
- pessimistic: 1.52 (불일관 — universality 부재)

## 8인 평가

**P (proponent)**: realistic mode 에서도 N=10 Tukey ΔAICc=129 → L327
"single-anchor dominance" 약점 *완전 해소*. PR 0.401 은 N=10 정규화 (1/N=0.1)
대비 4배 → effective n_eff ≈ 4. universal mode 면 PR 0.894 fully resolved.

**N (skeptic)**: pessimistic mode (A1689 가 *유일한 outlier*) 에서는 N=10 도
PR=0.123 → 여전히 single-source dominance. Tukey ΔAICc=27 은 cap 효과
누적이지 진짜 신호 아님. 어느 mode 가 진짜인지는 *실측 전 미정*.

**O (orthogonal)**: 9 cluster 가 3-probe 가용이지만 lensing + X-ray + SZ
joint analysis 는 cluster 당 σ_cluster 추출에 30-50% systematic budget.
실효 정보량은 "N_eff < N" 이며, hydrostatic mass bias (1−b≈0.85±0.10) 가
cluster 별 z-score 에 ±0.5 floor 추가.

**H (honest)**: 3 mode 중 어느 게 옳은지는 데이터로만 결정. realistic 이
가장 가능성 높지만 (cluster 들이 모두 같은 a0 를 보일 이유 없음 — A1689 의
특수 lensing geometry 가 신호 증폭한 것일 수 있음), pessimistic 가능성도
배제 못함. **L335 결론: forecast 만으로 ΔAICc=99 의 robustness 단정 불가**.

**M (methodologist)**: PR_target 기준 재정의 필요. N anchor 시 이상적 PR=1
(균등 분포). PR=1/N (single-source dominance). 본 결과 PR=0.401 (realistic)
는 effective_n=PR·N=4.0 → "4 anchor 이 χ² 의 대부분 제공". L323 d_eff=1
대비 정보량 4배 증가 — 의미 있는 개선.

**S (statistician)**: σ_consist=0.57 (realistic) 는 anchor universality 의
*marginal evidence*. universality 채택 임계: σ_consist < 0.3.
realistic 에서는 universality 가 *partially supported* — cluster regime 가 1개의
universal scale 인지, 또는 cluster 별 다른 scale 인지 데이터로 분리 필요.

**B (bayesian)**: BF(N=10 vs N=1) 의 marginalized evidence 를 (a) 모든 cluster
data 가 잘 fit 되면 ΔlnZ ~ +50 이상, (b) cluster 별 fit 이 잘 안 되면
universality penalty (1 a0 fit 13 clusters) 로 ΔlnZ < 0. *실측이 결정*.

**E (experimentalist)**: archive 데이터 즉시 가용:
- LoCuSS (Local Cluster Substructure Survey) — 50 cluster lensing.
- CLASH (HST) — 25 cluster strong+weak lensing.
- Chandra Cluster Cosmology Project — 100+ cluster X-ray.
- Planck PSZ2 (1653 cluster SZ), ACT-DR5, SPT-3G.
- 가용 sample size 는 13 후보 훨씬 초과. **sigma_cluster 추출은 archive
  re-analysis 만으로 가능, 신규 관측 불필요**.

## 정직 결론

- **데이터 가용성 PASS**: 7-13 cluster 즉시 가용 (3-probe ∩ equilibrium-clean = 7).
- **Forecast PASS (조건부)**: realistic / universal mode 면 ΔAICc/Tukey/PR
  모두 회복. pessimistic mode 면 N 증가해도 single-source dominance 잔존.
- **단정 불가**: 어느 mode 인지는 archive re-analysis 후 결정.
- **Net**: L327 의 "single-anchor 의존" 약점이 *해결 가능 path 명확*하지만
  *해결 보장 없음*. L336+ 에서 LoCuSS/CLASH/PSZ2 archive 실측 필수.

★★★★★ -0.07 (L331) → 변동 없음. forecast 만으로는 격하/회복 모두 미발생.
실측 후 mode 판정 시점 (L336+) 에 ★★★★★ -0.05 ~ -0.09 범위 이동 예상.
