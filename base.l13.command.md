# base.l13.command.md — L13 Phase-13: 논문 약점 직공

> 작성일: 2026-04-12. L12 완료 + 8인 재검토 이후 설계.
> 사용자 confirm 전부 생략. 묻지 말고 끝까지 자동 진행. 언어는 Python.

---

## 실행 명령

```
/bigwork-theory base.l13.command.md 에 기재된 L13
논문 약점 5개 파이프라인을 끝까지 수행.
사용자 confirm 전부 생략. 묻지 말고 진행. 언어는 Python.
base.l12.result.md, base.l11.result.md, base_2.md §7, refs/l8_new_findings.md,
simulations/l5/A01/mcmc_production.json, simulations/l4_alt/runner.py, CLAUDE.md 전부 참고.
L13 이름으로만 신규 파일 기록.
```

---

## 근본 목적

8인 재검토에서 식별된 약점들을 직접 공략한다.
L12가 "새 이론 경로 탐색"이었다면, L13은 "현재 A01의 내부 구조를 해부해 약점을 강점으로 전환"한다.

---

## 프로세스 규칙

- **이론 검토**: 서로 중복되지 않은 8인팀. 수단과 방법을 가리지 않고 동시에 병렬 및 상호토의. 결과 취합 후 최종 판정.
- **코드**: Rule-B 4인 순차 코드리뷰, 태그 필수.
- **주장 언어**: L7~L12 언어 체계 승계. 과장 금지.
- **게임체인저 기준**: Q83 or Q85 달성 시 논문 §4 재구성 트리거.

---

## Kill / Keep 기준 (L13 신규, 실행 전 고정)

**실행 시작 전** `refs/l13_kill_criteria.md` 에 아래 기준 고정.

### L13 KILL 조건

| ID | 조건 | 결과 |
|----|------|------|
| **K81** | 전체 SQMH ODE 수치 적분 Δchi² = A01 Δchi² ± 0.5 | A01 근사 충분. 1차 근사 사용 정당화. |
| **K82** | Ωm 진폭이 정규화 조건에서만 나옴 (이론 구조 아님) | 진폭 도출 실패. 논문에 "amplitude locking = normalization artifact" 명기 필요. |
| **K83** | wₐ 이론 보정 크기 < 0.1 | 섭동론으로 wₐ 갭 해소 불가. |
| **K84** | 새 각도에서도 Γ₀ 범위 > 20자리 | NF-27 완전 확정. |
| **K85** | DR3 Fisher: A01 vs ΛCDM 구분 SNR < 2σ | DR3로도 판가름 어려움. Euclid/CMB-S4 필요. |

### L13 KEEP 조건

| ID | 조건 | 결과 |
|----|------|------|
| **Q81** | 전체 ODE Δchi² > A01 + 2 | 1차 근사에서 누락 항 존재. 전체 ODE를 논문 메인으로. |
| **Q82** | Ωm 진폭이 SQMH 방정식 구조에서 이론적으로 도출 | "Ωm은 이론 예측" 논문 핵심 주장 추가 가능. |
| **Q83** | wₐ 이론 보정 ≥ 0.3 (DESI 방향) | wₐ 갭 이론적 부분 해소. 논문 §3 업그레이드. |
| **Q84** | 새 제약으로 Γ₀ 범위 ≤ 5자리 | NF-27 부분 해소. |
| **Q85** | DR3 Fisher: 특정 z-bin SNR ≥ 3σ | 명확한 검증 타임라인. 논문 §5 추가. |

---

## 탐색 방향 5개

### L13-O. 전체 ODE vs A01 근사

**약점**: A01은 SQMH ODE의 1차 근사. 근사 오차가 DESI 비교에 얼마나 영향을 주는가?

**방향**: 전체 SQMH ODE를 그대로 수치 적분해서 A01과 chi² 비교.
수단과 방법은 8인팀이 결정.

산출: `refs/l13_ode_derivation.md`, `simulations/l13/ode/`

---

### L13-A. Ωm 진폭의 이론적 기원

**약점**: A01의 진폭 = Ωm. Alt-20 스캔에서 경험적으로 설정됨.
이게 SQMH 방정식 구조에서 나오는 예측인가, 단순 정규화인가?

**방향**: SQMH 방정식에서 Ωm이 진폭으로 등장하는 이론적 근거를 찾아라.
수단과 방법은 8인팀이 결정.

산출: `refs/l13_amplitude_derivation.md`, `simulations/l13/amplitude/`

---

### L13-W. wₐ 이론 보정

**약점**: A01 예측 wₐ ≈ −0.13 vs DESI 중심값 −0.64. 2σ 내이지만 불안.

**방향**: SQMH 이론 범위 내에서 wₐ를 DESI 방향으로 개선할 수 있는 기여를 찾아라.
(고차 보정, 초기 조건 효과, 비평형 기여 등 — 수단과 방법은 8인팀이 결정.)

산출: `refs/l13_wwa_derivation.md`, `simulations/l13/wwa/`

---

### L13-Γ. Γ₀ 새 제약 각도

**약점**: NF-27 (Γ₀ fine-tuning = Λ_CC 재포장). L12-B Bekenstein → K72 KILL.

**방향**: Bekenstein이 아닌 완전히 다른 각도에서 Γ₀를 제약하는 조건을 찾아라.
수단과 방법은 8인팀이 결정.

산출: `refs/l13_gamma0_derivation.md`, `simulations/l13/gamma0/`

---

### L13-D. DR3 예측 명시화

**약점**: SQMH의 구체적 DR3 예측값이 없어 falsifiability 주장이 약함.

**방향**: A01이 DR3 각 z-bin에서 예측하는 BAO 거리를 계산하고,
DR3 예상 정밀도로 ΛCDM과의 구분 가능성을 정량화하라.
논문 Table 형식으로 문서화.

산출: `refs/l13_dr3_prediction.md`, `simulations/l13/dr3/`

---

### L13-I. 통합 판정

- K81-K85, Q81-Q85 최종 판정
- 논문 §2~§5 재구성 제안
- `refs/l13_integration_verdict.md`, `base.l13.result.md`

---

## 산출 파일 목록

| 파일 | 내용 |
|------|------|
| `refs/l13_kill_criteria.md` | K81-K85, Q81-Q85 |
| `refs/l13_ode_derivation.md` | L13-O 8인 토의 |
| `refs/l13_amplitude_derivation.md` | L13-A 8인 토의 |
| `refs/l13_wwa_derivation.md` | L13-W 8인 토의 |
| `refs/l13_gamma0_derivation.md` | L13-Γ 8인 토의 |
| `refs/l13_dr3_prediction.md` | L13-D DR3 예측표 |
| `refs/l13_integration_verdict.md` | 8인 통합 판정 |
| `simulations/l13/ode/` | L13-O 수치 |
| `simulations/l13/amplitude/` | L13-A 수치 |
| `simulations/l13/wwa/` | L13-W 수치 |
| `simulations/l13/gamma0/` | L13-Γ 수치 |
| `simulations/l13/dr3/` | L13-D 수치 |
| `base.l13.result.md` | L13 최종 결과 |
| `base.l13.todo.md` | WBS 체크리스트 |

---

*작성: 2026-04-12. L12 10라운드 완료 + 8인 재검토 이후. 실행 보류.*
