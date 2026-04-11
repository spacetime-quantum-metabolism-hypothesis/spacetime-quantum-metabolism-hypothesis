# base.l8.command.md — L8 Phase-8: SQMH 역유도 (살아남은 후보 → 근본 방정식)

> 작성일: 2026-04-11. L7 Phase-7 완료 이후 설계.
> 사용자 confirm 전부 생략. 묻지 말고 끝까지 자동 진행. 언어는 Python.

---

## 실행 명령

```
/bigwork-theory base.l8.command.md 에 기재된 L8
SQMH 역유도 파이프라인을 끝까지 수행.
사용자 confirm 전부 생략. 묻지 말고 진행. 언어는 Python.
base.l7.result.md, base.l6.result.md, simulations/l6/evidence/,
paper/, base.md, CLAUDE.md, refs/l7_*.md 전부 참고.
L8 이름으로만 신규 파일 기록.
```

---

## 근본 목적 (L7 결과 → L8 처방)

**L7 이후 상황**:

L7 확정 사항:
- A12 (0-param, Δ ln Z = +10.769) **1위**
- C11D (1-param, Δ ln Z = +8.771) **2위**
- C28 (1-param, Δ ln Z = +8.633) **3위**
- 세 후보 모두 Jeffreys STRONG, K17 PASS
- UV completion (L7-T): LQC/GFT/CDT 형태적 유사만. 완전 유도 불가 (Q21 미달)
- 경로 B 확정: "QG-motivated phenomenology"

**L8 핵심 질문**:

L7-T는 위에서 아래로: "SQMH → LQC/GFT/CDT에서 유도되는가?"
L8은 아래에서 위로: **"살아남은 각 후보(C11D/A12/C28) → SQMH 근본 방정식을 역으로 유도할 수 있는가?"**

SQMH 근본 방정식:
```
∂n/∂t + ∇·(nv) = Γ₀ − σ n ρ_m
σ = 4πG t_P (SI)
```

**역유도 전략**: 각 후보의 작용 / 배경 방정식 / 에너지 보존식에서 출발해,
SQMH 연속방정식과 동형(isomorphic) 구조가 출현하는지 탐색.
동형이면 "후보 = SQMH 특정 극한"으로 해석 → PRD Letter 이론 조건 충족 가능.

| L7 결론 | L8 처방 | 우선순위 |
|---------|---------|---------|
| Q21 미달 (UV completion 미완) | 역유도 경로: 후보 → SQMH 방정식 | ★★★ |
| C11D = CLW quintessence (A'=0) | disformal 구조에서 σ n ρ_m 소멸항 추출 | ★★★ |
| A12 = erf proxy (이론 연결 미완) | erf 형태를 SQMH ODE 적분에서 유도 | ★★★ |
| C28 = Maggiore-Mancarella RR | 비국소 보조장 방정식에서 SQMH 동형 탐색 | ★★ |
| 논문 §2 "QG-motivated" 강화 필요 | 성공한 유도를 §2에 반영 | ★★ |

---

## 프로세스 규칙

- **이론 검토**: 서로 중복되지 않은 8인팀. 수단과 방법을 가리지 않고 동시에 병렬 및 상호토의를 통해 유도. 결과를 취합하여 최종 판정.
- **코드**: Rule-B 4인 순차 코드리뷰, 태그 필수.
- **주장 언어**: L7 언어 체계 그대로 승계 (refs/l7_honest_phenomenology.md)
  - 역유도 성공 시: "C11D action contains a sector isomorphic to SQMH continuity"
  - 금지: "C11D is derived from SQMH" (인과 역전 금지)

---

## Kill / Keep 기준 (L8 신규, 실행 전 고정)

**실행 시작 전** `refs/l8_kill_criteria.md` 에 아래 기준 고정.

### L8 KILL 조건

| ID | 조건 | 결과 |
|----|------|------|
| **K31** | A12 역유도 실패: 8인팀 합의로 SQMH ODE 어떤 극한에서도 A12 erf 형태 출현 불가 | A12는 현상론 proxy 확정, §2 이론 연결 주장 금지 |
| **K32** | C11D 역유도 실패: 8인팀 합의로 CLW φ ODE에서 σ n ρ_m 구조 추출 불가 | C11D-SQMH 동형성 주장 금지 |
| **K33** | C28 역유도 실패: 8인팀 합의로 RR 보조장 방정식에서 SQMH 동형 없음 | C28는 독립 이론 확정, SQMH 연결 주장 금지 |
| **K34** | 3개 모두 K31-K33 → 역유도 경로 전면 실패 | L8 이론 채널 포기. JCAP 논문에 "역유도 시도 실패" §8 추가 후 종료 |
| **K35** | 역유도 성공했으나 8인팀 "사후 합리화" 판정 | 성공 클레임 철회, "형태 유사" 수준으로 격하 |

### L8 KEEP 조건

| ID | 조건 | 결과 |
|----|------|------|
| **Q31** | A12 역유도 부분 성공: SQMH ODE 균일 극한이 erf형태 배경 생성 (수치 일치 필요) | §2 A12 이론 연결 강화 가능 |
| **Q32** | C11D 역유도 성공: CLW φ ODE가 SQMH 연속방정식과 변수 치환으로 동치 | PRD Letter 이론 조건 충족 가능 |
| **Q33** | C28 역유도 부분 성공: RR 보조장 V 방정식이 n 방정식과 동형 | §2 각주 수준 추가 가능 |
| **Q34** | Q32 달성 (C11D 완전 동치) | PRD Letter 진입 → L7-P 조건부 실행 |
| **Q35** | Q31+Q33 동시 달성 | JCAP §2 강화. "복수 후보에서 SQMH 구조 출현" 서술 가능 |

---

## 실행 순서

### Phase L8-0. 기준 고정 + 문서 준비

- `refs/l8_kill_criteria.md` K31-K35, Q31-Q35 기재 후 저장
- `base.l8.todo.md` WBS 작성
- `simulations/l8/` 디렉터리 생성 (a12/, c11d/, c28/, integration/)

---

### Phase L8-A. A12 → SQMH 역유도

> 이론: 서로 중복되지 않은 8인팀, 수단과 방법 가리지 않고 동시에 병렬 및 상호토의.

**목표**: SQMH 균일 배경 ODE에서 A12 erf 형태가 출현하는지 탐색.

**수치**: `simulations/l8/a12/sqmh_ode_vs_erf.py` (Rule-B 4인)
- SQMH 배경 ODE 수치 적분 + A12 CPL E²(z) 비교
- K31 판정: chi²/dof > 10 → KILL. < 1 → Q31 PASS.

산출: `refs/l8_a12_derivation.md` + `simulations/l8/a12/sqmh_ode_vs_erf.py`

---

### Phase L8-C. C11D → SQMH 역유도 (최우선)

> 이론: 서로 중복되지 않은 8인팀, 수단과 방법 가리지 않고 동시에 병렬 및 상호토의.

**목표**: CLW 자율계 (x, y) ODE에서 SQMH σ n ρ_m 소멸항 구조 추출.
Q32 달성 시 PRD Letter 조건 충족.

**수치**: `simulations/l8/c11d/clw_vs_sqmh.py` (Rule-B 4인)
- CLW autonomous system 수치 적분
- σ_eff(a) 역산 + SQMH σ = 4πG t_P 비교
- K32 판정: σ_eff / σ_SQMH 비율 + CV 기준

산출: `refs/l8_c11d_derivation.md` + `simulations/l8/c11d/clw_vs_sqmh.py`

---

### Phase L8-R. C28 → SQMH 역유도

> 이론: 서로 중복되지 않은 8인팀, 수단과 방법 가리지 않고 동시에 병렬 및 상호토의.

**목표**: RR 비국소 보조장 방정식 (Dirian 2015)에서 SQMH 동형 구조 탐색.

**수치**: `simulations/l8/c28/rr_vs_sqmh.py` (Rule-B 4인)
- RR 배경 ODE (U, V, U1, V1) 수치 적분
- U(a) = Γ₀_eff - σ_eff P ρ_m 피팅, 잔차 계산
- K33 판정: 잔차 > 20% → KILL

산출: `refs/l8_c28_derivation.md` + `simulations/l8/c28/rr_vs_sqmh.py`

---

### Phase L8-N. 수치 통합 검증 (Rule-B 4인)

- `simulations/l8/integration/l8_comparison.py`
- 세 후보 결과 JSON 취합 → 통합 판정 테이블
- K31-K33 수치 판정 확정

---

### Phase L8-I. 통합 판정

> 8인팀 전체 합의. 병렬 토의 후 취합.

- `refs/l8_integration_verdict.md`
- 논문 §8 역유도 섹션 반영 (성공 시 §2도 수정)
- `base.l8.result.md` 작성

---

## 산출 파일 목록

| 파일 | 내용 |
|------|------|
| `refs/l8_kill_criteria.md` | K31-K35, Q31-Q35 고정 기준 |
| `refs/l8_a12_derivation.md` | A12 8인팀 역유도 토의 결과 |
| `refs/l8_c11d_derivation.md` | C11D 8인팀 역유도 토의 결과 |
| `refs/l8_c28_derivation.md` | C28 8인팀 역유도 토의 결과 |
| `refs/l8_integration_verdict.md` | 8인팀 통합 판정 |
| `simulations/l8/a12/sqmh_ode_vs_erf.py` | A12 수치 비교 |
| `simulations/l8/c11d/clw_vs_sqmh.py` | C11D 수치 비교 |
| `simulations/l8/c28/rr_vs_sqmh.py` | C28 수치 비교 |
| `simulations/l8/integration/l8_comparison.py` | 통합 비교 |
| `base.l8.result.md` | L8 최종 결과 |
| `base.l8.todo.md` | WBS 체크리스트 |
