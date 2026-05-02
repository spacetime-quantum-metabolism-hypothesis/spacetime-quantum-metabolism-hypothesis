# L657 — DR3 (2027 Q2) 후 paper update trajectory plan

본 문서는 DESI DR3 결과 공개 (2027 Q2 예상) 후 SQT paper 가 어떻게 update 되어야 하는지 *예측 trajectory plan* 이다. 수식·파라미터 값 0개 ([최우선-1] 준수). 본 plan 은 preregistered protocol 로서 DR3 결과 공개 *전* 에 확정·동결되어야 한다.

---

## §1. DR3 결과 시나리오 3가지

| 구분 | 시나리오 A: PASS | 시나리오 B: Inconclusive | 시나리오 C: KILL |
|---|---|---|---|
| DR3 w_a 영역 | 강한 음의 영역 (DR2 중심값 근방 혹은 더 강한 음수) | 중간 영역 (DR2 와 LCDM 사이 어중간) | 약한 음수 또는 양수 (LCDM 근방 또는 그 이상) |
| Falsifier 판정 | L498 6 falsifier 중 1 PASS | conditional / 미결 | 6 falsifier 중 1 KILL |
| Paradigm shift | A3+Time emergent / Bootstrap 부분 부활 가능 | 보류 (다음 falsifier 대기) | 영구 박탈 |
| Acceptance 기대값 | ★★★★ → ★★★★★ 가능 | ★★★★ 유지 | ★★★ 격하 |
| Paper 액션 | revision (positive 결과 반영) + 추가 paper 가능 | minimal update | retraction 권고 또는 framework 격하 후 재제출 |

판정 boundary 의 정확한 임계값은 본 plan 작성 시점 (DR3 공개 전) 에 *별도 preregistration 문서* 로 동결한다. 본 plan 은 trajectory 의 "구조" 만 다룬다.

---

## §2. Paper update trajectory (각 시나리오 × 섹션)

각 시나리오에서 paper 의 §0/§5/§6/§7/§8 이 어떻게 업데이트되는지 trajectory.

### §0 Abstract 어휘
- A: "DR2 hint" → "DR2 + DR3 confirmed", "first-of-six falsifier passed", positive language 강화
- B: "DR2 hint" 유지 + "DR3 inconclusive, awaiting Euclid / CMB-S4" 명시
- C: "DR2 hint" → "DR2 hint not confirmed by DR3", framework limitation 정직 명시

### §5 Quantitative
- A: DR3 결과를 DR2 와 나란히 표로 추가, joint DR2+DR3 fit 결과 제시, 6-falsifier dashboard 의 DR3 entry 를 PASS 로 갱신
- B: DR3 결과를 표에 추가하되 결론 미정으로 표시, dashboard entry 는 "pending" 유지
- C: DR3 결과를 표에 추가, dashboard entry 를 KILL 로 갱신, 본문 quantitative 결론을 framework-level limitation 으로 재서술

### §6 Limitations
- A: limitations 의 한 항목 해소 기록, 남은 5 falsifier 명시 유지
- B: "DR3 inconclusive" 를 limitations 의 신규 항목으로 추가, Euclid + CMB-S4 대기 명시 (의무)
- C: limitations 섹션 의무 확대 — DR3 KILL 항목, framework-level 재해석, retraction 권고 또는 격하 결정 명시

### §7 Outlook
- A: 다음 trigger 를 Euclid (성장 측) + CMB-S4 (조기 우주 측) 로 재정렬, paradigm-shift 후속 paper plan 명시
- B: Outlook 거의 변화 없음, 다음 falsifier 대기 자세 유지
- C: Outlook 을 "framework retraction 후 재제출 경로" 또는 "축소된 phenomenology 로의 격하 경로" 로 전환

### §8 Reproducibility
- A/B/C 공통: DR3 verify 스크립트를 신규 항목으로 추가 (`simulations/lXXX/dr3/run_dr3.sh` 기반, 재현 instruction 포함). DR3 데이터 경로·해시·DESI 공식 release 버전 고정 명시.

---

## §3. Submission timeline 영향

| 시나리오 | 본 paper 진행 | 후속 paper |
|---|---|---|
| A | DR3 결과 포함 revision 후 재제출 (target 저널 동일 또는 격상) | paradigm-shift 후속 paper (A3+Time emergent / Bootstrap 부분 부활) 신규 trajectory 가능 |
| B | 수정 minimal — referee 요청 시에만 DR3 결과 추가, 결론 변경 없음 | 다음 falsifier (Euclid / CMB-S4) 결과까지 대기 |
| C | retraction 또는 framework-level 격하 후 phenomenology paper 로 재제출 | paradigm-shift 후속 paper 영구 폐기 |

DR3 공개 시점 기준 paper 가 *under review* 단계라면 referee 에 DR3 update plan 사전 통보 의무. *published* 단계라면 시나리오 A/B 는 corrigendum / addendum, 시나리오 C 는 retraction 절차.

---

## §4. 사용자 결정 항목

본 plan 확정·실행 전 사용자 결정이 필요한 항목.

1. DR3 PASS/Inconclusive/KILL 의 *정확한 w_a 임계값* 동결 (별도 preregistration 문서).
2. 시나리오별 자동 decision tree 의 분기 조건 (예: B → A 변경 트리거가 후속 데이터 결합 결과인지, DR3 자체 추가 통계인지).
3. 시나리오 C 발동 시 retraction vs framework-level 격하 중 default 선택.
4. multi-session 의무 (L633 H2) 적용 범위 — DR3 update session 을 단일 세션으로 끝낼지, 8인 Rule-A 리뷰 + 4인 Rule-B 코드 리뷰 분리 의무인지.
5. preregistration 문서 자체의 공개 위치 (논문 §8 reproducibility 부록, OSF preregistration, GitHub tag 중 택일 또는 병행).

---

## §5. 8인 Rule-A 의무 (preregistered protocol)

본 trajectory plan 은 *이론 클레임* 영역 (paradigm shift, retraction 권고, framework 격하) 을 포함하므로 CLAUDE.md L6 규정에 따라 Rule-A 8인 순차 리뷰 의무.

- 리뷰 시점: DR3 공개 *전* (preregistration 동결 시점) + DR3 공개 *후* (실제 발동 시점) 두 차례.
- 사전 리뷰 주제: §1 시나리오 boundary, §2 trajectory 구조, §3 timeline 영향, §4 사용자 결정 항목 모두.
- 사후 리뷰 주제: 실제 DR3 결과의 시나리오 분류, paper update 본문, 결정 트리거의 정합성.
- 코드 영역 (DR3 verify 스크립트, evidence 재계산) 은 Rule-B 4인 리뷰 별도 의무.
- 리뷰 완료 전 paper revision / retraction / 격하 결정의 본 외부 발신 금지.

---

## §6. 정직 한 줄

본 plan 은 DR3 결과 공개 *전* 에 작성된 *예측 trajectory plan* 이며, 실제 DR3 결과·수치·임계값을 포함하지 않는다. 시나리오 분기는 preregistered protocol 로서만 의미를 가지며, DR3 공개 후 사후적으로 분기 조건을 조정하면 이 plan 의 falsifiability 는 무효화된다.
