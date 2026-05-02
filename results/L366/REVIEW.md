# L366 REVIEW — 4 후보 비교 + 5번째 pillar 사전 선정

## 입력 상태 점검
- `results/L362/`, `results/L363/`, `results/L364/`, `results/L365/` 모두 **빈 디렉터리** (2026-05-01 기준).
- `results/L73/SQT_AXIOMS_FORMAL.md` A4 항: "emergent metric 은 *Lagrangian 보류*. 부분 정밀."
- A4 closure 가 SQT 의 마지막 미해결 공리. 4 후보 중 하나가 5번째 pillar 로 들어와야 SQT 의 패턴→동역학→metric 사슬이 닫힘.

따라서 본 L366 은 **시뮬 결과 없이 사전 prior 비교** 에 한정한다. 정직하게 명시.

---

## 후보 4종 정성 비교 (사전 prior, 등급 ★)

| 후보 | 미시 출발점 | SQT A1 (흡수) | SQT A3 (등방 생성) | D1 (Newton G) | D5 (MOND a_0) | A4 작용 명시 | n(x,t) 호환 | 독립 반증 | 도구 | 종합 |
|---|---|---|---|---|---|---|---|---|---|---|
| **L362 Verlinde** entropic gravity | metric ← 정보/엔트로피 구배 | 중 | 약 | 중 | **강** | 약 | 중 | 강 (MOND) | 중 | ★★★½ |
| **L363 MERA** tensor network | metric ← 얽힘 RG 계층 | 약 | 약 | 약 | 약 | 중 | **강** | 약 | 약 | ★★½ |
| **L364 Causet** | metric ← causal poset | 약 | **강** (Poisson sprinkling = Γ_0 형식) | 중 | 약 | **강** (BDG action) | 중 | **강** (Λ swerves) | 중 | **★★★★** |
| **L365 Spin foam** | metric ← amplitude 합 (LQG 공변) | 중 | 약 | **강** | 약 | **강** (EPRL/FK) | 약 | 중 | 약 (수치 비용) | ★★★ |

---

## 채택 게이트 (K-L366-1~5) prior 통과 여부

| 후보 | K1 정합 | K2 작용 | K3 n장 | K4 반증 | K5 도구 | 사전 통과? |
|---|---|---|---|---|---|---|
| Verlinde | △ | FAIL (작용 부재) | △ | PASS | PASS | **부분 FAIL (K2)** |
| MERA | FAIL | △ | PASS | FAIL | FAIL | **FAIL** |
| Causet | △ | PASS (BDG) | △ | PASS | PASS | **PASS** |
| Spin foam | △ | PASS (EPRL) | FAIL (n 도출 우회) | △ | FAIL | **부분 FAIL (K3, K5)** |

prior 단계에서 5 게이트 모두 통과 가능성 가장 높음 = **Causet (L364)**.

---

## 사전 선정: Causet — *조건부* 5번째 pillar

### 채택 사유
1. **A3 자연 일치**: Causal set 의 Poisson sprinkling 은 Lorentz-invariant 균일·등방 *random* 생성. SQT A3 의 Γ_0 (uniform, isotropic, 자발 생성) 와 *형식적으로 동일* 한 통계 구조.
2. **A4 작용 명시**: Benincasa-Dowker-Glaser causal-set d'Alembertian / BDG action 이 명시된 Lagrangian-equivalent 도달. AX5 통과.
3. **독립 반증 채널**: Causet 우주상수의 swerves (fluctuations) 는 Λ 의 시간 변동을 예측 — DESI w(z) 변동 channel 과 *자연스러운 접점*.
4. **도구**: 공개 구현 존재, 10코어 CPU 환경에서 sprinkling 시뮬 즉시 가능.

### 잔존 위험 (정직)
- AX1 (A1 흡수 형식) 정합 prior 약. Causet 자체에는 bilinear 흡수 항이 자연 없음 → SQT 의 σ_0 ρ_m n 항을 *추가 가정* 으로 얹어야 함.
- AX3 (D1 회복) 중간. Causet → Newton G 는 emergent 영역 한정, σ_0/(4π τ_q) 도출과 직접 연결 미증명.
- AX4 (D5 MOND) 약. Verlinde 가 이 축에서는 우월. **만약 D5 회복이 5번째 pillar 의 우선 조건이라면 Verlinde 와 Causet 의 hybrid (entropic + causet) 가 차선책**.

### 탈락 사유
- **MERA**: A1·A3 정합 약 + cosmology 도구 미성숙. 5 게이트 중 3 FAIL.
- **Verlinde**: 작용 미명시 (K2 FAIL) — 단, MOND 자릿수 회복은 D5 채널에서 *보조 영감* 으로 유지.
- **Spin foam**: n(x,t) 스칼라 자연 출현 어려움 + 수치 비용 큼. K3, K5 FAIL.

---

## 최종 결정문

**조건부 채택**: Causet → SQT 5번째 pillar 사전 후보. L367 (Phase γ a4 closure) 에서 BDG action 의 SQT A1/A3 항 *추가 적합* 검증을 거쳐 정식 채택.

**보류 조건**: L362–L365 ATTACK 시뮬 결과가 prior 와 어긋나면 본 결정은 **무효**, NEXT_STEP 의 게이트 재평가 절차로 회귀.

---

## 비판 (4인팀 자율 분담, 사후 정리)

- **P (이론)**: BDG action 이 Lagrangian 단계 도달 명시 → A4 정성→정량 가교 가능. ★★★★.
- **N (수치)**: Sprinkling 통계는 Poisson, 우리 환경에서 즉시 시뮬 가능. ★★★★.
- **O (관측)**: Λ swerves 는 DESI w(z) 변동 채널과 자연 접점 — *추가 검증 가능 양 1개 확보*. ★★★★.
- **H (자기일관 헌터)**: "Causet 의 sprinkling 이 SQT Γ_0 와 형식적으로 동일하다" 는 *prior* 일 뿐, 실제 통합 ODE 에서 sprinkling 측도가 Γ_0 ε 의 에너지 보존 (A2) 까지 보존하는지 미검증. **L367 의 1번 과제**.

---

## 한국어 한 줄
정직: 4 후보 ATTACK 결과가 비어 있어 본 결정은 사전 prior 이며, Causet 가 SQT A3·A4 와 가장 자연스럽게 맞물리지만 흡수항 (A1) 호환은 L367 에서 별도 검증해야 한다.
