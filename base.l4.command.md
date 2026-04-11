# base.l4.command.md — L4 Full Boltzmann & Paper-Grade Validation 실행 지시서

> `/bigwork-paper` 스킬에 투입할 **최종 확정 지시안**.
> 사용자 confirm 전부 생략. 묻지 말고 끝까지 자동 진행. 언어는 Python.

---

## 실행 명령

```
/bigwork-paper base.l4.command.md 에 기재된 L4 full-Boltzmann + 논문
투고 준비 파이프라인을 끝까지 수행. 사용자 confirm 전부 생략. 묻지
말고 진행. 언어는 Python. base.l3.result.md (8 KEEP + 3 KILL),
base.md, base.fix.md, base.fix.class.md, refs/l3_kill_criteria.md,
Phase 2-4 기존 결과 전부 참고. 기존 L3 시뮬레이션과 중복되어도 L4
이름으로 새로 구현 및 기록.
```

---

## 🎯 근본 목적

**L3 생존자 8 개 (KEEP-A 5 + KEEP-B 3) + 보류 2 개 (C11D, C10k) 에 대해**
- full Boltzmann 배경 ODE 직접 구현 (toy 제거)
- linear 섭동 방정식 명시 전개 (μ, Σ, G_eff, c_s²)
- emcee MCMC posterior (walker 64, step 20000, burn 5000, seed 42)
- 논문 투고 수준 정밀도 (4 인 코드 리뷰 loop 수렴)

**그리고 최종 2-3 개 Phase 5 candidate 로 좁혀 논문 초안을 작성한다.**

**심층 의도**. L3 는 "배경 toy 로 어느 후보가 w_a<0 방향을 재현하는가"
까지였다. L4 는 "그 재현이 full theory 에서도 유지되는가 + 섭동 theory
에서 일관적인가 + MCMC posterior 가 좁혀지는가 + 논문으로 쓸 수 있는
가" 까지 확정한다. L3 에서 발견된 **C27/C28 toy 동일 → full eqs 분리
필수**, **C33 부호 재역전 → 원본 방정식 재확정 필수**, **C11D 경계 탈락
→ hi_class full 재판정**, **C10k 성장 채널 재평가** 문제를 전부 해소
한다.

**최종 결과는 반드시 `base.l4.result.md` 단일 파일에 통합 기록**. 중간
실행 로그는 `base.l4.todo.result.md`. 논문 초안은 `paper/` 9 섹션
markdown 에 작성.

---

## 📐 Kill / Keep 기준 (L3 에서 승계 + 신규 K9-K12 추가)

**실행 시작 전에** `refs/l4_kill_criteria.md` 에 아래 기준을 commit 하여
고정. 실행 도중 임계값 조정 **금지**.

### L3 에서 승계 (K1-K8)

L3 기준 그대로. `refs/l3_kill_criteria.md` 참조.

### L4 신규 KILL 조건

| ID | 조건 | 임계값 |
|---|---|---|
| **K9**  | MCMC 수렴 실패 (R̂ > 1.05 on any param) | auto-fail |
| **K10** | Full-Boltzmann 배경이 L3 toy w_a 부호와 반대 | auto-fail (toy 오도) |
| **K11** | 섭동 theory 에서 c_s² < 0 또는 ghost dof 발견 | auto-fail |
| **K12** | 2-D posterior 가 (w0, wa) 평면에서 LCDM 을 포함 (2σ 내) | marginal KILL |

### L4 KEEP 조건 (Phase 5 진입 = 논문 main candidate)

| ID | 조건 |
|---|---|
| **Q1** | K1-K12 전부 해당 없음 |
| **Q2** | MCMC 2σ posterior 에서 LCDM 배제 (또는 Δχ² ≤ -6 = ~2.5σ preference) |
| **Q3** | Full-Boltzmann 과 toy 의 w0, w_a 부호·크기 일치 (toy↔full consistency) |
| **Q4** | 섭동 theory 명시 전개 완료 + `c_s²>0` 증명 |
| **Q5** | Cassini |γ-1| 수치 재계산 < 2.3e-5 (거의 전원) |
| **Q6** | SQMH L0/L1 (σ=4πG·t_P, Γ₀) 직접 해석 가능 (이론 점수 ≥ 6/10) |

**Phase 5 진입 수 목표: 2-3 개**. 더 많으면 이론 점수로 tie-break.

---

## 📋 스코프

### 포함 (총 10 후보)

**KEEP-A 5 (최우선)**:
- C27 Deser-Woodard
- C28 Maggiore RR non-local
- C33 f(Q) teleparallel
- C41 Wetterich fluid IDE
- C26 Perez-Sudarsky diffusion

**KEEP-B 3 (LCDM 등가, 약한 유지)**:
- C23 Asymptotic Safety
- C5r RVM
- C6s Stringy RVM + CS

**보류 2 (재평가)**:
- C11D Disformal IDE (K2 경계 탈락 → hi_class disformal branch 로 재판정)
- C10k Dark-only coupled (배경 w_a=0 → RSD/σ_8 성장 채널 재평가)

**C32 Bare Mimetic 은 L3 확정 탈락 → L4 제외**.

### 작업 유형

| Task | 대상 | 우선순위 |
|---|---|---|
| Full-Boltzmann 배경 ODE 직접 구현 | 10 후보 전원 | 최우선 |
| Linear 섭동 방정식 명시 전개 + c_s² 검증 | 10 후보 전원 | 최우선 |
| emcee MCMC (walker 64, step 20k) | 10 후보 전원 | 최우선 |
| C27 vs C28 차별화 (U/V auxiliary 분리) | C27, C28 | 필수 |
| C33 부호 재확정 (Frusciante 2021 원본) | C33 | 필수 |
| C11D hi_class disformal full 재판정 | C11D | 필수 |
| C10k 성장 채널 (G_eff/G, σ_8) 평가 | C10k | 필수 |
| Phase 5 후보 2-3 개 확정 | 전체 | 필수 |
| 논문 초안 9 섹션 영어 markdown | KEEP 확정 후보 | 필수 |

### 제외

- L3 에서 폐기된 C32 재진입
- 새 L2/L3 관점 탐색 (금지)
- Chaplygin, L2 이전 폐기 family 재진입
- UV completion / 양자 중력 full theory (Phase 6 이월)
- 임의 파라미터 tuning 없는 full re-derivation (L0/L1 invariant 존중)

---

## 🧭 실행 순서 (사용자 confirm 전부 생략)

### Phase L4-0. 기준 고정 + 환경 점검

- `refs/l4_kill_criteria.md` 에 K1-K12, Q1-Q6 기재 후 저장
- hi_class (또는 classy) 설치 확인 — 없으면 Python custom Boltzmann 로 자동 fallback
- `simulations/l4/` 디렉터리 생성
- Phase 2/3 의 data loader, LCDM baseline 재사용 선언 (L3 와 동일 소스)

### Phase L4-A. Full-Boltzmann 배경 ODE 직접 구현

각 후보 `c<ID>` 에 대해 `simulations/l4/<ID>/background.py` 작성:

| ID | 구현 방식 | 참조 문헌 |
|---|---|---|
| C27 | auxiliary U, V, Ud, Vd localised ODE | Dirian 2015 Eq 2.5-2.8 (Deser-Woodard) |
| C28 | auxiliary U, S localised RR non-local | Dirian 2015 full RR branch |
| C33 | modified Friedmann with f_Q=df/dQ, f_QQ | Frusciante 2021 원본 배경 방정식 |
| C41 | hi_class fluid_ide branch (또는 Python rewrite) | Amendola 2000, Gavela 2009 |
| C26 | unimodular diffusion ODE with source J^0 | Perez-Sudarsky 원본 + CSL |
| C23 | effective RVM with ξH RG identification | Bonanno-Platania 2018 |
| C5r | Λ(H²) running vacuum | Gómez-Valent-Solà 2024 |
| C6s | stringy RVM (C5r) + CS Kerr-only contribution check | Arvanitaki 2020 |
| C11D | hi_class disformal_coupling branch + γ_D full range | Zumalacárregui-Koivisto-Bellini 2013 |
| C10k | hi_class couple_dm_de branch + β_d full | Amendola 2000 (dark-only) |

**주의**. L3 toy ↔ L4 full 비교를 **필수로 보고** (w0, wa 부호/크기 일치
여부). K10 발동 조건.

### Phase L4-B. Linear 섭동 방정식 명시 전개

각 후보 `simulations/l4/<ID>/perturbation.py`:

- synchronous gauge (Ma-Bertschinger 1995 convention)
- δ_m', θ_m', δ_DE', θ_DE' (fluid) 또는 δφ' (scalar) ODE
- `μ(a,k) = G_eff/G`, `Σ(a,k) = (1+η)/2` 출력
- c_s² (sound speed) 계산 + positivity 검사 (K11)
- ghost dof 검사 (K11)
- growth factor D(a,k), fσ_8(z) 예측

**문서화**: 각 후보 `paper/l4_<ID>_perturbation.md` 작성 (영어 LaTeX).

### Phase L4-C. emcee MCMC posterior

각 후보 `simulations/l4/<ID>/mcmc.py`:

- emcee.EnsembleSampler
- walkers: 64, steps: 20000, burn: 5000, thin: 10
- seed 42 (np.random.seed 내부 추가 필수 — CLAUDE.md 규칙)
- prior: flat within physical bounds
- log_prob = -0.5 * (BAO + SN + CMB + RSD chi²)
- chi² 실패 시 `return -np.inf` (sentinel 금지)
- R̂ < 1.05 convergence check (K9)
- corner plot 저장 (`matplotlib.use('Agg')` 는 import corner 이전 — CLAUDE.md 규칙)

결과 dump: `simulations/l4/<ID>/mcmc_posterior.json` +
`paper/figures/l4_<ID>_corner.png`.

### Phase L4-D. 특수 후보 처리

#### C27 vs C28 차별화

- 동일 toy 로는 구분 불가 (L3 동일 결과). Full eqs 에서 분리:
  - C27: Deser-Woodard `f(□⁻¹R)` localised via U/V pair
  - C28: Maggiore RR `R □⁻¹ R` localised via U/S pair
- 각자의 free function (c_0, mass scale) 에 대해 posterior 분리
- 결과 분리 불가 시 **C28 만 유지 (Maggiore 이론 선호)**, C27 는 L2 archive 로

#### C33 부호 재확정

- Frusciante 2021 Eq (배경 modified Friedmann) 를 Python 에 직접 구현
- L2 R3 (f_1>0 → w_a<0) vs L3 toy (f_1<0 → w_a<0) 중 어느 부호가 physical 인지 결론
- 필요 시 `f_Q = df/dQ` 역함수 계산으로 (Q, H) self-consistent 해 구함
- `simulations/l4/C33/sign_verification.md` 에 reasoning 기록

#### C11D hi_class disformal full 재판정

- hi_class disformal branch 에서 γ_D 를 [0, 5] 범위로 확장
- K2 재판정 (L3 에서 |w_a|=0.1149 로 0.009 미달 탈락)
- full 에서 |w_a| ≥ 0.125 이면 KEEP 복귀, 아니면 확정 탈락

#### C10k 성장 채널 평가

- 배경 w_a=0 은 확정 (L3). K2 배경 기준으로는 탈락
- 그러나 `G_eff/G = 1+2β_d²` 는 DM growth 증폭 → RSD Δχ² 채널 기여
- **별도 판정**: "성장 채널 only" Δχ²_{RSD} < -4 이면 KEEP-growth 로 유지
- σ_8 tension 계산 (CLAUDE.md 규칙: β_d~0.107 은 S_8 +6.6 악화)

### Phase L4-E. Phase 5 후보 확정 (최대 2-3 개)

- 전체 10 후보에 대해 Q1-Q6 평가
- Δχ² 오름차순 + 이론 점수 tie-break
- 최종 ranking table 작성
- **목표: 2-3 개 main candidate + 1-2 개 backup**
- 나머지는 "L4 확정 탈락" 으로 분류

### Phase L4-F. 논문 초안 작성 (영어 markdown, `paper/`)

9 섹션 구조 (base.md §2 참조):

```
paper/
  00_abstract.md
  01_introduction.md          # DESI tension + SQMH 동기
  02_sqmh_axioms.md            # L0/L1, σ=4πG·t_P, Γ₀
  03_background_derivation.md  # 배경 Friedmann + w(z) 유도
  04_perturbation_theory.md    # L4-B 결과 통합
  05_desi_prediction.md        # Phase 5 candidate w(z) 예측
  06_mcmc_results.md           # L4-C posterior 요약
  07_comparison_lcdm.md        # 2σ posterior + Δχ² 표
  08_discussion_limitations.md # base.md §10.4, §XVI 정직 기록
  09_conclusion.md
  references.bib               # BibTeX
  figures/                     # corner plots, w(z) curves, 3D posteriors
```

### Phase L4-G. 4 인 코드 리뷰 루프 (L3 G 재적용)

모든 `simulations/l4/<ID>/*.py` 에 대해 4 인 리뷰 (numerical / physical /
reproducibility / prevention rules). 4 리뷰 전부 pass 할 때까지 재작성.
5 회 수렴 실패 시 이론 탈락 → Phase 5 제외.

리뷰 결과 기록: `simulations/l4/<ID>/review.md`.

### Phase L4-H. Ranking + 최종 판정

- `simulations/l4/ranking.py`: 모든 후보의 Q1-Q6 점수 합산 + Δχ² 정렬
- `base.l4.result.md` 작성 (단일 통합):
  - Phase 5 확정 후보 2-3 개 (main card: full background, perturbation, MCMC)
  - L4 탈락 리스트 (사유 한 줄)
  - 논문 초안 완성도 점검
  - Phase 5 MCMC/투고 계획

### Phase L4-I. 문서 정리

- `base.l4.todo.md` WBS 원본 유지, 완료 태스크 `[x]` + 결론 한 줄
- `base.l4.todo.result.md` 에 실행 로그 append
- `CLAUDE.md` L4 재발방지 규칙 추가 (예: "toy↔full 부호 일치 검증 필수")
- `base.l4.result.md` 최종 통합본

---

## 📦 산출물 체크리스트

| 파일 | 내용 |
|---|---|
| `refs/l4_kill_criteria.md` | K1-K12, Q1-Q6 사전 고정 |
| `base.l4.todo.md` | Phase L4-0 ~ L4-I WBS |
| `base.l4.todo.result.md` | 실행 로그 + 4 리뷰 이력 |
| `base.l4.result.md` | 최종 통합 (2-3 개 confirmed candidates) |
| `simulations/l4/<ID>/background.py` | full Boltzmann 배경 ODE |
| `simulations/l4/<ID>/perturbation.py` | 섭동 방정식 + c_s² |
| `simulations/l4/<ID>/mcmc.py` | emcee 20k steps |
| `simulations/l4/<ID>/mcmc_posterior.json` | posterior 통계 |
| `simulations/l4/<ID>/review.md` | 4 인 리뷰 이력 |
| `simulations/l4/ranking.py` | Q1-Q6 종합 평가 |
| `paper/00_abstract.md` ~ `paper/09_conclusion.md` | 논문 초안 9 섹션 |
| `paper/l4_<ID>_perturbation.md` | 섭동 명시 전개 |
| `paper/figures/l4_<ID>_corner.png` | MCMC corner plots |
| `paper/figures/l4_w_of_z.png` | Phase 5 후보 w(z) 곡선 |
| `paper/references.bib` | BibTeX |
| `CLAUDE.md` | L4 재발방지 규칙 추가 |

---

## ⚖️ 최종 판정 규칙

**시나리오 A — Phase 5 후보 2-3 개 확정**
→ 논문 초안 완성, Phase 5 는 submission + referee 대응. `base.l4.result.md` 에 main + backup candidate, MCMC posterior, 섭동 결과, Δχ² 비교 표, 논문 섹션 완료 현황 기록.

**시나리오 B — 모든 후보가 K9-K12 에 걸림**
→ L3 KEEP 이 L4 full 에서 무너진 상황. `paper/negative_result.md` 확장 작성. SQMH base.md 는 "full Boltzmann 수준에서 데이터와 불일치" 재분류. 이 경우 Phase 6 이월 (UV completion 재탐색).

**시나리오 C — 1 개만 살아남음**
→ 단일 candidate 으로 논문 작성 진행. backup 없음을 본문에 honest 기록.

**시나리오 D — 3 개 초과 KEEP**
→ 이론 점수 tie-break 후 상위 3 개만 paper main, 나머지는 appendix.

---

## 🚫 금지 사항

- 사용자 confirm 요청 (끝까지 자동 진행)
- Python 외 언어 사용 (hi_class C 호출은 classy Python 래퍼 통해서만)
- 기준 (K/Q) 사후 조정
- 새 L3/L2 관점 추가
- L3 에서 폐기된 C32 재진입
- Toy CPL fit 만으로 Q3 충족 주장 (반드시 full background ODE)
- Vainshtein 사후 주입 (L2 규칙 승계)
- Phantom crossing 허용 (SQMH L0/L1 위반)
- 4 인 리뷰 미통과 결과 논문 게재
- `base.md` 원본 수정
- 결과 왜곡 (full Boltzmann 결과 ≠ L3 toy 주장 시 정직 기록 + toy 폐기)
- MCMC 에서 `log_prob` sentinel 값 합산 금지 (return -np.inf 필수)

---

## ✅ 필수 준수 (CLAUDE.md 재발방지 규칙 전부)

- **L3 에서 추가된 규칙도 전부 적용**:
  - L3 배경 fit ODE 폭주 → 해석 toy 교체
  - CPL 추출은 E²(z)↔CPL E²(z) 직접 least_squares fit
  - Fluid-level toy 배경 w_a=0 구조적 → 성장 채널 재평가
  - L3 K2 경계 ±0.01 이내 탈락은 toy 제한 가능성 → full 재판정 필수
  - C33 부호 재역전 주의 → Frusciante 2021 원본만 신뢰
  - RVM joint 에서 ν→upper bound 박힘 정상
  - C26 drift toy 안전 → Phase 5 full diffusion 전 proxy
- 모든 파일 UTF-8
- `print()` non-ASCII 금지, `matplotlib.use('Agg')` 는 `import corner` 이전
- emcee 내부 `np.random.seed(42)` 필수
- BAO D_V/D_M/D_H 단위 Mpc, DESI DR2 공식값 `w0=-0.757, wa=-0.83`
- DESY5 `zHD` 사용, numpy 2.x `np.trapezoid`
- growth ODE 배경은 LCDM 아날리틱 (backward quintessence 폭주 회피)
- compressed CMB high-z bridge 는 pure LCDM tail
- 4 인 리뷰 전부 pass 한 결과만 채택
- 결과 나쁘면 코드 의심 → 4 리뷰 재실행 → 수렴 후에도 나쁘면 이론 탈락
- 진행 로그 `base.l4.todo.result.md` 에 지속 append
- 완료 태스크 `base.l4.todo.md` 에 `[x]` + 결론 한 줄

---

## 📊 예상 계산 비용 (참고용, hard constraint 아님)

| Phase | 시간 추정 | 노트 |
|---|---|---|
| L4-0 기준 고정 + 환경 | 30 min | hi_class 설치 포함 |
| L4-A full-Boltzmann 배경 (10 후보) | 8-14 hours | 각 ~1 hour + 리뷰 |
| L4-B 섭동 ODE (10 후보) | 6-10 hours | ghost / c_s² 검사 포함 |
| L4-C MCMC (10 후보 × 20k steps) | 15-25 hours | walker 64, 후보당 1.5-2.5h |
| L4-D 특수 후보 처리 | 4-6 hours | C27/C28 분리, C33 재확정 |
| L4-E Phase 5 후보 확정 | 2 hours | ranking + report |
| L4-F 논문 초안 9 섹션 | 8-14 hours | 영어 + LaTeX 수식 |
| L4-G 4 인 리뷰 루프 누적 | +40% | full 구현은 리뷰 비중 큼 |
| L4-H Ranking + 문서 | 2 hours | |
| L4-I 정리 | 1 hour | |

**총 추정 50-90 시간**. 중단 금지 자동 진행.

---

## 🎯 성공 기준 (L4 종료 시점)

L4 종료 시점에 아래 모든 항목이 충족되면 성공:

1. `base.l4.result.md` 에 Phase 5 후보 2-3 개 확정 (0 개 시 시나리오 B)
2. 각 확정 후보에 대해:
   - Full Boltzmann 배경 Python 구현 (toy 아님)
   - 섭동 theory 명시 전개 문서 (paper/l4_<ID>_perturbation.md)
   - MCMC posterior (2σ LCDM 배제 또는 이론 점수 ≥ 8)
   - Cassini |γ-1| 수치 재계산 < 2.3e-5
3. `paper/00_abstract.md` ~ `paper/09_conclusion.md` 9 섹션 초안 완성
4. `paper/figures/` 에 corner plot + w(z) 곡선 + posterior triangle
5. `CLAUDE.md` L4 재발방지 규칙 추가
6. 모든 `simulations/l4/<ID>/review.md` 4 리뷰 pass 기록

---

**문서 이력**. 2026-04-11 작성. L4 full-Boltzmann + 논문 초안 지시서.
L3 결과 (`base.l3.result.md`) 를 입력으로 받아 Phase 5 confirmed
candidate 2-3 개 + 논문 초안 완성까지 자동 완주. 사용자 개입 없이 진행.
결과는 `base.l4.result.md` 와 `paper/` 디렉터리에 기록.
