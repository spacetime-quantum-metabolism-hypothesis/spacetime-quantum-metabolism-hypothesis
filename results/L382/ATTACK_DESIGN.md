# L382 ATTACK DESIGN — SK Wightman propagator W_+, W_- explicit (n field, thermal eq.)

**Status**: 독립 미시 deepening 세션 (L382)
**Date**: 2026-05-01
**Lineage**: L380 계열 (SK formalism) → 본 세션은 W_+, W_- 명시 + KMS β 검증.

> 정직 한 줄: 본 산출물은 자유 스칼라 n 장의 평형 Wightman 함수(이론 표준 결과) 를 SQMH n 장 표기로 재정리하고, KMS 조건을 수치적으로 검증한 것이며, 새로운 물리 예측은 포함하지 않는다.

---

## 0. 동기와 위치

SQMH 의 n 장 (대사 밀도 요동) 은 Schwinger-Keldysh (SK) closed-time-path 위에서 정의되는 양자 통계장이다.
선형 응답·요동-소산 정리 (FDR) 를 SQMH 측면에서 활용하려면 두 가지 Wightman 함수
- W_+(x, x') ≡ ⟨n(x) n(x')⟩
- W_-(x, x') ≡ ⟨n(x') n(x)⟩

를 명시적으로 알아야 한다. 본 세션은 다음을 수행한다.

(a) 평형 (열적, 온도 T = 1/β) 가정 하 n 장 Wightman 함수의 ω-공간 표현 W_±(ω, k) 도출.
(b) KMS 관계 W_+(ω) = e^{βω} W_-(ω) 를 수치 격자에서 직접 검증.
(c) ω → 0 / ω → ∞ 비대칭 한계 (FDR 와의 연결) 점검.

본 세션은 결과 자체보다 **SQMH 표기로의 정착 + 수치 인프라** 를 목적으로 한다 (이론 신규성 없음).

---

## 1. 설정 (방향만)

- 장: 자유 실수 스칼라 n(x), 질량 m, 분산 ω_k = √(k² + m²).
- 상태: 길깁스 (Bose-Einstein) 분포 n_B(ω) = 1/(e^{βω} − 1).
- SK 시간 윤곽: forward (+ branch), backward (− branch); Wightman 은 + → − 분기 사이 양자 평균.
- 검증 대상: KMS, 실수성, 양수성 (positivity of spectral function ρ(ω) = W_+ − W_-).

수식 형태는 본 세션에서 자유 도출 (CLAUDE.md 최우선-1: 외부 지도 금지). 본 ATTACK_DESIGN 에는 수식 없음. simulations/L382/run.py 안에서만 표현.

---

## 2. 수행 단계

1. **이론 정리** (REVIEW.md 본문)
   - SK 윤곽 위 두-점 함수 정의 (W_+, W_-, G_F, G_R, G_A 의 관계).
   - 평형 가정 → KMS 가 Wightman 비율을 e^{βω} 로 고정.
   - Spectral function ρ(ω) = W_+(ω) − W_-(ω) ≥ 0 (양수성 조건).

2. **수치 검증** (simulations/L382/run.py)
   - β ∈ {0.5, 1.0, 2.0}, m ∈ {0, 0.3, 1.0} 격자.
   - ω ∈ [−5, 5] 구간 grid 800 포인트.
   - W_±(ω) 계산, 비율 W_+/W_- 와 e^{βω} 잔차 측정.
   - ρ(ω) 양수성 확인.
   - figure: W_+(ω), W_-(ω), ρ(ω), KMS residual 4-패널 plot.

3. **검증 게이트**
   - K1 (KMS): max |W_+(ω)/W_-(ω) − e^{βω}| / e^{βω} < 1e-10 (해석적 일치).
   - K2 (양수성): min ρ(ω) ≥ −1e-12 (수치 영 이하).
   - K3 (실수성): |Im W_±(ω)| < 1e-12 (1+1D 단순 case).
   - K4 (β 스케일링): β 변경 시 비율 e^{βω} 가 정확히 추적.

4. **출력**: REVIEW.md (수식 + 수치 표 + 그림 링크), figure png.

---

## 3. 산출물

- `results/L382/ATTACK_DESIGN.md` (본 파일)
- `results/L382/REVIEW.md` (이론 + 수치 검증 결과)
- `simulations/L382/run.py` (Wightman 계산 + KMS 검증 + plot)
- `results/L382/wightman_kms.png` (4-panel figure, run.py 가 생성)

---

## 4. 비목표

- 상호작용 σ_n n³ vertex 효과 (NLO loop): L383+ 별도 세션.
- 비평형 Keldysh rotation (G_R, G_A 의 재구성): 본 세션은 평형 한정.
- SQMH-specific microphysics (소멸 항 J_q): L380 계열 별도.

본 세션은 표준 결과의 SQMH-내 정합 정리 + 수치 인프라 구축에 한정.
