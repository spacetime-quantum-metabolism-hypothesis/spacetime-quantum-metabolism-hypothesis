# L426 ATTACK_DESIGN — 8인팀 reviewer 공격 설계

**주제**: SQT depletion-zone formalism 이 halo concentration-mass relation c(M) 에 어떻게 수정 가능한지.
**목표**: c(M) 가 LCDM (Diemer-Joyce 2019, Ludlow 2016 등) 과 정량 차이를 만들 수 있는 reviewer 공격 채널 정리.
**제약** (CLAUDE.md 최우선-1): 구체적 수식/파라미터 값 사전 지시 금지. 비판 채널 이름/방향만.
**방법**: 8인 자율 토의 (Rule-A). 역할 사전 지정 없음.

---

## 8인팀 자율 발생 비판 채널

### 비판 #1 — depletion 은 large-scale gradient, halo interior 에 영향 없음
SQT depletion-zone 은 isolated halo 외곽의 *공간 흡수* 효과를 모형화한다.
NFW concentration c = r_vir/r_s 는 *halo 내부* density profile 에서 정의되며,
N-body LCDM 의 c(M) 는 turnaround/collapse 시점의 σ(M) 통계와 spherical collapse δ_c 에서 결정.
depletion-zone 은 spherical collapse threshold δ_c 또는 σ(M) 둘 중 어느 것에도 *직접* 진입하지 않음.
→ "c(M) 는 LCDM 에서 변하지 않는다" 가 null prediction.

### 비판 #2 — peak height ν(M) 채널 결여
Diemer-Joyce 2019 등 mainstream c(M) 모델은 c = c(ν) (ν = δ_c/σ(M,z)) 로 환원.
SQT depletion 은 σ(M) (linear power spectrum 분산) 을 수정하지 않으므로 ν 도 변하지 않음.
σ(M) 수정을 주장하려면 입력 P(k) 자체를 수정해야 하나, SQT 는 background level 모델이며
power spectrum modification 이 별도 파생되지 않음 (paper §4 limitation).

### 비판 #3 — 만약 c(M) 가 변한다면 lensing/X-ray 불일치
Cluster c(M) 관측 (Umetsu+, Sereno+, CLASH/LoCuSS) 은 LCDM 예측과 0.1 dex 수준 일치.
SQT 가 c(M) 를 0.05 dex 이상 이동시키면 *기존 관측에 모순* — 즉 SQT 는
"LCDM 와 구분 불능" 또는 "관측 모순" 두 갈림길.

### 비판 #4 — DM 입자성 가정 vs depletion
LCDM c(M) 는 *cold collisionless particle* 가정에서 옴. SQT depletion 은
"입자성 DM 없음, 공간 자체가 흡수원" 이지만 외관은 입자 DM 처럼 작동.
시뮬레이션 부재 (SQT-체 N-body 없음) 로 c(M) 정량 예측 불가능.
어떤 c(M) 곡선을 예측한다 하더라도 *post-hoc fit* 위험.

### 비판 #5 — Mass-dependent depletion scale 부재
NFW r_s scale 은 halo formation epoch z_form(M) 와 짝지어져 c(M) 의 mass dependence 를 만듦.
SQT depletion-zone 의 specific scale (r_dep(M)) 정의가 paper §5 에 부재.
mass dependence 를 만들려면 추가 axiom 필요 → axiom 경제성 페널티.

### 비판 #6 — Redshift evolution c(M, z)
Ludlow 2016: c(M,z) ∝ (1+z)^(-α), α≈0.5 (LCDM N-body). SQT 가 redshift evolution 을
다르게 예측할 path 가 없음. depletion-zone 은 background-level 이며 dark energy 채널과 분리.
→ c(M,z) 예측은 trivially LCDM-equivalent.

### 비판 #7 — 다른 modified gravity 대비 차별점 부재
f(R), DGP, screening 모델은 c(M) 에 명시적 수정 (e.g. Mitchell+ 2019: chameleon 에서 c 5–10% 증가).
SQT 가 이런 정량 prediction 을 만들지 못하면 "modified gravity" 카테고리에서 *least specific*.
reviewer: "왜 SQT 를 chameleon/symmetron/Galileon 대신 채택해야 하는가?"

### 비판 #8 — Falsifiability 제로
c(M) 채널에서 SQT 의 prediction 이 LCDM 와 동일하다면 c(M) 관측은
SQT 를 *falsify 도 verify 도 못함*. PASS_TRIVIAL 등급의 전형 — paper §6 에 추가 caveat 필요.

---

## 8인팀 합의 결론

- SQT depletion-zone 은 halo *외곽* (1–3 r_vir) splashback / turnaround 영역에 잠재적 영향 가능.
- 그러나 c(M) (interior density profile) 채널은 SQT axiom 만으로 LCDM 와 *구분 불능*.
- 정량 c(M) 예측을 만들려면 추가 axiom (mass-dependent depletion scale, modified σ(M)) 필요.
- 등급 사전 권고: PASS_TRIVIAL (LCDM-equivalent) 또는 NULL (예측 부재).
