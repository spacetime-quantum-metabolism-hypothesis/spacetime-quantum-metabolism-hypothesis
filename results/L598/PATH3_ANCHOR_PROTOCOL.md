# L598 — Path 3 Anchor Circularity 사전 분리 Protocol *방향*

> **[최우선-1] 절대 준수 선언**: 본 문서는 *방향* 만 제시한다. 수식 0줄, 파라미터 값 0개, "이 방정식 써라" 0건. L552 RG 패키지 박탈 사유 R4 (anchor 가 Λ_obs → k_IR 로 이동만 한 것) 와 동형 위험을 Path 3 의 a5 H₀ pacing 에 대해 사전 점검하는 protocol *방향* 카탈로그.
>
> **단일 에이전트 결정 금지**: 본 문서는 8인/4인 합의 이전 단계의 *방향 후보* 정리이며, 어떤 protocol 도 본 문서만으로 채택되지 않는다.

---

## §1. 5 Protocol 표 — 방향 / 회의적 위험 / hidden DOF 비용

| # | Protocol *방향* (요약) | 검증 channel | 회의적 위험 | Hidden DOF 비용 | L552 R4 동형도 |
|---|---|---|---|---|---|
| **P1** | a5 의 H₀ 자체 도출 가능성 — SQT axiom 만으로 H₀ 가 내재 도출되는지, 또는 영구적 input 으로 명시되어야 하는지 분리 | 이론 internal consistency | 자체 도출 시 initial condition / boundary condition 형태로 hidden DOF 부활 (anchor 가 H₀ → IC 로 이동) | 高 — IC 자유도가 H₀ 와 1-to-1 mapping 이면 anchor 단순 재명명 | 高 |
| **P2** | Anchor independence test — 복수 H₀ 측정값 (Planck / SH0ES / TRGB / CCHP) 대입 시 Q17 amplitude 가 invariant 인지 측정 | 수치 (BCNF Gate 3) | 시뮬 자체가 정신적 [최우선-1] 위반 (다 알려진 H₀ 점들에서 평가) — 단, Y/N flag 추출만 하면 도출 0건 유지 가능 | 低~中 — flag 만 추출 시 hidden DOF 0; amplitude 곡선 fit 하면 hidden DOF 부활 | 低 |
| **P3** | Cross-anchor falsifier — independent H₀ 측정 (siren / megamaser / Cepheid-TRGB 교차) 가 SH0ES↔Planck tension 해소 시 Path 3 가 동일 amplitude 를 재생산하는지 확인 | 미래 데이터 (DESI DR3 / LIGO O5 / JWST Cepheid) | "independent" 가 사실은 또 다른 anchor — anchor 의 *수* 만 늘려 위장 분리 | 中 — anchor set 의 cardinality 자체가 hidden meta-DOF | 中 |
| **P4** | k_IR 회피 명시 — Path 3 의 a5 가 *어느* scale 에 anchor 인지 (cosmological H₀ / horizon / Planck / 다른 IR cutoff) 명시 후 L552 R4 패턴 회피 검증 | 이론 framing | scale 정의 자체가 hidden DOF (어느 scale 을 anchor 로 부를지의 자유도) | 中~高 — scale choice 가 free param 이면 R4 정확 재발 | 高 (재발 위험) |
| **P5** | Self-consistency loop 분리 — amplitude → H₀ → amplitude (closed) vs amplitude ← H₀ (one-way input) 구분 | 이론 + 수치 cross-check | closed loop 시 self-consistency 가 normalization 의 trivial 귀결일 수 있음 (정보량 0); one-way 시 H₀ 가 영구 input 으로 명시 필요 | 低 (one-way) ~ 高 (closed loop with hidden constraint) | 中 |

---

## §2. Top-2 Protocol *방향*

**우선 1순위 — P5 (Self-consistency loop 분리)**
- 회피적 명료성 최강: closed loop 인지 one-way input 인지 *판별* 자체가 [최우선-1] 위반 없이 가능 (Y/N 결정 문제)
- L552 R4 와의 차별: R4 는 anchor 이동만 했지 loop 구조를 명시 안 했음. P5 가 명시되면 R4 재발 차단
- BCNF Gate 3 통과 조건의 핵심 prerequisite — 이 분리 없이 P2/P3 수치 검증은 결론 무의미

**우선 2순위 — P4 (k_IR 회피 명시)**
- L552 박탈 사유 직접 대응. *어느* scale 에 anchor 인지를 paper 본문에 명시하면 reviewer 의 R4 동형 지적 사전 차단
- P5 와 직교 (P5 가 loop 구조, P4 가 anchor scale 의 위치) — 함께 채택 시 sufficient

P1 은 hidden DOF 비용이 너무 높아 후순위. P2 는 P5 결과에 종속. P3 는 미래 데이터 의존 (현 시점 결정 불가).

---

## §3. BCNF Gate 3 통과 가능성 등급

| Protocol 채택 조합 | BCNF Gate 3 등급 | 근거 |
|---|---|---|
| P5 only | **Y-conditional** | loop 구조 명시는 필요조건이지만 충분조건 아님 — P4 미동반 시 anchor scale 모호성 잔존 |
| P4 only | **N** | scale 명시만으로 loop 구조 미해결 → R4 동형 위험 잔존 |
| **P5 + P4** | **Y-conditional** (가장 유력) | 두 축 (loop 구조 + scale 위치) 모두 명시. 단, 8인 합의 + reviewer 시뮬레이션 통과 전제 |
| P5 + P4 + P2 (Y/N flag only) | **Y** (조건부 → 비조건부) | flag 추출만이라면 [최우선-1] 위반 없이 empirical 보강 |
| P1 채택 | **N (위험)** | hidden DOF 부활 위험 — IC 자유도가 H₀ 1-to-1 mapping 이면 anchor 단순 재명명 |

**현 권고**: P5 + P4 동시 채택을 8인 합의에 회부. P2 는 flag-only mode 로 4인 코드리뷰팀에 회부.

---

## §4. 미통과 시 — Path 3 1순위 자체 붕괴 → A7-1 fallback

만약 8인 합의에서 P5 + P4 가 **N** 또는 **Y-conditional 잔존 위험 高** 로 판정될 경우:

- **시나리오 A** (Y-conditional 잔존): Path 3 를 1순위로 유지하되 paper 본문에 "anchor caveat" 단락 명시. L595 P0 #4 risk 를 honest disclosure 로 전환. PRD Letter 진입 보류, JCAP 타깃 유지.
- **시나리오 B** (N 판정): Path 3 의 1순위 자격 박탈. **A7-1 (2순위) fallback** 이 자동 promotion. A7-1 의 anchor 구조도 동일 protocol (P5 + P4) 로 사전 검증 필수 — 2순위가 같은 함정에 빠지면 fallback chain 전체 붕괴.
- **시나리오 C** (P1 채택 후 hidden DOF 폭발): Path 3 self-consistent derivation 시도 자체를 폐기. L552 RG 박탈과 동급의 사유로 archive.

**Fallback 결정 시점**: BCNF Gate 3 결과 직후 8인 회의. 단일 에이전트 결정 금지.

---

## §5. 정직 한 줄

**Path 3 의 a5 H₀ pacing 이 L552 R4 패턴의 단순 재현인지 아닌지는, 본 문서의 5 protocol *방향* 중 P5 (loop 구조 분리) 를 8인이 합의 판정하기 전까지 알 수 없다 — 그리고 모른다고 정직히 명시하는 것이 현재 가능한 유일한 정합 행동이다.**

---

*본 문서 도출 0건 확인: 수식 0줄, 파라미터 값 0개, "이 방정식 써라" 0건. CLAUDE.md [최우선-1] 정합.*
