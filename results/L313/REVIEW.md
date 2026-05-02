# L313 REVIEW — 4인 P/N/O/H

대상: ATTACK_DESIGN.md (Section 3 Branch B finalization plan).

## P (Positive)
- 3.3 mock-injection caveat 를 본문 단락으로 끌어올린 결정 옳음 — L272 결과 footnote 강등 시 reviewer 신뢰도 즉시 추락.
- 3.6 fixed-θ vs marginalized Δ ln Z 분리표 구조는 L6 재발방지 규칙 (Occam-corrected vs fixed-θ 혼동 금지) 정확히 준수.
- 3.8 forecast 단락이 falsifiability 를 paper 본문에 박아둠 — JCAP 타깃 "정직한 falsifiable phenomenology" 포지셔닝 (L6) 와 정합.
- 8 sub-section 분담이 8인 1대1 매핑이라 누락 위험 낮음.

## N (Negative)
- §3.7 (boundary 미결정성) 이 §3 안에 있으면 결과 단락 흐름 깨짐 — discussion 으로 이동 권고. ATTACK_DESIGN open issue 에 이미 적시되어 있으나 default 위치를 §4 로 잡는 편이 안전.
- §3.5 LOO 단락에서 ΔAICc 41–89 숫자만 인용하면 reviewer 가 "within-SPARC 검증" 으로 오독 위험. "leave-anchor-out (cross-regime), not leave-galaxy-out" 명시 필수.
- Table (σ posterior) 가 marginalized chain 기반인지 fixed-θ MAP 기반인지 ATTACK_DESIGN 에 미명시. 표 caption 에 source chain ID 박아야 함.
- §3.4 smooth alternative 가 "AICc 표 1행" 만으로 끝나면 reviewer 가 step-vs-smooth 미결정성을 놓칠 수 있음 — Δχ² 와 ΔAICc 모두, 그리고 부호 명시.

## O (Open question)
- L273 GMM k=2 (SPARC alone) 결과를 §3.2 또는 §3.5 어디에 넣을지 미정. "부분 지지" 라는 표현이 §3.2 결과 단락에 들어가면 over-claim 우려.
- §3.8 P9 dSph forecast 가 anchor 추가 시 σ_galactic 분리도 향상을 정량 보일 수 있는지 — Fisher matrix 토이 필요 여부 확정 필요.
- "regime boundary 가 sharp 인지 crossover 인지 데이터로 결정 불가" 를 본문에 명시할 때 RG FP (L301) 측 예측 (sharp vs smooth) 가 있는지 A 담당이 다시 확인해야 함.

## H (Honest concern)
- Branch B 의 marginalized Δ ln Z = 0.8 은 사실상 "데이터가 LCDM/단일σ 와 BB 를 구분 못함" 을 의미. §3 전체가 phenomenological 로 묶여도 reviewer 가 "왜 본 논문 main result 인가" 물을 위험. §1 (intro) 에서 BB 를 "main detection" 이 아니라 "structural hypothesis under test" 로 일관 표기되었는지 cross-check 필수.
- mock-injection 100% FDR 은 매우 강한 negative signal. §3.3 에 1단락 배치는 적절하나, abstract 와 conclusion 양쪽에도 동일 caveat 가 들어가지 않으면 selective reporting 비판 가능.
- L196 fixed-θ ΔlnZ=13 숫자가 과거 loop 에서 단독 인용된 이력 있는지 (CLAUDE.md L6 규칙 위반 흔적) §3 작성 전 grep 권고.
- 등급 ★★★★★ -0.05 상태에서 §3 over-claim 한 줄로 등급 하락 가능. 8인 모두 "정직 우선, 결정성 양보" 유지.

## 종합 판정
조건부 GO. §3.7 → §4 이동, Table caption chain ID 명시, LOO "cross-regime" 명시, abstract/conclusion mock caveat cross-write 4건 반영 후 LaTeX draft 진입.
