# L369 ATTACK DESIGN — JCAP Cover Letter v2

**Loop**: L369 (single, 독립)
**Date**: 2026-05-01
**Target**: JCAP cover letter v2 — L322–L341 정직 발견(audit) + L342–L368 회복 노력(recovery)을 단일 문서로 통합. 정직 disclosure + P17 pre-registration 강조.

## 상위 컨텍스트

- 누적 ~268 loop. L341 SYNTHESIS_255 시점 등급 ★★★★★ -0.08, JCAP 91-95%.
- L322-L341 audit 라운드에서 발견된 정직 limitations:
  1. BB σ_0 effective dim≈1 (sloppy, L323/L333)
  2. 3-regime 강제성 약함 → 2-regime baseline 권고 (L322/L332)
  3. Pillar 4 (parameter parsimony) ★★★→★★ 격하 (L325/L334, b/c priori 불가, post-hoc 인정)
  4. Cluster single-source A1689 의존 (L327/L335, 13-cluster pool 식별만)
  5. Subset Bayes 5-dataset MCMC 미완 (L328/L336, 24-30hr 설계)
  6. Micro 이론 80% 상한 (L330/L337, a4 emergent metric OPEN)
  7. SymG mock false-positive 30-80% 예상 (L329/L339)
  8. BB weight BIC 92.6% / Laplace 81% — narrative 격하 회피하나 robust 검증 필요 (L340)
  9. P17 pre-registration 2-tier 설계 완료 (L338, Tier A Λ-static + Tier B V(n,t))
- L342-L368 라운드: 위 9 항목에 대한 회복 노력. 일부 디렉터리 빈 채 — 정직 보고 필수.

## 8인 공격 (각자 독립 설계, 역할 사전지정 없음)

- **A1 (Disclosure 우선)**: cover letter v2 의 본질은 referee 가 audit 후 신뢰를 회복할 수 있도록 모든 격하·미완을 letter 본문(별첨 아니라)에 명기하는 것. L341 -0.08 등급, pillar 4 ★★, micro 80% 상한, sloppy dim=1 을 letter Sec. 1 에 즉시 노출.
- **A2 (Pre-reg 강조)**: P17 pre-registration 이 본 제출의 차별점. Tier A (Λ-static, 즉시 검증) / Tier B (V(n,t), derivation gate 통과 후) 분리. DESI DR3 / Euclid Q1 / LSST Y1 계열 의존성 명시. 사전 등록 라벨·해시·일자 letter 에 포함.
- **A3 (Recovery 정량)**: L342-L368 회복 노력에서 실제로 진전된 항목과 미수행 항목 분리. 빈 디렉터리 정직 인정 (L341 audit pattern 재사용).
- **A4 (Falsifier 8개)**: P17 falsifier 카드 letter 별첨. 각 카드: 예측, 데이터셋, 통과/불통과 임계값, 사전등록 일자. 임계값 사후 조정 금지.
- **A5 (Limitations 박스)**: Cover letter 끝에 "Known limitations (honest)" 박스. 9개 항목 전부 단문으로. 격하한 등급(★)도 본문 표로.
- **A6 (Positioning)**: JCAP target — "honest falsifiable phenomenology" (L6-T3 8인 합의 계승). PRD Letter 미타깃. "extra parameter preferred by data" 주장 금지 (L5 재발방지).
- **A7 (Reviewer-anticipated objections)**: R1 sloppy dim, R2 cluster single, R3 multimodality (dynesty mode), R4 BMA weight, R5 micro gap, R6 3-regime priori — 각 1문단 사전 응답.
- **A8 (Format)**: JCAP 표준 cover letter 1.5-2 page. 별첨: P17 pre-reg 카드 1page, limitations 박스 0.5page. 한국어 한 줄 정직 라인은 internal NEXT_STEP 에만 (제출본 영문).

## Top-3 (8인 합의)

A1 + A2 + A5. 이유:
- A1 = referee 신뢰 회복 핵심 채널.
- A2 = 본 제출이 다른 SQMH cover letter v1 와 구분되는 단 하나의 차별점.
- A5 = audit-recovery 통합 라운드의 산출물 형식.

(A4/A7 은 letter 별첨/내장 형태로 흡수, A6 은 letter tone 으로 흡수.)

## 통과 기준

- COVER_LETTER_v2.md 가 L322-L341 9 limitations 전체를 본문(별첨 아님)에 명기.
- P17 pre-reg Tier A/B 가 letter 본문에 1문단 이상 + 별첨 카드.
- Recovery 미수행 항목이 정직 리스트로 letter 에 노출.
- 등급 ★★★★★ -0.08 (or 갱신값) 명시. 이론 등급 임의 상향 금지.
- 정직 한국어 한 줄 NEXT_STEP 에 포함.

## 실패 시 처리

- L342-L368 빈 디렉터리 발견 시: L341 패턴 적용 — "claimed N, actual M" 라벨, 본문에 정직 표기.
- Cover letter 가 limitations 를 별첨으로만 처리 → 재작성.
- P17 Tier B derivation gate 미통과인데 Tier A 와 동격 표기 → 재작성.
