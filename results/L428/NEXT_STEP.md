# L428 NEXT_STEP — 8인팀 다음 단계 설계

**목표**: superfluid analogue 경로 — 응집물질의 vacuum normal-state / superfluid-state
두 phase 와 SQT n field 의 두 phase 를 *대응 후보로 검토* 할 수 있는지 방향 설계.
**제약** (CLAUDE.md 최우선-1): 구체적 수식·파라미터·계수 사전 지시 절대 금지. 방향만.
**방법**: 8인 자율 토의 (Rule-A). 자연 분담된 매핑 path 3개로 수렴.

---

## Path (i) — Volovik 두-phase 구조의 SQT 매핑 후보

**아이디어 방향**: Volovik 프로그램의 normal vs superfluid 두 component 를
SQT n field 의 *두 운영 상태* (예: 미응집 영역 vs 응집 영역, 또는 generation
지배 vs absorption 지배) 와 phenomenology 수준에서 대응시킬 수 있는지 탐색.

**탐색 keyword**:
- Volovik 의 emergent metric 도출 (He-3 A-phase Bogoliubov spectrum)
- 응집체 두 component hydrodynamics (Landau two-fluid model)
- SQT axiom 3 (Γ₀ 균일 생성) 과 axiom 1 (물질 흡수) 의 *방향성 차이* 가
  두-component 분리 후보로 작동 가능한지
- order parameter / phase 변수 의 SQT 측면 식별

**판정 기준**:
- 매핑이 SQT axiom L0–L4 의 형식 변형 *없이* 가능한가 (trivial analogy 수준)
- 새 axiom 추가 필요 시 axiom 4 5번째 축 후보 (Causet vs GFT) 와의 양립 여부
- 매핑 결과 SQT 가 second sound / roton / vortex quantization 류 *예측* 을
  만들 수 있는가 — 단순 narrative 동형이면 trivial 명시 후 격하

## Path (ii) — n field 에 두-component 구조 부여 (framework 확장)

**아이디어 방향**: SQT n field 를 단일 scalar 가 아닌 두 component
(예: normal density + condensed density) 로 일반화하여 Volovik 동형 후보를
*prediction 채널* 로 격상시킬 수 있는지 검토.

**탐색 keyword**:
- 응집체 mean-field theory 의 두 fluid 분리
- Z₂ → U(1) symmetry 확장 비용 (paper §6.1.2 row #19 와 직접 충돌 지점)
- emergent metric 이 두-component 의 어느 쪽에서 나오는가 (Volovik 응답: 두 쪽 모두)
- SQT 에서 두-component 분리가 Λ origin circularity (§5.2) 에 영향 주는지

**판정 기준**:
- framework 확장 비용 (axiom 추가 1–2개) vs 회복되는 claim 수
- 확장 후 §6.1.2 row #16 NOT_INHERITED → POSTDICTION 격상 가능성
- 동시에 row #18 (GFT BEC), #19 (BEC nonlocality) 도 함께 회복되는가
  (Z₂ → U(1) 확장 시 sister gap 동시 회복 가능성 검토)

## Path (iii) — Trivial 동형 명시 + 인용 격하 (정직 경로)

**아이디어 방향**: 회복 시도 비용이 회수 claim 가치를 초과한다면,
paper §6.1.2 row #16 의 "trivial 동형 명시 또는 인용 삭제" 옵션을 정직
선택. Volovik 인용을 motivation/inspiration 수준으로 격하하고 "구조적 동형
주장은 SQT axiom 에 없음" 을 명시.

**탐색 keyword**:
- §6.1.2 row #22 의 "5 program PASS 0/5" 표기 정형화
- "구조적 동형" 의 형식 정의 (narrative parallel vs formal isomorphism)
- §6.1 한계 표 강화 표현 후보 (L420 row #13 강화 사례 참조)

**판정 기준**:
- caveat 강화 표현이 reviewer 비판 #6, #8 (예측력 부재 + 동형 정의 부재) 을
  명시적으로 흡수하는가
- paper narrative 의 "BEC 응집체" 단어 사용 빈도 재조정 필요성

---

## 8인팀 합의 — 우선순위

1. **Path (iii) 우선**: framework 확장 비용 (Path ii) 이 매우 높고 (axiom 추가
   + Z₂→U(1) 변경 + #18/#19 와 sister gap 합동 회복 필요), L420 Λ_UV 사례와
   유사한 "도출 시도 후 caveat 강화" path 가 정직 비용 최소.
2. **Path (i) 차선**: 4인팀이 phenomenology 매핑 후보를 explicitly 시도해
   trivial 수준 일치 / 구조적 일치 어느 쪽인지 분류.
3. **Path (ii) 후순위**: framework 확장은 axiom 4 5번째 축 결정 (Causet vs
   GFT) 과 함께 통합 처리해야 효율적. L428 단독 범위 초과.

**도출 실패 시 정직 권고**: §6.1.2 row #16 caveat 을 다음 방향으로 강화.
> "Volovik 2-fluid analogue 는 SQT n field 의 단일 component 구조와 phase 구조
> 부재로 *narrative parallel* 수준이며, axiom L0–L4 에서 step-by-step 도출되지
> 않는다. 따라서 Volovik 인용은 motivation 수준이며 5 program 동형 PASS 카운트에
> 기여하지 않는다 (row #22 '0/5' 의 일부)."
