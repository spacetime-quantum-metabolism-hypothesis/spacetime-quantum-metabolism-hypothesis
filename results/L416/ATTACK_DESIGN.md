# L416 ATTACK_DESIGN — 8인팀 reviewer 공격 시뮬레이션

세션 일자: 2026-05-01
대상: paper/base.md §3.4 (RG saddle priori-impossible caveat, L407) + §3.6 (R-grid R=10 collapse caveat, L405)
원칙: CLAUDE.md 최우선-1/2 + Rule-A 8인 자율 분담. 사전 역할 지정 없음.

---

## 0. 전제

L407 결과: 자유 cubic-RG scan 에서 saddle 의 cluster band 확률 1.4%, ±0.10 dex
실험 정밀도 매칭률 0.5%, between-FPs 표준 가정 시 P=0 (구조적). 즉 saddle
*위치 자연성* priori 도출은 "선택된 RG truncation 안에서는" 영구 불가.

L405 결과: toy R-grid 에서 3R Δln Z 가 R=5→R=10 에서 78→15 (5배 collapse).
실데이터 marginalized Δln Z = 0.8 (R=5) — 동일 collapse 패턴이면 R=10 에서
*음수* 가능, Lindley fragility 신호.

본 ATTACK_DESIGN 은 두 caveat 가 **paper 본문에서 빠지거나 약화된 채로**
referee 에게 전달될 경우의 공격 벡터를 8인팀이 자율 분담으로 시뮬레이션
한다.

---

## 1. §3.4 caveat 부재 시 공격 벡터 (RG saddle priori-impossible)

8인팀 자율 분담 — 각자 한 줄 공격 시나리오:

- **A1 (RG/EFT 시각)**: "저자는 cubic β(σ) 의 saddle topology 가 96.8%
  '호환' 된다고 보고하나, *위치* 가 cluster band 에 떨어질 priori 확률은
  1.4% — RG 자연성 주장의 핵심은 *위치* 이며 topology 호환성은 *허용 조건*
  에 불과. 저자는 두 개념을 혼동했다." → **REJECT-기반-수치오해**.
- **A2 (Bayesian model selection 시각)**: "saddle 위치가 *외부 anchor* 로만
  결정된다면, three-regime 모델의 'priori 구조' 주장은 anchor 데이터 의존
  postdiction 이며, §3.5 의 mock injection FDR 100% 와 합쳐지면 모델
  evidence 의 *대부분* 이 anchor 적합 자유도에서 옴." → **fit-vs-prediction**
  공격.
- **A3 (philosophy of science 시각)**: "RG 자연성은 통상적으로 *coupling
  constant 의 차원분석적 자연스러움* 을 의미. 본 saddle 의 위치는 [a, b, c]
  3-coupling 공간의 lower-dim slice — measure-zero 사실상 fine-tuning."
  → **fine-tuning** 공격.
- **A4 (alternative theory advocacy)**: "monotonic σ(ρ) 가 Δln Z = -1.84
  (paper §3.4 자체 인용) 로 약 선호되는데, 비단조성 모델은 saddle 위치를
  free-parameter 로 추가하면서 Δln Z 0.8 에 그침 — Occam 원리에 반함."
  → **Occam-violation** 공격.
- **A5 (data systematics 시각)**: "cluster anchor (σ₀=7.75) 가 A1689
  single-source dominance 59.7% (§3.5 자체 인용) — saddle 위치가 anchor
  point 와 일치하는 것은 by construction. 이를 'RG topology 발견' 으로
  포장." → **anchor-circularity** 공격.
- **A6 (referee politics)**: "PRD Letter 진입 조건 (Q17 priori 도출) 미달성
  은 base.md L692 자체 인정. caveat 약화 시 'PRD 진입조건 위반 + 위장' 으로
  추가 죄목." → **double-violation** 공격.
- **A7 (literature comparison)**: "Wetterich 2008 Wilsonian truncation 1-loop
  결과는 cubic β(σ) 가 *생성되지 않음*. L407 가 가정한 cubic 형태 자체가
  ad hoc — RG 동기 약화." → **truncation-arbitrariness** 공격.
- **A8 (formal proof demand)**: "P=0 결과는 '표준 between-FPs 가정' 하 도출.
  저자는 이 가정의 정당성을 증명하지 않음 — 모든 RG flow 가 IR<saddle<UV
  를 만족하는가? holographic-RG, gradient-flow 등 비표준 cases 는?" → **assumption-coverage**
  공격.

### 공격 강도 종합

| 벡터 | 심각도 | 회피 비용 (caveat 추가) |
|------|--------|--------------------------|
| A1   | 매우높음 | "topology vs 위치" 분리 한 줄 |
| A2   | 높음   | postdiction 인정 (이미 §3.4) + "외부 anchor" 명기 |
| A3   | 중간   | fine-tuning 인정 한 줄 |
| A4   | 높음   | Δln Z = -1.84 정직 보고 (이미 §3.4) |
| A5   | 매우높음 | A1689 dominance 인정 (이미 §3.5) |
| A6   | 치명   | PRD 진입 불가 + JCAP 타깃 명기 (이미 L692) |
| A7   | 중간   | future work — Wetterich/EFT (이미 L407 NEXT_STEP) |
| A8   | 중간   | 가정 명기 + holographic 향후 작업 |

**caveat 부재 시 패턴**: A1+A5+A6 결합 → "위장된 fit, PRD 진입 자격 미달"
판정. desk-reject 가능.

**caveat 명시 시 패턴**: A2/A4/A5 는 본문 인정으로 무력화. A1/A8 은 한 줄
caveat 로 차단. A3/A7 은 future work 로 격하. → 정직한 phenomenology 로
JCAP 통과.

---

## 2. §3.6 caveat 부재 시 공격 벡터 (R-grid R=10 collapse)

- **B1 (Bayesian 정통)**: "marginalized Bayes factor 는 prior width 에 강하
  의존 (Lindley paradox). R=5 단일값 만 보고하면 *cherry-picked prior* 의심.
  R=10 에서 collapse 한다면 결론 reversal 가능." → **prior-cherry-pick** 공격.
- **B2 (replicability 시각)**: "L405 toy 결과 (R=10 에서 78→15 collapse)
  가 paper 부록에 언급되지만 본문 §3.6 에는 R=5 단일값만. 본문/부록
  inconsistency." → **본문-부록 불일치** 공격.
- **B3 (referee A 의 흔한 요구)**: "wide-prior limit 에서 Δln Z 의 점근 거동
  을 보여라. R={2,3,5,10,20,50} 보고 필수." → **요구사항 미충족** 공격.
- **B4 (model-comparison 통계학자)**: "R=5 의 Δln Z = 0.8 은 'inconclusive'
  (Kass-Raftery 1995 |Δln Z|<1 = barely worth mentioning). R=10 collapse
  시 음수 가능 — 결론은 'data does not support 3-regime'." → **결론-반전**
  공격.
- **B5 (Lindley paradox 명시 인용)**: "Lindley 1957 — wide-prior 에서
  Bayesian 은 항상 단순 모델을 선호. paper 가 이를 모르거나 숨김." → **고전결과-무지**
  공격.
- **B6 (메타-방법론)**: "BMA weight 31% (R=5) 도 R 의존 — R=10 에서 monotonic
  weight 가 dominant 가 될 수 있음. BMA 자체가 prior 의존이므로 R 변경 시
  포지셔닝 reversal." → **BMA-fragility** 공격.
- **B7 (sample-size 시각)**: "anchor 8점 (toy) / 실데이터 anchor 수도 적음.
  small-N 에서 R-sensitivity 가 큰 것은 정상이지만 paper 는 이를 'robust'
  로 잘못 표현." → **small-N-robustness** 공격.
- **B8 (dynesty vs Laplace)**: "L405 dynesty smoke 가 Laplace 대비 +4.27
  ln Z gap. R=5 의 0.8 도 Laplace 산출이라면 method 변경 시 [-3, +5] 범위
  변동 — 결론 fragile." → **method-dependence** 공격.

### 공격 강도 종합

| 벡터 | 심각도 | 회피 비용 |
|------|--------|------------|
| B1   | 매우높음 | R={2,3,5,10} 모두 본문 보고 |
| B2   | 매우높음 | 본문-부록 일관 |
| B3   | 높음    | R-grid 표 본문 |
| B4   | 치명    | "inconclusive" 정직 인정 |
| B5   | 높음    | Lindley paradox 명시 인용 |
| B6   | 중간    | BMA weight R-의존 한 줄 |
| B7   | 중간    | small-N caveat |
| B8   | 중간    | method dependence 한 줄 |

**caveat 부재 시 패턴**: B1+B2+B4 결합 → "결론 fragile, 본문이 부록 결과
숨김" 판정. major revision 또는 reject.

**caveat 명시 시 패턴**: R-grid 전체 보고 + collapse 인정 → "정직한 fragility
disclosure" 로 referee 안심.

---

## 3. 종합

§3.4 와 §3.6 caveat 부재 시 desk-reject 또는 major-revision 위험 매우 높음.
caveat 명시 비용은 한 줄 ~ 표 1개 수준이며 paper 의 정직성 narrative 강화.

---

## 4. 8인팀 합의 (만장)

두 caveat 본문 *명시 강화*. §3.4 — saddle 위치 자연성 priori 도출 영구 불가
+ 외부 anchor 의존 명기. §3.6 — R={2,3,5,10} 모두 본문 표, R=10 collapse 인정.
