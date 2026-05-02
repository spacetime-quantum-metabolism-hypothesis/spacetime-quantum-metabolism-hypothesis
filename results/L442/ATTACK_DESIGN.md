# L442 ATTACK DESIGN — Statistical Methods Appendix

## 목적
R3 reviewer 권고 해소: AICc/BIC/DIC/WAIC, marginalized lnZ (Laplace), proper BMA,
mock injection setup, R-grid sensitivity 를 한 부록 문서로 통합.

## 산출물
- `paper/STATISTICAL_METHODS_APPENDIX.md` (신설)
- `results/L442/{ATTACK_DESIGN, NEXT_STEP, REVIEW}.md`

## 3 단계 (8+4) 패턴

### Stage 1 — 8 인 팀 (이론 / 통계 / 베이지안 / 시뮬레이션 / 우주론 / 데이터 / 검증 / 편집)
- 역할 사전 지정 없음. 자유 분담.
- 산출: 부록 섹션 구조 + 정의 형식 + R3 권고 매핑.

분담 자연 수렴 결과
- A. AICc/BIC 의 정의·전제·작은 표본 보정.
- B. DIC/WAIC: pD 정의 차이, posterior sample 기반 추정자.
- C. marginalized lnZ Laplace 근사: −0.5 χ²_min + 0.5 ln det(2π Σ) 항.
- D. proper BMA weight: w_i ∝ Z_i π_i. fixed-θ vs marginalized 구별 (L6 재발방지 참조).
- E. mock injection setup: input theta_true, prior, noise model, seed, repetition.
- F. R-grid sensitivity: model R 격자 (N, log/lin spacing), Δχ² stability test.
- G. uncertainty propagation: profile likelihood vs MCMC posterior 비교.
- H. 편집 — R3 reviewer comment 매핑 표 작성.

### Stage 2 — 4 인 코드/수식 검증
- AICc 공식 `AICc = AIC + 2k(k+1)/(n-k-1)` (Hurvich-Tsai 1989) 부호·인자 점검.
- BIC `BIC = k ln n − 2 ln L_max` 점검.
- DIC `DIC = D_bar + p_D, p_D = D_bar − D(theta_bar)` 점검.
- WAIC `WAIC = -2(lppd - p_WAIC)` Watanabe 2010 정의 점검.
- Laplace `ln Z ≈ ln L_max + ln π(θ_MAP) + 0.5 d ln(2π) − 0.5 ln |H|` 차원·부호 점검.
- BMA Occam 패널티 (L6 재발방지) 명시.

### Stage 3 — Synthesis & write
- 정직 한 줄 명시: "이 부록은 정의·근사·재현 절차만 기술하며 새로운 데이터/예측을 포함하지 않는다."

## 제약
- 수치 결과 값 (Δχ², ln Z 차이 등) 은 본문/타 부록 인용만, 본 부록은 방법론.
- L6 재발방지: fixed-θ vs marginalized Δ ln Z 혼동 방지 절 필수.
- 유니코드 print 사용 안 함 (문서 전용, 코드 없음).
