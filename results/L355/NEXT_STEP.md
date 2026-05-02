# L355 NEXT STEP — 우선순위가 정해진 다음 행동

## 즉시 다음 단계 (이번 라운드 직후)

### N1. SQT 흐름 변수 사전(辭典) 한 페이지 정리
- 본 프로젝트 L0/L1 공리에서 사용되는 흐름 변수(예: n₀μ 곱, 유입속도 v(r), 정보 밀도) 들의 차원과 RG 가중치를 한 표로 묶는다.
- 산출 위치: results/L355/SQT_DICT.md (다음 라운드).
- 시간 예산: 책상 수준 1세션.

### N2. AS NGFP truncation 후보 3종 선정
- (a) Einstein–Hilbert + 최소결합 scalar — Percacci–Vacca line.
- (b) Einstein–Hilbert + 비최소결합 ξφ²R — Eichhorn–Held type.
- (c) f(R) + scalar — Falls–Litim 계열.
- 각 truncation에서 **NGFP 존속 여부 + relevant direction 수**만 인용표로 정리. 산출: results/L355/AS_TRUNC_TABLE.md.

### N3. 차원 매칭 표 (Step A)
- N1 × N2의 외적표 (SQT 변수 → 각 truncation의 (g,λ,ξ) 좌표).
- 매칭 가능/불가능을 1셀씩 표시. 매칭 가능한 셀이 0이면 즉시 KILL → AS와의 사상 자체 폐기.

## 중기 단계 (조건부 진행)

### N4. Cassini/GW170817/BBN 게이트 사전 통과 확인
- N2의 (b),(c)에서 IR로 흘러나온 effective action의 GW c_T 보장 여부를 문헌 기준으로 한 줄씩 확인.
- 본 프로젝트의 disformal/screening 재발방지 로그(CLAUDE.md) 와 모순 없는지 cross-check.

### N5. Step D 단일 변수치환 시도
- N3에서 매칭 가능 셀이 1개라도 살아있을 때만 진행.
- 단 한 번의 치환만 허용. 두 번째 변환 시도 시 즉시 라운드 종료.

### N6. Step E 함수족 포함 관계
- AS IR effective action이 생성 가능한 dark energy ρ(z)/H(z) 함수족을 한 줄 형식으로 적고, L33 챔피언 g(z) 가 그 안에 포함되는지만 본다. 숫자 fit 금지.

## 정책 게이트

- 8인 팀이 N1을 자율 분담으로 작성 (역할 사전 지정 금지).
- 4인 코드리뷰는 본 라운드에서 코드 산출이 없으므로 N5에서 처음 코드가 등장할 때 호출.
- N3에서 매칭 셀 0이면 본 라인은 즉시 동결 (D 등급), 다른 UV 후보(스트링/CDT/그룹필드) 라인을 다음 라운드로 옮긴다.

## 비-진행 사유 명시 (정직)
- 본 라운드에서는 RG 미분방정식이나 FRGE 적분을 새로 푸는 작업을 하지 않는다 — 이는 별도 라운드에서 코드 4인 리뷰와 함께 시작.
- AS NGFP 측 임계 지수는 외부 문헌 인용에 의존. 자체 재계산은 비범위.

## 위험 신호 (즉시 정지 트리거)
- SQT 측에서 흐름 변수가 RG 차원에서 모호(차원 가중치 미정의) 하게 남으면 N1에서 정지하고 공리 측 보강 라운드로 회귀.
- AS 측 (b),(c) truncation에서 NGFP가 외부 최근 문헌에서 사라진다는 근거가 발견되면 즉시 D 등급.
