# L475 SPECULATION — Cluster dip 가설: macroscopic decoherence boundary

**세션**: L475 (자유 추측 / speculation only)
**날짜**: 2026-05-01
**정직 한 줄**: cluster scale (~Mpc) 이 우주에서의 *quantum-classical 경계* 라는 가설 — 입증 시도 아니고, falsifiable 방향만 8인팀에 제시.

## CLAUDE.md 준수

- **[최우선-1]**: 본 문서는 *방향*만. 수식·파라미터·prefactor 일체 미지정. 8인팀이 자율 도출.
- **[최우선-2]**: 본 문서는 가설 진술 + 검증 채널 이름만. 수식 유도 없음.
- **자유 추측 명시**: 결과 무효 / paper 인용 금지. base.md 와 분리 보관.

---

## 0. 출발 관찰

L33~L34 BAO SQT 스캔에서 반복적으로 보고된 **cluster-scale dip** (z 효과로 wrapping 된 D_M/r_d, D_H/r_d 잔차의 cluster-redshift 영역 underdensity) 은 현재까지 다음 channel 로만 해석됨:

- (i) BAO sample variance / mock noise.
- (ii) IDE 또는 fluid-DE w_a 의 z-localised feature.
- (iii) modified gravity G_eff (z) wiggle.

이 세 가지는 *고전 배경/섭동* 채널이며 — L475 는 **네 번째 채널** 을 자유 추측으로 제시한다:

> **(iv) cluster scale 이 quantum coherence 가 우주적 평균에 기여하는 *경계* 이며, dip 은 그 경계 너머로 coherence 가 sharp 하게 dropout 하는 흔적이다.**

## 1. 가설 H475

**H475-A**: 우주 시스템의 Q-parameter (L403/L434 의 미정 canonical Q) 가 cluster scale 근방에서 *임계치 1 통과*. 이하는 양자, 이상은 고전.

**H475-B**: dropout 은 sharp 하지 않고 transition window (decoherence rate Γ_dec 가 Hubble rate H 와 교차하는 영역) 에서 일어난다.

**H475-C**: dropout 결과 cluster 통계 (BAO peak 위치, RSD f σ_8, weak lensing kappa) 의 ensemble-평균값이 *순수 고전 LCDM* 예측에서 작게 deviate 한다 — 이 deviate 가 BAO dip.

## 2. 평가 4축 (방향만)

### S1 — Decoherence vs entanglement 관점
- environmental decoherence (Joos-Zeh, Zurek) 은 *국소 기준계 측정자* 가정.
- 우주 background 에는 외부 측정자가 없음 → cosmological decoherence 의 *효과적* 메커니즘 후보:
  - CMB 광자 산란 (z 의존, T_CMB ∝ 1+z).
  - graviton bath (Hawking-Hartle, fluctuation-dissipation).
  - SQT-내재 metabolic mixing (L0/L1 axiom 의 비단조 확률 진화 가능성).
- entanglement 측: cluster-scale 까지 entangled state 가 보존되는가? 아니면 cluster scale 자체가 entanglement entropy 의 *상전이 임계*?
- → 본 가설은 *환경-유도 decoherence* 와 *내재 metabolism* 양쪽 미정 — 8인 자율 선택.

### S2 — Macroscopic coherence length L_coh
- L_coh 의 후보 출처:
  - Penrose-Diosi (m, ρ 기반) — galaxy 단위에서 saturate.
  - Joos-Zeh thermal photon (T_CMB, n_γ) — z 의존, 현 시점 ~ ?
  - SQT L0/L1 metabolic horizon (axiom 직접) — 미정.
- L475 자유 추측: 위 셋의 *정합 단일 scale* 이 cluster (1~10 Mpc) 근방으로 떨어질 가능성. 8인이 prefactor 도출.

### S3 — Quantum-classical transition 영역으로서의 cluster
- subgalactic (< Mpc): coherence loss 충분 → 고전.
- supercluster (> 100 Mpc): self-averaging 으로 ensemble 고전화.
- cluster (1~10 Mpc): *경계 영역* — Q ≈ 1, Γ_dec / H ≈ 1.
- 검증 채널:
  - **CH1**: BAO dip 의 redshift-shape 가 Γ_dec(z) / H(z) 의 z 의존성과 phenomenologically 합치하는가.
  - **CH2**: cluster-mass-bin 별 BAO residual 이 mass (decoherence 강도 proxy) 와 monotone 관계인가.
  - **CH3**: weak lensing convergence variance 의 cluster scale 비정규성.
  - **CH4**: 21cm intensity mapping (PUMA/SKA) cluster scale variance.

### S4 — Q-parameter 와의 연결 (L403 / L434)
- L403/L434 가 정의한 cosmic Q (canonical 미정) 가 cluster scale 에서 1 을 통과하는가?
- 직접 link:
  - Q 의 입력 (m, L, T_obs, T_K) 를 *cluster ensemble* 로 평균하면 어떤 정의 (A/C/D/E) 가 1 근방 출력을 내는가?
  - L403 Q_macro span 140-decade 결과는 *시스템별* — cluster *ensemble* 평균은 별도 계산 필요.
- 결합 가설: **L403 canonical Q 정의가 단일이면 그 정의는 cluster scale 에서 Q ≈ 1 을 자연 예측해야 한다** (정합성 강한 검증).

## 3. Falsifiable 예측 4개 (방향만)

- **F1**: BAO dip 의 z-shape 는 z 단조 함수 (단조 dropout) 가 아니라, transition window 에서 *peak-and-recover* 패턴. 단조 IDE 모델로는 fit 불가.
- **F2**: dip 진폭이 cluster mass-bin 에 따라 monotone 으로 변한다 (coherence loss 가 m, L 의존이므로).
- **F3**: 동일 redshift bin 에서 lensing 잔차와 BAO 잔차가 *상관*. 순수 고전 IDE/MG 는 무관.
- **F4**: SQT canonical Q 가 cluster ensemble 입력에서 ~1. 다른 정의가 1 에서 멀면 그 정의는 H475 부정.

## 4. 시뮬레이션 (선택 — toy)

`simulations/L475/run.py` — cluster scale 에서 sigmoid 형 *coherence weight* w(M, z) 를 가정하고, BAO 잔차 z-shape 가 transition-window 형태 (peak-and-recover) 가 *재현 가능한지* 만 확인. prefactor 미지정. 부호 / 위치 자유, 8인이 합의 후 prefactor 도출.

본 toy 는 H475-B/C 의 *질적 가능성* 만 확인. 실제 fitting / chi2 / dAICc 사용 금지 (CLAUDE.md L33~L34 재발방지 규칙 준수).

## 5. 8인 자율 결정 항목

- D1: decoherence 채널 (CMB γ / graviton / SQT 내재) 중 어느 것을 H475 micro-mech 으로 채택?
- D2: L_coh 도출 경로 — 외부 환경 vs L0/L1 axiom?
- D3: F1~F4 중 lab-falsifiable 채널 우선순위?
- D4: L403/L434 canonical Q 정의가 H475 와 정합성 가지려면 어느 정의여야 하는가?

## 6. 반대 가설 (devil's advocate)

- **NULL-1**: BAO dip 은 단순 sample variance. DR3 에서 사라질 가능성. → F1 단조성/ peak-and-recover 검사로 1차 falsify.
- **NULL-2**: 단조 IDE / fluid DE 로 충분 설명. → CH2, CH3 에서 mass-bin 상관 부재면 H475 약화.
- **NULL-3**: Q-cosmology 가 ill-defined (L403 다중 동률). → L434 canonical 합의 전 H475 인용 금지.

## 7. CLAUDE.md 부합성 자체 진술

- 본 문서는 *speculation*. base.md / paper 본문 인용 금지.
- 수식·prefactor·cosmological parameter 0개.
- L33 적분 버그 / clip / Om 범위 / k 패널티 규칙은 본 문서 미해당 (실 fitting 없음).
- L475 가 paper 채택되려면 (i) 8인 decoherence 채널 합의, (ii) toy 가 아닌 full-fluid + decoherence 채널 simulation, (iii) DR3 sample variance 통과 확인 필요.

---

**결론 한 줄**: cluster dip 을 양자→고전 전이의 *cosmological 흔적* 으로 보는 채널 (iv) 는 falsifiable F1~F4 가 있으며, L403/L434 canonical Q 합의와 정합성 검증 채널 (D4) 을 통해 SQT axiom 까지 직결된다.
