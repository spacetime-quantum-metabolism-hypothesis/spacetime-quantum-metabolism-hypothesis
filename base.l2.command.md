# base.l2.command.md — L2 재설계 탐색 실행 지시서

> 이 문서는 `/bigwork-paper` 스킬에 투입할 **최종 확정 지시안**. 사용자 confirm
> 없이 끝까지 자동 진행. 중간 체크포인트 전부 제거.

---

## 실행 명령

```
/bigwork-paper base.l2.command.md 에 기재된 L2 재설계 탐색을 끝까지 수행.
사용자 confirm 전부 생략. 묻지 말고 진행. 언어는 Python.
base.md, base.fix.md, base.fix.class.md, base_2.md, base.bad.1.md,
base.bad.2.md, base.todo.result.md 참고.
```

---

## 🎯 목표

**이론 정합성 탐색** — L2 kinetic/coupling sector 재설계. base.md 의 깨진 층
(L3/L4) 대체 후보 발굴 + 수식 레벨 정합성 증명.

---

## 📐 수락 조건 (사전 선언, KPI)

`refs/l2_acceptance.md` 에 기록. **4 조건 중 2 개 이상 만족** → L2 후보 채택.
0~1 개 → 폐기.

| ID | 조건 | 판정 방법 |
|---|---|---|
| **C1** | Cassini `|γ−1|<2.3e−5` **내재 통과** (Vainshtein 사후 주입 금지) | 수식 유도 + 수치 계산 |
| **C2** | Phase 3 best-fit β≈0.107 이 C1 을 **자동 만족** 하는 해석적 증명 | 수식 |
| **C3** | ∇_μ T^μν = 0 + Bianchi 동시 만족 (보존 법칙) | 수식 |
| **C4** | w_a<0 이 구조적 필연 or 자연 범위 (ad-hoc λ 튜닝 금지) | 수식 + 간단 수치 |

**전 후보 0/1 조건 통과 시 → Path F 재확인 후 L2 탐색 종료**.

---

## 📋 스코프

**포함**
- L2 kinetic sector 재설계
- Coupling 구조 재설계 (universal ξ 대안)
- Cassini 내재 통과 메커니즘
- w(z) 형태 자연성 논증

**제외** (별도 과제)
- Lindblad decoherence 유도 (`base.bad.1.md §3` → Phase 5 이월)
- UV completion / 양자중력 완성
- 관측 데이터 MCMC 재실행 (Phase 3/4 결과 **인용만**)

---

## 🔗 상속 / 재설계 / 인용 기준

**상속 (불가침)**
- L0/L1 대사 공리, σ = 4πG·t_P, Γ₀ = H₀·(…) (Phase 1 검증 완료)
- `base.md §V` 5개 프로그램 연결 (이론 유산)

**재설계 (교체)**
- `base.md §4` V(φ) = ½m²φ² 단순 포텐셜
- `base.md §IV` universal ξ = 2√(πG)/c² coupling
- `base.md §XVI` Cassini 사후 논증

**인용 (증거)**
- Phase 3 β≈0.107, χ²=1666.78 (`phase3/mcmc_phase3.py`, `r_d_tension.md`)
- Phase 3.6 B1 Cassini 984× 위반 (`simulations/screening.py`)
- Phase 3.6 B3 V_exp forward shooting (`simulations/kessence.py`)

---

## 🧭 실행 순서 (사용자 confirm 전부 생략, 끝까지 자동 진행)

### Phase L2-A. R1 — 후보 32 개 나열 + 16 인팀 평가

**16 인팀 서로 다른 시각**:

각 관점이 **후보 2 개씩 제안** → 총 **32 개 후보 라그랑지안**.

**산출**. `base.l2.md §1` (후보 12 개 표 + 8 인팀 평가 매트릭스 12×4, C1~C4
통과 여부)

### Phase L2-B. R2 — 4 개 수락 조건 필터

12 후보 × 4 조건 (C1~C4) 매트릭스. **2 개 이상 통과한 후보만 잔존**.

**산출**. `base.l2.md §2` (잔존 후보 리스트, 각 조건별 ✓/✗ 판정 + 근거 한 줄)

### Phase L2-C. R3 — 수식 유도 (4 인팀, 서로 다른 시각)

잔존 후보 각각에 대해 **4 명 독립 수식 유도**:

4명의 독립 관점 **합의 수식만** `base.l2.md §3` 채택. 불일치는 `§4 "미해결"` 기록.

**산출**. `base.l2.md §3` (잔존 후보별 수식 + 4 관점 합의 표시), `§4` (미해결)

### Phase L2-D. base.l2.md 통합

위 `§1~4` 합쳐 `base.l2.md` 완성. `§5` 결론 (후보 K 개 생존, 수락 조건 M 개
통과).

### Phase L2-E. base.l2.todo.md 초안

`base.l2.md §3` 수식을 구현/검증하는 작업 목록. **Phase 단위 WBS**.

### Phase L2-F. base.l2.todo.md 세세 확장 (2 회)

- **1 회차**. Phase → 세부 태스크 (T1.1, T1.2, …)
- **2 회차**. 태스크 → 원자 단위 (파일명, 함수명, 검증 방법)

### Phase L2-G. base.l2.todo.md 끝까지 수행

원자 태스크 순차 실행. **각 코드 작성 후 4 인 코드리뷰**:

1. **Numerical correctness** — 단위, 부호, ODE convention
2. **Physical sanity** — 에너지 양성, 인과성, ghost
3. **Reproducibility** — seed, 데이터 경로, 의존성
4. **Prevention rules** — `CLAUDE.md` 재발방지 항목 위반 검사

4 리뷰 **전부 pass** 한 결과만 사용. 실패 시 재작성.

---

## 📦 산출물 체크리스트

| 파일 | 내용 |
|---|---|
| `refs/l2_acceptance.md` | C1~C4 수락 조건 사전 선언 |
| `base.l2.md` | §0 요약 / §1 12 후보 + 8 인팀 / §2 필터 / §3 4 인팀 수식 / §4 미해결 / §5 결론 |
| `base.l2.todo.md` | Phase WBS → 세부 태스크 → 원자 태스크 (2 회 확장) |
| `base.l2.todo.result.md` | 실행 로그, 4 인 코드리뷰 결과, 최종 판정 |
| `simulations/l2/` | 잔존 후보 구현 (C1 검증, PN γ 계산 등) |
| `CLAUDE.md` | 새 재발방지 규칙 (코드리뷰 중 발견된 것) |

---

## ⚖️ 최종 판정 규칙

**시나리오 1** — 후보 1 개 이상 4/4 조건 통과
→ **L2 재설계 성공**. Phase 5 (관측 재검증) 준비.

**시나리오 2** — 후보 1 개 이상 2~3 조건 통과
→ **부분 성공**. `base.l2.md` 에 "개선 경로" 로 기록. Phase 5 진입 판단은
사용자 몫.

**시나리오 3** — 모든 후보 0~1 조건 통과
→ **Path F 재확인**. `paper/negative_result.md` 에 L2 탐색 negative 결과 부록
추가. 이론 생존 불가 선언.

---

## 🚫 금지 사항

- 사용자 confirm 요청 (끝까지 자동 진행)
- Python 외 언어 사용
- 관측 데이터 MCMC 재실행 (인용만)
- Vainshtein screening 사후 주입 (C1 내재 통과 강제)
- 코드리뷰 4 인 합의 미통과 결과 사용
- `base.md` 원본 수정 (base.l2.md, base_2.md 에만 기록)

---

## ✅ 필수 준수

- 모든 파일 UTF-8
- `CLAUDE.md` 재발방지 규칙 전부 준수
- 8 인팀 / 4 인팀 관점은 **서로 다른 시각** 유지 (동의 반복 금지)
- 진행 로그는 `base.l2.todo.result.md` 에 지속 append
- 완료 태스크는 `base.l2.todo.md` 에 `[x]` + 결론 한 줄 추가
