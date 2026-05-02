# L345 REVIEW — 4인 자율 분담 사전 검토 (실행 전)

## 검토 범위
- ATTACK_DESIGN.md 의 8인 공격 방향 (A1-A8) 정합성.
- NEXT_STEP.md 의 evidence 계산 절차의 통계적 무결성.
- L341 carry-over (-0.07) 및 본 loop 의 등급 영향 추정 정합성.

## 4인 자율 분담 (사전 역할 미지정 — 토의 자연 발생)

### 검토자 R1: 통계 방법론 무결성
- ln Z 와 Akaike weight 는 정보론적/통계적 의미가 다르다. ln Z 는 사전분포
  부피를 자연스럽게 패널티화하고, AICc 는 점추정+자유도 패널티만 적용.
- ATTACK A2/A4 에서 ln Z 를 일차 척도, Akaike 를 보조로 둔 것은 정합.
- 다만 비단조 family 의 사전분포가 단조보다 *구조적으로* 큰 도메인을 가질 경우
  Δ ln Z 가 단조 쪽으로 편향된다 (Lindley paradox 류). NEXT_STEP §2 에서
  진폭 prior 동일, 극값 위치 prior uniform 으로 강제한 것은 적절. PASS.
- 권고: "비단조 우세" 결론은 **두 prior set 모두에서** Jeffreys moderate 이상
  일 때만 인정. ATTACK A8 + NEXT_STEP §5 에 이미 반영. PASS.

### 검토자 R2: 시뮬레이션 안정성
- dynesty 3.0.0: `rstate = np.random.default_rng(seed)` 규칙은 CLAUDE.md 에 기재됨.
  NEXT_STEP §3 멀티시드 5개와 정합. PASS.
- emcee 와 달리 dynesty 는 stretch move 의존이 없으므로 `np.random.seed`
  추가는 불필요. 다만 fitness function 내부에서 numpy 전역 RNG 호출이 있을
  경우 해당 부분 시드 고정 필요 — 코드 작성 시 검사 항목.
- `dlogz < 0.1` + 멀티시드 σ(ln Z) < 0.5 의 이중 수렴 기준은 적정. PASS.
- 워커 thread pin (OMP=1) 과 spawn pool 강제는 CLAUDE.md 와 일치. PASS.

### 검토자 R3: 사전분포 등록의 정직성
- 사전 등록(pre-registration) 강제 + 사후 변경 금지 명시 (NEXT_STEP §0).
  L5 재발방지의 "Akaike weight 0.48 = no preference" 교훈과 정합. PASS.
- 두 prior set (wide A + tight B) 동시 보고는 sensitivity 노출 측면 정직.
  Set B 의 "tight physical-scale" 근거가 자의적이면 결과 편향 위험 → R3 가
  실행 단계에서 Set B 의 등록 근거를 별도 문서화하도록 요청. ACCEPT WITH FLAG.
- 비단조의 극값 위치 prior 를 환경 변수 도메인 전체에 uniform 으로 강제한
  것은 핵심 안전장치. 이 조항이 지켜지지 않으면 결과 무효 — 검증 시 코드
  레벨에서 prior bound 출력 + 어서션 권고.

### 검토자 R4: 등급/JCAP 영향 정합성
- ATTACK A7 의 등급 dial 수치 (+0.01~+0.02 / 0 / -0.01) 는 *가설*. 결과 후
  실제 dial 변경은 8인 팀 carry-over 합의 후. R4 동의.
- L341 carry-over -0.07 와 본 loop 가 *이론 등급*을 직접 건드리지 않음을
  명시 (본 loop 는 phenomenological 함수형 비교). 따라서 dial 변동이 발생해도
  L341 베이스라인에서 ±0.02 이내. PASS.
- JCAP 영향 ±1~2% 는 reviewer 가 비단조 선호의 prior 부피를 문제 삼을 위험
  반영. 정직 disclosure 시 +0~+1% 회복. 합리적 추정.

## 합의 결론
1. ATTACK_DESIGN A1-A8 은 proper Bayes factor 비교 원칙에 부합. 통과.
2. NEXT_STEP §0-§9 는 사전 등록 + 멀티시드 수렴 + 두 prior set 보고로
   사전분포-편향과 시뮬레이션-편향 모두 제어. 통과.
3. **본 REVIEW 는 사전(pre-execution) 검토** — 실제 evidence 결과는 본 loop
   에 *아직 산출되지 않았다*. Δ ln Z 수치는 별도 후속 작업에서 계산.
4. 사전 단계에서 결과 부호/크기를 추정/암시하는 진술은 금지 (최우선-1, -2).

## 위반 점검
- 최우선-1 (지도 금지): 본 ATTACK/NEXT_STEP/REVIEW 에 수식, 파라미터 값,
  특정 함수형 명시 없음. PASS.
- 최우선-2 (팀 독립 도출): 함수 가족 후보를 8인 팀 자율 도출로 위임. PASS.
- 결과 왜곡 금지: 본 loop 에 evidence 결과 미산출. 결과 fabrication 없음. PASS.
- 코드리뷰 자율 분담: R1-R4 사전 역할 미지정. PASS.

## 정직 보고
- 본 L345 산출물은 *설계 + 사전 검토* 에 한함. proper ln Z 수치는 본 세션에
  포함되지 않음. "비단조 우세" 또는 "단조 우세" 결론을 본 loop 단계에서
  단정 금지. carry-over -0.07 유지.

## 한 줄 (정직 한국어)
**Δ ln Z 는 아직 계산되지 않았다 — 본 loop 는 정직한 사전 등록과 절차만 확정했다.**
