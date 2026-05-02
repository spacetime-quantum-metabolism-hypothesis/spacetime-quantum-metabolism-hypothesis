# L460 — Cross-Coherence Audit (paper/base.md ↔ README.draft.md ↔ claims_status.json ↔ verification/ ↔ FAQ)

Date: 2026-05-01
Scope: 32-claim distribution, enum value count, 22-row limitations, emoji ↔ enum mapping coherence across all surfaced artefacts.
Method: programmatic count via `python3 -c "json.load(...)"`, full-text grep for distribution markers, side-by-side diff of self-audit summaries.

## 0. Inputs scanned

| Artefact | Path |
|---|---|
| Single source of truth (machine-readable) | `claims_status.json` (v1.1, last_synced_loop=L436) |
| Paper master | `paper/base.md` (1548 lines) |
| Public-facing summary | `README.draft.md` |
| Verification scripts | `paper/verification/{verify_*.py, README.md, README.ko.md, expected_outputs/}` |
| Verification audit (raw evidence) | `paper/verification_audit/audit_result.json` and R1–R8 |
| FAQ | `paper/faq_en.md`, `paper/faq_ko.md` |

## 1. 32-claim distribution — UNIFORM (post-fix)

`claims_status.json` programmatic count: PASS_STRONG=4, PASS_IDENTITY=3, PASS_BY_INHERITANCE=8, CONSISTENCY_CHECK=1, PARTIAL=8, NOT_INHERITED=8 → total 32 (matches `self_audit_distribution`).

| Surface | Distribution string | Match? |
|---|---|---|
| `claims_status.json` (counted) | 4/3/8/1/8/8 = 32 | — (canonical) |
| `claims_status.json::self_audit_distribution` | 4/3/8/1/8/8 + FRAMEWORK-FAIL 0 | ✅ |
| `paper/base.md` §0/TL;DR L149 | substantive 13% (4) + identity 9% (3) + inheritance 25% (8) + CONSISTENCY_CHECK 3% (1) + partial 25% (8) + NOT_INHERITED 25% (8) | ✅ |
| `paper/base.md` L495 (enum block prose) | identical breakdown, sum=32 ✓ | ✅ |
| `paper/base.md` §6.5(e) L622 | identical breakdown | ✅ |
| `README.draft.md` L21 | identical breakdown | ✅ |
| `paper/faq_en.md` L58 / `faq_ko.md` L52 | "13% (4 claims) substantive ... raw 28% PASS_STRONG headline" | ✅ |

Result: distribution numbers match across all surfaces. The "양면 표기 의무" (raw 28% headline + substantive 13%) is honoured everywhere it appears.

## 2. Enum active value count — FIXED (was 11→10 drift)

`claims_status.json::status_enum_active` array length: **10** entries (PASS_STRONG, PASS_IDENTITY, PASS_BY_INHERITANCE, CONSISTENCY_CHECK, PARTIAL, POSTDICTION, PENDING, NOT_INHERITED, OBS-FAIL, FRAMEWORK-FAIL).

Found 5 prose occurrences in `paper/base.md` advertising "**11 active values**" / "**11-value canonical**" — all 5 enumerated exactly the same 10 names inline.

Lines fixed (11 → 10):
- L482  "Status enum (canonical, **11 active values** ...)"
- L493  "11-value 등급으로 치환"
- L514  "Status enum (11 active: ...)"
- L868  "Enum 등급 master: line 482 의 11-value canonical"
- L978  "Enum 등급 master: line 482 의 11-value canonical"

Post-fix grep `"11 active|11-value"` against base.md → 0 hits ✓.
README.draft.md / FAQ never advertised "11 active" → no fix required there.

## 3. 22-row limitations — UNIFORM

| Surface | Count | Match |
|---|---|---|
| `claims_status.json::limitations` (counted) | 22 (1 OBS-FAIL + 1 UNRESOLVED + 6 OPEN + 5 ACK + 1 RECOVERY + 8 NOT_INHERITED) | — |
| `paper/base.md` §6.1.1 (rows 1–14) | 14 data rows | ✅ |
| `paper/base.md` §6.1.2 (rows 15–22) | 8 data rows | ✅ (14+8=22) |
| `paper/base.md` self-references "22행 한계 표" | 6 mentions, all consistent | ✅ |
| `README.draft.md` "22-row limitations table (§6.1)" | mention | ✅ |
| FAQ ("22행 정직 한계 표") | both EN/KO | ✅ |

Sub-issue resolved: §6.1.1 row 1 was advertised as "UNRESOLVED 영구" but the same item is OBS-FAIL everywhere else (§0 TL;DR L146; Claims-status table L178; `claims_status.json` L1-S8-worsening status="OBS-FAIL"; §6.5(e) self-audit L495 and L1051; emoji legend L445). One-character drift fixed in row 1 to "OBS-FAIL 영구" so the row itself, the table cross-reference (`§6.1 row 1`), and the JSON `L1-S8-worsening` are now identical labels.

NB: `claims_status.json::limitations[0]::status="OBS-FAIL"` was already correct; only the markdown table cell was drifted.

## 4. Emoji ↔ enum mapping — REPAIRED

Original mapping at base.md L449 mapped ✅ to `PASS / PASS_STRONG / PASS_TRIVIAL`. After L409/L412 reframing, two new active enum values (`PASS_IDENTITY`, `PASS_BY_INHERITANCE`) were never added to the legend, while the deprecated `PASS_TRIVIAL` was still listed as a primary alias.

Repaired to: `✅ ↔ PASS_STRONG / PASS_IDENTITY / PASS_BY_INHERITANCE (legacy PASS / PASS_TRIVIAL deprecated)`. Other mappings (⚠️, ⏰, ❌, 🚫, 📊) were already canonical and unchanged.

Cross-check: README.draft.md does not redefine its own mapping — it relies on the same emoji set, and every emoji used in the README ("Claims status" table) is consistent with the repaired legend.

## 5. Verification scripts coherence — CLEAN

`paper/verification/verify_lambda_origin.py` header: "CLASSIFICATION: CONSISTENCY_CHECK (down-graded from PASS_STRONG per L412)" — matches claims_status.json::lambda-origin status ✓.
`paper/verification/verify_milgrom_a0.py` header: PASS_STRONG — matches `expected_outputs/verify_milgrom_a0.json::classification` ✓.

Note (advisory, NOT a coherence break): `milgrom-a0` has its own verifier and is advertised as PASS_STRONG, but it is NOT one of the 32 claims in `claims_status.json`. The 32-claim audit is a defined cold-blooded subset that intentionally excludes Milgrom (it lives separately in §3.5 / verifier #2). This is not an inconsistency, just a scope boundary; we recommend a one-line comment in `claims_status.json` clarifying scope, but no edit was required.

The illustrative JSON snippet at base.md L497–507 still uses `"version": "1.0"` and shows `{"id": "milgrom-a0", "status": "PASS"}` (legacy enum). This is a *documented schema example*, not the live JSON, and the surrounding prose explicitly tags `PASS` as a deprecated legacy alias — left unchanged so the legacy mapping example remains traceable.

## 6. Cross-reference (§X.Y) audit — INHERITED CLEAN from L445

`results/L445/CROSS_REF_AUDIT.md` already verified all 22 unique `§`-anchors in base.md resolve to defined headings (0 broken). The L460 fixes (rows above) only touch table cell content and prose, not section numbering — re-running the L445 method against the post-L460 file would still return 0 broken. Not re-executed here (out of scope for L460 coherence audit).

## 7. Summary of edits applied to `paper/base.md`

| # | Line(s) | Before | After |
|---|---|---|---|
| 1 | 482 | "11 active values" | "10 active values" |
| 2 | 493 | "11-value 등급" | "10-value 등급" |
| 3 | 514 | "(11 active: ...)" | "(10 active: ...)" |
| 4 | 868 | "11-value canonical" | "10-value canonical" |
| 5 | 978 | "11-value canonical" | "10-value canonical" |
| 6 | 449 | emoji map ✅ → PASS / PASS_STRONG / PASS_TRIVIAL | ✅ → PASS_STRONG / PASS_IDENTITY / PASS_BY_INHERITANCE (legacy deprecated) |
| 7 | 986 | row 1 status "UNRESOLVED 영구" | "OBS-FAIL 영구" |

No edits required to: `claims_status.json`, `README.draft.md`, `paper/verification/*`, `paper/faq_*.md`.

## 8. Verdict

After L460 edits, the four canonical surfaces (paper/base.md, README.draft.md, claims_status.json, FAQ) carry **identical** values for:
- 32-claim distribution (4/3/8/1/8/8) and headline (raw 28% / substantive 13%)
- enum active count (**10**) and the 10 enum names
- 22-row limitations (14 §6.1.1 + 8 §6.1.2; row-1 status OBS-FAIL)
- emoji ↔ enum mapping (✅ covers 3 active PASS_*; legacy aliases marked deprecated)

Coherence audit: **CLEAN** post-fix.
