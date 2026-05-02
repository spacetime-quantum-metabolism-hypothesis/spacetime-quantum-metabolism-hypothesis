# L410 — Attack Design (8인팀)

**주제**: paper §6.1 row 8 "Cluster single-source dominance 59.7%" RECOVERY 상태에 대한 reviewer 공격 가능성 사전 모델링.
**현 상태**: A1689 + Coma + Perseus 3-cluster joint 로 단일 source dominance 91% → 59.7% 까지 해소. 13-cluster archive pool (LoCuSS / CLASH / PSZ2) 가용하나 실측 deferred.
**원칙**: CLAUDE.md [최우선-1/-2] 준수. 본 문서는 *방향 attack vectors* 만 정리. 수식/임계값 사전 지정 금지 — 8인이 자율 도출.

---

## 8인팀 자율 분담 (역할 사전 배정 *없음*, 토의로부터 자연 발생)

| ID | 자연 발생 영역 |
|----|---------------|
| R1 | Sample-statistics 통계학적 공격 |
| R2 | Lensing-systematics 우주론적 공격 |
| R3 | Single-source dominance metric 정의 공격 |
| R4 | Cluster selection bias |
| R5 | Theory-prior 채택 가능성 |
| R6 | Anchor=fit point by-construction risk (§3.5 와 연결) |
| R7 | LOO/Mock injection 추가 요구 |
| R8 | RECOVERY 라벨 자체 (semantic) |

---

## 예상 reviewer 공격 vectors

### A1. Sample-size 공격
- "3 cluster 만으로 σ_cluster anchor 의 표준오차가 신뢰 구간을 의미있게 좁히지 못함"
- 핵심 위험: N=3 의 t-분포 두꺼운 꼬리 → posterior width 가 LCDM 와 비구분
- 대응 방향: pool N 증가 시 σ 의 *expected* 감소율을 사전 forecast

### A2. Heterogeneous lensing systematics
- A1689 (strong+weak), Coma (X-ray hydrostatic), Perseus (X-ray) 는 *서로 다른 systematic family*
- "3 source = 1 systematic" 공격 (variance 감소가 각 cluster 의 독립 noise 가정에 의존)
- 대응 방향: weak-lensing 전용 sub-pool (LoCuSS/CLASH 동질 systematics) 분리 fit

### A3. Selection bias (massive, well-studied)
- A1689/Coma/Perseus 모두 "outlier-massive + 잘 연구된" cluster
- σ₀(ρ_env) 회귀에서 환경밀도 dynamic range 가 좁을 가능성
- 대응 방향: PSZ2 random-mass 표본 포함 시 dynamic range 증가 효과 forecast

### A4. Single-source dominance metric 정의
- "59.7%" 는 어느 정의? (variance contribution? χ² leverage? Cook's distance?)
- 정의 변경 시 dominance 지표가 다르게 나올 수 있음
- 대응 방향: 3+ 정의 (variance share / χ²-share / leave-one-out Δχ²) 동시 보고

### A5. Anchor=fit point recursion (§3.5 와 sliced)
- pool 확장이 anchor 자체를 늘리면 fit point 도 함께 증가 → 2:1 anchor:freedom 비율 유지 못 함
- 대응 방향: cross-validation (k-fold cluster) 로 mock-injection FDR 재산출

### A6. RECOVERY 라벨 의미
- "RECOVERY 진행중" 라벨이 여전히 상태 OPEN 임을 reviewer 가 강조 가능
- 대응 방향: dominance threshold (예: <30%) 사전 명시 + 미달 시 정직 ACK 유지

### A7. Theory-prior 가능성 (★ R5 영역)
- pool 확장 후 σ₀(ρ_env) 회귀가 여전히 postdiction 이면 §3.4 caveat 그대로 유지
- 대응 방향: a priori 4-microaxis derivation 분리 작업 (별도 LXX 위임)

### A8. Mock injection FDR 재계산 요구
- §3.5 "LCDM mock 200개, three-regime FDR 100%" 가 N=3 anchor 기준
- pool N=10+ 로 확장 시 mock injection 도 동일 N 으로 재실행 필요
- 대응 방향: N-scaling 하의 FDR 곡선 forecast

---

## 8인 합의 (직관 수렴)

1. **방어 가능 공격**: A1, A4, A6 — 통계 sample 추가 + 정의 다중 보고 + threshold 사전 설정으로 정직 disclose.
2. **본질 위험 공격**: A2, A3, A5 — pool 의 *질* (heterogeneous systematics + selection) 이 *양* (N) 보다 critical.
3. **회피 불가 공격**: A7 — postdiction caveat 는 anchor pool 확장으로 해소 안 됨 (§3.4).

→ NEXT_STEP 은 "정직 disclose + heterogeneous pool 의 systematics 분리" 로 설계.
