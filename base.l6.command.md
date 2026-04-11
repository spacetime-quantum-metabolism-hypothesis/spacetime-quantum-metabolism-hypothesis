# base.l6.command.md — L6 Phase-6: Theory Upgrade + Full Evidence + Growth Sector

> `/bigwork-paper` 스킬에 투입할 **최종 확정 지시안**.
> 사용자 confirm 전부 생략. 묻지 말고 끝까지 자동 진행. 언어는 Python.

---

## 실행 명령

```
/bigwork-paper base.l6.command.md 에 기재된 L6 이론 업그레이드 +
완전 marginalized evidence + growth sector + DR3 대응 파이프라인을
끝까지 수행. 사용자 confirm 전부 생략. 묻지 말고 진행. 언어는 Python.
base.l5.result.md, simulations/l5/, paper/, base.md, CLAUDE.md,
refs/l5_kill_criteria.md, L5 전체 결과 참고.
L6 이름으로만 신규 파일 기록.
```

---

## 🎯 근본 목적 (L5 비판 → L6 처방)

**L5 정직한 자기평가에서 출발**: L5 산출물은 JCAP major-revision-accept급
phenomenology paper 1편. "1990년대 quintessence 제안 수준"
(Caldwell-Dave-Steinhardt 1998 비유). 주장 가능한 것과 불가한 것을
엄밀히 구분한 뒤, L6 는 그 간극을 메운다.

**L6 목표**: 현상론 논문 → 이론 기반 예측 논문으로 업그레이드.
"postulate" → "derivation", "fixed-theta evidence" → "properly-marginalized
evidence", "background-only" → "perturbation + growth sector".

### L5 비판 목록 (정직하게 인정)

| 비판 | 심각도 | L6 처방 |
|------|--------|---------|
| **amplitude-lock 이 postulate** — Ω_m 고정은 유도가 아님 | ★★★ | L6-T1: 8인팀 이론 검토 |
| **Δ ln Z = +11.26 은 fixed-theta** — 진짜 marginalized 값은 더 작음 | ★★★ | L6-E: 완전 marginalized + 4인 코드리뷰 |
| **S_8 tension 미해결** — μ=1 구조 한계 | ★★★ | L6-G: μ(a,k) ≠ 1 + 4인 코드리뷰 |
| **CLASS 미구현** — 완전 CMB power spectrum 미검증 | ★★ | L6-G3: CLASS + 4인 코드리뷰 |
| **"5개 프로그램 통합" 주장 불가** — 우주론 채널만 | ★★ | L6-T3: 채널 범위 명시 제한 |
| **Cassini 우연 통과** (pure disformal A'=0 이므로) | ★ | L6-T2: 8인팀 검토 |
| **0-파라미터 alt ≈ 1-파라미터** — 자유도 정당화 불가 | ★ | L6-E3: Occam 분석 |

### L6 성공 기준 (종료 시점)

1. amplitude-locking 이 SQMH L0/L1 에서 **수식으로 유도**되거나,
   유도 불가임을 증명하고 "계층적 postulate" 로 격하 (8인팀 합의 필요)
2. C28, C11D, A12 에 대해 **완전 marginalized** Δ ln Z 산출 (4인 코드리뷰 통과 필수)
3. SQMH 섭동 방정식에서 **μ_eff(a,k)** 해석해 유도 + CLASS 수치 확인
4. μ_eff ≠ 1 인 경우 S_8 tension 개선 **정량화**
5. **DESI DR3 기계적 재실행** 스크립트 준비 완료
6. Paper v2: JCAP → **PRD Letter 또는 MNRAS 급** 판단 근거 확보

---

## 🔬 프로세스 규칙 (L6 전체 적용)

### Rule-A: 이론 확장 시 8인 순차 검토팀

이론 작업 (amplitude-lock 유도, μ_eff 도출, 포지셔닝 문서 등) 마다
아래 8인 팀이 **순서대로** (병렬 아님) 검토. 각 팀원은 이전 팀원의
결과를 참조해 자기 시각에서 분석 추가.

| 순서 | 역할 | 검토 관점 | 핵심 질문 |
|------|------|----------|----------|
| 1 | **물리학자** | 방정식 물리적 일관성 | 에너지-운동량 보존, 인과율 위반? |
| 2 | **수학자** | 수식 엄밀성 | 수렴, 경계조건, 유일성 증명 가능? |
| 3 | **우주론자** | 관측 정합성 | DESI/Planck 기존 결과와 충돌? |
| 4 | **회의론자 (Skeptic)** | 가정 비판 | 어떤 가정이 숨어 있나? 반례? |
| 5 | **관측천문학자** | 검증 가능성 | DR3/Euclid 에서 구분 가능한가? |
| 6 | **철학자/해석자** | 이론적 의미 | 설명인가, 재기술(re-description)인가? |
| 7 | **비교이론가** | 기존 이론 대비 | Caldwell 1998, Dirian 2015 대비 차별성? |
| 8 | **통합자 (Synthesizer)** | 1-7 통합 | 최종 판정: 유도 / postulate / 반증 |

**출력 형식**: 각 이론 작업 결과 문서에 "8인 검토 결과" 섹션 필수.
통합자(8번) 최종 판정이 없으면 해당 이론 주장 사용 금지.

### Rule-B: 코드 작성 후 4인 코드리뷰 팀

모든 Python 스크립트 작성 후 아래 4인이 **순서대로** 리뷰.
4인 전원 PASS 없이 코드 실행 결과를 논문/result에 기록 금지.

| 순서 | 역할 | 검토 항목 |
|------|------|----------|
| 1 | **버그 헌터** | NaN/inf 전파, off-by-one, None unpack, sentinel 합산, 음수 sqrt |
| 2 | **물리 검증자** | 단위(Mpc/km 혼용), 부호(w_a, ν), 정규화 E(0)=1, CLAUDE.md 물리 규칙 80+ |
| 3 | **재현성 검사자** | seed 위치(EnsembleSampler 직전), determinism, JSON _jsonify 변환기, UTF-8 |
| 4 | **규칙 감사자** | CLAUDE.md 전체 규칙 준수, 금지 항목(sentinel 합산, phantom crossing 허용 등), 재발방지 위반 |

**출력 형식**: 코드 파일 첫 주석 블록에
```
# CODE REVIEW: Bug✓ Physics✓ Repro✓ Rules✓  [날짜]
```
태그 없으면 미완성 코드로 간주, 결과 사용 금지.

---

## 📐 Kill / Keep 기준 (L6 신규)

**실행 시작 전에** `refs/l6_kill_criteria.md` 에 아래 기준 commit 후 고정.
실행 도중 임계값 조정 **금지**.

### L6 KILL 조건

| ID | 조건 | 결과 |
|----|------|------|
| **K17** | Marginalized Δ ln Z < +2.5 (Q8 재검증) | KILL — fixed-theta 아티팩트 확인 |
| **K18** | μ_eff(a=1, k=0.1/Mpc) < 0.8 또는 < 0 (ghost) | KILL — 불안정 섭동 |
| **K19** | CLASS full CMB χ² vs Planck > LCDM + 6 | KILL — CMB 죽음 |
| **K20** | 8인팀 Synthesizer: "반증" 판정 | 해당 이론 주장 폐기 |

### L6 KEEP 조건

| ID | 조건 |
|----|------|
| **Q13** | Marginalized Δ ln Z ≥ +2.5 (4인 코드리뷰 통과 코드로 산출) |
| **Q14** | CLASS Planck CMB χ² ≤ LCDM + 3 |
| **Q15** | μ_eff 유도 가능 + S_8 tension Δ(S_8) ≥ 0.010 개선 |
| **Q16** | DESI DR3 실측 w_a < 0 지속 + C11D/C28 ≥ 2σ 분리 |
| **Q17** | amplitude-locking 수식 유도 성공 (8인팀 합의) |

---

## 🧭 실행 순서

### Phase L6-0. 기준 고정 + 환경 점검

- `refs/l6_kill_criteria.md` 에 K17-K20, Q13-Q17 기재 후 저장
- `base.l6.todo.md` WBS 작성
- `simulations/l6/` 디렉터리 생성
- Python 환경 확인: dynesty, hi_class (또는 classy), emcee

---

### Phase L6-T. 이론 업그레이드 (8인팀 필수)

> **모든 L6-T 서브태스크는 Rule-A (8인 순차 검토) 적용.**
> 8인 검토 없이 이론 주장 논문 반영 금지.

#### L6-T1. Amplitude-locking 유도 시도 (8인팀)

**목표**: E²(z) = E²_LCDM + Ω_m · f(m·(1−a)) 에서
drift amplitude 가 왜 Ω_m 에 lock 되는가?

**접근 1 — SQMH 연속방정식 적분**:
- L0/L1: dn/dt + ∇·(nv) = Γ₀ − σ n ρ_m
- 배경 평균: dρ_DE/dt 에서 drift amplitude 추출
- Q: 정규화 E(0)=1 만으로 α_Q = Ω_m 이 uniquely fixed 되는가?

**접근 2 — 에너지 보존 강제**:
- E(0)=1 + 에너지 보존 두 조건이 자유 파라미터를 모두 고정하는가?
- 목표: zero-parameter 가 이론적 귀결인지 수치적 우연인지 판별

**접근 3 — CLW attractor (C11D 해석)**:
- V(φ) = V₀ exp(−λφ) tracker 해에서 Ω_φ(a) 의 Ω_m 의존성

**8인팀 검토 후 최종 판정**:
- "유도 성공": 수식 명시 → §3 paper 추가
- "에너지 보존 귀결": "thermodynamic postulate" 로 격하
- "순수 수치 우연 / 반증": K20, 해당 주장 폐기

산출: `refs/l6_amplitude_lock_analysis.md` (8인 검토 결과 섹션 포함)

#### L6-T2. C11D 일반 disformal (A' ≠ 0) PPN 분석 (8인팀)

- Pure disformal A'=0 → γ=1 exact (ZKB 2013) — "우연" 비판 대응
- A'≠0 에서 허용 범위 도출: Cassini |γ−1| < 2.3×10⁻⁵ → |A'| < ?
- 해당 A' 범위에서 background w(z) 변화량 ≤ measurement uncertainty?
- 8인팀: A'=0 물리적 강제 이유가 있는가, 또는 fine-tuning 인가?

산출: `refs/l6_c11d_general_disformal.md`

#### L6-T3. 이론 포지셔닝 문서 (8인팀)

현재 SQMH 의 정확한 이론 위상 문서화:

- **주장 가능 (8인 합의)**: DR3 falsifiable 예측 + zero-parameter 재현
- **주장 불가**: "SQMH 가 DESI 를 유도" / "멘델레예프 단계"
- Caldwell-Dave-Steinhardt 1998 비교: 무엇이 같고 무엇이 더 강한가
- PRD Letter 진입에 필요한 조건 명시

산출: `refs/l6_theory_positioning.md`

---

### Phase L6-E. 완전 Marginalized Bayesian Evidence (4인 코드리뷰 필수)

> **모든 L6-E 코드는 Rule-B (4인 코드리뷰) 통과 후 결과 사용.**

#### L6-E1. C28 완전 3D marginalized

L5 에서 C28 evidence = θ=(γ_0, β_shape, a_tail) 을 L4 MAP 고정,
(Om, h) 2D 샘플링 → fixed-theta 비판 대상.

완전 marginalized: (Om, h, γ_0) 3D 샘플링.
(β_shape, a_tail 은 poorly constrained → prior volume 패널티 반영.)

```python
# 설계
ndim = 3  # Om, h, gamma0
nlive = 800
prior: Om in [0.28,0.36], h in [0.64,0.71], gamma0 in [0,0.01]
# 4인 코드리뷰 태그 필수
# CODE REVIEW: Bug? Physics? Repro? Rules?  [날짜]
```

- 예상: Δ ln Z 감소 (Occam 패널티 ~2-4 units)
- K17 재검증: Δ ln Z ≥ +2.5?

산출: `simulations/l6/evidence/evidence_C28_full.json`

#### L6-E2. C11D 3D marginalized 재실행 (nlive 증가)

L5: 3D (Om, h, lam), nlive=350 → 부족.
L6: nlive=1000 으로 재실행. 예상 Δ ln Z ≈ +8-9 유지.

산출: `simulations/l6/evidence/evidence_C11D_full.json`

#### L6-E3. Occam 분석 통합

C28 (1-param) vs A12 (0-param) 의 Δ ln Z 격차 vs 이론적 Occam 패널티 비교:
- 이론적 Occam: −0.5 ln(prior_vol / posterior_vol) ≈ ?
- 실제 격차: Δ ln Z(C28) − Δ ln Z(A12)
- 결론: "데이터가 extra parameter 를 정당화하지 않음" 정량화

산출: `simulations/l6/evidence/occam_analysis.json`

---

### Phase L6-G. Growth Sector — μ(a,k) ≠ 1 (4인 코드리뷰 필수)

> **모든 L6-G 코드는 Rule-B 통과 필수.**
> 이론 도출 부분은 Rule-A (8인팀) 도 적용.

#### L6-G1. SQMH 섭동 방정식 도출 (이론: 8인팀)

SQMH 라그랑지안 (base.md §4.1) → 선형 섭동:

- C11D: Bellini-Cuesta-Jimenez-Verde 2012 (A'=0 극한)
  μ_eff = 1 + 2β²/(1 + β²k²/M_eff²)
- C28 RR non-local: Dirian 2015 eq 3.8 Δ_eff(k) 보정
- A12: 현상론적 — μ_eff = 1 (no perturbation coupling 선언)

8인팀 검토: 각 도출 수식 물리적 타당성 확인.

#### L6-G2. μ_eff 수치 계산 (코딩: 4인 리뷰)

`simulations/l6/growth/mu_eff_profiles.py`:
- k ∈ [0.01, 1.0] /Mpc, a ∈ [0.1, 1.0] 그리드
- K18: μ_eff < 0 (ghost) 또는 < 0.8 → KILL
- S_8 재계산: σ_8(z=0) 에 μ_eff(a,k) 성장 적분 반영
- K15 Q15: ΔS_8 ≥ 0.010 개선 여부

산출: `mu_eff_profiles.py` + `mu_eff.json` + `s8_mu_correction.json`

#### L6-G3. CLASS 구현 (4인 코드리뷰 필수)

hi_class 또는 CLASSy 사용:
- C11D pure disformal: `gravity_model = 'propto_omega'` 근사
- CMB TT/EE vs Planck 2018 χ²
- K19: Δχ²_CMB ≤ +3 (LCDM 대비)

hi_class 미설치 → 분석해 근사 (Hu-Sawicki-like transfer) 대체.
실패 시: "full CLASS verification 미완" §8 정직 기록. 결과 왜곡 금지.

산출: `simulations/l6/class/<ID>/cmb_spectrum.py` + `cmb_chi2.json`

---

### Phase L6-D. DESI DR3 재실행 준비

DESI DR3 데이터 공개 즉시 기계적 재실행 가능하도록 준비.

#### L6-D1. 재실행 스크립트 작성 (4인 코드리뷰)

`simulations/l6/dr3/run_dr3.sh`:
```bash
# DR3 공개 후: git pull CobayaSampler/bao_data
# → re-run simulations/l4/desi_fitting.py (DR3 데이터 경로 자동 감지)
# → diff vs L5 result → generate dr3_vs_l5_diff.json
```

주의: BAO 데이터 포맷 변화 (DR2 vs DR3 column 차이) 자동 감지 로직 필수.

#### L6-D2. DR3 해석 시나리오 (이론: 8인팀)

| 시나리오 | DR3 결과 | SQMH 결론 |
|---------|----------|-----------|
| α | w_a < −0.5 (강화) + C11D/C28 ≥ 3σ 분리 | PRD Letter 업그레이드 |
| β | w_a < 0 유지 + < 2σ 분리 | JCAP 현상론 유지 |
| γ | w_a > 0 (역전) | w_a 부호 예측 falsified |
| δ | phantom crossing (w < −1) | SQMH L0/L1 falsified |
| ε | A04 outlier |w_a| ≈ 0.5 (~8σ 분리) | alt-class 강력 지지 |

8인팀: 각 시나리오에서 SQMH 대응 전략 사전 합의.

---

### Phase L6-P. Paper v2 업그레이드

#### L6-P1. 이론 섹션 재작성

- §2: amplitude-locking 8인팀 최종 판정 반영
  (유도 성공 → 수식, postulate 확정 → 명시)
- §3: μ_eff(a,k) 해석해 + CLASS χ² 결과
- §4: Occam 분석 + properly-marginalized Δ ln Z 표

#### L6-P2. 저널 타깃 결정 트리 (8인팀 합의)

```
IF amplitude-lock 유도 성공 (Q17):
    AND marginalized Δ ln Z(C28) ≥ +5 (Q13):
    AND CLASS pass K19 (Q14):
    → PRD Letter (3-4 pages)

ELIF marginalized Δ ln Z ≥ +2.5 (Q13):
    AND 8인팀 "주장 가능" 목록 준수:
    → JCAP (현 수준 유지 + 정직한 §8)

ELSE (K17 fail — marginalized evidence 붕괴):
    → arXiv-only: "fixed-theta evidence 아티팩트 확인" 논문
```

---

## 📦 산출물 체크리스트

| 파일 | 포함 필수 태그 |
|------|--------------|
| `refs/l6_kill_criteria.md` | — |
| `refs/l6_amplitude_lock_analysis.md` | 8인 검토 결과 섹션 |
| `refs/l6_c11d_general_disformal.md` | 8인 검토 결과 섹션 |
| `refs/l6_theory_positioning.md` | 8인 검토 결과 섹션 |
| `simulations/l6/evidence/evidence_C28_full.json` | 코드에 4인 리뷰 태그 |
| `simulations/l6/evidence/evidence_C11D_full.json` | 코드에 4인 리뷰 태그 |
| `simulations/l6/evidence/occam_analysis.json` | 코드에 4인 리뷰 태그 |
| `simulations/l6/growth/mu_eff_profiles.py` | 4인 리뷰 태그 + 8인 이론 검토 |
| `simulations/l6/growth/s8_mu_correction.json` | 코드에 4인 리뷰 태그 |
| `simulations/l6/class/<ID>/cmb_chi2.json` | 코드에 4인 리뷰 태그 |
| `simulations/l6/dr3/run_dr3.sh` | 코드에 4인 리뷰 태그 |
| `base.l6.result.md` | 시나리오 판정 + 8인/4인 완료 확인 |
| `paper/` (v2) | L6 결과 반영 |

---

## ⚖️ L6 시나리오 판정

**시나리오 A — 완전 업그레이드 성공**:
amplitude-lock 유도 + marginalized STRONG + CLASS pass + S_8 개선
→ PRD Letter 타깃. 8인팀 "이론 기반 zero-parameter 예측" 합의.

**시나리오 B — 부분 업그레이드**:
lock postulate 공식 격하 + marginalized substantial + CLASS 통과
→ JCAP 유지. "정직한 현상론 + DR3 falsifier" 포지셔닝 확정.

**시나리오 C — Evidence 붕괴 (K17)**:
marginalized Δ ln Z < +2.5
→ arXiv negative result: "fixed-theta L5 evidence 는 Occam 아티팩트"

**시나리오 D — DR3 falsification**:
DESI DR3 w_a > 0 또는 phantom crossing
→ SQMH background-level falsified. Phase 7 = UV 재설계 또는 포기.

---

## 🚫 금지 사항

- **이론 주장**: 8인팀 Synthesizer 판정 없이 논문 반영 금지
- **코드 결과**: 4인 코드리뷰 태그 없이 result.md / paper 기록 금지
- fixed-theta evidence 값을 marginalized 값으로 발표 금지
- CLASS 미검증 상태에서 "full CMB consistent" 주장 금지
- L5 KILL 후보 (C27, C26, C33, C41) 재진입 금지
- DR3 전에 "DR3 에서 확인될 것" 확언 금지 (예측만)
- 기준 (K/Q) 사후 조정 금지 (실행 전 refs/l6_kill_criteria.md 고정)
- `base.md` 원본 수정 금지
- 결과 왜곡 (K17 fail 인데 STRONG 기록) 금지

---

## 📊 실행 순서 우선순위

```
즉시 (이론 분석, 수일):
  L6-0 기준 고정
  L6-T3 이론 포지셔닝 (8인팀) — 가장 가벼운 이론 작업
  L6-T1 amplitude-lock 시도 (8인팀)

병렬 가능 (수주):
  L6-E1 C28 full evidence (4인 리뷰) ←→ L6-G1/G2 μ_eff (8인+4인)

CLASS (수주~수개월, 의존성 높음):
  L6-G3 — hi_class 설치 복잡, 별도 세션

DR3 공개 후 (수시간, 기계적):
  L6-D1 자동 재실행 스크립트 실행

논문 (L6-T/E/G 완료 후):
  L6-P → 저널 타깃 결정 (8인팀 최종 합의)
```

---

## ✅ 필수 준수

- L1-L5 모든 CLAUDE.md 규칙 승계 (총 90+ 규칙)
- **Rule-A**: 이론 확장 → 8인 순차 검토 (병렬 금지)
- **Rule-B**: 코드 작성 → 4인 순차 코드리뷰, 태그 필수
- 모든 파일 UTF-8, print() non-ASCII 금지
- `matplotlib.use('Agg')` 는 `import corner` 이전
- numpy 2.x `np.trapezoid`
- dynesty 3.0.0: rstate = `np.random.default_rng(seed)`
- MCMC `log_prob` sentinel 합산 금지 → None/nan 시 `-np.inf`
- 결과 `base.l6.todo.result.md` 에 실시간 append
- 완료 태스크 `base.l6.todo.md` 에 `[x]` + 결론 한 줄

---

**문서 이력**. 2026-04-11 작성 및 개선.
L5 비판 ("JCAP급 현상론") → L6 처방:
이론 확장은 8인 순차 검토팀, 코드는 4인 코드리뷰 통과 필수,
실행은 `/bigwork-paper base.l6.command.md` 로 자동 완주.
