# base.l5.command.md — L5 Phase-5 Production MCMC + Evidence + Submission-Ready Paper 실행 지시서

> `/bigwork-paper` 스킬에 투입할 **최종 확정 지시안**.
> 사용자 confirm 전부 생략. 묻지 말고 끝까지 자동 진행. 언어는 Python.

---

## 실행 명령

```
/bigwork-paper base.l5.command.md 에 기재된 L5 production MCMC +
Bayesian evidence + submission-ready paper 파이프라인을 끝까지 수행.
사용자 confirm 전부 생략. 묻지 말고 진행. 언어는 Python.
base.l4.result.md (Phase-5 main 2 + re-eval 2), simulations/l4_alt/
alt20_results.json (alt-20 생존자 15), base.md, base.fix.md,
base.fix.class.md, refs/l4_kill_criteria.md, refs/alt20_catalog.md,
Phase 2-4 및 L4 기존 결과 전부 참고. L4 코드베이스 재사용, L5 이름
으로만 신규 파일 기록.
```

---

## 🎯 근본 목적

**L4 종료 시점에서 확정된 생존자 전원에 대해**
- production-grade MCMC (48 walkers × 2000 steps, R̂ < 1.02)
- Bayesian evidence (nested sampling) 기반 엄밀 model comparison
- C11D / C26 재평가 pending 해소
- alt-20 degenerate cluster 축약 분석 ("canonical drift class")
- KiDS-1000 / DES-Y3 cosmic-shear S_8 채널 추가
- DESI DR3 Fisher forecast (w_0, w_a 1σ 예측 + discrimination power)
- **논문 submission-ready 완성본** (v1 → arXiv 업로드 가능한 상태)

**그리고 최종 winner 1-3 개를 SQMH 공식 예측으로 확정.**

### 심층 의도

L4 는 "L3 toy 가 full theory 에서도 유지되는가" 를 확정했다. 결과:

1. **Mainstream 2 확정** (C28 RR, C33 f(Q))
2. **Mainstream 2 재평가 보류** (C11D K3 template, C26 ansatz 재공식화)
3. **Alt-20 0-파라미터 후보 4 hard + 11 soft** 가 **같은 drift 방향**으로
   수렴하여 C28 수준의 Δχ² 를 달성

L5 의 핵심 질문은:

- **Q5.1**: Alt-20 의 "canonical drift class" (A01/A05/A06/A12/A16/A17/A20
  이 동일 posterior 로 수렴) 는 **진짜로 한 개의 물리적 효과인가, 아니면
  여러 독립적 drift 구조의 우연한 축합인가**?
- **Q5.2**: C28 1-parameter 이 0-parameter 대안(A01)보다 **Bayesian
  evidence 기준**으로 실제로 선호되는가?
- **Q5.3**: C11D hi_class 재판정이 K3 를 해소할 수 있는가? 해소 시
  최강 후보(Δχ²=−22.92) 로 승격되는가?
- **Q5.4**: DESI DR3 에서 이 후보들이 **실제로 구분 가능한가** (Fisher
  forecast)?
- **Q5.5**: Cosmic-shear S_8 데이터를 추가해도 drift-류 (μ=1) 후보가
  생존하는가? σ_8 tension 악화는?

L5 는 이 5 질문에 수치적 답을 준 뒤, 가장 강한 1-3 후보를 **paper v1**
에 통합하여 arXiv 업로드 가능한 상태로 마무리한다.

**최종 결과는 반드시 `base.l5.result.md` 단일 파일에 통합 기록**.
중간 실행 로그는 `base.l5.todo.result.md`. 논문 v1 은 `paper/` 기존
9 섹션 업데이트 + `paper/10_appendix_alt20.md` 추가.

---

## 📋 L5 생존자 목록 (L4 최종 확정)

### Tier 1 — Mainstream production (2)

| ID  | Family                 | L4 Δχ² | L4 w_0, w_a      | Params |
|-----|------------------------|--------|------------------|--------|
| C28 | Maggiore RR non-local  | −21.08 | (−0.849, −0.242) | 1      |
| C33 | f(Q) teleparallel      |  −6.28 | (−0.984, −0.262) | 2      |

### Tier 2 — Alt-20 hard-K2 (4)

| ID  | Closed-form               | L4 Δχ² | L4 w_0, w_a      | Params |
|-----|---------------------------|--------|------------------|--------|
| A01 | `1 + m·x`                 | −21.12 | (−0.899, −0.115) | 0      |
| A05 | `√(1 + 2m·x)`             | −21.03 | (−0.900, −0.124) | 0      |
| A12 | `1 + erf(m·x)`            | −21.62 | (−0.886, −0.133) | 0      |
| A17 | `1 + m·x·exp(−x²)`        | −21.26 | (−0.895, −0.178) | 0      |

### Tier 3 — Re-evaluation pending (2)

| ID   | Family                  | L4 Δχ² | L4 상태            |
|------|-------------------------|--------|--------------------|
| C11D | Disformal IDE           | −22.92 | KILL K3 (template) |
| C26  | Perez-Sudarsky diffusion| ~0     | KILL K10 (ansatz)  |

### Tier 4 — Alt-20 K2-soft degenerate class (11)

A03, A04, A06, A08, A09, A11, A13, A15, A16, A19, A20.
(A04 는 |w_a|=0.469 로 K2 최강이지만 Δχ²=−8.89 로 약함 → 별도 다룸.)

**총 L5 대상 19 후보** (2 main + 4 alt-hard + 2 re-eval + 11 alt-soft).

---

## 📐 Kill / Keep 기준 (L4 승계 + 신규 K13-K16)

**실행 시작 전에** `refs/l5_kill_criteria.md` 에 아래 기준 commit 하여
고정. 실행 도중 임계값 조정 **금지**.

### L4 에서 승계 (K1-K12)

L4 기준 그대로. `refs/l4_kill_criteria.md` 참조.

### L5 신규 KILL 조건

| ID | 조건 | 임계값 |
|---|---|---|
| **K13** | Production MCMC R̂ > 1.02 on any param (48×2000 후) | auto-fail |
| **K14** | log Bayesian evidence ln Z − ln Z_LCDM < −1 (decisive against) | KILL |
| **K15** | Cosmic shear S_8 posterior > 0.84 (DES-Y3 3σ 상한 초과) | KILL |
| **K16** | Alt-20 degeneracy: "canonical drift class" 로 projection 후 독립 자유도 < 1 | cluster merge 처리 (kill 아님) |

### L5 KEEP 조건 (arXiv submission 진입)

| ID | 조건 |
|---|---|
| **Q7**  | K1-K16 전부 해당 없음 (또는 K16 만 해당 → cluster 대표만 승격) |
| **Q8**  | ln Z − ln Z_LCDM ≥ +2.5 (substantial, Jeffreys' scale) |
| **Q9**  | DESI DR3 Fisher 예측 σ(w_a) 에서 LCDM 과 ≥ 2σ 분리 예상 |
| **Q10** | Cosmic shear 포함 joint χ² 가 BAO+SN+CMB+RSD 값보다 +3 이내 |
| **Q11** | H₀ tension (SH0ES 대비) 최소 개선 없음 허용, 악화 금지 (|Δh_tension| ≤ +0.005) |
| **Q12** | 이론 해석 문서 (`paper/l5_<ID>_interpretation.md`) 작성 완료 |

**submission winner 목표: 1-3 개** (mainstream 1-2 + alt-20 class 대표 1).

---

## 🧭 실행 순서 (사용자 confirm 전부 생략)

### Phase L5-0. 기준 고정 + 환경 점검

- `refs/l5_kill_criteria.md` 에 K13-K16, Q7-Q12 기재 후 저장
- `base.l5.todo.md` WBS 작성 (L5-0 ~ L5-J)
- `simulations/l5/` 디렉터리 생성
- `simulations/l5/common.py` 작성:
  * L4 common.py import + 다음 추가
  * `run_mcmc_production(...)` — 48 walkers × 2000 steps × burn 500, thin 10
  * `nested_evidence(log_prob, prior_transform, ndim)` — dynesty 기반
  * `fisher_forecast(E_func, Om, h, sigma_bao_dr3, sigma_sn)` — DESI DR3
  * `load_desy3_cosmic_shear()` — KiDS-1000 + DES-Y3 S_8 데이터 + 공분산
  * `chi2_joint_with_shear(E_func, ...)` — 기존 + cosmic shear 추가
- dynesty 설치 확인 (없으면 pip install dynesty)
- Phase 2/3/4 의 data loader 재사용 선언

### Phase L5-A. Mainstream production MCMC (C28, C33)

각 후보 `simulations/l5/<ID>/mcmc_production.py`:

- walkers: 48, steps: 2000, burn: 500, thin: 10, seed 42
- prior: L4 와 동일 (flat within physical bounds)
- chi²: BAO+SN+CMB+RSD (+ L5-D 에서 cosmic shear 추가)
- R̂ < 1.02 on all params (K13). 미달 시 walker 확장 재시도 (최대 2 회)
- corner plot (matplotlib.use('Agg') import corner 이전 — CLAUDE.md 규칙)

결과 dump: `simulations/l5/<ID>/mcmc_production.json` +
`paper/figures/l5_<ID>_corner.png`.

### Phase L5-B. Alt-20 hard-K2 production MCMC (A01, A05, A12, A17)

각 후보에 대해 `simulations/l5/A<NN>/mcmc_production.py`:

- 2-D posterior (Ω_m, h) only
- 48 walkers × 2000 steps (2-D 이므로 K13 쉽게 통과)
- 이론 해석 문서 `paper/l5_A<NN>_interpretation.md` 작성:
  * L0/L1 유도 사슬
  * closed-form 과 SQMH metabolism 연결
  * 왜 amplitude 가 Ω_m 에 lock 되는지

### Phase L5-C. Bayesian evidence (nested sampling)

각 L5 대상 후보에 대해 `simulations/l5/<ID>/evidence.py`:

- dynesty static nested sampler, 1000 live points
- prior_transform: uniform cube → physical box
- log_prob = -0.5 * chi²_joint
- 결과: ln Z, ln Z ± err
- LCDM 기준으로 Δ ln Z = ln Z − ln Z_LCDM 계산
- K14 (decisive against) / Q8 (substantial) 적용

**Jeffreys' scale**:

| Δ ln Z  | 해석            |
|---------|-----------------|
| > +5    | strong          |
| +2.5 ~ +5 | substantial   |
| +1 ~ +2.5 | weak          |
| −1 ~ +1 | inconclusive    |
| < −1    | decisive against (K14) |

결과 dump: `simulations/l5/<ID>/evidence.json`.

### Phase L5-D. Cosmic shear S_8 채널 추가

- `simulations/l5/common.py::load_desy3_cosmic_shear()` 구현:
  * DES-Y3 cosmic shear: S_8 = 0.772 ± 0.017 (Abbott 2022)
  * KiDS-1000: S_8 = 0.759 ± 0.024 (Asgari 2021)
  * Planck baseline: S_8 = 0.834 ± 0.016 (Planck 2018)
- 모든 L5 대상에 대해 S_8(z=0) 계산 + σ_8 posterior 추가
- K15 (S_8 > 0.84) 적용
- Planck vs weak-lensing tension (S_8 ~ 2.5σ) 악화 여부 보고

### Phase L5-E. C11D / C26 재평가

#### C11D hi_class disformal full 재판정

- hi_class (Python wrapper classy) 설치. 없으면 **disformal-exact
  분석 해** (Sakstein-Jain 2015 해석 공식) 직접 구현
- γ_D bounds 재확장 [0, 5]
- 정확 w(z) 에서 K3 (phantom crossing) 재판정
- K3 clear 시 Tier 1 로 승격
- K3 재확인 시 확정 KILL

#### C26 재공식화

- 새 ansatz: `J⁰ = α_Q H ρ_m` (L4 결과에서 L3 drift toy 재현)
- 전체 unimodular diffusion ODE 다시 풀기
- L3 toy (closed-form drift) 와 Δχ², w_a 부호 일치 검증 (K10)
- 일치 시 Tier 1 으로 승격
- 불일치 시 확정 KILL + paper negative result 추가

### Phase L5-F. Alt-20 degenerate class reduction

목표: A01, A03, A05, A06, A08, A09, A11, A12, A13, A15, A16, A17,
A19, A20 (14 candidates) 의 **실질 자유도** 확정.

- 각 후보의 best-fit E²(z) 를 z ∈ [0, 2] 에서 비교
- SVD 기반 principal drift mode 추출:
  * 14 × 200 matrix: 각 후보의 (E²/E²_LCDM − 1)(z)
  * 주성분 분석 → 독립 자유도 n_eff 수
- n_eff = 1 기대 (모두 "m·(1−a) 드리프트" 의 재파라미터화)
- n_eff ≥ 2 이면 서브클래스 분리
- **canonical drift class 대표**: Δ ln Z 기준 최상위 1 개 선정
- 결과: `simulations/l5/alt_class/class_reduction.json` +
  `paper/10_appendix_alt20.md` 작성

### Phase L5-G. DESI DR3 Fisher forecast

- `simulations/l5/forecast/desi_dr3_fisher.py`:
  * DESI DR3 예상 BAO precision (DR2 × ~1.5, factor ~2 improvement on w_a)
  * DESY6 SN 포함 시 시나리오 별도
  * 각 L5 winner 후보에 대해:
    - σ(w_0), σ(w_a) Fisher 예측
    - LCDM 대비 2σ 분리 가능 여부 (Q9)
    - candidate-candidate pairwise discrimination (|Δw_a| / σ(w_a))

결과 dump: `simulations/l5/forecast/dr3_forecast.json` +
`paper/figures/l5_dr3_forecast.png` (2D w_0-w_a 타원 + 후보별 예측점).

### Phase L5-H. Paper v1 업데이트 (submission-ready)

기존 `paper/00-09.md` 를 L5 결과로 업데이트:

- `00_abstract.md`: L5 winner + Δ ln Z + DR3 forecast 한 줄 추가
- `03_background_derivation.md`: alt-20 canonical drift class 수식 추가
- `05_desi_prediction.md`: DR3 Fisher forecast 그림 + 표
- `06_mcmc_results.md`: production MCMC (R̂<1.02) posterior 로 교체
- `07_comparison_lcdm.md`: Δ ln Z 표 추가 (Jeffreys' scale)
- `08_discussion_limitations.md`:
  * cosmic shear S_8 영향 기록
  * H₀ tension 악화 없음 확인
  * alt-20 class degeneracy 해석
  * Base.md §10.4, §XVI 정직 기록 재확인
- `09_conclusion.md`: submission winner 1-3 확정
- **신규** `paper/10_appendix_alt20.md`:
  * 20 후보 전체 표 (L2/L3/L4/L5 verdict)
  * canonical drift class 주성분 분석
  * 0-parameter 대안이 1-parameter 이론과 동급 evidence 를 내는 현상 논의
- `paper/figures/` 에 추가:
  * `l5_<ID>_corner.png` (48×2000 후 full posterior)
  * `l5_dr3_forecast.png`
  * `l5_alt_class_svd.png`
- `paper/references.bib` 에 추가: dynesty, DES-Y3 cosmic shear, KiDS-1000,
  DESI DR3 예상치

### Phase L5-I. arXiv 업로드 점검

- PDF build test (tectonic 또는 pandoc → LaTeX → PDF)
- 모든 figure embed 확인
- BibTeX 모든 \cite 키 검증
- `paper/arxiv_submission_checklist.md` 작성:
  * abstract 250단어 이내
  * author 정보 (base.md §I placeholder)
  * 기본 category: astro-ph.CO, cross: gr-qc
  * LaTeX source + figures zip 구성
- **실제 업로드는 사용자 판단**. 준비까지만.

### Phase L5-J. 문서 정리 + CLAUDE.md 업데이트

- `base.l5.todo.md` WBS 원본 유지, 완료 태스크 `[x]` + 결론 한 줄
- `base.l5.todo.result.md` 에 실행 로그 append
- `CLAUDE.md` L5 재발방지 규칙 추가:
  * dynesty 설치/실행 팁
  * alt-20 class degeneracy 해석 규칙
  * cosmic shear S_8 데이터 로드 규칙
  * Fisher forecast 단위 주의
- `base.l5.result.md` 최종 통합본 (시나리오 판정 포함)

---

## 📦 산출물 체크리스트

| 파일 | 내용 |
|---|---|
| `refs/l5_kill_criteria.md` | K13-K16, Q7-Q12 사전 고정 |
| `base.l5.todo.md` | Phase L5-0 ~ L5-J WBS |
| `base.l5.todo.result.md` | 실행 로그 |
| `base.l5.result.md` | 최종 통합 (winner 1-3) |
| `simulations/l5/common.py` | production MCMC + nested + fisher + cosmic shear |
| `simulations/l5/<ID>/mcmc_production.py` | 48×2000 MCMC |
| `simulations/l5/<ID>/mcmc_production.json` | R̂<1.02 posterior |
| `simulations/l5/<ID>/evidence.py` | dynesty nested sampling |
| `simulations/l5/<ID>/evidence.json` | ln Z, Δ ln Z vs LCDM |
| `simulations/l5/A<NN>/` (A01, A05, A12, A17) | alt-hard production |
| `simulations/l5/C11D_reeval/` | hi_class disformal full re-judge |
| `simulations/l5/C26_reform/` | J⁰=α_Q H ρ_m 재공식화 |
| `simulations/l5/alt_class/class_reduction.json` | SVD + n_eff |
| `simulations/l5/forecast/dr3_forecast.json` | DESI DR3 Fisher |
| `paper/10_appendix_alt20.md` | 20 후보 전체 + class 분석 |
| `paper/l5_<ID>_interpretation.md` | 각 winner 이론 해석 |
| `paper/figures/l5_<ID>_corner.png` | production corner plots |
| `paper/figures/l5_dr3_forecast.png` | DR3 예측 타원 |
| `paper/figures/l5_alt_class_svd.png` | canonical drift class |
| `paper/arxiv_submission_checklist.md` | arXiv 업로드 체크리스트 |
| `CLAUDE.md` | L5 재발방지 규칙 추가 |

---

## ⚖️ 최종 판정 규칙

**시나리오 α — winner 2-3 개 확정 (목표)**
→ paper v1 완성, submission-ready. Tier 1 + Tier 2 에서 상위 2-3 개
+ alt-20 class 대표 1 개. C11D 또는 C26 재평가 통과 시 우선권.

**시나리오 β — winner 1 개만 (단일)**
→ paper v1 단일 main. backup 없음을 본문에 honest 기록. alt-20 class
대표는 appendix 로 강등.

**시나리오 γ — 모든 Tier 1/2 가 K14 (evidence decisive against)**
→ paper v1 을 "null result + alt-20 observation" 논문으로 재구성.
"DESI DR2 preference 는 0-parameter drift lock 으로 재현 가능 →
추가 자유도 정당화 실패" 결론.

**시나리오 δ — C11D K3 clear**
→ C11D 를 최상위 winner 로 승격. 나머지 재정렬. paper 에서 C11D full
disformal 배경 수식을 §3 에 상세 기록.

**시나리오 ε — alt-20 n_eff ≥ 2**
→ canonical drift class 가 실제로 여러 독립 물리임. 서브클래스 각
대표를 별도 winner 로 취급. appendix 확장.

---

## 🚫 금지 사항

- 사용자 confirm 요청 (끝까지 자동 진행)
- Python 외 언어 사용 (hi_class C 호출은 classy Python 래퍼만)
- 기준 (K/Q) 사후 조정
- 새 L4/L3/L2 관점 탐색 (금지)
- L4 에서 폐기된 C27, C41, C23, C5r, C6s, C10k, C32 재진입
- Alt-20 L2 탈락 후보 (A02, A07, A10, A14, A18) 재진입
- Toy CPL fit 만으로 Q3/Q8 충족 주장 (반드시 full background ODE)
- Phantom crossing 허용 (SQMH L0/L1 위반)
- `base.md` 원본 수정
- 결과 왜곡 (Δ ln Z < 0 인데 winner 로 승격 금지)
- MCMC `log_prob` sentinel 합산 금지 (CLAUDE.md 규칙)
- cosmic shear 데이터 추정값 사용 (공식 공개값만: Abbott 2022, Asgari 2021)
- DR3 forecast 에 cosmic variance 누락 금지

---

## ✅ 필수 준수 (CLAUDE.md + L4 재발방지 규칙 전부)

- L1-L4 모든 CLAUDE.md 규칙 승계 (총 80+ 규칙)
- 모든 파일 UTF-8
- `print()` non-ASCII 금지
- `matplotlib.use('Agg')` 는 `import corner` 이전
- emcee 내부 `np.random.seed(42)`
- BAO D_V/D_M/D_H 단위 Mpc, DESY5 `zHD`
- numpy 2.x `np.trapezoid`
- compressed CMB high-z bridge pure LCDM
- `_jsonify` 재귀 변환기 (Python 3.14 np.bool_/np.float_)
- Windows 스레드 제한 (`OMP/MKL/OPENBLAS_NUM_THREADS=1`)
- phantom_crossing 수치 guard `|w+1|>1e-3`
- K10 정의: w_a 부호 기준 + `sqmh_sign_consistent` 플래그 별도
- sibling module collision 방지 (후보별 디렉터리 분리)
- 결과 `base.l5.todo.result.md` 에 실시간 append
- 완료 태스크 `base.l5.todo.md` 에 `[x]` + 결론 한 줄

---

## 📊 예상 계산 비용 (참고용, hard constraint 아님)

| Phase | 시간 추정 | 노트 |
|---|---|---|
| L5-0 기준 + 환경 + dynesty | 1 hour | |
| L5-A C28/C33 production MCMC (2 후보) | 4-6 hours | 48×2000 + R̂ 재시도 |
| L5-B alt-hard production (4 후보 × 2-D) | 2-3 hours | 2-D 이므로 빠름 |
| L5-C Bayesian evidence (8 후보) | 6-10 hours | dynesty 1000 live × 2k-4k iter |
| L5-D Cosmic shear 채널 통합 | 2 hours | 데이터 로드 + chi² 확장 |
| L5-E C11D 재판정 + C26 재공식화 | 6-10 hours | hi_class 또는 분석 해 |
| L5-F Alt-20 class reduction | 2 hours | SVD + 해석 |
| L5-G DESI DR3 Fisher forecast | 3 hours | |
| L5-H Paper v1 업데이트 | 6-10 hours | 9 섹션 + appendix |
| L5-I arXiv 점검 | 2 hours | PDF build + checklist |
| L5-J 정리 + CLAUDE.md | 1 hour | |

**총 추정 35-55 시간**. 중단 금지 자동 진행.

---

## 🎯 성공 기준 (L5 종료 시점)

L5 종료 시점에 아래 모든 항목이 충족되면 성공:

1. `base.l5.result.md` 에 submission winner 1-3 개 확정 (시나리오 α/β/δ/ε)
2. 각 winner 에 대해:
   - Production MCMC R̂ < 1.02 달성
   - Bayesian evidence Δ ln Z ≥ +2.5 (Q8)
   - DESI DR3 Fisher 2σ 분리 예측 (Q9)
   - Cosmic shear joint 안정성 (Q10)
   - H₀ tension 악화 없음 (Q11)
   - 이론 해석 문서 완성 (Q12)
3. `paper/00-10.md` 업데이트 + `paper/10_appendix_alt20.md` 신규
4. `paper/figures/` 에 production corner + DR3 forecast + alt-class SVD
5. `paper/arxiv_submission_checklist.md` 완성
6. C11D 재판정 확정 (승격 또는 확정 KILL)
7. C26 재공식화 확정 (승격 또는 확정 KILL)
8. Alt-20 canonical drift class 의 n_eff 수치 확정 (SVD 근거)
9. `CLAUDE.md` L5 재발방지 규칙 추가
10. `base.l5.todo.md` 전 태스크 `[x]`

---

## 📚 참조 문헌 (신규, L5 에서 추가)

- dynesty: Speagle 2020 (nested sampling library)
- DES-Y3 cosmic shear: Abbott et al. 2022 (S_8 = 0.772 ± 0.017)
- KiDS-1000: Asgari et al. 2021 (S_8 = 0.759 ± 0.024)
- Planck 2018 weak-lensing tension: Planck Coll. 2020, Di Valentino 2021
- DESI DR3 expected precision: DESI Coll. 2024 forecast paper
- Sakstein-Jain disformal analytic: Sakstein 2014, Jain-Khoury 2010
- Jeffreys' scale: Jeffreys 1961, Trotta 2008

---

**문서 이력**. 2026-04-11 작성. L5 production MCMC + Bayesian evidence
+ cosmic shear + DR3 forecast + submission-ready paper 지시서. L4 결과
(`base.l4.result.md` + `simulations/l4_alt/alt20_results.json`) 를 입력
으로 받아 arXiv 업로드 가능한 paper v1 완성까지 자동 완주. 사용자 개입
없이 진행. 결과는 `base.l5.result.md` 와 `paper/` 디렉터리에 기록.
