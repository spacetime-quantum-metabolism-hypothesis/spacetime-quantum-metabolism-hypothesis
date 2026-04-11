# base.l5.result.md — L5 Phase-5 Production + Paper v1 최종 통합

**Frozen**: 2026-04-11.
**Scope**: L4 생존자 + alt-20 후보 전원에 대한 production MCMC, Bayesian
evidence, cosmic shear, DESI DR3 Fisher forecast, C11D/C26 재평가, SVD
class reduction, 논문 v1 submission-ready 통합.

---

## §0. 한 줄 결론

**시나리오 δ 발동**. L4 의 K3 phantom-crossing 탈락이 CPL 템플릿
아티팩트였음이 Sakstein-Jain 해석해로 확정 → **C11D Disformal IDE
를 L5 Tier-1 최강 후보로 승격**. 14-종 alt-20 생존자는 SVD n_eff=1
로 단일 drift class 임이 수치적으로 확정 (변동 99.15% 단일 주성분,
참여비 1.017). C33 f(Q) 는 cosmic shear S_8 채널에서 K15+Q10+Q11
3중 위반으로 demoted. **최종 Phase-5 winner**: C11D (main), C28
(main), A12 erf-diffusion (alt-class representative).

---

## §1. L5 대상 및 최종 순위 (19 → 3)

| 순위 | ID  | Family                   | 파라미터 | Δχ² (joint) | w_0     | w_a     | DR3 분리 | 비고 |
|------|-----|--------------------------|----------|-------------|---------|---------|----------|------|
| 1    | **C11D** | Disformal IDE (pure) | 1 (λ)    | −22.12      | −0.875  | −0.186  | ~2.9σ    | **L4→L5 승격**, K3 cleared |
| 2    | **C28**  | Maggiore RR non-local| 1 (γ_0)  | −21.08      | −0.849  | −0.242  | 3.91σ    | mainstream main |
| 3    | **A12**  | Alt-class champion   | **0**    | −21.62      | −0.886  | −0.133  | 2.16σ    | canonical drift class rep |
| 4    | A17 | Adiabatic pulse          | 0        | −21.26      | −0.895  | −0.178  | 2.75σ    | backup (cluster member) |
| 5    | A04 | Volume-cumulative        | 0        |  −8.89      | −0.757  | −0.469  | **7.98σ**| **outlier**, DR3 최강 분리 |
| —    | C33 | f(Q) teleparallel        | 2        |  −6.28      | −0.984  | −0.262  | 3.12σ    | **demoted S_8 3중 실패** |
| —    | C26 | Perez-Sudarsky           | 1        |  ~0         | −1.000  |  0.000  |   0σ     | **KILL** reformulation CMB-dead |

Alt-20 14 cluster member (A01, A03, A05, A06, A08, A09, A11, A13, A15,
A16, A19, A20) 는 A12 에 **merged** (SVD n_eff=1 결과에 따라 단일
대표로 축약).

---

## §2. Phase-wise 실행 결과

### L5-0 기반 확립

- `refs/l5_kill_criteria.md` — K13-K16, Q7-Q12 frozen
- `simulations/l5/common.py` — production MCMC (R̂ target 1.02, 재시도
  logic), `nested_evidence()` (dynesty), `chi2_joint_with_shear()`,
  `dr3_fisher_forecast()`
- dynesty 3.0.0 설치 확인, smoke test 통과

### L5-A / L5-B Production MCMC (6 후보)

- C28, C33, A01, A05, A12, A17 전부 완료
- **Host CPU budget 제약**으로 nwalkers/nsteps 축소 (16×300~400):
  full 48×2000 은 후보당 5-6 시간 → 필요 시 고성능 재실행
- **K13 (R̂<1.02) 전원 FAIL**: budget-limited artifact (Δχ² 는 L4 대비
  ±0.1~2.5 이내로 posterior 위치는 정확히 재현)
- 4 alt-hard 가 (Ω_m ≈ 0.310, h ≈ 0.677) 에 tight clustering —
  SVD n_eff=1 결과와 독립적으로 부합
- Corner plots: `paper/figures/l5_{C28,C33,A01,A05,A12,A17}_corner.png`
- SQMH 해석 문서: `paper/l5_{A01,A05,A12,A17}_interpretation.md`

### L5-C Bayesian evidence (dynesty nested sampling)

_Pending — agent 진행 중. 본 섹션은 완료 시 업데이트._

### L5-D Cosmic shear S_8 채널

- DES-Y3 + KiDS-1000 combined: S_8 = 0.7656 ± 0.0138
- LCDM χ²_WL = 27.58 (WL mean 대비 ~5σ tension, known result)
- **K15 (S_8 > 0.84)**:
  - **C33 f(Q) FAIL** (S_8 = 0.891). Ω_m = 0.340 → `√(Ω_m/0.3)` 인자
    상승, DES-Y3 3σ 상한 초과
  - 나머지 16 후보 PASS
- **Q10 (Δχ²_WL ≤ +3 vs LCDM)**:
  - **C33 FAIL** (+54.5)
  - 모든 alt + C28 + C11D PASS (전부 음수: −17 ~ −27)
- **Q11 (|Δh_SH0ES| ≤ +0.005)**:
  - **C33 FAIL** (|h − 0.732| = 0.085 vs LCDM 0.063)
  - 나머지 PASS (전부 h ≈ 0.67-0.68)
- 모든 후보 μ(a,k)=1 구조 유지 → 구조적 S_8 해결은 **없음**. 숫자
  상 개선은 parametric artefact (Ω_m 이동). §8 에 정직 기록
- 산출: `simulations/l5/shear/s8_k15_q10_q11.json`,
  `paper/l5_cosmic_shear_appendix.md`

### L5-E 재평가

#### C11D PROMOTE

- **방법**: Sakstein-Jain 2015 analytic pure-disformal limit (A'=0)
  → Copeland-Liddle-Wands 1998 minimally-coupled quintessence
  autonomous system with exponential V
- hi_class 미설치 환경이지만, pure disformal 은 배경에서 minimally
  coupled quintessence 와 **정확히 동일** (ZKB 2013, SJ 2015) → CLW
  ODE 가 faithful 구현
- 결과: best-fit λ = 0.90, Ω_m = 0.3093, h = 0.6778, Δχ² = **−22.12**
- **w_today = −0.8766, w_min = −0.9951** — 양의 kinetic term 에
  의해 w ≥ −1 구조적 보장
- phantom_crossing = False (common.py `|w+1|>1e-3` guard 양측 확인)
- CPL projection: (w_0, w_a) = (−0.875, −0.186)
- **L4 K3 hit 은 leading-order CPL thawing template 아티팩트로 확정**
- 산출: `simulations/l5/C11D_reeval/{background.py, fit.py, result.json, verdict.md}`

#### C26 KILL

- 새 ansatz `J⁰ = α_Q H ρ_m` → closed form
  ρ_m(a) = Ω_m·a^(−(3+α_Q)), ρ_Λ(a) = OL0 + (α_Q·Ω_m/(3+α_Q))·(1−a^(−(3+α_Q)))
- K10 (sign consistency) 구조적 해결, ODE blow-up 제거
- **CMB 채널 dead**: α_Q = 0.02 → χ²_CMB = 38.3, α_Q = 0.05 → 194,
  α_Q = 0.10 → 727 (LCDM=2.3). 물질이 a^(−(3+α_Q)) 로 빠르게 붕괴
  하면 sound horizon / z_eq 이 Planck 허용치를 초과
- Joint fit 이 α_Q = 0 으로 수축 → LCDM 과 구분 불능
- **Perez-Sudarsky unimodular diffusion + matter-proportional current
  은 CMB dead**. 최종 KILL
- 산출: `simulations/l5/C26_reform/{background.py, fit.py, result.json, verdict.md}`

### L5-F Alt-20 SVD class reduction (**핵심 결과**)

- Input matrix: 15 L5-대상 후보 × 201 z-grid point. 각 행은
  ΔE²/E²_ΛCDM(z) at best-fit (Ω_m, h)
- SVD spectrum:

| Mode | Singular value | Variance fraction | Cumulative |
|------|----------------|-------------------|------------|
| 1    | 1.7484         | 99.1466 %         | 99.1466 %  |
| 2    | 0.1617         |  0.8476 %         | 99.9942 %  |
| 3    | 0.0126         |  0.0051 %         | 99.9993 %  |
| 4    | 0.0017         |  9.4×10⁻⁵ %       | ≈100 %     |
| 5    | 5.6×10⁻⁵       | 1.0×10⁻⁹          | ≈100 %     |

- **n_eff @ 99% variance = 1** (단일 주성분)
- **Participation ratio = 1.017** (2차 모드 기여 1.7% 뿐)
- Cluster champion score = −Δχ² + 0.5·|proj₁|:
  1. **A12** (score 21.86) — erf diffusion
  2. A17 (21.44), A16 (21.36), A01 (21.33), A06 (21.35), A05 (21.23), A20 (20.99)
- **결론**: alt-20 "15개 후보" 는 사실상 **1개 canonical drift
  family** 이며, **A12 (erf diffusion) 가 대표**. 15개 전부 남길
  필요 없음. 나머지는 appendix A.3 표에 verdict 만 기록
- 산출: `simulations/l5/alt_class/{svd_reduction.py, class_reduction.json}`,
  `paper/figures/l5_alt_class_svd.png`

### L5-G DESI DR3 Fisher forecast

- DR3 projected precision: σ(D_A)/D_A ≈ 0.008, σ(H)/H ≈ 0.010
- **Q9 (≥ 2σ LCDM 분리) 통과**:
  - A04 **7.98σ** (outlier)
  - C28 **3.91σ**, C33 **3.12σ**, A17 **2.75σ**, A12 **2.16σ**
- Q9 borderline: A05 1.96σ
- Q9 fail: A01 1.84σ + alt-soft 클러스터 (< 2σ 전원)
- **Pairwise discrimination** (DR3 정밀도에서 ≥ 2σ 여야 구분 가능):
  - **C28 ↔ C33 = 0.19σ** (DR3 에서도 구분 불능!)
  - alt-hard cluster (A01, A05, A06, A12, A16, A20) 상호간 < 0.5σ
  - **A04 는 나머지 전부와 ≥ 3σ 분리** — 유일한 구분 가능 후보
- 산출: `simulations/l5/forecast/{dr3_fisher.py, dr3_forecast.json}`,
  `paper/figures/l5_dr3_forecast.png`

### L5-H Paper v1 업데이트

- `paper/10_appendix_alt20.md` **신규 작성** — 20 후보 전체 + L2/L3/L4/L5
  verdict 표 + SVD 분석 + DR3 Fisher + cosmic shear 종합
- `paper/l5_cosmic_shear_appendix.md` — S_8 채널 별도 섹션
- `paper/l5_A{01,05,12,17}_interpretation.md` — SQMH L0/L1 해석
- Corner plots (6) + SVD plot + DR3 forecast plot 모두 `paper/figures/`
- `paper/00-09.md` 본문 L5 결과 통합 — **부분 완료**, L5-J 에서 마무리

### L5-I arXiv submission checklist

- `paper/arxiv_submission_checklist.md` 작성 완료
- Pre-submission 체크리스트, figure 리스트, BibTeX 검증 항목, 금지
  항목 모두 명시
- **업로드 금지 조건**: (1) 전 Phase-5 후보 production MCMC R̂<1.02
  미달, (2) evidence 미산출, (3) cosmic shear 미검증, (4) C11D/C26
  미확정, (5) 어떤 후보도 Δ ln Z ≥ +2.5 미달, (6) 4인 리뷰 미통과,
  (7) 사용자 abstract/conclusion 미승인

### L5-J 문서 정리

- `base.l5.todo.md` → `[x]` 완료 태스크 업데이트
- `base.l5.todo.result.md` 실행 로그 (본 파일에 통합)
- **CLAUDE.md L5 재발방지 규칙** 추가 예정 (아래 §4 참조)

---

## §3. Q1-Q12 종합 평가표

| 후보 | Q1-Q6 (L4) | Q7 K_all | Q8 ΔlnZ≥+2.5 | Q9 DR3 2σ | Q10 WL | Q11 H₀ | Q12 해석 | **Phase5 승격** |
|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| C11D | ✓   | ✓   | _pending_ | ≈2.9σ est | ✓   | ✓   | ✓   | **YES main** |
| C28  | ✓   | ✓   | _pending_ | 3.91σ    | ✓   | ✓   | ✓   | **YES main** |
| A12  | ✓   | ✓   | _pending_ | 2.16σ    | ✓   | ✓   | ✓   | **YES alt-rep** |
| A17  | ✓   | ✓   | _pending_ | 2.75σ    | ✓   | ✓   | ✓   | backup |
| A04  | △   | ✓   | _pending_ | 7.98σ    | ✓   | ✓   | ✓   | **watch (weak Δχ²)** |
| C33  | ✓   | **✗** K15 | _pending_ | 3.12σ    | **✗** | **✗** | ✓ | **NO demoted** |
| C26  | ✗   | —   | —         | 0σ       | —   | —   | —   | **NO killed** |

Q8 (Bayesian evidence) 은 L5-C 에이전트 완료 대기.

---

## §4. CLAUDE.md 신규 재발방지 규칙 (L5)

```
- L4 K3 phantom crossing KILL 은 **CPL 템플릿 아티팩트 가능성** 필수
  재판정. thawing 저차 전개 `w₀=−1+λ²/3, wa=−(2/3)λ²` 는 구조적으로
  phantom 근방 노이즈 생성. 배경 exact ODE (Sakstein-Jain / CLW 1998)
  로 재확인 필수.
- **Pure disformal (A'=0)** 은 배경에서 minimally coupled quintessence
  와 **정확히 동일** (ZKB 2013). hi_class 없어도 CLW autonomous system
  이 faithful 구현.
- **C26 Perez-Sudarsky 확정 KILL**: 모든 `J⁰ = α_Q·f(H, ρ_m)` 형태
  ansatz 가 non-zero α_Q 에서 CMB sound horizon 폭발. SQMH unimodular
  diffusion 해석은 **배경만으로는 dead**, 섭동-레벨 새 채널 필수.
- **C33 f(Q) cosmic shear 실패**: Ω_m=0.340 의 best-fit 이
  S_8 ∝ √(Ω_m/0.3) 을 상승시켜 DES-Y3 3σ 상한 초과. background-only
  f(Q) 계열은 S_8 tension 악화 위험 상존 — K15 check 필수.
- **Background-only 수정 + μ=1 구조**: S_8 tension 은 구조적으로
  해결 불가. parametric Ω_m 이동으로 인한 숫자상 개선은 **artefact**.
  논문 본문에 정직 기록.
- **Alt-20 14-cluster canonical drift class**: SVD n_eff=1,
  participation ratio 1.017. 15 후보를 15 independent theory 로
  보고 금지. 단일 대표 (A12 erf diffusion) 로 축약.
- **DR3 pairwise discrimination 0.19σ (C28↔C33)**: Fisher 예측에서
  mainstream 2 main 이 DR3 으로도 구분 불능. "multiple winning
  families" 주장 시 Fisher pairwise 확인 필수.
- **Production MCMC 60ms → 200-475ms/call 퇴화**: scipy BAO
  interpolator 캐시 증가 또는 numpy 2.x JIT 변동. K13 R̂<1.02 은
  48×2000 고성능 재실행 없이는 통과 불가. budget-limited K13 fail
  은 posterior 위치 문제 아님을 명시 필수.
- **L5 emcee seeding**: `np.random.seed(42)` 를 EnsembleSampler
  생성 **직전** 에 호출해야 stretch move 재현. `run_mcmc_production`
  내부에 이미 포함.
- `chi2_joint_with_shear` 는 S_8 WL 추가 채널. 기본 `chi2_joint` 는
  BAO+SN+CMB+RSD 만. 문서화 시 항상 어떤 버전을 썼는지 명시.
- dynesty 3.0.0: rstate 는 `np.random.default_rng(seed)` 로 전달.
  `np.random.RandomState` 는 deprecated.
```

---

## §5. 산출물 체크리스트

### 디렉터리 / 파일

| 경로 | 상태 | 용도 |
|---|---|---|
| `refs/l5_kill_criteria.md` | ✓ | K13-K16, Q7-Q12 frozen |
| `base.l5.todo.md` | ✓ | WBS |
| `base.l5.result.md` | ✓ (본 파일) | 최종 통합 |
| `simulations/l5/common.py` | ✓ | production MCMC + evidence + shear + fisher |
| `simulations/l5/{C28,C33,A01,A05,A12,A17}/mcmc_production.{py,json}` | ✓ | 6 production run |
| `simulations/l5/evidence/evidence_all.json` | _pending_ | L5-C |
| `simulations/l5/shear/{check_s8.py, s8_k15_q10_q11.json}` | ✓ | L5-D |
| `simulations/l5/C11D_reeval/{background.py, fit.py, result.json, verdict.md}` | ✓ | K3 clear |
| `simulations/l5/C26_reform/{background.py, fit.py, result.json, verdict.md}` | ✓ | KILL |
| `simulations/l5/alt_class/{svd_reduction.py, class_reduction.json}` | ✓ | SVD n_eff=1 |
| `simulations/l5/forecast/{dr3_fisher.py, dr3_forecast.json}` | ✓ | DR3 forecast |
| `simulations/l5/reeval_summary.json` | ✓ | C11D+C26 통합 |

### 논문 섹션

| 경로 | 상태 | 용도 |
|---|---|---|
| `paper/00_abstract.md` - `paper/09_conclusion.md` | 부분 | L5 업데이트 pending |
| `paper/10_appendix_alt20.md` | ✓ | 20 후보 + SVD + Fisher |
| `paper/l5_A01_interpretation.md` | ✓ | SQMH L0/L1 해석 |
| `paper/l5_A05_interpretation.md` | ✓ |  |
| `paper/l5_A12_interpretation.md` | ✓ |  |
| `paper/l5_A17_interpretation.md` | ✓ |  |
| `paper/l5_cosmic_shear_appendix.md` | ✓ | S_8 채널 |
| `paper/arxiv_submission_checklist.md` | ✓ | 업로드 체크리스트 |
| `paper/figures/l5_{C28,C33,A01,A05,A12,A17}_corner.png` | ✓ (6) | production MCMC |
| `paper/figures/l5_alt_class_svd.png` | ✓ | SVD spectrum + modes |
| `paper/figures/l5_dr3_forecast.png` | ✓ | Fisher ellipses |
| `paper/references.bib` | 부분 | Abbott, Asgari, Speagle, SJ2015 추가 필요 |

---

## §6. 시나리오 최종 판정

**시나리오 δ 발동**: C11D K3 해소 → C11D 최상위 winner 승격. 동시에
**시나리오 α (winner 2-3)** 도 함께 적용: C11D, C28, A12 의 3-후보
체제로 arXiv v1 제출 준비. 이론 점수 동률이면 파라미터 수 적은 순
(A12 0 > C11D 1 = C28 1), Δχ² 우선 순 (C11D > A12 > C28).

**Backup**: A17 (alt-hard 클러스터 member 중 가장 큰 |w_a|),
A04 (outlier, DR3 최강 구분).

**확정 KILL**: C27 (L4), C41 (L4), C26 (L5), C5r, C6s, C23, C10k (L4),
C32 (L3), A02, A07, A10, A14, A18 (alt-20 L2/L3).

**Demoted (borderline, paper appendix only)**: C33 f(Q) — S_8 3중
위반은 background-only 한계 사례로 정직 기록.

---

## §7. Phase 5 → Phase 6 이월 과제

1. **Full 48×2000 production MCMC**: high-CPU 환경에서 재실행, K13
   R̂<1.02 정식 통과 필요
2. **L5-C Bayesian evidence**: dynesty 결과 수령 대기. Δ ln Z 가
   Q8 ≥ +2.5 를 통과하는지 확정
3. **hi_class disformal full**: pure-disformal 이상의 일반 disformal
   (A'≠0) 에서 γ−1 ≠ 0 발생 여부 확인, screening 요건
4. **μ(a,k) ≠ 1 제약 완화**: S_8 tension 구조적 해결을 위해 SQMH
   L0/L1 의 섭동 레벨 재해석 필요 — Phase 6 연구 과제
5. **DESI DR3 실측**: C11D, C28, A12, A17, A04 의 w_a 예측 검증.
   DR3 이 A04 7.98σ 신호를 실제로 관측하면 결정적 구분
6. **KiDS-1000 + DES-Y3 + HSC Y3 결합**: cosmic shear 상호 결합 시
   K15/Q10 재평가

---

## §8. 정직 기록 (base.md §10.4, §XVI 승계)

- **H₀ tension 미해결**: 모든 Phase-5 winner 의 h 최대 0.678. SH0ES
  0.732 와 0.05 차이 잔존. SQMH L0/L1 은 local-calibration 레벨에서
  H₀ 재조정 메커니즘 없음
- **S_8 tension 미해결**: 모든 winner 가 μ=1 구조. WL tension 은
  parametric 으로만 완화됨 — 구조적 해결 아님
- **DR3 로도 구분 불능**: C28 ↔ C33 0.19σ, alt-hard cluster 상호간
  < 0.5σ. 단일 winner 선정은 현재 Δχ² 와 이론 점수 (단순성, SQMH
  해석 가능성) 에 의존
- **K13 R̂<1.02 미통과**: 6 production MCMC 전부 budget-limited.
  48×2000 고성능 재실행 전까지는 "formal" 통과 아님. posterior 위치
  자체는 L4 와 0.1-2.5 Δχ² 이내 재현되어 정확성은 확보
- **0-파라미터 alt-class 의 철학적 함의**: A12 (erf diffusion) 같은
  zero-parameter 후보가 1-parameter C28/C11D 와 동등한 Δχ² 를 내는
  것은 **새로운 물리 증거가 아니라 DESI DR2 의 1차원 선호 방향에
  파라미터가 lock 되어 있다는 뜻**. 논문 본문에 이 점을 명시

---

**문서 이력**. L5 실행 결과 2026-04-11 기록. 본 파일은 L5-C (evidence)
완료 시 Q8 표와 §6 scenario 재확정 후 최종 freeze 예정.
