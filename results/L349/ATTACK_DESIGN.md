# L349 ATTACK DESIGN — CLASH 25 cluster σ_cluster joint fit

**날짜**: 2026-05-01
**세션 분류**: SQMH L349 (독립)
**한 줄 요약 (정직)**: CLASH 25개 클러스터 mass profile 데이터에서 클러스터 스케일 SQMH 보정 강도 σ_cluster 와 그 불확실성을 joint fit 으로 추정한다.

---

## 1. 동기 (Why CLASH)

- CLASH (Postman+ 2012, ApJS 199 25; Umetsu+ 2016 ApJ 821 116; Merten+ 2015 ApJ 806 4) 는 25개 X-ray-selected 또는 lensing-selected 갤럭시 클러스터의 weak+strong lensing 합성 mass profile 을 0.02 < r/r_vir < 1 범위에서 stacked + individual 로 공개.
- 클러스터 스케일 (r ~ 100 kpc – 2 Mpc) 은 SQMH 의 ψ-기반 보정이 갤럭시 (~kpc) 와 우주론 (~Gpc) 사이의 **결손 스케일 (missing-scale gap)** 에 해당. L34X 시리즈에서 BAO/SN/CMB 스케일은 침식되었지만 클러스터 스케일 검증은 미수행.
- 산출 목표: 단일 스칼라 σ_cluster ± 1σ. 이 값이 0 과 양립 가능하면 SQMH 클러스터 채널 KILL, 양립 불가능하면 후속 L350+ 에서 강체 (강제) 채널로 승격.

## 2. 탐색 방향만 (지도 금지)

> CLAUDE.md 최우선-1 준수. 아래는 **방향**과 **현상 이름**만이며 수식/숫자/계수 없음.

- (방향 A) NFW 또는 Einasto baseline mass profile 위에 SQMH 보정항을 가법적으로 또는 곱셈적으로 부여하는 두 옵션을 모두 열어둔다.
- (방향 B) 보정의 스케일 의존은 클러스터 viral radius 또는 scale radius 를 무차원화 기준으로 사용하는 가능성을 팀이 자율 도출.
- (방향 C) σ_cluster 는 25 클러스터 전체에 공통인 단일 nuisance-free 진폭 파라미터로 해석 (cluster-by-cluster σ_i 도출은 L350 단계).
- (방향 D) joint fit 의 자유도 카운팅은 클러스터당 NFW (M_vir, c_vir) + 공통 σ_cluster, AICc/BIC 패널티 명시.

수식, 함수형, 파라미터 범위, 부호 가정은 본 문서에 적지 않는다. 8인 팀이 독립 도출.

## 3. 데이터

| 출처 | 표본 | 반경 범위 | 형태 |
|---|---|---|---|
| Umetsu+ 2016 (ApJ 821 116) | CLASH 16 X-ray-selected | 0.2–2 Mpc | Σ(R), ΔΣ(R) + cov |
| Merten+ 2015 (ApJ 806 4) | CLASH 19 (overlap) | 0.02–2 Mpc | κ(r) joint SL+WL |
| Niikura+ 2015 (ApJ 821 87) | CLASH 20 stacked | full | NFW c-M relation |

기준: Umetsu 2016 cov + Merten 2015 SL+WL κ 결합. 25 클러스터 union 은 두 카탈로그 + 추가 강한렌즈 후속 (Zitrin+ 2015) 에서 인용. 데이터는 공식 archive 또는 저자 공개분만 사용 (CLAUDE.md 재발방지: 임의 추정값 금지).

## 4. 자유도 / fit 구조

- per-cluster nuisance: (M_vir,i, c_vir,i) — 25 × 2 = 50.
- 공통: σ_cluster (1).
- 총 51 파라미터. 데이터 포인트 ~ 25 × 15 bins ≈ 375.
- joint chi² = Σ_i chi²_i(M_i, c_i, σ_cluster). σ_cluster 만 marginalize 하면 25 클러스터에 걸친 profile 형태 변형이 1차원 진폭으로 압축.
- AICc 패널티: 51 → AICc = chi² + 2k(k+1)/(N-k-1). LCDM-NFW (k=50) 대비 Δk=1.

## 5. 8인 팀 자유 분담 (역할 사전 지정 금지)

- 8인 팀에 다음 **방향**만 전달: "CLASH 25 mass profile 에서 SQMH 클러스터 보정의 단일 진폭 σ_cluster 와 1σ 를 도출하라."
- 팀이 자율로: (a) NFW vs Einasto baseline 결정, (b) σ_cluster 진입 함수형, (c) prior 범위, (d) Σ vs κ vs ΔΣ 채널 선택, (e) cov 처리.
- 토의 후 자연 발생하는 분업만 인정 (CLAUDE.md 최우선-2).

## 6. 코드리뷰 4인팀 체크포인트

- Umetsu cov 행렬 부호 / 정칙성.
- (M_vir, c_vir) prior 가 boundary 박힘 검사 (재발방지: L3 boundary 박힘).
- σ_cluster=0 reference chi² 와 best-fit chi² 차이가 AICc 패널티(~2) 보다 큰지.
- numpy 2.x trapezoid, ASCII 변수명, multiprocessing spawn + 스레드=1.

## 7. KILL / PASS 기준

| 코드 | 조건 | 의미 |
|---|---|---|
| K-CL1 | σ_cluster best-fit 의 1σ 가 0 포함 | SQMH 클러스터 채널 KILL |
| K-CL2 | Δχ²(σ_cluster vs 0) < 2 | AICc 패널티 미달 → LCDM-NFW 채택 |
| P-CL1 | Δχ² > 9 (3σ) AND boundary 미박힘 | L350 강체 채널 승격 |
| P-CL2 | 2 ≤ Δχ² ≤ 9 | provisional, DR3 또는 Euclid 클러스터 stack 으로 재판정 |

## 8. 산출물

- `results/L349/sigma_cluster_posterior.json` (L350 이후)
- `results/L349/REVIEW.md` (본 세션 종료 시점 리뷰)
- `results/L349/NEXT_STEP.md` (다음 액션)

## 9. 위험 / 사전 등록

- CLASH 25 는 X-ray selected 편향 → hot, relaxed 클러스터 위주. Selection bias 가 σ_cluster 에 흡수될 가능성. NEXT_STEP 에서 LoCuSS / HSC-XXL 비교 cross-check 필요.
- baryonic feedback (AGN, cooling) 가 r < 0.1 r_vir 에서 NFW 와 deviation. 보수적으로 r > 0.1 r_vir 만 fit.
