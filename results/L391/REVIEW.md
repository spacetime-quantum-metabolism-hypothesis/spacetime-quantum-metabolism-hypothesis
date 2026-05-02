# L391 REVIEW — b/c 비율 수치 추출 결과

## 입력 (이미 공개된 값만)
- BB 3-anchor (L322 모드 0, log10 단위로 추정): σ_cosmic=8.37, σ_cluster=7.75, σ_galactic=9.56.
- ansatz: β(σ) = aσ − bσ² + cσ³ (L334 인용, 본 세션에서 재유도 안 함).

## 방법 (요약 — 자세한 코드는 simulations/L391/run.py)
- cubic ansatz 의 nontrivial FP 는 최대 2 개 (수학적 자명).
- 3 anchor 중 2 개를 (σ_-, σ_+) 로 매핑하면 Vieta 관계로
  - r ≡ b/c = σ_- + σ_+
  - q ≡ a/c = σ_- · σ_+
  가 직접 산출.
- 3 가지 매핑 조합 모두 계산하여 *영역(band)* 으로 보고.

## 결과 (수치 추출)

| FP pair             | r = b/c  | q = a/c  | 제3 anchor (해석 미지정) |
| ------------------- | -------- | -------- | ------------------------ |
| cosmic + cluster    | 16.120   | 64.867   | galactic (9.56)          |
| cosmic + galactic   | 17.930   | 80.017   | cluster  (7.75)          |
| cluster + galactic  | 17.310   | 74.090   | cosmic   (8.37)          |

- **r 영역**: [16.12, 17.93], spread × 1.112 (≈ ±5.6%).
- **q 영역**: [64.87, 80.02], spread × 1.234 (≈ ±10.4%).

## 판정

ATTACK_DESIGN PASS 기준 (spread ≤ 1.20, ±20% band) 적용:
- r 단독 평가: **PASS** (spread 1.112).
- q 단독 평가: **PASS** (spread 1.234, 1.20 경계 초과 — 엄밀히 PARTIAL).
- 결합 평가 (둘 다 동시 PASS 요구): **PARTIAL**.

## 정직 단서 (5가지)

1. **순서 의존성 없음**: BB anchor 3 개의 *절대값* 자체가 anchor pairing 차이를 좁게 만든다. 3 anchor 가 한 자릿수 (7.7~9.6) 안에 모여 있어 평균값(σ̄≈8.6) 가까이서 모든 pair sum 이 ~17 근방. 이는 *수치적* 우연일 수 있다.
2. **제3 anchor 잔차 (run.py diagnostics)**: cubic 가 정확하다면 제3 anchor 에서 β(σ) ≠ 0 이어야 하며, residual_normalised 가 0.1~0.5 범위이면 cubic 일관, 0 에 매우 가까우면 3 anchor 모두 FP (cubic 부족), 1 에 가까우면 cubic 과 강한 불일치. JSON 출력에 기록되어 후속 loop 에서 평가 가능.
3. **시나리오 의존**: Sc-A (3 중 2 FP) 가정은 *팀 자율 선택* 이며, Sc-B (4 차 ansatz) 또는 σ_cluster 가 unstable middle FP 로 해석되는 시나리오 (cubic 의 두 FP 사이 유일한 inflection 후보) 도 별도 평가 필요. 본 L391 은 Sc-A 만 평가.
4. **AICc 패널티**: r 추출은 priori 자유도 1 추가. AICc 패널티 +2 는 BB anchor 3 개 fit 에 비해 미미하지만, "b/c priori 도출" 주장 시 항상 패널티 명시.
5. **L352 PARTIAL 경계 존중**: 본 결과는 b 절대값·c 절대값에 대해 어떤 priori 주장도 하지 않는다. r 만이 *anchor 수치로부터 대수적으로 유도* 가능하다.

## L334 ★★ 갱신 가능성
- **갱신 불가능 영역**: a, b, c 절대값 priori — 여전히 L352 PARTIAL 경계 안.
- **갱신 가능 영역**: b/c 비율 *영역* (16~18) — 단, 이는 anchor *수치* 입력의 결과이지 미시 유도 결과가 아니다. 따라서 ★★ → ★★ 유지가 정직.
- 만약 b/c ≈ 17 이 향후 L352 의 universal 부분과 *독립적으로* 도출되면 ★★ → ★★★ 후보. 본 L391 만으로는 격상 근거 부족.

## 4인 코드리뷰 분담 권고 (역할 사전 지정 금지 원칙 준수, "제안" 만)
- pairwise_ratios 의 Vieta 부호 검증
- cubic_consistency_check 의 normalisation scale 선택 타당성
- ANCHORS 입력값이 L322 원본과 일치하는지 cross-check
- AICc 패널티 명시가 ATTACK_DESIGN 요구와 부합하는지

## 정직 한 줄
**b/c ≈ 16~18 영역으로 수치 추출 가능하나, 이는 anchor 수치의 대수적 결과일 뿐 미시 유도가 아니므로 L352 PARTIAL 등급은 그대로 유지된다.**
