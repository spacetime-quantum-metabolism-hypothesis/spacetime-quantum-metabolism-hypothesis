# L441 — SYNTHESIS v4 FINAL (L422–L440 19 loop 통합)

**날짜**: 2026-05-01
**범위**: L422–L440 (19 loop) REVIEW.md 종합
**선행**: L421 SYNTHESIS v3 ACTUAL (L412–L420 9 loop 통합) — JCAP acceptance 63–73% 유지

**정직 한 줄**: L422–L440 19 loop 는 (a) PASS_STRONG 격상 시도 5건 전원 실패 (BTFR slope, MOND 차별성, dSph 자동 강화, NS, c-M), (b) NOT_INHERITED 회복 시도 2건 모두 실패 (Volovik framework-derivation, Jacobson entropic — Jacobson 영구 NOT_INHERITED 확정), (c) paper §2.4.1 / §2.5 / §2.6 / §6.1.2 / §6.1.2.1 정직 caveat sync + B1 bilinear postulate 명시화 + Q-parameter Definition C 단일 winner 결정 (P3 axiom 도출 보류로 PARTIAL 유지) + Padmanabhan 0/7 PASS 인용 격하, (d) 인프라 5건 (verification scripts, claims_status.json, README draft, Cover Letter v4, Referee Response v3, FAQ EN/KO) 정상 산출의 사이클로 종결, **32 claim 분포 4+3+8+1+8+8+0=32 변동 없음**, JCAP acceptance **63–73% 유지** (상한 근접; 정직성 자산 누적 + 5건 격상 실패의 net effect 상쇄).

---

## 1. 19 Loop Verdict 표 분류

### 1.1 PASS_STRONG 격상 시도 (전원 실패, 5건)

| Loop | 시도 | 결과 | 등급 변화 |
|---|---|---|---|
| L422 | BTFR slope=4 a priori 격상 (SPARC 175) | **FAIL**: bisector slope 3.58 (Q≤2) ~ 3.70 (Q=1), K1–K4 모두 FAIL, ΔAICc(free−fixed-4) = −115.8 ~ −54.9 (free 압도) | §4.1 row 2 변경 없음 — postdiction caveat 유지 |
| L423 | SPARC outer V_flat MOND-등가성 차별성 | **FAIL**: full sample slope 0.269±0.008 (MOND prior 0.25 와 ~3σ), Q=1 sub 등가. SQT만의 차별성 부정, MOND/Verlinde phenomenological 등가 영역 | 차별성 미달, sub-leading 잔차 채널 후속 |
| L424 | dSph anchor 자동 강화 (BB three-regime) | **FAIL**: ΔlnZ −22 ~ +34 시나리오 의존 (cherry-pick 위험), mock false-rate 0%→0% 변화 없음, ATTACK B2 부분 확정 | §6.1 row #5 ACK_REINFORCED 권고 (4 조건 사전등록 필요) |
| L425 | NS σ_0 anchor pool 추가 (P11) | **FAIL**: EOS-marg ΔlnZ ≈ 0 (median < 1e-3), A8 KILL 발동, EOS family variance 가 SQT 보정 흡수 | P11 "조건부 reserve" → "보류" 강등 |
| L426 | c(M) 채널 LCDM 차별성 | **PASS_TRIVIAL**: max \|Δc/c\| = 0.46% (관측 산포 ~25% 의 1/50) — LCDM 구분 불능 | §5/§6.1 row 추가 권고 (PASS_TRIVIAL 격하) |

**격상 회복 = 0건**. 5/5 KILL/FAIL/TRIVIAL.

### 1.2 NOT_INHERITED 회복 시도 (전원 실패/확정, 2건)

| Loop | 시도 | 결과 | row 변화 |
|---|---|---|---|
| L428 | Volovik 2-fluid analogue framework 도출 | **3 path 전원 FAIL**: phase 변수 부재, n field 확장 axiom 4 종속 (deferred), trivial caveat 강화만 가능 | §6.1.2 row #16 NOT_INHERITED → NOT_INHERITED_REINFORCED 권고, row #22 동형 정의 명시 |
| L429 | Jacobson entropic δQ=TdS 내부 채널 도출 | **영구 FAIL**: framework 'T' 부재가 근원, axiom 7 추가 path 동어반복 회피 불가 | §6.1.2 row #17 NOT_INHERITED 영구 확정, §6.5(e) footnote 강화 |

### 1.3 Paper Sync / 정직 caveat 강화 (PR 적용, 5건)

| Loop | 변경 | 위치 |
|---|---|---|
| L427 | Dual foundation (Causet + GFT) 명시 등재 + D1–D12 12/12 응답 | §2.5 + §2.6 + §6.1.2 + §6.1.2.1 |
| L430 | B1 bilinear absorption ansatz postulate 명시화 (mass-action hidden assumption 정직 등록) | §2.2 derived 1 row + §2.2.1 신설 + §6.5(e) cross-link |
| L431 | §2.4.1 신설: 4-pillar PARTIAL 의 axiom 4 OPEN 종속분 / 독립 잔여분 분리 | §2.4.1 신설 (D1–D8 4건 흡수 / 2건 부분 / 2건 보류) |
| L432 | Padmanabhan emergent gravity 0/7 PASS, hard FAIL 2 (Step 1 N_sur, Step 4 Newton) | 인용 "축약된 영감" 격하 권고 (PARTIAL #5) |
| L434 | Q-parameter canonical = Definition C (Joos-Zeh) physical 우선 단일 winner | PARTIAL 유지 (P3 axiom 도출 8인 K3 후속) |

### 1.4 인프라 / 출판 자산 (정상 산출, 6건)

| Loop | 산출 | 비고 |
|---|---|---|
| L435 | `paper/verification/` 5 stand-alone scripts + expected_outputs + README EN/KO + requirements | 모두 5초 budget 통과, monotonic 12.1σ 정직 disclosure |
| L436 | `claims_status.json` v1.1 machine-readable 생성 | 32 claim 분포 + 22 limitations, i18n EN/KO drift assertion 통과 |
| L437 | `README.draft.md` + `README.ko.md` 신규 작성 | 기존 root README.md 보존 (덮어쓰기 회피), §A.1 spec 전체 충족 |
| L438 | `paper/COVER_LETTER_v4.md` 신규 | v3 대비 down-grade only, 등급 상향 0건 |
| L439 | `paper/REFEREE_RESPONSE_v3.md` 신규 | 8 attack 면 중 7면 무력화, 4 OPEN 정직 disclose |
| L440 | `paper/faq_en.md` + `paper/faq_ko.md` 최종 draft | 12 항목 EN/KO 동일 정직 강도, L412–L420 발견 12건 모두 반영 |

### 1.5 Descriptive only / Caveat 추가 (1건)

| Loop | 시도 | 결과 |
|---|---|---|
| L433 | CMB θ_* 0.7% δr_d "structural" prediction 검증 | **descriptive only**: 동일 β=0.30 이 θ_* 와 ~10³σ 충돌, "(Planck σ × 23)" 의 σ 가 r_d 의 σ 임을 명시해야 정직. PARTIAL #6 등급 *descriptive* 한정 명시 권고 |

---

## 2. 32 claim 분포 변화

| 카테고리 | L421 (v3) | L441 (v4) | 변동 |
|---|---:|---:|---|
| PASS_STRONG | 4 | **4** | 0 (L422/L426/L424/L425/L423 격상 시도 5건 전원 실패) |
| PASS_IDENTITY | 3 | **3** | 0 |
| PASS_BY_INHERITANCE | 8 | **8** | 0 |
| CONSISTENCY_CHECK | 1 | **1** | 0 (Λ origin frozen) |
| PARTIAL | 8 | **8** | 0 (B1 명시화·C 채택 모두 PARTIAL 유지, 격상 없음) |
| NOT_INHERITED | 8 | **8** | 0 (Volovik #16 + Jacobson #17 모두 영구 NOT_INHERITED 확정·강화) |
| FRAMEWORK-FAIL | 0 | **0** | 0 |
| **합계** | **32** | **32** | **변동 없음** (요청서 예상 일치) |

**raw 28% / substantive 13%** 양면 표기 lock 유지.

---

## 3. NOT_INHERITED 8 row 의 회복 도달 (L427 dual + L428/L429 결과)

| row | 항목 | L427 후 | L428/L429 후 |
|---|---|---|---|
| #15 | Singularity / black-hole completion | direct 회복 진행 | (변동 없음) |
| #16 | Volovik 2-fluid analogue | partial 회복 진행 | **L428 후 NOT_INHERITED_REINFORCED** (framework 도출 3 path FAIL) |
| #17 | Jacobson entropic δQ=TdS | partial 회복 진행 | **L429 후 영구 NOT_INHERITED 확정** (footnote 강화) |
| #18 | GFT BEC 계열 micro-gravity | direct 회복 진행 | (변동 없음) |
| #19 | BEC nonlocality (Z₂ ≠ U(1)) | direct 회복 진행 | (변동 없음) |
| #20 | DESI ξ_q joint fit | latent (paper 본문 회복 주장 금지) | (변동 없음) |
| #21 | 3자 정합성 (BAO+SN+CMB+RSD) | latent (paper 본문 회복 주장 금지) | (변동 없음) |
| #22 | 5-program 동형 PASS 0/5 | partial 회복 진행 | **L428 후 정의 명시 권고** ("narrative parallel" 경계, "광고 아님") |

**direct 3 + partial 3 + latent 2 = 8 ✓** (L427 §6.1.2.1 정직 산수 유지). L428/L429 결과로 #16, #17 의 caveat 강화만 추가, 카운트 무변동.

---

## 4. 학계 JCAP Acceptance 재추정: **63–73% 유지** (상한 근접)

| 요인 | L421 v3 | L441 v4 | Δ |
|---|---|---|---|
| PASS_STRONG 회복 | 0건 (L417–L420 4 시도 실패) | **0건** (L422/L426 + L424/L425/L423 5 시도 전원 실패) | 0 (실패 누적은 acceptance 영향 없음, 광고 강등이 아니므로) |
| NOT_INHERITED 회복 | 0건 | **0건** (L428/L429 모두 NOT_INHERITED 확정·강화) | 0 (Jacobson 영구 NOT_INHERITED 정직 확정은 net positive 미세) |
| 정직 caveat 강화 | 누적 12+ 위치 | **추가 5건 sync** (§2.4.1 신설 / B1 등록 / Dual 등재 / Padmanabhan 격하 / Q Definition C) | +0~+1 (정직성 강화) |
| 인프라/검증 자산 | claims_status v1.1 spec only | **6건 산출** (verification scripts / JSON / README / Cover Letter v4 / Referee v3 / FAQ EN/KO) | +1~+2 (reviewer accessibility 상승) |
| S_8 tension 구조적 미해결 | 영속 | **영속** (μ_eff ≈ 1 구조 + L426 c-M PASS_TRIVIAL 재확인) | 0 |
| Q parameter ambiguity | OPEN | **L434 단일 winner C 결정** (PARTIAL 유지, P3 OPEN) | +0~+1 (caveat 명시화 + canonical 정의 lock) |

**상하 변동 없음**: PASS_STRONG 회복이 0건이라 상한 견인 없음, 정직성 자산 + 인프라 산출이 +1 ~ +3 점 미세 상승을 만들지만 격상 실패 5건의 net이 상쇄. **실질 평균이 v3 대비 약 1–2 point 상승, 그러나 63–73% bracket 내부 이동**.

**PRD Letter 진입 = 영구 불가** 재확인 (Q17 + Q13/Q14 미달성 누적, BTFR/MOND/dSph/NS/c-M 추가 격상 channel 모두 실패).

**JCAP "honest falsifiable phenomenology"** 포지셔닝 굳히기 (L6 8인 합의 + L427 Dual + L431 §2.4.1 + L432 Padmanabhan 격하 + L433 descriptive 한정 모두 정합).

---

## 5. paper/base.md 갱신 결과 (L422–L440 직접 수정 누적)

| # | 위치 | 출처 | 변경 |
|---|---|---|---|
| 1 | §2.2 derived 1 row | L430 | 의존 컬럼 a1+a4 → a1+a4+B1, sketch 컬럼에 bilinear ansatz 명시 |
| 2 | §2.2.1 신설 단락 | L430 | B1 (bilinear absorption ansatz) postulate 등록, P1–P4 도출 후보 표 |
| 3 | §2.4.1 신설 절 | L431 | 4-pillar PARTIAL 종속분/잔여분 분리, §6.5(e)/§6.1.1#11/§6.1.2.1/§2.6 cross-ref |
| 4 | §2.5 | L427 | Dual foundation (Causet + GFT) 명시 등재 + axiom 영향 차이 표 + D9/D11/D12 응답 |
| 5 | §2.6 caveat 첫 항목 | L427 | D10 응답 (Dual 4 축 Lagrangian 일관성 직교/완화 두 해석 OPEN) |
| 6 | §6.1.2 표 헤더 + 8 row | L427 | "회복 채널" + "회복 도달 정성" 컬럼 추가, direct 3 + partial 3 + latent 2 ✓ |
| 7 | §6.1.2.1 | L427 | Dual coexistence 정량 회복 폭 + #20/#21 paper 본문 회복 주장 금지 + #17 footnote 분리 |
| 8 | §6.5(e) PARTIAL caveat | L430 | mass-action 함수형 → §2.2.1 B1 single source of truth cross-link |

**갱신 권고 잔존** (paper 본문 미반영 / next loop 필요):
- §4.1 row 2 BTFR/a₀ "postdiction caveat" 강화 (L422/L423)
- §6.1 row #5 dSph 4 조건 사전등록 ACK_REINFORCED (L424)
- §4.1 row 추가: c-M PASS_TRIVIAL (L426)
- PARTIAL #5 Padmanabhan "축약된 영감" 격하 (L432)
- PARTIAL #6 CMB θ_* "descriptive only" 명시 (L433)
- §6.1.2 row #16 NOT_INHERITED_REINFORCED + row #22 동형 정의 명시 (L428)
- §6.5(e) footnote #17 영구 NOT_INHERITED 확정 (L429)
- Q parameter Definition C canonical lock (L434, P3 8인 K3 후속)

---

## 6. 잔존 작업 (Phase-7 / 후속 loop)

1. **paper/base.md 권고 8건 sync 적용**: L442+ 1 loop 으로 일괄 PR 처리 가능.
2. **8인 K3 합의 (Q parameter P3 axiom 도출)**: Definition C 의 thermal photon 환경 가정 axiom 도출 가능성 (L434 권고).
3. **Phase 5+ B1 도출 시도**: Schwinger-Keldysh + FRG 또는 axiom 1 부언 (L430 P1/P2).
4. **DESI DR3 unblinding** 후 Trigger A–D 활성화 시점 §6.1.2 row #20/#21 latent → direct 회복 검토.
5. **Euclid DR1 4.4σ 사전 등록** 검증 (L413/L419 결과 lock).
6. **prefactor O(1) 자유도 정량 분석** (L434 ATTACK A4 후속).
7. **`paper/verification/`** 의 stand-alone scripts CI 통합.
8. **README master 결정**: root README.md (한국어 SQMH 프로젝트) vs README.draft.md (§A.1 spec) 통합 (L437 P0 ambiguity).

---

## 7. 정직 한 줄

L422–L440 19 loop 는 PASS_STRONG 격상 시도 5건 전원 실패 (BTFR / MOND 차별성 / dSph / NS / c-M) + NOT_INHERITED 회복 시도 2건 (Volovik framework-derivation FAIL, Jacobson entropic 영구 NOT_INHERITED 확정) + 정직 caveat 강화 5건 sync (Dual foundation 등재, B1 명시화, §2.4.1 종속/잔여 분리, Padmanabhan 0/7 PASS 격하, Q Definition C canonical) + 인프라/출판 자산 6건 (verification scripts, claims_status.json, README draft EN/KO, Cover Letter v4, Referee Response v3, FAQ EN/KO) 의 사이클로 종결, **32 claim 분포 4+3+8+1+8+8+0=32 변동 없음** (요청서 예상 일치), **JCAP acceptance 63–73% 유지** (상한 근접; 격상 실패 5건과 정직성/인프라 자산 +6건이 net 상쇄, 평균 1–2 point 미세 상승), PRD Letter 진입 영구 불가 재확인 — 회복은 없으나 정직성 + 인프라 자산 누적이 net positive.
