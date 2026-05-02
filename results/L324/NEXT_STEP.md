# L324 — NEXT_STEP

**상태**: 본 loop = 설계 + 8인 review 완료. 실측 시뮬레이션은 후속 세션.

---

## 즉시 실행 큐 (L325-L327)

### L325 — Cross-dataset σ_0 pairwise + leave-SPARC-out
**범위**: K1, K2, K3, K9.
**입력**:
- SPARC: 175 disk (기존 BB anchor pipeline)
- DESI BAO: bao_data 13pt + 전체 cov (CobayaSampler 공식)
- Planck compressed CMB: chi2_joint 'cmb' 키 (hi_class 대체 금지, L6 룰)

**절차**:
1. SPARC-only BB fit → (σ_0^S, error)
2. DESI-only BB fit (배경 E(z) → ratio 변환) → (σ_0^B, error)
3. CMB-only BB fit (Z_CUT=5 fixed) → (σ_0^C, error)
4. Pairwise tension: (σ_0^S - σ_0^B) / sqrt(err_S² + err_B²) 등 3쌍
5. Joint (BAO+CMB only, no SPARC) BB fit → σ_0^{B+C} posterior 폭 확인 (K9)

**병렬**: 4 fit 동시, multiprocessing.spawn Pool(4), OMP=1.

**합격**: K1-K3 모두 <2σ + K9 finite posterior. fail 시 결과 정직 기록.

### L326 — Strata + tracer-block 변동 (K4, K5)
**범위**: SPARC strata jackknife + DESI 2-block.
**합격**: K4 <2.4σ effective (Bonferroni), K5 <1σ.

### L327 — Z_CUT 민감도 + Q_DMAP (K6, K7, K8)
**범위**: Z_CUT ∈ {2, 3, 5} CMB chi2 차이로 σ_0 응답 + Q_DMAP / suspiciousness.
**합격**: K6 <0.5σ, K7 <9, K8 <5.

---

## Deferred (별도 long session)

- **L328+**: A6 selection-corrected V_eff reweighting. selection function S(M, z)
  모델링 필요 (SPARC: H I flux, DESI: tracer color/flux cut, Planck: full-sky).
  비용 큼.
- **L329+**: A8 distance-ladder ±5% perturbation. SPARC 거리 재로딩 + propagation.

---

## 코드 가드 (CLAUDE.md 룰 미리 명시)

- multiprocessing: `mp.get_context('spawn').Pool(4~9)`.
- 환경변수: `OMP_NUM_THREADS=MKL_NUM_THREADS=OPENBLAS_NUM_THREADS=1`.
- numpy 2.x: `np.trapezoid` 직접 호출.
- DESI fit: D_V(BGS) + D_M/D_H(나머지) 13pt + 전체 cov.
- CMB chi2: `chi2_joint(...)['cmb']` 직접. Hu-Sugiyama 재계산 금지.
- print(): ASCII only. 라벨만 unicode 허용.
- in-place 정규화 금지: `D = sol.y[0].copy(); D /= D[-1]`.
- ξ_q 양수/음수 분리 보고. SQMH-consistent branch 명시.
- chi2 None/nan → `return -np.inf` (sentinel 합산 금지).
- emcee 사용 시 `np.random.seed(42)` 내부 seed.
- 결과 다르면 base.fix.md 정직 기록.

---

## 결과 처리 분기

### 시나리오 A: 모든 K 통과
- σ_0 cross-dataset consistent 확정
- 본 이론 +0.005~+0.010 향상 (★★★★★ -0.04~-0.045)
- JCAP acceptance 95-98% 상향
- Sec 4.5 신규 "Cross-dataset robustness" 본문 추가

### 시나리오 B (예측 ~60%): K9 fail or K2 fail
- 영구 limitation #5 추가: "BB σ_0 는 SPARC anchor-driven, BAO+CMB 만으로 미결정"
- Sec 6.5 신규 limitation 항목
- Acceptance -2% (93-97% → 91-95%)
- 본 이론 -0.005 (★★★★★ -0.055)
- mock 100% finding 과 함께 정직 disclosure block 으로 묶음

### 시나리오 C: K1 또는 K3 fail
- BAO 또는 CMB 와 SPARC 가 직접 tension
- 영구 limitation #5 + #6 추가
- Acceptance -3~-5% (90-92%)
- 그래도 reviewer trust 로 buffer (235-loop 누적)

---

## 한 줄 결정 (8인 합의 후)

본 L324 는 설계 + review 만. 실측은 L325 부터. K9 가 가장 중요한 결정 KPI.
사전 fail 위험 ~60% 정직 기록 — 결과 왜곡 금지 룰 준수.
