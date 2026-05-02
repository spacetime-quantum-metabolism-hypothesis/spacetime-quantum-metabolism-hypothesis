# L334 — RG β-function (b, c) first-principles 도출 시도: ATTACK DESIGN

## 배경
L325 결론: σ_cosmic, σ_cluster, σ_galactic 3개 anchor 중 최소 1개는 data-fit 필요. 이유는 RG β-function 의 b (2차), c (3차) 계수가 미확정이기 때문. 본 라운드는 이 (b, c) 를 미시 SQT EFT 에서 *priori* 도출 가능한지 평가한다.

## 목표 (구체화)
β(σ) = a·σ − b·σ² + c·σ³ 형태에서:
- (Q1) b 계수: 1-loop EFT 에서 어떤 미시 결합으로부터 발생하는가?
- (Q2) c 계수: 2-loop 또는 더 깊은 기하 (예: anomalous dim, OPE coefficient) 에서 결정되는가?
- (Q3) 만약 (a, b, c) 모두 priori 가능하면, 3개 FP 가 σ_cosmic, σ_cluster, σ_galactic 의 *절대값* 까지 priori 결정되는가?
- (Q4) 불가능한 경우, 최소 몇 개 priori 결정 가능 (정직 평가)?

## 공격 방향 (방향만 — 수식 금지)
1. **1-loop 구조 분석**: SQT 에서 σ 가 dim-ful 스케일이라면 β-function 의 각 항은 *어떤 무차원 결합* 의 다항식이어야 한다. σ 자체로 다항 전개하는 형태는 RG group 이론에서 dimensional consistency 문제가 있다. → 우선 무차원화 절차 (σ → σ̂ = σ/σ_0) 가 필요한지 확인.
2. **결합 후보**: SQT 미시에는 적어도 (i) 중력 결합 G·σ², (ii) 양자 셀 단위 t_P·μ, (iii) 메트릭 곡률 R 과 σ 의 비최소 결합 등 후보 가능. b 가 *어느* 결합에서 도출되는지 mapping.
3. **anomalous scaling**: c 가 1-loop 에서 0 이고 2-loop 에서만 살아나면, b/c 비율은 EFT 의 high-derivative 구조 (Wilson coefficient ratio) 에 의존. 이 비율이 SQMH 의 holographic 가정 (S = A/4) 에서 universal 한지 점검.
4. **fixed-point topology vs absolute scale**: RG FP 의 위치 (σ*) 는 보통 b/c 비율로 *비*만 결정. 절대 스케일은 별도 anchor (예: σ_0) 가 필요. 따라서 priori 결정 가능한 최대 자유도는 (FP 개수 − 1) = 2 비율.
5. **holographic 제약**: 만약 holographic 정리 (Bousso bound) 가 σ_0 자체를 dim-ful anchor 로 고정하면, 비율 2개 + scale 1개 = 3 anchor priori 가능. 단 holographic 가정이 SQT 에서 *유도되는지* 가 핵심 질문.

## 검증 절차 (시뮬 없음, 이론 평가)
- 8인 팀 (이론 P, EFT 전문 X, 양자중력 Y, 통계 N, 관측 O, 통합 H, 재발방지 Z, 회의주의 K) 자율 토의.
- 각자 (Q1)~(Q4) 에 독립 답변.
- 합의 도달 시 결론, 불일치 시 다수/소수 모두 기록.
- 외부 인용 시 출처 명시 (ZKB, Bonanno-Reuter, Codello-Percacci 등).

## 성공 기준
- (a, b, c) 중 priori 도출 가능한 수와 그 근거 명시.
- 불가능 부분은 *왜* 불가능한지 (자유도 부족, 미시 모델 부재, 등) 정직 진단.
- L325 등급 (★★★☆☆) 변경 여부 판단.

## 위험
- 외부 RG 결과 (asymptotic safety 등) 를 SQT 에 무비판 이식 → 과적합. CLAUDE.md "지도 금지" 원칙 준수: 외부 수식 인용 OK, 그러나 SQT 와의 *연결* 은 팀이 독립 도출.
