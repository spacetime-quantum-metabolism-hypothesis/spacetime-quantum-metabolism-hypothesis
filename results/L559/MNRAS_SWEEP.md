# L559 — paper/MNRAS_DRAFT.md 전수 mismatch sweep

세션: L559 (단일 세션, grep + 디스크 cross-check 만, **paper edit 0건**)
일자: 2026-05-02
대상: `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/paper/MNRAS_DRAFT.md` (197 lines)
디스크 사실 근거:
- `paper/verification/verify_milgrom_a0.py` (직접 실행 stdout 재현)
- `paper/verification/verify_mock_false_detection.py` (직접 실행 stdout 재현)
- `paper/verification/expected_outputs/verify_milgrom_a0.json`, `verify_mock_false_detection.json`
- `claims_status.json` v1.2 (L516 동기화)
- `results/L482`, `L491`, `L495`, `L498`, `L503`, `L506`, `L509`, `L550`, `L553`

배경: L555 R6 — L553 가 sample-only 검토 (3 라인 + RAR universality 만). 본 L559 는 197 라인 전수 sweep.

---

## §1 수치 mismatch 표

| Line | Section | paper 표기 | 디스크 사실 (인용 경로) | Status |
|------|---------|-----------|---------------------|--------|
| 14 | 정직 한 줄 | "0.42σ deviation, PASS_STRONG" | stdout `0.71 sigma` + `PASS` (verify_milgrom_a0.py 직접 실행); JSON `"verdict": "PASS"` (expected_outputs/verify_milgrom_a0.json L10) | **MISMATCH** (CRITICAL — abstract surface) |
| 28 | Abstract | "gives a 0.42σ deviation" | 산수 `\|1.129−1.20\|/0.10 = 0.71σ` (paper L87 자체 산수와도 모순) | **MISMATCH** (CRITICAL) |
| 82 | §3.1 | "a₀(SQT) ≈ 1.129 × 10⁻¹⁰ m s⁻²" (H₀=73, c=2.998e8) | 디스크 verify_milgrom_a0.py 산출 `1.129e-10` (실측 stdout 재현 일치) | **OK** |
| 85 | §3.2 | "SPARC RAR fit (**174** galaxies)" | claims_status.json L102 `SPARC 175 / 3389 pts`; L1.094 caveat 인용도 175 | **MISMATCH** (LOW; 174 vs 175 — 1 galaxy diff, 출처 표기 불일치 가능성) |
| 87 | §3.2 산수 | "0.71σ" | 산수 일치 ✓ | **OK** |
| 89 | §3.2 본문 괄호 | "verification script's H₀=73 input ... yields **0.42σ**; ... we adopt 0.71σ ... and quote 0.42σ as the verification-script result" | verify_milgrom_a0.py 는 0.42σ 를 **절대 출력하지 않음** (단일 경로 σ_obs=0.1e-10 고정, 0.71σ 만 출력) — paper L89 "verification-script result = 0.42σ" 진술은 거짓 | **MISMATCH** (CRITICAL — 거짓 인용; L553 §3 R3 평가에서 single-handed reject 위험 지목) |
| 92 | §3.3 | "H₀=67.4 → 1.04 × 10⁻¹⁰ (1.6σ low)" | 손계산 `(1.20−1.04)/0.10=1.6σ` ✓; 1.04 = 2.998e8·(67.4e3/3.086e22)/(2π) ≈ 1.0418e-10 (반올림 OK) | **OK** |
| 92 | §3.3 | "H₀=73.0 → 0.71σ" | ✓ | **OK** |
| 130 | §5.2 JSON snippet | `"deviation_sigma": 0.71` | JSON 디스크 L9 `0.71` ✓ | **OK** |
| 131 | §5.2 JSON snippet | `"verdict": "PASS_STRONG"` | JSON 디스크 L10 `"verdict": "PASS"` | **MISMATCH** (HIGH — 디스크 JSON 과 paper 가 인용한 JSON 비대칭) |
| 132 | §5.2 JSON snippet | `"H0_input_km_s_Mpc": 73.0` | 디스크 JSON 에 이 키 부재 (`expected` 블록에는 a0/dev/verdict 만) | **MISMATCH** (LOW — paper 가 디스크 schema 에 없는 키 인용) |
| 137 | §5.3 mock falsifier | "a *fabricated* H₀ = 100 input and confirms that the framework would reject (**≥ 5σ deviation**)" | verify_mock_false_detection.py 는 H₀=100 입력 토큰 자체 부재. 실제 동작: LCDM mock 200회 anchor-fit false-positive rate 계산. 직접 stdout: `three-regime false-detection rate on LCDM mock: 100.0%` + `CAVEAT: high rate => anchor-driven advantage on null data.` (5σ 토큰 무관, "framework rejects" 토큰 무관) | **MISMATCH** (CRITICAL — paper 가 인용한 동작이 디스크 스크립트와 전혀 다름; L553 §2.4 에서 미해결로 남긴 항목 확정) |
| 26-28 abstract | "1.13 × 10⁻¹⁰" / "1.129" / "(1.20 ± 0.10)" | 디스크 1.129e-10 ✓; 손계산 c·H₀/(2π) for H₀=73 = 1.1287e-10 → 1.13/1.129 둘 다 OK | **OK** |

추가 확인:
- §4.2 BTFR L107: "M_b ∝ V_f⁴ ... No additional parameter" — 디스크 SPARC slope fit (L482 / L491 검증) 결과 인용 없음. 정성 일치 진술만. **MISMATCH 아님** (정량 토큰 없음).
- §1 figure caption / §TABLES — paper 본문에 figure / table 본체 미포함 (texx file 빈 placeholder). 추후 figure 첨부 시 별도 sweep 필요.

---

## §2 Grade claim mismatch 표

paper 가 사용한 grade 토큰:

| Line | Section | paper grade | claims_status.json 등록 grade | Status |
|------|---------|-------------|------------------------------|--------|
| 14 | 정직 한 줄 | "PASS_STRONG" (a₀) | rar-a0-milgrom: `PASS_MODERATE` (claims_status L98; L516 demotion ΔAICc=+4.707, k_h=2) | **MISMATCH** (CRITICAL — claims_status v1.2 self_audit_distribution `PASS_STRONG: 0` 명시) |
| 28 | Abstract | "PASS on a₀ alone" (단순 PASS) | PASS_MODERATE | partial — abstract 의 generic "PASS" 는 enum 외 (디스크 enum 은 PASS_STRONG/PASS_MODERATE/PASS_QUALITATIVE/PASS_IDENTITY/PASS_BY_INHERITANCE). enum 비준수. |
| 74 | §2.4 | "one PASS_STRONG numerical match" | PASS_MODERATE | **MISMATCH** (HIGH — §6.1 limitations honesty 와 비대칭) |
| 131 | §5.2 JSON | `"verdict": "PASS_STRONG"` | 디스크 JSON `"verdict": "PASS"` (legacy enum); claims_status `PASS_MODERATE` | **MISMATCH** (HIGH — §1 항목과 중복) |
| 192 | submission checklist | "verify_milgrom_a0.py runs PASS_STRONG on reviewer machine" | 디스크 stdout 은 단순 `PASS` 토큰 (`PASS_STRONG` 미출력). claims_status 는 `PASS_MODERATE` | **MISMATCH** (HIGH — reviewer 가 clone/run 시 즉시 발견; PASS_STRONG vs PASS 표기 충돌) |
| classifications JSON L3 | (verify_milgrom_a0.json) | `"classification": "PASS_STRONG (substantive prediction, MOND a_0)"` | classifications meta 자체는 디스크 file 이지만 claims_status v1.2 L516 demotion 적용 시 `PASS_MODERATE` 로 동기화 필요 | **DRIFT** (paper 가 직접 인용은 안 함; 별도 sync 항목) |

**디스크 v1.2 distribution 정합성**: claims_status.json L25-L42 "self_audit_distribution" 은 `PASS_STRONG: 0`, 모든 substantive 행은 PASS_MODERATE/PASS_QUALITATIVE 로 demoted. paper 본문 `PASS_STRONG` 5회 출현 (L14, L74, L131, L192, JSON snippet) — **5/5 모두 schema 위반**.

paper 가 사용 안 한 grade (claims_status enum):
- `PASS_QUALITATIVE` (Bullet 에 적용; paper §4.3 본문에 명시 없음 — 정성 한도 캐비엣은 텍스트로 들어 있으나 grade label 부재)
- `PASS_BY_INHERITANCE`, `PASS_IDENTITY`, `CONSISTENCY_CHECK` 등 — Path-γ scope 외 → 정합 (인용 불필요)

---

## §3 Citation pointer broken/drift links

| Line | paper 인용 path | 디스크 실재 여부 | Status |
|------|---------------|---------------|--------|
| 96, 122, 164 | `paper/verification/verify_milgrom_a0.py` | 존재 ✓ | **OK** |
| 97, 165 | `paper/verification/expected_outputs/verify_milgrom_a0.json` | 존재 ✓ | **OK** |
| 137, 164, 193 | `paper/verification/verify_mock_false_detection.py` | 존재 ✓ (단 동작 mismatch — §1 L137 항목 참조) | OK (path) / **MISMATCH** (의미) |
| 164 | `paper/verification/compare_outputs.py` | 존재 ✓ | **OK** |
| 166 | `paper/verification/conda_env.yml` | 존재 ✓ | **OK** |
| 162 | `github.com/[redacted]/spacetime-quantum-metabolism-hypothesis` | redacted; 검증 불가 | OPEN |
| 163 | git tag `mnras-v1-l539` | `git tag` 미확인 (본 세션 scope 외) | OPEN |
| paper 외 implicit | `results/L482`, `L491`, `L498` | 존재 ✓ (L495 도 존재) | **OK** |
| paper 외 implicit | `results/L503`, `L506`, `L509` (claims_status 가 cite) | 본 sweep scope 외 ls 미실행 (claims_status 가 cite, paper 본문 cite 없음) | N/A |

**broken link 0건**. 모든 paper 본문이 인용한 path 실재 ✓. 단 `verify_mock_false_detection.py` 는 path 는 실재하지만 paper 가 기술한 *동작* (5σ reject) 과 디스크 *동작* (false-positive rate) 이 **다른 스크립트**.

---

## §4 Caveat coverage 매핑

claims_status.json + base.md 의 핵심 caveat 들이 paper 본문에 어떻게 (또는 못하고) 들어있는지:

| Caveat | claims_status 등록 | paper 본문 위치 | Coverage |
|--------|-------------------|----------------|----------|
| Verlinde 2017 numerical degeneracy | base.md / paper §2.4 자체 caveat | L45, L71, L74, L145, L156, L184, L195 (7회 출현) | **FULL** (가장 잘 된 coverage) |
| Bullet 잔존 cluster DM | claims_status `bullet-cluster: PASS_QUALITATIVE` (L107-L114; L509 Abell 520 conflict) | L39, L110 (정성 진술), L148 (limitation 1줄) | **PARTIAL** — Abell 520 dark-core conflict (L509) 명시 부재. paper 는 "이 framework 는 cluster DM 제거 안 함" 만 진술; "MOND-style 자체가 4/4 PASS_STRONG_QUANTITATIVE 불가, Abell 520 직접 충돌" 디스크 사실 누락. |
| Hidden DOF 9–13 (L495) | claims_status L23 limitation `L23-hidden-DOF-zero-param-overclaim`, ACK | paper 본문 0회 — "zero free parameter" 광고는 abstract 에 없으나, "no additional parameter" L107 BTFR 진술이 hidden DOF 9-13 audit 미언급 | **MISSING** (HIGH — claims_status future_plan 이 "abstract 부터 정정" 요구; paper §6 limitations 7개에 hidden DOF 항목 없음) |
| Son+2025 contingency | base.md / 다른 paper 들에 등장; MNRAS scope (galactic-only) 에선 cosmology contingency 와 무관 | paper 본문 0회 | **N/A** (Path-γ scope 외; missing 정당) |
| RAR universality 철회 (L491/L492/L503) | claims_status L26 `L26-RAR-a0-NOT-universal` ACK; future_plan 이 abstract/§4.1 에 'subset-stability ACK' 캐비엣 추가 요구 | paper §4.1 (L103-L104) "we *do not* derive μ(x); asymptotic limits consistent" 만 — universality 철회 명시 없음. §6 limitations 에도 없음. | **MISSING** (HIGH — L553 §2.2 도 동일 gap 지목; claims_status future_plan 직접 위반) |
| L502 AICc honest (PASS_STRONG 0/33) | claims_status L24 ACK | paper 본문 0회 — paper 는 PASS_STRONG 5회 출현 (§2 표 참조) | **MISSING** (CRITICAL — claims_status 와 paper 가 정반대 메시지) |
| L498 falsifier independence (N_eff ≈ 4) | claims_status L25 ACK | paper §5.3 만; "5σ" 단일 토큰 (디스크 동작과도 mismatch — §1 L137) | **MISSING** + **MISMATCH** (Path-γ 가 cosmology falsifier 인용 안 해도 정당하지만, 인용한 것 (mock falsifier) 자체가 거짓) |
| Cassini channel-conditional (L506) | claims_status L27 ACK | Path-γ scope 외 — paper 본문 cassini 미언급 | **N/A** (정당) |
| EFE / dwarf spheroidal | (없음 — limitation 으로만 존재) | L28, L114, L149 (3회) | **FULL** |
| H₀ tension sensitivity | base.md / paper §3.3 자체 caveat | L92, L150 (§6 limitation 6) | **FULL** |
| SPARC galaxy-by-galaxy fit 부재 | base.md | L28, L113, L147 (3회) | **FULL** |
| μ(x) 미유도 | base.md | L54, L104, L146 | **FULL** |

**미커버 caveat 3개** (HIGH 우선순위):
1. Hidden DOF 9-13 (L495)
2. RAR universality 철회 (L491/L492/L503)
3. L502 AICc PASS_STRONG 0 정직성

---

## §5 정정 우선순위

### CRITICAL (single-handed reject 위험; reviewer 가 즉시 발견)
1. **L89 거짓 인용** ("verification-script result = 0.42σ"): 디스크 코드는 0.42σ 출력 불가 → reviewer clone/run 즉시 발각, data fabrication 의심 트리거. **괄호 전체 삭제**.
2. **L137 mock falsifier 동작 거짓 기술** ("≥ 5σ deviation, framework rejects"): 디스크 스크립트 동작은 false-positive rate (100%) 산출, 5σ 무관. **§5.3 본문 재작성** — 실제 디스크 caveat (anchor-fit advantage 가 null data 에서도 살아남음) 으로 교체.
3. **L14 / L28 abstract `0.42σ`**: 본문 산수 (L87) 와 자체 모순. **`0.42σ → 0.71σ` 토큰 치환**.
4. **L14 / L74 / L131 / L192 `PASS_STRONG`**: claims_status v1.2 `PASS_STRONG: 0` 와 정반대. 디스크 verdict `PASS` (legacy enum) / claims_status `PASS_MODERATE` (v1.2 enum). **`PASS_STRONG → PASS_MODERATE` 일괄** (또는 claims_status 동기화 한 후 `PASS`).

### HIGH (referee round 신뢰 타격)
5. **Hidden DOF 9-13 disclosure 누락** (claims_status L23 future_plan 직접 위반): §6 limitations 또는 §2.1 P1-P3 부근에 한 줄 추가.
6. **RAR universality 철회 캐비엣 부재** (claims_status L26 future_plan 직접 위반): §4.1 말미에 "aggregate-only match; per-galaxy/environment universality not claimed (L491/L492/L503)" 추가.
7. **L502 AICc honest disclosure 누락**: §6 limitation 8번째 항목으로 "Hidden DOF k_h_applicable=2 + ΔAICc=+4.707 → AICc-honest 등급은 PASS_MODERATE; PASS_STRONG 표기는 단순 임계값 (dev<2σ) 기반의 코드 verdict" 추가.
8. **L131 JSON snippet 디스크 schema drift**: `H0_input_km_s_Mpc` 키 디스크 부재. 디스크 JSON schema 에 맞춰 paper snippet 재작성 *또는* 디스크 JSON 에 키 추가 (별도 4인 Rule-B).
9. **§4.3 Bullet 정성 한도 명시화**: Abell 520 dark-core conflict (L509) 한 줄 추가 — claims_status `cross_channel_caveat_L509` 정직 반영.

### LOW (reviewer 외부 발견 가능성 낮음, 정직성 차원)
10. **L85 `174 galaxies` vs claims_status `175`**: 1-galaxy 차이. Lelli+2017 원논문 정확 카운트 재확인 후 통일.
11. **L132 `H0_input_km_s_Mpc` 키**: 디스크 schema 에 추가하거나 paper snippet 에서 삭제.
12. **L74 "PASS_STRONG numerical match" → "single < 1σ numerical match"**: PASS_STRONG 토큰 자체 회피하면 grade-system 일관성 자동 확보.

### Non-trigger (이미 정합 / 본 sweep scope 외)
- L82, L87, L92, L130 수치: 디스크 정합 ✓
- Verlinde / EFE / μ(x) / H₀ sensitivity caveat 들: FULL coverage ✓
- 인용 path: broken 0건 ✓
- L162-L164 git tag / repo URL: redacted, scope 외

---

## §6 정직 한 줄

본 L559 sweep 은 paper/MNRAS_DRAFT.md 197 라인을 전수 정독하고 디스크 cross-check 만 수행했으며 paper / claims_status / 검증 스크립트 어느 디스크 파일도 수정하지 않았다 — L553 의 sample-only 검토가 놓친 7건 (§5.3 mock falsifier 동작 거짓 기술 [CRITICAL], paper L74 PASS_STRONG 진술 [HIGH], L131 JSON snippet `PASS_STRONG` + `H0_input` 키 drift [HIGH/LOW], L192 submission checklist `PASS_STRONG` [HIGH], L85 174 vs 175 galaxy 카운트 [LOW], hidden DOF 9-13 disclosure 부재 [HIGH], L502 AICc honest disclosure 부재 [HIGH], §4.3 Abell 520 conflict 명시화 [HIGH]) 가 본 라운드에서 추가 발견되었으며, 이 모든 정정은 8인 Rule-A 의무이고 본 단일 세션의 권한 밖이다.
