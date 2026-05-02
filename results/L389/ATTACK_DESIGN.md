# L389 ATTACK DESIGN — BRST Diffeomorphism Gauge Invariance Check

## 주제
n-graviton coupling 의 BRST diffeomorphism gauge invariance 검증.

## 목표
SQMH 작용 ∫ d^4x √(-g) L 이 BRST 변환 (s-operator) 하에서 nilpotent 하게 불변임을 n-graviton 차수까지 확인.

## 방향 (지도 금지)
- BRST 변환의 일반 구조: s = ξ^μ ∂_μ + (gauge ghost 항). 구체적 변환식은 팀이 독립 도출.
- Diffeomorphism gauge symmetry: 일반좌표변환의 무한소 형태로부터 ghost / antighost / Nakanishi-Lautrup 보조장 도입.
- Nilpotency: s² = 0. 이 조건이 작용 불변성과 ghost 변환의 일관성을 동시에 강제.
- n-graviton expansion: g_μν = η_μν + κ h_μν 전개 후 차수별 (n=1,2,3,...) BRST 불변성 확인.
- Ward identity / Slavnov-Taylor identity 와의 관계.

## 8인 팀 자유 분담 (역할 사전 지정 금지)
- 8인이 토의로 자율 분담. 다음 영역이 자연스럽게 등장 예상:
  1. BRST operator 정의 및 nilpotency 증명
  2. SQMH 작용에 대한 무한소 diffeomorphism 변환
  3. Ghost / antighost sector
  4. n=1 (single graviton) 차수 검증
  5. n=2 (two-graviton vertex) 차수 검증
  6. 일반 n 차수 induction
  7. BRST cohomology 및 physical state 조건
  8. 결과 기록 및 모순/예외 추적

## 4인 코드리뷰 (수치 검증 필요시)
- symbolic check (sympy / xAct 류) 사용시 4인 자율 분담 코드리뷰.
- 역할 사전 배정 금지.

## K-기준 (사전 정의)
- K1: BRST operator s 의 nilpotency s² = 0 (off-shell or on-shell 명시).
- K2: ∫ L 의 BRST 변분 = total derivative (boundary 항만 남음).
- K3: n=1, 2 차수 직접 계산 PASS.
- K4: 일반 n 차수 induction 또는 generating-functional 논증 일관성.
- K5: SQMH 추가 항 (ψ field, n0μ coupling 등) 이 BRST 구조를 깨지 않음.

## 산출 형식
- REVIEW.md: 8인 토의 결과 + K1~K5 PASS/FAIL + 정직 한 줄 결론.

## 정직 원칙
- 부분 PASS / 미증명 차수는 정직히 명시.
- 모순 발견 시 결과 왜곡 금지 — 그대로 기록.
