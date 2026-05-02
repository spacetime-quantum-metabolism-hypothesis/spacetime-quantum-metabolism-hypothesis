# L349 REVIEW

**날짜**: 2026-05-01
**세션**: SQMH L349 독립 — CLASH 25 cluster σ_cluster joint fit 설계.
**한 줄 (정직)**: 본 세션은 ATTACK_DESIGN 과 NEXT_STEP 만 작성한 설계 단계이며 실제 σ_cluster 수치는 아직 산출되지 않았다.

---

## 1. 본 세션 산출

| 파일 | 상태 |
|---|---|
| `results/L349/ATTACK_DESIGN.md` | 작성 완료 |
| `results/L349/NEXT_STEP.md` | 작성 완료 |
| `results/L349/REVIEW.md` | 본 문서 |

수치 결과 (σ_cluster best-fit, 1σ, Δχ²) 는 본 세션에서 **산출하지 않았다**. 데이터 다운로드와 8인 팀 독립 도출 세션이 선행되어야 한다.

## 2. 핵심 설계 결정

- 단일 진폭 σ_cluster (1 파라미터) + per-cluster (M_vir, c_vir) (50 파라미터) joint fit.
- 데이터: Umetsu 2016 + Merten 2015 + Zitrin 2015 의 25 CLASH 클러스터.
- KILL/PASS: σ_cluster=0 대비 Δχ² 와 AICc 패널티 비교.

## 3. CLAUDE.md 준수 검토

- 최우선-1 (지도 금지): ATTACK_DESIGN 과 NEXT_STEP 어디에도 수식, 함수형, 부호 가정, 파라미터 값 없음. 방향과 현상 이름만 기재. **준수**.
- 최우선-2 (8인 팀 독립): NEXT_STEP 에서 8인 팀에 전달할 prompt 도 방향-only 로 명시. **준수**.
- 시뮬레이션 병렬: NEXT_STEP 4인팀 환경에 multiprocessing spawn + 스레드=1 강제 명기. **준수**.
- 임의 추정값 금지: CLASH 데이터 출처를 ApJ 논문 + 저자 archive 로 한정. **준수**.
- 변수명 ASCII / numpy 2.x trapezoid: 환경 가드에 포함. **준수**.

## 4. 위험 요소 (현시점)

1. **CLASH 25 selection bias**: X-ray relaxed 위주. σ_cluster 가 selection 효과를 흡수할 위험. NEXT_STEP cross-check 로 완화.
2. **per-cluster nuisance 50개**: M_vir, c_vir prior boundary 박힘 발생 가능 (L3 재발방지 사례). 4인팀 사전 점검 필요.
3. **baryonic feedback**: r < 0.1 r_vir 에서 NFW deviation. 보수적 cut 명기.
4. **AICc 패널티 미달 가능성**: 1 파라미터 추가가 Δχ² < 2 만 개선하면 LCDM-NFW 채택. 사전 등록된 KILL 기준 (K-CL2) 으로 정직 보고.

## 5. 8인 팀 사전 점검 항목 (다음 세션 입력)

- 방향 prompt 초안에 수식이 한 줄도 없는지 재확인 (위반 시 즉시 재작성, CLAUDE.md 최우선-1).
- 팀 역할 사전 지정 없음 — 인원 수 8인만 명시.
- "L34X 결과를 참고" 류 문구 금지 (이론 형태 유출 위험).

## 6. 다음 세션 입력 (요약)

1. CLASH 25 데이터 archive 다운로드 완료.
2. 8인 팀 독립 도출 세션 (이론 형태 자유).
3. 4인 코드리뷰 팀이 joint fit 코드 검증.
4. σ_cluster ± 1σ 최초 산출.

## 7. 결론 (한 줄, 정직)

L349 는 CLASH 25 클러스터 σ_cluster joint fit 의 사전 등록 설계만 마쳤으며, 수치 결과 산출과 KILL/PASS 판정은 다음 세션에서 수행한다.
