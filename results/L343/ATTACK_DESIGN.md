# L343 ATTACK DESIGN — RG cubic β-function saddle FP 정량 매핑

## 상위 컨텍스트
- 누적 loop: L77~L342 = 246 (라벨 명목 255). 등급 ★★★★★ −0.07. JCAP 90~94%.
- L341 결정: 3-regime narrative 보존 (논문 본문 "compatible with cubic β-function
  fixed-point topology" 표현 유지, "predicts" 금지).
- L334 미해결 과제: σ_cluster anchor 가 RG saddle FP 와 *자연스럽게* 정렬하는지
  정량 미평가. L343 는 이 한 점만 독립 평가.

## 본 라운드의 본질
3-regime narrative 가 RG topology 의 "산물" 이라고 인접 표현으로 쓰려면
**최소** 두 조건 필요:

1. cubic β(σ) ansatz 의 FP 토폴로지가 압도적 다수에서 saddle 을 **포함**.
2. saddle 의 위치가 σ_cluster anchor 부근에 *우선적* 으로 출현.

두 조건이 모두 만족되어야 "기하적 자연스러움" 주장 가능. 단일 조건만이면
narrative 약화.

## 8인 독립 공격 방향 (수식 금지 — 방향만)

### A1 — FP 토폴로지 분류
일반 cubic β(σ) 의 FP 분류 (Trivial 0 + 두 비자명 root, 안정성 부호 조합)
가 만들어내는 위상 클래스 수. 클래스 분포가 균등인가, 한 패턴이 우세한가.

### A2 — saddle 위치 분포
물리적 [σ_min, σ_max] 밴드 위에서 saddle FP 의 위치 분포. cluster 밴드
[0.8, 2.5] (BAO ratio 단위 toy) 에 saddle 이 우선 떨어지는지, 아니면
band-width 비례로 균등한지.

### A3 — 비단조 dip 의 기하적 필연성
saddle 토폴로지 보유 시 g(σ) = ∫β dσ 가 cluster 밴드에서 *비단조 dip* 을
생성하는 비율. 100% 면 필연, 50% 부근이면 우연.

### A4 — 자유 파라미터 비용
(a, b, c) 3 자유도 → AICc 패널티 6. L322 ΔAICc(2→3) = +0.77 와 결합 시
"3-regime 강제" 임계는 ΔAICc < −2 필요.

### A5 — 정직 표현
saddle 자연스러움 비율 r_nat 가 toy band-width 비율 (≈ 0.34) 와 동일 수준이면
**선호 없음** (uniform). 본문 표현 "consistent with topology" 까지 가능,
"selected by topology" 는 금지.

### A6 — narrative 보존 조건
- saddle 토폴로지 클래스 점유율 ≥ 90% → narrative *이론적 호환성* 유지 가능.
- saddle naturalness > 0.6 → narrative *자연스러움* 약 주장 가능.
- saddle naturalness ≈ uniform → narrative 의 "기하적 필연" 표현 금지.

### A7 — 위험
toy 가 SQT 미시 Lagrangian 이 아니므로 "(a,b,c) 부호" 자체에 물리적 의미를
부여하면 즉시 최우선-1 위반. 결과 해석을 "위상 구조 호환성" 으로만 한정.

### A8 — sequencing
1. simulations/L343/run.py 로 (a,b,c) grid scan + dip geometry test.
2. 결과의 두 비율 (topology 점유율, saddle naturalness, dip fraction)
   해석.
3. narrative 보존 / 약화 / 강화 판정.

## 산출물
- simulations/L343/run.py
- results/L343/scan_results.json
- results/L343/REVIEW.md
- results/L343/NEXT_STEP.md

## 사전 forecast (8인 합의 중앙값)
- saddle 포함 토폴로지 점유율 ≥ 95% (cubic 일반성).
- saddle naturalness ≈ 0.30~0.40 (band-width 비율 부근 → uniform).
- dip fraction 0.5~0.7 (필연 아님).
- narrative 판정 기대치: **호환성 유지, 필연성 미입증**.
