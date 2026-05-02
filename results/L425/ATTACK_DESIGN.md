# L425 ATTACK DESIGN — NS saturation σ_0 prediction (P11 anchor 후보)

상위 컨텍스트:
- L332/L367: P11 (NS M_max / saturation) 는 3-regime baseline 의 조건부 anchor.
  EOS systematic 우려가 핵심 caveat.
- 본 세션 임무: SQT 가 예측하는 NS saturation σ_0 가 EOS-dependent 인가, 아니면
  structural (EOS marginalization 후에도 살아남는가) 인가를 8인 독립 공격으로
  판정.

## 8인 독립 공격 (역할 사전 지정 없음, 자유 접근)

### A1 — EOS family span 의 정의 문제
- "EOS-independent" 주장은 marginalization domain 에 결정적으로 의존.
  APR, SLy4, BSk21/22, DD2, MPA1 등 chiral-EFT 호환 family 만 묶을지,
  아니면 hybrid quark / hyperonic / phase-transition EOS 까지 포함할지에 따라
  σ_0 산포가 한 자릿수 변할 수 있다.
- 공격: SQT 의 saturation prediction 이 *어느 EOS class* 에서 "structural" 인지
  명시하지 않으면 P11 anchor 의 ΔlnZ 기여가 prior 선택의 함수로 변동.
- 대응 요구: EOS class 를 *물리 도메인* (pure baryonic chiral-EFT) 으로
  pre-specify 하고 본문에 명시. 다른 class 는 별도 supplementary.

### A2 — high-ψ 곡률 ↔ NS 중심밀도 매핑의 비선형성
- g(rm1) high-ψ regime 곡률은 ψ_NS_core 영역에서 평가. ψ_NS_core 는 EOS 에 따라
  factor ~2 변동 (중심밀도 ρ_c 가 EOS 별 ~0.6 - 1.2 fm^-3).
- 공격: 곡률 자체는 SQT structural 이라도 *evaluation point* 가 EOS-shift 하므로
  실효 σ_0 는 EOS 의 함수. "structural" 주장은 evaluation prescription 까지
  포함해야 정직하다.
- 대응 요구: σ_0 forecast 는 ρ_c 분포에 대한 marginalized posterior 로 보고.
  point estimate 는 misleading.

### A3 — NICER mass-radius constraint 의 정보량 부족
- NICER PSR J0740+6620 R = 12.39 +0.30/-0.98 km, J0030+0451 R = 12.71 +1.14/-1.19
  km. δR/R ~ 8 % 수준. M-R curve 1점만 묶고, dM/dR slope 는 사실상 측정 못함.
- 공격: SQT 가 영향을 주는 양이 dM_max/dρ_c (saturation slope) 인데, NICER 단독
  으로는 slope 정보가 약하다. anchor 로 쓰면 ΔlnZ 가 EOS prior 폭에 흡수.
- 대응 요구: NICER 단독 anchor 는 ΔlnZ +0.5 이하로 가정. 실질 anchor 는 NICER
  + GW170817 + universal relations 조합 시에만 의미.

### A4 — GW170817 tidal deformability Λ̃ 의 SQT 결합 채널
- LIGO/Virgo Λ̃ < 720 (low-spin prior, 90% UL) 는 EOS softness 제약. SQT 의
  "saturation" 이 이 Λ̃ 에 직접 들어가는 채널은 *간접* — high-ψ regime 곡률이
  EOS pressure 에 보정만큼만 작용.
- 공격: SQT-only correction 이 Λ̃ 변화량 < 5 % 정도면 GW170817 으로는 detect
  불가. anchor 로서 정보 ~ 0.
- 대응 요구: SQT correction 의 Λ̃ sensitivity 를 실제로 forecast. 5 % 미만이면
  P11 = "GW170817 무관" 으로 정직 표기.

### A5 — universal relations (I-Love-Q) 가 SQT 변형을 흡수
- Yagi-Yunes I-Love-Q 관계는 EOS 무관 정확도 ~1 %. SQT 가 NS 내부 압력 구조를
  변형하면 이 관계도 함께 shift 하나, 동일하게 "거의 EOS-free" 로 shift 하면
  *관측적으로 무차별*.
- 공격: SQT-induced shift 가 universal relations 안에 들어가 버리면 anchor 로
  쓸 수 있는 잔차가 작다.
- 대응 요구: SQT correction 이 universal relation residual 에 만드는 변화량을
  Δ(I/M³) 또는 Δ(C ≡ M/R) 로 표현해 forecast. 표준 EOS variance < SQT shift
  여야 anchor 자격.

### A6 — anchor pool 추가 ΔlnZ 의 prior 의존성
- ΔlnZ 는 (1) 관측 σ_0 의 분포 폭, (2) SQT prior on σ_0, (3) baseline (LCDM
  또는 2-regime SQT) 의 자유도 차이에 의존. 어느 하나라도 ad hoc 이면 ΔlnZ
  숫자가 의미 잃음.
- 공격: P11 ΔlnZ +N 주장 시 prior 가 SQT 본문에서 *독립적으로 정의된* 것이
  아니면 circular.
- 대응 요구: σ_0 prior 를 L322 multistart_result 에서 직접 도출 (post-hoc 수동
  설정 금지). 도출 경로 본문 명시.

### A7 — EOS-marginalized vs EOS-fixed forecast 차이를 정직 보고
- 4인 코드리뷰팀에 강제 요구: EOS-fixed (e.g. SLy4 only) forecast 와
  EOS-marginalized (chiral-EFT family flat prior) forecast 의 ΔlnZ 두 값을
  *동시* 표시. 둘 차이가 > 1 이면 P11 = EOS-dependent 판정.
- 공격: EOS-fixed 만 보고하면 본문 자동 과장.

### A8 — Kill switch
- EOS-marginalized ΔlnZ < +1 이면 P11 = "anchor pool 추가 비추천". 본문에서
  "P11 reserve" 표현도 삭제, NEXT_STEP 으로만 보존.
- EOS-marginalized ΔlnZ > +3 이면 본문 baseline 재판정 권한 (3-regime 강제 가능).
- ΔlnZ ∈ [+1, +3] 이면 현 정책 유지: "조건부 reserve, EOS-tight prior 시점에
  재평가".

## 종합 판정 (사전)

본 세션 simulation 결과를 받기 전, 8인 사전 컨센서스:
- σ_0 의 SQT 예측은 *high-ψ regime 곡률* 이라는 의미에서 structural 후보지만,
  evaluation point (ρ_c) 와 measurement channel (NICER/GW170817) 양쪽이
  EOS 에 종속 → 종합적으로는 "structural-but-EOS-coupled".
- P11 anchor 가치는 EOS prior 폭의 함수. 본 세션 forecast 의 핵심은
  **EOS-marginalized ΔlnZ** 단일 숫자.

## 본 세션 deliverables 요건

1. simulations/L425/run.py — NS saturation σ_0 mock forecast.
   * EOS family: 4-5 chiral-EFT (APR, SLy4, BSk21, BSk22, MPA1) flat prior
     marginalize.
   * 2-regime baseline vs 3-regime SQT 두 모델 ΔlnZ Monte Carlo (~500 mock).
   * 병렬: multiprocessing spawn pool, 워커당 단일 스레드.
   * 산출: results/L425/forecast_summary.json
2. REVIEW.md (4인 자율분담) — 코드 검증 + 수치 결과 + ΔlnZ 해석.
3. NEXT_STEP.md — A8 kill switch 발동 여부 결정 + L426 ~ 다음 행동.

## 정직 한 줄

P11 의 anchor 가치는 σ_0 prediction 의 structural 정도가 아니라
EOS-marginalized ΔlnZ 숫자가 결정한다.
