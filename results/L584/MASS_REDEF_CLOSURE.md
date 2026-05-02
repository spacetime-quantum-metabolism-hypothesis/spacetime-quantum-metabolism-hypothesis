# L584 — Mass Redefinition 영구 종결 sync (paper / claims_status / CLAUDE.md) — *방향 only*

**일자**: 2026-05-02
**상위 의존**: L582 `MASS_PATH1_RULE_A.md` (Mass Path 1 박탈, 4 트리거) — mass redef 7 path 전체 박탈/폐기/미달 → 영구 종결.
**산출 형태**: *방향* 권고만. 실제 paper / claims_status.json / CLAUDE.md 직접 edit 0건.
**의무**: 8인 Rule-A 순차 리뷰 후에만 sync 실행 (본 문서는 Rule-A 패키지의 입력).
**[최우선-1] 준수**: 본 문서 본문 어디에도 수식·파라미터 값·유도 경로 힌트 없음. 방향 어휘만.

---

## §0 영구 종결 사실 요약 (입력 전제)

- **mass redef 7 path** = kinetic ρ 계열 (R3–R7 5개) + causal-set valence 계열 (2개) — 모든 path 가 박탈 / 자발 폐기 / 트리거 미달 중 하나로 귀결.
- **L575 / L579 / L582** 누적 결론: rest mass μ 의 "이론적 재정의" 시도는 모두 트리거 발화 (수치 불일치, sector mixing, kinetic-to-mass mapping 모호성, Higgs sector silent import 등) 로 귀착.
- **결과**: paper §6 의 "13 hidden DOF disclosure" 문구는 **영구 유지 의무**. 13 DOF 를 "이론에서 도출됨" 으로 격상하려던 모든 경로 폐쇄.

---

## §1 paper/base.md §6.5(e) 갱신 *방향*

리뷰자 8인 합의 후 §6.5(e) (Limitations / disclosure 단락) 의 갱신 권고 *방향* 만 나열. 본문은 작성하지 않음.

1. **13 DOF disclosure 강화**:
   - 현 disclosure 가 "13 free parameter" 명시에 그쳤다면, **각 DOF 가 어느 sector 에서 silently import 되는지** 라벨링 필요. 특히 Higgs sector (rest-mass scale 의 진정한 출처) 가 외부에서 들어온다는 사실을 explicit 으로 적시.
   - 어휘는 "phenomenology framework with N-tier disclosed external inputs" 방향 — "0 free parameter" 광고 어휘 영구 폐기.

2. **mass redef 7 path 종결 cross-mention**:
   - L575 / L579 / L582 의 path 박탈 사실을 §6.5(e) 본문 또는 각주에 한 단락으로 cross-reference. 해당 단락은 "rest mass μ 를 이론 내부 양으로 재정의하려는 시도가 모두 실패하였음" 을 정직하게 적시하는 *방향*.

3. **rest mass μ 정의 모호성 1-paragraph 추가** *방향*:
   - axiom 1 의 "rest mass μ" 표기는 본문 변경 금지 (CLAUDE.md 규약). 단, §6.5(e) 에 "μ 의 출처 / 정의는 axiom 수준에서 외부 입력이며 본 framework 가 동역학적으로 결정하지 않는다" 는 취지의 단락을 disclosure 로 추가하는 *방향*.

4. **PRD Letter 진입 조건 재고**:
   - L6 재발방지 규칙 (Q17 / Q13+Q14) 에 더해, mass redef 영구 종결로 인해 PRD Letter 진입 조건이 더 멀어졌음을 §6 conclusion 부분에 정직하게 반영하는 *방향*. JCAP "정직한 falsifiable phenomenology" 포지셔닝 유지 강화.

---

## §2 claims_status.json v1.3 schema 변경 *방향*

직접 edit 금지. 8인 Rule-A 합의 후 별도 세션에서 patch 적용.

1. **새 limitation 항 추가** *방향*:
   - 키 명 *방향*: `mass_redef_permanent_closure` 류. 값에는 "L582 mass redef 종결, 13 hidden DOF 영구 disclosure 의무" 취지 텍스트.
   - cross-ref 필드: L575 / L579 / L582 결과 문서 path, 박탈된 7 path 식별자 (kinetic ρ R3–R7, causal-set valence 2 개).

2. **Higgs sector silent import 명시** *방향*:
   - 기존 limitation 블록 또는 새 entry 에 "rest-mass scale = Higgs sector 외부 입력" 사실 1 항 등재.

3. **PASS_STRONG enum 영구 0 명시화** *방향*:
   - L557 발견 (실제 13-tier) 이후 PASS_STRONG 인스턴스 0 사실을 schema 주석/설명 필드에 영구 명시. enum 자체는 유지하되 "현재 어떤 claim 도 이 등급에 도달하지 않으며, mass redef 종결로 향후 진입 경로 한정됨" 취지 명시.

4. **L582 박탈 4 path 새 limitation 등재** *방향*:
   - kinetic ρ R3–R7 4 트리거 + causal-set valence 3 트리거 외 5 건 — 각 박탈 사유와 트리거 카운트를 limitation 또는 closed_paths 류 entry 로 등재.

5. **schema 7-tier ↔ 실제 13-tier 정합** *방향*:
   - 문서화된 7-tier 와 코드/데이터의 13-tier 간 격차를 schema description 에 명시하거나, tier 매핑 table 을 별 필드로 추가하는 *방향*.

---

## §3 CLAUDE.md 등록 권고 *방향*

직접 edit 금지. 권고 문구 *방향* 만 제시 (실제 등재 시 한 줄 요약):

> L582 — mass redefinition 영구 종결. 7 path 모두 박탈/폐기/미달 (kinetic ρ R3–R7 4 트리거 + causal-set valence 3 트리거 외 5건). 13 DOF disclosure 영구 유지 의무. axiom 1 'rest mass μ' 본문 변경 금지.

본 한 줄은 기존 "L30~L33 재발방지" 형 블록과 동등한 위치 (별도 "L582 재발방지" 섹션 또는 기존 누적 블록 말미) 에 등재 *방향*.

---

## §4 paper 본문 어휘 통일 *방향*

8인 Rule-A 후 paper 전역 검색·치환 권고 *방향*:

- **영구 금지 어휘**:
  - "통합 이론" / "unified theory" — phenomenology pivot (L569) 와 정합 위반.
  - "0 free parameter" / "zero free parameters" — 13 DOF disclosure 와 모순.
  - "priori 도출" / "derived a priori" — mass redef 종결로 도출 주장 근거 소멸.

- **권고 대체 어휘**:
  - "phenomenology framework" / "falsifiable phenomenology"
  - "13 hidden DOF disclosed" / "N-tier disclosed external inputs"
  - "data-anchored parametrisation" 류 (도출 주장 회피)

- 절차 *방향*: paper/base.md 전역 grep → 영구 금지 어휘 인스턴스 리스트업 → 8인 Rule-A 패키지 입력 → 합의 후 일괄 치환.

---

## §5 schema 정합 (7-tier ↔ 13-tier) *방향*

- **현 상태**: claims_status.json 문서/주석은 7-tier 로 표기, 실제 코드·데이터 사용은 L557 이후 13-tier 로 운용. drift 상태.
- **권고 *방향***:
  1. schema description 필드에 "공식 enum 7-tier, 운용 시 sub-tier 6 개 추가 → 실효 13-tier" 주석 추가.
  2. PASS_STRONG enum 항을 유지하되 "current_count: 0" 명시 필드로 영구 불변 사실 고정.
  3. L582 박탈 path 들을 closed_paths 또는 dead_ends 류 별 array 로 분리 등재 (limitations 와 구분).
- 어떤 형태든 **schema 자체를 본 세션에서 직접 수정하지 않음**. 8인 Rule-A 합의 후 별도 patch.

---

## §6 정직 한 줄

본 L584 는 sync *방향* 만 정의하며, 실제 paper / claims_status.json / CLAUDE.md 직접 edit 0건. mass redef 영구 종결은 L575 / L579 / L582 누적 결과이며, 본 문서는 그 사실을 코덱스에 반영할 때의 어휘·구조 가이드일 뿐. 8인 Rule-A 순차 리뷰 통과 전까지 어떤 sync 도 실행되지 않는다.

---

## 부록 A — 8인 Rule-A 리뷰 패키지 권고 입력

- 본 문서 (`results/L584/MASS_REDEF_CLOSURE.md`)
- `results/L582/MASS_PATH1_RULE_A.md` (박탈 사유 4 트리거)
- L575 / L579 결과 문서 (박탈 / 폐기 / 미달 사유)
- 현 `paper/base.md §6.5(e)` 본문 (sync 대상 비교용)
- 현 `claims_status.json` (schema diff 입력)

## 부록 B — 4인 Rule-B 코드 리뷰 비대상

본 L584 는 *방향* 문서 (이론·정책 클레임) 이므로 Rule-A 8인 순차 리뷰 대상. 코드 patch 가 발생하는 sync 단계 (claims_status.json 실제 갱신) 에서만 Rule-B 4인 자율 분담 코드 리뷰 별도 진행 권고.
