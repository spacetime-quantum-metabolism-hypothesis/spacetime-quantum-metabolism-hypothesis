# L638 — claims_status.json v1.3 갱신 Plan (PLAN ONLY)

- **세션**: L638
- **작성일**: 2026-05-02
- **단계**: PLAN ONLY (실제 JSON edit 0건, paper edit 0건)
- **선행**: L516 (v1.2 13-tier extension), L549/L552/L562/L566 (박탈 4),
  L557 (schema audit, 4 mismatch), L564 (fabrication 90%), L582/L584 (mass redef
  영구 종결), L596/L635 (erratum), L631 (N_eff 라벨), L634 (paper plan v3)
- **목표**: claims_status.json v1.2 → v1.3 변경 항목을 사전 명세화하여
  8인 Rule-A 리뷰 입력으로 사용
- **금지 (CLAUDE.md 최우선-1 준수)**: 본 문서는 plan 명세서 — JSON 본문 직접
  수정 0건, 수식 0줄, 파라미터 값 신규 도출 0건

---

## §1. v1.2 → v1.3 변경 항목 표

| # | 위치 (JSON 키) | 현재 (v1.2) | 변경안 (v1.3) | 출처 / 근거 | 종류 |
|---|----------------|-------------|---------------|-------------|------|
| 1 | `version` | `"1.2"` | `"1.3"` | 본 plan 채택 시 bump | meta |
| 2 | `last_synced_loop` | `"L516"` | `"L638"` | 본 sync | meta |
| 3 | `last_synced_date` | `"2026-05-01"` | `"2026-05-02"` (또는 8인 합의일) | 본 sync | meta |
| 4 | `schema_doc` | L516 13-value enum extension | + L638 v1.3 paradigm-shift / hidden-DOF / fabrication / 박탈 4 disclosure | L557, L582, L631, L634 | meta |
| 5 | `single_source_of_truth` | L495/L502 + cross-channel | + L549/L552/L562/L566 박탈 4 + L564 fabrication + L582 mass redef 종결 | L584 권고 | meta |
| 6 | `status_enum_active` | 13개 (PASS_STRONG 포함) | 동일 13개 유지하되, `PASS_STRONG` 항목에 `"permanent_zero": true` 메타 주석 키 추가 | L516 distribution `PASS_STRONG: 0` 영구화 | enum |
| 7 | `enum_extension_note_L516` 주석 | (L516 시점) | + L638 sync note (L584/L631/L634 cross-ref) 추가 한 줄 | L584/L631/L634 | meta |
| 8 | `self_audit_distribution.PASS_STRONG_permanent` | (없음) | 신규 키: `0 (permanent, L638 lock)` | L516 결과 영구화 | distribution |
| 9 | (limitations 신규) `L28-mass-redef-permanent` | — | ACK, permanent=true, section_ref=results/L582 + L584 권고; future_plan 에 "재개 금지, paper §6.5(e) erratum cross-ref" | L582, L584 | limitations |
| 10 | (limitations 신규) `L29-Neff-estimator-relabel` | — | ACK; L631 라벨 정정: `"Cheverud–Galwey"` → `"participation-ratio (Cheverud-Galwey 와 다름; 본 채널은 Bro et al. 2008 참여비율)"`. 기존 `L25-N_eff-falsifier-channel-correlation` `future_plan` 텍스트 동시 정정. | L631 | limitations + edit-existing |
| 11 | (limitations 신규) `L30-paradigm-shift-candidates-disclosure` | — | ACK, permanent=true; 박탈 4 후보 (L549, L552, L562, L566) 의 paradigm-shift 후보 등재 여부 = "박탈 cross-mention 의무". 즉, 4 박탈 path 는 "후보로 등재되었으나 박탈" 로 기록되어야 하며, 그 cross-mention 이 limitations 에 의무화. | L549/L552/L562/L566 | limitations |
| 12 | (limitations 신규) `L31-revoked-paths` (4 sub-row) | — | ACK, permanent=true; 4 박탈 경로 각각의 path id, 박탈 사유, paper §location, "재인용 금지" 플래그 | L549/L552/L562/L566 | limitations |
| 13 | (limitations 신규) `L32-fabrication-90pct` | — | ACK, permanent=true; L564 fabrication 90% 검출 결과 — 어떤 값/문장이 "후속 검증에서 fabrication 으로 분류" 되었는지 한 줄 + paper §6.5(e) erratum cross-ref | L564, L596, L635 | limitations |
| 14 | (limitations 강화) `L23-hidden-DOF-zero-param-overclaim` | k_hidden = 9~13, abstract sweep | + 9~13 의 *각 row 별 분해 표* (B1, η_Z₂, Λ_UV, dark-only, M16, Υ⋆, three-regime×2, scale stipulation×1–4) 및 어느 claim row 에 적용되는지 explicit cross-link (L516 demotion log row id 와 동일) | L495, L502, L516 | edit-existing |
| 15 | (claims 메타) `claims[*].status == PASS_STRONG` | (현재 0건) | "PASS_STRONG enum 영구 0" 명시화 — `self_audit_distribution.PASS_STRONG_permanent: 0` (#8) 와 일관, 추후 어떤 sync 도 신규 PASS_STRONG 행 추가 금지의 정책 진술 | L516 결과 + L638 lock | policy |
| 16 | (paper sync) `paper_sync_v3` (신규 메타 키) | — | paper plan v3 (L634) 의 어휘/section_ref 와 일치시키기 위한 sync 항목 — abstract / §6.5(e) erratum / §4.1 row caveat / §6.1.1 row 1–14 / §6.1.2 row 15–22 와 본 JSON 간 1:1 매핑 표 | L634 | meta |
| 17 | (limitations 강화) `L26-RAR-a0-NOT-universal` | aggregate-only | + L549 박탈 path (해당 시) cross-ref | L549 (해당 박탈이 RAR 인 경우) | edit-existing |

> **주의**: #11/#12/#13 의 박탈 4 항목 구체 (L549/L552/L562/L566 각 path id, 박탈 사유, 사례 분류) 는 본 plan 에서 inline 으로 기재하지 않는다 — 8인 Rule-A 가 해당 results/ 디렉터리를 직접 정독하여 entry 를 채운다 ([최우선-1] 사전 지도 금지 원칙).

---

## §2. L557 schema audit 4 mismatch 해소 매핑

L557 audit 에서 발견된 paper ↔ disk JSON 4 mismatch (구체 항목명은 L557 보고서 인용)
의 해소 경로를 v1.3 변경 #5/#9/#14/#16 에 분산 매핑.

| L557 mismatch # | 종류 | v1.3 해소 위치 | 비고 |
|-----------------|------|----------------|------|
| 1 | section_ref 불일치 (paper § vs JSON section_ref) | #16 paper_sync_v3 표 | 1:1 cross-ref 의무화로 drift 차단 |
| 2 | claim row label 표현 drift | #16 paper_sync_v3 + 8인 Rule-A 검수 | i18n.{en,ko}.label 표준 어휘 lock |
| 3 | mass redef 항 paper 잔존 vs JSON 미반영 | #9 L28-mass-redef-permanent + L584 권고 | paper §6.5(e) erratum cross-ref 의무 |
| 4 | hidden DOF count 표현 (paper "zero" vs JSON 9~13) | #14 L23 강화 (row 별 분해) + #5 SoT 갱신 | abstract sweep cross-link |

---

## §3. 8인 Rule-A 의무 항목 (이론 클레임 / 정책 변경)

본 v1.3 변경은 다수의 *이론 클레임 표현* 변경을 포함하므로, CLAUDE.md "L6 8인/4인 규칙"
(Rule-A 8인 순차 리뷰 / Rule-B 4인 코드 리뷰) 중 **Rule-A 8인 순차 리뷰 의무**.

다음 항목은 8인 Rule-A 통과 전 JSON 본문 반영 금지:

1. **#6, #8, #15 — `PASS_STRONG enum 영구 0` 명시화** : 정책 lock 변경. 추후 sync 가
   본 정책을 우회하지 못하게 하는 메타 lock 이므로 8인 합의 필수.
2. **#9 — L28-mass-redef-permanent** : "재개 금지" 플래그가 영구 정책. L582/L584 결과를
   8인이 단계별로 cross-check 한 뒤 lock.
3. **#11, #12 — 박탈 4 paradigm-shift 등재 / 재인용 금지** : 박탈 path 의 *재인용 금지*
   는 향후 모든 sync 에 대한 차단막. 8인 의무 cross-mention.
4. **#13 — fabrication 90% disclosure** : 정직성 클레임. paper 기조와 직결.
5. **#14 — L23 hidden DOF 행별 분해** : 각 row 의 hidden DOF 정량 분해는 이론 등급에
   직접 영향. 8인 row-by-row 검수.
6. **#16 — paper_sync_v3 cross-ref 표** : paper plan v3 (L634) 와의 1:1 매핑이
   sync drift 방지의 핵심. 8인 합의 후 lock.

다음 항목은 메타 / 라벨 정정으로 Rule-B 4인 sufficient (단, 8인 Rule-A 가 #1–#6 와
함께 일괄 처리하는 것 권장):

7. **#1, #2, #3 — version/loop/date bump** : meta only
8. **#4, #5, #7 — schema_doc / SoT / extension_note 텍스트 보강** : 인용 추가만
9. **#10 — L631 N_eff 라벨 정정** : 단순 라벨 교체 (의미 변화 없음)
10. **#17 — L26 박탈 cross-ref 추가** : cross-link 추가만

### 8인 Rule-A 진행 절차 (제안)

1. **방향 제공만**: 8인에게 v1.3 변경 항목 표 (§1) 제공, 각 row 의 *근거 results/ 디렉터리*
   path 만 제공. JSON 텍스트 자체는 제공 금지 — 각 인이 독립 도출.
2. **순차 리뷰**: 8인 각자 #1–#16 검토 후 자율 분담으로 합의문 산출.
3. **합의 후 JSON edit**: 합의 문서 → 별도 세션 (L638-followup) 에서 JSON 본문 갱신.
4. **Rule-B 4인 검수 (선택)**: JSON 갱신 후 schema 정합 / parsing 검증.

---

## §4. 정직 한 줄

본 v1.3 갱신은 어떠한 신규 PASS 도 만들지 않으며, 오직 (a) `PASS_STRONG = 0` 의
영구화, (b) hidden DOF 9~13 의 row 별 분해 disclosure, (c) 박탈 4 / fabrication 90% /
mass redef 영구 종결 의 한계 등재 — 즉 *불리한 사실의 정직 기록* 만으로 구성된다.