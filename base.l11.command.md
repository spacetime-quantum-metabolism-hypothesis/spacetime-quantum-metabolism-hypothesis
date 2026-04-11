# base.l11.command.md — L11 Phase-11: 볼츠만 출생-사망 동형성 → 경험식 파생 20개

> 작성일: 2026-04-11. L10 완료 이후 설계.
> 사용자 confirm 전부 생략. 묻지 말고 끝까지 자동 진행. 언어는 Python.

---

## 실행 명령

```
/bigwork-theory base.l11.command.md 에 기재된 L11
볼츠만 출생-사망 동형성 경험식 파생 20개 파이프라인을 끝까지 수행.
사용자 confirm 전부 생략. 묻지 말고 진행. 언어는 Python.
base.l10.result.md, base.l9.result.md, refs/l8_new_findings.md,
refs/l9_final_verdict.md, base_3.md, CLAUDE.md 전부 참고.
L11 이름으로만 신규 파일 기록.
```

---

## 근본 목적

**핵심 통찰 (NF-3)**:

SQMH 방정식은 Boltzmann 선형 출생-사망 과정과 수학적으로 동형이다.

```
dn̄/dt + 3Hn̄ = Γ₀ − σn̄ρ_m
↕ 동형
dN/dt = λ − μN   (출생률 λ=Γ₀, 소멸률 μ=σρ_m+3H)
```

볼츠만 출생-사망 과정은 물리학/생물학/화학/통계학 전반에 걸쳐
수십 개의 경험식과 연결되어 있다.

**L11 전략**:
이 동형성을 역방향으로 활용한다.
볼츠만 출생-사망에서 유도된 기존 경험식들을
SQMH 변수로 치환하여 새로운 우주론 경험식을 파생.
파생된 경험식이 관측 가능한 예측을 주는가?

---

## 프로세스 규칙

- **이론 검토**: 서로 중복되지 않은 8인팀. 수단과 방법을 가리지 않고 동시에 병렬 및 상호토의를 통해 유도. 결과를 취합하여 최종 판정.
- **코드**: Rule-B 4인 순차 코드리뷰, 태그 필수.
- **주장 언어**: 경험식 파생 성공 시 "SQMH birth-death isomorphism predicts X"
  - 금지: "SQMH proves X" (파생된 경험식은 현상론 수준)
- **관측 가능성 기준**: 파생 결과가 현재 또는 2030년대 관측으로 검증 가능해야 의미 있음

---

## Kill / Keep 기준 (L11 신규, 실행 전 고정)

**실행 시작 전** `refs/l11_kill_criteria.md` 에 아래 기준 고정.

### L11 KILL 조건

| ID | 조건 | 결과 |
|----|------|------|
| **K61** | 15개 시도 전부 SQMH 변수 치환 후 물리적으로 의미 없는 결과 | 볼츠만 동형성 경험식 파생 전략 폐기. |
| **K62** | 가장 유망한 시도 3개 모두 관측 불가 예측만 생성 | 경험식 파생이 현상론적 가치 없음 확정. |
| **K63** | 8인팀 "사후 합리화" 판정 | 해당 파생 경험식 클레임 철회. |

### L11 KEEP 조건

| ID | 조건 | 결과 |
|----|------|------|
| **Q61** | 15개 중 1개 이상: SQMH → 관측가능한 정량 예측 성공 | 논문 §discussion "새 경험식" 섹션 추가. |
| **Q62** | MM 전이 곡선이 A12 erf와 수치적으로 유사 (χ²/dof < 2) | A12 연결 새 경로 발견. §2 이론 연결 부활 가능. |
| **Q63** | wₐ < 0 방향성이 상세 균형 접근으로 설명 | wₐ<0의 물리 의미 최초 SQMH 유래 설명. |
| **Q64** | 다크에너지 출현 적색이동 z_DE 정량 예측 성공 | falsifiable prediction 추가. |
| **Q65** | 비가우시안성(bispectrum) 예측이 Euclid 검출 가능 수준 | 2030년대 새 검증 채널. |

---

## 15개 시도 목록

### [시도 1] Michaelis-Menten 전이 → w(z) 경험식

**동형 출처**: 효소 반응 동역학. 고기질/저기질 농도 극한에서 다른 거동.
**SQMH 적용**:
- 고ρ_m 극한: n̄_eq → Γ₀/(σρ_m) → w → -1 + σρ_m/(3H)
- 저ρ_m 극한: n̄_eq → Γ₀/(3H) → w → 다른 값
- 전이 곡선: w(ρ_m) = -1 + ρ_m/(ρ_m + K_M), K_M = 3H/σ (미카엘리스 상수)
**목표**: 이 w(z) 곡선이 A12 erf 형태와 수치적으로 얼마나 유사한가?
**수치**: `simulations/l11/michaelis/mm_vs_erf.py`
**Q62 판정**: χ²/dof < 2이면 PASS

---

### [시도 2] 마스터 방정식 → ρ_DE 확률분포

**동형 출처**: 이산 마스터 방정식. 정상 분포 = 음이항(Negative Binomial).
**SQMH 적용**:
- n̄ 이산 분포: P(n) = NegBin(r, p), r = Γ₀/H, p = σρ_m/(σρ_m + 3H)
- ρ_DE = n̄ × (플랑크 에너지) → ρ_DE 분포 계산
- <ρ_DE>, Var(ρ_DE), skewness 예측
**목표**: ρ_DE 요동의 크기와 비가우시안성 예측
**수치**: `simulations/l11/master/master_equation_rhode.py`

---

### [시도 3] 첫 통과 시간 → 다크에너지 출현 적색이동 z_DE

**동형 출처**: 출생-사망에서 상태 0 → 상태 n에 도달하는 평균 시간.
**SQMH 적용**:
- n̄ = 0 (다크에너지 없음) → n̄ = n̄_eq (현재값) 도달 시간
- τ_DE = 1/(effective birth rate) = 1/(Γ₀/n̄_eq)
- τ_DE를 우주 나이 t(z)와 비교 → z_DE 예측
**목표**: 다크에너지가 "켜지는" 적색이동 정량 예측
**수치**: `simulations/l11/first_passage/dark_energy_onset.py`
**Q64 판정**: z_DE 예측값이 관측 z_DE ~ 0.3~0.5와 일치하면 PASS

---

### [시도 4] 상세 균형 → wₐ < 0 방향성 해석

**동형 출처**: 출생-사망 상세 균형: λ_n = μ_{n+1} (평형 조건).
**SQMH 적용**:
- 상세 균형: Γ₀ = σn̄ρ_m + 3Hn̄ (완전 평형)
- 현재 우주는 평형에서 벗어남: Γ₀ > or < σn̄ρ_m + 3Hn̄?
- 비평형 방향 → wₐ 부호 결정
- wₐ < 0: 계가 위에서 평형으로 수렴 (과도 생성 → 감소)
- wₐ > 0: 계가 아래에서 평형으로 수렴 (과도 소멸 → 증가)
**목표**: wₐ < 0의 방향성에 SQMH 물리 의미 부여
**수치**: `simulations/l11/detailed_balance/wwa_direction.py`
**Q63 판정**: wₐ < 0가 상세 균형 접근 방향과 정합적이면 PASS

---

### [시도 5] 요동-소산 정리 → G_eff/G 응답함수 경험식

**동형 출처**: FDT: <x(t)x(0)> = kT × χ(t) (응답함수).
**SQMH 적용**:
- n̄ 요동 <δn̄(t)δn̄(0)> = n̄_eq × exp(-t/τ_rel), τ_rel = 1/(σρ_m + 3H)
- δG_eff/G = (σ/ρ_crit) × <δn̄> × (물질 섭동 응답)
- G_eff/G(k, z) = 1 + SQMH_FDT_correction(k, z)
**목표**: C28과 다른 경로에서 G_eff/G(k,z) 스케일 의존성 예측
**수치**: `simulations/l11/fdt/geff_response.py`

---

### [시도 6] 슈테판-볼츠만 유사 → Γ₀ 자연성 경험식

**동형 출처**: 광자 출생-사망(흑체) → ρ_복사 = (π²/30) T⁴.
**SQMH 적용**:
- 시공간 양자가 T_Planck에서 열평형이라면:
- ρ_n = C × (kT_Planck)⁴ / (ℏc)³ × (축퇴인수)
- 이것이 Γ₀ × n̄_eq와 매칭되는가?
- C 계산 → Γ₀ 예측값과 비교
**목표**: 슈테판-볼츠만 유추로 Γ₀ 스케일 자연성 설명 시도
**수치**: `simulations/l11/stefan_boltzmann/sb_gamma0.py`

---

### [시도 7] 생성함수 → 다크에너지 비가우시안성 예측

**동형 출처**: 출생-사망 생성함수 G(z,t) = Σ P(n,t)zⁿ → 모든 모멘트.
**SQMH 적용**:
- G(s,t) 마스터 방정식에서 해석적 풀이
- <n̄²> - <n̄>² → Var(ρ_DE)/ρ_DE²
- 3차 누적률 → ρ_DE bispectrum
- 4차 → trispectrum
**목표**: Euclid에서 검출 가능한 ρ_DE 비가우시안성 수준 예측
**수치**: `simulations/l11/generating_func/dark_energy_cumulants.py`
**Q65 판정**: bispectrum 신호 > Euclid 노이즈이면 PASS

---

### [시도 8] WKB/큰수 극한 → SQMH 유효 작용원리

**동형 출처**: 이산→연속 극한에서 마스터 방정식 → Fokker-Planck → 경로적분.
**SQMH 적용**:
- V_eff(n̄) = κn̄²/2 − Γ₀n̄ (NF-9 후보)
- 경로적분: Z = ∫Dn̄ exp(-S[n̄]/ℏ_eff)
- S[n̄] = ∫dt [n̄̇²/(2Γ₀) + V_eff(n̄)]
- 이것이 특정 스칼라장 이론 Lagrangian과 동일한가?
- → 노에터 정리 → 보존량 → 새 경험식
**목표**: SQMH 보존량 (에너지, 운동량, 전하) 파생
**수치**: `simulations/l11/wkb_action/sqmh_lagrangian.py`

---

### [시도 9] Gillespie 알고리즘 → 확률론적 H(z) 산포

**동형 출처**: Gillespie 알고리즘 = 출생-사망 과정의 정확한 확률 실현.
**SQMH 적용**:
- 각 "사건" (시공간 양자 생성/소멸) → n̄(t) 특정 경로
- n̄(t) → ρ_DE(t) → H(z) 궤적
- 앙상블 평균: <H(z)> ± σ_H(z)
- σ_H(z) 예측 → DESI BAO 산포와 비교
**목표**: H(z) 측정 산포에서 SQMH 양자 잡음 시그니처 탐색
**수치**: `simulations/l11/gillespie/stochastic_hz.py`

---

### [시도 10] 절멸 확률 → 다크에너지 붕괴 시나리오

**동형 출처**: 출생-사망에서 n=0 흡수 상태 도달 확률 P_ext = (μ/λ)^n₀.
**SQMH 적용**:
- P_extinction = (σρ_m + 3H / Γ₀)^n̄₀
- 현재 우주: λ=Γ₀, μ=σρ_m+3H 비율 계산
- P_ext(z=0) → n̄₀를 어떻게 정의하는가?
- 다크에너지 미래: Big Crunch? 평형? 영원 팽창?
**목표**: SQMH에서 우주 종말 시나리오 정량화
**수치**: `simulations/l11/extinction/dark_energy_fate.py`

---

### [시도 11] 준종(Quasi-species) 방정식 → σ 분포 폭

**동형 출처**: Eigen 준종 방정식 = 출생-사망 + 돌연변이 행렬.
**SQMH 적용**:
- 시공간 양자가 σ₁, σ₂, ..., σ_k 값을 가질 수 있다고 가정
- 전이 행렬 W_ij (돌연변이 = σ 값 변화)
- 정상 분포: σ_eff = Σ p_i σ_i (유효 커플링)
- 이것이 NF-1 σ RG running을 대체하는가?
**목표**: σ가 단일 값이 아닌 분포를 가질 때 우주론 기여
**수치**: `simulations/l11/quasispecies/sigma_distribution.py`

---

### [시도 12] 분기 과정 → 시공간 위상 요동

**동형 출처**: Galton-Watson 분기 과정. 각 개체가 자손을 낳음.
**SQMH 적용**:
- 각 시공간 양자가 "자손" 양자를 생성할 수 있다고 가정
- 분기 확률 생성함수 f(s) = Σ p_k s^k
- 임계 분기(평균 자손 수 = 1): σρ_m = Γ₀ + 3H
- 임계점 → 스케일 불변 요동 → 멱함수 분포
**목표**: SQMH 임계점에서 스케일 불변 ρ_DE 요동 예측
**수치**: `simulations/l11/branching/critical_branching.py`

---

### [시도 13] 화학 마스터 방정식 → ρ_DE 요동 주파수 스펙트럼

**동형 출처**: CME → Fokker-Planck → O-U 과정 → S(ω) = 2D/(ω²+γ²).
**SQMH 적용**:
- 완화율: γ = σρ_m + 3H ~ H₀
- 확산: D = Γ₀/2 (포아송 잡음)
- ρ_DE 요동 스펙트럼: S_DE(ω) = 2D/(ω² + H₀²)
- ω = H₀에서 피크 → 허블 시간 스케일 요동
**목표**: ρ_DE 요동의 주파수 스펙트럼 → 21cm/PTA에서 검출 가능성
**수치**: `simulations/l11/cme_spectrum/rhode_power_spectrum.py`

---

### [시도 14] Kingman 합체 (역방향) → SQMH 인과 기원

**동형 출처**: Kingman coalescent = 역방향 출생-사망. 현재 → 과거로 역추적.
**SQMH 적용**:
- 역방향 SQMH: dn̄/dt = -(Γ₀ − σn̄ρ_m − 3Hn̄)
- 모든 시공간 양자가 단일 "공통 조상"으로 합체되는 시간 T_MRCA
- T_MRCA = 플랑크 시간? 인플레이션 종료 시점?
- T_MRCA가 우주론적 초기 조건을 결정하는가?
**목표**: SQMH의 우주론적 기원 시점 정량화
**수치**: `simulations/l11/kingman/sqmh_coalescent.py`

---

### [시도 15] 영-팽창 포아송 → 우주 공동(Void)에서 ρ_DE 편향

**동형 출처**: Zero-inflated Poisson = 일부 영역에서 n=0 (출생이 없음).
**SQMH 적용**:
- 우주 공동(Void): 물질 밀도 ρ_m → 0 → σρ_m → 0
- σρ_m → 0이면: n̄_eq → Γ₀/(3H) (최대값)
- 우주 필라멘트: ρ_m 높음 → n̄_eq 낮음
- 공동 vs 필라멘트 ρ_DE 차이: Δρ_DE/ρ_DE = f(ρ_m)
- → DESI void catalog에서 검출 가능한 ρ_DE 편향
**목표**: 우주 대규모 구조에서 ρ_DE 공간 분포 이질성 예측
**수치**: `simulations/l11/void_bias/rhode_void_bias.py`
**관측**: DESI void 통계 + Dark Energy Survey void lensing

---

### [시도 16] 재규격화군 고정점 → σ의 적외선 고정점 해석

**동형 출처**: RG 흐름에서 출생-사망 결합 상수의 고정점.
**SQMH 적용**:
- σ = 4πGt_P가 QG RG 흐름의 적외선(IR) 고정점인가?
- β함수: β(σ) = μ dσ/dμ = 0 at σ_IR = 4πGt_P
- 자외선 고정점 σ_UV → IR 흐름 → σ_SQMH
- 점근 안전성 (AS)의 σ analogon 계산
**목표**: σ = 4πGt_P가 RG 의미에서 "자연스러운" 값임을 보이기
**수치**: `simulations/l11/rg_fixed_point/sigma_ir_fixed.py`

---

### [시도 17] 엔트로피 생성률 → wₐ 부호와 열역학 화살

**동형 출처**: 비가역 출생-사망 → 엔트로피 생성: dS/dt = Σ J·F ≥ 0.
**SQMH 적용**:
- 엔트로피 생성률: dS/dt = (Γ₀ − σn̄ρ_m) × ln(Γ₀/(σn̄ρ_m))
- 상세 균형 위반이 클수록 dS/dt 크다
- wₐ < 0 ↔ dS/dt > 0 (열역학 제2법칙)
- 정량적: wₐ = f(dS/dt, H, ρ_m) 경험식 유도
**목표**: wₐ < 0를 엔트로피 생성률로 직접 표현하는 경험식
**수치**: `simulations/l11/entropy_prod/wwa_entropy.py`
**검증**: dS/dt > 0이면 Q63과 연동 (상세균형 접근 방향 확인)

---

### [시도 18] Turing 불안정성 → 다크에너지 공간 패턴 조건

**동형 출처**: 두 성분 반응-확산계에서 Turing 패턴 (λ_u ≠ λ_v).
**SQMH 적용**:
- (n̄, δ_m) 2성분 계: n̄ 방정식 + 물질 섭동 δ_m 방정식 결합
- Turing 조건: |f_n g_m| < 0, 확산비 D_n/D_m >> 1
- SQMH는 확산항 없으므로 Turing 패턴 발생 조건이 다름
- 대신: 결합 섭동계에서 불안정 모드 탐색
**목표**: SQMH-물질 결합에서 다크에너지 공간 클러스터링 조건
**수치**: `simulations/l11/turing/sqmh_turing.py`
**관측 연결**: DESI 대규모 구조에서 ρ_DE 클러스터링 신호

---

### [시도 19] Lyapunov 함수 → 다크에너지 안정성 증명 + w > -1 재유도

**동형 출처**: 출생-사망 자유에너지: F[n̄] = n̄ ln(n̄/n̄_eq) − n̄ + n̄_eq, dF/dt ≤ 0.
**SQMH 적용**:
- SQMH Lyapunov 함수: V(n̄) = n̄ ln(n̄/n̄_eq) − (n̄ − n̄_eq)
- dV/dt = −(n̄ − n̄_eq)² × (σρ_m + 3H)/n̄ ≤ 0 (전역 안정성)
- 전역 안정성 → n̄ → n̄_eq 보장 → w → -1 (점근)
- w > -1 항상 (NF-12)을 Lyapunov 관점에서 독립 재유도
**목표**: NF-12 (w > -1) 의 3번째 독립 증명 + 안정성 시간 스케일
**수치**: `simulations/l11/lyapunov/sqmh_stability.py`

---

### [시도 20] 대편차 이론 → ρ_DE 초과 요동 확률

**동형 출처**: 출생-사망 대편차: P(n >> n̄_eq) ~ exp(−N × I(n/n̄_eq)), I(x) = x ln x − x + 1.
**SQMH 적용**:
- N = n̄_eq × V_허블 (허블 부피 내 총 시공간 양자 수)
- P(ρ_DE >> <ρ_DE>) ~ exp(−N × I(ρ_DE/<ρ_DE>))
- N ~ 10¹²³ (플랑크 부피로 허블 부피 나눔)
- → P(ρ_DE 10배 초과) ~ exp(−10¹²³) ≈ 0 (극도로 억제)
- 우주상수 문제: "왜 ρ_DE가 현재값인가?" → 대편차로 해석
**목표**: 다크에너지 미세조정 문제에 SQMH 통계역학적 해석 제시
**수치**: `simulations/l11/large_deviation/rhode_fluctuation.py`
**철학적 의미**: ρ_DE의 현재값은 대편차 의미에서 "전형적" 값

---

## 실행 순서

### Phase L11-0. 기준 고정 + 문서 준비

- `refs/l11_kill_criteria.md` K61-K63, Q61-Q65 기재
- `base.l11.todo.md` WBS 작성
- `simulations/l11/` 디렉터리 생성 (15개 서브디렉터리)

---

### Phase L11-A. 15개 시도 병렬 실행

> 이론: 서로 중복되지 않은 8인팀, 수단과 방법을 가리지 않고 동시에 병렬 및 상호토의.

각 시도별 산출:
- 이론 도출 문서 (8인 병렬 토의)
- Python 수치 검증 코드 (Rule-B 4인)
- Kill/Keep 개별 판정

**우선순위 처리 순서**:
1. 시도 1 (MM), 시도 3 (첫통과), 시도 4 (상세균형) — 관측 연결 가능성 최고
2. 시도 7 (생성함수), 시도 15 (void 편향) — 새 관측 채널
3. 나머지 10개

---

### Phase L11-N. 수치 통합 + 랭킹

- `simulations/l11/integration/l11_comparison.py`
- 15개 결과 취합 → 관측 가능성 점수 매기기
- Q61-Q65 수치 판정

---

### Phase L11-I. 통합 판정 (8인)

- `refs/l11_integration_verdict.md`
- 관측 가능한 경험식 순위 1~15 확정
- 논문 반영 가능 경험식 선별
- `base.l11.result.md` 작성

---

## 산출 파일 목록

| 파일 | 내용 |
|------|------|
| `refs/l11_kill_criteria.md` | K61-K63, Q61-Q65 |
| `refs/l11_derivation_all15.md` | 15개 시도 8인 토의 전체 |
| `refs/l11_integration_verdict.md` | 8인 통합 판정 |
| `simulations/l11/michaelis/mm_vs_erf.py` | 시도 1 |
| `simulations/l11/master/master_equation_rhode.py` | 시도 2 |
| `simulations/l11/first_passage/dark_energy_onset.py` | 시도 3 |
| `simulations/l11/detailed_balance/wwa_direction.py` | 시도 4 |
| `simulations/l11/fdt/geff_response.py` | 시도 5 |
| `simulations/l11/stefan_boltzmann/sb_gamma0.py` | 시도 6 |
| `simulations/l11/generating_func/dark_energy_cumulants.py` | 시도 7 |
| `simulations/l11/wkb_action/sqmh_lagrangian.py` | 시도 8 |
| `simulations/l11/gillespie/stochastic_hz.py` | 시도 9 |
| `simulations/l11/extinction/dark_energy_fate.py` | 시도 10 |
| `simulations/l11/quasispecies/sigma_distribution.py` | 시도 11 |
| `simulations/l11/branching/critical_branching.py` | 시도 12 |
| `simulations/l11/cme_spectrum/rhode_power_spectrum.py` | 시도 13 |
| `simulations/l11/kingman/sqmh_coalescent.py` | 시도 14 |
| `simulations/l11/void_bias/rhode_void_bias.py` | 시도 15 |
| `simulations/l11/rg_fixed_point/sigma_ir_fixed.py` | 시도 16 |
| `simulations/l11/entropy_prod/wwa_entropy.py` | 시도 17 |
| `simulations/l11/turing/sqmh_turing.py` | 시도 18 |
| `simulations/l11/lyapunov/sqmh_stability.py` | 시도 19 |
| `simulations/l11/large_deviation/rhode_fluctuation.py` | 시도 20 |
| `simulations/l11/integration/l11_comparison.py` | 통합 비교 |
| `base.l11.result.md` | L11 최종 결과 |
| `base.l11.todo.md` | WBS 체크리스트 |

---

## L10 → L11 핵심 변화

| 항목 | L10 | L11 |
|------|-----|-----|
| 접근 방향 | SQMH에서 UV/미시 기원 탐색 | 볼츠만 동형성에서 경험식 역수입 |
| 탐색 채널 수 | 7개 | 20개 |
| 목표 | 이론 완결성 | 관측 가능한 경험식 파생 |
| A12 연결 | 불가 확정 (NF-14) | MM 전이 곡선으로 새 경로 시도 (시도 1) |
| 새 관측 채널 | DR3, CMB-S4+Euclid | void 편향, H(z) 산포, ρ_DE 스펙트럼 |

---

*작성: 2026-04-11. L10 10라운드 완료 기준. 실행 보류. 총 20개 시도.*
