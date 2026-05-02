# L365 NEXT_STEP — Spin foam pillar 평가 후속 절차

## 정직 한국어 한 줄
사전(dictionary)이 없는 상태에서 시뮬레이션을 먼저 돌리면 과적합이므로, 다음 세션은 코드 0줄 — 8인 팀의 독립 유도와 4인 팀의 문헌 사실 검증만 진행한다.

## 단계

### S1. 문헌 fact-finding (코드 없음, 4인 자율팀)
- spin foam 모델군 (BC, EPRL, FK, KKL) 핵심 정의를 1차 문헌에서 확인 (Rovelli-Vidotto 2014, Perez 2013 living review)
- GFT condensate cosmology 의 출현 우주론 가능 범위 정직 보고 (Oriti 2016, Pithis-Sakellariadou 2019)
- "spin foam ↔ continuum field" 사전 시도 사례 정리 (이 단계에서 SQT 와의 매핑 금지)
- 산출: L365/lit_facts.md (사실만, 해석/SQT 매핑 금지)

### S2. 8인 자율팀 독립 유도 세션
- 입력: ATTACK_DESIGN.md 의 방향 + S1 의 사실
- 금지: S1 사실에서 결합상수/수식 직접 차용
- 과제: spin foam ↔ n 사전 후보 N≥3 독립 제안 → 각 후보별 C-1~C-4 자기 평가
- 산출: L365/team_dictionary_proposals.md (후보별 분리 기록)

### S3. 후보별 한계 분석 (시뮬 없이)
- 각 후보가 large-j / continuum 극한에서 P1~P3 와 충돌하는 영역을 해석적으로 식별
- Immirzi parameter, measure ambiguity 가 어떤 자유도로 나타나는지 정직 보고
- 산출: L365/limits_per_proposal.md

### S4. (조건부) 시뮬레이션 진입 결정
- S2 후보 중 하나가 C-1, C-2 를 해석적으로 통과한 경우에만 시뮬 진입
- 진입 시: GFT condensate cosmology 배경 ODE 토이를 SQT 팀이 독립 작성, multiprocessing 병렬 (≤9 워커), AICc 패널티 명시
- 진입 금지 사유 발생 시 (모든 후보 C-1 실패) → "보조 motivation" 격하 결정 후 종료

### S5. 4인 코드리뷰 (S4 진입 시에만)
- 자율 분담, 역할 사전 지정 금지
- BAO/SN/CMB/RSD 데이터 로딩, ODE convention (E²=Ω_r(1+z)⁴+ω_m+ω_de 이중카운팅 금지), trapezoid (numpy 2.x), Cassini 정합성 자동 체크 모두 포함

### S6. 승격/격하 결정 세션
- 8인 팀 표결 + 정직 결과 기록 (REVIEW.md 에 누적)
- "데이터가 LCDM 와 구분 못함" 결과도 정직 기록 (L3 RVM 패턴 학습)

## 일정 가드
- S1, S2, S3 는 각 별도 세션. 동일 세션 내 통합 금지 (지도 누출 위험).
- S4 는 production MCMC 예산 (5–6 시간/후보) 고려해 후보별 분리 프로세스.

## 비-진입 조건 (체크리스트)
- [ ] DR3 데이터 사용 시도 → 즉시 중단 (DR3 미공개)
- [ ] universal coupling 가정 → Cassini 자동 위반 위험, dark-only embedding 강제
- [ ] background-only 로 σ8/S8 해결 주장 → 금지 (μ_eff≈1 한계)
- [ ] CPL 저차 전개로 phantom crossing 주장 → hi_class 또는 exact 배경 재판정 전 인용 금지
