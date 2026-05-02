# SQMH Glossary / 용어집

영문/한국어 병기. 본 용어집은 SQMH (Spacetime Quantum Metabolism Hypothesis) 논문 및
부속 문서 (results/, simulations/, paper/) 전반에서 사용되는 핵심 용어를 통일한다.

---

## A. Theory-level terms / 이론 용어

### SQMH (Spacetime Quantum Metabolism Hypothesis)
- **EN**: Working hypothesis that spacetime is a metabolic medium of finite quanta
  (creation rate σ₀, annihilation rate Γ₀) and that observed dark-sector phenomenology
  is the macroscopic shadow of this metabolism.
- **KO**: 시공간을 유한한 양자(생성률 σ₀, 소멸률 Γ₀)들의 신진대사 매질로 가정하는
  작업 가설. 관측된 암흑부문 현상은 이 신진대사의 거시적 그림자라는 입장.

### SQT (SQMH Tail / Saturation-Quantum Tail)
- **EN**: The high-z saturation tail of the SQMH ψ-field, parametrised by the
  ratio r = ψ₀/ψ(z) and a global amplitude. The "L33 SQT" form combines a
  low-z tanh ramp with a high-z linear ratio term, weighted by a sigmoid.
- **KO**: SQMH ψ-필드의 고적색편이 포화 꼬리. r = ψ₀/ψ(z) 비율과 전역 진폭으로
  매개변수화. L33의 SQT 형태는 저z tanh + 고z 선형 ratio 항을 sigmoid로 혼합.

### Three-regime structure (formerly "Branch B")
- **EN**: The post-L100 partition of SQMH phenomenology into three regimes
  (low-z thawing, intermediate transition, high-z saturation). Replaces the
  earlier "Branch A / Branch B" dichotomy. The label "Branch B" is deprecated;
  use "three-regime" in all new documents.
- **KO**: L100 이후 SQMH 현상학을 세 영역(저z thawing, 중간 전이, 고z 포화)으로
  분할하는 구조. 이전의 "Branch A/B" 이분법을 대체. "Branch B" 표기는 폐기되었으며
  신규 문서에서는 반드시 "three-regime"을 사용한다.

### Postdiction
- **EN**: A model output that reproduces *already-published* data
  (DESI DR2, Pantheon+, Planck 2018) within stated tolerances. Distinct from
  prediction: postdictions do not by themselves constitute a successful test.
- **KO**: 이미 공개된 데이터(DESI DR2, Pantheon+, Planck 2018)를 명시된 허용오차
  내에서 재현하는 모형 결과. 예측(prediction)과 구분되며, postdiction 자체로는
  성공적 검증이 아니다.

### Prediction (a priori)
- **EN**: A model output specifying a measurable quantity *before* the
  corresponding data are released (e.g. DESI DR3 D_M/r_d at z=0.93).
  Only a priori predictions count toward falsification milestones.
- **KO**: 해당 데이터가 공개되기 *이전*에 측정 가능량을 명시하는 모형 결과.
  반증 마일스톤(falsification milestone)에는 a priori 예측만 인정된다.

---

## B. Status / verdict labels / 상태·판정 라벨

### OBS-FAIL (Observational failure)
- **EN**: Candidate model is rejected because its prediction conflicts with
  current observational data at the agreed threshold (Δχ² > kill threshold,
  or boundary-violating w_a, S_8, γ-1, etc.).
- **KO**: 후보 모형이 현 관측 데이터와 합의된 임계치를 넘어서는 충돌을 일으켜
  기각된 상태(Δχ² > kill threshold, 또는 w_a/S_8/γ-1 경계 위반 등).

### FRAMEWORK-FAIL
- **EN**: Candidate model is rejected because of *structural* incompatibility
  with SQMH axioms (sign of energy flow, baryon-Einstein-frame separation,
  positivity of n₀μ, etc.) regardless of fit quality.
- **KO**: 적합도와 무관하게 SQMH 공리(에너지 흐름 부호, 바리온 Einstein-frame
  분리, n₀μ 양수성 등)와 *구조적*으로 양립 불가능하여 기각된 상태.

### CONSISTENCY_CHECK
- **EN**: Verification step that re-derives a quantity through an independent
  channel (e.g. background ODE vs. analytic CPL fit, BAO-only vs. joint).
  A mismatch above tolerance flips the candidate to OBS-FAIL or
  FRAMEWORK-FAIL.
- **KO**: 독립 경로로 동일 양을 재유도하는 검증 단계(예: 배경 ODE vs CPL fit,
  BAO-only vs joint). 허용오차를 넘는 불일치 시 OBS-FAIL/FRAMEWORK-FAIL로
  판정이 전환된다.

### PASS_IDENTITY
- **EN**: Successful CONSISTENCY_CHECK at a specific milestone (Lxx). Tagged
  with the milestone label (e.g. PASS_IDENTITY@L46) and the channel checked
  (BAO13, SN, CMB-θ*, RSD, WL).
- **KO**: 특정 마일스톤(Lxx)에서 CONSISTENCY_CHECK를 통과한 상태. 마일스톤 라벨과
  검증 채널(BAO13, SN, CMB-θ*, RSD, WL)을 함께 표기한다(예: PASS_IDENTITY@L46).

### KILL / KILLED
- **EN**: Final, terminal verdict. A KILLed candidate is moved to negative-
  result registry and not revisited unless the underlying data or threshold
  changes.
- **KO**: 최종 종결 판정. KILL된 후보는 negative-result 레지스트리로 이관되며,
  근거 데이터나 임계치가 바뀌지 않는 한 재탐색하지 않는다.

### PROVISIONAL
- **EN**: Status assigned when a check used a degraded channel (e.g.
  compressed CMB instead of full Boltzmann, toy ODE instead of hi_class).
  Promotion to PASS_IDENTITY requires the full-channel re-run.
- **KO**: 축약 채널(예: compressed CMB, toy ODE)로 검증된 상태. 전체 채널
  재실행 후에야 PASS_IDENTITY로 승격 가능.

---

## C. Mid-level methodology / 방법론 용어

### Joint analysis
- **EN**: Combined likelihood over BAO + SN + CMB(θ*) + RSD (and optionally
  WL/S_8). "BAO-only" results are not joint conclusions.
- **KO**: BAO + SN + CMB(θ*) + RSD (선택적으로 WL/S_8) 결합 likelihood.
  "BAO-only" 결과를 joint 결론과 동일시하지 말 것.

### AICc penalty
- **EN**: Small-sample-corrected information criterion. Required whenever a
  candidate adds free parameters; if Δχ² gain < AICc penalty, the simpler
  model wins.
- **KO**: 소표본 보정 정보 기준. 자유 파라미터 추가 시 반드시 적용. Δχ² 개선이
  AICc 패널티보다 작으면 단순 모형 채택.

### Occam-corrected evidence (Δ ln Z)
- **EN**: Fully marginalised Bayesian evidence difference. Distinct from
  fixed-θ Δ ln Z (which evaluates at MAP). Reports must specify which.
- **KO**: 완전 marginalisation된 Bayesian 증거 차이. fixed-θ Δ ln Z(MAP 평가)와
  구분. 보고 시 어느 쪽인지 명시 필수.

### Dark-only embedding
- **EN**: SQMH coupling restricted to the dark sector (DM + DE), with baryons
  kept in the Einstein frame. Required to evade Cassini |γ-1| < 2.3×10⁻⁵.
- **KO**: SQMH 결합을 암흑부문(DM + DE)에 한정하고 바리온은 Einstein frame에
  분리. Cassini |γ-1| < 2.3×10⁻⁵을 피하기 위한 필수 구조.

### Disformal coupling
- **EN**: Metric redefinition g̃ = A·g + B·∂φ∂φ. Pure disformal (A'=0) gives
  static γ=1 exactly (Zumalacárregui-Koivisto-Bellini 2013).
- **KO**: 계량 재정의 g̃ = A·g + B·∂φ∂φ. 순수 disformal(A'=0)은 정적 γ=1을
  정확히 부여(ZKB 2013).

### Compressed CMB (θ*)
- **EN**: Hu-Sugiyama fit to the acoustic scale, used as a CMB shortcut when
  full Boltzmann (CLASS/hi_class) is unavailable. Theory floor 0.3% must be
  added to the σ.
- **KO**: 음향 스케일에 대한 Hu-Sugiyama fit. 전체 Boltzmann이 없을 때 사용하는
  CMB 축약. σ에 이론 하한 0.3%를 반드시 추가.

---

## D. Workflow tags / 작업 흐름 태그

### Lxx (milestone)
- **EN**: Sequential SQMH session label (L1, L2, ..., L446). Each milestone
  has its own results/Lxx/ directory and decisions are referenced as
  "L46-G3", "L100-T7" etc. (G = general check, T = team discussion).
- **KO**: SQMH 세션 순차 라벨(L1, L2, ..., L446). 각 마일스톤은 results/Lxx/를
  보유하며, 결정은 "L46-G3", "L100-T7" 형식으로 인용(G=일반 검토, T=팀 토의).

### Rule-A / Rule-B review
- **EN**: Rule-A = 8-person sequential theory review (claims, axioms,
  positioning). Rule-B = 4-person code review (scripts, growth, CLASS).
- **KO**: Rule-A = 8인 순차 이론 리뷰(주장·공리·포지셔닝). Rule-B = 4인 코드 리뷰
  (스크립트·성장·CLASS).

### Negative-result registry
- **EN**: paper/negative_result.md and per-Lxx negative_results.md. All
  KILLed candidates must be appended honestly with the kill reason.
- **KO**: paper/negative_result.md 및 각 Lxx의 negative_results.md. 모든 KILL
  후보는 사유와 함께 정직하게 기록해야 한다.

---
