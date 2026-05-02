# L363 REVIEW — MERA 5번째 pillar 가능성, 사전 리뷰 (Pre-Execution)

본 문서는 ATTACK_DESIGN / NEXT_STEP 자체에 대한 사전 점검이며, Step 1~4 완료
후 본 리뷰가 결과 리뷰로 갱신된다 (현재는 PRE 상태).

## 1. ATTACK_DESIGN 사전 점검 (Rule-A 8인 점검 대상)

### 통과
- K-T1~K-O1 기준이 K-D2 (Δ ln Z) 와 K-D3 (PPN) 양쪽을 함께 요구 → L4 의
  "K3 단일 KILL" 류 false-kill 위험 회피.
- K-D4 S_8 영향 명시 → L5 의 "background-only μ=1 한계" 재발 방지.
- a4 의 수식·부호·계수에 관한 어떤 힌트도 Command 에 없음 (CLAUDE.md 최우선-1
  통과). 8인 팀 독립 유도 보장.

### 우려 / 보완 포인트
- (W1) "5번째 pillar" 라는 라벨링 자체가 결과 편향을 만들 수 있음 — 실제 결과가
  S1 (P3 흡수) 일 때 "pillar 4.5" 라는 식의 절충 라벨로 도주하지 말 것.
  본 REVIEW 가 사전에 S1/S2/S3 만 인정하도록 경계함.
- (W2) cMERA 토이 (B1) 의 결과는 SQT 매개변수와 직접 비교되어선 안 됨 — 오직
  스케일링 지수만. 직접 매개변수 매핑 시 toy artefact 위험 (L4 K3 사례).
- (W3) K-D2 Δ ln Z > +2 는 약한 기준. 실제로는 fully-marginalized 가
  Occam 패널티로 음수일 가능성 큼 (L6 교훈). PASS 시에도 fixed-θ vs
  marginalized 명시 필수.

## 2. NEXT_STEP 사전 점검 (Rule-B 4인 코드리뷰 대상 항목)

### 통과
- 병렬 실행 (spawn 9), 스레드 고정 OMP=1, numpy 2.x trapezoid, JSON
  직렬화 _jsonify, emcee 시드 강제 — 모두 CLAUDE.md 재발방지 반영.
- B3 의 0-param vs 1-param 비교가 Occam 정당화 식 `net_gain =
  delta_logz_gap + occam_diff` 적용 대상임을 NEXT_STEP 이 함의 (명시적
  공식 대신 절차로 표현 — 지도 금지 원칙 준수).

### 우려
- (W4) sibling background module collision 위험 명시됨 → 후보 디렉터리
  분리 강제. 4인 코드리뷰 시 import 경로 확인 필수.
- (W5) cMERA 토이의 N, χ 값이 너무 작으면 (N<8, χ<2) 스케일링 추출 불가.
  너무 크면 (N>20, χ>8) 단일 머신 메모리 초과. NEXT_STEP 이 주는 N=8~16,
  χ=2~4 범위는 단일 머신 (10코어) 에서 안전.
- (W6) Step 3 Fisher 매트릭스에 RSD f σ_8 채널 포함 시, μ_eff = 1 가정
  유지 여부 확인. background-only 모델은 자동으로 μ=1 — L6 규칙 그대로
  적용.

## 3. 사전 위험도 평가

| 위험 | 확률 | 영향 | 대응 |
|---|---|---|---|
| R1 cMERA 비-AdS 정의 | 중 | K-T3 FAIL | S1/S3 시나리오로 정직 보고 |
| R2 a4 가 P1 에 이미 내포 | 중-고 | K-T1 FAIL → P5 탈락 | 사전 grep 으로 Step 0 에서 확인 |
| R3 데이터가 a4 정당화 안 함 | 중-고 | K-D1, K-D2 FAIL | 0-param 우선, S1 결론 수용 |
| R4 8인 팀이 Command 의 "5번째 pillar" 표현에 anchored | 중 | 결과 편향 | 본 REVIEW 의 W1 경고 사전 공유 |

## 4. 결정 트리 (Pre-registered)

```
Step 0 grep: a4 이미 P1 에 내포?
  ├ Yes → R2 발동, P5 탈락 결론, S1 로 직행
  └ No → Step 1 진행
        ├ K-T1 + K-T2 + K-T3 모두 PASS?
        │   ├ Yes → Step 2/3 진행
        │   │       ├ K-D1, K-D2 PASS, K-D3 위반 없음 → P5 임시 승인 (S2)
        │   │       ├ K-D 부분 PASS → S1 (P3 보강)
        │   │       └ K-D3 위반 → S1 강제 (PPN 우선)
        │   └ No → S1 또는 S3 (이론 충돌 시)
```

## 5. 본 리뷰의 한계
- 본 REVIEW 는 **PRE** 상태. Step 1~4 완료 후 결과를 받아 본 문서에 추가
  섹션 (§6 POST-EXECUTION REVIEW) 으로 합본해야 한다.
- 8인 팀 / 4인 코드리뷰가 실제로 이루어졌는지 별도 로그 확인 필요.

## 한국어 한 줄
정직: 사전 평가 기준으론 R2 (a4 가 이미 P1 에 부분 내포) 가 가장 큰 위험이며, 본 L363 결과는 P5 신설보다 P3 의 정량 보강으로 귀결될 확률이 더 높다고 본다.
