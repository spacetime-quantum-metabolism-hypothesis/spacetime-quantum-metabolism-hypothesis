# L345 ATTACK DESIGN — 비단조 vs 단조 σ_0(env) Bayes factor (proper ln Z)

## 상위 컨텍스트
- L345 는 L341 (-0.07 carry-over) 와 **독립**. 본 loop 는 σ_0(env) 환경
  의존성의 **함수형 우열** 을 *proper marginalized evidence* 로 재판정한다.
- 기존 라운드들은 Akaike weight (point-estimate + AICc 패널티) 로 비단조
  형태가 단조 형태보다 *유리해 보이는* 결과를 얻었다.
- 그러나 Akaike weight 는 모델 사전분포 부피를 측정하지 않는다. 본 loop 는
  proper Bayesian model comparison (ln Z) 으로 같은 비교를 다시 수행한다.

## 핵심 질문
Δ ln Z = ln Z(non-monotonic) − ln Z(monotonic) 의 **부호와 크기**.
판정은 Jeffreys scale 로만 한다 (Akaike weight 인용 금지).

## 8인 공격 방향 (방향만 — 수식/파라미터 값 금지)

### A1 (모델 정의 — 함수형만)
- 단조 모델: σ_0 가 환경 변수의 단조 함수 (증가 또는 감소 한 가지).
- 비단조 모델: 단일 극값(또는 변곡)을 갖는 함수형. 두 모델은 동일한 환경
  관측가능량에 대한 의존성을 공유하되 단조성 제약 유무만 차이.
- **Command 는 구체적 함수형/파라미터/극값 위치를 지정하지 않는다.** 8인 팀이
  자율적으로 함수 가족 후보를 도출.

### A2 (사전분포의 진실성)
- Akaike weight 가 비단조에 유리했던 이유 가설: 비단조 함수의 자유도가
  데이터에 좁은 영역에서 fit 을 향상시켰으나, **사전분포 부피 패널티**가
  AICc 패널티보다 더 가혹할 수 있음.
- 따라서 사전분포 선택이 결론을 좌우. 사전분포 선정 원칙을 사전 등록(pre-registration):
  단조/비단조 모두 동일한 환경 변수 범위, 동일한 polynomial/structural 자유도.
- 이론적 사전분포가 없으면 wide weakly-informative 와 tight physical-scale
  두 가지 선택 모두 보고.

### A3 (Evidence 추정 알고리즘)
- nested sampling (dynesty) 우선. 후보군: dynesty static + dynamic 두 모드.
- 보조 검증: thermodynamic integration 또는 harmonic-mean estimator 와의
  교차 비교 (해먼믹은 신뢰도 낮음 — 참고용).
- Δ ln Z 표준오차는 dynesty internal + 멀티시드 5회 재실행 표준편차 둘 다 보고.

### A4 (Jeffreys scale 적용)
| |Δ ln Z| | 해석 |
|--------|------|
| < 1 | inconclusive |
| 1–2.5 | weak |
| 2.5–5 | moderate |
| > 5 | strong |
| > 10 | decisive |
판정은 부호 + 크기 모두. "weak preference for non-monotonic" 같은 표현 허용,
"non-monotonic wins" 단정 표현은 |Δ ln Z|>5 일 때만.

### A5 (Akaike weight 와의 정합성 검증)
- Akaike weight 는 reference 만. ln Z 와 결론이 갈리면 ln Z 를 채택하고
  Akaike 가 사전분포 부피를 무시하기 때문임을 본문에 명시.
- 두 척도 부호가 일치하면 robust, 충돌하면 sensitivity section.

### A6 (위험 — 잠재적 실패 모드)
- 비단조 함수가 single peak 위치 사전분포를 좁게 잡으면 evidence 인위 상승.
  → 사전분포는 환경 변수 전 영역 uniform 으로 강제.
- 데이터의 특정 환경 bin 결손이 비단조 신호를 만들 수 있음. cross-validation
  bin-leave-one-out 보고 필수.
- nested sampling 수렴 실패 시 ln Z 보고 금지. live points 충분/멀티시드 일치 필수.

### A7 (등급/JCAP 영향 — 가설)
- Δ ln Z > +2.5 (non-monotonic 우세): 등급 dial +0.01~+0.02 가능. JCAP +1~+2%.
- |Δ ln Z| < 1 (inconclusive): carry-over. 단 "비단조 선호" 본문 표현 정정 필요.
- Δ ln Z < −2.5 (monotonic 우세): 단조 baseline 으로 환원, 비단조 부분 강등.
  등급 dial -0.01 가능.

### A8 (sequencing)
1. 함수 가족 후보 자유 도출 (방향만 — 단조/비단조 각 1 family).
2. 사전분포 등록 (wide + tight 2조).
3. dynesty evidence 계산 (멀티시드 5회).
4. Akaike weight 결과와 부호 비교.
5. Jeffreys scale 판정 + 등급/JCAP carry-over 갱신 권고.

## 출력 산출물
- ATTACK_DESIGN.md (본 파일).
- NEXT_STEP.md (실행 절차/사전분포 등록서).
- REVIEW.md (4인 자율 분담 — 사전 역할 미지정).

## 종합 판정 (사전)
- 본 loop 의 결정 변수는 단 하나: Δ ln Z 부호와 |Δ ln Z|.
- Akaike weight 결과 인용 금지 — 본 loop 는 proper Bayes factor 가 목적.
- 결과가 inconclusive 면 정직 그대로 보고. carry-over 처리.
