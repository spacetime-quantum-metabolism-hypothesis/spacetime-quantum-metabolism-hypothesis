# L642 — Schema Mismatch 정정 Plan

**상태**: PLAN ONLY — 실제 edit 0건, 수식 0줄.
**선행**: L637 (verify 실행으로 mismatch 식별), L638 (claims_status v1.3 plan).
**후행**: 8인 Rule-A 검토 → 별도 LXX 에서 실제 edit.
**작성일**: 2026-05-02.

---

## §1 — M1 / M2 / M3 정정 plan 표

| ID | 발견 위치 | 현재 상태 (As-Is) | 정정 plan (To-Be) | 변경 대상 | 적용 LXX |
|----|----------|-------------------|--------------------|----------|---------|
| **M1** | milgrom verify 출력 vs JSON vs paper plan v3 | stdout `PASS` / JSON `classification: PASS_STRONG` / paper `moderate-pass` — 3개 어휘 동시 존재 | 3개 채널 모두 `PASS_MODERATE` 로 통일 (paper v3 `moderate-pass` 는 표기형만 정합) | (a) `verify_milgrom*.py` print 라벨, (b) `expected_outputs/milgrom*.json` `classification` 필드, (c) paper plan v3 표기 cross-ref | 별도 LXX |
| **M2** | 7 JSON schema 비대칭 | 일부 JSON `verdict` 만, 일부 `classification` 만, 일부 둘 다 — key 비대칭 | 7 JSON 전체 **2-field 통일**: `classification` (13-tier enum, L557 sync) + `verdict` (binary `PASS`/`FAIL` 파생) | 7 expected_outputs JSON 일괄 schema 정정 | 별도 LXX |
| **M3** | monotonic 17σ (논문) vs 12.1σ (toy) | JSON note 에 정직 기재 완료 (L633/L637 disclosed) | **추가 sync 불요**. paper plan v3 §5 에 toy↔full cross-ref 한 줄 명시 권고 | paper plan v3 §5 footnote (텍스트 한 줄 추가만) | 별도 LXX |

---

## §2 — Sync target 어휘 결정 (M1)

**결정**: `PASS_MODERATE` 단일 어휘.

근거:
- L513/L515 milgrom 등급 부여 sync (이전 lab note 기록).
- Paper plan v3 `moderate-pass` 와 표기 정합 (대문자/하이픈 표기 차이만; 의미 동일).
- `PASS_STRONG` 은 milgrom 결과보다 높은 강도를 시사 — 데이터 정합성 위반.
- bare `PASS` 는 13-tier enum 의 어느 tier 인지 불명확 — schema 위반.

폐기 어휘:
- `PASS` (13-tier 미정합).
- `PASS_STRONG` (강도 과대 표기).

---

## §3 — L638 v1.3 plan 과 sync 항목

| L638 v1.3 항목 | L642 plan 정합성 |
|----------------|------------------|
| 13-tier enum (L557) 강제 | M2 정정 plan 에 직접 연결 — `classification` 필드 enum 검증 |
| `verdict` (binary) + `classification` (tier) 2-field 표준 | M2 To-Be 와 동일 |
| milgrom tier sync `PASS_MODERATE` | M1 To-Be 와 동일 |
| toy↔full disclosure note 의무 | M3 현 상태 (이미 disclosed) 와 정합, paper cross-ref 권고만 추가 |

→ L642 plan 은 L638 v1.3 의 하위 집합이며 충돌 없음.

---

## §4 — 8인 Rule-A 의무

본 plan 의 **모든 항목** 은 이론/clae 어휘 변경 (PASS_MODERATE / 13-tier enum) 을 포함하므로 Rule-A (8인 순차 리뷰) 필수.

승인 흐름:
1. L642 plan (현 문서) 작성 완료.
2. 8인 Rule-A 순차 리뷰 — M1 어휘, M2 schema 통일, M3 cross-ref 권고 각각 sign-off.
3. 8/8 합의 시 별도 LXX 에서 실제 edit (verify_*.py / JSON / paper).
4. 7/8 이하 합의 시 plan 재작성.

코드만 변경 (실제 edit) 단계 진입 시 추가 Rule-B (4인 코드리뷰) 도 의무.

---

## §5 — 정직 한 줄

본 문서는 plan-only 이며, M1/M2/M3 의 실제 정정은 8인 Rule-A 통과 후 별도 LXX 에서만 수행한다 — 본 작성으로 인한 verify_*.py / expected_outputs JSON / paper / claims_status / 디스크 변경 0건.
