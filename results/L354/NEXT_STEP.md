# L354 NEXT STEP — 8인 + 4인 자율 진입 가이드

## 0. 진입 전 체크

- [ ] `ATTACK_DESIGN.md` 정독 완료.
- [ ] CLAUDE.md 최우선-1, -2 (지도 금지, 팀 자율 도출) 숙지.
- [ ] 이전 세션 (L353 이하) σ_0 수치/유도 경로를 의도적으로 차단.

## 1. 8인 팀 (Rule-A, 이론 도출)

### Step 1. 자유 토의 — 문제 정의 합의 (역할 사전지정 금지)
- Wetterich exact equation 의 어떤 형태를 출발점으로 삼을지 자율 합의.
- σ_0 가 어떤 operator 의 결합으로 정의되는지 SQMH 공리 (L0/L1, 대사항) 에서 자율 재유도.
- truncation ansatz 후보 나열 — LPA, LPA', derivative expansion, vertex expansion 등 중 어느 조합을 시도할지 자율 결정.

### Step 2. β-function 도출
- 합의된 truncation 에서 σ_0 의 β-function 을 자율 유도.
- 도출 과정에 Command 또는 외부 힌트 의존 금지. 문헌 인용은 허용 (Wetterich 1993, Reuter, Berges-Tetradis-Wetterich 2002 등 표준 리뷰).

### Step 3. 비교 axis 결정
- perturbative 1-loop (또는 2-loop) 를 어떤 scheme (MS-bar, ζ-function 등) 로 계산할지 자율 결정.
- 비교 지표 (fixed-point 위치, IR σ_0, UV scaling, anomalous dimension η) 자율 선택.

### Step 4. 수치 시뮬레이션 명세 작성
- ODE 변수, 적분 경계 (k_UV, k_IR), 초기조건, 단위 무차원화 방식 자율 명세.
- 4인 코드리뷰 팀에 명세 전달.

### Step 5. 결과 해석 + 8인 합의
- Wetterich 결과 vs perturbative 결과 차이의 물리적 의미 해석.
- truncation artefact 검증 (truncation 차수 변화에 대한 σ_0 robustness).
- AICc 패널티 적용 후 최종 truncation 채택.
- `REVIEW.md` 에 8인 서명.

## 2. 4인 코드리뷰 팀 (Rule-B, 코드 검증)

### Step A. 자율 분담 (사전지정 금지)
- 8인 팀 명세를 받고 자율적으로 검토 영역 분담.
- 데이터 로딩 / β-function 코드 / ODE solver / 단위계 / fixed-point 검색 / 시각화 등을 자율 분배.

### Step B. 표준 검증
- Gaussian 한계 (자유 이론) 에서 β=0 재현 확인.
- 알려진 toy model (예: O(N) scalar) 로 코드 sanity check — 문헌 fixed-point 와 일치 확인.
- ODE solver 의 stiff 영역 (fixed-point 근방) 안정성 검증.
- 병렬 실행 (`spawn` Pool, 워커 스레드 1로 고정) 확인.

### Step C. CLAUDE.md 재발방지 적용
- numpy 2.x `np.trapezoid` 만 사용.
- 유니코드 print 금지 (변수명 ASCII).
- ODE 폭주 시 수치값 보고 금지 — 분기 처리 또는 해석 toy 대체.
- 식별자 공백 금지.

### Step D. 코드 승인
- 4인 자율 합의 후 `REVIEW.md` 에 코드 승인 섹션 서명.
- 버그 발견 시 8인에게 회신, 8인은 재계산.

## 3. 종료

- `REVIEW.md` 의 8인 합의 + 4인 코드 승인 + Wetterich vs perturbative 비교표 + AICc 비교 모두 채워지면 종료.
- 결과가 base.md 와 충돌 시 base.fix.md 갱신.
