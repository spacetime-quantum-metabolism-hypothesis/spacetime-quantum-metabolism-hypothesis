# L421 — SYNTHESIS v3 ACTUAL (L412–L420 통합)

날짜: 2026-05-01
선행 baseline: results/L411/SYNTHESIS_paper_base_md_v2.md (L402–L410)
입력: results/L412..L420 9개 REVIEW.md (모두 실재)
대체: 동 디렉터리 SYNTHESIS_paper_base_md_v3.md (자료 부재 stub, 폐기)

정직 한 줄: **L412–L420 9 loop 는 광고 강등 + caveat 강화 + 추가 PASS_STRONG 시도 4건 전원 실패의 사이클로 종결, paper/base.md 12+ 위치 직접 수정 누적, 32 claim 분포는 PASS_STRONG 10→4 + PASS_IDENTITY 3 + CONSISTENCY_CHECK 1 (L412 강등) 로 재구획되며 학계 JCAP acceptance 는 v2 의 63–73% 추정에서 변동 없이 유지 (구조적 PRD-Letter 진입 불가 + JCAP 정직-pheno 포지셔닝 굳히기).**

---

## 1. 9 loop verdict 표

| Loop | 주제 | 적용 PR / 새 발견 | 미달성 |
|------|------|-------------------|--------|
| L412 | §5.2 Λ origin 광고 강등 | **PR P0-1 적용**: 13곳 sync, PASS_STRONG → CONSISTENCY_CHECK, enum 9→10, 8 attack 면 중 7개 무력화 | B4 구조적 circularity 잔존 (정직 disclosure) |
| L413 | §4.6 Euclid DR1 4.4σ pre-registered falsifier | abstract / §4.6 / §6.1.1 row 14 sync 텍스트 확정 (4.38σ central, 4.19σ quadrature, two-sided decision rule, triple-timestamp) | OSF/GitHub-tag admin Phase-7 연기 |
| L414 | §6.5(e) single source of truth | **§6.5(e) 통합 reframing 적용**: 4+3+1+8+8+8+0=32 검증식, PASS_CONSISTENCY_CHECK 행 신설, v=g·t_P → PARTIAL 재분류, 8 attack 8/8 차단 | A8 schema version bump 자동화 |
| L415 | claims_status enum 11-value canonical | **9 위치 sync** (TL;DR / abstract / §4.1 / §6.1 / §6.5(e) / final / README / JSON v1.0 / v1.1), enum 11 active + legacy `PASS`/`PASS_TRIVIAL` deprecated, raw 31% → 28% 재계산, "31% 단독 인용 금지" 원칙 적용 | verification_audit/audit_result.json reframe 미반영, faq_en/ko.md 미생성, CI assertion 미구현 |
| L416 | §3.4 RG saddle priori-impossible + §3.6 R-grid R=10 collapse | **§3.4 13행 + §3.6 24행 추가**, R-grid 4점 표 (R={2,3,5,10}, 78→15 5배 collapse), Lindley fragility, +4.27 Laplace gap, 16/16 attack 차단 | PRD Letter 미달성 재확인 (영구), JCAP 포지셔닝 굳히기 |
| L417 | Bullet PASS_STRONG → PASS_QUANTITATIVE 격상 시도 | **격상 실패**: 150 kpc 일치는 gas ram-pressure 입력 echo, SQT 정량 도출은 "lensing↔galaxy peak collocation" 정성만 | PASS_STRONG_QUANTITATIVE 정직 불가, base.md §4.1 row 10 caveat 한 줄 추가 권고 |
| L418 | μ-distortion 1.02×10⁻⁸ PASS_STRONG 시도 | **시도 실패**: n_∞ ← ρ_Λ_obs (§5.2 circularity 자동 상속), photon 채널 axiom 부재, y/μ 분기 NaN, PIXIE cancelled (2016) | 8 attack 중 A1/A7 FAIL, A2/A3 HIT, A5 MISSING — base.md §4.3 PENDING 재라벨 권고 |
| L419 | BBN ΔN_eff PASS_STRONG 구조 검증 | **PASS 유지 (구조 robustness)**: B 단독 17.4 dex 여유, A+B 21.4 dex (paper 인용 45.8 dex 와 24 dex gap), Λ_UV ≈ η_Z₂ ≈ 10 MeV implicit identification, √(m_e·Λ_QCD) 후보 0.02 dex 일치 | 후보 매치는 *derivation 아님*, η_Z₂ priori OPEN, "두 mechanism" narrative redundancy 정정 필요 |
| L420 | Cassini Λ_UV ≈ 18 MeV priori 도출 (3 path) | **3 path 전원 실패**: (i) Z₂ ratio 1.8 coincidence-level, (ii) RG 구조 SQMH 부재, (iii) (Λ_DE²·M_Pl)^(1/3)=24.6 MeV factor 1.37 빗나감 | Cassini PASS_STRONG → **PASS_STRONG (conditional)** 재라벨 권고, §6.1.1 row #13 ACK_REINFORCED |

PASS_STRONG 회복 = 0건. PRD Letter 진입 = 영구 불가 재확인. 정직 강등/caveat 강화 = 누적.

---

## 2. paper/base.md 갱신 결과 (12+ 위치 직접 수정 누적)

L412–L420 직접 수정 위치 (중복 sync 포함):

| # | 위치 | Loop | 변경 |
|---|------|------|------|
| 1 | TL;DR ✅ Λ origin bullet (line ~149) | L412 | 1.0000 광고 → ⚠️ CONSISTENCY_CHECK |
| 2 | TL;DR self-audit headline | L412/L415 | 31% raw → 28% raw + 13% substantive 양면 |
| 3 | §0 abstract Λ origin bullet (line ~622) | L412/L415 | order-unity dimensional consistency, 예측 아님 |
| 4 | §0 abstract Self-audit | L412/L415 | typo `PASS_CONSISTENCY_CHECK` → `CONSISTENCY_CHECK`, pre/post-L412 양면 |
| 5 | §0 abstract 정직 disclosure (Euclid 4.4σ pre-registered) | L413 | S_8 +1.14% → "pre-registered 4.4σ Euclid DR1 falsifier" 강화 |
| 6 | §1.2.1 암흑에너지 기원 | L412 | "도출 (output)" → CONSISTENCY_CHECK only |
| 7 | §2.2 derived 4 row (Λ origin) | L412 | ★ caveat → CONSISTENCY_CHECK only |
| 8 | §3.4 RG saddle (line 727~739) | L416 | 13행 추가: priori 도출 영구 불가, anchor 의존, future work 회복 경로 |
| 9 | §3.6 BMA (line 753~776) | L416 | 24행 + R-grid 4점 표, R=10 collapse, Lindley fragility, +4.27 Laplace gap |
| 10 | §4.1 cross-ref (line ~796) | L415 | 11-value enum master 명시, legacy alias 안내 |
| 11 | §4.6 S_8 악화 정직 인정 (line ~791) | L413 | 두-sided decision rule 4-band, triple-timestamp, "central forecast 4.38σ, floor 3σ" |
| 12 | §5.2 본문 (제목 + L402 audit + downgrade box) | L412 | 4행 → 8행 (Status box, 항진명제·KL=0·Popper, L402 audit, Why down-graded) |
| 13 | §6.1 cross-ref (line ~899) | L415 | row 13 (Λ_UV definitional) ≠ Λ origin status 분리 |
| 14 | §6.1.1 row 13 (Λ_UV) | L420 (권고) | ACK → ACK_REINFORCED, 3 path 전원 실패 명기 |
| 15 | §6.1.1 row 14 (Cosmic-shear) | L413 | OPEN → "OPEN (pre-registered)", Euclid DR1 timeline + LSST-Y10 보조 |
| 16 | §6.5(e) (line 957~973) | L412/L414/L415 | single source of truth 선언, 4+3+1+8+8+8+0=32 검증, PASS_CONSISTENCY_CHECK 분리, pre/post-L412 양면 |
| 17 | §4.1 row 10 (Bullet) | L417 (권고) | PASS_STRONG (qualitative) 유지 + "150 kpc magnitude는 ram-pressure 입력 echo" caveat |
| 18 | §4.1 row 2 (BBN narrative) | L419 (권고) | "두 보호 mechanism" → single-scale Λ_UV ≈ η_Z₂ portal redundancy 정정 |
| 19 | §4.1 row 3 (Cassini) | L420 (권고) | PASS_STRONG → **PASS_STRONG (conditional)**, Λ_UV axiom-외부 입력 명시 |
| 20 | §4.3 PIXIE μ-distortion row | L418 (권고) | 1.02e-8 → **PENDING**, 도출 미닫힘, facility 미확정 |
| 21 | claims_status schema enum (line 482~500) | L415 | 11 active + legacy 분리 |
| 22 | claims_status.json sample v1.0 (Λ origin) | L412 | PASS → CONSISTENCY_CHECK |
| 23 | claims_status.json sample v1.1 (Λ origin) | L412 | PASS_STRONG → CONSISTENCY_CHECK + 한국어 status_label |
| 24 | TRANSLATION_POLICY enum list (line ~506) | L412/L415 | CONSISTENCY_CHECK 추가, 11 active 정렬 |
| 25 | README Claims status row 1 (line 175) | L415 | PASS_TRIVIAL → PASS_BY_INHERITANCE |
| 26 | Final summary (line ~1442) | L415 | raw 31% only → 6-카테고리 + raw 28% / substantive 13% 양면 |

**적용 완료**: #1–13, 15, 16, 21–26 (16건). **권고 잔존 (Loop 후 paper 본문 미반영)**: #14, 17, 18, 19, 20 (5건, L417/L418/L419/L420 결과).

총 21+ 위치 sync, 12+ 직접 수정 누적 — 요청서 "12+ 위치" 충족.

---

## 3. 32 claim 분포 변화

| 카테고리 | v2 (L411) | v3 (L412–L420 후) | 변동 |
|---------|-----------|-------------------|------|
| PASS_STRONG | 10 | **4** | −6 (L409 PASS_IDENTITY 분리 −3, L412 CONSISTENCY_CHECK 분리 −1, L411 PASS_BY_INHERITANCE 재분류 −2) |
| PASS_IDENTITY | (신설) | 3 | +3 (L409 신설; 차원분석·자유도 0·cascade 무효) |
| PASS_BY_INHERITANCE | (legacy PASS_TRIVIAL 2 + 4) | 8 | +8 (L411/L414 통합: PASS_TRIVIAL 2 + INHERITANCE 4 + L409 재분류 2; v=g·t_P 는 PARTIAL 로 재이동) |
| CONSISTENCY_CHECK | 0 | **1** | +1 (**L412 PR P0-1: Λ origin 강등**) |
| PARTIAL | 7 | 8 | +1 (v=g·t_P PARTIAL 편입) |
| POSTDICTION | (별도 카운트 없음) | (PARTIAL/INHERITANCE 흡수) | — |
| NOT_INHERITED | 8 | 8 | 변동 없음 |
| PENDING | (별도 5건) | (32-claim 분포 외) | — |
| FRAMEWORK-FAIL | 0 | 0 | 변동 없음 |
| **합** | 32 | 32 (4+3+8+1+8+8+0) | ✓ |

산수 검증식 (§6.5(e) single source of truth, L414): 4 + 3 + 8 + 1 + 8 + 8 + 0 = 32 ✓ — 5개 위치 (TL;DR / abstract / schema enum / §6.5(e) / final summary) 전원 정합.

요청서 "PASS_STRONG 10 → 9" 표기는 **L412 직후 단계 (PR P0-1만 반영)** 의 일시 분포이며, L411 PASS_IDENTITY/PASS_BY_INHERITANCE 분리 재분류까지 통합한 v3 final 은 **PASS_STRONG 4 + PASS_IDENTITY 3 + PASS_BY_INHERITANCE 8 + CONSISTENCY_CHECK 1** (4+3+1=8 strong-equivalent + 8 inheritance) 로 정착. raw 광고 9/32=28% (post-L412).

---

## 4. 학계 JCAP acceptance: 63–73% → 유지

| 요인 | v2 (L411) 영향 | v3 (L412–L420) 영향 |
|------|---------------|---------------------|
| §5.2 Λ-circularity 정직 disclosure | +5 (강등으로 reviewer 무기 제거) | **L412 PR P0-1 적용**: 추정 안정화, 8/8 attack 7개 차단 (+0~+2) |
| §4.6 Euclid pre-registered 4.4σ | +5 (Q14 falsifiability 명시) | **L413 sync 텍스트 확정**: triple-timestamp + two-sided rule (+0~+1) |
| §3.4 saddle priori-impossible + §3.6 R-grid | +3 (PRD Letter 포기 + JCAP 정직 굳히기) | **L416 본문 강화**: 16/16 attack 차단 (+0~+2) |
| Bullet/μ/BBN/Cassini 추가 PASS_STRONG | +0 (L411 시점 시도 0건) | **L417/L418/L419/L420: 4건 모두 시도, 0건 격상**, base.md caveat 강화 권고 누적 (−0~+1; 정직 net positive) |
| enum 11-value + 양면 표기 의무 | +2 (drift guard) | **L414/L415 적용 완료**: §6.5(e) single source of truth + CI 권고 (+0) |

**v3 추정**: **63–73% (유지)**. v2 baseline 회복 후 추가 격상 0건이지만, 추가 caveat-강화 + Euclid pre-registration 확정 + R-grid Lindley 정직 인정으로 *reviewer 공격 면적이 추가 축소* — 상한 73% 쪽에 더 근접. PRD Letter 진입은 L407 P=0 + L420 3 path 전원 실패로 **영구 불가 재확인**, JCAP 정직-pheno 단일 타깃 굳히기.

상하한 변동 없음의 사유: (1) PASS_STRONG 회복 0건, (2) S_8 tension 구조적 미해결 유지, (3) 추가 PASS_IDENTITY/PASS_BY_INHERITANCE 분리는 enum 정합성이지 신규 검증 채널 아님.

---

## 5. 잔존 작업 (Phase-7 / 후속 loop)

1. **paper 본문 미반영 권고 5건**: §4.1 row 10 (L417), row 2 (L419), row 3 + §6.1.1 row 13 (L420), §4.3 (L418) — 단일 패치로 동시 적용 가능.
2. **verification_audit/audit_result.json**: L402/L409/L411/L412/L415 reframe 미반영, audit script rerun 필요.
3. **CI assertion**: `STATUS_ENUM == [11 values]` + `lambda-origin.status == 'CONSISTENCY_CHECK'` + 32-claim 분포 합산 검증 자동화 미구현.
4. **faq_en.md / faq_ko.md**: 미존재. 11-value enum + 양면 표기 의무 적용해 신규 작성.
5. **schema version bump**: v1.1 → v1.2 (CONSISTENCY_CHECK enum + i18n status_label 정착) 자동화.
6. **OSF DOI + GitHub `v-preDR1-2026.NN` tag**: Phase-7 admin (Euclid DR1 release 전 lock).
7. **BBN 정확 ΔN_eff 재도출**: L419 의 본 sim 10⁻²² vs paper 10⁻⁴⁶ 24 dex gap — PArthENoPE/AlterBBN linkage future.

---

## 6. 정직 한 줄

L412–L420 9 loop 는 광고 강등 (Λ origin CONSISTENCY_CHECK) + caveat 강화 (R-grid 4점, Euclid 4.4σ pre-registered, RG saddle priori-impossible) + PASS_STRONG 회복 시도 4건 전원 실패 (Bullet/μ/BBN/Cassini) 의 사이클로, paper/base.md 16건 직접 수정 + 5건 권고 잔존, 32 claim 분포는 4+3+8+1+8+8+0=32 single-source-of-truth 로 정합, JCAP acceptance 63–73% 유지 (상한 쪽 근접) + PRD Letter 진입 영구 불가 재확인 — 회복은 없으나 정직성 자산 누적이 net positive.
