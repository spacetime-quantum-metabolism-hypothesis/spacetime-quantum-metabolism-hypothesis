# L370 ATTACK_DESIGN — Companion Paper Outline

**세션**: L370 (독립)
**주제**: SQT 수치 방법론 + 5-dataset MCMC + cluster pool 분석을 별도 companion paper 로 분리.
**날짜**: 2026-05-01
**정직 한국어 한 줄**: 메인 논문은 SQT 이론 + 핵심 결과만, companion paper 는 수치 방법론과 데이터셋 처리 디테일을 받는 분리 구조다.

---

## 0. 동기 (Why a companion paper?)

- 메인 논문(JCAP 또는 PRD Letter 계열) 은 **이론 + falsifiable 결과** 에 집중.
- 수치 적분 정확도, 5-dataset chi² 결합 규약, cluster pool (L33 14-cluster drift class 등) 의 SVD/participation ratio 분석 같은 **방법론 디테일** 은 본문 길이를 침범.
- referee 가 재현/방법론 질문 시 인용 가능한 self-contained 보조 논문이 필요.
- 본 attack 은 companion paper Sec 1–5 의 **구조만** 잡는다 (수식 도출 X — CLAUDE.md 최우선-1 준수: 방향만 제공).

## 1. Companion paper Sec 1–5 구조

### Sec 1. Introduction & Scope
- 메인 논문 결과 (L33 Q93 챔피언, L46–L56 audit/decision, L48 T17_full + T20 sigma8 grid scan) 를 references 로 받기.
- companion 논문이 **다루지 않는 것** 명시: SQT 이론 도출, ψ^n a priori test, UB 변종 탐색.
- companion 논문이 **다루는 것**: (i) BAO/SN/CMB compressed/RSD/WL 5-dataset chi² 파이프라인, (ii) 수치 적분/ODE/grid scan 정합성, (iii) cluster pool 통계 (SVD, participation ratio).

### Sec 2. Numerical methods
- 적분 규약: `cumulative_trapezoid`, `N_GRID=4000`, `z_grid up to z_eff.max()+0.01` (L33 표준).
- ODE 규약: forward shooting, OMP/MKL/OPENBLAS_NUM_THREADS=1, multiprocessing spawn pool.
- ratio clip / phantom-crossing guard / numpy-2.x trapezoid 호환.
- 재현성 체크리스트: emcee `np.random.seed`, dynesty `default_rng`, json `_jsonify`.

### Sec 3. Five-dataset MCMC pipeline
- 데이터: DESI DR2 BAO (13pt + cov), DES-SN5YR (DESY5/zHD + analytic M marginalization), Planck compressed CMB (theta_*, ω_b prior, Hu-Sugiyama 0.3% theory floor), DESI/SDSS RSD f σ_8, DES-Y3 cosmic shear S_8.
- chi² 합산 규약: `chi2_joint` (BAO+SN+CMB+RSD) vs `chi2_joint_with_shear` (+WL) — 보고 시 어느 쪽 사용했는지 명시 (CLAUDE.md L5 규칙).
- 사전분포/경계: Om∈[0.28, 0.36] tight box, h∈[0.64, 0.71], smooth penalty.
- 방어 패턴: chi² 실패 시 sentinel 금지, `return -np.inf`. 멀티스타트 `best=(1e8, None)` 방어.

### Sec 4. Cluster pool analysis
- 후보군 구성: L46–L56 의 alt 후보들 + L48 T17_full + T20 sigma8 grid scan 결과.
- canonical drift class 식별: SVD `n_eff`, participation ratio (L5 Alt-20 14-cluster class, n_eff=1, PR=1.017).
- 단일 대표 축약 규칙: 14-cluster 류는 single representative 보고. "독립 후보 N개" 주장은 SVD 검증 후에만.
- DR3 pairwise discrimination Fisher 예측 (mainstream 후보 간 0.19σ → 데이터로 구분 불능 명시).

### Sec 5. Reproducibility & code release
- 저장소 구조: `simulations/L33`, `simulations/L46`–`L56`, `results/L33`–`L56`.
- 환경 고정: Python 3.14, numpy 2.x, scipy, emcee, dynesty 3.0, multiprocessing spawn.
- 데이터 출처 (CLAUDE.md 준수): DESI BAO github.com/CobayaSampler/bao_data, DES-SN5YR `sn_data/DESY5/`.
- 한계 정직 기록: μ_eff≈1 → S8 tension 미해결, hi_class 미설치 시 K19 provisional, DR3 미공개 단계.

## 2. 메인 논문과의 분리 원칙

- 메인 논문은 SQT 이론 prediction 과 핵심 chi² 개선 (예: L33 Q93 dAICc) 만.
- companion 논문은 **그 결과를 어떻게 얻었는가** 만.
- 중복 금지: 같은 표/수치를 양쪽에 싣지 않는다. companion 은 메인의 표를 인용.

## 3. 산출 파일 (이 세션)
- ATTACK_DESIGN.md (본 문서)
- NEXT_STEP.md
- REVIEW.md

## 4. 비-목표 (out of scope, 본 세션)

- 실제 companion paper 본문 작성 (LaTeX) — outline 만.
- 새 시뮬레이션 실행.
- L33 결과 재해석 또는 L48 추가 grid scan.
