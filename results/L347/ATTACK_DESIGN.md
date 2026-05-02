# L347 — ATTACK DESIGN: A1689 + Coma + Perseus 3-cluster joint σ_cluster

## 상위 컨텍스트
- L341 ★★★★★ -0.08 carry-over (L335 cluster pool 13개, 3-probe∩equilibrium-clean = 7).
- L327 진단 잔존: anchor χ² ~98% 가 A1689 단일 cluster.
- L335 forecast: realistic mode σ_consist=0.57 (marginal), universal mode 0.18 (PASS),
  pessimistic 1.52 (불일관). 어느 mode 인지 *실측 전 미정*.
- L347 임무: **포레스트 axis 를 "13 cluster N-scan" 에서 "3 cluster deep-dive" 로 좁혀
  single-source dominance 해소를 1차 정량**.

## 왜 N=3 인가 (정직)
- N=13 풀스캔은 archive re-analysis (LoCuSS+CLASH+PSZ2+Chandra+ACT/SPT) 단위로
  여러 loop 필요. L347 단일 loop 안에서 가능한 것은 *문헌 기반 점추정*.
- 3 cluster 선정 기준:
  - **A1689**: 기존 anchor (L208 ΔAICc=99 의 출처). reference 점.
  - **Coma (A1656)**: z=0.023, 가장 잘 측정된 nearby massive cluster.
    lensing (Okabe+10, Kubo+07), X-ray (Snowden+08), SZ (Planck PSZ2) 모두 보유.
  - **Perseus (A426)**: z=0.018, X-ray brightest. Chandra deep, lensing weak,
    SZ (Planck) 보유. cool-core + sloshing 알려짐 → equilibrium 가정 한계 노출용
    *adversarial* 샘플.
- **선정 의도**: 1 reference + 1 clean nearby + 1 known-systematic-rich.
  세 cluster 가 universal σ_cluster 를 보이면 *모드 판정 강함*.
  Perseus 만 outlier 면 systematic 한계 정량.

## 8인 자유 분담 (역할 사전 지정 없음)

### A1. σ_cluster 추출 채널
- 3 probe (lensing M(<r), X-ray HSE, SZ pressure) 각각에서 cluster regime
  표지값 추출. universal scale 가설 하에 세 값이 일관해야 함.
- A1689 는 strong lensing arc 풍부 → lensing 채널 우월.
- Coma 는 X-ray HSE 채널 정밀 (1-b≈0.85±0.10).
- Perseus 는 X-ray 깊지만 cool-core → HSE 적용 영역 r > 0.3 r_500 제한.

### A2. 단일 cluster σ_cluster 의 정의
- BB cluster regime 정상화 스케일. 세 cluster 모두 같은 dex 평면에서 비교.
- 추출은 *해석적 점추정* (M(<r), T_X, σ_v, P_e profile literature value 결합).

### A3. 3-cluster 분산 통계
- 핵심 metric: **σ_inter / σ_mean** (dex 단위).
- PASS criterion: < 0.3 dex (L335 universality 임계).
- N=3 분산은 freedom 2 → 신뢰구간 매우 큼. point estimate 일관성만 1차 진단.

### A4. Single-source dominance 해소 정량
- Participation ratio PR_3 = (Σ z_i)² / (3·Σ z_i²) where z_i = |residual|/σ_i.
- A1689 단독 시 PR=1.00 (정의). 3 cluster 균등이면 PR=1.00 (모두 같은 z),
  A1689 압도면 PR≈0.34 (1/3).
- 적절 metric: A1689 contribution share = z_A1689² / Σ z_i².

### A5. Pessimistic mode 검증
- 만약 Coma+Perseus 가 LCDM 와 일관 (z<2σ) 이고 A1689 만 z>5σ 이면
  L335 pessimistic mode 가 데이터에 의해 선호 → universality 가설 약화 →
  *L208 ΔAICc=99 가 A1689 specific anomaly* 결론.

### A6. Universal mode 시나리오
- 세 cluster 모두 |z|>2σ + σ_consist<0.3dex 면 universal anchor regime 입증.
- 이 경우 L335 universal forecast (N=10 ΔAICc=1032) 가 plausible path.

### A7. Honest 한계 (반드시 기록)
- N=3 은 통계적으로 *작다*. mode 판정에 결정적이지 않음.
- 문헌 점추정에는 cluster 별 systematic budget (lensing line-of-sight,
  X-ray hydrostatic bias, SZ calibration) 30-50% 미반영 위험.
- Perseus cool-core → equilibrium 가정 위반. 결과를 universal claim 의
  반례로 해석하면 systematic 인지 진짜 신호인지 분리 불가.
- Coma merger history (NGC 4889 + 4874 두 BCG) → quasi-equilibrium.
- 따라서 L347 결과는 **mode probability 갱신** 수준이지 mode 확정 아님.

### A8. 결과 해석 분기
- σ_inter/σ_mean < 0.3 dex (3개 모두 일관): universal mode prior 상승 →
  ★★★★★ -0.06 ~ -0.07 (회복 0.01-0.02).
- 0.3 ≤ ratio < 0.7 (marginal): 현 -0.08 유지. realistic mode 잔존.
- ratio ≥ 0.7 (Perseus or Coma 가 A1689 와 dex 단위로 다름): pessimistic mode
  확률 상승 → ★★★★★ -0.09 ~ -0.10 (격하 0.01-0.02).

## 산출물
- `results/L347/ATTACK_DESIGN.md` — 본 문서
- `results/L347/REVIEW.md` — 8인 자율 분담 평가
- `results/L347/NEXT_STEP.md` — L348+ 계획 (A2029, A2142, A1835 추가 → N=6)

## 정직 한 줄
N=3 deep-dive 은 mode 확률을 갱신할 뿐 universality 를 입증/반증하지 않는다.
