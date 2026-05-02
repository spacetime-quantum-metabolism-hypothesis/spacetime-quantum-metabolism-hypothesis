# L347 — 8인 자율 review: A1689+Coma+Perseus 3-cluster joint σ_cluster

자율 분담: 데이터 점추정 / 분산 통계 / single-source 정량 / honest 한계 4축.
역할 사전 지정 없음.

## 입력 (문헌 점추정 — 신규 archive re-analysis 아님)

| Cluster | z | M_500 (10^14 M_sun) | T_X (keV) | σ_v (km/s) | 주 systematic |
|---|---|---|---|---|---|
| A1689 | 0.183 | ~9 (lensing) | ~9.5 | ~1430 | strong-lensing line-of-sight 정렬 가능 |
| Coma (A1656) | 0.023 | ~7 (HSE/lensing) | ~8.5 | ~1000 | dual-BCG quasi-merger |
| Perseus (A426) | 0.018 | ~6.5 (HSE) | ~6.8 | ~1280 | cool-core + sloshing |

(값은 published literature 의 *대표 중앙값*. 본 loop 는 archive fitting 미수행 —
L348+ 의 LoCuSS/CLASH/PSZ2 re-analysis 에서 정밀화.)

## 8인 평가

**P (proponent)**: 세 cluster 모두 m_500 ~ 6-9 × 10^14, T_X ~ 7-10 keV 범위에서
같은 차수. cluster regime 의 보편 anchor 가설 *first-order consistent*.
σ_v 차이 (Perseus 1280 vs Coma 1000) 는 ~25% — dex 로는 0.10 dex.
universality 임계 0.3 dex 안.

**N (skeptic)**: 그러나 단순 mass/T_X 일관성은 **anchor 신호의 일관성과
다르다**. L208 anchor χ² 는 cluster regime 의 BB normalization 에서 추출.
mass/T_X 가 비슷해도 anchor z-score 는 cluster geometry, lensing detail,
HSE bias 에 결정적으로 의존. *진짜 anchor σ 추출은 수행 안 됨* — 본 review 는
proxy 일관성만.

**O (orthogonal)**: A1689 의 lensing 신호는 line-of-sight filament 정렬로 ~30%
boost 가능 (Lemze+09 등). 이 경우 A1689 "anchor" 가 specific geometric
artifact 일 가능성 — Coma/Perseus 는 그런 정렬 없음 → A1689 만 outlier 경향
*예상* (pessimistic mode 선호).

**H (honest)**: 본 loop 는 *문헌 proxy 일관성* 만 제시했지 σ_cluster 점추정 자체를
계산하지 않았다. "σ_inter/σ_mean < 0.3 dex" 라는 핵심 질문에 정량 답변 미제공.
보고할 수 있는 것은:
- **mass/T_X proxy dispersion**: 0.10-0.15 dex (universality 와 양립).
- **anchor z-score dispersion**: **미측정** (이번 loop 에서 풀지 못함).
**결론을 "PASS" 로 보고하면 결과 왜곡**. 정직 라벨: *unresolved*.

**M (methodologist)**: PR_3 metric 정의됨 (z_A1689² / Σ z_i²). 그러나
z_Coma, z_Perseus 가 미측정 → PR 계산 불가. 본 loop 의 정량 산출은
proxy mass dispersion 한 가지뿐.

**S (statistician)**: N=3 의 σ_inter 95% CI 는 Bayesian inverse-chi²
under flat prior 하에 *factor 3 폭*. 점추정 0.10 dex 이라도 95% CI 는
대략 [0.04, 0.30] dex. universality 임계 0.3 에 *경계*. N=3 으로는 mode
판정 통계력 부족 — 최소 N=6-7 필요.

**B (bayesian)**: 사전 prior P(realistic)≈0.5, P(universal)≈0.3,
P(pessimistic)≈0.2 (L335 정성). proxy 일관성 0.10-0.15 dex 정보는 likelihood
ratio 미미 (anchor 신호 직접 측정 아니라서). posterior ≈ prior. **본 loop
의 베이지안 갱신은 negligible**.

**E (experimentalist)**: 실측 archive 작업 시 1 cluster 당 lensing+X-ray+SZ
joint fit 약 2-4 주 노력. N=3 deep fit 은 6-12 주. 본 프로젝트 페이스
(L341 정직 보고: 9 loop 미수행) 고려 시 archival re-analysis 는 별도
계획/리소스 필요.

## 정직 결론

- **mass/T_X proxy 일관성**: PASS (0.10-0.15 dex).
- **anchor σ_cluster 직접 일관성**: **미측정** (본 loop 에서 정량 부재).
- **single-source dominance 해소 정량 (PR_3)**: 미산출.
- **Mode 갱신**: negligible (likelihood 약함).
- **★★★★★ 등급 변동**: 변동 없음 (-0.08 유지). proxy 만으로 회복/격하 모두
  근거 부족.
- **honest limitation 추가**: *L347 anchor σ 직접 추출 미수행 — proxy 만
  보고*. limitations 12 (L341 11 + 신규 1).

## 한 줄
mass/T_X proxy 는 universality 와 양립하나 anchor σ 직접 일관성은 본 loop 가 풀지 못했다.
