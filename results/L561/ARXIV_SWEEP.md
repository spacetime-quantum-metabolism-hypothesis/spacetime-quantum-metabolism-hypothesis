# L561 — paper/arXiv_PREPRINT_DRAFT.md 전수 mismatch sweep

세션: L561 (단일 세션, grep + 디스크 cross-check 만, **paper edit 0건**)
일자: 2026-05-02
대상: `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/paper/arXiv_PREPRINT_DRAFT.md` (214 lines, single-agent L547 D-path)
디스크 사실 근거:
- `paper/verification/verify_milgrom_a0.py` (직접 실행 stdout 재현)
- `paper/verification/verify_mock_false_detection.py` (직접 실행 stdout 재현)
- `paper/verification/expected_outputs/verify_milgrom_a0.json`
- `claims_status.json` v1.2 (project root, L516 동기화)
- `results/L482, L491–L495, L498, L502, L506, L513, L515, L526_R8, L537, L545` (실재 확인)
- `paper/verification_audit/R3_axioms.json`, `R5_quantum_result.json` (실재)

배경: L559 (`results/L559/MNRAS_SWEEP.md`) 가 MNRAS_DRAFT.md 에서 fabrication 의심 2건 (L89 0.42σ 거짓 인용 + L137 H₀=100 mock 거짓 기술) + mismatch 7건 발견 — 동일 single-agent path (L547) 작성된 arXiv preprint 검증 의무.

본 sweep 의 결론은 MNRAS 와 매우 다름: **arXiv preprint 는 L559 critical fabrication 2건이 모두 부재**하다. 단 numerical roundings + 일부 disclosure gap 존재.

---

## §1 수치 mismatch 표

| Line | Section | paper 표기 | 디스크 사실 (인용 경로) | Status |
|------|---------|-----------|---------------------|--------|
| 13, 34, 78 | Abstract / §1.2 / §4.1 | a₀(SQT) = 1.042 × 10⁻¹⁰ m s⁻² (H₀=67.4) | 손계산 c·H₀/(2π) = 1.0421e-10 ✓ | **OK** |
| 13, 35, 77 | Abstract / §4.1 | a₀(SPARC RAR M16) = 1.069 × 10⁻¹⁰ | claims_status L97 row `rar-a0-milgrom`; M16 reference value | **OK** (paper 본문은 1.069 인용; 디스크 verify_milgrom_a0.json 은 σ_obs=1.20 anchor 다른 채널) |
| 13, 36 | Abstract | "2.5% below ... within ~1σ" | (1.069−1.042)/1.069 = 2.53% ✓; σ ≈ 0.27/1.069 RAR uncertainty ~ 1σ 범위 한도 (RAR published σ 가 paper 에 명시 안 됨; 정성 claim) | **OK** (정성) |
| 65 | §3 | "H₀=73.0 (SH0ES) gives a₀ = 1.13 × 10⁻¹⁰" | 손계산 1.1287e-10 → 반올림 1.13 ✓; verify_milgrom_a0.py 직접 실행 출력 `1.129e-10` (script 는 H₀=73 hardcoded) | **OK** (반올림) |
| 65 | §3 | "still within RAR 1σ" | 디스크 verify_milgrom_a0.json: dev=0.71σ vs σ_obs=1e-11 anchor (1.20 fiducial) — RAR M16 1.069 anchor 와는 다른 σ. paper "RAR 1σ" 진술의 anchor σ 정의 모호 | **AMBIGUOUS** (LOW; "RAR uncertainty" 단일 토큰; M16 σ 직접 인용 부재) |
| 13, 82 | Abstract / §4.1 | ΔAICc = +0.7 (naive) → +4.7 (applicable-only) → +18.8 (full k_h=9) | claims_status L51 `delta_aicc_honest=4.707, k_h_applicable=2`; L502 결과 일치; +0.7 / +18.8 은 L502/L513 chain 인용 (직접 sweep 외) | **OK** |
| 13 | Abstract | "N_eff = 4.44, combined ρ-corrected significance 8.87σ" | l498_results.json `N_eff_ParticipationRatio=4.4366..` ≈ 4.44 ✓; `Z_combined_correlation_corrected_all6=8.8718..` ≈ 8.87 ✓ | **OK** |
| 117 | §5 | "naive count of 6 and naive combined 11.25σ" | l498_results.json grep 으로 11.25 직접 미발견 (l498 JSON 일부만 확인); 11.25 ≈ √(5×5²+0×0²)?  추정. 정확 산출은 본 sweep scope 외 | **OPEN** (숫자 디스크 미직접 인용; L498 source 추가 검증 권장) |
| 128 | §5 | "Li–Ji 5.00; Cheverud–Galwey 5.71; naive 6.00" | l498_results.json `N_eff_LiJi=5.0` ✓, `N_eff_CheverudGalwey=5.706..` ≈ 5.71 ✓ | **OK** |
| 128 | §5 | "Z_comb ≈ 10.83σ alone" (CMB-S4+ET+SKA orthogonal) | l498 본 sweep grep 미직접 인용 | **OPEN** (LOW; L498 추가 grep 권장) |
| 128 | §5 | "Euclid×LSST = 0.80, DESI×Euclid = 0.54, DESI×SKA = 0.32" | l498_results.json grep `0.5345224838248487` (DESI×Euclid 추정 0.54 토큰 일치); 0.80 / 0.32 직접 grep 부재이나 sweep 부분 grep 한계 | **OK** (부분 확인) |
| 89 | §4.2 | ΔN_eff ≈ 10⁻⁴⁶ < 0.17 | claims_status L72 `BBN ΔN_eff ≈ 10⁻⁴⁶ < 0.17 (η_Z₂≈10MeV...)` ✓ | **OK** |
| 98 | §4.3 | β_eff = Λ_UV/M_Pl ≈ 7.4 × 10⁻²¹ (small-coupling channel) | claims_status L78 `cassini-ppn` row 인용; L506 channel selection — Λ_UV 7.4e-21 정확 토큰은 본 sweep 미grep | **OPEN** (LOW; L506 직접 검증 미실행, paper 근거는 L506 cassini channel 4 dark-only embedding) |
| 99 | §4.3 | "β=0.107 yields |γ−1| ≈ 2.3 × 10⁻², ~10³× hard-fail" | claims_status L82 `cassini-ppn caveat`: "channel 3 universal_phase3 (β=0.107) FAILS Cassini" ✓; 2.3e-2 vs Cassini 한도 2.3e-5 ratio = 10³ ✓ | **OK** |
| 106 | §4.4 | EP \|η\| ≤ 10⁻¹⁵ (MICROSCOPE) | MICROSCOPE Touboul 2017 한도 ✓ | **OK** |
| 136 | §6 | "Conservative count: k_hidden = 9" | claims_status `k_hidden = 9 conservative ~ 13 expanded` ✓; L495 HIDDEN_DOF_AUDIT.md path 실재 ✓ | **OK** |
| 145 | §6 | "Extended count: ~13" | claims_status 일치 ✓ | **OK** |
| 149 | §6 | "PASS_STRONG count is 0 / 32" | claims_status L26 self_audit_distribution `PASS_STRONG: 0` ✓; L40 distribution rows 합 32~33; L621 `PASS_STRONG 0/33` 와 1 행 차이 | **MISMATCH** (LOW — 0/32 vs claims_status 0/33; L516 추가 1행 add_claim L482 RAR 으로 33 행. paper 가 32 인용은 pre-L516 카운트) |
| 149 | §6 | "pre-L412 31%, post-L412 28%, substantive 13%" | claims_status L36 `raw_PASS_STRONG_advertised_post_L412: 9/32 = 28%`, L37 `pre-L412: 10/32 = 31%` ✓; substantive 13% 는 별도 산출 (paper 가 raw 인용을 금지한다고 명시 — 본문은 self-consistent) | **OK** |

추가 확인:
- §7 정직 한 줄 (L210): "PASS_MODERATE 4건, no PASS_STRONG" — claims_status v1.2 distribution 정합 ✓.
- §6 `1. M16 ... 6. Axiom-scale stipulation` 6 항목 enumeration 인데 텍스트 "k_hidden=9" 와 1:1 매핑 불일치 — 항목 (3 anchors=3, three-regime=2 등) 합산 시 9 도달. **표기 가독성 한계** (LOW).

---

## §2 Mock falsifier 기술 검증 (L559 critical 재발 가능성)

**핵심 질문**: arXiv_PREPRINT_DRAFT.md 가 verify_mock_false_detection.py 인용? "H₀=100" 토큰 등장? L137 (MNRAS) 와 동일 거짓 기술?

**Grep 결과** (paper 본문 214 라인):
- `verify_mock_false_detection.py` — **0회 출현**
- `H₀=100` / `H0=100` / `fabricated` — **0회 출현**
- `mock` 토큰 — **1회만 출현** (L81, §4.1 row "OOS / mock (L493 / L494). 30% out-of-sample retention; 0/1000 mock false-positives → real signal confirmed at the SPARC anchor.")
- `5σ` — N_eff 단락 (L121, "5σ-class falsification trigger") 1회; mock 과 무관

**평가**:
- arXiv preprint 는 verify_mock_false_detection.py 자체를 인용하지 **않음**.
- L81 mock false-positive 진술 ("0/1000")은 **L493/L494** 결과 인용. L494 디스크: `claims_status L51` "L494 false-positive 0/200 → real signal" — paper 인용 "0/1000" 는 claims_status `0/200` 과 **불일치** (200 vs 1000).
- **이는 MNRAS L137 의 H₀=100/5σ 거짓 기술과 동일 카테고리는 아니지만, 별도 mismatch (mock false-positive 카운트)** 로 LOW–MEDIUM 우선순위.

**판정**: L559-class CRITICAL fabrication 2건 (L89 0.42σ 거짓 / L137 H₀=100 mock 거짓) **둘 다 arXiv 에서 부재**. 단 L81 "0/1000" vs claims_status "0/200" mismatch 1건 신규 발견 (HIGH 우선순위).

| 항목 | MNRAS_DRAFT (L559 발견) | arXiv_PREPRINT (L561 검증) |
|------|------------------------|--------------------------|
| 0.42σ 거짓 인용 | L89 fabrication (CRITICAL) | **부재** ✓ (paper 는 0.71σ 토큰 미사용 — H₀=67.4 / 2.5% / 1σ 채널만 사용) |
| H₀=100 mock 거짓 기술 | L137 fabrication (CRITICAL) | **부재** ✓ (verify_mock_false_detection.py 0회 인용) |
| Mock false-positive count | (없음) | L81 "0/1000" vs claims_status `0/200` (HIGH 신규) |

---

## §3 PASS_STRONG / PASS_MODERATE 일관성

paper 의 grade 토큰 출현 (grep 결과):
- `PASS_MODERATE`: 13회 (Abstract, §1.2, §4.1–4.4 row, §6 consequence, §7.1, 정직 한 줄)
- `PASS_STRONG`: 8회 — **모두 negative 문맥** ("PASS_MODERATE *rather than* PASS_STRONG", "downgraded *from* PASS_STRONG", "demoting it from PASS_STRONG", "We do *not* claim PASS_STRONG", "no PASS_STRONG anywhere", "PASS_STRONG count is 0/32")
- `PASS_QUALITATIVE` / `PASS_BY_INHERITANCE` / `PASS_IDENTITY`: 0회 (Path-D scope 적합)

| Line | paper grade 토큰 | 문맥 | claims_status v1.2 정합 |
|------|----------------|------|---------------------|
| 13 (abstract) | "PASS_MODERATE rather than PASS_STRONG" | 4 channels | ✓ (rar-a0/bbn/cassini/ep 모두 `PASS_MODERATE`) |
| 73 (§4) | "downgraded from PASS_STRONG to PASS_MODERATE" | 4 channels | ✓ |
| 84, 93, 102, 111 | "Grade: PASS_MODERATE" (각 4 row) | a₀ / BBN / Cassini / EP | ✓ 4/4 |
| 13, 165, 191, 210 | "no PASS_STRONG ... 0% headline" | summary | ✓ (claims_status `PASS_STRONG: 0`) |

**판정**: arXiv preprint 의 grade 사용은 **claims_status v1.2 와 100% 일관**. MNRAS_DRAFT 가 5/5 PASS_STRONG 위반 (L559 §2) 한 것과 정반대.

**그러나** reviewer 가 trust 하려면:
- §4 row 가 `claims_status.json` schema (id, status, k_h_applicable, delta_aicc_honest) 를 직접 인용하지 **않음** — paper 는 L502 / L495 path 만 인용. claims_status.json 자체 path 는 paper 본문 0회 출현. (LOW; reviewer 가 GitHub clone 시 claims_status.json 직접 검사 가능하므로 critical 아님)

---

## §4 Hidden DOF disclosure 검증

**§6 본문 평가**:
- ✓ `k_hidden = 9` 명시 (L136)
- ✓ 6 항목 enumeration (M16, anchor×3, Υ⋆, B1, three-regime×2, axiom-scale)
- ✓ Extended count `~13` 명시 (L145)
- ✓ ΔAICc ≥ +18 (k_h=9) 표기 (L147)
- ✓ "PASS_STRONG count 0/32" 헤드라인 (L149)
- ✓ raw 카운트 standalone 인용 금지 명시 (L149, L513/L515 sync)
- ✓ §6.5(e) base.md 디스클로저 transcribe 명시 (L151)

**MNRAS L559 §4 missing caveat 3건과 비교**:
1. Hidden DOF 9-13 — MNRAS MISSING / **arXiv FULL ✓** (§6 전체)
2. RAR universality 철회 (L491/L492/L503) — MNRAS MISSING / **arXiv 부분** (§4.1 L79-L80 cross-form spread + dwarf KS 만 인용; "universality 철회" 단일 캐비엣 명시 없음 — L80 `KS dwarf-vs-bright p=0.005` 토큰도 본문 부재 — paper 는 "non-trivial cross-dataset disagreement" 만; **PARTIAL**)
3. L502 AICc honest disclosure — MNRAS MISSING / **arXiv FULL ✓** (§4 row 4건 + §6 L147)

**판정**: arXiv preprint 의 hidden-DOF disclosure 는 MNRAS 보다 압도적으로 정직. 단 L491/L492/L503 universality 철회 명시 1건 PARTIAL.

---

## §5 Caveat coverage 매핑

| Caveat | claims_status / base.md 등록 | arXiv 본문 위치 | Coverage |
|--------|---------------------------|----------------|----------|
| Verlinde 2017 numerical degeneracy | base.md / claims_status | L42 ("MOG, TeVeS, EMG, EG, Verlinde entropic gravity ... different hidden inputs") | **PARTIAL** (Verlinde 명시되나 "entropic gravity numerical degeneracy" 한 단어 없음 — 단순 비교 컨텍스트만) |
| Bullet 잔존 cluster DM / Abell 520 | claims_status `bullet-cluster: PASS_QUALITATIVE`, L509 Abell 520 dark-core | **0회** (Bullet/Abell 520 토큰 부재) | **MISSING** (Path-D scope 가 galactic-only 라서 부분적 정당; 단 §1.3 비교에서 Verlinde 만 언급, Bullet 정성-한도 cluster scope 제외 정직 명시 부재 — LOW) |
| Son+ contingency | base.md / paper §1.2.1 | §1.1 P1 (L23): "Son et al. (2025) raises possibility ... canonical late-time acceleration evidence partially absorbed into host-age systematic"; §7.3 L173, §7.4 L180; 정직 한 줄 L210 | **FULL** ✓ (4회 출현) |
| Universality 철회 (L491/L492/L503) | claims_status L26 ACK | §4.1 L79-L80 cross-form / dwarf 진술; §7.2 / §7.3 에서 명시적 "universality 철회" 토큰 부재 | **PARTIAL** (HIGH) |
| Q17 미달 (amplitude-locking 미유도) | base.md / paper L6 §"PRD Letter 진입 조건" | §7.2 L167 "Q17 amplitude-locking is *not* dynamically derived; E(0)=1 normalisation only" ✓; 정직 한 줄 L210 "no cosmic-acceleration derivation" ✓ | **FULL** ✓ |
| S₈ 미해결 | claims_status / base.md | §7.2 L168 "No claim that S₈ tension is resolved (μ_eff ≈ 1 structurally; ΔS₈ < 0.01%)" ✓ | **FULL** ✓ |
| Cassini channel-conditional | claims_status L82 / L506 | §4.3 (L96-L102) 전체 + §7.2 L169 "No claim of Cassini PASS in the universal-coupling channel" ✓ | **FULL** ✓ |
| EFE / dwarf spheroidal | base.md | 본문 0회 (Path-D galactic-only scope 에서 EFE 명시 부재) | **MISSING** (LOW; Path-D scope 가 SPARC aggregate 한정이므로 dwarf disagreement L80 만 cite) |
| H₀ tension sensitivity | base.md / paper §3 | §3 L65 ("Sensitivity to H₀ is linear: H₀=73.0 ... 1.13 × 10⁻¹⁰, still within RAR 1σ") ✓ | **FULL** ✓ |
| SPARC galaxy-by-galaxy fit 부재 | base.md | 본문 0회 (L80 dwarf KS만; per-galaxy 0.427 dex spread L503 미인용) | **MISSING** (HIGH; L491/L503 spread 정량값 인용 부재) |
| μ(x) 미유도 | base.md / paper §6 | 본문 0회 (M16 functional 은 hidden DOF #1 로만 인용; "μ(x) 비유도" 명시 부재) | **MISSING** (LOW) |
| Postdiction risk | (paper 자체 caveat) | §7.3 L175 "Three-regime structure (galaxy/cluster/cosmic) was identified through data-fitting, not pre-registered" ✓ | **FULL** ✓ |
| 0 free parameter overclaim | claims_status L23 ACK | §1.1 L24 "previously advertised as '0 free parameters'. A self-audit identified up to nine implicit choices" ✓ | **FULL** ✓ |

**Missing 우선순위**:
- **HIGH**: RAR universality 철회 (PARTIAL); SPARC per-galaxy spread 0.427 dex 정량 인용 부재
- **LOW**: Bullet/Abell 520 명시 부재 (galactic scope); EFE 부재; μ(x) 비유도 명시

**MNRAS 대비 압도적 우월**: 정직성 / hidden DOF / Q17/S₈ caveat 모두 FULL.

---

## §6 Citation pointers — broken/drift links

| Line | 인용 path | 디스크 실재 | Status |
|------|----------|-----------|--------|
| 32, 52, 65, 192 | `paper/verification/verify_milgrom_a0.py` | ✓ | OK |
| 65, 192 | `paper/verification/expected_outputs/verify_milgrom_a0.json` | ✓ | OK |
| 192 | `paper/verification_audit/R3_axioms.json` | ✓ | OK |
| 192 | `paper/verification_audit/R5_quantum_result.json` | ✓ | OK |
| 32, 192 | `paper/base.md` | ✓ (paper 디렉토리) | OK |
| 23 | `results/L526` (R8 §4.1) | `L526_R8` 디렉토리 실재 ✓ — paper 인용 `L526` 단순형 (R8 suffix 없음) | **OK** (R8 분리되어 있음; LOW 표기 정합성) |
| 24, 134 | `results/L495/HIDDEN_DOF_AUDIT.md` | ✓ | OK |
| 117 | `results/L498/FALSIFIER_INDEPENDENCE.md` | ✓ | OK |
| 24, 134, 192 | `results/L502/HIDDEN_DOF_AICC.md` | ✓ | OK |
| 99, 192 | `results/L506` (Cassini robustness) | ✓ (CASSINI_ROBUSTNESS.md) | OK |
| 24, 134 | `results/L513/REVIEW.md` | ✓ | OK |
| 192, 204 | `results/L482, L491, L492, L493, L494, L515, L526, L537, L545` | 전부 ✓ (find 결과) | OK |
| 42, 192 | `paper/COMPARISON_TABLE.md` | ✓ | OK |
| 48 | `paper/02_sqmh_axioms.md` | ✓ | OK |
| 192 | `paper/verification/verify_milgrom_a0.py` ancillary list | ✓ | OK |

**broken link 0건**. 모든 paper 본문 인용 path 디스크 실재. ✓

**미언급 verification 스크립트** (paper 가 ancillary list 에 포함 안 함):
- `verify_S8_forecast.py`, `verify_lambda_origin.py`, `verify_Q_parameter.py`, `verify_cosmic_shear.py`, `verify_monotonic_rejection.py`, `verify_mock_false_detection.py` (6개)
- §arXiv submission metadata L192 ancillary list 가 `verify_milgrom_a0.py` 만 포함 — Path-D galactic-only scope 적합 (cosmology/S₈ 인용 안 함). **OK** (정합).

---

## §7 정정 우선순위

### CRITICAL (single-handed reject 위험)
**없음.** L559 critical 2건 (0.42σ 거짓, H₀=100 mock 거짓) **둘 다 부재**. arXiv preprint 는 honest disclosure path 를 시종 유지.

### HIGH (referee round 신뢰 타격)
1. **L81 "0/1000 mock false-positives" vs claims_status `0/200`**: claims_status L51 `L494 false-positive 0/200` 와 paper `0/1000` 토큰 mismatch. 1000 vs 200 = 5× 차이. 디스크 L494 결과 직접 검증 후 정정 필요. **→ §4.1 row L81 토큰 `0/1000 → 0/200` 치환** (또는 L494 결과 갱신).
2. **RAR universality 철회 명시 부재**: claims_status L26 future_plan ACK ("aggregate-only match; per-galaxy/environment universality not claimed (L491/L492/L503)") 가 paper §4.1 / §7 limitations 에 단일 토큰 부재. § 4.1 L80 "non-trivial cross-dataset disagreement" 는 약함. **→ §4.1 말미 또는 §7.2 limitations 에 "universality not claimed (L491/L492/L503; per-galaxy intrinsic spread 0.427 dex)" 추가**.
3. **SPARC per-galaxy 0.427 dex spread 정량 인용 부재**: claims_status L51 / L503 결과. paper 본문 0회. **→ §4.1 row 에 per-galaxy spread 0.427 dex 토큰 추가**.

### LOW (정직성 차원, reviewer 외부 발견 어려움)
4. **L149 "0 / 32" vs claims_status "0 / 33"**: L516 add_claim L482 RAR 으로 33 행. **→ "0/32 → 0/33" 토큰 치환**.
5. **L65 "still within RAR 1σ" anchor σ 모호**: M16 published σ_a0 직접 인용 권장. **→ "RAR 1σ" → "M16 published σ_a0 ≈ ±0.05 × 10⁻¹⁰" 형태 명시**.
6. **§6 enumeration 가독성**: 6 줄 항목 합 vs k_hidden=9 텍스트 표기 정합 매핑 명시 권장 (anchor×3 / three-regime×2 / axiom-scale×1 명시).
7. **Bullet/Abell 520 명시 부재 (galactic scope)**: §1.3 또는 §7.3 limitations 에 "cluster-scale dark matter (Bullet/Abell 520) not addressed by present preprint scope" 한 줄 추가 권장.
8. **§1.3 Verlinde "numerical degeneracy" 명시 부재**: 단순 비교 토큰만 (L42); claims_status / base.md 의 "Verlinde 2017 numerical degeneracy" 정합 표기 권장.
9. **L526 vs L526_R8 디렉토리 표기**: paper L23 / L204 에서 `L526` 단순형. 디스크는 `L526_R1 ~ L526_R8` 분리. R8 suffix 명시 권장.

### Non-trigger (이미 정합)
- 1.042 / 1.069 / 1.13 수치 ✓
- 4.44 / 8.87 / 5.00 / 5.71 N_eff 산출 ✓
- PASS_STRONG 0/32 헤드라인 (33 LOW 차이만)
- Q17 미달 / S₈ 미해결 명시 ✓ FULL
- 모든 path 디스크 실재 ✓ broken 0건
- Hidden DOF k=9 disclosure ✓ FULL
- Son+ contingency ✓ FULL
- Cassini channel-conditional ✓ FULL
- 정직 한 줄 (L210) ✓
- L547 D-path 단일 에이전트 명시 + 8인/4인 review 의무 명시 (L5, L214) ✓

---

## §8 정직 한 줄

본 L561 sweep 은 paper/arXiv_PREPRINT_DRAFT.md 214 라인을 전수 정독하고 디스크 cross-check 만 수행했으며 paper / claims_status / 검증 스크립트 어느 디스크 파일도 수정하지 않았다 — L559 가 MNRAS_DRAFT.md 에서 발견한 CRITICAL fabrication 2건 (0.42σ 거짓 인용, H₀=100 mock 거짓 기술) 은 arXiv preprint 에 **둘 다 부재**하며 (verify_mock_false_detection.py 자체 0회 인용, 0.42σ 토큰 0회 출현, PASS_STRONG 토큰 8회 모두 negative 문맥), 본 sweep 에서 새로 발견된 mismatch 는 HIGH 3건 (L81 "0/1000" vs claims_status "0/200", RAR universality 철회 명시 부재, SPARC per-galaxy 0.427 dex spread 인용 부재) + LOW 6건이며, 정정 권한은 8인 Rule-A 에 있고 본 단일 세션 권한 밖이다.
