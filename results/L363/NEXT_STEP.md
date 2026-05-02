# L363 NEXT STEP — MERA ↔ SQT a4 작업 계획

## Step 0 — 사전 체크 (즉시)
- L363 ATTACK_DESIGN.md 의 K-T1~K-O1 기준 8인 팀 사전 합의
- a4 항이 기존 산출물 (L33, L46~L56) 어디에 잠재되어 있는지 grep
  - 키워드: `a4`, `a^4`, `quartic`, `(1+z)^4`, `entanglement`, `MERA`
- 잠재 중복 확인 후, MERA 채널이 정말 새로운 자유도인지 사전 판정

## Step 1 — Axis A 이론 (8인 자율, 1세션)
- 입력: ATTACK_DESIGN 방향 키워드 ("MERA, cMERA, entanglement scaling,
  holographic bound, SQT a4")
- 산출: 각 팀원 독립 1쪽 노트 → 합치된 K-T1, K-T2, K-T3 판정
- 금지: Command 에 수식 삽입, 역할 사전 배정

## Step 2 — Axis B 시뮬레이션 (4인 코드리뷰)
- B1: cMERA 토이 (qubit chain N=8~16, bond chi=2~4) — entanglement 엔트로피
  스케일링만 측정, SQT 매개변수 매핑은 별도 모듈
- B2: SQT 배경 ODE 에 a4 자유 1-파라미터 추가 → BAO+SN+CMB+RSD joint
  fit, AICc / dynesty Δ ln Z
- B3: 0-param (MERA 고정값) vs 1-param 비교
- 환경: `multiprocessing spawn(9)`, `OMP/MKL/OPENBLAS_NUM_THREADS=1`,
  numpy 2.x → `np.trapezoid`, IDE bookkeeping `omega` 표기 준수
- 4인 코드리뷰: 자율 분담 (역할 사전지정 금지), 데이터 로딩 / chi2 / fit / 결과 검증

## Step 3 — Axis C 관측
- C1 채널 식별: a4 가 D_M/D_H, σ_8(z=0), CMB θ*, RSD f σ_8 에 미치는
  민감도 매트릭스
- C2: 현행 데이터로 a4 의 5σ 배제 영역 → 그 안에 MERA 예측이 들어가는지
- C3: DR3 / Euclid Fisher pairwise (vs C28, A12, LCDM)

## Step 4 — 판정 회의 (전체 팀)
- K-T1, K-T2, K-D2 + K-D3 동시 PASS → P5 임시 승인 (PRD Letter 검토 진입 X,
  L6 규칙 적용: Q17 또는 Q13+Q14 동반 충족 전까지 본문 반영 금지)
- 부분 PASS → P3 보강 (S1 시나리오) 으로 격하, ATTACK_DESIGN.md 업데이트
- 충돌 (S3) → 즉시 정지, base.fix.md 에 충돌 정직 기록

## Step 5 — 산출물 보관
- `results/L363/REVIEW.md` 에 8인 팀 리뷰 + 4인 코드리뷰 결과 합본
- 시뮬레이션 raw: `simulations/l363/` (sibling background module collision
  주의 — 후보별 디렉터리 내부 상대 import)
- emcee/dynesty 사용 시 `np.random.seed(42)` 강제, JSON 직렬화 `_jsonify`

## 일정 가늠 (정직)
- Step 1: 1 세션 (이론 토의)
- Step 2: 30~60 분/후보 × 1 = 약 1 시간 (B2 dynesty)
- Step 3: 30 분 (Fisher 행렬)
- Step 4: 1 세션
- 총: 1~2 작업일 (싱글 머신)

## 위험 요소 (정직 명시)
- R1. MERA 의 cMERA 연속극한이 비-AdS 배경에서 잘 정의되지 않음 (Beny 2013
  미해결) → K-T3 에서 막힐 가능성
- R2. SQT 의 a4 가 P1 에서 이미 부분 도출되어 있으면 K-T1 자동 FAIL → P5
  탈락
- R3. 데이터가 a4 추가 자유도를 정당화하지 않으면 K-D1, K-D2 모두 FAIL
  (L5 0-param vs 1-param 사례 반복 위험)

## 한국어 한 줄
정직: 본 작업의 가장 큰 병목은 K-T2 (MERA 가 a4 를 자유도 없이 고정) 이며, 실패 시 P5 가 아니라 P3 의 미세 보강으로 정리하는 것이 정직한 결과다.
