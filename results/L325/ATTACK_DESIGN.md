# L325 — Theory-prior vs data-driven anchor dichotomy

## 단일 loop 독립 사고. 8인 공격 면(面)

### 컨텍스트 핵심
- L272: BB 3-regime tertile split 의 LCDM mock false-detection 100% (median ΔAICc=133)
- L301: RG FP 위치 σ*_1=0, σ*_2=b/(2c), σ*_3=b/c — 그러나 (b, c) 정량 미확정
- L294: σ_0 ∝ G·t_P 는 단일 Planck 스케일 dim uniqueness — 3 regime 분리 무관

### 핵심 dichotomy
A. **Theory-prior anchor**: 데이터 보기 전 (b, c) 또는 σ_cosmic, σ_cluster, σ_galactic 을 미시이론 (1-loop β, holographic) 으로부터 *수치적으로* 도출.
B. **Data-driven anchor**: tertile / quantile split, 또는 BAO bin 별 σ_eff 측정 후 fit. → L272 형태 overfitting 채널.

### 8인 공격 (사전 역할 미지정)

A1. (b, c) 계수의 1-loop β-function 직접 계산 가능성 — SQT field theory Lagrangian 에서 출발 가능?
A2. σ_0 = 4πG·t_P 단일 스케일에서 *dimensionless* 비율 σ_galactic/σ_cosmic, σ_cluster/σ_cosmic 산출 경로?
A3. RG FP 3개 *위치* 가 (b, c) 비율로만 결정 — 비율 b/c 자체의 priori 예측?
A4. Holographic 인수 4π 가 horizon area 에서 왔다면, regime 별 *characteristic horizon* (Hubble, virial, galactic) 로부터 σ_regime 직접 도출 가능?
A5. L294 dim uniqueness 는 ONE scale only — 3 anchors 는 dim 만으로 절대 fix 불가. additional input 필수, 그 input 이 데이터인지 이론인지 구별.
A6. False-detection mitigation: anchors 를 *prior 분포* (Gaussian around theory mean) 로 두면 vs *delta function* 으로 두면 — false rate 차이 정량.
A7. Frequentist k-fold CV: 절반 데이터로 anchor fit, 나머지 절반에서 ΔAICc 재계산 — 진짜 신호 vs 자유도 분리.
A8. Asymptotic safety FP 가 정량적이려면 truncation 차수 (Einstein-Hilbert vs higher-derivative) 명시. 어느 truncation 에서 (b, c) numerically stable?

### Top 3 (independent triage)
- **A1** — (b, c) 의 미시 도출이 가능하다면 theory-prior 채널 살아남음. 가장 결정적.
- **A4** — horizon-area 인수에서 regime-specific σ 직접 — 가능하면 BB 살림.
- **A6** — anchor prior 분포 mock test 로 false-rate 정량화.

### 진짜 질문
σ_cosmic, σ_cluster, σ_galactic 의 *수치값* 이 어떤 데이터도 보지 않은 상태에서 도출되는가?

답: **현재 No.**
- L294 는 σ_0 단일 스케일만 고정.
- L301 은 FP *구조* (3개 존재) 만 제공, 위치 비율 b/c 미확정.
- BB 의 σ_cosmic=10^8.37 등은 BAO bin tertile 에서 추출한 *post-hoc* 라벨.

### 시뮬 설계 (실행 보류 — 이론 결정 우선)
S1. Mock LCDM 1000 realisations, anchors 를 *fixed Gaussian prior* (μ=L301 FP 값, σ=0.5 dex) 로 marginalise. False-rate 재측정.
S2. Anchors 가 진정 theory-prior 라면 false-rate ≤ 5% 예상. 만약 여전히 >50% 면 prior 도 충분하지 않음.
