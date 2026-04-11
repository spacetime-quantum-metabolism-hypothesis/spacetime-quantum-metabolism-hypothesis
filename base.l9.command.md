# base.l9.command.md — L9 Phase-9: C28-A12 동형성 강화 + erf 기원 탐색

> 작성일: 2026-04-11. L8 완료 + L9 Round 1-5 결과 반영 수정본. 2026-04-11.
> 사용자 confirm 전부 생략. 묻지 말고 끝까지 자동 진행. 언어는 Python.

---

## 실행 명령

```
/bigwork-theory base.l9.command.md 에 기재된 L9
erf proxy 물리적 유도 파이프라인을 끝까지 수행.
사용자 confirm 전부 생략. 묻지 말고 진행. 언어는 Python.
base.l8.result.md, base.l7.result.md, base.l6.result.md,
refs/l8_new_findings.md, refs/l8_allruns_summary.md,
paper/, base.md, CLAUDE.md 전부 참고.
L9 이름으로만 신규 파일 기록.
```

---

## 근본 목적 (L8 결과 → L9 처방)

**L8 이후 상황**:

L8 확정 사항:
- 세 후보 역유도 11라운드 전원 FAIL
- SQMH 배경 ODE ≡ ΛCDM (σ·ρ_m/(3H₀) = 1.83×10⁻⁶²)
- K32 TRIGGERED (C11D), K33 TRIGGERED (C28)
- A12 K31 미발동 (chi²=7.63, 1 < 7.63 < 10)
- 8인 학술 평가 핵심 지적: "erf proxy가 왜 작동하는지 아무도 설명 못 함"

**L9 핵심 질문**:

L8은 배경 ODE 레벨에서 역유도를 시도했다. 실패 원인: σ 62차 갭, 배경 = ΛCDM.
L9는 다른 레벨에서 탐색한다:

> **"A12 erf proxy의 wₐ = -0.133은 어디서 오는가?  
> SQMH 또는 어떤 물리 메커니즘에서 이 값이 유도 가능한가?"**

탐색 경로:
1. 섭동 레벨 SQMH (배경이 아닌 성장방정식)
2. 유효 다크에너지 유체 방정식에서 wₐ<0 유도
3. SQMH 비균일 항 (∇·(nv) 항) — 균일 limit 버림
4. 양자 보정 / 반응함수 접근
5. 정보 엔트로피 / 확산 방정식에서 erf 출현 조건

SQMH 이외 경로도 허용:
- C11D (CLW) 섭동에서 wₐ<0 구조 유도 가능한가?
- C28 (RR) full Dirian 2015 방정식에서 wₐ<0 정확히 재현 가능한가?

| L8 결론 | L9 처방 | 우선순위 |
|---------|---------|---------|
| A12 배경 역유도 불가 | 섭동 레벨에서 wₐ<0 기원 탐색 | ★★★ |
| SQMH bg = ΛCDM | 비균일 항(∇·(nv)) 우주론 기여 계산 | ★★★ |
| erf 물리 미설명 | 확산방정식 → erf 출현 조건 수치 탐색 | ★★★ |
| S8/H0 미해결 | §limitations 정직 명시 (재결합 이전 물리 필요, 스코프 밖) | ★ |
| C28 simplified ODE 실패 | full Dirian 2015 구현 및 wₐ 재확인 | ★★ |
| 논문 §2 이론 연결 미완 | 성공한 유도를 §2에 반영 | ★★ |

---

## 프로세스 규칙

- **이론 검토**: 서로 중복되지 않은 8인팀. 수단과 방법을 가리지 않고 동시에 병렬 및 상호토의를 통해 유도. 결과를 취합하여 최종 판정.
- **코드**: Rule-B 4인 순차 코드리뷰, 태그 필수.
- **주장 언어**: L7/L8 언어 체계 그대로 승계 (refs/l7_honest_phenomenology.md)
  - 성공 시: "wₐ<0 structure emerges from SQMH perturbation-level sector"
  - 금지: "SQMH predicts wₐ=-0.133 exactly" (정확 수치 예측 주장 금지)

---

## Kill / Keep 기준 (L9 신규, 실행 전 고정)

**실행 시작 전** `refs/l9_kill_criteria.md` 에 아래 기준 고정.

### L9 KILL 조건

| ID | 조건 | 결과 |
|----|------|------|
| **K41** | 섭동 SQMH도 wₐ<0 생성 불가: 8인팀 합의로 어떤 메커니즘에서도 erf 유도 불가 | A12는 순수 현상론 proxy 확정. §2 이론 연결 완전 포기. |
| **K42** | C28 full Dirian 구현해도 wₐ값 불일치 (|wₐ_C28 - wₐ_A12| > 0.1) | C28-A12 동형 연결 불가. 독립 이론 확정. |
| **K43** | 비균일 SQMH (∇·nv 항) 우주론 기여 계산 결과 역시 62차 갭 | SQMH 모든 레벨에서 배경 DE에 무기여. |
| **K44** | S8/H0: 재결합 이전 물리 없이 해결 불가 (L9 Round 1-5 확정). | 논문 §limitations에 "구조적 미해결, 재결합 이전 물리 필요" 명시. 더 이상 탐색 안 함. |
| **K45** | 8인팀 "사후 합리화" 판정 | 성공 클레임 철회. |

### L9 KEEP 조건

| ID | 조건 | 결과 |
|----|------|------|
| **Q41** | 섭동 SQMH에서 wₐ<0 구조 출현: 성장방정식 f·σ8에서 SQMH-like 보정 (>1% 수준) | §2 섭동 연결 서술 가능. JCAP 이론 섹션 강화. |
| **Q42** | C28 full Dirian ODE로 wₐ = -0.13 ± 0.05 재현 | C28-A12 구조 동형 "medium level" 달성. §2 각주 → 본문 승격. |
| **Q43** | 비균일 항에서 erf-like 적분이 출현 (수학적 구조) | "SQMH spatial gradient → erf diffusion profile" 주장 가능. §2 강화. |
| **Q44** | Q41+Q43 동시 달성 | PRD Letter 재진입 검토. 이론 완결성 대폭 강화. |
| **Q45** | C28 wₐ 값을 γ₀ 조정으로 A12 wₐ=-0.133에 더 근접 (|Δwₐ|<0.03) | C28-A12 동형 "strong level" 달성 가능. PRD Letter 재검토. |

---

## 실행 순서

### Phase L9-0. 기준 고정 + 문서 준비

- `refs/l9_kill_criteria.md` K41-K44, Q41-Q44 기재 후 저장
- `base.l9.todo.md` WBS 작성
- `simulations/l9/` 디렉터리 생성 (perturbation/, gradient/, c28full/, integration/)

---

### Phase L9-A. 섭동 레벨 SQMH → wₐ<0 탐색

> 이론: 서로 중복되지 않은 8인팀, 수단과 방법을 가리지 않고 동시에 병렬 및 상호토의.

**목표**: SQMH 배경은 ΛCDM이지만, 섭동 방정식에서 σn̄ρ_m 항이 δ(성장인자)에 기여하는가?
- 성장방정식: δ'' + Hδ' − 4πGρ_m δ = SQMH 보정항?
- G_eff/G = 1 + f(σ, n̄, ρ_m) 형태의 유효 중력 상수 출현 여부
- f·σ8 측정값에서 SQMH 보정의 관측 가능성

**수치**: `simulations/l9/perturbation/sqmh_growth.py` (Rule-B 4인)
- SQMH 보정 포함 성장방정식 수치 적분
- A12 CPL 성장 곡선과 비교
- Q41 판정: SQMH 보정 > 1%이면 PASS

산출: `refs/l9_perturbation_derivation.md` + `simulations/l9/perturbation/sqmh_growth.py`

---

### Phase L9-B. 비균일 SQMH (∇·nv 항) → erf 유도

> 이론: 서로 중복되지 않은 8인팀, 수단과 방법을 가리지 않고 동시에 병렬 및 상호토의.

**목표**: 균일 limit 버리고 ∂n/∂t + ∇·(nv) = Γ₀ − σnρ_m 풀 방정식 탐색.
- v(r) = g(r)·t_P (유입속도 = 중력가속도 × 플랑크시간)
- 구형 대칭 해에서 n(r, t) 적분 → E²(z) 기여?
- 적분 결과가 erf 형태가 되는 조건 수학적 탐색

**수치**: `simulations/l9/gradient/sqmh_gradient.py` (Rule-B 4인)
- 구형 대칭 SQMH PDE 수치 적분 (r, t)
- 적분된 ρ_DE(t) 추출 → CPL 피팅
- Q43 판정: erf-like 적분 구조 출현 여부

산출: `refs/l9_gradient_derivation.md` + `simulations/l9/gradient/sqmh_gradient.py`

---

### Phase L9-C. C28 Full Dirian 2015 구현 → wₐ 정확 재현

> 이론: 서로 중복되지 않은 8인팀, 수단과 방법을 가리지 않고 동시에 병렬 및 상호토의.

**목표**: L8-R에서 simplified ODE (OmDE_RR < 0 실패) 이후 full Dirian 2015 방정식 구현.
- 완전 U, V 교차항 포함: ρ_DE = m²M_P²/4·(2U − V̇² + 3HVV̇)
- E²_RR(a=1) = 1 정규화 달성
- wₐ_C28 추출 → A12 wₐ=-0.133과 비교

**수치**: `simulations/l9/c28full/rr_full_dirian.py` (Rule-B 4인)
- Dirian 2015 Eq 2.5-2.8 완전 구현
- γ₀ = 0.0015로 wₐ 값 추출
- Q42 판정: |wₐ_C28 − wₐ_A12| < 0.1이면 PASS

산출: `refs/l9_c28full_derivation.md` + `simulations/l9/c28full/rr_full_dirian.py`

---

### Phase L9-D. S8/H0 §limitations 서술 확정 (탐색 종결)

> L9 Round 1-5에서 K44 확정 (ΔS8<0.01, ΔH0<0.7 km/s/Mpc).
> 재결합 이전 물리 필요 — SQMH 스코프 밖. 더 이상 탐색 안 함.

**목표**: 논문 §limitations에 삽입할 정확한 언어 확정.
- "S8 tension requires 16.4% G_eff suppression; SQMH provides 10⁻⁶². Structurally unresolvable without pre-recombination physics."
- "H0 tension requires +5.6 km/s/Mpc; max CPL achieves 0.7. Pre-recombination mechanism needed."

산출: `refs/l9_limitations_language.md` (논문 삽입용 언어 확정)

---

### Phase L9-E. C28-A12 동형성 심화 (Q42 → Q45)

> 이론: 서로 중복되지 않은 8인팀, 수단과 방법을 가리지 않고 동시에 병렬 및 상호토의.

**목표**: Q42 PASS (|wₐ_C28 − wₐ_A12| = 0.057) 달성 이후 더 깊은 탐색.
- γ₀ 스캔: γ₀ ≠ 0.0015 값에서 wₐ_C28 → -0.133 수렴 가능한가?
- C28 wₐ의 γ₀ 의존성 df/dγ₀ 계산 → 최적 γ₀ 탐색
- 만약 |wₐ_C28 − wₐ_A12| < 0.03 달성 가능하면 Q45 PASS

**수치**: `simulations/l9/c28full/rr_gamma_scan.py` (Rule-B 4인)
- γ₀ ∈ [0.0005, 0.005] 스캔, wₐ(γ₀) 곡선
- L6 posterior γ₀=0.0015±0.0004 범위 내에서 최적값 탐색
- Q45 판정: posterior 범위 내에서 |Δwₐ| < 0.03 달성 가능 여부

산출: `refs/l9_c28_isomorphism.md` + `simulations/l9/c28full/rr_gamma_scan.py`

---

### Phase L9-N. 수치 통합 + erf 출현 조건 분석 (Rule-B 4인)

- `simulations/l9/integration/l9_erf_analysis.py`
- 네 경로 (섭동/비균일/C28/S8H0) 결과 취합
- erf 형태 출현 조건 통합 분석
- K41-K44, Q41-Q44 수치 판정 확정

---

### Phase L9-I. 통합 판정

> 8인팀 전체 합의. 병렬 토의 후 취합.

- `refs/l9_integration_verdict.md`
- 논문 §2 이론 섹션 반영 (성공 시)
- `base.l9.result.md` 작성

---

## 산출 파일 목록

| 파일 | 내용 |
|------|------|
| `refs/l9_kill_criteria.md` | K41-K44, Q41-Q44 고정 기준 |
| `refs/l9_perturbation_derivation.md` | 섭동 레벨 8인 토의 결과 |
| `refs/l9_gradient_derivation.md` | 비균일 SQMH 8인 토의 결과 |
| `refs/l9_c28full_derivation.md` | C28 full Dirian 8인 토의 결과 |
| `refs/l9_s8h0_analysis.md` | S8/H0 탐색 또는 실패 명시 |
| `simulations/l9/tensions/s8h0_analysis.py` | S8/H0 수치 분석 |
| `refs/l9_integration_verdict.md` | 8인팀 통합 판정 |
| `simulations/l9/perturbation/sqmh_growth.py` | 성장방정식 수치 |
| `simulations/l9/gradient/sqmh_gradient.py` | 비균일 PDE 수치 |
| `simulations/l9/c28full/rr_full_dirian.py` | C28 full 구현 |
| `simulations/l9/integration/l9_erf_analysis.py` | 통합 erf 분석 |
| `base.l9.result.md` | L9 최종 결과 |
| `base.l9.todo.md` | WBS 체크리스트 |
