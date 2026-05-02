# L395 — Sec 6 Limitations Table FINAL (14-row + 비단조 fit caveat)

**Loop**: L395 (독립)
**주제**: Sec 6 limitations table **FINAL** — 14-row honest table 확정 + L346 비단조 fit caveat 통합.
**상위 컨텍스트**:
- L368 ATTACK_DESIGN/REVIEW 에서 14-row 구조 확정 (영구 4 + L322-L330 신규 6 + L332-L340 추가 2 + L368 신규 2 = 14).
- L346 REVIEW J1: σ_0(z) 비단조성은 *prediction 이 아니라 fit* (J1 판정), 4-pillar a priori 강제력 없음.
- L368 R2 conditional: "Phase 7 will solve" 식 hedging 표현 금지.
**원칙**:
- 정직 disclosure 우선. 격하 회피용 hedging 금지.
- L346 J1 의 비단조 fit caveat 를 14-row 표에 *별도 행이 아니라 본문 단락 + 행 4 footnote* 로 통합 (Row 카운트는 14 유지).
- CLAUDE.md 최우선-1 (방향만, 지도 금지) 준수: 본 문서는 *문서 통합 작업* 이며 이론 도출 아님. 수식 미포함.

---

## 1. FINAL 14-row 표 확정 (L368 → L395 직접 계승)

L368 §3 의 14-row 표를 그대로 채택한다. 변경 없음.

| # | Limitation | Status | Source loop |
|---|-----------|--------|-------------|
| 1 | σ_8 +1.14% structural | structural | L5 K15, L341 |
| 2 | H0 ~10% partial only | partial | L341 |
| 3 | n_s OOS (CMB primary 직접 예측 불가) | structural | L341 |
| 4 | β-function full derivation 미완 | partial | L334, L346 J1 |
| 5 | 3-regime 강제성 약함 (2-regime baseline) | downgraded | L332 |
| 6 | Sloppy dim ≈ 1 (cluster-dominant reparam) | acknowledged | L333 |
| 7 | Theory-prior 부분만 (pillar 4 ★★) | downgraded | L334 |
| 8 | Cluster single-source A1689 (13-cluster plan) | plan | L335 |
| 9 | Subset Bayes factor (5-dataset full joint 미실행) | plan | L336 |
| 10 | Micro 70-80% 상한 (5번째 pillar OPEN) | acknowledged | L337 |
| 11 | a4 emergent metric micro origin OPEN | OPEN | L338 |
| 12 | P17 Tier B V(n,t) derivation gate 미완 | OPEN | L338 |
| 13 | Cosmic-shear / S_8 외부 채널 미검증 | structural | L368 신규 |
| 14 | DR3-class blinded validation 미수행 | plan | L368 신규 |

카운트: 4 (영구) + 6 (L322-L330) + 2 (L332-L340) + 2 (L368) = **14**.

## 2. L346 비단조 fit caveat 통합 방식

L346 REVIEW J1: "비단조 σ_0(z) 는 SQT 4 pillar 의 a priori prediction 이 아니라 데이터에서 발견된 fit이며, 4 pillar 는 그것을 강제하지 않고 단지 모순되지 않을 뿐이다."

이 사실을 14-row 표에 통합하는 방식 *세 옵션 중* 본 loop 채택:

- **옵션 A (rejected)**: 신규 행 15 로 추가 → 카운트 15. L368 의 14 카운트와 충돌, 재발방지 ("Limitations table 카운트 변경 시 abstract 등 4곳 동기화 필수") 트리거. *기각*.
- **옵션 B (rejected)**: 행 4 (β-function full deriv) 또는 행 7 (Theory-prior 부분만) 의 status/Mitigation 텍스트만 강화. 정직 disclosure 강도 부족. *기각*.
- **옵션 C (CHOSEN)**: 행 4 + 행 7 의 footnote 로 명시 + Sec 6 본문에 *비단조 fit caveat* 단락을 별도로 1단락 추가. 14-row 카운트 유지하면서 L346 J1 의 표현 완전 반영.

채택 근거:
- L368 R8 재발방지 ("카운트 변경 4곳 동기화") 위반 회피.
- L346 J3 권고 ("Sec 3 본문에서 '4 pillar 가 비단조성을 예측한다' 류 표현 모두 약화 또는 삭제") 와 정합.
- 14-row 표 자체는 *외부 한계*, 비단조 fit caveat 는 *4-pillar 내부 강도* 의 정직 표시 — 분리 통합이 의미상 자연스럽다.

## 3. 비단조 fit caveat 단락 (Sec 6 추가 단락 초안 방향)

별도 1 단락. 핵심 메시지 (방향):

- 비단조 σ_0(z) 는 *데이터 fit 결과* 이지 4 pillar 의 a priori prediction 이 아니다.
- 4 pillar (RG saddle / Holographic / Z_2 / a4 scaling) 는 비단조성을 *허용* 하지만 *강제* 하지 않는다.
- Falsifiable prediction 으로 lock 하려면 P17 Tier B (V(n,t) full derivation) 완료 선행 필요.
- 따라서 본 논문은 비단조성을 *postdiction* 으로 표기, *prediction* 표현 사용 금지.

행 4 footnote: "β-function full derivation 미완은 L346 J1 의 비단조 σ_0(z) postdiction 판정과 동일 근거를 공유한다."

행 7 footnote: "★★ 격하는 4 pillar 가 σ_0(z) 형상을 *강제* 하지 못한다는 L346 정성 판정 (Pillar 별 등급 표) 에 직접 근거한다."

## 4. Hedging 금지 표현 차단 (L368 R2 conditional 후속)

본 Sec 6 draft 에서 *금지* 표현:
- "future Phase 7 will solve ..."
- "we expect future data to confirm ..."
- "prediction confirmed by data" (비단조 항목 한정)

대체 표현:
- "remains structural and is acknowledged as a permanent limitation of the background-only formulation."
- "deferred to future work; current paper does not claim resolution."
- "consistent with, but not predicted by, the present formulation."

## 5. 산출물 명세

- ATTACK_DESIGN.md (본 문서): 14-row + 비단조 caveat 통합 설계.
- REVIEW.md: 8인 자율 분담 리뷰 (정직 disclosure + hedging 차단 적정성).
- SEC6_DRAFT.md: 논문 Sec 6 영문/국문 본문 초안 — 14-row 표 + 비단조 fit caveat 단락 + hedging-free 표현 적용.

## 6. 정직 한 줄

> 14행 한계 표는 그대로, 비단조 σ_0(z) 는 prediction 이 아니라 fit 임을 본문 단락과 두 footnote 로 못박아 hedging 없이 인정한다.
