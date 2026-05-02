# L549 — P3a Rule-A 회의적 압박 (8인 단일 세션)

> 작성: 2026-05-02. 단일 세션 multi-perspective skeptical review.
> 대상: results/L541/P3A_DERIVATION.md (P3a, Path-α + GFT BEC → Z₂ SSB → CMB-S4/LiteBIRD B-mode).
> 양식: 좋은 점 생략, 문제점만 집중. 250자 이내/리뷰어.
> CLAUDE.md 정합: 신규 수식 0, 신규 파라미터 0, paper/base.md edit 0.

---

## R1 — Kibble–Zurek 보조 가정의 정당성

§4.1 의 B1 (Kibble–Zurek scaling) 은 SQT axiom A1–A6 외부의 *통계역학 결과*. §4.2 는 "B1 의 자연 결과" 라며 wall network attractor scaling 을 도입했지만, K-Z scaling 은 (i) quench rate τ_Q 의 finite, (ii) critical exponent ν, z 의 universality class 선택, (iii) freeze-out adiabaticity 위반 시점이라는 *3 개의 hidden DOF* 를 함의함. B1 = "1 개 보조 가정" 이라는 §4.3 주장은 사실 ≥3 hidden DOF 의 *압축* — L1 자격 자체가 분식. 진정 보조 가정 수는 ≥3, 등급은 L1 미달.

## R2 — L0 미달의 의미: priori 인가 후보 가설인가

§0 은 "OOM 은 보조 가정 1개로 결정" 이라 했지만, §4.2 마지막은 "수치 prefactor O(1) 은 priori 결정 불가" 라고 자인. 즉 *함수형* 만 priori 이고 *값* 은 priori 아님. 이는 논문 표준 priori (예: Standard Model gauge coupling 의 GUT 통일 예측) 와 다름 — 함수형 priori 는 *모든* 자연스러운 dimensional analysis 가 만족시키는 약한 조건. P3a 는 priori 라기보다 "**dimensional 합치 후보**" — L1 자격 부여 자체가 over-grading. 적정 등급은 PASS_QUALITATIVE.

## R3 — CMB-S4 falsifier 단방향성

§5 는 LiteBIRD/CMB-S4 가 BB bispectrum 검출 시 PASS 라고 시사. 그러나 (i) cosmic string, (ii) primordial GW non-Gaussianity, (iii) inflationary feature, (iv) reionization patchy screening 모두 동일 BB 비-가우시안 신호 생성. 검출 → P3a confirm 이 아니라 "≥4 개 후보 중 1 개" — falsifier 로서 *비대칭*. Null 시 KILL 은 정당하나, 검출 시 confirm 은 baseless. K10 sign-consistency 통과만으로 falsifier 자격 미달.

## R4 — Path-α 자체의 hidden DOF

A3' Γ₀(t) 는 axiom 3 의 "균일 생성률 상수 Γ₀" 를 *시간 함수* 로 격상. 이는 paper §6.5(e) hidden DOF count 에 +1 (Γ₀ 의 시간 의존성 함수형 자유도) 추가. L495 의 9~13 DOF 에 +1 → 10~14 DOF. L502 AICc penalty Δχ²_penalty = 2k 재계산 시 P3a 자체가 PASS_MODERATE 강등 가능. §1 axiom 목록은 A3' 격상의 DOF cost 를 미계상.

## R5 — Postdiction risk: Kibble–Zurek 의 cherry-pick

P3a 결과를 알고서 보조 가정으로 K-Z 를 *선택* 한 의혹. 동일 oom 도출 가능 후보: (i) Coleman-Weinberg radiative SSB, (ii) thermal phase transition with critical bubble, (iii) Vilenkin scaling regime (cosmic string analog). 셋 모두 wall density attractor 결과 상이. §4.1 이 K-Z 만 "유일한" 보조 가정으로 명명한 것은 ex-post 정당화. 진정 priori 라면 *3 후보 모두 동일 OOM 도출* 을 보여야 함. 미수행 → cherry-pick 위험.

## R6 — GFT BEC pillar 의 evidence base 약함

§1 A5 는 L530 §E "GFT BEC" 를 axiom 으로 도입. 그러나 GFT BEC 는 4-pillar 중 가장 weak — Schwinger-Keldysh / Wetterich RG 와 달리 *수학적 well-posedness* 미확립 (Oriti et al. 2016 의 mean-field 근사 한정). condensate phase φ_c 의 *complex order parameter* 자격 자체가 axiom 이 아닌 *모델 선택*. §2.1 의 "A4 ∧ A5 ⇒ Z₂ SSB 필연" 은 A5 의 model-dependent 부분에 의존. axiom 자격 ✗.

## R7 — N_eff falsifier 와 채널 중복

L498 N_eff=4.44 의 6 채널 중 F3 (CMB-S4 N_eff measurement) 은 P3a 의 CMB-S4 BB 채널과 동일 *instrument* 사용. 두 falsifier 가 instrument-systematics correlated. (i) CMB-S4 foreground subtraction, (ii) lensing reconstruction, (iii) beam systematics — 모두 N_eff TT/EE 와 BB bispectrum 양쪽에 영향. 독립 채널 가산으로 P3a 와 F3 를 *둘 다* 카운트하면 statistical independence 위반. 채널 수 inflation 위험.

## R8 — Hidden DOF 재계산 결과

집계: L495 base 9~13 + R4 (Γ₀(t) 시간의존) +1 + R1 (K-Z hidden 3) +3 + R6 (GFT BEC model selection) +1 = **14~18 DOF**. L502 AICc penalty 2k = 28~36. P3a 가 BB bispectrum *수σ* 검출로 Δχ² ~ 9 (3σ) 개선해도 ΔAICc = 9 − 28~36 = −19~−27 (worse). PASS_MODERATE 도 미달, **DEMOTE → CANDIDATE** 가 정직 등급. §4.3 의 L1 등급은 DOF cost 미계상 결과.

---

## 최종판정

**판정: priori 자격 박탈 → CANDIDATE / PASS_QUALITATIVE 강등**

사유 (집계):
1. R1 + R8 — K-Z "1 보조 가정" 은 hidden ≥3 DOF 압축. AICc penalty 재적용 시 P3a 자체가 net negative gain.
2. R2 — *함수형 priori* 만 결정, 수치 prefactor priori 불가. 이는 dimensional 합치 후보 수준 (PASS_QUALITATIVE) 이지 L1 structural priori 미달.
3. R3 — falsifier 단방향성 (검출 → ≥4 후보 중 1, confirm 자격 없음).
4. R5 — K-Z cherry-pick 위험 (Coleman-Weinberg / thermal / Vilenkin 동등 후보 미검증).
5. R6 — A5 GFT BEC 의 axiom 자격 약함 (model selection 의존).

권고:
- L536 §3 의 ★ 등급 (P3a) 회수, **CANDIDATE** 로 격하.
- L1 priori 주장은 (i) K-Z DOF 명시 +3, (ii) 대체 보조 가정 3 후보 동등 OOM 검증, (iii) F3 와 instrument-correlation 분리, 셋 모두 통과 후 재평가.
- *현재 세션에서 처음으로 L1 priori 라고 주장된 후보* 라는 사실 자체가 cherry-pick 압박 신호 — over-grading 의심을 우선 유지.

CLAUDE.md 정합: 결과 왜곡 금지 — L1 priori 가 깨졌음을 정직 disclosure. 신규 수식 0, 파라미터 0, paper/base.md edit 0.
