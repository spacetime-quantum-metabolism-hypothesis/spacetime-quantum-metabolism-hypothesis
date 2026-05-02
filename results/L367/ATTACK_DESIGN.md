# L367 ATTACK DESIGN — Sec 3 narrative revision (3-regime baseline 복귀)

상위 컨텍스트:
- L322 ΔAICc(2→3) = +0.77 (정보론적으로 2-regime 약 우세)
- L332 권고: "2-regime baseline 채택, 3-regime 은 P11 조건부 reserve"
- L337 Pillar B (Wetterich functional RG): 3-regime fixed point 구조 (IR / saddle / UV)
  가 **이론 측에서 자연 발생**. β-function 의 saddle FP 는 g(rm1) 의 중간 regime
  비단조성과 위상학적으로 매칭.

사용자 통찰 (L367 본 세션 입력):
- ΔAICc=+0.77 은 "데이터가 2-regime 와 3-regime 를 구분하지 못한다" 를 의미하지
  "2-regime 가 진짜다" 를 의미하지 않는다.
- L337 매핑상 RG saddle FP 가 사라지면 Pillar B 의 micro 완성도 (gap_2, gap_6)
  가 동반 후퇴한다. baseline 을 2-regime 로 잠그면 micro 측 narrative 가
  단절된다.
- 따라서 baseline 은 *이론 측 동기 (RG saddle 비단조)* 를 유지하고, 통계 측
  caveat (ΔAICc +0.77) 를 정직하게 명시하는 쪽이 종합적으로 더 정직하고 더
  완성도 높다.

## 8인 독립 공격

### A1 (이론적 우선권 vs 통계적 우선권)
- ΔAICc < 2 영역은 통계학적으로 "구분 불가" 영역. AICc 단독으로 단순 모델
  강제하면 이론 동기를 데이터가 *부정* 한 것으로 오독될 위험.
- 정직한 narrative: "이론은 3-regime, 데이터는 미구분, 둘 다 baseline 호환".

### A2 (Pillar B 정합성)
- L337 gap_2 (a3 Γ_0 ≈ H_0) 와 gap_6 (D3 τ_q) 가 RG IR FP 와 saddle FP 의
  *분리된* 두 스케일에 의존. 2-regime 으로 축약하면 saddle scale 이 IR 에
  흡수되어 gap_2/gap_6 closure 경로가 사라진다.
- 결론: 3-regime 는 단순 fitting flexibility 가 아닌 *구조적 micro 요구*.

### A3 (overfitting 위험 재평가)
- L332 N (반박자) 의 핵심 주장: "3-regime 은 confirmation bias / overfitting".
- 반박: AICc 가 자유도를 이미 패널티화 — +0.77 은 "패널티 후" 차이. 즉
  3-regime 는 데이터 fit 자체로는 ~ +2~3 χ² 개선. 이론 동기 있으면 그 개선이
  noise 가 아닐 가능성 무시 못 함.
- 단, 본문 주장 강도는 절제: "preferred but not statistically required".

### A4 (caveat 명시 의무)
- 본문에 명시할 통계 caveat:
  1. ΔAICc(2→3) = +0.77 (현 데이터 미구분)
  2. 2-regime merge 는 동등 수용 가능한 대체 fit
  3. 3-regime 강제는 P11 NS saturation 등 미래 anchor 에 조건부 (L332 결론
     유지)
- 이 caveat 가 본문에 들어가는 한 narrative 정직성 손상 없음.

### A5 (서술 구조 제안)
- Sec 3 main: 3-regime baseline (RG saddle 동기) 설명 + best-fit 파라미터
- Sec 3.x sensitivity / robustness: 2-regime merge 비교, ΔAICc 표,
  "data does not yet distinguish" 명시
- Sec 3.y (선택): P11 forecast 는 supplementary 또는 NEXT_STEP 으로

### A6 (JCAP 등급 영향)
- L332 권고 (2-regime baseline) 채택 시: JCAP 91-95%, 등급 -0.07 유지
- L367 권고 (3-regime baseline + caveat) 채택 시:
  - 통계 정직성: 동등 (caveat 명시 조건)
  - 이론 정합성: +0.02 ~ +0.05 (Pillar B 와의 단절 회피)
  - JCAP 등급 추정: 91-96% (caveat 충분 시 상향, caveat 부족 시 -2%)

### A7 (재발방지 — confirmation bias 차단 장치)
- 3-regime baseline 채택 시 본문 작성 시 다음 항목 자체 검사:
  1. "3-regime 가 데이터에서 입증되었다" 류 *과장 표현 금지*
  2. "2-regime 는 기각된다" 류 *부정 표현 금지*
  3. ΔAICc 표 본문 포함 (supplementary 격하 금지)
  4. "baseline 선택은 이론 동기" 명시 (data-driven 으로 위장 금지)

### A8 (Kill switch)
- 향후 anchor (P11 등) 가 추가되어 ΔAICc(2→3) > +2 (실질적 2-regime 우세) 로
  이동하면 본문 baseline 즉시 2-regime 로 회귀, L367 narrative reverse.
- 즉 본 권고는 "현 시점 미구분 영역에서의 합리적 선택" 이며 데이터가
  결정하면 즉각 양보.

## 종합 판정

L332 의 "2-regime baseline 권고" 는 *통계 단독* 으로는 옳다. 그러나 SQT/SQMH
는 이론과 데이터의 공동 산물이며, 통계가 미구분 영역에 있을 때는 이론 동기
(Pillar B RG saddle) 가 baseline 결정의 합리적 tiebreaker 다.

**L367 권고**: Sec 3 baseline = **3-regime (RG saddle 동기)**, 통계 caveat
(ΔAICc +0.77, 2-regime 동등 수용) 본문 명시, P11 anchor 는 NEXT_STEP 보존.

L332 reverse 의 범위는 *narrative baseline 선택* 에 한정. L332 의 P11 forecast
순위, EOS systematic 우려, "현 시점 글로벌 입증 불가" 정직 한 줄은 모두 유지.
