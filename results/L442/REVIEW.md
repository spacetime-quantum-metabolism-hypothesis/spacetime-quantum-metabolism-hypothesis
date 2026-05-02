# L442 REVIEW — STATISTICAL_METHODS_APPENDIX.md

## Stage 1 (8 인 팀 / 자율 분담, 역할 사전 지정 없음)

자유 분담 결과 자연 분배:
- A: AICc/BIC — §A.1.1, A.1.2 작성. Hurvich-Tsai 보정, n-k-1>0 가드 명시.
- B: DIC/WAIC — §A.1.3, A.1.4 작성. WAIC pointwise lppd/p_WAIC 정의 명시.
- C: Laplace lnZ — §A.2 작성. d/2·ln(2π) − 0.5 ln|H| 부호·차원 점검.
- D: BMA — §A.3 작성. fixed-θ vs marginalized 구별 (L6 재발방지).
- E: mock injection — §A.4 작성. 48×2000, seed=42 (Python 3.14 + emcee 안정화 규칙 준수).
- F: R-grid sensitivity — §A.5 작성. N=4000 + cumulative_trapezoid (L33 재발방지),
  ratio clip 200 (L33 재발방지) 명시.
- G: profile vs MCMC — §A.2 후반에 통합 (별도 절 없이 cross-check 로 흡수).
- H: 편집 — §A.6 R3 매핑 표, §A.7 부정직성 방지 (do-not-claim) 절 작성.

8 인 합의 사항
- 본 부록은 정의/근사/재현 절차만 포함. 새 데이터 fit, 새 posterior 숫자 도입 금지.
- L6 fixed-θ vs marginalized 혼동 방지 절 (§A.2.1) 필수 포함 — 합의.
- L33 적분 버그 (N=800 + cumsum) 명시적으로 "forbidden" 표기 — 합의.
- L5 Alt-20 SVD-degenerate (n_eff=1) BMA artefact 경고 §A.3 에 반영 — 합의.

## Stage 2 (4 인 코드/수식 검증, 역할 사전 지정 없음)

자율 분담 결과
- AICc 공식 `+ 2k(k+1)/(n-k-1)` 부호·분모 — PASS.
- BIC `k ln n − 2 ln L_max` — PASS.
- DIC `D_bar + p_D = D(theta_bar) + 2 p_D` 등가 표현 — PASS.
- WAIC `-2(lppd - p_WAIC)` Watanabe 부호 — PASS.
- Laplace `+ (d/2) ln(2π) − 0.5 ln det H` 차원 점검:
  posterior covariance `Σ = H^-1` 이므로 `+ 0.5 ln det Σ = − 0.5 ln det H` 정합 — PASS.
- BMA `w_i ∝ π_i Z_i` (marginalized Z, fixed-θ 사용 금지) — PASS.
- mock injection seed `seed=42` 내부 + `seed=100+i` 외부 — Python 3.14 + emcee
  재발방지 규칙 일치 — PASS.
- R-grid `N=4000`, `cumulative_trapezoid`, ratio clip 200 — L33 규칙 일치 — PASS.

지적 사항
- (해소됨) §A.4 step 5 의 MCMC 설정 48×2000 은 L4 K13 MCMC 예산과 일치.
- (해소됨) §A.5 ratio clip 의 sensitivity 테스트 범위 (100/200/400/800) 명시.

수식 부호/차원 추가 위반 없음. 4 인 합의 PASS.

## Stage 3 — Synthesis

8 인 + 4 인 모두 PASS. 작성 완료. 본문 본 부록 인용 추가 작업은 후속 LXX 에서 처리.

## 정직 한 줄
이 부록은 SQMH 주 분석에서 사용한 통계 도구의 정의·근사·재현 절차를 한 곳에
모은 메타 문서이며, 새 데이터/새 posterior/새 예측을 일절 도입하지 않는다.
