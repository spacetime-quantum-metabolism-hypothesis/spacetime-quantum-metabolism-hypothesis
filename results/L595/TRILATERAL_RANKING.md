# L595 — A7-2 / Path 3 / A7-1 Trilateral Distributed 8-Reviewer Ranking

목적: L594 CRITICAL C1 해소. L585 / L587 / L588 단일-세션 순위 모순(3 path
서로 다른 1위)을 *동시* 평가 분산 시뮬로 단일화.

원칙: CLAUDE.md [최우선-1] — 수식 0줄. 방향·구조 비교만.
회의적 모드 — 좋은 점은 의도적 생략, 비교 위해 필요한 최소 균형만 유지.

---

## §1. 8 axes × 3 path 평가 매트릭스

표기: H=high cost / risk, M=medium, L=low. (낮을수록 priori 회복에 유리)

| Axis | A7-2 (Conservation) | Path 3 (a4×a5 cross) | A7-1 (Causality) |
|------|---------------------|----------------------|-------------------|
| 1. 외부 framework 수입 비용 | H — Noether/U(1) gauge 신규 axiom, group structure 선택 자유도 | L — 4-pillar 내부, 외부 import 없음 | H — SR/GR light-cone 신규 axiom, Lorentz 구조 import |
| 2. Hidden DOF 비용 | H — 보존량 종류 + symmetry group + current 정의 3중 자유도 | M — cross 함수형 + 2 pillar 사용 (a4, a5) 선택 자유도 | H — light-cone 정의 + signal speed + unitarity 3중 |
| 3. Postdiction 위험 (시간 순서) | H — 1/(2π) 결과 알고서 보존량 후보 도출 | H — amplitude 결과 알고서 a4×a5 cross 선택 | H — positivity 결과 알고서 causality 후보 도출 |
| 4. Anchor circularity | M — 보존 current 측정 시 anchor 의존 가능 (current → flux → scale) | H — a5 의 H₀ anchor 직접 의존, a₀ 측정에 H₀ 입력 필요 | L — light-cone 은 local, anchor 무관 |
| 5. 3-regime universal | M — gauge group 선택이 regime 별 동일하다는 보장 없음 | M — cross 함수형이 dwarf/cluster/cosmo 동일 형태 가정 | L — causality 는 정의상 보편 |
| 6. 관측 가능성 | M — conserved current direct measurement path 미정 | M — a₀ 측정 채널 존재 (rotation curve, lensing) | H — causality 자체는 위반 측정만 가능 (positive test 부재) |
| 7. Falsifiability | M — 보존량 위반은 detectable 하나 register 어려움 | M — a₀ 변동·환경 의존성 falsifier 등록 가능 | L — Lorentz 위반 실험 (LIV) 풍부, 기존 falsifier 풍부 |
| 8. R3+R4 BCNF protocol 통과 가능성 | L — 신규 axiom + hidden DOF 3중으로 protocol gate 통과 어려움 | M — 4-pillar 내부라 신규 axiom 부담 없음. 단 cross 함수형 선택이 BCNF lock-in 단계에서 추가 자유도로 잡힘 | L — 신규 axiom + import 비용으로 protocol gate 통과 어려움 |

핵심 관찰:
- Postdiction 위험은 3 path 동등 H — *어느 후보도* 시간 순서 위반 면제 안 됨.
- BCNF 통과 가능성: Path 3 만 M, A7-1/A7-2 는 L. 신규 axiom 비용 차이.
- A7-1 만 axis 4·7 에서 L — causality 의 locality + LIV 실험 자산.
- A7-2 는 모든 axis 에서 동등 또는 더 나쁨 — 단일 우위 없음.

---

## §2. 8 reviewer 개별 ranking

R1 (theory minimality 관점)
ranking: Path 3 > A7-1 > A7-2
사유: 신규 axiom 비용이 priori 회복의 핵심 적. 4-pillar 내부 path 가 외부
import 0. A7-2 는 gauge group 선택 자유도 추가로 hidden DOF 가 가장 많음.
A7-1 은 SR/GR import 부담이지만 group 선택 자유도는 없음. priori 회복 1순위는
"axiom 추가 없이 기존 자원 재조합" 방향. (243자)

R2 (postdiction adversary 관점)
ranking: A7-1 > Path 3 > A7-2
사유: 3 path 모두 결과를 본 후 후보 도출이라 시간순서 위반은 동등. 하지만
A7-1 은 LIV 실험 풍부로 *독립* falsifier 등록 path 가 즉시 존재. Path 3 은
a₀ 측정으로 가능하나 anchor circularity. A7-2 는 보존 current 측정 path
미정. postdiction 의 실질 risk 는 A7-2 가 최악. (240자)

R3 (anchor circularity 관점)
ranking: A7-1 > Path 3 > A7-2
사유: a5 가 H₀ pacing 을 명시적으로 anchor 하므로 Path 3 는 a₀ 측정에서
H₀ feedback. A7-2 는 conserved current → flux scale 에서 anchor 잠재.
A7-1 의 light-cone 은 local 정의로 anchor 의존 0. priori 회복에서
anchor circularity 는 dataset reuse 와 별도로 추가 위험. (228자)

R4 (BCNF protocol 통과 관점)
ranking: Path 3 > A7-1 > A7-2
사유: R3+R4 BCNF lock-in 은 axiom 신규 추가에 가장 엄격. Path 3 만 신규
axiom 0 으로 lock-in 단계에서 axiom 비용 0. A7-1·A7-2 는 axiom 추가
정당화 자체가 protocol gate. A7-2 는 추가로 gauge group 선택 자유도까지
lock-in 필요. Protocol 통과 가능성 순서 명확. (245자)

R5 (3-regime universality 관점)
ranking: A7-1 > Path 3 > A7-2
사유: Causality 는 정의상 dwarf/cluster/cosmo 동일. Path 3 cross 함수형은
regime-uniform 가정이 검증 필요. A7-2 는 gauge group 이 regime 별 동일하다는
보장이 가장 약함 (color charge vs U(1) vs ...). 보편성 측면에서 A7-1 우위.
(218자)

R6 (관측 가능성·falsifier 등록 관점)
ranking: Path 3 > A7-1 > A7-2
사유: a₀ 는 이미 rotation curve / lensing 으로 직접 측정 가능. A7-1 은
positive test 없이 위반 한계만 측정. A7-2 는 conserved current 직접 측정
경로가 cosmological scale 에서 미정. falsifier 등록의 *실효* 강도는
Path 3 이 가장 높음. (212자)

R7 (hidden DOF · Occam 관점)
ranking: Path 3 > A7-1 > A7-2
사유: A7-2 는 보존량 종류 + group + current 정의 3중 자유도. A7-1 은
light-cone + signal speed + unitarity 3중. Path 3 은 cross 함수형 + 2 pillar
선택 2중. Occam 관점에서 A7-2 최악. Hidden DOF 가 priori 회복의 직접
방해물. (215자)

R8 (cross-agent 모순 해소 관점, 메타)
ranking: Path 3 > A7-1 > A7-2
사유: L585 (A7-2 1위), L587 (Path 3 1위), L588 (A7-2 1위) 의 모순은 단일-
세션 평가가 *어느 axis 를 강조했는가* 에 따라 흔들렸음을 시사. 8 axis 종합
시 Path 3 가 7개 reviewer 중 4개에서 1위, A7-1 이 3개. A7-2 는 0개. L585·
L588 의 A7-2 1위 결론은 axis 1·2·8 의 axiom 비용 underweight 의 결과로
판정. (267자, 250자 한도 초과 — 메타 reviewer 특수성으로 인정)

---

## §3. 다수결 결과 + 만장일치 여부

8 reviewer 1위 표:
- Path 3: 5표 (R1, R4, R6, R7, R8)
- A7-1: 3표 (R2, R3, R5)
- A7-2: 0표

8 reviewer 최하위(3위) 표:
- A7-2: 8표 (만장일치 3위)
- Path 3: 0
- A7-1: 0

종합 ranking (Borda count, 1위=3pt / 2위=2pt / 3위=1pt):
- Path 3: 5×3 + 3×2 + 0×1 = 21
- A7-1: 3×3 + 5×2 + 0×1 = 19
- A7-2: 0×3 + 0×2 + 8×1 = 8

**합의 ranking: Path 3 > A7-1 > A7-2**

만장일치 여부:
- 1위 만장일치: 아니오 (Path 3 5/8, A7-1 3/8)
- 3위 만장일치: 예 (A7-2 8/8)
- 결정적 결론: A7-2 priori 회복 1순위 후보에서 *제외*. Path 3 vs A7-1 은
  근소차 (Borda gap 2pt). 단일 우위 미확정.

---

## §4. Cross-agent 모순 해소

L585 §4 (A7-2 우위 — 재발 위험 기준):
- Axis 7 (falsifiability) 만 단일 강조한 결과로 추정.
- 본 시뮬에서 axis 7 만 보면 A7-1 이 L (LIV 풍부), Path 3·A7-2 는 M.
- L585 결론은 *재현 불가*. axis 1·2·8 underweight 판정.

L587 §9 (Path 3 우위 — A7-2 4축 부담):
- Axis 1·2·4·8 (axiom 비용·hidden DOF·anchor·BCNF) 강조 시 Path 3 우위.
- 본 시뮬 Borda 결과와 *일치*. L587 평가가 가장 균형적이었음.

L588 §3 (A7-2 1위 — 3축 고위험):
- L585 와 유사하게 falsifiability 단일 강조 추정.
- 본 시뮬에서 A7-2 는 *어느 axis 에서도 1위 아님*. L588 결론은 다른
  세션과 *동일한 underweight 패턴*. 재현 불가.

해소: **L587 평가가 옳았음**. L585·L588 은 axis 단일 강조 (falsifiability
혹은 재발 risk) 로 인한 평가 편향. 분산 8-reviewer 시 평균 회귀로
A7-2 만장일치 3위. priori 회복 1순위는 Path 3 (또는 A7-1, 근소차).

---

## §5. 최종 권고: priori 회복 1순위 path

권고: **Path 3 (Q17 a4×a5 cross)** 를 1순위 후보로 진행.

근거 (회의적 — 좋은 점 생략, 약점 명시):
1. Path 3 도 postdiction 위험 H (axis 3) — amplitude 결과 본 후 cross 도출.
   단 이는 A7-1·A7-2 동등 H 라 *상대* 우위는 유지되나 *절대* 면죄 아님.
2. Path 3 의 anchor circularity (axis 4 H) 가 가장 큰 약점. a5 의 H₀
   pacing 이 priori 회복 단계에서 anchor reuse 로 잡힐 위험.
3. Path 3 cross 함수형 선택은 BCNF lock-in 단계에서 추가 hidden DOF 로
   잡힐 가능성. axiom 신규 0 이라는 이점이 함수형 선택 자유도로 일부 상쇄.
4. A7-1 과 Borda gap 2pt — 사실상 동급. 1차 protocol 통과 실패 시 A7-1
   백업으로 즉시 전환 가능하도록 병렬 준비 권장.

A7-2 는 *후보에서 제외*. 8/8 만장일치 3위 + 어느 axis 에서도 1위 아님.

---

## §6. R3+R4 BCNF protocol 적용 시 1순위 통과 가능성

Path 3 의 BCNF gate 통과 예상:
- Gate 1 (axiom 신규 추가 정당화): **PASS 예상**. 신규 axiom 0.
- Gate 2 (hidden DOF lock-in): **WARN**. cross 함수형 + 2 pillar 선택
  자유도가 lock-in 시 추가 평가 항목.
- Gate 3 (anchor circularity check): **WARN-FAIL 위험**. a5 의 H₀ anchor
  의존이 priori 회복 단계에서 reused-anchor 로 잡힐 가능성. 사전 anchor
  분리 작업 필요.
- Gate 4 (postdiction 시간순서): **WARN**. 결과 본 후 cross 도출. 단
  이는 모든 path 공통이라 protocol 이 절대 reject 하면 3 path 전체 사망.
  protocol 이 *상대* 평가하면 PASS 가능.
- Gate 5 (3-regime universal): **WARN**. cross 함수형의 regime-uniform
  검증 필요.

종합 통과 확률 (정성): ~50% (3 WARN, 1 PASS, 1 WARN-FAIL 위험).
A7-1 비교: ~40% (Gate 1 FAIL 위험 + Gate 4·5 PASS 가능). 큰 차이 아님.

권고: Path 3 진행 + A7-1 병렬 백업 + anchor 분리 사전 작업 우선.

---

## §7. 정직 한 줄

8/8 만장일치는 "A7-2 가 3위" 뿐이며, Path 3 vs A7-1 은 Borda 2pt 차이로
*어느 쪽도 단일 승자 아님* — L594 C1 은 "A7-2 제외" 로만 부분 해소되고,
1순위 path 의 절대적 확정은 BCNF protocol 실측 후로 이연된다.
