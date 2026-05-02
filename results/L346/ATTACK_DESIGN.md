# L346 ATTACK DESIGN — 비단조성 σ_0(z) 의 theory-prior 강도 진단

## 상위 컨텍스트
- 독립 loop. L341 -0.08 등급에 의존하지 않음 (영향 평가는 본 round 한정).
- 직접 선행: L334 (pillar 4 RG b,c priori 도출 불가, ★★★→★★ 격하).
- 직접 선행: L337 (micro 80% 상한, theory-prior 부분만 인정).
- 본 round 임무: σ_0(z) 의 비단조 (non-monotonic) 형상이 SQT 4 pillar
  (RG saddle, Holographic, Z_2, 그리고 4번째 = a4 emergent metric / scaling pillar)
  로부터 **데이터 보기 전 *예측* 되는가**, 아니면 BAO/BB 데이터에 **사후 fit** 인가.

## 핵심 질문 (L346 axis)
> "SQT 4-pillar 가 σ_0(z) 의 *부호 변화* 와 *극값 위치 z_*≈O(0.5)* 를
> *데이터 가시 전*에 a priori 로 내놓을 수 있는가?"

이 질문은 두 의미에서 critical 하다:
1. **이론 강도 의미**: 비단조성이 prediction 이면 SQT 는 falsifiable + 강한 이론.
2. **저널 의미**: PRL/PRD Letter 진입 조건 = "structural prediction confirmed".
   비단조가 fit 이면 JCAP phenomenology 상한 유지.

## 8인 공격 방향 (방향만 — 수식·파라미터·유도 경로 금지)

### A1 — Pillar 분리 진단
4 pillar 각각이 σ_0(z) 의 *형상* 에 어떤 *질적* 제약을 거는지 분리.
- RG saddle pillar: saddle structure 가 *부호 변화* 를 강제하는가, *단조* 만 허용하는가?
- Holographic pillar: boundary entropy bound 가 σ_0(z) 의 monotonicity 에 어떤 sign 을 주는가?
- Z_2 pillar: discrete 대칭이 σ_0 의 z-반사 구조를 요구하는가?
- 4번째 pillar (a4 / scaling): emergent metric 의 dimensional argument 가
  극값 위치를 예측하는 영역 (혹은 예측 못 하는 영역) 식별.

각 pillar 의 *예측력 등급* 을 H/M/L/0 로 부여 (수식 없이 정성적).

### A2 — Prior vs Posterior 시간선 audit
"이론 발표 시점 / 코드 commit 시점 / 데이터 노출 시점" 의 git timeline 으로
σ_0(z) 비단조 형상이 어느 시점에 처음 등장했는지 직접 추적.
- 비단조 형상이 데이터 fit 결과로 *발견* 되었으면 = posterior.
- 비단조 형상이 4-pillar 도출 직후 *제안* 되었으면 = prior.

git log 가 답한다. 논쟁 금지, 자료가 결정.

### A3 — Counterfactual: pillar 제거 실험
4 pillar 중 1 개씩 제거 시 σ_0(z) 가 단조로 회귀하는지 사고실험.
- 1 pillar 제거 → 단조: 그 pillar 가 비단조 *원인*.
- 모두 제거해도 비단조 잔류: data-driven artifact 시그널.
- 어느 pillar 제거해도 비단조 유지: pillar 들이 *집합적으로 redundant* (= 약한 prior).

### A4 — Bayesian theory-prior strength
"비단조 형상에 대한 prior probability" 를 4-pillar 만으로 계산할 수 있는가.
- 강한 prior (P(non-mono | 4 pillars only) > 0.5): prediction.
- 약한 prior (P ≈ 0.5): agnostic, fit.
- P < 0.3: 비단조는 anti-prediction (이론과 충돌, fit 으로 강제됨).

수치 답 금지 — 등급 H/M/L 만.

### A5 — Pre-registration retrospective
P17 (L338 Tier B) pre-reg 가 σ_0(z) 비단조를 *명시* 했는지 확인.
- 명시 + DR3 unblinding 미완 → 비단조는 falsifiable prediction 후보.
- 명시 안 됨 → 비단조는 post-hoc.

### A6 — Alt 14-cluster drift 와 비교
L5 alt-20 14-cluster canonical drift class 가 SVD n_eff=1 (단일 자유도) 로
축약되었던 경험. 비단조 σ_0(z) 도 *그 1 자유도의 한 표현* 인지 진단.
- 그렇다면 비단조는 새 정보 아님 = 약한 prediction.
- 다른 자유도라면 = 독립 prediction 가치.

### A7 — Falsifier 강도
비단조 형상이 prediction 이라면, *어떤 관측이* 그것을 falsify 하는가?
- DR3 BAO 전체 z-bin 에서 σ_0(z) 단조 관측 → SQT 비단조 prior 위반.
- DR3 비단조 관측 + 극값 위치 일치 → strong confirmation.
- 극값 위치 *불일치* (>2σ) → SQT 비단조 wrong-shape, fit-only.

### A8 — 정직 한국어 한 줄 (사전 가이드)
가능한 결론 형태:
- "비단조는 4-pillar 의 *부분적* prediction (대부분 fit)."
- "비단조는 a posteriori discovery, 이론은 retro-fit."
- "비단조는 a priori prediction, DR3 가 결정."
선택은 A1-A7 결과 종합 후.

## 산출물 구조
- ATTACK_DESIGN.md (본 문서) — 8 axis 정의.
- REVIEW.md — 8 axis 자율 분담 평가 결과 + theory-prior 등급.
- NEXT_STEP.md — DR3 unblinding 전 lock 해야 할 항목, P17 보강 항목.

## 메타 — 등급 영향 추정 (사전)
L346 결과는 다음 셋 중 하나:
- (a) 비단조 prediction 입증 (A1-A4 모두 H) → 등급 +0.02 회복.
- (b) 부분 prediction (혼재) → 등급 변동 없음, JCAP 유지.
- (c) post-hoc fit 확정 → pillar 4 ★★ 추가 격하 위험, 등급 -0.01.

본 round 는 *진단* 만 수행, 등급 변경은 다음 SYNTHESIS round 가 판정.
