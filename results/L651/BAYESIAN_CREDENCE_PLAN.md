# L651 — Bayesian Credence per Claim (Plan)

> **상태**: PLAN 전용. paper / claims_status / 디스크 edit 0건.
> **출처**: L629 Angle 3 (Bayesian credence per claim) 후속.
> **[최우선-1] 준수**: 수식 0줄. 정량 prior 수치 0개. 등급(★~★★★★★)만.
> **세션 기간**: ~5min, plan 작성 한정.

---

## §1. 카테고리별 Claim Credence 표

### Category 1 — Quantitative claims (paper §5)

| # | Claim (요약) | Credence | 근거 (정성) |
|---|---|---|---|
| 1.1 | a₀ = c·H₀/(2π) PASS_MODERATE (0.71σ) | ★★★★ | 측정값 vs 무모수 예측 0.71σ, multi-session 재현 (L548/L550). 단 1 데이터 포인트 한계로 ★★★★★ 미부여. |
| 1.2 | σ₀ dimensional uniqueness (4πG·t_P 형) | ★★★ | 차원해석은 unique 하나 4π 인자/Planck-time choice 는 convention 의존. paper 본문이 "uniqueness modulo O(1)" 으로 약화 표기 시 ★★★. |
| 1.3 | 6 falsifier preregistration (DESI/Euclid/CMB-S4/ET/SKA/LSST) | ★★★★ | preregistration 자체는 절차적 강함. 단 6 모두 균등 falsifiable 이라는 주장은 ★★★ (CMB-S4/ET 제약력 비대칭). 종합 ★★★★. |

### Category 2 — Limitations claims (paper §6)

| # | Claim | Credence | 근거 |
|---|---|---|---|
| 2.1 | 4 priori path 박탈 정직 기록 (L549/L552/L562/L566) | ★★★★★ | 디스크 audit 기록 존재, 자발적 disclosure. 외부 검증 가능. |
| 2.2 | fabrication 90% (L564) 자발적 disclosure | ★★★★★ | L564 audit 기록 명시, 자기보고지만 외부 reviewer 가 trace 가능. |
| 2.3 | 회의적 0/4 (L578/L587/L588/L589) | ★★★★ | 4세션 모두 0/4 결과 디스크에 존재. 단 "회의적 압박 수준" 자체는 self-rated. |
| 2.4 | hidden DOF 9-13 | ★★★ | 추정 범위 자체가 ±2 brackets. paper 가 "estimated range, not measured" 명시 조건. |
| 2.5 | mass redef 영구 종결 (L582) | ★★★★ | L582 결정 기록 존재, 향후 재시도 시 명시적 위반. ★★★★★ 미부여 이유: "영구" 는 미래 클레임. |

### Category 3 — Paradigm shift claims (paper §7 conditional)

| # | Claim | Credence | 근거 |
|---|---|---|---|
| 3.1 | A3+Time emergent (L610) GR 1.5~2.5/4 | ★★ | conditional, GR 부분점수. paper 가 "tentative" 명시 시 ★★ 유지. |
| 3.2 | Bootstrap (L605) GR 0.8/4 | ★ | <1/4 점수, paradigm shift 핵심 클레임 미달. |
| 3.3 | Self-incompleteness (L618 A8+A11) | ★★ | 메타이론적 클레임, falsifiable 경로 불명. |
| 3.4 | Scope axiom (L625 A0) | ★★ | A0 도입 자체는 ★★★ 가능하나 paradigm shift 함의는 ★★. |

### Category 4 — External verification claims (paper §7)

| # | Claim | Credence | 근거 |
|---|---|---|---|
| 4.1 | multi-session 의무 (L633 H2) | ★★★★ | 절차 규칙으로 정착됨, 디스크 enforce. |
| 4.2 | DR3 (2027 Q2) BCNF protocol | ★★★ | 미래 데이터 의존, 프로토콜 자체는 사전 등록. credence 조건부. |

---

## §2. Credence 등급 기준

- ★★★★★: 거의 확실 (paper 본문 strong claim 가능)
- ★★★★: 높음 (paper 본문 moderate claim 가능)
- ★★★: 중간 (conditional / "subject to" 표현 권장)
- ★★: 낮음 (speculation / "tentative" 명시 필수)
- ★: 매우 낮음 (paradigm shift level / 본문에서 conjecture 표기)

---

## §3. Paper §5/§6/§7 본문 적용 plan (paper edit 0건)

본 L651 은 **plan 전용**. 실제 paper 반영은 후속 세션 (L65X+) 에서 8인 Rule-A 통과 후.

- §5 (Quantitative): 1.1/1.2/1.3 credence 를 본문 footnote 에 등급 형태로만 노출, 수치 prior 0개.
- §6 (Limitations): 2.1~2.5 는 ★★★★~★★★★★ 다수 → 본문 strong language 가능. 단 2.4 (hidden DOF) 는 "estimated range" 표현 강제.
- §7 (Paradigm shift): 3.1~3.4 모두 ★★ 이하 → "conditional", "tentative", "conjecture" 표현 강제. ★ 등급 (3.2) 은 본문에서 *speculative* 명시.
- §7 (External): 4.1 strong, 4.2 conditional → "subject to DR3 release" 명시.

---

## §4. 회의적 압박 + 자기평가 한계

1. **credence 부여 자체가 [최우선-1] 정신적 위반?** — 본 plan 은 등급(★)만 부여, 정량 prior 수치 0개 유지. 수식/파라미터 0. 정신적 위반 위험은 인정하나 본 산출물 범위 내 회피 가능.
2. **credence ≠ 측정값**. paper 의 *self-assessment* 일 뿐 외부 검증 미경유.
3. **Reviewer 신뢰도 ↓ 가능**. self-credence 는 통상 reviewer 에게 무의미. 본문에서는 credence 그 자체보다 **언어 강도(strong/moderate/tentative/conjecture)** 매핑으로 사용.
4. **카테고리 간 비교 금지**. 같은 ★★★ 라도 quantitative 와 paradigm 은 동일 confidence 가 아님.
5. **자기평가 편향**: 저자 본인이 부여한 credence 는 optimism bias 경향. 8인 팀 Rule-A 가 보정.

---

## §5. 8인 Rule-A 의무

본 plan 은 **이론 클레임의 강도 조정** 에 직결됨 → CLAUDE.md 의 "이론 클레임 → Rule-A 8인 순차 리뷰 필수" 적용.

- 8인 팀이 §1 표의 각 등급에 대해 독립적으로 ★ 재평가.
- 등급 차이 ±1 이상 발생 claim 은 본문 반영 보류.
- 8인 합의 도달 후에만 paper §5/§6/§7 언어 강도 조정 (후속 세션).
- 역할 사전 지정 금지. 자율 분담.

---

## §6. 정직 한 줄

본 credence 부여는 paper 의 self-assessment 이며, 외부 reviewer 의 독립 prior 가 아니다 — 본문 반영 시 반드시 "self-assessed" 로 라벨링한다.
