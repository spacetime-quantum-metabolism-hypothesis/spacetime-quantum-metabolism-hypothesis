# L393 ATTACK DESIGN — Sec 4 Predictions Table v2

## 주제
Paper Section 4 의 정량적 예측 표 v2 작성. L175 의 14-prediction 셋을 22개로 확장하여 (P15~P27) 각 항목을 PASS / PARTIAL / UNRESOLVED / falsifier 4-카테고리로 정직하게 라벨링.

## 목표
- 기존 P1~P14 (L175 SECTION_4_PREDICTIONS) 재라벨링 (현 데이터 기준 PASS/PARTIAL/UNRESOLVED 갱신).
- P15~P27 신규 13개 예측: 다음 영역에서 자연 발생하는 falsifiable 항목 발굴.
  - 우주론 (DR3 BAO, sigma8 / S8, H0 tension, Hubble drift)
  - 강한 중력장 (BH ringdown, EHT polarimetry, 중력파 dispersion)
  - 입자 / 보조 (DE-photon coupling, FRB DM 분포, neutrino mass sum)
  - 천체물리 (UDG dynamics, dwarf rotation curve, cluster lensing)
  - 실험실 (atom interferometry, torsion balance, 5th force)
- 각 예측에 falsifier 명시 (어떤 측정값이 어느 임계 초과하면 SQT 폐기).

## 방향 (지도 금지)
- "DESI DR3 가 어떻게 SQT 를 falsify 할 수 있나" — 팀이 자유 도출.
- 예측 numerical value 는 기존 시뮬레이션 결과 (L48 sigma8, L33 wa, L389 PPN 등) 인용. 새 수식 도출 금지.
- Falsifier 임계는 8인 팀 합의로 결정. 외부 강제 금지.

## 8인 팀 자유 분담 (역할 사전 지정 금지)
- 8인 토의로 자율 분담. 자연 발생 예상 영역:
  1. P1~P14 재검토 (현 상태 라벨)
  2. 우주론 신규 예측 발굴
  3. 강중력장 / GW 신규 예측 발굴
  4. 입자 / lab 신규 예측 발굴
  5. 천체물리 / 은하동역학 신규 예측 발굴
  6. Falsifier 임계 정량화
  7. PASS/PARTIAL/UNRESOLVED 4-카테고리 라벨 일관성 감사
  8. 표 통합 및 정직 한 줄 작성

## 4인 코드리뷰
- 신규 예측 numerical 인용 시 출처 (L-session ID, 데이터 ref) 검증.
- 역할 사전 지정 금지. 자율 분담.
- 라벨 PASS 주장 시 chi2 / p-value 출처 확인.

## K-기준 (사전 정의)
- K1: 22개 예측 모두 falsifier 명시 (어느 측정값 / 어느 임계).
- K2: 4-카테고리 (PASS / PARTIAL / UNRESOLVED / falsifier-only) 분포 정직 — 모두 PASS 라벨링은 의심.
- K3: P15~P27 신규 13개가 P1~P14 와 중복되지 않음.
- K4: 각 항목이 ΛCDM / MOND / AQUAL / Verlinde 중 최소 1개와 구분되는 수치 차이 명시.
- K5: 정직 한 줄 — UNRESOLVED 비율이 어느 정도인지 솔직 기록.

## 산출 형식
- ATTACK_DESIGN.md (이 파일)
- REVIEW.md: 8인 팀 토의 / 4인 코드리뷰 / K1~K5 결과 + 정직 한 줄
- SEC4_TABLE.md: 22행 표 (번호 / 영역 / 예측 / 현 상태 / falsifier / 출처)

## 정직 원칙
- "다 PASS" 결론 금지. UNRESOLVED 가 다수면 그대로 기록.
- L5 winner 들 mu_eff≈1 / S8 미해결 등 알려진 한계는 PARTIAL / UNRESOLVED 로 솔직 표시.
- L175 P1~P14 라벨 변경 시 사유 명시.
