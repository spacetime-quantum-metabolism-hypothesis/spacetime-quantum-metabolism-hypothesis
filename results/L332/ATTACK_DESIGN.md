# L332 ATTACK DESIGN — 3-regime vs 2-regime 결정적 구분

상위 컨텍스트: L322 결과 ΔAICc(2→3) = +0.77 (즉 2-regime merge 가 0.77 우세). 누적
245 loop, 등급 ★★★★★ -0.07, JCAP 91-95%. 현 데이터 (DESI BAO + Pantheon+ + CMB
compressed + RSD) 만으로는 3-regime 강제성이 약함.

## 8인 독립 공격

### A1 (관측 anchor 후보 sensitivity)
- P9 dSph (dwarf spheroidal kinematics): 매우 저 ψ 영역 (ratio < 1.05) 의 g(rm1)
  곡률 직접 측정. 중간 regime 가 아닌 저 regime 에 집중 → 3-regime 차별력 약함.
  예상 ΔAICc 기여: ±0.2.
- P11 NS saturation (중성자별 maximum mass scaling): 고 ψ ratio (>50) 에서 g(rm1)
  의 turnover/saturation 형태 강제. 2-regime 의 sigmoid-weight 단일 amp 와
  3-regime 의 separate high-amp 를 직접 구분. **이것이 가장 강력**. 예상 ΔAICc:
  −1.5 ~ −2.5 (3-regime 쪽 favor).
- Dark void galaxies (cosmic void H0 anomaly, ψ ↓ region): 저-중 regime 경계
  curvature 프로빙. 보조 역할.

### A2 (정보론적 임계값)
- 3-regime 강제 임계: ΔAICc(2→3) < −2 (실질적 evidence). 현재 +0.77 → 임계 도달
  하려면 anchor 추가 chi2 개선이 ≥ 2.77 + 2*(추가 자유도) 필요. 3-regime 자유도
  +2 가정 시 단일 anchor 가 Δχ² ≥ 6.77 줄여야 함.

### A3 (forecast 조건)
- P11 NS saturation 의 mock: 고 ψ regime 에서 g_high - g_mid 차이가 σ_data 의 3σ
  이상이면 reject 가능. 현 sigmoid-weight 모델이 실제로는 mid amp 와 high amp 를
  ~15% 차이로 구별하므로, NS data σ < 5% 정확도면 3-regime 강제 성공.

### A4 (대체 가설)
- 2-regime merge 가 *진짜 글로벌 최적* 일 가능성: SQT 가 본질적으로 매끄러운
  단일 transition 일 수 있음. 3-regime 분리는 numerical overfitting 의 잔재.
  L322 의 +0.77 은 이 해석과 일관.

### A5 (anchor independence test)
- 추가 anchor 가 BAO/SN/CMB 와 *독립* 정보를 줘야 함. dSph 는 H0 와 부분
  degenerate → 정보 이득 적음. NS saturation 은 nuclear EOS 결합으로 제 4의 채널
  성격 → 정보 이득 큼.

### A6 (체계 오차 위험)
- NS maximum mass 는 EOS 불확실성 ~0.2 M_sun. SQT 신호가 ψ-ratio 에서 1-2% 수준
  이면 EOS systematic 에 묻혀 false null. anchor 도입 전 EOS marginalization
  필수.

### A7 (글로벌 입증 가능성 정직 평가)
- 현 데이터로는 글로벌 입증 **불가능**. ΔAICc=+0.77 은 단순 모델 우세를 가리킴.
- P11 anchor 가 가설대로 작동 시 *조건부* 글로벌 입증 가능 (Δχ² ≥ 6.77 가정).
- 가능성: ~30-40% (NS EOS systematic 고려).

### A8 (sequencing)
1. P11 mock forecast (FIM 또는 quick-fit) → 예상 ΔAICc 분포.
2. EOS marginalization 통합 후 robust forecast.
3. P9, void 는 P11 결과 후 후순위.
- Kill switch: P11 forecast 에서 95% 시뮬에서 |ΔAICc(2→3)| < 2 이면 3-regime
  글로벌 입증 단념, 2-regime 채택 → 논문 본문 수정.

## 종합 판정
- 3-regime 강제 가능 anchor: **P11 NS saturation 단독 가장 유망**.
- ΔAICc 임계: −2 (실질) ~ −5 (강함).
- 정량 forecast (8인 합의 중앙값):
  - P11 추가 시 ΔAICc(2→3) 기대 ≈ −1.8 (1σ ±2.0). "3-regime 약 우세" 가능성 55%.
  - P9 dSph 만 추가: ΔAICc ≈ +0.3 (변화 거의 없음).
  - Void galaxies: ΔAICc ≈ −0.1.
- 정직 결론: 글로벌 입증은 P11 + EOS systematic 통제 하에서만 *조건부* 가능.
  현 시점에서는 입증 불가, 2-regime 이 baseline 으로 채택되어야 함.
