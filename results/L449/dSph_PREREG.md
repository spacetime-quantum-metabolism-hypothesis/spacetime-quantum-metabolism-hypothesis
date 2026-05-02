# dSph anchor 사전등록 (Pre-Registration) — DRAFT v0

**상태**: DRAFT (L449 N1 — 섹션 골격 only).
**Final commit 예정**: L451 (8인 합의 회의 L450 후).
**Triple-timestamp 채널**: GitHub release tag `v-dSph-prereg-YYYY.NN`
+ OSF DOI (TBD at L451) + paper commit hash (TBD at L451).

**근거 문서**:
- 동기: results/L424/{ATTACK_DESIGN, NEXT_STEP, REVIEW}.md (4 조건 도출).
- 메타-거버넌스: results/L449/{ATTACK_DESIGN, NEXT_STEP}.md (6 섹션 잠금).
- paper §6.1 row 14 (Euclid DR1 4.4σ pre-registration) triple-timestamp
  프로토콜의 dSph 적용 변종.

**원칙 (CLAUDE.md [최우선-1, 2] 준수)**: 본 DRAFT 는 *형식적 잠금* 만
포함. 4 조건의 *수치값*, *부호*, *prior 폭*, *primary mapping 선택*,
*결정 매트릭스 cell label*, *false-rate threshold* 는 모두 placeholder
상태이며 L450 8인 합의 회의에서만 결정. DRAFT 단계에서 수치 채워넣기
금지 — cherry-pick 위험.

---

## §0. 잠금 진술 (Locking Statement)

본 문서가 GitHub tag + OSF DOI + paper commit 3 채널 동시 commit
완료된 시점 (L451 timestamp) 이후, 아래 6 섹션의 어떤 항목도 변경
불가. 변경 시 사전등록 무효 — re-registration 필수 (새 tag + 새 DOI
+ 새 paper commit). archive 측정값은 *본 시점 이전에 공개된* 카탈로그
(McConnachie 2012 AJ 144 4 + Walker 2009 ApJ 704 1274 + Gaia DR3
Vallenari et al. 2023) 만 사용. 본 시점 이후 archive 도입은 어떤
종류든 금지.

---

## §1. Sample lock

**Anchor pool 명단** (5 classical Local Group dSph):
- Draco
- Ursa Minor (UMi)
- Sculptor (Scl)
- Sextans
- Carina

**제외 명단** (3 dSph):
- Fornax
- Leo I
- Leo II

**제외 objective criterion** [TBD — L450 합의]:
- 형식: distance > X kpc OR contamination level > Y OR ...
- 수치 X, Y 는 L450 8인 합의에서 결정.
- "tension 결과 회피" 사유 *금지*.

**Post-registration 신규 dSph 정책**:
- Gaia DR4 (또는 후속 catalog) 에서 신규 dSph 발견 시 *automatic
  addition 금지*. 새 dSph 추가는 별도 re-registration (새 tag +
  새 DOI) 필수.

**잠금 진술**: 본 시점 이후 anchor pool 의 추가/제거/교체 금지.

---

## §2. Primary ρ_env mapping lock

**Primary mapping** [TBD — L450 합의]:
- 후보 (i): Local-Group outer regime — D_LG (Local Group barycenter
  거리) 기반 log10(ρ/ρ_c).
- 후보 (ii): Galactic-internal regime — M_dyn / r_half³ 기반
  log10(ρ/ρ_c).
- 8인 합의로 (i) 또는 (ii) 한 가지 선택. 합의 메커니즘: 만장일치 →
  실패 시 8인 다수결 → 동수 시 P8 synthesizer 결정.

**Secondary mapping**:
- Primary 가 아닌 다른 한 매핑은 *sensitivity check only*. paper 본문
  보고 시 "primary X 결과 + secondary 비교" 형식 강제. secondary 가
  primary 보다 *결과가 좋다* 는 이유로 사후 swap 금지.

**잠금 진술**: primary/secondary 분류는 본 시점 이후 변경 불가.

---

## §3. σ₀ 변환 prior lock

**변환식 함수형 출처** [TBD — L450 합의]:
- 후보 (a): Walker 2009 ApJ 704 1274, eq. [TBD].
- 후보 (b): McConnachie 2012 AJ 144 4, eq. [TBD].
- 후보 (c): Wolf et al. 2010 mass estimator.
- 8인 합의로 한 채널 선택. 함수 형태 + 식 번호 + DOI 명기.

**Prior 분포 폭**:
- 인용 publication 의 reported σ 그대로 차용. inflation/contraction
  금지.

**잠금 진술**: 변환식 함수형 + prior 폭은 본 시점 이후 변경 불가.
fitting 후 prior 폭 사후 조정 금지.

---

## §4. 부호-결정 결정 매트릭스

**3 분기 × R-grid {2, 3, 5, 10} = 12 cell 매트릭스** [TBD — L450 합의]:

| 분기 \ R | R=2 | R=3 | R=5 | R=10 |
|----------|-----|-----|-----|------|
| (i) cosmic regime 재진입 (σ₀_dSph ≈ cosmic 값) | [TBD] | [TBD] | [TBD] | [TBD] |
| (ii) cluster 위치 이동 (σ₀_dSph ≈ cluster 값) | [TBD] | [TBD] | [TBD] | [TBD] |
| (iii) galactic 단조 회복 (σ₀_dSph ≈ galactic 값) | [TBD] | [TBD] | [TBD] | [TBD] |

각 cell label ∈ {PASS_THREE_REGIME, PASS_TWO_REGIME, PASS_MONOTONIC,
INCONCLUSIVE, FAIL_ALL}. L450 8인 합의에서 12 cell 모두 결정. 빈 칸
잠그기 금지 — '데이터 보고 채움' 시 사전등록 의미 상실.

**잠금 진술**: 12 cell label 은 본 시점 이후 변경 불가.

---

## §5. 175-point mock false-rate threshold

**Baseline**: paper §3.5 175-point SPARC mock false-detection rate
= 100% (toy LCDM null injection 기준).

**Threshold** [TBD — L450 합의]:
- 강화 임계: dSph 5점 추가 시 false-rate ≤ X% → row #5 ACK_REINFORCED
  → ACK 또는 RECOVERY 격상 가능.
- 약화 임계: dSph 5점 추가 시 false-rate ≥ Y% → row #5 ACK_REINFORCED
  유지 + P9 conditional falsifier 등급 유지.
- INCONCLUSIVE 구간: X% < false-rate < Y%.
- X, Y 는 L450 8인 합의에서 결정. 다만 X < 100% (즉 baseline 보다
  낮은 강화 임계) 형식적 잠금.

**Mock 실행 프로토콜**:
- N_mock = 200 (L405 / L424 동일).
- LCDM null injection (σ_truth 단일값 + ε_err noise).
- random seed prereg 시 고정 (`seed = TBD`).

**잠금 진술**: X, Y, N_mock, seed 는 본 시점 이후 변경 불가.

---

## §6. Triple-timestamp lock

**채널 1 — GitHub release tag**:
- repo: spacetime-quantum-metabolism-hypothesis
- tag: `v-dSph-prereg-YYYY.NN` (NN = 등록 순번)
- commit hash: [TBD — L451]
- tag date: [TBD — L451]

**채널 2 — OSF DOI**:
- project: SQMH dSph anchor pre-registration
- DOI: [TBD — L451 mint]
- freeze date: [TBD — L451]

**채널 3 — paper commit**:
- file: paper/base.md (§6.1 row #5 + §4 P9 row 갱신)
- commit hash: [TBD — L451]
- commit date: [TBD — L451]

**Cross-reference 의무**:
- 3 채널 commit 은 같은 날짜 (UTC) 에 완료.
- 각 채널 commit message 에 다른 2 채널 cross-link 명기.

**잠금 진술**: 3 채널 어느 하나라도 force-push / tag-rewrite / DOI-revoke
시 사전등록 전체 무효 — 새 등록번호로 re-registration.

---

## §7. paper/base.md cross-reference

본 prereg 등록 commit (L451) 시 paper/base.md 동시 갱신:

- **§6.1 row #5**: ACK_REINFORCED 강화 + 본 prereg 문서 cross-link
  (L449 dSph_PREREG.md + GitHub tag + OSF DOI).
- **§4 P9 row**: 등급 *qualitative* → *conditional-falsifier* (prereg
  활성화 후만 falsifier).
- 두 row 갱신은 prereg commit 과 *동일 PR* 또는 *직속 후속 PR* 에
  포함.

---

## §8. DRAFT → FINAL 전환 조건

본 DRAFT 가 FINAL 로 전환되려면:
1. L450 8인 합의 회의 완료 (primary mapping + 12 cell + prior 출처
   + X/Y threshold + sample 제외 criterion 5 항목 결정).
2. DRAFT 의 모든 [TBD] placeholder 수치/부호/선택 채움.
3. CLAUDE.md Rule-A 8인 순차 리뷰 통과 (이론 클레임 검증).
4. paper §6.1 row #5 + §4 P9 row 갱신 안 8인 승인.
5. L451 commit + DOI mint + paper PR.

전환 전까지 본 DRAFT 는 *형식 골격* 으로만 인용 가능. 본 DRAFT 의
placeholder 자체를 사전등록 내용으로 인용 금지.
