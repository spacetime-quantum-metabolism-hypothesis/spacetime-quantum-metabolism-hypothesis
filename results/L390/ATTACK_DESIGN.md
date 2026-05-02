# L390 ATTACK DESIGN — Conformal Anomaly Trace T^μ_μ (n field contribution)

## 1. 주제 및 배경

SQMH 의 metabolic scalar 장 n(x) (단위 부피당 spacetime metabolic 단위 수)
는 양자장으로 quantize 될 때 conformal symmetry breaking 에서 anomalous trace
를 발생시킬 가능성이 있다. 본 연구는 n 장에서 유래하는 conformal anomaly
T^μ_μ 의 numerical 평가와 Λ_eff (관측 vacuum energy) 에 미치는 영향을
정직하게 정량한다.

## 2. 탐색 방향 (지도 금지 원칙 준수)

### 2.1 물리 현상의 이름만 제공
- Conformal anomaly (trace anomaly) — Capper-Duff 1974, Duff 1977/1994 review
- Heat-kernel coefficient a_2 (Seeley-DeWitt 전개)
- Curvature invariant set: {R^2, R_μν R^μν, R_μνρσ R^μνρσ, □R}
- Renormalization scheme dependence (μ scale)
- Effective action Γ_eff 와 vacuum stress-tensor ⟨T_μν⟩

### 2.2 수학 분야의 이름만 제공
- Curved-space QFT (Birrell-Davies)
- Zeta-function regularization
- Dimensional regularization in d=4-2ε

### 2.3 절대 금지
- 구체적 anomaly coefficient 수치 (a, b, c, c' 값)
- ⟨T^μ_μ⟩ 의 명시적 form 제시
- Λ_eff 와 anomaly 의 연결 공식 사전 제공
- L46/L48/L100+ 등 과거 SQT/SQMH 결과의 amplitude 재사용

## 3. 팀 구성 (역할 사전 지정 금지)

- **이론 도출 8인**: 자유 분담. anomaly 유도, n 장 spin/coupling 가정,
  curvature 배경 (FLRW vs static), regularization 선택 모두 팀이 자율 결정.
- **수치 검증 4인**: 8인이 산출한 표현식만 받아 별도 분담. 데이터 fit /
  단위 변환 / scheme dependence 체크 / 코드 cross-check.
- 두 팀 모두 사전 역할 배정 없음. 토의에서 자연 발생 분업만 인정.

## 4. 산출 요구사항 (수식 금지, 결과만 명시)

K-test (Kill criteria):

- **K1 차원 일관성**: ⟨T^μ_μ⟩ 의 SI 차원이 [energy density] 인지 토이로 검증.
  실패 시 즉시 reject.
- **K2 scheme 독립성**: 두 가지 이상 regularization (zeta vs dim-reg) 으로
  같은 leading curvature term 을 얻는지 비교. 차이가 O(1) 이상이면 toy
  artifact 로 판정.
- **K3 FLRW 평가**: 현재 우주 H_0, R(today) 에서 수치값 산출.
  단위: J/m^3.
- **K4 Λ_eff 비교**: ρ_Λ,obs ≈ 5.4e-10 J/m^3 와 비율. 1/N (N≥10^120)
  이면 negligible, O(1) 이면 fine-tuning 문제 재발.
- **K5 SQMH 정합**: anomaly 부호와 n 장 metabolic 소멸 항 (psi^n 류) 의
  부호 정합성 — 단, **사전 부호 지정 금지**. 팀이 독립 도출.

## 5. 정직성 약속

- 결과가 base.md 와 다르면 base.fix.md 에 기록.
- ⟨T^μ_μ⟩ ≪ ρ_Λ 로 나오면 "n 장 anomaly 는 dark energy 채널 무관" 으로
  정직 보고. 강제 amplitude 부풀림 금지.
- ⟨T^μ_μ⟩ ~ ρ_Λ 로 나오면 fine-tuning / cancellation 조건 명시.
- 수치 한 자리 단위라도 부정확하면 즉시 base.fix.md.

## 6. 실행 순서

1. 8인 팀 자유 토의 → trace anomaly 표현식 도출 (수식은 결과 파일에만).
2. 4인 코드리뷰 팀이 toy 작성 → K1–K4 통과 여부.
3. SQMH 정합성 K5 판정.
4. REVIEW.md 에 통과/탈락 + 정직 한 줄.

## 7. 환경

- Python 3, numpy 2.x (`np.trapezoid` 사용).
- 병렬 필요 시 `multiprocessing.get_context('spawn').Pool(≤9)`,
  `OMP/MKL/OPENBLAS_NUM_THREADS=1`.
- 유니코드 print 금지 (cp949). matplotlib 라벨만 OK.
