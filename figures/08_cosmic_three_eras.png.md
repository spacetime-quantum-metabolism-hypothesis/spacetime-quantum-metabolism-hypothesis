# Figure 08: 우주 3시대 -- 복사 -> 물질 -> 암흑에너지

## 내용
SQMH에서 우주 3시대 자동 전이: 복사 → 물질 → 암흑에너지. 핵심: T^α_α=0 (복사)에 의한 자동 디커플링.

## 주요 결과
- **Top panel**: 밀도 분율 Ω_r(a), Ω_m(a), Ω_DE(a) 진화
  - 복사-물질 등가: a_eq ≈ 2.90×10⁻⁴ (z ≈ 3445)
  - 물질-DE 등가: a_DE ≈ 0.77 (z ≈ 0.29)
- **Bottom panel**: SQMH 순대사율 R_net/Γ₀
  - 복사 시대: T^α_α = 0 → 소멸항 = 0 → 순생성만
  - 물질 시대: 소멸 활성화 → 중력 지배
  - DE 시대: 물질 희석 → 다시 순생성 지배

## 검증 상태
- **base.md VII**: 3시대 자동 재현 확인
- **T^a_a=0 디커플링**: 복사 에너지-운동량 텐서의 trace=0이 Lorentz invariance에서 자동 도출

## 데이터 출처
- Omega_m=0.3153, Omega_DE=0.6847, Omega_r=9.15e-5 -- Planck 2018 (arXiv:1807.06209, Table 2)
- H0=67.36 km/s/Mpc -- Planck 2018

## 해석
SQMH의 가장 우아한 특징 중 하나: 복사 시대에 중력-DE 결합이 자동으로 꺼짐. ad hoc 가정이 아니라 T^a_a=0 (massless 입자의 에너지-운동량 텐서 trace)에서 필연적으로 따르는 결과. BBN 등 복사 시대 관측과의 정합성을 자연스럽게 보장.

## 재생성
```
cd simulations && python cosmic_three_eras.py
```
