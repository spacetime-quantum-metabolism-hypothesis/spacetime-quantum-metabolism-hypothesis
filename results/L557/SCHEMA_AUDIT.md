# L557 — claims_status.json v1.2 Schema Audit

**Date**: 2026-05-02
**Scope**: disk-level integrity audit of `claims_status.json` (33 claims + 27 limitations)
against `paper/MNRAS_DRAFT.md` (PASS_STRONG advertisements) and against the v1.2 (post-L516)
13-value enum extension. **No file edits were performed** (Rule-A 미경유 → audit-only).

---

## §1. Schema version + 7-tier(실은 13-tier) enum 정의 위치

| 항목 | 위치 (claims_status.json line) | 값 |
|---|---|---|
| `version` | L2 | `"1.2"` |
| `schema_doc` reference | L4 | `paper/base.md §claims_status.json (line 480ff) + L516 13-value enum extension` |
| `last_synced_loop` | L6 | `L516` |
| `last_synced_date` | L7 | `2026-05-01` |
| **Active enum (claim status)** | L8–L22 | 13 values (목록 §2 참조) |
| **Legacy/deprecated enum** | L23 | `["PASS", "PASS_TRIVIAL"]` |
| **Demotion log (L516)** | L43–L54 | 6 rows: newton/bbn/cassini/ep/rar/bullet |

**중요**: 임무 설명서가 *"7-tier"* 라고 표현했지만, 디스크 schema 는 **13-value enum**
(`status_enum_active`, L8–L22) + **2-value legacy deprecated** (L23) 의 구조이다. 실제 13개:

```
PASS_STRONG, PASS_MODERATE, PASS_QUALITATIVE, PASS_IDENTITY, PASS_BY_INHERITANCE,
CONSISTENCY_CHECK, PARTIAL, POSTDICTION, PENDING, NOT_INHERITED,
OBS-FAIL, FRAMEWORK-FAIL, OPEN_PROVISIONAL
```

PASS-계열만 추리면 **5-tier** (`PASS_STRONG / PASS_MODERATE / PASS_QUALITATIVE /
PASS_IDENTITY / PASS_BY_INHERITANCE`). 임무 문구의 "7-tier" 는 아마 PASS 5종 + FAIL +
PASS-aliased PASS = 7 의 비공식 카운트일 가능성. **disk 정의는 13(active) + 2(legacy) = 15**.

`PASS_STRONG` 은 active enum 에 *남아있지만* (L9), L516 demotion 후 실 사용 카운트는 0
(self_audit_distribution L26). 즉 "정의는 살아있지만 모든 substantive 클레임에서 비워진"
상태로 의도된 자기심사 결과.

---

## §2. Grade enum 사용 카운트 (claims 33 + limitations 27)

### Claims 배열 (33 entries) — `status` 필드

| Status | self_audit_distribution 선언값 (L25–L42) | 실제 JSON 카운트 (Python) | 일치? |
|---|---:|---:|:---:|
| PASS_STRONG | 0 | 0 | OK |
| PASS_MODERATE | 5 | 5 | OK |
| PASS_QUALITATIVE | 1 | 1 | OK |
| PASS_IDENTITY | 3 | 3 | OK |
| PASS_BY_INHERITANCE | 8 | 8 | OK |
| CONSISTENCY_CHECK | 1 | 1 | OK |
| PARTIAL | 7 | 7 | OK |
| NOT_INHERITED | 8 | 8 | OK |
| FRAMEWORK-FAIL | 0 | 0 | OK |
| **TOTAL** | **33** | **33** | **OK** |

**선언값과 실제 카운트 100% 일치.** "PASS_combined_post_L516 = 6/33 = 18%" 도
PASS_MODERATE(5) + PASS_QUALITATIVE(1) = 6 으로 정확.

### Limitations 배열 (27 entries) — `status` 필드

| Status | 카운트 |
|---|---:|
| OBS-FAIL | 1 (L1-S8-worsening) |
| UNRESOLVED | 1 |
| OPEN | 6 |
| ACK | 10 |
| RECOVERY | 1 |
| NOT_INHERITED | 8 |
| **TOTAL** | **27** |

`UNRESOLVED / OPEN / ACK / RECOVERY` 는 active 13-value enum 에 *없는* 라벨 — limitations
배열에서만 쓰는 별도 vocabulary. enum_doc 에 명시 안 되어 있으나 schema 위반은 아님
(다른 필드이므로). **Drift 가능성**: limitations status enum 도 별도 명시되어야 향후
sync 안전.

### Legacy enum 잔재 검색 (전 파일 grep)

| Token | grep 카운트 (전체 파일) | claims 의 status 필드 사용? |
|---|---:|---|
| `"PASS"` (단독) | 1 (L23 legacy 목록 내부) | **0 (clean)** |
| `PASS_TRIVIAL` | 3 (L23 legacy + 2 caveat 텍스트 L169, L179 — "legacy PASS_TRIVIAL alias absorbed") | 0 status 필드 사용 |
| `FAIL` (substring) | 16 (대부분 caveat 텍스트의 "FAILS"/"FAIL" 서술) | status 필드는 OBS-FAIL 1건만 |

→ **legacy enum 의 status 필드 잔재 0건**. clean.

---

## §3. paper ↔ claims_status mismatch 위치

### §3.1 PASS_STRONG 표기 grep — paper/MNRAS_DRAFT.md

| Line | 컨텍스트 | 디스크 schema 와 정합? |
|---|---|---|
| L14 | "MOND a₀ 정량 PASS (verify_milgrom_a0.py: 0.42σ deviation, **PASS_STRONG**)" | **MISMATCH**: claims_status `rar-a0-milgrom` 은 `PASS_MODERATE` (L98). 디스크에 `PASS_STRONG` 0건. |
| L74 | "**A reader who only reads this MNRAS paper sees one PASS_STRONG numerical match**" | **MISMATCH** (동일 사유). |
| L131 | JSON expected schema 에서 `"verdict": "PASS_STRONG"` | **MISMATCH**: 실제 expected_outputs/verify_milgrom_a0.json (L8) `"verdict": "PASS"` — 본문 표기와 디스크 산출물도 불일치. |
| L192 | 체크리스트 "verify_milgrom_a0.py runs **PASS_STRONG** on reviewer machine" | **MISMATCH**: verify_milgrom_a0.py 는 `print("PASS" if dev < 2 else "FAIL")` (L19) — 출력은 `"PASS"` 문자열이지 `"PASS_STRONG"` 아님. |

**합계: paper 본문에 PASS_STRONG 4회 등장, 4회 모두 디스크 schema (claims_status v1.2 + 실제 verify 산출물) 와 불일치.**

### §3.2 verify_milgrom_a0.json (`paper/verification/expected_outputs/`) 자체 자기 모순

| Line | 필드 | 값 |
|---|---|---|
| L3 | `classification` | `"PASS_STRONG (substantive prediction, MOND a_0)"` |
| L8 | `expected.verdict` | `"PASS"` |

→ 한 파일 내에서 `classification=PASS_STRONG` ↔ `verdict=PASS` (legacy enum) 충돌. 임무
문구가 인용한 "디스크 JSON `verdict: "PASS"`" 는 이 파일이며, paper L131 의
`"verdict": "PASS_STRONG"` 는 **paper 내 인라인 schema 기재가 expected_outputs JSON 본체와 다른** 형태.

### §3.3 §4.1 RAR universality 철회 (claims_status L638–L645) ↔ paper cross-ref

claims_status.json `L26-RAR-a0-NOT-universal` (L637–L646):
- status: `ACK`
- future_plan (L641): "abstract / §4.1 row a₀ 에 'subset-stability ACK' 캐비엣 추가."
- 핵심 데이터: per-galaxy intrinsic spread 0.427 dex, K_X 1/4 PASS, environment FAIL.

paper/MNRAS_DRAFT.md cross-ref 검사:
- §1.4 (L52–L54): SPARC galaxy-by-galaxy 미수행 명시는 있음 — 그러나 "**universality 철회**"
  나 "K_X1/X2/X3 subset-stability FAIL" 또는 "0.427 dex per-galaxy intrinsic spread"
  *3건 모두 paper 본문에 없음*. grep `universality / K_X / 0.427 / per-galaxy intrinsic`
  결과 0 hit.
- §4.1 (L103–L104): RAR 정성 매칭 서술만 있음. subset-stability 캐비엣 없음.
- Abstract (L20–L28): "0.42σ deviation … PASS_STRONG" 라고 *자랑*. 철회 캐비엣 0.
- §6 limitations 7건 (L143–L151): "no SPARC galaxy-by-galaxy" 는 한 줄 (#3) 있으나
  *universality 부재* 와는 의미가 다름 (전자=미수행, 후자=수행 결과 부재).

→ **L26 future_plan 의 paper 반영 0/3 위치** (abstract, §4.1, §6 모두 미반영).

### §3.4 그 외 paper-vs-disk 의무 cross-ref 누락

L24 future_plan (L23 hidden DOF — "9 conservative ~ 13 expanded"): paper 에 hidden DOF
숫자 등장 0회. paper grep `hidden DOF / hidden.DOF / 9 hidden / 13 hidden` 0 hit.
(다만 본 MNRAS 가 *Path-γ galactic-only* 로 cosmology claim count = 0 을 명시하므로
hidden-DOF 는 companion JCAP 측 의무. MNRAS 측 의무성은 약함 — defensible.)

L25 (N_eff ≈ 4 falsifier independence): MNRAS scope 외 (cosmic-shear, BAO, RSD 모두
companion). paper 미반영은 의도된 scope 분리. **단, 임무 설명서 §3 의
"falsifier N_eff=4.44 명시" 는 디스크 값 `N_eff ≈ 4` (L633) 와 다름** — 0.44 의 출처
미상. claims_status 에는 4.44 정확값 없음.

L27 (Cassini channel-conditional): MNRAS scope 외 (PPN 은 cosmology/dark-only embedding
sector). 의도된 분리.

---

## §4. 추가 inner consistency 검증

### §4.1 33-claim 합산
self_audit_distribution.total = 33; 실제 claims 배열 length = 33; 카테고리 합산 0+5+1+3+8+1+7+8+0 = **33** OK. (PARTIAL 7 ↔ "POSTDICTION" 은 sigma0-three-regime
claim 의 caveat 안에 들어가 있고 별도 status 로 카운트 안 됨 — `POSTDICTION` enum 은
L8–L22 active 에 *나열돼 있지만 실 사용 0건*. 정의는 살아있고 사용은 비어있는 상태.)

### §4.2 hidden-DOF 0% headline 명시
- self_audit_distribution.substantive_only_post_L516 (L38): `"0/33 = 0% (every substantive row demoted by L502 AICc penalty)"` — **headline 명시 OK**.
- 이 0% 는 substantive PASS_STRONG 0 을 의미하지 hidden-DOF 0 이 아님. 임무 설명서가
  "hidden-DOF 0% headline" 이라고 부른 것은 실은 "PASS_STRONG 0%" headline. 정확한
  표현은 디스크에서 `substantive_only_post_L516` 키. hidden-DOF 자체는 9–13개로 0 아님
  (L23 enum_extension_note + L611 limitations L23-hidden-DOF-zero-param-overclaim).

### §4.3 falsifier N_eff
- L631 (limitations L25): `"N_eff ≈ 4 (active 5 detection 중)"` — disk 값 **4**, 임무
  문구의 4.44 와 차이 0.44. claims_status 어디에도 4.44 없음 (`grep 4.44` = 0 hit).
  **임무 prompt 의 4.44 는 외부 출처 (L498 이전 결과 가능성) 로, 디스크 v1.2 와 불일치
  가능성 있음**. L498 원자료(`results/L498/FALSIFIER_INDEPENDENCE.md`) 직접 확인 권고.

### §4.4 Demotion log 내적 정합
6 rows (L46–L53), 각각 `from / to / delta_aicc_honest / k_h_applicable / hidden_dof`
+ optional cross_channel_caveat. 모두 claims 배열의 status 변경과 일치
(newton/bbn/cassini/ep/bullet 5건은 PASS_MODERATE/PASS_QUALITATIVE 로 status 일치;
rar-a0-milgrom 은 신규 추가 row 로 PASS_MODERATE 이는 self_audit `claim_added_L516: +1`
명시와 일치). **OK**.

### §4.5 limitations status vocabulary drift
limitations 배열에서 사용되는 `UNRESOLVED / OPEN / ACK / RECOVERY` 4개 라벨은
`status_enum_active` (claims 용) 에 정의 없음. 별도 limitations enum 미문서화.
**Future drift 위험**: limitations status enum 도 schema_doc 에 명시 권고.

### §4.6 "PASS_STRONG" 정의는 살아있는 채로 사용 0
status_enum_active L9 에 PASS_STRONG 등재 + self_audit L26 = 0. 의도된 결과지만 *왜
정의를 남겨뒀는가* 설명이 enum_extension_note 에 있음 ("re-grading"의 결과로 비어진
것). 향후 어떤 claim 이 K_h_applicable=0 인 첫 번째 strict-passing 행이 나오면
PASS_STRONG 으로 승격 가능하도록 *정의는 살려둔 정책*. 정합.

---

## §5. 정직 한 줄

claims_status.json v1.2 자체 inner consistency 는 33-claim 합산·demotion log·자기심사
분포 모두 100% 정합이며 legacy enum status-필드 잔재 0건이지만, paper/MNRAS_DRAFT.md
4 위치 (L14·L74·L131·L192) 의 `PASS_STRONG` 광고는 디스크 schema (`PASS_MODERATE`) 및
실제 verify_milgrom_a0.json `"verdict": "PASS"` 와 모두 불일치하고, L26 RAR universality
철회의 paper-반영 의무 (abstract / §4.1 / §6) 는 0/3 미이행이며, 임무 prompt 가 인용한
falsifier `N_eff=4.44` 는 디스크값 `≈ 4` (L631) 와 0.44 차이로 출처 재확인이 필요하다.
