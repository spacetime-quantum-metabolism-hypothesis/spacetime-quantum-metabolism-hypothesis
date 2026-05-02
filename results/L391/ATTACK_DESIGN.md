# L391 ATTACK DESIGN — b/c 비율의 수치 추출 시도 (numerical extraction)

## 배경 (인용만)
- L334 합의: β(σ) = aσ − bσ² + cσ³ 의 a, b, c **수치 priori 도출 불가**. priori 는 σ_0 holographic anchor 1개뿐.
- L352 시도: b 의 1-loop first-principle 도출 → **PARTIAL**. universal 부분 한정 가능, scheme 종속 잔류로 단일 b 숫자 priori 불가.
- L322 BB 3-anchor 수렴 모드: (σ_cosmic, σ_cluster, σ_galactic) ≈ (8.37, 7.75, 9.56) (log10 단위로 추정되는 값, 본 세션 입력 데이터로만 사용).

## L391 임무 (좁고 정직)
**b/c 비율의 *수치 추정 가능 영역*** 만 산출한다. b 절대값·c 절대값 priori 시도 금지 (L352 PARTIAL 경계 존중).

## 공격 대상
- 단일 무차원 비율 r ≡ b/c.
- 보조 비율 q ≡ a/c (필요 시 동시 추출, 단 priori 자유도 증가는 AICc 패널티 명시).
- 결과는 **range / band** 형태로만 보고 (point estimate 단정 금지).

## 입력 (이름만)
1. β(σ) = aσ − bσ² + cσ³ 의 일반 fixed-point 구조 — *수식 자체는 팀 자율 유도*.
2. BB 3-anchor 수치 (8.37, 7.75, 9.56) — 이미 공개된 fit 결과로만 인용.
3. cubic ansatz 의 nontrivial FP 개수가 최대 2 인 사실 (수학적 자명 사실, 지도 아님).

## 가능한 시나리오 (팀이 자율 선택)
- **Sc-A**: 3 anchor 중 2 개를 cubic 의 nontrivial FP 로, 1 개를 trivial 또는 inflection 로 간주.
- **Sc-B**: 3 anchor 모두를 더 높은 차수 ansatz 의 FP 로 간주 → 그러나 본 L391 범위는 cubic 한정 → **거부**.
- **Sc-C**: 3 anchor 중 어느 2 개를 선택할지에 대해 데이터 χ² 비교로 모델 선택.
- 팀은 위 중 어느 시나리오를 채택할지 자유 결정. 시나리오별 r 추정값 비교.

## 금지 사항 (최우선-1)
- L14/L22/L334 의 b, c 형태·부호·크기를 미리 인용 후 "개선" 금지.
- "b/c = anchor 합" 같은 직접 공식 사전 명시 금지 (팀이 도출).
- 특정 anchor 조합 ((cosmic, galactic) vs (cosmic, cluster) 등) 사전 지정 금지.
- regularisation scheme 사전 선택 금지.

## 팀 구성 (역할 사전 지정 금지)
- **8인 이론팀**: 인원수만. 자유 분담. 시나리오 선택, FP 매핑, 비율 추출 식 유도, 오차 전파 자율.
- **4인 코드리뷰팀**: 수치 추출 코드 (`simulations/L391/run.py`) 자율 분담 검토. 역할 사전 배정 없음.

## 산출 기준
- **PASS**: r = b/c 의 단일 시나리오에서 일관된 좁은 band (±20% 이내) 도출. AICc 패널티 명시 후에도 의미 있음.
- **PARTIAL**: r 범위는 추출되나 시나리오 의존 (Sc-A 의 anchor 선택에 따라 결과 변동 ≥ factor 2).
- **FAIL**: cubic ansatz 자체가 3 anchor 와 양립 불가 (예: 3 nontrivial FP 강제 시).

## 과적합 방지
- 추출된 r 을 다른 (이미 fit 된) 데이터에 다시 사용하지 않는다 (circular 방지).
- 본 추출은 *posterior structural diagnostic* 으로만 사용. 새 priori 자유도 1 추가 시 AICc Δ +2 패널티 명시.

## 정직 한 줄
**r = b/c 의 *수치 영역* 추출은 FP 매핑 시나리오 선택 후에만 가능, 그 자체가 1 자유도 추가이므로 priori 절약 효과 ≤ 1.**
