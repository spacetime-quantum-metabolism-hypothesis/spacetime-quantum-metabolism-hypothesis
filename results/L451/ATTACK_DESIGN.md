# L451 ATTACK_DESIGN — Bayes factor anti-cherry-pick mock injection-recovery

**주제**: 추가 anchor 추가 시 ΔlnZ 부호의 *재현성* 을 mock injection-recovery
실측으로 정량 — L424 의 "scenario × mapping 조합으로 −22 ~ +34 변동" 이
"anchor pool 확대의 데이터 우연성" 인지 "구조적 신호" 인지 분리.

**선행**:
- L424 REVIEW: dSph 추가 시 ΔlnZ 변동 ±34 (cherry-pick risk 확인).
- L405 forecast: P9 dSph 1점 toy 의 ΔlnZ ≈ +0.8 (anchor 확장 가정).
- paper §6.1 row #5 "three-regime 강제성 약함, dSph + NS 추가" ACK_REINFORCED.

**원칙**: CLAUDE.md [최우선-1, 2] 준수. 8인 자율 토의 (Rule-A).
역할 사전 지정 없음. 본 ATTACK 는 *도구 검증* 임무 — 새 이론 도출 없음.
mock 분포 측정만으로 "Bayes factor 가 anti-cherry-pick 인가" 의 운영 정의.

---

## 8인팀 자율 발생 비판 채널 (B1–B8)

### B1 — "anti-cherry-pick" 의 작동 기준 부재
"Bayes factor 가 자유도 패널티로 cherry-pick 을 방어한다" 는 *주장* 은 paper
본문에 정성. 운영 정의 부재 — 어떤 분포에서 ΔlnZ 가 어떻게 분포해야
"anti-cherry-pick" 으로 인정? 본 task 가 그 임계 *측정* 이지 *입증* 이 아님.

### B2 — Mock injection 의 truth 선택 자유도
"SQT pre-fit" 이라는 것은 baseline 8 anchor 에 three-regime 가 적합된 뒤
그 모델을 truth 로 박은 mock 생성. 이 truth 자체가 V-shape 을 *가정* 한
self-fulfilling prophecy 위험. 반드시 두 truth (LCDM null + SQT-fit)
을 병행해 *부호 비대칭* 을 본다.

### B3 — dSph anchor 추가의 두 매핑 모두 측정 필수
L424 의 LG-outer / galactic-internal 두 매핑이 부호 반전을 일으켰음. mock
runs 에서도 *두 매핑* 모두 실행해야 cherry-pick 위험 정직 측정 가능.

### B4 — N=200 표본수의 통계 한계
ΔlnZ 의 ±34 변동을 200 mock 으로 측정하면 표준오차 ~σ/√200 ≈ σ/14.
σ_ΔlnZ ~ 5 가정 시 평균 정밀도 ~0.35 — sub-σ 효과 검출 가능.
실측 σ 가 더 크면 (예: 두 매핑이 서로 다른 분포로 갈리면) 표본수 미달.
사후 적정성 판단 필요.

### B5 — Hessian 특이성 / Laplace 실패 처리
L424 baseline R∈{3,5} monotonic Hessian nan 발생. Mock 200 회 중 일부
realisation 에서 Laplace 가 실패하면 그 realisation 을 어떻게 처리할지
*사전등록*. 본 ATTACK: 실패 시 NaN 으로 표기 + 성공 표본의 분산만 보고.
실패율 자체가 cherry-pick 진단 신호.

### B6 — R-prior 의존성
ΔlnZ 는 R 에 강하게 의존 (L424 baseline: R=2 +81 vs R=10 +16). Mock 분포
도 R 에 의존. 본 task 는 R=5 를 *primary* 로 잡고 R∈{2,5,10} sensitivity
sweep 도 1회만 (mock 없이) 추가. R sweep 에 mock 곱셈은 budget 초과.

### B7 — "anti-cherry-pick" 판정 기준
다음 중 하나를 만족하면 PASS:
  (a) ΔlnZ 분포 평균이 baseline 보다 낮은 음수 (model penalty);
  (b) 분포 폭 σ_ΔlnZ < 5 (cherry-pick 폭 ±34 보다 좁음);
  (c) 매핑 두 종 (LG / INT) 의 ΔlnZ 분포가 *유의차이 없음* (mapping 자유도가
      mock 변동 안에 흡수).
정확한 statistic 은 4인팀 자율 결정.

### B8 — Toy proxy 의 paper 해석 유효 범위
본 mock 은 toy 8 + 5 anchors. paper §3.5 175 SPARC + 1 cluster + 2 cosmic
+ 5 dSph = 183 point 와 *직접 비교 불가*. 본 task 결과는 "toy 수준 cherry-
pick 진단" — paper 수준 결론은 별도 budget (L425 후속, 본 ATTACK 범위 외).

---

## 8인팀 합의 결론

- L424 가 발견한 ΔlnZ ±34 변동은 *시나리오 × 매핑 의 데카르트 곱 자유도*
  로 발생. 본 L451 는 그 자유도가 *mock realisation 변동* 보다 큰지 작은지
  를 정량.
- 핵심 측정량: ΔlnZ(three_regime − lcdm) 분포의 평균, 표준편차, 매핑별 차.
- 결과 해석은 (B7) 의 (a)/(b)/(c) 셋 중 어느 것이 충족되는가로 정직 보고.
  하나도 충족되지 않으면 "Bayes factor 는 본 toy 에서 anti-cherry-pick
  으로 작동하지 않는다" 가 정직 결론.

---

## NEXT_STEP / REVIEW 로 이행

- NEXT_STEP: 4인팀에게 mock injection-recovery task 를 (T1) truth 두 종 ×
  (T2) 매핑 두 종 × (T3) dSph 포함 / 비포함 = 8 셀 매트릭스로 분담.
- REVIEW: 4인팀 실행 결과 + (B7) 셋 기준 평가 + 정직 한 줄.
