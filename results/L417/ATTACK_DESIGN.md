# L417 Attack Design — 8인 팀 자율 분담

## 목표
paper/base.md §4.1 row 10 "Bullet cluster offset PASS_STRONG (qualitative)" 의 구조적 약점을 reviewer 관점에서 최대 압박.

## 8인 자율 분담 (역할 사전 지정 없음, 토의 자연 분업)
규칙: 각자 독립 공격 라인 최소 1개, 중복 금지. 라인 간 cross-talk 최종 단계에만.

## 공격 라인 (수렴된 최종 8라인)

### A1. "qualitative ≠ prediction" 비판
"baryon 따라 depletion zone" 은 *방향성 진술*. **150 kpc** 이라는 숫자가 아니다. SQT 가 어떤 충돌이라도 "baryon 따라" 나오면 통과 → no-content tautology 의심.

### A2. 환경독립 σ₀ 가정의 한계
P14 axiom-level 에서 σ₀(환경) 비단조성을 *허용*. Bullet 처럼 격렬 충돌 (3000 km/s) 환경에서 σ₀ 가 *변하지 않는다* 는 가정의 정당화 부재. dynamic environment 효과 무시.

### A3. Lensing peak 위치 = 갈락시 위치 = 빈 SQT 진술
"depletion zone follows galaxies" 는 사실상 "DM follows galaxies" 와 phenomenologically 구분 불능. Λ-CDM 도 PASS. SQT 만의 "독자성" 부재.

### A4. Offset magnitude 비교 차원
MOND: predicted offset ≈ 0 (gas dominates baryons). Λ-CDM: offset ≈ 150 kpc (DM halo). SQT: ? — 숫자 없음 → MOND vs Λ-CDM 구분 가능하지만 SQT vs Λ-CDM 구분 불가.

### A5. Collision dynamics timescale 누락
충돌 속도 v ≈ 3000 km/s, halo 통과 시간 τ_cross ≈ 10⁸ yr. SQT depletion zone re-equilibration 시간 τ_q 이론적 정의 없음. τ_q ≪ τ_cross 가정해야 "baryon-tracking" 성립 — 이 부등식 검증 부재.

### A6. Lensing convergence κ 정량 부재
Clowe 2006 핵심 결과: κ 분포 이중 peak. SQT 는 ρ_eff(x) = ρ_baryon(x) + ρ_depletion(x) 의 *공간 분포* 예측 부재. peak separation 도, peak amplitude 도 미예측.

### A7. PASS_STRONG 라벨 인플레이션
MOND fail → SQT PASS 의 논리는 falsification asymmetry. "MOND 가 fail 한다" 가 SQT 를 *strong*하게 만들지 않음. PASS_QUALITATIVE 강등 압력.

### A8. 통계적 유의성 부재
Clowe 2006 offset = 150 kpc 의 8σ detection. SQT 예측 가능 범위 [0, ∞] (정량 없음) → 어떤 σ 도 reject 못함. unfalsifiable in current form.

## 종합 reviewer 평결
**"qualitative consistency ≠ quantitative prediction"** — 현재 §4.1 row 10 은 PASS_QUALITATIVE 가 정직. PASS_STRONG 라벨 유지하려면 (i) τ_q < τ_cross 부등식 도출, (ii) offset numerical prediction in kpc, (iii) Λ-CDM 와 distinguishable signature 중 최소 1개 필요.
