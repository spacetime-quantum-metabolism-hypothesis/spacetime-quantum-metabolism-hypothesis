# L627 — SQT 정밀도 향상 path 방향 (Empirical precision over paradigm ambition)

> **[최우선-1] 절대 준수**: 본 문서는 **방향만** 기재. 수식 0줄, 파라미터 값 0개, 도출 0건.
> 본 문서는 8인 자율 도출 *이전 단계*의 path 정찰이며, 어떤 정밀화 path 도 본 세션 단독으로 실행하지 않는다.

---

## §1. 5 path 표 (방향 / [최우선-1] 위험 / 외부 의존)

| Path | 방향 (수식 없음) | [최우선-1] 위험 | 외부/세션 의존 | 본 세션 단독 실행 |
|------|------------------|------------------|----------------|-------------------|
| **P1**. a₀ 기하 인자 정밀화 | disc azimuthal projection 의 sub-leading 보정 *방향*. 현 상태 = "geometric plausibility" (L605 §1) | **고**. 인자 정밀화는 즉시 수치 도출 진입 → [최우선-1] 위반 직행 | 8인 자율 도출 (L599 룰) | **불가** |
| **P2**. σ₀ dimensional uniqueness 강화 | 동일 차원 family 후보의 명시 배제 *방향*. 현 상태 = 차원분석 단독 PASS | **중**. 후보 나열만 하면 안전, 계수 비교 들어가면 위반 | 8인 자율 도출 의무 (Rule-A) | **불가** (정찰만) |
| **P3**. 6 falsifier 정량 예측 명시화 | DR3 / Euclid 등 외부 데이터에 대한 paradigm-specific 부호·범위 예측 *방향*. L623 §3 박탈 회피 조건과 직접 연결 | **최고**. paradigm-specific 값 도출 = 본질적 [최우선-1] 위반 | 8인 도출 + 외부 데이터 (DR3 비공개) | **불가** |
| **P4**. 3-regime σ₀(env) boundary 정량화 | cosmic ↔ cluster ↔ galactic 환경 전환 임계 *질문*. 현 상태 = 질적 분리만 | **중**. boundary 자체는 관측 fit 이지만 postdiction risk 그대로 | 관측 데이터 + 8인 합의 | **불가** (postdiction 위험) |
| **P5**. N_eff 결합 정밀화 | cross-correlation 더 정밀 추정 + Fisher information *방향*. 현 상태 = ρ-corrected combined (L498) | **저**. 통계적 재추정은 hidden DOF 누적 위험 (+1) | 4인 코드리뷰 (Rule-B) | 부분 가능 (코드 재검토만) |

---

## §2. Top-2 path 선정

선정 기준: (a) [최우선-1] 위험 최소, (b) GR-level empirical 정확도 향상 기여, (c) 외부 검증 가능성.

1. **P5 (N_eff 결합 정밀화)** — 위험 가장 낮음. 4-pillar 정합 강화 채널. 단 hidden DOF 위험 명시.
2. **P3 (falsifier 정량 예측)** — 효과 가장 큼 (L623 박탈 회피 직결). 단 [최우선-1] 위험 최고 → 8인 자율 도출 *전용*.

P1 / P2 / P4 는 본 세션 외부 (8인) 로 위임.

---

## §3. GR-level empirical 정확도 도달 가능성 평가

- **GR analogue**: 정량 예측 1건 외부 검증 (perihelion) = paradigm 가치의 *진짜 원천*.
- **SQT 현 상태**: empirical 정확도 ≈ 0 (L605 GR 4축). paradigm-derived 새 예측 1–2/5 (L623).
- **본 5 path 중 1 성공 시**: empirical 정확도 +0.5 → 0.8/4 → 1.3/4 (L605 metric).
- **전 path 실패 시**: SQT = 영구 phenomenology 확정. paradigm shift 자격 박탈 (L569/L591 pivot 영구 정합).
- **DR3 진검 통과**: 부호 예측 1건 일치 = L623 §3 박탈 회피 최소 조건. P3 가 직접 채널.

평가: GR-level 도달은 **이론상 가능**하나 본 5 path 중 P3 + 외부 검증 일치 동시 충족이 필요. 단일 path 만으로는 도달 불가.

---

## §4. 본 세션 단독 실행 가능성

| Path | 단독 실행 가능 | 사유 |
|------|----------------|------|
| P1 | ✗ | [최우선-1] 위반 직행 — 인자 정밀화는 즉시 수치 도출 |
| P2 | ✗ | 8인 자율 도출 의무 (Rule-A). 본 세션 단일 에이전트 결정 금지 |
| P3 | ✗ | paradigm-specific 값 도출 = 본질적 [최우선-1] 위반 |
| P4 | ✗ | postdiction risk + 8인 합의 필요 |
| P5 | △ | 4인 코드리뷰 (Rule-B) 범위 내 부분 가능. 단 본 세션은 *방향* 단계 |

→ **본 세션 산출은 path 정찰 문서 1건 (본 문서) 한정**. 어떤 정밀화 path 도 본 세션에서 실행 금지.

---

## §5. 정직 한 줄

> 5 path 모두 본 세션 단독 실행 불가; SQT 의 GR-level empirical 정확도는 이론상 가능하나 P3 (falsifier 정량 예측) + 외부 검증 일치를 8인 자율 도출 경로로 통과해야만 도달하며, 그 외 경로는 영구 phenomenology 확정 시나리오와 정합한다.
