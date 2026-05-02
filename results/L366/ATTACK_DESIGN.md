# L366 ATTACK_DESIGN — SQT a4 micro origin closure: Verlinde / MERA / Causet / Spin foam 비교

## 목적
SQT 공리 A4 (emergent metric, Lagrangian 보류) 의 미시 기원 후보 4 개 — L362 Verlinde entropic, L363 MERA tensor network, L364 Causal set, L365 Spin foam — 를 동일 기준으로 비교하고 SQT 의 5번째 pillar 로 채택할 단일 후보를 선정한다.

## 정직 한국어 한 줄
A4 가 Lagrangian 까지 닫혀야 SQT 가 "패턴 → 동역학 → metric" 사슬을 완성하므로, 4 후보를 자체 메리트가 아니라 SQT 기존 4 pillar (A1 흡수 / A2 보존 / A3 생성 / A6 선형유지) 와의 정합성으로 채점한다.

---

## 평가 축 (8 축, 각 0–5)

L362–L365 가 도입된 맥락 (a4 partial → full closure) 에 종속한 축만 사용. 각 후보의 자체 우수성 (예: Verlinde 의 MOND 자릿수) 은 SQT 정합성으로 환산되어야 가산된다.

| 축 | 의미 | 측정 방식 |
|---|---|---|
| AX1 SQT-A1 정합 | 흡수 bilinear 형식과 미시 구조의 양립 | 미시 도출에서 R_abs 형 항이 자연 출현하는가 |
| AX2 SQT-A3 정합 | 균일·등방 자발 생성과의 양립 | 미시 동역학에서 Γ_0 같은 등방 source 가 자연 출현 |
| AX3 D1 회복 | Newton G 의 σ_0, τ_q 도출과 충돌 없음 | 미시 모델의 G 도출이 D1 과 동등 영역에서 일관 |
| AX4 D5 회복 | MOND a_0 자릿수 도출과 충돌 없음 | 미시 모델이 깊은 MOND 영역에서 동일 스케일 산출 |
| AX5 Lagrangian 도달 | A4 의 정성 → 정량 (작용 원리) 가능 여부 | 후보가 명시적 작용 (또는 path integral) 정의를 가짐 |
| AX6 양자장 호환 | n(x,t) 스칼라장 해석과 양립 | 후보의 미시 자유도가 n 의 거시 한계를 자연히 산출 |
| AX7 반증 채널 | SQT 와 별개의 관측 채널 부여 | 표준 우주론 외 독립 가설 (예: Lorentz 위반, BH entropy 보정) |
| AX8 도구 성숙도 | Phase γ 시뮬에서 즉시 사용 가능한 코드/수식 도구 사슬 | 공개 구현, 안정성, 우리 환경 (10코어 CPU) 적합도 |

각 후보 점수 산정은 L362–L365 ATTACK 결과 (현재 비어 있음) 가 채워지면 본 표를 갱신한다. 본 L366 은 SQT 정합성 기반 사전 비교 (a-priori prior) 만 제공.

---

## 4 후보 비교 (사전 prior, ATTACK 결과 도착 전)

| 후보 | 핵심 미시 가정 | A1 정합 | A3 정합 | D1 회복 | D5 회복 | Lagrangian | n장 호환 | 반증 채널 | 도구 성숙 | 종합 prior |
|---|---|---|---|---|---|---|---|---|---|---|
| L362 Verlinde entropic | metric ← 정보/엔트로피 구배 | 중 | 약 | 중 | 강 | 약 (작용 부재) | 중 | 강 (MOND) | 중 | ★★★½ |
| L363 MERA tensor network | metric ← 얽힘 renormalisation 계층 | 약 | 약 | 약 | 약 | 중 (path integral 접근) | 강 (장 자연) | 약 | 약 (cosmology 부재) | ★★½ |
| L364 Causet | metric ← 부분순서 (causal poset) | 약 | 강 (Poisson sprinkling = Γ_0 형식) | 중 | 약 | 강 (BDG action) | 중 | 강 (Λ swerves) | 중 (CausalSets.jl 류) | ★★★★ |
| L365 Spin foam | metric ← 양자 amplitude 합 (LQG 공변) | 중 | 약 | 강 (Newton 한계 잘 정의) | 약 | 강 (EPRL/FK action) | 약 (n 스칼라 도출 우회) | 중 | 약 (수치 비용 큼) | ★★★ |

(prior 등급은 L73 SQT 공리 형식과의 *구조적* 양립도. 시뮬 결과가 들어오면 갱신.)

---

## 선정 규칙 (Pass/Fail)

- **K-L366-1 (정합성)**: AX1+AX2+AX3+AX4 합 ≥ 14/20.
- **K-L366-2 (작용 도달)**: AX5 ≥ 4 (Lagrangian/path-integral 명시 후보만 통과).
- **K-L366-3 (장 호환)**: AX6 ≥ 3 (n(x,t) 거시 한계 자연 도출).
- **K-L366-4 (반증)**: AX7 ≥ 3 (SQT 와 *추가* 독립 채널 제공).
- **K-L366-5 (도구)**: AX8 ≥ 3 (Phase γ 즉시 진입 가능).

K-L366-1 ~ 5 모두 PASS 인 후보가 둘 이상이면 종합 점수 최댓값 채택. 모두 FAIL 이면 5번째 pillar 보류 (A4 부분 정밀 유지) 후 L367 에서 재설계.

---

## 자율 분담 — 4인팀 (역할 사전 지정 금지)
4인팀이 후보별 독립 채점. 점수 합의 후 표 작성. 사전 역할 (예: "Verlinde 담당") 배정 없음.

## 위험 / 함정
- L362–L365 ATTACK_DESIGN 이 비어 있음 → prior 만으로 최종 채택 금지. 본 L366 은 *비교 프레임워크* + *사전 추천* 까지만 산출.
- "MOND 자릿수 회복" 같은 자체 메리트가 SQT 정합성을 자동 보장하지 않음 (예: Verlinde 는 A3 등방 생성과 정합 약함).
- AX5 (Lagrangian) 만으로 채택 금지. AX1/AX3 정합 미달 시 작용이 있어도 SQT 의 a4 가 아닌 *경쟁* 이론.
- 사전 prior 등급은 ATTACK 시뮬 결과로 +/-2★ 까지 변동 허용.

## 산출
- `RANKING.csv` (8축 × 4후보)
- `SELECTED_PILLAR.md` (채택 후보 + 채택 사유 + 잔존 위험)
- L367 진입 게이트 결정문
