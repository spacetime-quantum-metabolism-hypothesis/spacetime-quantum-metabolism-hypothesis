# L407 ATTACK_DESIGN — 8인팀 공격 설계

**주제**: Three-regime σ₀(env) postdiction. Reviewer 가 "data 보고 fit"으로 칠 위험. RG saddle FP *위치* 자연성 증명 path 가 있나?

**좌표**: paper/base.md §3.4 caveat — "비단조성은 데이터 fit 에서 발견됨 (postdiction). 4 미시 축은 비단조성을 *허용* 할 뿐 a priori *예측* 하지 않음."

---

## 1. Reviewer 공격 표면 (8인팀 시뮬레이션)

### A1 — 통계학자 (overfitting reviewer)
> "ΔAICc=99 는 anchor=fit point 의 by-construction. Mock injection 에서 false-detection 100%. § 3.5 caveat 도 인정. 'falsifiable test' 는 monotonic 기각이지 *위치 예측*이 아니다."

**Severity**: 결정적. 본문 §3.5 가 이미 인정한 내용을 reviewer 도 그대로 사용.

### A2 — RG 이론가 (Wetterich)
> "cubic β(σ) topology 가 saddle 을 *허용* 하는 것은 trivial. b/c 계수가 first-principle 도출 안 됨. cluster anchor 7.75 가 cosmic IR 8.37 보다 *작다* — Wetterich monotone flow 의 standard topology (IR < saddle < UV) 와 모순. 이건 'topology 96.8% 호환'이 아니라 *topology 부적합*."

**Severity**: 치명. **L407 simulation 으로 정량 확인**: standard between-FPs 가정 시 P(saddle ∈ cluster band) = 0 (구조적). 자유 (a,b,c) scan 도 ±0.10 dex 매칭률 0.50% 에 불과.

### A3 — Holographic 이론가
> "σ₀ = 4πG·t_P 는 *우주적 평균*에서 holographic bound 와 정합. 환경 의존성 (σ_cluster = σ_cosmic / 4.2) 은 holography 가 *예측하는 양*이 아니다. screening 인자가 필요한데 그것은 4 미시축 *외부*."

**Severity**: 중대. holography 는 magnitude 만 고정, 환경 dependence 는 별개 mechanism 요구.

### A4 — Phenomenologist (cluster expert)
> "Cluster band [7.5, 8.0] 자체가 single-source dominance (A1689) 59.7%. § 3.7 13-cluster pool 까지 가야 이 anchor 가 robust. 현 paper 는 anchor 자체가 fragile."

**Severity**: 중대 — 그러나 §3.7 가 이미 회복 경로 명시.

### A5 — EFT/RG matching reviewer
> "1-loop EFT 에서 b, c 는 field content 와 cutoff 의존. 4 미시축 (T^α_α coupling, dark-only embedding, conformal Lagrangian, β_eff = Λ_UV/M_Pl) 으로 b, c 의 sign 만 잡혀도 *큰 진전*. 현 paper 는 b, c sign 도 derivation 없음."

**Severity**: 중대. 하지만 *future work* path 명확 — § 6.1 row "RG b, c future" 에 등재.

### A6 — Bayesian (model selection)
> "Δln Z_marginalized = 0.8. R=3,5,10 prior sensitivity 도 모두 |Δln Z| < 1.5. Jeffreys scale 에서 'not worth more than a bare mention'. 17σ narrative 와 충돌. PASS 등급은 PASS_WEAK 강등 필요."

**Severity**: 중대 — 그러나 paper §3.6 에 이미 정직 기록. "17σ" 는 § 3.3 에서 *regime-간 gap* 한정 표기.

### A7 — 이론적 일관성 (foundations)
> "6 axiom + 5 derived 가 σ₀ 를 *정의* 하지만 σ₀(env) 는 정의 안 함. base.md §2 도식에서 environment 함수성은 *외삽*. 이건 framework 외부 추가 가정."

**Severity**: 결정적 — 단, paper 가 이미 §3.4 에서 동일 자가 인정.

### A8 — Editor/Devil's advocate
> "결국 §3.4 caveat 가 paper *전체*의 limit 이다. PASS_STRONG 11/32 중 σ₀ 관련은 6/32 가 holographic identity 산술 따름결과 — independent prediction 0. SQT 는 *consistent phenomenological framework* 지 *predictive theory* 가 아니다."

**Severity**: 결정적. 이게 reviewer 의 최종 판정 가능성 가장 큼.

---

## 2. RG saddle FP 위치 자연성 *증명* path 평가

| Path | 목표 | 평가 (8인팀 합의) | 단계 |
|------|------|------|------|
| P1: Wetterich Wilsonian truncation | b, c 를 cutoff scale Λ_UV ↔ IR flow 로 도출 | **부분 가능**. b sign 만 잡아도 monotone 기각의 *이론적* 근거. 위치는 cutoff identification 자유도로 fix 안 됨. | NEXT_STEP §1 |
| P2: 1-loop EFT operator scan | dark-only T^α_α coupling 의 1-loop β-function 으로 σ_cluster 위치 예측 | **불확실**. matter sector field content 가정 의존. 그러나 sign 만 fix 해도 *direction* 예측. | NEXT_STEP §2 |
| P3: Holographic argument | cluster 영역 = Page-curve middle 영역으로 자연 emergence | **약함**. holography 는 σ₀ magnitude 만 고정. 환경 의존성 자연 도출 어려움. 시도는 가능. | NEXT_STEP §3 |
| P4 (★): Cluster < cosmic 위치 → topology 재해석 | cluster 를 *deeper* IR FP, cosmic 을 saddle, galactic 을 UV 로 재배치 | **L407 수치 발견 트리거**. base.md §3 의 "cosmic = IR, cluster = saddle" 표를 정정해야 함. base.md §3.1 표 갱신 후보. | NEXT_STEP §4 |

**8인팀 합의**: P1 + P2 동시 진행이 *최소* 필요. P4 는 base.md §3.1 표 자체의 *해석 정정* — 시뮬레이션이 발견한 가장 큰 이론적 의문점.

---

## 3. 핵심 reviewer 공격 → 대응 매트릭스

| 공격 | 대응 강도 | 근거 |
|------|----------|------|
| postdiction 이다 | **자가 인정** (§3.4) | 더 이상 새 방어 불필요; 단 falsifiable monotonic-기각 차원에서만 PASS 주장 |
| 위치 자연성 미입증 | **자가 인정** (§3.2 ★) | RG b, c future work 우선순위 격상 |
| cluster < cosmic topology 부적합 | **L407 발견** | base.md §3.1 표 RG 해석 열 *정정 필수* |
| Δln Z < 1 | **자가 인정** (§3.6) | 17σ 표기 § 3.3 한정 명시 강화 |

---

## 4. 결론 (8인팀 4:4 → 만장 합의)

- priori 도출 *전면 가능성* = **낮음** (P1+P2 부분만)
- §3.4 caveat **유지**가 정직한 baseline
- L407 발견 (cluster < cosmic, between-prior P=0) → §3.1 표 RG 해석 열 정정 필요. 이건 priori 도출 실패가 아니라 *해석 오류 정정* — paper 강화.
- "위치 자연성 증명" 대신 "위치 *불자연성*을 정직 기록 + RG b, c future work" 로 전환 권고.

→ NEXT_STEP.md 로.
