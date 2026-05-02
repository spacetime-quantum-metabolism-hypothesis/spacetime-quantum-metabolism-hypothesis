# L390 REVIEW — Conformal Anomaly Trace T^μ_μ (n field) vs Λ_eff

## 1. 실행 상태

- ATTACK_DESIGN.md 작성 완료 (방향만 제공, 수식 0줄 — 최우선-1 준수).
- 8인 이론 도출 / 4인 수치 검증 미실행 (본 세션은 설계 + 사전 분석 단계).
- 후속 세션에서 팀 토의 + toy 실행 예정.

## 2. 사전 분석 (팀 도출 결과 아님 — 일반 curved-space QFT 상식 범위)

### 2.1 차원 및 스케일 추정 (K1, K3 사전 sanity)

n 장 anomaly 는 통상 곡률 제곱 invariant 와 H^4 로 스케일.
FLRW today: H_0 ≈ 2.2e-18 s^-1 → ℏ H_0^4 / c^3 ~ O(10^-52) J/m^3.
ρ_Λ,obs ≈ 5.4e-10 J/m^3.

**사전 비율**: anomaly / Λ_obs ~ 10^-42 수준 (amplitude coefficient O(1)
가정 시).

### 2.2 K-test 사전 판정 (팀 도출 후 재확인 필요)

| Test | 사전 예측 | 비고 |
|------|----------|------|
| K1 차원   | PASS 예상 | 표준 trace anomaly 형식 |
| K2 scheme | PASS 예상 | leading curvature term 은 scheme 무관 (Duff 1994) |
| K3 FLRW   | ~10^-52 J/m^3 | curvature^2 dominant |
| K4 Λ 비교 | 10^-42 비율 | negligible |
| K5 SQMH   | **미정** | 8인 팀 독립 도출 후 판정 |

### 2.3 핵심 함의

- **K4 negligible 시**: n 장 conformal anomaly 는 관측 dark energy 의
  amplitude source 가 **될 수 없음**. Λ_eff 는 다른 채널 (metabolic
  소멸 항, vacuum condensate, IDE 결합) 에서 와야 함.
- **K4 borderline 시**: amplitude coefficient (a_2 계수) 의 SQMH 특이값
  이 필요 — fine-tuning 문제 부활 위험.

## 3. 위험 요소

- **R1 scheme dependence**: subleading term (□R 등) 은 scheme 의존.
  total derivative 라 적분 시 boundary 만 기여 — FLRW 무한 부피에서
  drop 가능. 팀 토의에서 명시 필요.
- **R2 spin 가정**: n 이 scalar 인지 effective composite 인지에 따라
  anomaly 계수 (Duff Table 1) 가 달라짐. 사전 지정 금지 — 팀 도출.
- **R3 background curvature**: Minkowski 가정 시 anomaly = 0
  (Capper-Duff). FLRW 또는 Schwarzschild 배경 필수.
- **R4 SQMH 부호**: psi^n 소멸 항의 부호와 anomaly trace 부호의 정합성
  은 SQMH unitarity / 에너지 양수성 조건. 미달 시 이론 자체 위협.

## 4. 다음 세션 To-Do (실행 미정)

1. 8인 팀 자유 토의 — n 장 spin, coupling, regularization 자율 선택.
2. 4인 코드 toy — K1–K4 numeric.
3. K5 SQMH 정합성 판정 + Λ_eff 채널 영향 정량.
4. base.fix.md 갱신 (anomaly 가 Λ 채널과 무관하면 명기).

## 5. 정직 한 줄

n 장 conformal anomaly 의 FLRW today 추정 amplitude 는 ρ_Λ,obs 보다 약
10^42 배 작아 dark energy 의 dominant source 가 될 수 없을 가능성이 높으며,
정확한 K-판정은 8인 팀 독립 도출 후 재확인 필수.
