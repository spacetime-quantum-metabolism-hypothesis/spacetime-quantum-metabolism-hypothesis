# base.l3.command.md — L3 Winnowing & Full-Stack Validation 실행 지시서

> `/bigwork-paper` 스킬에 투입할 **최종 확정 지시안**.
> 사용자 confirm 전부 생략. 묻지 말고 끝까지 자동 진행. 언어는 Python.

---

## 실행 명령

```
/bigwork-paper base.l3.command.md 에 기재된 L3 winnowing 및 full-stack
검증 파이프라인을 끝까지 수행. 사용자 confirm 전부 생략. 묻지 말고
진행. 언어는 Python. base.l2.result.md (11 생존자), base.md, base.fix.md,
base.fix.class.md, Phase 3/4 기존 결과 전부 참고. 기존 시뮬레이션과
중복되어도 L3 이름으로 새로 구현 및 기록.
```

---

## 🎯 근본 목적

**L2 11 생존자를 정량 winnowing 하여 Phase 5 확정 후보로 좁히고, 동시에
그 후보들에 대한 full-stack 검증 (DESI DR2 fitting, MCMC, 섭동 이론
명시 전개, CLASS/CAMB 수준 Boltzmann 구현) 까지 완주**.

**최종 결과는 반드시 `base.l3.result.md` 단일 파일에 통합 기록**.
중간 실행 로그는 `base.l3.todo.result.md`, 최종 결론·keep/kill 리스트·
Phase 5 진입 후보·MCMC posterior 요약·섭동/CLASS 결과 요약은 전부
`base.l3.result.md` 에 수렴. 사용자는 `base.l3.result.md` 한 파일만
읽으면 전체 L3 판정을 파악할 수 있어야 함.

L1/L2 는 수식 + toy 수준이었다. L3 는 **관측 데이터 실측, 섭동 방정식
명시 유도, Boltzmann 코드 구현** 을 모두 포함한다.

**심층 의도**. L2 는 "수식상 가능한 경로 11 개" 를 나열했으나 이 중
실제 데이터 적합성이 담보된 것이 몇 개인지 불명. L3 의 의의는 "시뮬
레이션 결과가 나쁜 것은 배제, 좋은 것만 살리는" 필터링과 동시에
"살아남은 후보에 대해 Phase 5 논문 투고 수준까지 준비" 하는 것.

---

## 📐 Kill / Keep 기준 (사전 고정, 사후 조정 금지)

**실행 시작 전에** `refs/l3_kill_criteria.md` 에 아래 기준을 commit 하여
고정한다. 실행 도중 임계값 조정 **금지**.

### KILL 조건 (하나라도 해당 → 즉시 탈락)

| ID | 조건 | 임계값 |
|---|---|---|
| **K1** | BAO+SN+CMB+RSD joint `Δχ² vs LCDM` | `> +4.0` (95% CL) |
| **K2** | `|w_a|` 진폭이 DESI 중심값의 비율 | `< 15%` (즉 `|w_a| < 0.125`) |
| **K3** | Phantom crossing 발생 (w(z) 가 -1 교차) | SQMH L0/L1 부호 규약 위반 |
| **K4** | Cassini `|γ-1|` 수치 재계산 | `> 2.3e-5` (수식 증명과 수치 불일치) |
| **K5** | 재현성 (seed 고정 시 결과 drift) | `> 1e-3` |
| **K6** | SQMH L0/L1 불변 조건 (σ=4πG·t_P, Γ₀) 암묵 수정 필요 | 자동 탈락 |
| **K7** | 섭동 theory 에 ghost / gradient instability (c_s² < 0) | 자동 탈락 |
| **K8** | CLASS/CAMB 구현 시 수치 blow-up (N_eff divergence 등) | 자동 탈락 |

### KEEP 조건 (전부 충족 → Phase 5 진입)

| ID | 조건 |
|---|---|
| **P1** | K1-K8 전부 해당 없음 |
| **P2** | `Δχ² ≤ 0` (LCDM 대비 개선 또는 동일) **또는** 이론 정합성 점수 `≥ 8/10` (SQMH L0/L1 직접 연결) |
| **P3** | Python 재현성 완전 (seed, data path, 의존성 pinned) |
| **P4** | 섭동 theory 명시 전개 완료 (linear + 1 st order) |
| **P5** | CLASS 또는 CAMB 수준 Boltzmann 구현 존재 (hi_class branch 활용 또는 patch) |

**Phase 5 진입 후보 수**. 고정 안 함. `P1~P5 전부 만족` 하는 **전부**.
전원 탈락 시 `paper/negative_result.md` 부록 작성 후 종료.

### 임계값 선택 근거 (claude 추천값)

- **K1 +4.0**: 2-σ 수준 (Δχ²=4 ≈ 95% CL). 너무 엄격하면 이론 정합성
  높은 후보 (C26, C32) 를 초반에 잃음.
- **K2 15%**: C28 (Dirian 2015 `|w_a|=0.19`) 를 경계 근처에서 살려
  full 재구현으로 재판정 받게 함.
- **K3 phantom crossing 금지**: SQMH L0/L1 metabolism 부호 규약 ("matter
  는 DE 로 흘러간다") 과 충돌.
- **K4 수치 재확인**: L2 는 수식 증명 위주, L3 는 태양계 PPN 수치 직접.
- **Phase 5 진입 수 미고정**: 사용자 지시 "최대한 모든 시도를 폭넓게".

---

## 📋 스코프

### 포함

- L2 생존자 11 개 (C5r, C6s, C10k, C11D, C23, C26, C27, C28, C32, C33, C41) 전부
- DESI DR2 BAO 13 포인트 + 공분산 full fit
- DESY5 SN (`zHD`) + 공분산 full fit
- Compressed CMB (θ*, ω_b, ω_c) + theory floor 0.3%
- RSD fσ8 compilation (Phase 3 와 동일 소스, Gil-Marín, Alam, eBOSS, DESI)
- Joint chi² 최소화 (scipy.optimize multi-start, 최소 8 start)
- emcee MCMC (각 생존자별, walker 64, step 20000, burn 5000)
- **섭동 theory 명시 전개**: linear scalar perturbation, ODE in k-space,
  dark matter δ, peculiar velocity θ, φ perturbation δφ (스칼라 모델 한정),
  G_eff(a,k), η(a,k) 정의
- **CLASS/CAMB 구현**:
  - hi_class 이미 지원: C5r (RVM), C10k (dark-coupled quintessence), C11D
    (disformal branch), C41 (fluid IDE), C33 (f(Q) Frusciante 2021 patch)
  - Patch 필요: C23 (asymptotic safety as effective RVM), C26 (unimodular
    diffusion), C27 (Deser-Woodard localised), C28 (Maggiore RR localised)
  - 지원 불가: C6s (CS anomaly), C32 (mimetic full) — 최선 근사 + honest 기록

### 제외

- L2 외 신규 관점 탐색 (금지)
- L2 에서 폐기된 family 재진입 (Chaplygin 등 금지)
- Phase 3/4 MCMC 전체 재실행 (Phase 5 업무)
- UV completion, quantum gravity (Phase 6 이월)

---

## 🧭 실행 순서 (사용자 confirm 전부 생략)

### Phase L3-0. 기준 고정

- `refs/l3_kill_criteria.md` 에 K1-K8, P1-P5 기재하고 저장
- 이후 변경 금지 (사후 조정 적발 시 테스트 무효)

### Phase L3-A. 데이터 로더 통합

- `simulations/l3/data_loader.py`
  - BAO: CobayaSampler `bao_data` DESI DR2 13 포인트 + 전체 공분산
  - SN: CobayaSampler `sn_data/DESY5/` (`zHD`)
  - CMB: compressed (θ* + ω_b + ω_c) + theory floor 0.3%
  - RSD: fσ8 compilation (Phase 3 소스 재사용)
- `simulations/l3/lcdm_baseline.py`
  - LCDM best-fit chi² (Ω_m, H_0, σ_8) 단일 값 고정 commit
  - 이후 Δχ² 비교 기준

### Phase L3-B. 섭동 theory 템플릿

- `simulations/l3/perturbation_base.py`
  - Linear scalar perturbation ODE (synchronous gauge)
  - dark matter `δ', θ'`, radiation `δ_r', θ_r'`, scalar `δφ', δφ'_N`
  - `μ(a,k) ≡ G_eff/G`, `Σ(a,k) ≡ (1+η)/2` 출력
  - Benchmark against LCDM (`μ=Σ=1`) numerically
- 각 생존자는 이 템플릿을 상속하여 자기 방정식만 override

### Phase L3-C. 11 생존자 full-ODE 배경 + chi²

**구현 순서 (우선순위)**

1. **1 순위 (A)**: C10k, C27, C33 — 3 개
2. **2 순위 (A−)**: C11D, C23, C41 — 3 개
3. **3 순위 (B)**: C5r, C6s, C26, C28, C32 — 5 개

각 후보 `c<ID>` 에 대해 생성:

```
simulations/l3/<ID>/
    background.py       # full ODE, w(z), H(z)
    perturbation.py     # 섭동 방정식 명시
    chi2.py             # BAO+SN+CMB+RSD joint chi²
    optimize.py         # scipy.optimize multi-start (8 start)
    cassini.py          # |γ-1| 수치 재계산
    run.py              # 전체 파이프라인 실행
    result.json         # 결과 dump
```

**실행 후 즉시 Kill/Keep 판정**. KILL 해당 시 해당 후보 `status=KILLED`
기록 후 다음 후보. KEEP 이면 Phase L3-D 로.

### Phase L3-D. MCMC (각 생존자별)

KILL 되지 않은 후보만 대상:

```
simulations/l3/<ID>/mcmc.py
    - emcee EnsembleSampler
    - walkers: 64
    - steps: 20000
    - burn: 5000
    - thin: 10
    - seed: 42 (재현성)
    - prior: flat within physically motivated bounds
    - log_prob: -0.5 * (BAO+SN+CMB+RSD chi²)
    - convergence: R̂ < 1.05 on all params
    - corner.py plot 저장
```

**주의**. CLAUDE.md 재발방지 규칙 전부 준수.
- `log_prob` 에서 chi² 실패 시 `return -np.inf` (sentinel 금지)
- `np.random.seed(42)` 를 `run_mcmc` 내부에 추가 (emcee stretch move 대비)
- `matplotlib.use('Agg')` 는 `import corner` 이전

### Phase L3-E. CLASS/CAMB 구현

KEEP 후보 대상:

**hi_class 지원 직접 가능**:
- **C5r RVM**: `Omega_Lambda_0` running 으로 patch
- **C10k Dark-coupled**: `couple_dm_de` branch + `β_d`
- **C11D Disformal**: `disformal_coupling` branch
- **C33 f(Q)**: Frusciante 2021 patch 있으면 포함, 없으면 구현 이월
- **C41 Fluid IDE**: `fluid_ide` branch

**Python 래퍼 자체 구현 (hi_class 미지원)**:
- **C23 Asymptotic Safety**: effective RVM 형으로 hi_class 재해석
- **C26 Perez-Sudarsky**: unimodular diffusion, custom Friedmann + 섭동
- **C27 Deser-Woodard**: auxiliary `U, V` localised form, custom ODE
- **C28 Maggiore RR**: auxiliary `U, S` localised, Dirian 2015 full eq 구현

**구현 불가 + 최선 근사**:
- **C6s Stringy RVM + CS**: CS anomaly 는 기존 hi_class 에 없음 → RVM 부분만
  hi_class + CS 효과는 leading order python patch 로 근사, honest 기록
- **C32 Mimetic**: Lagrange multiplier 제약 은 hi_class 에 없음 →
  background effective 방식으로 근사, honest 기록

```
simulations/l3/<ID>/classy_wrapper.py
    - classy 또는 camb python 호출
    - 출력: CMB TT/EE/TE, matter power P(k), D(a,k), f(a,k), σ_8(z)
    - 실패 시 fallback: Python 자체 구현 (상세 ODE)
```

### Phase L3-F. 섭동 theory 명시 전개 (논문용)

각 KEEP 후보에 대해 `paper/l3_<ID>_perturbation.md` 작성:

- Metric perturbation convention (synchronous or Newtonian gauge)
- Linear ODE 전체 명시 (LaTeX 수식)
- μ(a,k), Σ(a,k), G_eff/G 유도
- Sound speed c_s² 계산 + ghost 없음 증명
- Growth index γ 계산
- RSD fσ8 예측

**문제 발생 시**. 섭동 전개 중 ghost / gradient instability 발견
→ K7 kill 조건 발동, 해당 후보 탈락.

### Phase L3-G. 4 인 코드 리뷰 루프 (무한 반복)

**이것이 L3 의 핵심 규칙**. 코드 작성 후 4 인 리뷰 4 가지 모두 pass
할 때까지 재작성.

1. **Numerical correctness reviewer**
   - 단위 (SI 일관성), 부호, ODE convention
   - numpy 2.x trapezoid, non-ASCII 유니코드 금지
   - BAO D_V/D_M/D_H 단위 Mpc 일관성
   - E(z) coupled ODE (ad hoc 근사 금지)
   - IDE convention 이중카운팅 금지
2. **Physical sanity reviewer**
   - 에너지 양성, 인과성 (c_s² > 0), no ghost
   - Ω_m + Ω_r + Ω_DE = 1 closure
   - Friedmann constraint 준수
   - Phantom crossing 감시
3. **Reproducibility reviewer**
   - seed 고정 (np.random, emcee 내부 둘 다)
   - 데이터 파일 경로 절대 path
   - requirements.txt 버전 pin
   - backend (matplotlib Agg) 순서
4. **Prevention rules reviewer**
   - CLAUDE.md 재발방지 항목 전부 grep 검사
   - 과거 발견된 함정 재발 없음 확인

**4 리뷰 실패 → 재작성**. `결과가 틀리게 나오면 코드가 잘못된 것으로
우선 가정`, 코드 재검증 루프를 수렴할 때까지 반복. **단** 루프 5 회
이후에도 "코드는 정확한데 결과가 나쁨" 이면 이론 탈락으로 판정 후
다음 후보 진행.

**코드 리뷰 결과 기록**. `simulations/l3/<ID>/review.md` 에 4 리뷰 각각
의 통과/재작성 이력 기록.

### Phase L3-H. Ranking + 최종 판정

- `simulations/l3/ranking.py`
  - 모든 KEEP 후보를 Δχ² 오름차순 정렬
  - tie-break: 이론 정합성 점수 (L0/L1 직접 연결 강도 0-10)
- `base.l3.result.md` 작성:
  - Keep list (상세 카드: 섭동 결과, MCMC posterior, chi², classy 결과)
  - Kill list (탈락 사유 한 줄)
  - Phase 5 MCMC 진입 후보 전부 명시
  - 전원 탈락 시 `paper/negative_result.md` 부록 작성

### Phase L3-I. 문서 정리

- `base.l3.todo.md` → `base.l3.todo.result.md` 로 실행 로그 append
- `CLAUDE.md` L3 재발방지 규칙 추가
- `base.l3.result.md` 최종 통합본
- `base.l3.todo.md` 는 WBS 원본으로 유지 (삭제 금지)

---

## 📦 산출물 체크리스트

| 파일 | 내용 |
|---|---|
| `refs/l3_kill_criteria.md` | K1-K8, P1-P5 사전 고정 기준 |
| `base.l3.todo.md` | Phase L3-0 ~ L3-I 원자 태스크 WBS |
| `base.l3.todo.result.md` | 실행 로그, 4 인 리뷰 결과, kill/keep 판정 |
| `base.l3.result.md` | 최종 통합 결과 (keep list + kill list + Phase 5 진입 후보) |
| `simulations/l3/data_loader.py` | 통합 데이터 로더 |
| `simulations/l3/lcdm_baseline.py` | LCDM best-fit chi² 기준점 |
| `simulations/l3/perturbation_base.py` | 섭동 theory 템플릿 |
| `simulations/l3/ranking.py` | 최종 ranking |
| `simulations/l3/<ID>/` | 11 후보별 background + pert + chi² + MCMC + classy |
| `simulations/l3/<ID>/review.md` | 4 인 리뷰 이력 |
| `paper/l3_<ID>_perturbation.md` | 섭동 명시 전개 (keep 후보만) |
| `paper/negative_result.md` | 전원 탈락 시 부록 |
| `CLAUDE.md` | L3 재발방지 규칙 추가 |

---

## ⚖️ 최종 판정 규칙

**시나리오 A — 최소 1 개 후보가 P1-P5 전부 통과**
→ Phase 5 MCMC/논문 투고 준비 진입. `base.l3.result.md` 에 keep list
기록, 1 순위 후보에 대해 다음 라운드 (Phase 5) 계획 초안 작성.

**시나리오 B — 모든 후보 K1-K8 에 걸림**
→ 정직하게 `paper/negative_result.md` 에 L3 winnowing negative 결과
부록 작성. 이론 생존 불가 선언. `base.md` 는 "잠정적으로 기각된 가설"
로 재분류.

**시나리오 C — 일부 KEEP 하지만 Δχ² 전부 > 0 (LCDM 보다 나쁨)**
→ "이론 정합성 점수" 로만 ranking. 1-2 후보만 Phase 5 이월, 나머지
kill. base.l3.result.md 에 약한 생존으로 명시.

---

## 🚫 금지 사항

- 사용자 confirm 요청 (끝까지 자동 진행)
- Python 외 언어 사용
- 기준 (K/P) 사후 조정
- 새 L2 관점 추가 (L2 44 후보 외 탐색 금지)
- Chaplygin family, 기타 L2 폐기 후보 재진입
- Toy CPL fit 로만 판정 (반드시 full background ODE)
- 외부 논문 숫자 인용으로 K2 회피 (반드시 Python 재현)
- Vainshtein 사후 주입 (L2 규칙 승계)
- Phantom crossing 허용 (SQMH L0/L1 위반)
- 4 인 리뷰 합의 미통과 결과 사용
- `base.md` 원본 수정
- 결과 왜곡 (시뮬 결과 ≠ 이론 주장 시 정직 기록)

---

## ✅ 필수 준수

- 모든 파일 UTF-8
- CLAUDE.md 재발방지 규칙 전부 준수 (특히):
  - BAO D_V/D_M/D_H 단위 Mpc
  - DESI DR2 공식값 (`w0=-0.757, wa=-0.83`), DR1 혼동 금지
  - E(z) coupled ODE (ad hoc 근사 금지)
  - IDE convention omega=rho/rho_c0, 이중카운팅 금지
  - scipy.optimize multi-start 방어 (`if best[1] is None`)
  - growth ODE drag term `-β·φ_N·δ_N` 포함
  - DESY5 `zHD` 사용
  - numpy 2.x `np.trapezoid`
  - `print()` non-ASCII 금지
  - `matplotlib.use('Agg')` 는 corner import 이전
  - emcee 내부 `np.random.seed`
  - growth ODE 배경은 LCDM 아날리틱 (backward quintessence 폭주 회피)
  - compressed CMB high-z bridge 는 pure LCDM tail
- 4 인 리뷰 전부 pass 한 결과만 채택
- 결과가 나쁘면 먼저 코드 의심 → 4 리뷰 재실행 → 수렴 후에도 나쁘면
  이론 탈락
- 진행 로그는 `base.l3.todo.result.md` 에 지속 append
- 완료 태스크는 `base.l3.todo.md` 에 `[x]` + 결론 한 줄

---

## 📊 예상 계산 비용 (참고용, hard constraint 아님)

| Phase | 시간 추정 | 노트 |
|---|---|---|
| L3-0 기준 고정 | 5 min | 사전 commit |
| L3-A 데이터 로더 | 30 min | Phase 3 재사용 |
| L3-B 섭동 템플릿 | 1 hour | LCDM benchmark |
| L3-C 11 후보 background+chi² | 6-10 hours | 각 30-60 min + 리뷰 |
| L3-D MCMC (keep 후보 × 각 6-8 개) | 8-16 hours | emcee walker 64 × 20000 |
| L3-E CLASS/CAMB | 4-8 hours | hi_class 지원 따라 |
| L3-F 섭동 전개 문서 | 2-4 hours | LaTeX 수식 |
| L3-G 4 인 리뷰 루프 | 누적 +30% | 재작성 분 |
| L3-H Ranking + 문서 | 1 hour | |
| L3-I 정리 | 30 min | |

**총 추정 22-42 시간**. 중단 금지 자동 진행.

---

**문서 이력**. 2026-04-11 작성. L3 winnowing + full-stack 검증 지시서.
사용자 개입 없이 자동 완주. 실행 결과는 `base.l3.result.md` 와
`paper/negative_result.md` (필요 시) 에 기록.
