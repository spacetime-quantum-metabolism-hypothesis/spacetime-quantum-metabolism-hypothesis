# L425 REVIEW — NS σ_0 forecast 코드/수치 (4인 자율분담)

## 코드 검증 (자율분담 — 사전 역할 지정 없음)

### 발견 1: BLAS 스레드 핀 위치
- `os.environ[...]` 가 numpy import *이전* 에 설정됨. 워커당 단일 스레드 보장 OK.
- multiprocessing context 는 'spawn' (CLAUDE.md 권고 준수).

### 발견 2: numpy 2.x 호환
- `np.trapezoid` 직접 호출 사용 (CLAUDE.md L34 재발방지 항목 준수).
- `np.random.default_rng(seed)` 사용 — dynesty 가 아니지만 동일 컨벤션.

### 발견 3: chi2/Laplace 적분 정확성
- `lnL_eos_marg` 의 log-sum-exp 정상 구현 (M = max, exp(half-M).mean()).
- `ln_evidence_3reg` 의 1-D γ_hi 적분: n_grid=129, ±4σ 범위. Gaussian prior
  꼬리 누락량 < 1e-4 (충분).
- 2-regime 모델 (γ_hi=0 fixed) 은 적분 차원이 1 작음 → 자동으로 Occam 패널티
  포함. 별도 파라미터 카운트 보정 불필요.

### 발견 4: EOS-fix vs EOS-marg 분리 보고
- ATTACK A7 요구사항 (두 prescription 동시 보고) 충족.
- inject (γ_truth = 0.04) 와 null (γ_truth = 0) 분리 → false positive rate
  추정 가능.

### 발견 5: 잠재적 한계 (정직 기록)
- 본 forward map (A_M, A_R, A_L) 은 *phenomenological*. 진짜 SQT 3-regime
  곡률→NS observable 매핑은 TOV + chiral-EFT 기반 EOS perturbation 으로
  계산해야 함 (현재는 선형 ansatz).
- EOS family 5종은 chiral-EFT 호환 nucleonic 만. hybrid quark / hyperonic 제외
  (ATTACK A1 의 명시적 사전 제한).
- NICER R(1.4) σ=0.8 km, M_max σ=0.10 M_sun 는 *현재* (2024-2026) 측정 수준.
  SKA / nextgen NICER 시점에서 σ 절반 이하로 축소되면 결과 재판정 필요.

## 수치 결과 (n_mock = 500, 9 워커, 0.25 초)

| Prescription | inject γ=0.04 | null γ=0 |
| --- | --- | --- |
| EOS-marginalised median ΔlnZ | -7e-5 | -1.9e-4 |
| EOS-marginalised mean ΔlnZ   | -1.5e-4 | -5.8e-5 |
| EOS-marginalised std         | 8.5e-4 | 1.3e-3 |
| EOS-fixed median ΔlnZ        | -1.6e-4 | -2.4e-4 |
| frac(ΔlnZ > 1) (inject)      | 0.0 % | 0.0 % |
| frac(ΔlnZ > 3) (inject)      | 0.0 % | 0.0 % |

**판정: ΔlnZ ≈ 0 (EOS-marg median ≪ +1) → A8 KILL 발동.**

## 민감도 점검 (sanity check)

코드 정상 작동 확인을 위한 보조 실험:
- γ_hi_true scan ∈ {0, 0.05, 0.10, 0.20, 0.40}: ΔlnZ median 모두 < 1e-3.
  → SQT 의 high-ψ 곡률이 NICER+GW170817 noise floor 아래.
- 결합 강도 A_{M,R,L} × 30 인공 증폭: ΔlnZ std ≈ 0.41, frac>1 ≈ 3 %.
  → 매우 강한 결합에서도 EOS-marginalisation 이 신호를 흡수 (ATTACK A1/A5
  공격이 실제로 작동함을 직접 입증).

## 해석

1. SQT 의 NS saturation σ_0 예측은 "structural" 후보지만, 관측 채널
   (NICER mass-radius, GW170817 tidal) 의 현재 noise floor 와 EOS family
   variance 가 SQT 보정량을 *완전히 흡수*. anchor 자격 없음.
2. ATTACK A4 (NICER 정보량 부족), A5 (universal relations 흡수), A7
   (EOS-marg vs fix 차이) 모두 sim 으로 확인.
3. ATTACK A8 kill switch 발동 조건 (EOS-marg ΔlnZ median < +1) 충족.
   → P11 anchor pool 추가 *비추천*.

## 4인 합의 (자율 도출)

- 코드 정상. 수치 결과 정직.
- 결과는 "SQT 가 틀렸다" 가 아니라 "현재 데이터 수준에서 SQT-NS 채널 정보량
  부재" 를 의미.
- 본문 baseline 결정에 영향 없음: L367 의 "3-regime baseline + caveat"
  narrative 유지. P11 은 "조건부 reserve" 에서 "보류" 로 한 단계 강등.
- 향후 nextgen NICER (σ_M < 0.03 M_sun) 또는 binary NS post-merger GW signal
  탐지 후 재평가 가능성 보존.

## 정직 한 줄

EOS-marginalised ΔlnZ ≈ 0 → P11 NS anchor 는 현재 무가치.
