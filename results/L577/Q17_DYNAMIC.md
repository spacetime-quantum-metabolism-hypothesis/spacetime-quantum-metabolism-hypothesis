# L577 — Q17 amplitude-locking 동역학 도출 *방향* 탐색

> **[최우선-1] 절대 준수**: 본 문서는 *방향*만 제공한다.
> 수식 0줄, 파라미터 값 0개, "이 방정식을 써라" 류 지시 0건, 도출 0건.
> 모든 path 는 *이름과 회의적 압박* 만 기술한다.
> 실제 동역학 도출은 8인 팀이 본 문서의 방향만 듣고 독립 수행한다.

> **컨텍스트 요약**
> - Q17 = Δρ_DE 의 amplitude 가 Ω_m 와 locking. 현재 paper L513 §6.5(e) 에서
>   "exact coefficient = 1 은 E(0)=1 normalization 귀결, 동역학적 도출이 아님"
>   으로 partial only 판정.
> - L552 RG 패키지 (Wetterich-style fixed-point 기반 Q17 동역학) 박탈 사유:
>   anchor 이동 (Λ_obs → k_IR) + truncation 의존성.
> - 사용자 새 권한: 4-pillar 외부 axiom 추가 가능 + 출판 회귀 비용 0.
> - PRD Letter 진입 조건: Q17 완전 달성 OR (Q13 + Q14 동시).
>   Q13 (S_8 +1.14% structural worsening) + Q14 (lensing) 미달 상태.
> - 본 L577 은 Q17 path *방향* 만 평가; 도출 자체는 후속 세션 8인 팀.

---

## §1. 5-Path 평가표

각 path 는 (a) 방향 이름, (b) hidden DOF 비용, (c) anchor-free 가능성,
(d) postdiction (사후 끼워맞춤) 위험을 *질적으로* 만 기술한다.
숫자/수식/파라미터 값은 일절 적지 않는다.

| # | Path 방향 이름 | Hidden DOF 비용 | Anchor-free 가능성 | Postdiction 위험 | 1줄 회의 |
|---|---|---|---|---|---|
| 1 | 새 axiom A7 (DE-mass coupling 직접 명시) | 높음 — 외부 축 추가는 4-pillar 가 7-pillar 로 확장, 기존 일관성 검증 전부 재실행 | 가능 — coupling 자체가 정의이므로 anchor 불필요 | 낮음 (정의 차원); 단 Q17 외 기여 없으면 ad hoc | 가장 직관적, 그러나 "axiom 추가 = 도출 아님" 비판 직격 |
| 2 | a3 (emission balance) 강화 — Γ₀ 를 mass density 종속으로 격상 | 중간 — 기존 a3 내 함수 형태 확장; 새 functional 자유도가 hidden DOF | 부분 가능 — Γ₀ 의 mass-dependence 가 기존 mass scale 만 사용하면 anchor-free | 중간 — Γ₀(t) 단독 (L549 P3a) 박탈 패턴 재발; 함수 형태 선택 자유도가 fit 으로 흡수될 위험 | L549 P3a 박탈 와 구조적으로 동형. 단일 보조 가정으로 DOF 추가하는 패턴 회피 의무 |
| 3 | a4 + a5 cross — geometric projection × Hubble pacing | 낮음 — 두 기존 axiom 의 곱 구조만 활용, 새 자유도 0 명목 | 높음 — 두 axiom 모두 anchor-free | 높음 — cross product 의 정확한 구조가 결과를 강제하지 않으면 "왜 이 곱인가" 의 정당화 부재 | DOF 비용은 가장 낮지만 도출의 *유일성* 입증 부담이 가장 큼. D4 5th path 와 결합 가능성 사전 점검 필수 |
| 4 | Wetterich RG fixed point + anchor-free protocol + 4번째 regime 사전 등록 | 중간 — RG truncation 자유도는 그대로; 단 사전 등록으로 postdiction 차단 | 의도적 anchor-free (L552 R4 응답) | 중간 — L552 박탈 직접 사유 (anchor circularity) 를 protocol 로 봉합하는 시도. Protocol 자체가 충분조건인지 외부 검증 필요 | "박탈 사후 보정" 인상 강함. 4번째 regime 의 사전 예측이 *진짜* falsifiable 한지 8인 팀 합의 필수 |
| 5 | 외부 framework import (dilaton-radion / GSL / TOV-cosmological 등) | 매우 높음 — 외부 framework 자체의 hidden DOF 가 SQMH 로 통째 이전 | 외부 framework 의존 (대부분 anchor 있음) | 높음 — 외부 framework 의 fit-to-data 이력이 그대로 SQMH 위험으로 이전 | 가장 비싼 path. Q17 외 부수 효과 (e.g. Q13/Q14 동시 해결) 가능성으로만 정당화 가능 |

> **공통 경고**: 어떤 path 든 *수식 형태* 를 사전에 적시하면 [최우선-1] 위반.
> 위 표는 path 의 *이름과 위험* 만 기술하며, 실제 도출 경로는 8인 팀 자율.

---

## §2. Top-2 Path

회의적 압박을 통과할 잠재력 기준 (DOF 비용 ↓ + anchor-free ↑ + postdiction ↓
+ 다른 Q 항목 동반 해결 가능성):

1. **Path 3 (a4 × a5 cross)** — DOF 비용 최저, anchor-free 자연스러움 최고.
   유일성 입증 부담이 크지만, 4-pillar 내부 도출이라는 점에서 "pillar 외부
   axiom 추가 없이" Q17 을 달성하는 유일한 후보. D4 5th path 결합 가능성.

2. **Path 1 (axiom A7)** 또는 **Path 4 (Wetterich + protocol)** — tie.
   - A7: 정직한 외부 axiom. "도출 아님 = 정의" 비판을 정면 수용하되, 외부
     axiom 추가가 출판 회귀 비용 0 환경에서 허용되므로 cost-benefit 가능.
   - Wetterich + protocol: L552 박탈 직접 응답. anchor-free protocol +
     4번째 regime 사전 등록이 8인 팀 합의로 통과되면 Q17 동역학 후보 부활.

> Path 2 (a3 강화) 는 L549 P3a 박탈 패턴 재발 위험으로 후순위.
> Path 5 (외부 framework) 는 Q13/Q14 동반 해결 시나리오에서만 검토.

---

## §3. Q17 완성 시 PRD Letter 진입 시나리오

PRD Letter 진입조건: **Q17 완전 달성** OR **(Q13 + Q14 동시 달성)**.

- **Q17 완성 단독**: PRD Letter 진입 조건의 절반 (OR 의 첫 항) 충족.
  Q13/Q14 미달 상태 그대로 → Letter 영구 차단은 *해제*. 즉 Q17 완성만으로
  Letter 진입 가능.
- **Q13/Q14 동시 미달 채로 Q17 부분 (현재)**: Letter 영구 차단 유지.
- **Q17 + Q13 + Q14 동시 달성**: Letter 강진입 (조건 양쪽 모두 충족).

> 회의 한 줄: "Q17 완전 달성" 의 판정 권한은 8인 팀 합의 + 외부 (코드리뷰 4인)
> 검증. 단일 에이전트 또는 단일 path 도출만으로 "완전 달성" 선언 금지.
> L513 §6.5(e) 의 "normalization 귀결" 비판이 8인 팀 만장일치로 해소되어야
> "완전" 으로 인정.

---

## §4. 사용자 권한 갱신 환경에서의 path 평가

- **사용자 axiom 수정 권한 부여** → Path 1 (A7 추가) 가 정책상 허용됨.
  L552 이전 환경에서는 4-pillar 보존이 hard constraint 이라 Path 1 자체가
  봉쇄. 본 권한 갱신으로 Path 1 가 실질 후보로 부상.
- **출판 회귀 비용 0** → 박탈 사후 보정 (Path 4) 의 사회적 비용이 0. 단
  과학적 비용 (8인 팀 신뢰도, 외부 referee 평가) 은 그대로. "공짜" 아님.
- **결론**: 권한 갱신은 Path 1, 4 의 *허용 여부* 를 변경시킬 뿐, *통과
  여부* 는 8인 팀 회의적 검증에 그대로 의존. 권한이 도출의 질을 보장하지
  않는다.

---

## §5. 4-pillar 외부 axiom 추가 시 hidden DOF 갱신

현재 hidden DOF 범위: **9–13** (4-pillar 내부 자유도 추정).

- **Path 1 (A7 추가)**: hidden DOF 상한 +k (k = A7 도입으로 추가되는
  functional / parametric 자유도). 8인 팀이 A7 의 형식을 정한 후에야 k
  결정. 사전 추정 금지 ([최우선-1]).
- **Path 2 (a3 강화)**: 기존 axiom 내부 functional 확장 → hidden DOF 상한
  부분 증가 (a3 내부 함수 자유도). 정확한 증분은 도출 후 측정.
- **Path 3 (a4 × a5 cross)**: 새 자유도 명목 0. 단 cross 의 정당화 차원이
  meta-DOF 로 작동할 수 있음 (선택의 자유). 8인 팀 평가.
- **Path 4 (Wetterich + protocol)**: hidden DOF 는 RG truncation 차수 +
  protocol 외부 등록 사전 예측 항목 수. anchor-free protocol 자체는 DOF
  소비 아닌 falsifiability 강화.
- **Path 5 (외부 framework)**: 외부 framework 의 free parameter 수 그대로
  이전. 일반적으로 가장 큰 DOF 폭증.

> 갱신 결과는 path 채택 후 8인 팀이 실측 (parameter counting + Bayesian
> evidence) 으로 결정. 본 §5 는 *방향* 만 적시.

---

## §6. 정직 한 줄

> **권한 확장은 path 의 허용을 늘렸을 뿐, Q17 동역학 도출의 *질* 을 보장하지
> 않는다. 5 path 모두 회의적 압박 (anchor-free, postdiction 차단, hidden DOF
> 명시, [최우선-1] 준수) 을 통과해야 비로소 "동역학적 도출" 자격을 얻는다.**

---

## 산출 메타

- 작성일: 2026-05-02
- 산출 위치: `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L577/Q17_DYNAMIC.md`
- 후속: 8인 팀이 본 §2 top-2 path 중 1개를 자율 선택하여 독립 도출.
  코드/시뮬레이션 작업은 4인 코드리뷰 팀 별도.
- CLAUDE.md 정합: [최우선-1] 절대 준수 확인 (수식 0, 파라미터 값 0,
  도출 0, 방향 + 회의적 압박만).
- 단일 에이전트 결정 금지 — 본 문서는 *방향 후보 평가* 이며 path 채택
  결정권은 8인 팀.
