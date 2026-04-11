# L2 Acceptance Conditions (Pre-registered)

> 사전 선언 (2026-04-10). L2 재설계 후보는 아래 4 조건 중 **2 개 이상 만족** 시
> 채택. 0~1 개 만족 → 폐기 → Path F 재확인.

---

## C1 — Cassini 내재 통과

**조건**. 후보 라그랑지안이 `|γ−1| < 2.3e−5` (Cassini Bertotti+ 2003) 을
**Vainshtein 사후 주입 없이 내재적으로** 만족.

**근거**. Phase 3.6 B1 에서 unscreened universal coupling `β ≈ 0.107` 이
Cassini 984× 위반. B2 Vainshtein 은 원래 라그랑지안에 없는 cubic Galileon
추가 항이므로 "zero free parameter" 주장 위반.

**판정**. 수식 유도 (정적 PPN γ 계산) + 수치 검증 (β 또는 ξ posterior 값 대입).

**불가**. "적절한 cutoff", "모델 의존적 screening", "linearized 가정" 등
사후 변명 금지.

---

## C2 — Phase 3 posterior 자동 만족

**조건**. Phase 3 joint MCMC best-fit (β ≈ 0.107, median) 이 **수정 없이**
C1 을 자동 만족.

**근거**. 데이터에 맞는 파라미터 값이 Cassini 한도도 동시 만족해야만 이론이
"실제로 작동" 함. β 값이 데이터 vs 태양계에서 다르면 단일 이론 아님.

**판정**. `β_data = 0.107 → |γ−1|_predicted < 2.3e−5` 해석적 증명. β 대체
파라미터 사용 시 동일 논리로 평가.

---

## C3 — 보존 법칙 + Bianchi

**조건**. `∇_μ T^μν = 0` (매질 + 스칼라 부문 총합) 이 Bianchi identity
`∇_μ G^μν = 0` 과 동시 성립.

**근거**. base.bad.1.md §1 에서 Planckton 가설이 "텐서 보존 법칙 위반" 으로
기각됨. SQMH 는 이 비판을 피해야 정합성 유지.

**판정**. 수식 수준에서 4 divergence 직접 계산.

**허용**. 매질↔스칼라 에너지 교환은 허용 (IDE 일반). 단 총 T^μν 는 conserved.

---

## C4 — w_a<0 구조적 자연성

**조건**. 관측된 `w_a < 0` (DESI+Planck+DES-all, arXiv:2507.09981) 이 후보의
**구조적 필연** or **자연 범위** 로 나옴. Ad-hoc λ 튜닝 금지.

**근거**. Phase 1/2/3 에서 V_mass 는 `w_a > 0` 구조적, V_RP freezing 은
`w_a < 0` 이나 데이터에 의해 LCDM 한계로 수렴, V_exp 는 특정 λ 범위만
`w_a < 0`.

**판정**. (a) 구조적 필연 (모든 자연 파라미터에서 `w_a<0`) → 강 통과. 
(b) 자연 범위 (베이지안 prior 범위 절반 이상에서 `w_a<0`) → 약 통과.
(c) 특정 점에서만 → 실패.

**약 통과 이상**. C4 ✓.

---

## 최종 판정 매트릭스

| 합계 | 판정 |
|---|---|
| 4/4 | 강 채택 → Phase 5 우선 진입 |
| 3/4 | 채택 → R3 수식 유도 후 추가 판단 |
| 2/4 | 조건부 채택 → 누락 조건 명시 |
| 0~1/4 | **폐기** |

모든 후보 0~1 → Path F 재확인 → `paper/negative_result.md` 부록 추가.
