# L402 — 8인팀 reviewer attack 설계 (§5.2 Λ origin circularity)

세션 일자: 2026-05-01
대상: paper/base.md §5.2 ρ_q/ρ_Λ = 1.0000 *exact* PASS_STRONG 광고.
원칙: CLAUDE.md [최우선-1, 2] — 방향만 제공, 8인팀 자율 토의 시뮬.

## 0. 임무 framing

PRD/JCAP reviewer 가 §5.2 를 읽고 reject/major-revision 으로 가게 만들 가능 공격선
을 사전 발굴한다. 8명은 역할 사전 지정 없이 자유 발언, 토의 중 자연 분업.

---

## 1. 8인팀 토의 시뮬 (요약)

**P1 (관측우주론):** "ρ_q/ρ_Λ = 1.0000 은 측정 정밀도가 아니라 *대수 항등식*
이다. n_∞ 가 ρ_Λ_obs / (ε/c²) 으로 정의되고 다시 ρ_q = n_∞·ε/c² 로 곱하면
당연히 1.0000 이 나온다. 이건 *prediction* 이 아니라 *self-consistency check*
조차 못 된다 — 차원 검토일 뿐."

**P2 (장이론):** "동의. 이는 c² 단위 변환이 자기 자신과 같다는 것에 불과하다.
물리적 내용이 0 이라는 결정적 증거: 어떤 ε 값을 넣어도 1.0000 이 그대로 유지됨.
ε 가 물리상수가 아닌 *fitting handle* 이라는 뜻이다."

**P3 (통계):** "Bayesian 관점에서 prior = posterior 인 update. KL divergence 0.
이건 evidence 가 아니다. abstract/README 에 'PASS_STRONG' 으로 광고하면 reviewer
report 1번 항목으로 fatal 지적 들어온다. 'circularity caveat 명시' 도 약함 —
*claim 자체를 strong status 에서 제외* 하라는 요구가 정상."

**P4 (현상론):** "단, 변호 가능 측면 — *order-of-magnitude* 일치는 trivial 아님.
n₀μ 차원 추정이 10⁻²⁷ kg/m³ 영역에 *떨어진다는 것* 자체는 60-자릿수 vacuum
catastrophe 대비 의미있다. 문제는 광고 방식: '1.0000 exact' 가 아닌 '~10⁰
order' 로 환원해야 한다."

**P5 (수리물리):** "Schwinger-Keldysh KMS 균형으로부터 n_∞ 를 *독립* 도출하는
경로가 존재하는지가 핵심이다. Hubble H₀ + Planck-scale dynamics + 균형조건만으로
n_∞ 가 나오면 ρ_Λ 는 진짜 prediction 이 된다. 현재 axiom 3 형태는 ρ_Λ_obs 가
boundary condition 으로 들어가 있어 그런 도출이 *가능했던* 것을 가렸다."

**P6 (철학·방법론):** "Popper 기준에서 unfalsifiable 위험. ρ_Λ_obs 가 input 인
한 어떤 측정값으로 ρ_Λ 가 바뀌어도 1.0000 으로 맞춰진다 — falsifier 없음.
'rho_q/rho_Lambda = 1.0000' claim 은 falsifiable claim 의 모양을 가졌으나 실제
로는 항진명제다."

**P7 (편집자 시각):** "PRD Letter 는 *predict, don't postdict* 정책. JCAP 도
referee 1번이 'circularity = no novel content' 로 reject 가능. abstract level
에서 빼고 본문 §5.2 로 강등 + 'consistency check' 로 명명 변경 권고.
'caveat 명시' 정도로는 부족."

**P8 (synthesizer):** "팀 합의:
1. *대수적으로* circular — 회피 불가능 (현재 axiom 3 구조에서).
2. *물리적으로* trivial 은 아님 — 차원이 60자리 catastrophe 영역이 아닌 데
떨어진다는 점은 의미.
3. **광고 강등 필요**: 'PASS_STRONG ρ_q/ρ_Λ=1.0000' → 'CONSISTENCY_CHECK
order-unity dimensional match'.
4. **회피 path 존재**: H₀+KMS 독립 도출 시도 (NEXT_STEP 참조).
5. 회피 실패 시 §5.2 caveat *강화* 필수 — 단순 명시가 아닌 abstract/README/
claims-table 3 곳에서 동시 강등."

---

## 2. 공격선 정리 (reviewer report 예측)

| # | 공격 | severity | 회피 가능? |
|---|------|----------|------------|
| A1 | 1.0000 exact 는 단위변환 항등식 | CRITICAL | NO (구조적) |
| A2 | ε 자유도 → ρ_q 가 ρ_Λ_obs 에 잠금 | CRITICAL | NO |
| A3 | Bayesian KL update = 0 | HIGH | NO |
| A4 | Popper falsifier 결여 | HIGH | NO |
| A5 | abstract 광고가 정직 한계 (caveat 명시) 와 위계 충돌 | HIGH | YES (강등) |
| A6 | order-unity match 자체는 trivial 아님 인정 | LOW (변호) | — |
| A7 | KMS / H₀-only 독립 도출 부재 | MEDIUM | YES (시도 가치) |
| A8 | rho_Lambda_obs 가 input 인 다른 표현 (n₀μ = ρ_P/4π) 도 결국 같음 | MEDIUM | NO |

## 3. 정직 판정

A1, A2, A3, A4, A8 는 **현재 axiom 3 구조에서 회피 불가능**. A5, A7 은 회피
가능 (광고 강등 + 독립도출 시도).

**권고**: §5.2 caveat 를 *강화* (abstract level 추가) + ρ_q/ρ_Λ=1.0000 을
PASS_STRONG 에서 제외 + NEXT_STEP 의 H₀+KMS 독립 도출 시도.
