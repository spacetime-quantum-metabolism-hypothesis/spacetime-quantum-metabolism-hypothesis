# L410 — 4인팀 코드리뷰 + 시뮬 결과 (Cluster anchor pool 확장 forecast)

*역할 사전 배정 없음. 4인이 자율 분담으로 데이터 정합성 / 코드 / 통계 / 정직성 검토.*
*★ mock-based forecast; published archive crawl deferred. RECOVERY 확정 아님.*

---

## 시뮬 결과 (`simulations/L410/run.py`)

| N | dom_var | dom_chi2 | dom_loo | dAICc(3reg-mono) | FDR(3reg) | status |
|---|---------|----------|---------|------------------|-----------|--------|
| 3  | 0.412 | 0.000 | 56.930 | +nan    | 0.000 | OPEN |
| 5  | 0.327 | 0.004 | 5.555  | +inf    | 0.000 | OPEN |
| 8  | 0.229 | 0.590 | 0.228  | +89.48  | 0.000 | OPEN |
| 13 | 0.158 | 0.290 | 0.489  | +20.57  | 0.000 | RECOVERY-PROGRESS |

(`dom_var` = variance share, `dom_chi2` = Cook's-distance variant, `dom_loo` = LOO θ-norm 변화비.)

---

## 4인 자율 검토

### V1 — 데이터 정합성
- POOL 13 cluster 의 `(rho_env, σ₀)` 값은 *plausible mock*. published 표 단일 통합 archive 부재.
- Tier 분할 (1: WL, 2: X-ray, 3: PSZ2) 은 ATTACK_DESIGN A2 systematics 분리 fit 위한 sub-pool 분리에 직접 연결.
- 정직 명시: 본 결과로 published value RECOVERY 확정 주장 금지. forecast only.

### V2 — 코드 검증
- multiprocessing spawn + OMP/MKL/OPENBLAS=1 확인 (CLAUDE.md 시뮬 원칙 준수).
- `fit()` 에 `if best[1] is None` 방어 present (CLAUDE.md scipy.optimize 다중 start 함정 준수).
- N=3, N=5 의 `dAICc=nan/inf` 는 `n - k - 1 ≤ 0` (3-regime k=6, n=3 또는 5) 의 자기-올바른 거동.
   → N≥8 에서만 3-regime AICc 의미 있음. N=3 에서 3-regime 채택은 by-construction overfit (§3.5 와 일관).
- LOO θ-변화비가 N=3, 5 에서 폭주 (56.9, 5.55) → small-N 회귀 자체가 불안정 (V3 통계 코멘트 참조).

### V3 — 통계 검토
- variance-share dominance: 3 → 5 → 8 → 13 에서 0.412 → 0.327 → 0.229 → 0.158. **N≈8 에서 임계 30% 통과**, N=13 에서 16% 도달.
- chi2-leverage dominance: N=8 에서 0.59 (높음) → 단일 cluster (mock 기준 MACS J0717 merging outlier) 가 χ² 의 절반 이상 leverage. ATTACK_DESIGN A2 (heterogeneous systematics) 가 실재.
- LOO θ-변화비: N=8 에서 0.228 로 안정화. N=13 에서 0.489 로 다시 상승 → Tier-2 X-ray 추가가 회귀 모형 *형태* 변경 (A2 의 second-order 효과).
- mock injection FDR = 0.000 (전 N): mock 데이터의 LCDM null 이 3-regime 의 6 파라미터 자유도를 전혀 정당화하지 못함 → **§3.5 "FDR 100%" 와 정반대 결과**. caveat: 본 mock 의 LCDM null 잡음 모델이 §3.5 보다 보수적. §3.5 와 metric/잡음 일치 시 재검증 필요 (V4 정직성).
- 결론: dominance 단일 metric 으로는 N≥8 에서 "목표 30% 달성" 가능. 단 chi2-leverage / LOO 정의 동시 사용 시 N=13 에서도 30% 미만 보장 *불가*.

### V4 — 정직성 검토
- 본 시뮬은 §6.1 row 8 RECOVERY 의 *상한 forecast*: published 실측이 mock 보다 *더 heterogeneous* 할 가능성 높음 (A2/A3/A5 공격 vector).
- mock injection FDR=0 결과를 paper §3.5 "FDR=100%" 와 *대치* 로 보고 금지. 두 결과는 metric/잡음 정의가 다름.
- N≥8 에서 "variance-share 30% 도달" 만 단독 보고 시 dominance metric cherry-picking 위반 → 반드시 3 metric 동시 + max(3) < 30% 조건.
- threshold 0.30 은 8인팀 합의 사전 설정 (NEXT_STEP §ii). 사후 변경 금지.

---

## 4인 합의 (RECOVERY 가속도 평가)

1. **포워드 진행 가능 단계** (조건부): published Tier-1 WL 8-cluster 실측 archive 수집 + V3 의 max-3-metric < 30% 동시 검증.
2. **현 시뮬 결과의 의미**: variance-share dominance 단일 채널에서 N=8 에서 30% 통과 → 회복 *경로* 존재 시사. 하지만 chi2-leverage 와 LOO 변화비가 동시에 30% 미만이 되려면 systematics 분리 fit (Tier-1 only sub-fit) 별도 필요.
3. **paper 본문 반영 권장**: §6.1 row 8 의 status 는 현재 "RECOVERY 진행중" 유지. dominance threshold (3 metric simultaneous < 30%) 와 mock-vs-published 차이를 명시.
4. **다음 LXX 위임 사항**:
   - LXX-archive: published σ₀(env) 또는 동등 측정값을 cluster-별 (Limousin 2007, Umetsu 2016, Reiprich 2002, ...) 직접 추출.
   - LXX-systematics: WL-only sub-pool vs X-ray-only sub-pool 별도 fit. cross-method consistency Δχ² 보고.
   - LXX-FDR: §3.5 의 mock-injection 정의를 본 스크립트와 align 후 FDR 곡선 N-scaling 재산출.

---

## 정직 한 줄
**N=13 mock forecast 에서 variance-share dominance 16% 도달, 단 chi2-leverage 29% / LOO 49% 동시 < 30% 미달 → "RECOVERY 가속 *경로* 확인" 까지만 주장 가능, RECOVERY 종결 주장 금지.**
