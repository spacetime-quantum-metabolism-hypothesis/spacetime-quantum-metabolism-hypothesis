# L389 REVIEW — BRST Diffeomorphism Gauge Invariance Check

세션: L389 독립
일자: 2026-05-01
주제: n-graviton coupling 의 BRST diffeomorphism gauge invariance 검증

---

## 1. 8인 팀 자율 분담 (토의 자연 발생)

토의 초기 라운드에서 다음 분담이 자연스럽게 형성되었다 (사전 지정 없음):

- A: BRST operator s 정의, ghost c^μ / antighost b_μ / NL field B_μ 도입
- B: nilpotency s² = 0 off-shell 증명 (ghost 비선형 변환 포함)
- C: SQMH 작용 √(-g)(R/16πG + L_ψ + L_metabolism) 의 diffeomorphism 무한소 변분
- D: graviton 전개 g = η + κh, ghost 전개, gauge fixing term L_gf = -(1/2α)(∂^μ h_μν − ½ ∂_ν h)²
- E: n=1 차수 직접 계산 (single h, single c)
- F: n=2 차수 직접 계산 (hh, hc∂c, bc∂h cross-term)
- G: 일반 n induction — Ward / Slavnov-Taylor identity Z[J,K] 관점
- H: SQMH 고유 항 (ψ field, n0μ source) 의 BRST 일관성, 결과 통합

---

## 2. 도출된 구조 (팀 독립 유도, 형태만 기록)

- BRST 변환은 일반 좌표변환의 ghost 화 형태로 닫힘 (Kugo-Ojima 표준 구조와 일치).
- Gauge fixing + ghost 항은 s-exact (s Ψ form) 으로 표현 가능 → 물리적 cohomology 보존.
- SQMH 추가 항 L_ψ, L_metabolism 은 모두 scalar density 로 구성 → 일반좌표변환 covariant.
- 따라서 BRST 변분은 표준 Einstein-Hilbert 부분과 동일 패턴으로 처리됨.

---

## 3. K-기준 판정

| K | 내용 | 판정 | 비고 |
|---|------|------|------|
| K1 | s² = 0 nilpotency | PASS | off-shell, ghost 비선형 변환 사용. 표준 결과 |
| K2 | ∫ L 의 BRST 변분 = total derivative | PASS | scalar density 구조로부터 직접 |
| K3a | n=1 차수 직접 계산 | PASS | s h_μν = ∂_μ c_ν + ∂_ν c_μ + O(κ) → quadratic 작용 변분 boundary |
| K3b | n=2 차수 직접 계산 | PASS | cubic vertex h h ∂c 항 cross-term 정확히 상쇄 (de Donder gauge) |
| K4 | 일반 n induction | PASS (구조적) | Z[J,K] BRST master equation (S, S) = 0 만족. Diffeomorphism 의 well-known 결과 재확인 |
| K5 | SQMH 고유 항 BRST 일관성 | PASS | L_ψ, L_metabolism 모두 covariant scalar density. ψ field 가 BRST singlet (s ψ = c^μ ∂_μ ψ) 이면 닫힘 |

전 항 PASS.

---

## 4. 잠재적 위험 / 정직 기록

- K4 의 "일반 n" 은 직접 그래프 계산이 아닌 master equation 구조 논증. 4-graviton 이상 직접 vertex 검증은 본 세션 범위 외.
- ψ field 의 BRST 변환을 c^μ ∂_μ ψ 로 가정 — 이는 ψ 가 scalar 일 때만 성립. ψ 가 다른 표현 (spinor, 보조장 등) 이면 변환 규칙 재정의 필요.
- Anomaly 가능성 (one-loop 이상) 은 본 tree-level 분석에서 다루지 않음. 4d diffeomorphism 의 경우 표준적으로 anomaly-free 이나, SQMH ψ sector 의 측정 (measure) anomaly 는 별도 검증 권장.
- L_metabolism 의 명시적 형태가 covariant scalar density 라는 가정에 의존. 만약 명시적 시간 의존성 (preferred frame) 이 들어가면 diffeomorphism 깨짐.

---

## 5. 정직 한 줄

**SQMH 작용은 ψ 가 scalar 이고 L_metabolism 이 covariant scalar density 인 한 BRST diffeomorphism gauge invariance 를 n-graviton 모든 차수에서 보존한다 — 단, 이는 표준 GR 의 well-known 결과의 재확인이며, SQMH 고유의 새로운 보장은 ψ sector 의 BRST singlet 가정에 의존한다.**
