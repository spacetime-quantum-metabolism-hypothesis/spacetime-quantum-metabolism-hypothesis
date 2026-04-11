# base.l13.command.md — L13 Phase-13: 논문 약점 직공

> 작성일: 2026-04-12. L12 완료 + 8인 재검토 이후 설계.
> 사용자 confirm 전부 생략. 묻지 말고 끝까지 자동 진행. 언어는 Python.

---

## 실행 명령

```
/bigwork-theory base.l13.command.md 에 기재된 L13
논문 약점 6개 파이프라인을 끝까지 수행.
사용자 confirm 전부 생략. 묻지 말고 진행. 언어는 Python.
base.l12.result.md, base.l11.result.md, base_2.md §7, refs/l8_new_findings.md,
simulations/l5/A01/mcmc_production.json, simulations/l4_alt/runner.py, CLAUDE.md 전부 참고.
L13 이름으로만 신규 파일 기록.
```

---

## 근본 목적

8인 재검토에서 식별된 약점들을 직접 공략한다.
L12가 "새 이론 경로 탐색"이었다면, L13은 "현재 A01의 내부 구조를 해부해 약점을 강점으로 전환"한다.

**반드시 해소해야 할 핵심 비판 3개**:

1. **근본 동기 미완**: 왜 Γ₀인가? 왜 σ = 4πGt_P인가?
   이 두 파라미터의 물리적 근거가 없으면 SQMH는 사후 설명에 불과하다.

2. **물리적 정당성 미완**: ρ_DE = ΩΛ[1 + Ωm×(1−a)]에서 추가항 Ωm×(1−a)가
   왜 물리적으로 정당한지가 논문의 핵심 주장이 되어야 한다.
   이걸 SQMH 방정식에서 도출하지 못하면 논문의 핵심이 흔들린다.

3. **SQMH 고유성 미입증 (가장 위험한 비판)**:
   A01은 사실상 CPL w₀ = −1+Ωm/3 ≈ −0.9 고정 모델과 거의 같다.
   "dark energy가 과거에 좀 더 많았다"는 형태를 갖는 모든 모델이
   DESI를 더 잘 맞추는 것 아닌가?
   Ωm으로 진폭을 고정한 것이 이론적으로 필연적임을 보이지 못하면,
   SQMH는 DESI 개선을 설명하지 못하고 단순히 편승한 것이 된다.

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
| **K84** | 새 각도에서도 Γ₀ 범위 > 20자리, σ=4πGt_P 근거도 없음 | NF-27 완전 확정. 두 파라미터 모두 근거 없음 명기 필요. |
| **K85** | DR3 Fisher: A01 vs ΛCDM 구분 SNR < 2σ | DR3로도 판가름 어려움. Euclid/CMB-S4 필요. |
| **K86** | A01이 "wₐ<0인 임의 1파라미터 모델"과 통계적으로 구분 불가 | SQMH 고유성 없음. 편승 모델 확정. 논문 포지셔닝 전면 재검토. |

### L13 KEEP 조건

| ID | 조건 | 결과 |
|----|------|------|
| **Q81** | 전체 ODE Δchi² > A01 + 2 | 1차 근사에서 누락 항 존재. 전체 ODE를 논문 메인으로. |
| **Q82** | Ωm 진폭이 SQMH 방정식 구조에서 이론적으로 도출 | "Ωm은 이론 예측" 논문 핵심 주장 추가 가능. |
| **Q83** | wₐ 이론 보정 ≥ 0.3 (DESI 방향) | wₐ 갭 이론적 부분 해소. 논문 §3 업그레이드. |
| **Q84** | Γ₀ 또는 σ=4πGt_P 중 하나라도 이론적 근거 확보 | 근본 동기 부분 해소. 논문 §2 강화. |
| **Q85** | DR3 Fisher: 특정 z-bin SNR ≥ 3σ | 명확한 검증 타임라인. 논문 §5 추가. |
| **Q86** | SQMH가 Ωm 진폭을 자유 파라미터 없이 유일하게 결정함을 증명 | "coincidence 아님" 확립. SQMH 고유성 확보. 논문의 핵심 강점. |

---

## 탐색 방향 6개

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

### L13-Γ. 근본 파라미터 (Γ₀, σ) 이론적 기원

**약점**: 왜 Γ₀인가? 왜 σ = 4πGt_P인가?
두 파라미터 모두 이론적 근거가 없다. NF-27(Γ₀ = Λ_CC 재포장), L12-B Bekenstein → K72 KILL.
σ = 4πGt_P 역시 L12-V Verlinde → K73 KILL. 둘 다 현재 미완.

**방향**: L12에서 시도하지 않은 완전히 새로운 각도에서 Γ₀와 σ 중 하나라도 이론적 필연성을 찾아라.
어느 하나라도 부분적 근거가 생기면 Q84.
수단과 방법은 8인팀이 결정.

산출: `refs/l13_gamma0_derivation.md`, `simulations/l13/gamma0/`

---

### L13-U. SQMH 고유성 — coincidence인가 예측인가

**약점 (가장 위험)**: A01 = ΩΛ[1 + Ωm(1−a)]는 사실 CPL에서 w₀ = −1+Ωm/3로 고정한 것과 유사하다.
"dark energy가 과거에 더 많았다"는 형태의 임의 모델도 DESI를 잘 맞출 수 있다.
이 경우 SQMH는 DESI 개선에 편승한 것이지 예측한 것이 아니다.

**방향**: 
- "wₐ < 0인 임의 1파라미터 phenomenological 모델"과 A01을 통계적으로 비교하라.
- Ωm이 진폭으로 등장하는 것이 SQMH 방정식 구조에서 필연적임을 증명하거나 반증하라.
- SQMH만이 자유 파라미터 없이 이 특정 형태를 유일하게 예측한다는 것을 보여야 한다.
수단과 방법은 8인팀이 결정.

K86/Q86 판정 주도.

산출: `refs/l13_uniqueness_derivation.md`, `simulations/l13/uniqueness/`

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
| `refs/l13_uniqueness_derivation.md` | L13-U 고유성 8인 토의 |
| `refs/l13_dr3_prediction.md` | L13-D DR3 예측표 |
| `refs/l13_integration_verdict.md` | 8인 통합 판정 |
| `simulations/l13/ode/` | L13-O 수치 |
| `simulations/l13/amplitude/` | L13-A 수치 |
| `simulations/l13/wwa/` | L13-W 수치 |
| `simulations/l13/gamma0/` | L13-Γ 수치 |
| `simulations/l13/uniqueness/` | L13-U 수치 |
| `simulations/l13/dr3/` | L13-D 수치 |
| `base.l13.result.md` | L13 최종 결과 |
| `base.l13.todo.md` | WBS 체크리스트 |

---

*작성: 2026-04-12. L12 10라운드 완료 + 8인 재검토 이후. 실행 보류.*
