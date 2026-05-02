# L405 — 8인팀 reviewer attack 설계 (§3.6 BMA Δln Z = 0.8 only)

세션 일자: 2026-05-01
대상: paper/base.md §3.6 — *marginalized* Δln Z = 0.8 (R=5 prior),
BMA weight three-regime 31%.
원칙: CLAUDE.md [최우선-1, 2] — 방향만 제공, 8인팀 자율 토의 시뮬.
선행: L401 (SYNTHESIS_315), L402 (Λ-circularity), L403/L404 PLAN-ONLY.

---

## 0. 임무 framing

paper §3.6 의 marginalized Δln Z = 0.8 은 Jeffreys 척도에서 "barely worth
mentioning" (|Δln Z| < 1.0). PRD/JCAP referee 가 이 한 줄을 잡고 "this is the
*entire* statistical case — and it does not even clear the lowest Jeffreys
threshold" 로 reject 가능하다. 동시에 §3.6 "★ R=3/5/10 모두 보고 필수" 약속이
이행되지 않은 상태 (R=5 단일점만 보고). 8명 자율 토의로 공격선 발굴.

---

## 1. 8인팀 토의 시뮬 (요약)

**P1 (관측우주론):** "Δln Z=0.8 은 Bayes factor ≈ 2.2 — 동전 던져 두 번
연속 앞면 정도. 이걸로 *broken* σ₀(env) 의 새 물리를 옹호한다는 건 거의 농담.
mock injection 100% false-detection 와 합쳐지면 referee 가 §3.6 만 보고 *통계적
신호 없음* 으로 결론낸다."

**P2 (장이론):** "구조적으로 더 나쁘다. 3-regime k=5 vs LCDM k=1 인데
marginalized 에서 0.8 만 나온다는 건 Occam 패널티가 거의 모든 fit 이득을 잡아
먹었다는 뜻이다. fixed-θ Δln Z ~13 → marginalized 0.8, 즉 prior volume 패널티
~12. 이건 모델이 prior 에 *민감* 하다는 강력한 신호다."

**P3 (통계):** "★ 핵심 결함: §3.6 가 'R=3/5/10 모두 보고 필수' 라고 *스스로*
명시했는데 R=5 점 하나만 보고된 상태다. referee report 1순위 항목.
Jeffreys-Lindley paradox 영역 — wide prior 에서 Δln Z 가 음수로 떨어질 수
있고, narrow prior 에서만 양수로 살아남는 fragile 구조일 가능성이 매우 높다.
prior sensitivity 미보고는 Bayesian 분석의 minimum requirement 위반."

**P4 (현상론):** "변호 가능선: Δln Z=0.8 은 *marginalized* 값이고
fixed-θ 에서는 ~13. fixed-θ 13 도 'evidence' 는 아니지만 likelihood 측면 신호는
강하다. 동시에 §3.5 mock 100% false rate 는 *anchor 점=fit 점* 회로 때문이지
3-regime 자체가 random 이라는 뜻은 아니다. paper 가 둘을 분리 보고하면 산다."

**P5 (수리물리):** "BMA weight 31% 도 미묘하다. 5-model 가중에서 31% 는
*최고* weight 일 가능성이 큰데 paper 가 그걸 명시 안 했다. '3-regime 이 5
model 중 1위 (31%) + 2-regime 합산 64.8%' 형태로 강조선을 바꾸면 marginalized
0.8 약점이 BMA-dominance 강점으로 일부 상쇄된다."

**P6 (철학·방법론):** "Δln Z=0.8 만 가지고 'three-regime 이 데이터에 의해
선호된다' 주장은 Popper-Bayesian hybrid 기준에서 *under-justified*. 'three-regime
가 LCDM 와 *통계적으로 구분 불능* 하지만 4-axis 미시구조 *허용* 으로
의미있다' 가 정직한 framing 이다. 'modest preference' 도 과장."

**P7 (편집자 시각):** "JCAP referee 는 §3.6 한 줄에서 'this falls below the
Jeffreys threshold for substantial evidence' 로 lead paragraph 시작 가능. 회피
유일한 길은 (a) prior R sensitivity 전수 보고, (b) Δln Z=0.8 을 *결론적
증거* 가 아닌 *consistency check* 로 격하 + 핵심 주장은 ΔAICc=99 (anchor
caveat 명시) 와 4-axis postdiction-허용 구조로 이동, (c) 추가 anchor (P9 dSph
+ P11 NS) 로 Δln Z 강화 시도."

**P8 (synthesizer):** "팀 합의:
1. Δln Z=0.8 단독은 referee 1차 reject 사유로 충분히 약하다.
2. R=3/5/10 sensitivity grid 미보고가 가장 즉시적 fatal weakness. *반드시*
   4점 이상 (R=2/3/5/10 권장) grid 결과를 §3.6 에 표 형태로 추가.
3. fixed-θ 13 vs marginalized 0.8 분리 보고는 정직하나, *어느 쪽이 결론인지*
   명시 부재. 결론은 marginalized 가 baseline (L6 합의) 이므로 §3.6 첫 줄에
   'baseline = marginalized = 0.8' 못박기.
4. 회복 path: 추가 anchor (P9 dSph low-rho gap + P11 NS ultra-high-rho) 가
   *3-regime 예측과 일치* 하면 Δln Z 강화 가능. 일치 안 하면 3-regime 자체
   기각 — Popper falsifier.
5. dynesty 등 full-posterior MCMC 로 Laplace 근사 검증 필요 (Hessian-singular
   영역에서 Δln Z bias 가능)."

---

## 2. 공격선 정리 (reviewer report 예측)

| # | 공격 | severity | 회피 가능? |
|---|------|----------|------------|
| B1 | Δln Z=0.8 < Jeffreys 1.0 ("barely worth mentioning") | CRITICAL | NO (구조적) |
| B2 | R=3/5/10 sensitivity 미보고 (§3.6 *자체* 약속 위반) | CRITICAL | YES (즉시 보고) |
| B3 | Jeffreys-Lindley fragility — wide R 에서 Δln Z<0 가능 | HIGH | partial (R-grid 로 검증) |
| B4 | fixed-θ 13 vs marginalized 0.8 격차 자체가 over-fitting 신호 | HIGH | NO (구조적) |
| B5 | mock 100% false-detection + Δln Z=0.8 결합 = 신호 없음 | CRITICAL | NO (정직 인정) |
| B6 | k=5 (3-regime) k=1 (LCDM) ⇒ Occam 패널티 ~12 정상 — 변호선 | LOW (변호) | — |
| B7 | BMA weight 31% 가 5-model 중 1위 라는 점 미강조 | MEDIUM | YES (강조 변경) |
| B8 | full-posterior MCMC (dynesty/emcee) 미수행 → Laplace bias 위험 | MEDIUM | YES (smoke test 시작) |
| B9 | extra anchor (P9 dSph, P11 NS) 부재 — Δln Z 강화 channel 미시도 | MEDIUM | YES (forecast 가능) |
| B10 | "modest preference" 표현 자체가 Δln Z=0.8 에 과 |  HIGH | YES (격하 framing) |

---

## 3. 정직 판정

- B1, B4, B5 는 **구조적으로 회피 불가능** — paper 본문에서 정직 격하 필요.
- B2, B7, B10 은 즉시 회피 가능 (§3.6 재작성 + R-grid 표 추가).
- B3, B8, B9 는 본 L405 simulations/run.py 에서 *시작* 했고, 실 데이터
  full posterior 는 별도 budget (L406 후속) 에서 완결.

**권고**:
1. §3.6 baseline 진술을 "Δln Z = 0.8 (Jeffreys: barely worth mentioning,
   Bayes factor ≈ 2.2) — 단독으로는 결정적 증거 아님. ΔAICc=99 (anchor
   circularity caveat 명시) + BMA top-rank 31% 와 결합해서만 의미." 로 격하.
2. R={2,3,5,10} sensitivity 표 즉시 추가 (본 L405 run.py 결과).
3. 추가 anchor (P9 dSph, P11 NS) 가 3-regime 예측과 일치 시 Δln Z 강화 측정 —
   불일치 시 3-regime 기각 falsifier 사전 등록 (NEXT_STEP 참조).
4. dynesty/emcee full posterior 후속 (Laplace 검증).

정직 한 줄: marginalized Δln Z=0.8 단독으로는 referee 통과 어려움 — 약점이
며, R-sensitivity 미보고는 §3.6 자체 약속 위반으로 즉시 fatal.
