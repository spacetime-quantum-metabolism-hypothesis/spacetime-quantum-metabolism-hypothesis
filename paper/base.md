# SQT 논문 — 설계도 + 이론적 토대 (base.md)

> **가제**: *시공간 양자 이론(SQT): 암흑에너지 기원·MOND a₀·반증 가능 우주론을 위한 6공리 framework*
> **배포**: GitHub 공개, DOI publish
> **타겟 독자**: 학계 reviewer + 일반 청중 (과학 유튜브 시청자 수준)
> **저자 및 도구**: 인간 연구자가 최초 아이디어와 모든 결정 수행. 일부 시뮬레이션과 문헌 정리에 AI 도구 보조 사용.

---

## ⚠️ 작성 원칙 (CRITICAL)

> **본 paper 는 현재 repo 와 *완전히 독립적으로* 배포된다.**
> 실제 paper 작성 시 다음 repo-내부 식별자는 **반드시 모두 제거**:
>
> - **Lxxx 형식 loop ID** (L77, L207 등) — 내부 작업 흔적
> - **Pxxx 형식 prediction ID** (P15, P22 등) — 내부 enumeration → *서술형* 이름으로 대체
> - **REVIEW.md / report.json / SYNTHESIS_xxx.md 등 내부 파일 참조**
> - **반복 작업 횟수 (loop count)** — 학계 paper 의 신뢰성과 무관, 모두 제거
>
> ### 내부 명칭 → 외부 paper 표기 치환 표 (★ 필수)
>
> | 내부 명칭 | 외부 paper 표기 (영문 / 한국어) |
> |----------|------------------------------|
> | Branch B | "three-regime σ₀(env) parameterization" / "3-regime σ₀ 모형". 첫 사용 시 풀어 쓴 후 약어 *the three-regime model* 가능 (학계 jargon 회피) |
> | Branch A | "monotonic σ₀(env) hypothesis" / "단조 σ₀ 가설" (chronology 설명 시) |
> | F1 / F2 / F3 | "causality test", "Lorentz-invariance test", "vacuum-stability test" / "인과성 검증", "로렌츠 불변성 검증", "진공 안정성 검증" |
> | Pillar 1–4 | **"foundation"** (학계 톤). "Schwinger-Keldysh open-system foundation" 등. 한국어: **"축"** ("4 미시 축") |
> | "Tier A / Tier B" | "minimal model / V(n,t)-extended model" / "최소 모델 / V(n,t)-확장 모델" |
> | axiom a1–a6 | **"postulate" 권고** (관측 검증 대상이므로). 첫 사용: "we adopt six postulates (P1–P6, hereafter axioms for brevity)" |
> | derived D1–D5 | 첫 사용 시 "derived relation 1: Newton's G recovery" 등 풀어 쓰기 |
>
> ### 용어 결정 요약 (★ P0)
> - 영문: **postulate** (axiom 약식 OK), **foundation** (pillar 대신)
> - 한국어: **공리** (postulate 번역), **축** (foundation 번역)
>
> **검증**: 최종 PDF 에 `L\d{2,3}`, `P\d{1,2}`, `Branch [AB]`, `Pillar [1-5]`, `F[1-3]` pattern 0건. publish 전 grep 확인 필수.
>
> **본 base.md 의 두 역할**:
> 1. 논문 설계도 (구조, figure/table 계획)
> 2. **이론적 토대 서술** (실제 본문 작성 시 substantive source)

---

## 🌐 다국어 구조 (Bilingual Structure)

### GitHub repository 구조 (final)

```
├── README.md                  ← English landing page (★ section A 참조)
│   └── 최상단 language switcher: 🇺🇸 English | 🇰🇷 한국어
├── README.ko.md               ← 한국어 full mirror (요약본 아님)
│   └── 최상단 language switcher
├── LICENSE                    ← MIT (코드) + CC-BY-4.0 (텍스트/그림)
├── LICENSES.md                ← 디렉토리별 license 표 (어느 폴더가 어느 license)
├── CITATION.cff               ← Zenodo DOI citation
├── claims_status.json         ← 22행 한계 표 + 22 예측 표 machine-readable
├── .github/
│   ├── workflows/
│   │   └── verify.yml         ← CI/CD 자동 검증 (PASS/FAIL badge 생성)
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── verification_failure.md
│   │   └── suggestion.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── CONTRIBUTING.md
│   ├── CODE_OF_CONDUCT.md
│   └── og-image.png           ← GitHub social preview (1200×630)
├── paper/
│   ├── main_en.tex            ← English paper (master, ★ section B 참조)
│   ├── main_ko.tex            ← 한국어 paper (mirror)
│   ├── main_en.pdf / main_ko.pdf
│   ├── base.md                ← 본 설계도 (한국어, 내부 작업용)
│   ├── base_en.md             ← English design (대외 공개)
│   ├── verification/          ← ★ section C 참조
│   │   ├── README.md          ← 5줄 quickstart
│   │   ├── README.ko.md
│   │   ├── requirements.txt   ← version pinning
│   │   ├── conda_env.yml
│   │   ├── Dockerfile
│   │   ├── verify_*.py        ← 영문 주석, tqdm 진행 표시
│   │   ├── ai_prompts/
│   │   ├── expected_outputs/  ← reference output
│   │   ├── compare_outputs.py ← diff 도구
│   │   └── TROUBLESHOOTING.md
│   ├── verification_audit/    ← ★ 내부 8인 cold-blooded audit (R1–R8), §6.1.2 raw evidence
│   │   ├── R*.md              ← audit 결과 보고 (8개)
│   │   ├── R*.py              ← audit 재현 스크립트
│   │   └── R*.json            ← audit raw evidence (machine-readable)
│   ├── figures/
│   │   ├── hero.png           ← I1 infographic (README embed)
│   │   ├── og-image.png       ← social preview
│   │   └── F0–F9, I1–I4
│   ├── faq_en.md / faq_ko.md
│   └── TRANSLATION_POLICY.md
├── results/                   ← 공개 정책: 공개 + 별도 README 로 internal ID 설명
│   └── INTERNAL_IDS.md        ← Lxxx / Pxxx / Branch 등 내부 명칭 → paper 외부 명칭 매핑
└── data/                      ← 외부 데이터 mirror (SPARC subset 등)
```

### 우선순위
1. **GitHub landing page (`README.md`)**: 영문 master, 첫 줄 language switcher
2. **GitHub release**: 영문 + 한국어 PDF 양방
3. **Zenodo DOI**: GitHub release tag → Zenodo 자동 연동 → DOI 발급
4. **DOI 발급 후**: README/CITATION.cff/paper PDF 에 DOI 추가 commit
5. **arXiv 제출 안 함** (별도 학술 publishing 채널 사용 안 함)
6. **Code/주석/docstring**: 영문 (커뮤니티 호환)

### 번역 정책 (`TRANSLATION_POLICY.md` 별도 작성)
- **Master 언어**: 영문. 영문 update 가 한국어보다 *항상* 선행
- **Mirror lag 허용**: 영문 update 후 한국어 7일 이내 sync
- **README.ko.md 정책**: 영문 README 의 *full mirror* (요약본 아님)
- **학계 용어**: 영문 그대로 (falsifier, postdiction, marginalized 등)
- **핵심 결과 수치**: 영문/한국어 정확 동일
- **정직 caveat 강도**: 영문/한국어 동일 (한쪽 약화 금지)

---

## 🎨 GitHub UX 3-layer spec (★ 신설)

> 본 framework 는 *서로 다른 톤·길이·정보 우선순위* 를 가진 3개 layer 산출물.
> 각 layer 의 *별도 spec* 명시.

### Layer A — `README.md` (GitHub landing page)

**대상**: 첫 방문자 (3초 안에 "이 repo 가 뭔가" 파악)
**길이**: 1 페이지 스크롤 (모바일 기준)
**톤**: 일반 청중 + 학계 양방 친화

#### A.1 필수 구성 요소 (위→아래 순서)

```markdown
# Spacetime Quantum Theory (SQT)

🇺🇸 English | [🇰🇷 한국어](README.ko.md)

[badges: DOI (Zenodo) | CI | License | OSF preregistration]

![Hero infographic](paper/figures/hero.png)

> **One-sentence headline**: *"A 6-axiom framework that derives the cosmological constant scale and Milgrom's a₀ from spacetime-quantum dynamics — with explicit honest disclosure of where it fails."*

## TL;DR
- ⚠️ ρ_q/ρ_Λ(Planck) order-unity (CONSISTENCY_CHECK; circularity structural — see §5.2; L402 audit confirmed unavoidable)
- ✅ a₀ = c·H₀/(2π) derivation
- ✅ Bullet cluster offset PASS (where MOND fails)
- ❌ S_8 tension: SQT *worsens* by +1.14% (OBS-FAIL, structural, no escape)
- ⚠️ Three-regime σ₀(env) is post-hoc fit, not a priori prediction
- ⏰ **Decisive falsifier: DESI DR3 w_a (2025–2026)**
- 📊 Self-audit (32 claims, *L402–L415 reframed + L495/L502/L513/L515 hidden-DOF audit*): **★ honest headline (hidden-DOF AICc penalty applied, L502): PASS_STRONG 0% (0/32, no qualifying candidate)**. Reference distribution (penalty *not* applied): substantive 13% (4) + σ₀-identity 9% (3) + inheritance 25% (8) + CONSISTENCY_CHECK 3% (1, Λ origin) + partial 25% (8) + NOT_INHERITED 25% (8) + framework-FAIL 0. Raw advertised counts pre-L412 31% / post-L412 28% are *hidden-DOF AICc penalty unapplied*; **standalone citation prohibited** (must accompany hidden-DOF 0% headline; L513/L515). 9 hidden DOFs identified (L495). 6 pre-registered falsifiers compress to N_eff=4.44, 8.87σ ρ-corrected combined (L498). Full §6.1 22-row + §6.5(e) single source of truth + raw evidence in [paper/verification_audit/](paper/verification_audit/)

## Verify in 5 seconds
\`\`\`bash
git clone https://github.com/<user>/<repo>.git
cd <repo>/paper/verification
pip install -r requirements.txt
python verify_lambda_origin.py     # Λ origin dimensional consistency check (circular w.r.t. ρ_Λ_obs — see §5.2)
\`\`\`
4 more scripts in `paper/verification/`. See [Verification README](paper/verification/README.md).
For internal audit details (R1–R8 cold-blooded audit), see [paper/verification_audit/](paper/verification_audit/).

## Claims status (machine-readable: claims_status.json)

*Summary view of full 22-row limitations table (§6.1) + 11-row PASS table (§4.1). Each row below aggregates one or more entries in the canonical tables; see cross-reference column.*

*Two distinct meanings of "fail" used throughout this document (do not conflate):*
- ❌ **OBS-FAIL** (observational worsening) — SQT structurally worsens fit to a real dataset, no parameter escape from the theory side (e.g. S_8). This is a *theory-vs-data tension*.
- 🚫 **FRAMEWORK-FAIL** (internal inconsistency) — the paper framework itself contains a logical / mathematical contradiction surfaced by self-audit. **Currently 0** (see §6.5(e)).

| Claim | Status | Evidence | Caveat | Maps to |
|-------|--------|----------|--------|---------|
| Λ origin | ⚠️ CONSISTENCY_CHECK | ρ_q/ρ_Λ order-unity match (dimensional consistency, *not* a prediction) | circularity structural (n_∞ uses ρ_Λ_obs as input via axiom 3); L402 Path-α independent derivation failed (10⁶⁰ mismatch) | §5.2; §6.1 row 13 (Λ_UV definitional) |
| MOND a₀ | ✅ PASS | a₀ = c·H₀/(2π), ~1σ | geometric 1/(2π) plausibility | §1.2.2 |
| Bullet cluster | ✅ PASS_STRONG | offset consistent (where MOND fails) | qualitative | §4.1 row 10 |
| BBN ΔN_eff | ✅ PASS_STRONG | ΔN_eff ≈ 10⁻⁴⁶ < 0.17 | consistency, not prediction; L502 hidden-DOF AICc → ΔAICc≥+18 (k_h=9) demotes to ≤PASS_MODERATE | §4.1 row 2; §6.5(e) L513 |
| Solar-system PPN (Cassini, GW170817, LLR, EP) | ✅ PASS_STRONG / PASS_BY_INHERITANCE | \|γ−1\|≈10⁻⁴⁰; \|Δc/c\|=0; Ġ/G=0; \|η\|=0 | GW170817 / LLR are PASS_BY_INHERITANCE (legacy `PASS_TRIVIAL` alias — Lagrangian-form choice + axiom tautology); disformal revival ⇒ KILL; L506 Cassini cross-form CHANNEL_DEPENDENT (universal coupling 4/4 FAIL); L502 hidden-DOF AICc demotes Cassini/EP to ≤PASS_MODERATE | §4.1 rows 3–6; §6.5(e) L513 |
| Three-regime σ₀(env) | ⚠️ POSTDICTION | 17σ regime-gap | data-driven anchors, not a priori | §3.4; §6.1 rows 5–7 (anchor strength, sloppy d_eff, theory-prior) |
| CMB θ_* shift | ⚠️ PARTIAL | δr_d/r_d ≈ 0.7% (Planck σ × 23) | matter-era φ evolution; same channel as Phase-2 BAO | §4.1 row 8 |
| S_8 tension | ❌ OBS-FAIL (structural worsening) | +1.14% worse than ΛCDM (ξ_+ +2.29%) | structural μ_eff≈1, no parameter escape (data tension; framework internally consistent) | §4.6; §6.1 row 1; §6.1 row 14 (cosmic-shear external) |
| DESI w_a | ⏰ PENDING | DR3 2025–2026 | minimal SQT: w_a=0; V(n,t)-extension gate OPEN | §4.3, §4.4, §5.4; §6.1 row 12 |
| Foundational/inheritance gaps | ⚠️ NOT_INHERITED | 8/32 claims (singularity, Volovik, Jacobson, GFT/BEC chain) | axiom 4 5th-pillar decision (Causet vs GFT) blocks 5 of 8 | §6.1 rows 15–22 |

## How to cite
\`\`\`bibtex
@article{<author><year>,
  title   = {<title>},
  author  = {<author>},
  year    = {<year>},
  version = {1.0},
  doi     = {10.5281/zenodo.<id>},
  url     = {https://github.com/<user>/<repo>}
}
\`\`\`

> **DOI versioning**: Zenodo concept DOI 는 모든 버전 통합, version DOI 는 특정 release 인용. paper 본문 인용은 *concept DOI* 권장.

## Documentation
- [Paper PDF (English)](paper/main_en.pdf) | [Paper PDF (한국어)](paper/main_ko.pdf)
- [FAQ for general audience](paper/faq_en.md) | [한국어 FAQ](paper/faq_ko.md)
- [Verification quickstart](paper/verification/README.md)
- [Honest limitations table (machine-readable)](claims_status.json)
- [Pre-registration on OSF](<osf-link>)

## Contributing
See [CONTRIBUTING.md](.github/CONTRIBUTING.md).

## License
Code: MIT. Text/Figures: CC-BY-4.0. Per-directory table: [LICENSES.md](LICENSES.md).
```

#### A.2 모바일 친화 정책
- 모든 표는 4 column 이하 또는 `<details>` collapse
- 코드 블록 80자 이내 wrap
- LaTeX 수식은 Unicode 또는 image fallback (예: ρ_q, σ₀, H₀)
- Hero image 는 1200×630 (social preview 호환)

#### A.2.1 모바일 표 collapse 표준 양식

긴 표(>5행 또는 4 column)는 모바일에서 가로 스크롤을 유발하므로, default 부분(첫 N행) + `<details>` collapse 부분으로 분리한다. 각 표의 collapse 정책은 **표의 역할**(3초 hook 핵심 / 보충 자료)에 따라 결정한다.

**표별 collapse 정책 (정합성 R8 spec)**

| 위치 | 행 수 | Default 표시 | Collapse |
|---|---|---|---|
| README **Claims status** 표 | 7행 | 전체 7행 default (3초 hook 핵심 — collapse 금지) | 없음 |
| §4.1 **PASS 표** | 11행 | 첫 5행 | 6–11행 `<details>` |
| §6.1.1 표 | 14행 | 첫 5행 | 6–14행 `<details>` |
| §6.1.2 표 | 8행 | 첫 5행 | 6–8행 `<details>` |
| §4.6 **22 예측 표** | 22행 | 첫 8행 | 9–22행 `<details>` |
| **TODO 14장 표** | 카테고리별 | 카테고리별 첫 3 항목 | 4번째 이후 `<details>` |

**Markdown collapse syntax 표준 template**

```markdown
| col1 | col2 | col3 | col4 |
|---|---|---|---|
| row 1 ... |
| row 2 ... |
| row 3 ... |
| row 4 ... |
| row 5 ... |

<details>
<summary>Show full table (rows 6–N)</summary>

| col1 | col2 | col3 | col4 |
|---|---|---|---|
| row 6 ... |
| row 7 ... |
| ... |
| row N ... |

</details>
```

**주의사항**
- `<details>` 내부의 표는 헤더(`| col1 | col2 |` + `|---|---|`)를 **재선언** 필수 (GitHub Markdown 렌더러는 collapse 블록 내부 표를 독립 파싱)
- `<summary>` 텍스트는 collapse 행 범위를 명시 (예: "Show full table (rows 6–22)")
- collapse 정책 적용 시 표 *내용*은 손대지 않음 (R1/R3 작업과 분리)
- README Claims status 표는 3초 hook 의 핵심 신호이므로 default 전체 표시 강제

#### A.3 README.ko.md 정책
- README.md 의 *full mirror* (모든 섹션 동일)
- 학계 용어는 영문 + 한국어 병기 (예: "falsifier (반증 가능 검증)")
- 첫 줄 language switcher: `[🇺🇸 English](README.md) | 🇰🇷 한국어`

---

### Layer B — `paper/main_en.tex` (학계 본문)

**대상**: 학계 reviewer + 인용 연구자
**길이**: 표준 paper (본문 ~25 페이지 + appendix)
**톤**: 학술적, 정직, 정량

#### B.1 본문 (1–7장)
- 본 base.md 의 1–7장 구조 그대로
- 모든 내부 명칭 → 서술형 치환 (Branch B → "three-regime σ₀(env) parameterization" 등)
- Figure F0–F9 본문 통합
- Statistical methods appendix 신설 (R3 권고)

#### B.2 Appendix
- A: FAQ (8장 — 학생/일반인 보충)
- B: Verification (9장 — code 인용)
- C: Statistical methods (Bayes factor, BMA, mock injection 정의)
- D: Dataset inventory (4.2 표 확장)

#### B.3 Submission 전 grep 검증 (★ 절대 필수)
- `L\d{2,3}` 0건
- `P\d{1,2}` 0건
- `Branch [AB]` 0건
- `Pillar [1-5]` 0건
- `F[1-3]` test 명칭 0건 (서술형 치환)
- `loop`, `iter`, `iteration count` 0건

---

### Layer C — `paper/verification/README.md` (검증 quickstart)

**대상**: 학생, 시민과학자, skeptical reviewer
**길이**: 1 페이지 (5분 안에 첫 검증 완료)
**톤**: 실용, 단계별, 친절

#### C.1 필수 구성 요소

```markdown
# SQT Verification

🇺🇸 English | [🇰🇷 한국어](README.ko.md)

[CI badge: PASS/FAIL]

## 5-second quickstart
\`\`\`bash
pip install -r requirements.txt
python verify_lambda_origin.py
\`\`\`
Expected output: `ratio = 1.000000`. See `expected_outputs/`.

## All 5 verification scripts
| # | Script | Verifies | Time |
|---|--------|---------|------|
| 1 | verify_lambda_origin.py | ρ_q/ρ_Λ = 1.0000 | <1s |
| 2 | verify_milgrom_a0.py | a₀ = c·H₀/(2π) | <1s |
| 3 | verify_monotonic_rejection.py | 17σ regime-gap | <2s |
| 4 | verify_mock_false_detection.py | 100% false-positive rate caveat | <60s |
| 5 | verify_cosmic_shear.py | S_8 +1.14% → ξ_+ +2.29% | <1s |

## Compare to expected outputs
\`\`\`bash
python compare_outputs.py  # diff with reference
\`\`\`

## Reproduce with Docker
\`\`\`bash
docker build -t sqt-verify .
docker run sqt-verify
\`\`\`

## Conda environment
\`\`\`bash
conda env create -f conda_env.yml
conda activate sqt
\`\`\`

## LLM verification (alternative to Python)
30-minute LLM prompt verification: see `ai_prompts/`.

## Troubleshooting
See [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## Report a discrepancy
If your output differs from `expected_outputs/`, please open an issue using the [verification_failure template](../../.github/ISSUE_TEMPLATE/verification_failure.md).
```

#### C.2 Script 작성 규칙
- 영문 주석 (한국어 docstring 옵션)
- `tqdm` 진행 표시 (mock 200 회 등 hang 방지)
- 80자 line wrap
- `OMP_NUM_THREADS=1` 환경 변수 강제
- `np.random.default_rng(42)` seed 고정

#### C.3 `compare_outputs.py` 정책
- `expected_outputs/*.json` vs 실제 output JSON diff
- ±5% 허용 오차 (numerical reproducibility)
- PASS/FAIL 명확 출력

---

### 📐 작성 전 결정 사항 (Decisions, ★ P0)

본 섹션은 8인 검토 결과 paper 본문 작성 *전* 에 결정 필요한 항목들 정리.
별도 `paper/AMBIGUITIES.md` 가 living document 로 추적.

#### D-1. 17σ 정확값 + dof + sigma 환산 공식 (P0)
- 출처: 내부 verification result (정확 Δχ² 값)
- 본문 표기: "Δχ² = X (sigma = Y, 1-DOF Wilks approximation)"
- Statistical methods appendix 에 chi²-to-sigma 변환 공식

#### D-2. ρ_q/ρ_Λ 의 H₀ 의존성 표 (P1)
| H₀ (km/s/Mpc) | ratio ρ_q / ρ_Λ |
|--------------|-----------------|
| 67 (Planck) | (계산 필요) |
| 70 | (계산 필요) |
| 73 (SH0ES) | 1.0000 |

5.2 circularity caveat 옆 본문 + verification script 양방 명시.

#### D-3. Anchor ↔ Dataset 1:1 매핑 (P1)
| Anchor | log σ₀ | 출처 dataset | 측정 종류 |
|--------|--------|------------|----------|
| Cosmic | 8.37 | Planck CMB ρ_Λ | 우주론 standard |
| Cluster | 7.75 | A1689 (Limousin 2007) | strong + weak lensing |
| Galactic | 9.56 | SPARC (Lelli 2016) | rotation curves |

각 anchor 가 *measurement* 인지 *theory-prior* 인지 명시.

#### D-4. SPARC quality cut 정책 (P1)
- Baseline: Q=1 만 (90 galaxies, conservative)
- Robustness: Q=1+2 (확장 sample) — appendix only

#### D-5. Mock injection generative model (P1)
- Underlying truth: LCDM (Planck 2018 best-fit), σ_8 = 0.811
- Noise: Gaussian σ = 0.10 dex per galaxy
- N_mock = 200, seed = 42
- `verify_mock_false_detection.py` docstring 과 본문 spec 동기화

#### D-6. DESI DR3 inconclusive band 출처 (P1)
- Threshold (-0.5, -0.1) 가 *DESI DR3 projected σ(w_a) ~ 0.10–0.18 기반*
- 본문 4.4 절에 출처 명시

#### D-7. CI/CD 비용 제약 (P1)
- 5 verification script 총 실행 < 5분 보장 (GitHub Actions free tier)
- mock 200 회 등 무거운 검증은 cron 주간 실행 (PR 마다 안 함)

#### D-8. base.md vs base_en.md master 분리 (P1)
- *paper 본문* (main_en.tex): 영문 master
- *내부 설계* (base.md): 한국어 master (저자 native)
- *대외 공개 설계* (base_en.md): base.md 의 영문 번역
- TRANSLATION_POLICY.md 에 명시

#### D-9. results/ 공개 정책 사이즈 (P1)
- GitHub: *핵심 final synthesis + key figures* 만 (< 100 MB)
- Zenodo: 전체 bulk archive (raw simulation results)
- INTERNAL_IDS.md: 내부 ID → 외부 명칭 매핑

#### D-10. paper ↔ verification cross-link 형식 (P1)
- paper PDF footnote 에 GitHub URL + script filename
- 예: "verified by `verify_lambda_origin.py` at <github-url>/paper/verification/"

#### D-11. LaTeX class 결정 (P0)
- 학술 publishing 안 함 (arXiv/journal 안 함)
- *Generic LaTeX article class* (`\documentclass{article}` + `geometry`, `amsmath`, `graphicx`)
- 또는 더 학계 친화적 `aastex` (선택)

#### D-12. Figure 형식 (P2)
- 본문 figure: vector (PDF/SVG)
- README hero / social preview: raster (PNG, 1200×630)

#### D-13. ACK / RECOVERY 약어 풀이 + emoji 범례 (P3)
- ACK: "Acknowledged (no immediate fix path)"
- RECOVERY: "Partial mitigation underway (quantitative reduction)"
- README 첫 사용 시 emoji 범례:
  - ✅ pass — quantitatively verified
  - ⚠️ caveat — see paper Sec 6
  - ⏰ pending — awaiting future data
  - ❌ obs-fail — observational worsening, no escape from theory side (data tension; e.g. S_8)
  - 🚫 framework-fail — internal inconsistency surfaced by self-audit (currently 0)
  - 📊 self-audit summary — 32-claim cold-blooded audit; raw evidence in `paper/verification_audit/`

  *Emoji ↔ enum mapping (canonical, L460 sync)*: ✅ ↔ `PASS_STRONG` / `PASS_IDENTITY` / `PASS_BY_INHERITANCE` (legacy `PASS` / `PASS_TRIVIAL` deprecated), ⚠️ ↔ `PARTIAL` / `POSTDICTION` / `NOT_INHERITED` / `CONSISTENCY_CHECK`, ⏰ ↔ `PENDING`, ❌ ↔ `OBS-FAIL`, 🚫 ↔ `FRAMEWORK-FAIL`, 📊 ↔ summary metadata. Human-facing tables use emoji+label, machine-readable JSON uses enum only.

#### D-14. 한국어 paper 학술 인용 가치 (P2)
- 한국어 main_ko.pdf 는 *교육/대중 공개용* (학계 인용 목적 아님)
- 학계 인용 = 영문 main_en.pdf + Zenodo DOI

#### D-15. data/ 디렉토리 license 표 (P3)
- SPARC: CC-BY-4.0
- DESI: CC-BY-4.0
- Planck: CC-BY-4.0
- A1689 (Limousin): paper 인용만 (재배포 불가, 가공 결과만)
- 각 dataset 별 LICENSE 파일 + LICENSES.md 본 표

---

### 3-layer 정보 흐름

```
Layer A (README.md)         3초 첫인상 + 1페이지 TL;DR
    ↓ "Verify" 클릭
Layer C (verification/)     5분 직접 실행
    ↓ "Read paper" 클릭
Layer B (main_en.pdf)       30분 학술 본문
    ↓ "Cite" 또는 "Contribute"
CITATION.cff / CONTRIBUTING.md
```

---

### 추가 정책 파일

#### `claims_status.json` (★ machine-readable 25행 한계 [22 legacy + 3 audit overlay] + 22 예측)

*Status enum (canonical, **10 active values** — L402/L409/L411/L412/L415 reframed; do not conflate "OBS-FAIL" and "FRAMEWORK-FAIL"):*
- `PASS_STRONG` — substantive falsifiable prediction (additional axiom 입력 필요)
- `PASS_IDENTITY` — σ₀=4πG·t_P holographic 항등식의 산술 따름결과 (자유도 0, 차원 분석; **L409 분리 신설**)
- `PASS_BY_INHERITANCE` — 외부 prior knowledge 상속 (구 `PASS_TRIVIAL` 2건 흡수: GW170817 Lagrangian-form, LLR 동어반복)
- `CONSISTENCY_CHECK` — dimensional / order-unity match that is *not* a falsifiable prediction (e.g. §5.2 Λ origin per **L402/L412 down-grade**; 신설)
- `PARTIAL` — caveat 명시 — 함수형/관측 채널 부분 검증
- `POSTDICTION` — 데이터 fit 후 명명, a priori 도출 아님
- `PENDING` — falsifier 미도래 (DESI DR3 등)
- `NOT_INHERITED` — paper framework 외부, 미상속
- `OBS-FAIL` — *observational* worsening vs ΛCDM, no parameter escape from theory side (data tension)
- `FRAMEWORK-FAIL` — *internal* logical/mathematical inconsistency in the paper framework (currently 0; see §6.5(e))
- (legacy) `PASS`, `PASS_TRIVIAL` — deprecated aliases. 신규 항목 사용 금지; v1.1 마이그레이션 시 `PASS_BY_INHERITANCE` 또는 적절한 10-value 등급으로 치환.

> Self-audit 32 claim 분포 (L411 reframed, L415 sync, L513/L515 hidden-DOF overlay): **PASS_STRONG 4 (13%) + PASS_IDENTITY 3 (9%) + PASS_BY_INHERITANCE 8 (25%) + CONSISTENCY_CHECK 1 (3%, Λ origin) + PARTIAL 8 (25%) + NOT_INHERITED 8 (25%) + FRAMEWORK-FAIL 0**. 합 4+3+8+1+8+8 = 32 ✓. **★ L502 hidden-DOF AICc penalty 적용 시 PASS_STRONG 0/32 (0%) — 광고 substantive 13% 단독 인용 시 hidden-DOF 0% headline 동반 의무 (L513/L515)**. OBS-FAIL 은 §6.1.1 #1 (S_8) 별도 분류, claim 분포 외부. *Legacy 매핑*: 구 `PASS_STRONG 10` (pre-L412) = 신 `PASS_STRONG 4 (substantive) + PASS_IDENTITY 3 + CONSISTENCY_CHECK 1 (Λ origin) + PASS_BY_INHERITANCE 2 (Lagrangian-form/LLR)` (합 10 ✓). Post-L412 raw PASS_STRONG = 9/32 (28%) — Λ origin 제외.

```json
{
  "version": "1.0",
  "framework": "SQT",
  "claims": [
    {"id": "lambda-origin", "status": "CONSISTENCY_CHECK", "caveat": "circularity-structural (L412 down-grade from PASS_STRONG)"},
    {"id": "milgrom-a0", "status": "PASS"},
    {"id": "S8-worsening", "status": "OBS-FAIL", "kind": "observational-tension", "permanent": true, "framework_internal": false}
  ],
  "limitations": [...]  // 25 행 (§6.1.1 14 own + §6.1.2 8 audit-discovered + §6.1.3 3 advertised-count/independence/AICc audit, L495/L498/L502)
}
```

**i18n mapping 정책 (R6 추가, 2026-05-01)**:

- 영문 schema key (`id`, `status`, `caveat`, `kind`, `permanent`, `framework_internal`) 는 **master** — 모든 자동화 도구·CI·외부 인용은 영문 key 만 참조한다.
- 한국어는 *display string* 한정으로 inline `i18n` object 에 mirror. `README.ko.md` 등 한국어 미러 문서는 `claims[i].i18n.ko` 를 읽어 표를 렌더링한다.
- Status enum (10 active: `PASS_STRONG`, `PASS_IDENTITY`, `PASS_BY_INHERITANCE`, `CONSISTENCY_CHECK`, `PARTIAL`, `POSTDICTION`, `PENDING`, `NOT_INHERITED`, `OBS-FAIL`, `FRAMEWORK-FAIL`; legacy aliases `PASS`, `PASS_TRIVIAL` deprecated) 은 **영문 고정 — 번역 금지** (자동화 안정성). 한국어 표기가 필요하면 `i18n.ko.status_label` 별도 문자열 필드로만 제공.
- master(영문) ↔ mirror(한국어 i18n) drift 방지: CI 에서 모든 claim/limitation 항목에 `i18n.en.label` 와 `i18n.ko.label` 양쪽 존재 assertion. 누락 시 빌드 실패.
- 번역 정책 전반은 `TRANSLATION_POLICY.md` 참조 — *master = 영문 schema key, mirror = 한국어 `i18n` object* 원칙을 한 곳에 명문화.

권고 schema v1.1 (i18n 지원, 신규 작성용):

```json
{
  "version": "1.1",
  "framework": "SQT",
  "claims": [
    {
      "id": "lambda-origin",
      "status": "CONSISTENCY_CHECK",
      "caveat": "circularity-structural (L412 down-grade from PASS_STRONG; L402 Path-α independent derivation failed 10⁶⁰)",
      "permanent": false,
      "framework_internal": false,
      "i18n": {
        "en": {
          "label": "Λ origin (ρ_q/ρ_Λ order-unity match — dimensional consistency, not a prediction)",
          "caveat": "circularity is structural (n_∞ uses ρ_Λ_obs as input via axiom 3)",
          "status_label": "CONSISTENCY_CHECK"
        },
        "ko": {
          "label": "Λ 기원 (ρ_q/ρ_Λ order-unity 일치 — 차원 정합성, 예측 아님)",
          "caveat": "구조적 순환성 (n_∞ 가 axiom 3 을 통해 ρ_Λ_obs 를 입력으로 사용)",
          "status_label": "정합성 점검"
        }
      }
    },
    {
      "id": "milgrom-a0",
      "status": "PASS_STRONG",
      "i18n": {
        "en": {"label": "MOND a₀ = c·H₀/(2π)", "status_label": "PASS (strong)"},
        "ko": {"label": "MOND a₀ = c·H₀/(2π)", "status_label": "통과 (강함)"}
      }
    },
    {
      "id": "S8-worsening",
      "status": "OBS-FAIL",
      "kind": "observational-tension",
      "permanent": true,
      "framework_internal": false,
      "i18n": {
        "en": {"label": "σ_8 worsening +1.14%", "status_label": "OBS-FAIL (permanent)"},
        "ko": {"label": "σ_8 악화 +1.14%", "status_label": "관측-실패 (영구)"}
      }
    }
  ],
  "limitations": [
    /* 14 행, 각 항목도 동일 i18n 구조 (en/ko label 필수) */
  ]
}
```

**대안 schema** (대규모 번역 확장 시): 영문 master `claims_status.json` 과 별도 `claims_status_i18n.ko.json` 분리 후 `id` 키로 join. R6 권고는 inline `i18n` (단일 파일, 현재 규모 적합) — 향후 ja/zh 추가 시 분리형 전환 검토.

위 v1.0 예시는 LEGACY (i18n 미지원). 신규 항목 추가 시 v1.1 schema 사용.

#### `LICENSES.md` (디렉토리별 license 표)
```markdown
| Directory | License |
|-----------|---------|
| `paper/verification/*.py` | MIT |
| `paper/*.tex`, `paper/*.md` | CC-BY-4.0 |
| `paper/figures/*` | CC-BY-4.0 |
| `data/` | upstream license (SPARC: CC-BY-4.0) |
```

#### `.github/CONTRIBUTING.md`
환영 contribution 카테고리:
- 추가 cluster anchor 데이터 + analysis
- 번역 개선 (영문 ↔ 한국어)
- Figure / infographic 개선
- Verification script 확장
- Bug report / verification failure
- **§6.1.2 internal-audit NOT_INHERITED 항목 해결 PR**:
  - GFT 5번째 foundation 등재 (#18, #19, #25 동시 회복)
  - V(n,t) derivation gate 닫기 (#12, #20, #21)
  - 5 program 구조적 동형 명시 (#22)

#### `.github/CODE_OF_CONDUCT.md`
Contributor Covenant 2.1 표준.

#### `.github/ISSUE_TEMPLATE/`
- `bug_report.md`
- `verification_failure.md` (output 차이 보고용 표준)
- `suggestion.md`

#### `results/INTERNAL_IDS.md`
internal ID (Lxxx, Pxxx, Branch B 등) → paper 외부 명칭 매핑 표.
*results/ 디렉토리는 GitHub 공개 (negative result audit 용)*, 단 INTERNAL_IDS.md 가 외부 독자 안내.

---

## 0. 초록

**Headline**: *"SQT 는 anchor 데이터에서 σ₀(env) 의 monotonic form 을 강하게 기각하는 falsifiable test 를 통과하나, σ₀ 의 amplitude 자체는 first-principle 로 도출되지 않는다."*

핵심 4 claim:
1. 암흑에너지 기원 메커니즘 — ρ_q/ρ_Λ(Planck) order-unity 일치, **CONSISTENCY_CHECK only** (예측 아님; circularity 가 구조적임 — §5.2; L412 PR P0-1 적용으로 PASS_STRONG → CONSISTENCY_CHECK 강등)
2. MOND 가속도 a₀ 도출 — a₀ = c·H₀/(2π) (geometric factor)
3. Three-regime σ₀(env) parameterization — anchor 주도 (postdiction)
4. 22개 예측, 6 pre-registered falsifiers (N_eff=4.44 after correlation correction; 8.87σ combined, ρ-corrected) — DESI DR3 가 가장 결정적; 3 load-bearing orthogonal channels = CMB-S4 / ET / SKA (§4.9, L498)

**정직 disclosure**: σ_8 +1.14% structural worsening (**pre-registered as a 4.4σ Euclid DR1 cosmic-shear falsifier**, L406 forecast; central 4.38σ, 3σ falsification floor; two-sided decision rule §4.6), marginalized Bayes factor = 0.8 only, anchor circularity in Λ derivation, three-regime structure 는 데이터 fit 에서 발견된 postdiction.

**Self-audit 결과 (32 claim 검증, *L409–L414 통합 reframing + L495/L502/L503/L506 hidden-DOF audit 통합, L515 sync*)**:

- **★ 정직 헤드라인 (hidden-DOF AICc penalty 적용 후, L502)**: **PASS_STRONG 0% (0/32, 자격 유지 후보 0건)**. *applicable* k_hidden 만 적용해도 PASS_STRONG 7 후보 (substantive 4 + L482 RAR + Bullet + 3-regime postdiction) 중 3건 즉시 PASS_MODERATE 강등, 4건 RETAINED 경계 (전체 k_hidden=9 적용 시 함께 강등). L482 RAR ΔAICc(SQT−free) = +0.70(naive) → +4.7(applicable) → +18.8(전체).
- **광고용 raw 카운트 (★ 단독 인용 금지)**: pre-L412 PASS_STRONG 10/32 (31%) / post-L412 9/32 (28%). 본 카운트는 *hidden DOF AICc penalty 미적용* 상태 — L502 정직 기준에서는 0%. 단독 인용 금지 (L414/L495 ATTACK A4 cross-ref guard).
- **Hidden DOF 카운트 (L495)**: paper 광고 "0 free parameter" 는 *부정확*. 함수형 (M16) +1, anchor pick (cosmic/cluster/galactic) +3, Υ★ convention +1, B1 bilinear ansatz +1, three-regime carrier+saddle +2, axiom-scale stipulation +1 = **9 hidden DOF (보수) ~ 13 (확장)**. paper/TABLES.md row 1 의 "5 free parameters in Branch B" 의 약 2배. abstract/intro/appendix drift 8 위치 식별 → L515 차단 적용.
- **Universality cross-checks (L503/L506)**: a₀ universality K=1/4 PASS (per-galaxy intrinsic spread 0.427 dex ≫ 0.13 dex SPARC floor; KS dwarf-vs-bright p=0.005; cluster offset +0.7~+1.0 dex 미달). Cassini |γ−1| 8-channel cross-form **CHANNEL_DEPENDENT** (universal coupling at Phase-3 β=0.107 → |γ−1|≈2.3×10⁻² 로 ~10³× hard-fail; K_C1–C4 4/4 FAIL) — PASS_STRONG 은 dark-only / screening 채널 선택에 의존, global SQMH 예측 아님.
- **분포 (참고, AICc penalty 미적용)**: substantive 13% (4) + identity 9% (3) + inheritance 25% (8) + CONSISTENCY_CHECK 3% (1, Λ origin / §5.2 circularity) + PARTIAL 25% (8) + NOT_INHERITED 25% (8) + FRAMEWORK-FAIL 0 (S_8 OBS-FAIL 별개 카테고리, §6.1). 본 분포의 광고 인용 시 반드시 위 hidden-DOF 0% 정직 헤드라인 동반 표기.
- Full breakdown: §6.5(e) (single source of truth) + §6.1 22행 표 + `paper/verification_audit/` + `results/L495/HIDDEN_DOF_AUDIT.md` + `results/L502/HIDDEN_DOF_AICC.md` + `results/L503/UNIVERSALITY.md` + `results/L506/CASSINI_ROBUSTNESS.md`. (TL;DR / `claims_status.json` 동기화 의무)

**★ Phase 7–8 정직 후속 (L526–L537, *paper update v9 통합*)**:

- **Son+25 age-bias contingency (L526 R1–R8)**: 사전 등록 falsifier (DESI w_a, Λ origin, three-regime σ₀) 16건이 Son+2025 age-bias 보정 *수용* 시 hidden assumption 통해 status 변동 위험. paper §1.2.1 가속 우주는 *전제* 이며 Son+ branch 가 correct 일 경우 §5 cosmology 본문 격하 트리거 — *전제 caveat* §1.2.1 명시 (L526 R8 §4.1).
- **Path-α (axiom 3' Γ₀(t) 시간진화 / L527)**: 신규 a priori 채널 후보 1건 — *galactic-scale Γ₀ 시간 지문* (toy 7.52% 회복 추정, 단일 에이전트 추정으로 *낮은 신뢰도*). 8인 Rule-A 라운드 자유 도출 의무 (L537 R9-Exec-A 1순위 미실행). JCAP acceptance 중앙 ≈ 10–12% (Path-α + two-scale).
- **Path-γ (galactic-only repositioning / L528)**: SQT cosmology 본문 *영구 폐기* + A1/A4/A5 만 유지하는 갈락틱 격하 옵션. MNRAS 격하 재제출 시 acceptance 중앙 **20–30%** (단일 에이전트 추정, 8인 Rule-A 미실행). PRD Letter 진입 *영구 차단*.
- **Hybrid Path-α + Path-γ (L535)**: cosmology 약화 + galactic 강화 결합 acceptance 중앙 18–28% (22%). MNRAS (1순위) / ApJ (2순위) / JCAP (3순위) 분리 제출 옵션 (JCAP majority >50% 영구 미달).
- **Two-scale / GFT BEC / Causet meso compat (L529 / L530 / L533 / L534)**: a priori 신규 회복 0건. ψ^n 완전 회복은 Causet meso framework 와 구조적 *불가* (L534).
- **메타-진단 종결 (L537 Phase 8)**: L532–L536 audit 디스크 부재 — Phase 8 5-track 가설 verdict 5/5 N/A. Round 9 (R9-Disk-Audit 선결 + R9-Exec-A 8인 Rule-A) 권고 (CLAUDE.md "결과 왜곡 금지" 정합).
- 본 v9 통합은 **paper edit 0건 / 시뮬레이션 신규 0건 / claims_status.json edit 0건** (CLAUDE.md [최우선-1]/[최우선-2] 정합) 상태에서의 *방향 등재* 만 — 실제 §0/§1.2.1/§6.1 row 추가 본문 갱신은 본 §0 footnote + §1.2.1 caveat + §6.1.3 row 28–30 까지 적용 완료. claims_status.json v1.2 → v1.3 sync 는 Rule-B 후속 의무.

---

## 1. 1장 — 서론

### 1.1 일반인 한 단락

> "현대 우주론은 우주 에너지의 95%(암흑물질 + 암흑에너지)를 설명할 통합 모델이 없다. SQT 는 시공간 자체가 양자 단위로 존재하며, 물질이 이를 흡수하면 중력이 나타나고 빈 공간이 새 양자를 생성하면 우주 가속이 일어난다는 가설이다. 6 axiom 으로부터 암흑에너지 기원·MOND·은하단/은하 regime 차이 등 6개 우주론 난제를 단일 framework 로 다룬다."

### 1.2 6대 동기 난제

#### 1.2.1 암흑에너지 기원
관측: Λ ≈ 6.9 × 10⁻²⁷ kg/m³. 표준 모델: 측정값 (input). SQT: order-unity *dimensional consistency check* (CONSISTENCY_CHECK only — circularity 구조적, 진정 a priori 도출 아님; §5.2 / L412 PR P0-1 강등).

> **★ 가속 우주 *전제* caveat (L526 R1–R8 / L538 v9)**: 본 절 (그리고 §5 cosmology 본문 전체) 은 *late-time cosmic acceleration 의 관측적 정립* 을 입력 전제로 한다. Son+2025 (age-bias correction) 가 correct 일 경우 — *감속 우주 또는 약한 Λ* — §5 본문 cosmology claim 의 다수가 격하 또는 사망. SQT framework 자체는 axiom 3 의 Γ₀ 시간의존화 (Path-α, L527) 또는 cosmology 본문 폐기 (Path-γ, L528) 를 통해 부분 생존 가능하나, 본 §1.2.1 의 "Λ 가 SQT 흡수/생성 균형의 자연스러운 결과" narrative 는 Son+ branch 에서 무효. *전제 의존 사실*은 hidden assumption 이며, paper §6.1.2 / §6.1.3 audit 채널 외부에서 본 §1.2.1 caveat 으로 명시 (L526 R8 §4.1 / L538 sync).

#### 1.2.2 MOND a₀ 보편성
관측: a₀ = 1.2 × 10⁻¹⁰ m/s². MOND: 측정값 (1 free parameter). SQT: a₀ = c·H₀/(2π) 도출.

#### 1.2.3 S_8 tension (★ SQT 약점, 정직)
Planck CMB σ_8 ≈ 0.81, weak lensing σ_8 ≈ 0.78 — 3σ 차이. SQT 는 *해결 못함* (구조적 μ_eff≈1, +1.14% 악화).

#### 1.2.4 H₀ tension
CMB ≈ 67, local ≈ 73 km/s/Mpc. SQT: ~10% 부분 완화만.

#### 1.2.5 Bullet cluster MOND 실패
SQT 의 depletion zone 이 baryon (galaxies) 따라 → Bullet 관측 일관.

#### 1.2.6 은하단-은하 regime 충돌
MOND 가 galaxy rotation curve PASS 하나 cluster mass fail. SQT 의 environment-dependent σ₀ 가 자연 분리.

### 1.3 SQT 한 문장 정의

> "물질이 시공간 양자를 흡수 (중력 발현) 하고, 빈 공간이 새 양자를 생성 (우주 가속) 한다. 흡수 단면적 σ₀(환경) 는 cosmic / cluster / galactic 환경에 따라 비단조 변화한다."

### 1.4 선행 비교
MOND, MOG, TeVeS, EMG, EG, SymG f(Q), RVM, k-essence, Verlinde entropic.

### 1.5 논문 구조
2장 공리 / 3장 three-regime σ₀ / 4장 예측 / 5장 우주론 / 6장 정직 한계 / 7장 전망 / 부록 FAQ + 검증 코드.

---

## 2. 2장 — 공리와 도출 관계

### 2.1 6 공리

| ID | 진술 | 자연어 |
|----|------|--------|
| axiom 1 | 물질이 시공간 양자 흡수 | "중력 = 흡수 결과" |
| axiom 2 | 에너지 보존 | 표준 |
| axiom 3 | 빈 공간이 Γ₀ 균일 생성 | "우주 가속 = 생성 결과" |
| axiom 4 | 발현 metric (★ 미시 OPEN) | "공간이 양자에서 emerge" |
| axiom 5 | 물질이 depletion zone 안에 묶임 | "은하 = 흡수 영역" |
| axiom 6 | 선형 유지 | 안정 조건 |

### 2.2 5 도출 관계 + dependency graph

| ID | 도출 결과 | 의존 axiom | Sketch |
|----|----------|-----------|--------|
| derived 1 | Newton's G 회복 | a1 + a4 + **B1** | bilinear 흡수율 R = σ·n·ρ_m (B1 ansatz, 본 §2.2 직후 단락) → continuity 정상상태 → ∇²Φ ∝ ρ_m → 1/r² (★ B1 은 axiom 결론 아닌 *추가 함수형 ansatz*; L430 명시화) |
| derived 2 | n_∞ 정상상태 | a3 균형 | 생성 = 흡수 평형 (단, ρ_Λ_obs input — 5.2 circularity) |
| derived 3 | ε = ℏ/τ_q | a3 + a6 | 양자 에너지 = ℏ × 진동 주파수 |
| derived 4 | Λ = nε/c² → ρ_Λ | a1 + a3 + d2 + d3 | ★ CONSISTENCY_CHECK only (5.2 circularity 구조적; L412 PR P0-1 강등) |
| derived 5 | Milgrom a₀ = c·H₀/(2π) | a4 + a5 | disc azimuthal 1/(2π) projection |

#### 2.2.1 ★ B1 — Absorption-rate functional ansatz (bilinear mass-action) [L430 신설]

derived 1 (Newton's G 회복) 의 도출 사슬은 다음 *암묵 입력* 을 사용한다:

> **B1 (bilinear absorption ansatz)**:
> 시공간 양자의 흡수율 밀도는 양자 수밀도 n 과 물질 밀도 ρ_m 의
> *선형곱* 으로 주어진다 — R(x) = σ · n(x) · ρ_m(x).

**B1 의 정직 분류**:

- B1 은 axiom 1–6 어느 것의 *결론* 도 아니다. axiom 1 ("물질이 시공간 양자
  흡수") 은 흡수의 *존재* 를 진술하지 *함수형* 을 진술하지 않으며,
  차원 분석 (σ·n·ρ_m vs σ'·n²·ρ_m vs σ''·n·ρ_m^(1/2)·∇n …) 도 함수형
  유일성을 주지 않는다.
- 따라서 B1 은 *paper postulate (hidden until L430)* 로 분류한다. 본
  L430 으로 명시화 (paper postulate 등록).
- "PARTIAL #1 mass-action 함수형" (§6.5(e) 8 PARTIAL 표 row 1) 의
  단일 출처 (single source of truth).

**B1 의 도출 시도 — 미해결, future work** (results/L430/NEXT_STEP.md §(i)):

| 후보 경로 | 미시 축 | 상태 |
|-----------|---------|------|
| P1: SK 4-vertex IR-stable fixed point | 미시 축 #1 (SK) + #2 (Wetterich FRG) | 미실시 (Phase 5+ 우선순위) |
| P2: axiom 1 부언 (single-quantum leading-order) | axiom 표 minimal patch | NEXT_STEP 권고만 |
| P3: holographic counting | 미시 축 #3 | 보조 증거, primary 도출 불가 |
| P4: EFT matching at IR | hi_class branch | future work, paper 외부 |

**falsifiability**: B1 이 *틀렸다면* 흡수율은 다른 함수형 (예 R ∝ n²·ρ_m
이면 ∇²Φ ∝ ρ_m^(1+α) — 비선형 Poisson) 을 따르며, SPARC galactic-내부
회복 / 1/r² 한계 / Cassini PPN |γ−1| 가 함께 시그니처를 남긴다. Phase 5
EFT matching 이 비-bilinear 함수형을 선호하면 derived 1 은 ansatz-dependent
prediction 으로 *재분류* (PARTIAL → POSTDICTION 강등 위험).

**왜 PASS_STRONG 이 아직 유지 가능한가** (L409 N1 cross-ref):

> "σ₀ = 4πG·t_P 가 입력일 때조차, *유한 t_P* 에서 1/r² 회복은 B1 + RG
> running 의 **비자명 cancellation** 을 요구. t_P → 0 한계만이 trivial —
> 유한 t_P 에서 SPARC 회복은 prediction." (단, B1 자체의 microscopic 도출
> 은 future work — 이 caveat 를 §6.5(e) PARTIAL row 1 이 흡수.)

### 2.3 기초 검증 — 통과 항목

- **Causality test**: Schwinger-Keldysh retarded propagator G_R 의 상반평면 해석성 (PASS)
- **Lorentz-invariance test**: Wightman propagator KMS 조건 (PASS, machine zero 정밀도)
- **Vacuum-stability test**: V(n) 최솟값 + ghost-free kinetic term (PASS)

### 2.4 미시 4 축 (4 microscopic pillars)

| 축 | 정식 명칭 | 상태 |
|------|----------|------|
| 1 | Schwinger-Keldysh open-system formulation | KMS PASS |
| 2 | Wetterich functional renormalization | Wilson-Fisher 재현, β-function 계수 algebraic only (★★⅓) |
| 3 | Holographic dimensional bound | σ₀ = 4πG·t_P uniqueness |
| 4 | Z₂ spontaneous symmetry breaking | η ≲ 10 MeV 제약 |

#### 2.4.1 4-pillar convergence PARTIAL: axiom 4 OPEN 종속분 vs 독립 잔여분 (L431)
> 본 절의 4 축은 *나열* 이며, paper 단계에서 *상호 일관성 = 동일 micro Lagrangian 도출* 은
> 검증되지 않았다 — 따라서 §6.5(e) self-audit 에서 "4-pillar convergence" 는 PARTIAL 등급
> (PARTIAL 8/32 중 1건) 으로 분류된다. 이 PARTIAL 등급은 두 종류의 caveat 합산이며 본문에서
> *분리 추적* 한다:
>
> 1. **axiom 4 OPEN 종속분** — micro origin 부재 (§2.5 의 5번째 축 미결정, §6.1.1 row 11,
>    §6.1.2.1 의 NOT_INHERITED 5건 chained root). 5번째 축 결정 또는 Dual foundation 시나리오
>    (L427) 채택 시 *부분* close 가능. 단독 close 시 PARTIAL → PASS_BY_INHERITANCE 부분 격상
>    (footnote 수준), §2.4 절 자체 등급은 잔여 독립분으로 PARTIAL 유지.
> 2. **독립 잔여분** — 1-loop quadratic hierarchy (§2.6), conformal anomaly (§2.6),
>    Wetterich β-function 계수의 algebraic-only 한계 (§2.4 row 2, ★★⅓). axiom 4 close 와
>    무관하게 살아있는 future-work 항목.
>
> Dual foundation 시나리오 채택은 종속분 (4 축 공통 Lagrangian 채널, cross-channel 정합성
> 채널, NOT_INHERITED 연쇄 회복 채널) 의 *방향성* 부분 close 만 제공하며, 잔여 독립분은 별도
> future work. Dual cost vs single 5번째 축 cost 의 정량 비교는 별도 loop (L432+) 에서 다룬다.
> 본 절은 *분리 추적* 의 본문 진입점이며, paper 등급 표 (§6.5(e)) 의 PARTIAL 카운트 (8/32)
> 자체에는 변동이 없다 — 등급 *해석* 만 정직 분리한다. (출처: results/L431/{ATTACK_DESIGN,
> NEXT_STEP, REVIEW}.md)

### 2.5 ⚠ 5번째 축 후보 (axiom 4 OPEN) — Dual foundation 명시 등재 (L427)

**Causet meso (coarse-grained causal set) + GFT (Group Field Theory)** 두 후보 모두 본 framework 와 *조건부 호환* 으로 명시 등재한다 (L404 권고, L427 sync).

| 후보 | 조건부 PASS | axiom 4 (Z₂ SSB) 영향 | axiom 3 (σ₀=4πG·t_P) 영향 |
|------|------------|----------------------|--------------------------|
| Causet meso | 4/5 조건부 PASS (미달 1 조건 — dimensionality emergence 정량 검증 OPEN) | 보존 (Z₂ 단독) | 무관 |
| GFT | 조건부 호환 (NOT_INHERITED 회복 폭 우세, 단 *군 mismatch* 분기 OPEN) | **Z₂ vs U(1) 군 mismatch — 확장/축소/공존 3 분기** | **재도출 risk 비제로** |

본 paper 는 두 foundation 사이의 *우선순위 결정을 명시적으로 유보* 한다. Dual foundation 은 *foundational layer* 의 dual 이며 *cosmological observable* 의 derived prediction 자유도는 0 추가 — AICc 패널티 비대상. 5번째 axis 결정은 DESI DR3 unblinding timeline 과 *직교* 한 별도 *micro-decision register* 의 Trigger A–D (axiom 4 군 구조의 외부 QFT/holography 채널, σ₀ holographic 항등식의 별도 dimensional reduction 채널, NOT_INHERITED #20 의 외부 재현, 또는 trigger 미발생 시 양립 정책 영구 유지) 에 *데이터-독립* 으로 사전 등록한다 (§6.5(b) 참조).

★ 정직 (L427): Dual 등재 시 framework completeness 80% 상한 (§6.1.1 #10) 은 *영구* 한계로 격상 가능. JCAP "honest falsifiable phenomenology" 포지셔닝과 정합 — PRD Letter 진입 조건 (Q17 priori 도출 + Q13/Q14) 미달성 재확인. NOT_INHERITED 8 항목의 회복 도달 정량 경계는 §6.1.2 본문 (direct 3 + partial 3 + latent 2) 참조.

### 2.6 정직 caveat
- 미시 4 축의 *상호 일관성* (동일 Lagrangian 도출 가능성) 부분 — 본문 1단락 명시 필요. **L427 추가**: 5번째 축의 dual 본질은 4 축 Lagrangian 일관성 가정과 *직교* (foundational layer 분리) 또는 *완화* (joint consistency 약화) — 두 해석 모두 OPEN 으로 명시 유보.
- 1-loop quadratic hierarchy 살아있음
- Conformal anomaly 가 Λ_obs 대비 무시 가능

### 2.7 ★ 본문에 추가 필수: axiom-derivation dependency graph (Figure 0)
화살표 도식 — 6 axiom → 5 derived 화살표, 4 축은 5 derived 의 micro 보강.

---

## 3. 3장 — Three-regime σ₀(env) parameterization

### 3.1 세 regime 값
| 환경 | σ₀ (log) | 해석 |
|------|----------|------|
| Cosmic (우주 평균) | 8.37 | RG IR fixed point 부근 |
| Cluster (은하단) | 7.75 | Saddle FP — 비단조 dip |
| Galactic (은하) | 9.56 | RG UV fixed point 부근 |

### 3.2 RG 동기 (saddle FP topology)
cubic β(σ) = aσ - bσ² + cσ³ → 3 fixed point. cubic topology 96.8% 가 호환.
★ 정직: saddle 의 *위치* 자연성은 미입증 (band 내 uniform).

### 3.3 핵심 falsifiable test: monotonic 기각
단조 σ(ρ_env) 가 anchor 데이터에서 Δχ²=288 으로 기각 (regime-간 gap 에서). 1-DOF 근사 시 약 17σ 등가.

### 3.4 ⚠ 핵심 정직 caveat
> *"σ₀(env) 의 비단조성은 데이터 fit 에서 발견됨 (postdiction). 4 미시 축은 비단조성을 *허용* 할 뿐 a priori *예측* 하지 않음.*
> *SPARC galactic-내부 단조 모델 marginalized Δln Z = -1.84 (단조 약 선호).*
> *17σ 신호는 *regime-간* gap 에만 존재."*

★ **추가 정직 (L407, saddle 위치 priori-impossible)**: cubic-RG topology
호환률 96.8% 는 *허용 조건* 이며 saddle *위치* 자연성과는 분리되는 개념이다.
자유 cubic-RG scan 에서 saddle 이 관측 cluster band 에 떨어질 priori 확률은
1.4% (±0.10 dex 실험 정밀도 매칭률 0.5%), 표준 between-FPs 가정
(IR < saddle < UV) 하에서는 σ_cluster = 7.75 < σ_cosmic = 8.37 이 부등식을
위반하므로 P = 0 — **현재 RG truncation 안에서 saddle 위치의 priori 도출은
영구 불가**. 따라서 saddle 위치는 *외부 anchor* (cluster 관측 데이터) 만으로
결정되며, 이는 §3.5 의 anchor-circularity 및 mock injection FDR 100% 신호와
일관된다. 회복 경로는 비표준 RG (Wetterich Wilsonian truncation, holographic-RG,
1-loop EFT matching) 에 한정되며 §7 future work 핵심 우선순위로 분리. 본
caveat 는 PRD Letter 진입 조건 (Q17 priori 도출) 미달성을 재확인하며 JCAP
"정직한 falsifiable phenomenology" 포지셔닝과 정합.

### 3.5 Anchor caveat (overfitting 정직 정량)
- ΔAICc=99 — 단, anchor=fit point 인 by-construction 위험
- Mock injection (LCDM mock 200개): three-regime 모델의 false-detection rate 100%
- LOO (leave-one-out): 1-out 41–89, 2-out 임계, 3-out 0
- Endpoint dominance: cosmic+galactic 91% χ² 기여, cluster 9% only

### 3.6 Bayes factor (proper marginalized)
- Δln Z_marginalized = 0.8 only (이전 fixed-θ ~13 은 narrative 격하)
- BMA weight: three-regime 31% (R=5), three-regime + 2-regime 합산 64.8% *(주의: §0/Self-audit "31% PASS_STRONG" 과 *다른* 의미 — 이쪽은 BMA posterior weight, 5-model 비교)*
- 2-regime merge ΔAICc=+0.77 (3-regime 강제 데이터 ≪)
- ★ R=3/5/10 모두 보고 필수 (prior width sensitivity)

★ **추가 정직 (L405, R-grid prior-width sensitivity / Lindley fragility)** —
marginalized Bayes factor 는 prior width R 에 강하 의존 (Lindley 1957
paradox). R={2, 3, 5, 10} 4 점 모두 보고 (toy calibration, L405):

| R   | Δln Z (3R−LCDM, toy) | Δln Z (2R−LCDM, toy) | 비고 |
|-----|----------------------|-----------------------|------|
| 2   | +81.12 | +16.54 | monotonic Hess 특이 (nan) |
| 3   | +79.90 | +15.98 | OK |
| 5   | +78.37 | +15.09 | 본문 인용 baseline |
| 10  | +14.68 | +13.76 | **collapse — 5배 급락** |

- toy calibration (8 anchors, §3.5/§3.6 구조 calibrated) 에서 R=5 → R=10
  사이 3R Δln Z 가 ~5 배 감소. 동일 *상대 변화 패턴* 이 실 데이터에 적용
  된다면, 실 데이터 R=5 의 Δln Z = 0.8 은 R=10 에서 **음수로 떨어질
  가능성** 실재 — 결론 reversal 위험 (Lindley fragility).
- 본 R-grid 표 절대값은 *toy* 만 신뢰 가능. 실 데이터 production dynesty
  R={2, 3, 5, 10} 측정은 L406 production run (budget pending).
- L405 dynesty smoke 에서 Laplace 대비 +4.27 ln Z gap — 3-regime hard
  threshold 의 Laplace 신뢰 부족. method dependence 명기.
- BMA weight 31% 도 "at R=5" 한정. R 전 영역에서 stable 하지 않음.
- 본 §3.6 Δln Z = 0.8 은 Kass-Raftery 1995 기준 |Δln Z| < 1 = "barely
  worth mentioning" — *inconclusive* 결론을 referee 앞서 본문에 정직 인정.
  cross-link: §3.4 postdiction + saddle 위치 priori-impossible, §3.5 anchor
  circularity.

### 3.7 Cluster anchor 확장 (회복 경로)
- 다중 cluster joint (A1689+Coma+Perseus): single-source dominance 59.7% 해소
- 13-cluster archive pool (LoCuSS/CLASH/PSZ2) 가용

---

## 4. 4장 — 예측

### 4.1 검증 완료 (PASS) — ★ audit 결과 반영 (PASS 종류 분리)

> **Cross-reference**: 본 **12행** 표 (RAR row 12 추가, L512) 는 README "Claims status" 7+1행 summary 의 *full canonical 형태*. README rows 3 (Bullet), 4 (BBN), 5 (Solar-system 4종 = Cassini/GW170817/LLR/EP), 7 (CMB θ_*) 가 본 표 row 2,3–6,8,10 에 1:N 매핑. 한계 (OBS-FAIL/UNRESOLVED/NOT_INHERITED; framework-internal contradiction 은 §6.5(e) audit 에서 0건) 는 §6.1 25행 표 참조 (§6.1.1 14 + §6.1.2 8 + §6.1.3 3 audit overlay). **Enum 등급 master**: line 482 의 10-value canonical (`PASS_STRONG / PASS_IDENTITY / PASS_BY_INHERITANCE / CONSISTENCY_CHECK / PARTIAL / POSTDICTION / PENDING / NOT_INHERITED / OBS-FAIL / FRAMEWORK-FAIL`; legacy `PASS`, `PASS_TRIVIAL` deprecated). 본 표의 `PASS_TRIVIAL` 표기는 legacy alias — 신규 인용 시 `PASS_BY_INHERITANCE` 사용.

| 예측 | 데이터 | 결과 | 종류 |
|------|------|------|------|
| σ₀ regime 구조 | SPARC + cluster + cosmic | PASS aggregate | PASS_STRONG (postdiction caveat §3.4) |
| BBN ΔN_eff < 0.17 | Planck/light element | ΔN_eff ≈ 10⁻⁴⁶ | **PASS_STRONG** (η_Z₂≈10MeV ≫ T_BBN + β_eff² 두 보호) — *L502 caveat: hidden-DOF AICc (k_h=9) ΔAICc=+18 demotes to ≤PASS_MODERATE; §6.5(e) L513* |
| Cassini PPN \|γ−1\| < 2.3×10⁻⁵ | Cassini 2003 | \|γ−1\| ≈ 1.1×10⁻⁴⁰ | **PASS_STRONG** (★ β_eff = Λ_UV/M_Pl ≈ 7.4×10⁻²¹ 작음에서 옴; T_photon=0 단독 mechanism *아님*) — *L506 cross-form CHANNEL_DEPENDENT (universal coupling at β=0.107 → 4/4 FAIL); L502 hidden-DOF AICc demotes to ≤PASS_MODERATE* |
| GW170817 \|Δc/c\| < 10⁻¹⁵ | LIGO 2017 | 0 (구조적) | PASS_TRIVIAL (conformal-only Lagrangian 형태 선택의 귀결, disformal 부활 시 KILL) |
| LLR Ġ/G | LLR mm | 0 (axiom-defined) | PASS_TRIVIAL (G axiom 상수 동어반복) |
| EP \|η\| < 10⁻¹⁵ | MICROSCOPE | 0 (β_b=0) | PASS_STRONG (dark-only embedding 구조적) — *L502 hidden-DOF AICc (k_h=9) ΔAICc=+18 demotes to ≤PASS_MODERATE; §6.5(e) L513* |
| CMB primary peak | Planck | radiation era T^α_α≈0 | PASS |
| **CMB θ_*** | Planck | δr_d/r_d ≈ 0.7% (Planck σ × 23) | **PARTIAL** ★ matter era φ 진화로 shift; Phase-2 BAO 와 동일 채널 |
| Halo 형태 = baryon | Lensing | PASS | PASS_STRONG |
| Bullet cluster offset | Clowe 2006 | PASS, MOND fail | PASS_STRONG (qualitative) — L417 caveat: SQT 독자 정량 예측은 peak_lens ≡ peak_galaxies (정성). 관측 ~150 kpc lens-vs-gas magnitude 는 gas ram-pressure (입력) echo — depletion-zone formalism 만으로 독립 정량 도출 불가 (results/L417/) |
| **RAR a₀** | SPARC (M16) | a₀_RAR = 1.069×10⁻¹⁰ vs SQT 1.042×10⁻¹⁰ m/s² (2.5% 일치) | **PASS_MODERATE** — caveat (1) L491 cross-form spread 0.37 dex (median 0.023 dex 만 PASS); (2) L492 dwarf 0.46×10⁻¹⁰ cross-dataset 불안정; (3) L495 hidden DOF 3 (M16 fit + Υ★ + H₀ anchor); (4) L502 hidden-DOF AICc 적용 시 ΔAICc=+4.71 → MODERATE 강등; (5) L493 30% OOS retention + L494 0/1000 mock false-positive 로 real signal 확정 (results/L491–L495, L502) |

### 4.2 Dataset inventory (★ 본문 표 추가 필수)

| Dataset | N | Source | Version | Citation |
|---------|---|--------|---------|----------|
| SPARC | 175 (Q=1: 90) | Lelli 2016 | v2.3 | Lelli, McGaugh & Schombert 2016 |
| DESI BAO | 13 pts | DESI 2024 | DR2 | DESI Collab. 2024 |
| Planck CMB | compressed | Planck 2018 | TT,TE,EE+lowE | Planck Collab. 2018 |
| A1689 | 1 cluster | Limousin 2007 | — | Limousin et al. 2007 |
| Bullet cluster | — | Clowe 2006 | — | Clowe et al. 2006 |

### 4.3 근기 falsifier (3개, 2025–2030)

| 시설 | SQT 예측 | 결정 시기 |
|------|---------|----------|
| **DESI DR3 w_a** | 최소 모델: w_a=0; V(n,t)-확장: w_a~-0.3 (gate OPEN) | **2025–2026 ⭐** |
| PIXIE μ-distortion | 1.02e-8 (노이즈 대비 10σ, 전경 대비 2σ) | 2025–2030 |
| LSST σ_8 | 5σ falsifier — SQT 가 S_8 *악화* (+1.14%) | 2030+ |

### 4.4 DESI DR3 inconclusive band (★ 사전 정의)
- w_a < -0.5: SQT 최소 모델 OBS-FAIL (관측이 minimal model 을 falsify; framework-FAIL 아님 — V(n,t) 확장 경로 별도)
- -0.5 ≤ w_a ≤ -0.1: **inconclusive** (V(n,t) gate 결정 후 재판정)
- w_a > -0.1: SQT V(n,t)-확장 OBS-FAIL (관측이 extension 을 falsify; framework-FAIL 아님)

### 4.5 중기 falsifier (4개)
Euclid f·σ_8, CMB-S4 lensing, ET GW scalar mode, 21cm post-EDGES.

### 4.6 ★ S_8 악화 정직 인정 (영구 한계, pre-registered Euclid 4.4σ falsifier)
SQT 구조적 μ_eff≈1 → cosmic shear ξ_+(10') = LCDM 보다 +2.29% (= 2 × ΔS_8, ΔS_8 = +0.0114).

**Facility forecast (L406, `results/L406/forecast_facilities.json`)**:
- DES-Y3 (현재): 0.63σ — 미검출 정합.
- LSST-Y10 (~2032): 2.85σ — 보조 falsifier.
- **Euclid DR1 cosmic-shear 2pt (~2026–2027): 4.38σ 중심값** (paper 본문 round 4.4σ; prediction-uncertainty ±0.0008 quadrature 포함 시 4.19σ). 4.4σ 는 *중심 forecast* 이며, falsification floor 는 cosmology convention 3σ. Discovery-grade 5σ 주장 아님.

**Pre-registered two-sided decision rule** (Euclid DR1 ξ_+(10') 측정 m 의 ΛCDM 대비 초과율, L413 §D):
- +1.5% ~ +3.0%: SQT **CONSISTENT** (1σ band of prediction).
- +0.5% ~ +1.5%: ambiguous (Δχ² ~ 4, tension, not exclusion).
- −0.5% ~ +0.5%: SQT **excluded ~4σ** (LCDM-like).
- < −0.5%: SQT **excluded > 5σ** (anti-SQT).

**Pre-registration triple-timestamp**: arXiv submission ID + GitHub release tag `v-preDR1-2026.NN` + OSF DOI (Phase-7 admin, locked *before* Euclid DR1 cosmic-shear 2pt 공식 release).

**구조적 mitigation 불가**: SQT 허용 sector (Cassini |γ−1|<2.3×10⁻⁵ + GW170817 c_T=c) 안에서 모든 μ_eff 채널이 ≥ 1 (L406 §A 4-channel 열거). S_8 악화는 fixable bug 아니라 **structural prediction**. 검출 = SQT falsified, 도망 불가.

(Toy linear-bias forecast caveat: 4.4σ 중심값은 ξ_+ ∝ S_8² Gaussian likelihood 가정. Full hi_class + Euclid mock 3×2pt nuisance-marginalized likelihood 는 Phase-7 작업.)

### 4.7 사전 등록 (DESI DR3 minimal locked, V(n,t)-확장 gated)
OSF 사전 등록 + GitHub release tag (DESI DR3 발표 *전*) 약속.

### 4.8 22 예측 종합 표
9 PASS / 5 PARTIAL / 8 UNRESOLVED — 별첨 Table T3. *Falsifier 부분 통계는 §4.9 (L498 N_eff=4.44, 8.87σ ρ-corrected) 와 §6.1.3 row 24 가 canonical.*

### 4.9 ★ Falsifier independence — correlation-corrected statistics (L498)

The six pre-registered falsifiers (DESI DR3, Euclid, CMB-S4, ET, LSST, SKA-null) are **not** six independent tests. Cosmic-shear / BAO observable overlap collapses the effective channel count.

**Headline correction (L498, `results/L498/FALSIFIER_INDEPENDENCE.md`):**

- **6 pre-registered falsifiers (N_eff=4.44 after correlation correction; 8.87σ combined, ρ-corrected — *not* 11.25σ naive).**
- **Active 5 (drop SKA null): 9.95σ ρ-corrected (vs. 12.32σ naive).**
- Correlation correction costs ~2.4σ in headline combined Z. Naive multiplication of channel σ values is **prohibited**; cite ρ-corrected only.

**Correlated pairs (cosmic-shear / BAO bloc):**
- Euclid × LSST: **ρ = 0.80** (both WL + clusters at low z; essentially same physics, different sky/depth).
- DESI DR3 × Euclid: **ρ = 0.54** (shared BAO/RSD leverage at z<2).
- DESI × SKA: ρ = 0.32 (minor RSD overlap).

**3 load-bearing orthogonal channels:** **CMB-S4** (recombination physics), **ET** (GW scalar polarization), **SKA-null** (21cm; consistency null). These three alone deliver Z_comb = √(7.9² + 7.4² + 0²) ≈ 10.83σ at full independence and remain truly uncorrelated. They — *not* the cosmic-shear bloc — carry the structural falsification weight.

**N_eff estimators:** participation-ratio 4.44 (most conservative, adopted as headline), Li–Ji 5.00, Cheverud–Galwey 5.71, naive 6.00. The "6 independent 5σ-class falsifiers" wording is replaced everywhere by **"5 active + 1 null falsifier across N_eff ≈ 4.44 independent observable channels, 8.87σ ρ-corrected combined."** All Bonferroni / Holm tests at family α=0.05 still pass for the five active channels (LSST passes by ~2× margin only — if true Euclid×LSST ρ exceeds 0.80, LSST contributes nothing beyond Euclid).

(Cross-ref: §4.3 near-term + §4.5 mid-term canonical six; §6.1 row 14 cosmic-shear external; L406 facility forecasts; L485/L486/L487 SKA / CMB-S4 / ET pre-registrations.)

---

## 5. 5장 — 우주론 함의

### 5.1 T^μν_n explicit form
T^μν_n = (ρ_q+p_q)u^μu^ν + p_q g^μν, w_q = -1 (cosmic).

### 5.2 ★★ Λ 기원 — CONSISTENCY_CHECK (L412 PR P0-1 강등; 가장 중요한 정직 disclosure)

**Status (post-L412 PR P0-1)**: `CONSISTENCY_CHECK` *(이전 `PASS_STRONG` 에서 강등)*. claims_status table / abstract / TL;DR / verifier 광고 4 곳 동기화.

ρ_q/ρ_Λ(Planck) order-unity 일치 (수치적으로 1.0000 *exact* 로 떨어짐 — 그러나 이 *exact* 성은 단위 변환 항등식의 결과이지 prediction 이 아니다). **단**:
> *"이 일치는 *구조적으로* circular 이다. n_∞ 정상상태 도출 (derived 2) 에서 ρ_Λ_obs 가 axiom 3 균형식의 input 으로 들어가, derived 4 에서 다시 ρ_q = n_∞·ε/c² 로 곱해져 ρ_Λ_obs 가 그대로 재현된다. ε 자유도가 어떤 값을 갖더라도 1.0000 이 유지되므로 ρ_q/ρ_Λ = 1.0000 은 *항진명제* (Bayesian KL update = 0) 이며 Popper 의미의 falsifier 가 부재한다. 따라서 본 결과는 (a) Λ 의 *order-of-magnitude* (10⁻²⁷ kg/m³ 영역) 가 60-자릿수 vacuum catastrophe 가 아닌 위치에 떨어진다는 *차원 분석 정합성* 과 (b) axiom 3 균형식이 단위 변환과 모순되지 않음을 보일 뿐, Λ 값을 *a priori* 로 예측하는 것이 아니다. 진정 a priori 도출은 4 축 b, c 계수 first-principle 도출 (현재 ★★⅓) 후 가능."*

**L402 audit 결과 (2026-05-01)**: Hubble + Planck-scale dynamics + KMS 균형 단독으로 n_∞ 를 *독립* 도출하는 회피 path (Path-α) 시도 → 10⁶⁰ 자릿수 어긋남으로 실패. 현재 axiom 3 구조에서 circularity 회피 *불가능* 확정.

**Why down-graded (L412 NEXT_STEP Path-iii hybrid)**: 이전 "PASS_STRONG ρ_q/ρ_Λ = 1.0000 *exact*" 광고는 L402/L412 ATTACK_DESIGN 에서 8 공격선 (B1 광고-본문 위계 충돌, B2 self-aware circularity, B3 *exact* 표기 변호선 폐쇄, B5 TL;DR 첫 ✅ bullet 위치, B6 enum mismatch, B7 31% headline inflated counting, B8 verifier 명칭 *predict* 함의) 으로 referee 1번 desk-reject 사유였다. PR P0-1 강등 단일 행위로 7/8 공격선 무력화, 잔존 1 (B4: 구조적 circularity 회피 불가) 은 본 disclosure 로 정직 노출 — 무기화 → 정직성 자산으로 반전.

### 5.3 Bianchi 항등식
∇_μ T^μν_n = -Q (흡수 sink), Hubble 당 10.4%.
→ effective |w_a|~0.3. DESI DR2 w_a=-0.83 의 1/3 (factor 3 부족).

### 5.4 DESI w_a 정직
- 최소 SQT: w_a=0, 8σ tension
- V(n,t)-확장: w_a 부호 OK 하나 (w_0, w_a) box 동시 미충족, AICc 미달
- V(n,t)-확장 derivation gate OPEN

### 5.5 Cosmography PASS
q_0 = -0.55, j_0 = +1.0 (Λ-like).

### 5.6 BBN PASS, 재결합 무영향, neutrino 독립.

### 5.7 ★ SPARC 내부 vs *regime-간* 메커니즘 분리
SPARC galactic-내부에서 단조 약 선호. *Regime-간* gap 만이 비단조 evidence 제공.

---

## 6. 6장 — 정직 한계

### 6.1 한계 표 (14행 → 22행 → **25행** 확장)

본 절은 세 종류의 한계를 *명시적으로 분리*해서 제시한다: (i) paper 자체 framework 가 가진 본래 한계 14건 (§6.1.1), (ii) 32 claim 내부 audit 에서 *추가로 드러난* 미상속 항목 8건 (§6.1.2), (iii) **광고 카운트 / 독립성 / 정보기준 audit 항목 3건 (§6.1.3, L495/L498/L502 신설)**. GitHub 사용자 입장에서 이 세 set 는 출처와 성격이 다르므로 같은 표에 섞지 않는다.

> **Cross-reference**: 본 25행이 canonical 한계 source. README "Claims status" summary 의 행별 매핑 — row 1 (S_8) ↔ #1 + #14, "NOT_INHERITED" 종합 row ↔ #15–#22, "Three-regime POSTDICTION" ↔ #5–#7, "Λ origin caveat" ↔ #13 (**§6.1.1 row 13 은 Λ_UV definitional/RG 한계; Λ origin 자체의 status 는 §5.2 + claims_status.json 에서 `CONSISTENCY_CHECK` master**), "DESI w_a PENDING" ↔ #12, **"Hidden DOF / falsifier independence / AICc penalty audit overlay" ↔ #23–#25 (§6.1.3, L495/L498/L502)**. PASS 항목의 *상보* 표는 §4.1 (12행, RAR row 12 추가 L512). **Enum 등급 master**: line 482 의 10-value canonical.

#### 6.1.1 Paper framework limitations (14 entries)

These limitations arise within the paper's own framework (postulates 1–6, four foundations, three-regime σ₀). 즉, paper 가 *주장하는 범위 안에서* 자기-인식한 한계들이다.

| # | 한계 | 상태 | Future plan |
|---|------|------|-------------|
| 1 | σ_8 +1.14% 구조적 worsening | OBS-FAIL 영구 | disclose (관측 텐션 별도 카테고리; §0/TL;DR/§6.5(e) 와 정합) |
| 2 | H₀ ~10% 만 완화 | UNRESOLVED | disclose |
| 3 | n_s SQT 외부 (no prediction) | OPEN | Inflation 외부 |
| 4 | β-function 계수 b, c first-principle 미달 | OPEN | 축 2 future |
| 5 | Three-regime 강제성 약함 (anchor 4-5개 필요) | ACK | dSph + NS 추가 |
| 6 | Sloppy parameter d_eff≈1 | ACK | Cluster pool |
| 7 | Theory-prior anchor 부분만 (postdiction) | ACK 축 4 ★★⅓ | RG b/c future |
| 8 | Cluster single-source (variance reduction 59.7%) | RECOVERY | Pool 확장 |
| 9 | Subset-specific Bayes factor | ACK | 5-dataset MCMC |
| 10 | Micro completeness 80% 상한 | OPEN | axiom 4 5번째 축 |
| 11 | axiom 4 발현 metric 미시 OPEN | OPEN | Causet meso |
| 12 | DESI V(n,t)-확장 derivation gate | OPEN | Toy 미충족 |
| 13 | Λ_UV definitional, RG-유도 아님 | ACK | UV completion |
| 14 | Cosmic-shear 외부 채널 (**Euclid DR1 4.4σ pre-registered falsifier**) | OPEN (pre-registered) | Euclid DR1 cosmic-shear 2pt 2026–2027; 중심 4.38σ, 3σ floor; two-sided decision rule §4.6; LSST-Y10 2.85σ 보조; triple-timestamp arXiv + GitHub tag `v-preDR1-2026.NN` + OSF DOI (Phase-7 admin); cf. L406/L413 |

#### 6.1.2 Internal-audit findings: claims not inherited from earlier framework (8 entries) — Dual foundation 등재 후 회복 진행도 (L427)

These items emerged from a cold-blooded internal audit of 32 claims from earlier related framework. 이 8건은 §6.1.1 의 self-acknowledged 한계와는 성격이 다르며, audit (R1–R8 8인) 과정에서 *외부에서 들여올 수 없음*이 확인된 항목들이다. **L427 sync**: §2.5 의 Causet meso + GFT *dual foundation 명시 등재* 에 따라 8 항목의 회복 도달 가능성을 *정성 라벨* (direct / partial / latent) 로 분리 표기. 단, *paper §6.5(e) 의 32 claim 등급 분포 (PASS_STRONG / PASS_IDENTITY / ... / NOT_INHERITED) 자체는 변동 없음* — 본 표는 회복 *도달 가능성의 정성 매핑* 일 뿐 등급 자동 격상 아님.

| # | 한계 | 현재 상태 | 회복 채널 (Causet / GFT / Dual) | 회복 도달 정성 (L427) |
|---|------|----------|--------------------------------|---------------------|
| **15** | **특이점 해소 (Planck 밀도 포화) 미상속** | NOT_INHERITED | Causet (direct) + GFT (partial) | **direct** — discreteness postulate via Causet, BEC saturation via GFT |
| **16** | **Volovik 2-fluid analogue 미상속** | NOT_INHERITED | GFT (partial) | partial — BEC 동형 채널 |
| **17** | **Jacobson δQ=TdS 미상속** | NOT_INHERITED | Causet (partial) | partial — *어느 branch 도 단독 회복 불가, §6.5(e) footnote 분리* |
| **18** | **GFT BEC 해밀토니안 미상속** | NOT_INHERITED | GFT (direct) | **direct** — GFT branch 등재 시 |
| **19** | **BEC nonlocality 메커니즘 미상속** | NOT_INHERITED | GFT (direct) | **direct** — *단 관측 채널 분리 (galactic σ profile / cluster lensing residual) OPEN* |
| **20** | **DESI ξ_q joint fit (Δχ²=−4.83) 결과 인용 불가** | NOT_INHERITED | GFT (latent) | **latent — paper 본문 회복 주장 금지**, 외부 재현 trigger B 필요 |
| **21** | **3자 정합성 (BBN/CMB/late DE) 미상속** | NOT_INHERITED | GFT (latent, #20 의존) | **latent — paper 본문 회복 주장 금지**, #20 의존 |
| **22** | **5 program 구조적 동형 (Padmanabhan/Volovik/Causet/Jacobson/GFT) 부분만** | NOT_INHERITED | Causet (partial 1/5) + GFT (partial 1/5) | partial 2/5 — Padmanabhan/Volovik/Jacobson 3 잔존 |

**산수 검증 (L427)**: direct 3 (#15, #18, #19) + partial 3 (#16, #17, #22) + latent 2 (#20, #21) = **8** ✓

##### 6.1.2.1 NOT_INHERITED 8 항목의 *연쇄 root cause* + Dual 등재 후 회복 정량 (L427 sync)

기존 진단: 8 항목 중 5건 (#16, #18, #19, #20, #21) 이 GFT/BEC 미채택의 연쇄 결과. axiom 4 의 5번째 축 (Causet vs GFT) 결정이 critical decision point.

**L427 갱신** (§2.5 dual foundation 명시 등재 후):
- *Causet meso 단독 등재 시*: 1–2 항목 (#15, #17 부분) 회복 — axiom 4 (Z₂ SSB) 보존, σ₀ holographic 항등식 영향 없음.
- *GFT 단독 등재 시*: 5 항목 (#15 부분, #16, #18, #19, #22 부분) 회복 — axiom 4 군 mismatch (Z₂ vs U(1)) cost 동반, σ₀ holographic 항등식 재도출 risk 비제로.
- *Dual coexistence (본 paper 정책)*: NOT_INHERITED 8 항목 중 **direct 3 + partial 3 = 부분 이상 진행 6 / latent 2 잔존** 의 정성 경계. #20 (DESI ξ_q joint fit) + #21 (3자 정합성) 은 *paper 본문에서 회복 주장 금지* — 외부 재현 trigger B (NOT_INHERITED #20 의 다른 그룹 재현 + r_d shift 동반 보고) 필요. #17 (Jacobson δQ=TdS) 은 어느 단일 branch 도 단독 회복 불가 — *§6.5(e) self-audit footnote 에 별도 분리 명시*.

★ 정직 (L427): Dual 등재의 NOT_INHERITED 회복은 *paper-internal* inheritance 진행이며, 외부 관측 채널 활성화 (특히 #19 BEC nonlocality 의 galactic / cluster signature) 는 *별도 falsifier 등재* 가 필요한 OPEN 항목. 본 표의 direct/partial/latent 는 *결정* 이 아닌 *정성 가능성 매핑* 으로, paper §6.5(e) 의 NOT_INHERITED 8/32 카운트는 *DR3 unblinding + micro-decision register Trigger A–D 발생 전까지 변동 없음*.

#### 6.1.3 Advertised-count / independence / information-criterion audit (3 entries, L495 / L498 / L502)

These three rows surface *meta-audit* findings about how PASS_STRONG counts and falsifier σ values are advertised. They are not framework-internal limitations (§6.1.1) nor missing inheritances (§6.1.2); they are honest accounting corrections that *must accompany* any cited PASS_STRONG count or combined falsifier σ.

| # | 한계 | 상태 | Cross-ref |
|---|------|------|-----------|
| **23** | **Hidden DOF count = 9 (보수) ~ 13 (확장)**: paper 광고 "0 free background parameters beyond ΛCDM" 는 부정확. 함수형 (M16) +1, anchor pick (cosmic/cluster/galactic) +3, Υ★ convention +1, B1 bilinear ansatz +1, three-regime carrier+saddle +2, axiom-scale stipulation +1 = **9 hidden DOF (보수)**. abstract/intro/appendix 8 drift 위치 식별, L515 차단 적용. | ACK (drift-guarded) | `results/L495/HIDDEN_DOF_AUDIT.md`; §0/§6.5(e); L515 |
| **24** | **Falsifier independence**: 6 pre-registered falsifier 의 N_eff = **4.44** (participation-ratio, headline) — *not* 6. Combined Z = **8.87σ (ρ-corrected, all six)** / **9.95σ (active 5)** — naive 11.25σ / 12.32σ 는 단독 인용 금지. 3 load-bearing orthogonal channels = CMB-S4 / ET / SKA-null (Z_comb ≈ 10.83σ). Correlated pairs: Euclid×LSST = 0.80, DESI×Euclid = 0.54, DESI×SKA = 0.32. | ACK (correction adopted) | `results/L498/FALSIFIER_INDEPENDENCE.md`; §4.9; L514 |
| **25** | **Hidden-DOF AICc penalty**: row 23 의 k_hidden = 9 보수 풀카운트를 AICc capacity penalty 에 강제 차감 시 **PASS_STRONG (substantive) 4건 (Newton / BBN ΔN_eff / Cassini \|γ−1\| / EP \|η\|<10⁻¹⁵) 전부 ΔAICc ≥ +18 → ≤PASS_MODERATE 강등**. applicable-only (k_h_app) 차감에서도 Newton +4 즉시 강등, BBN/Cassini/EP +2 RETAINED 경계. **광고 substantive 13% 도 hidden-DOF 정직 잣대 하 PASS_STRONG = 0%**. | ACK (headline 0%) | `results/L502/HIDDEN_DOF_AICC.md`; §6.5(e) L513-bullet; L513 |
| **26** | **Son+25 age-bias contingency (16건 hidden-assumption 의존)**: L526 R1–R8 8인 audit 결과 — 사전등록 falsifier 16건 (DESI w_a, three-regime σ₀ anchor, Λ origin, RAR row 12 일부, ISW dark cross 등) 이 Son+2025 age-bias correction *수용* 시 status 변동 위험. paper §1.2.1 가속 우주는 *전제 입력* 이며 Son+ correct branch 에서 §5 cosmology 본문 격하/사망 트리거 발생. *paper-internal* 한계 아님 — *외부 데이터 channel 의존 contingency*. | ACK (caveat 명시 §1.2.1) | `results/L526_R1`–`L526_R8/`; §1.2.1 caveat; L526 R8 §4.1; L538 |
| **27** | **a₀(z) priori 채널 가능성 (Path-α / L527)**: axiom 3 → axiom 3' (Γ₀(t) 시간의존) 형식 수정 시 *galactic-scale a₀(z) 시간 지문* 이 신규 falsifiable a priori 채널 후보로 등장. toy 회복 추정 7.52% (단일 에이전트, *낮은 신뢰도*). 8인 Rule-A 자유 도출 미실행 — 본 row 는 *방향 등재* 만, 실제 채택은 Round 9 (R9-Exec-A) 의무. | OPEN (Round 9 의무) | `results/L527/PATH_ALPHA.md`; L538 §0 footnote |
| **28** | **메타-진단 종결 (L537 Phase 8 부재)**: L532–L536 audit 디스크 산출 0건 (L532 디렉터리 부재, L533–L536 빈 디렉터리). Phase 8 5-track 가설 verdict 5/5 N/A. 메타-진단 한계효용 0 도달 (L531 §6.1 결론 유지). Round 9 (R9-Disk-Audit 선결 + R9-Exec-A 1순위) 권고. *결과 왜곡 금지* 정합 — 디스크 부재 정직 보고. Path-γ MNRAS 격하 재제출 옵션 (acceptance 중앙 20–30%, L528) / Hybrid α+γ (18–28%, L535) 동시 등재; PRD Letter / JCAP majority 영구 차단. | ACK (Round 9 의무) | `results/L528/PATH_GAMMA.md`; `results/L535/HYBRID_AG.md`; `results/L537/PHASE8_SYNTHESIS.md`; L538 |

**산수 검증 (3-section total, L538)**: §6.1.1 14 + §6.1.2 8 + §6.1.3 6 (3 기존 + 3 신규 row 26–28) = **28** ✓. 22-row legacy reference (§6.1.1 + §6.1.2) 는 보존 — 외부 도구가 22-count 가정 시 §6.1.1+2 만 인용하고 §6.1.3 는 "audit overlay" 로 별도 표기. 25-row legacy (L523) → 28-row (L538) trajectory 는 §6.1.3 footnote 만 누적.

### 6.2 비단조 σ₀(z) 는 *postdiction*, prediction 아님
> "비단조성은 데이터 fit 에서 발견되었고, 4 미시 축에서 a priori 도출되지 않음. 축들은 비단조성을 허용할 뿐 강제하지 않음."

### 6.3 Mock injection 100% false-detection caveat
LCDM mock 200개 중 100% 에서 three-regime 모델이 universal 모델 대비 ΔAICc>10 (false-positive). Anchor-driven 자유도 우위 정량 disclose.

### 6.4 Marginalized Δln Z = 0.8 — narrative 격하
이전 fixed-θ "Akaike weight 100%" 주장 폐기. Proper marginalized evidence 가 baseline.

### 6.5 ★ Methodological caveats
- **(a) Λ origin circularity**: 5.2 절 명시.
- **(b) Iterative model refinement**: 본 framework 는 다단계 반복 수정 거침. p-hacking 방지를 위해 (i) 모든 negative result 보존 (Sec 6.1), (ii) DESI DR3 사전 등록 (4.7), (iii) all-data + leave-out 양방 보고.
- **(c) Internal-naming origin**: "three-regime" parameterization 명칭은 데이터 fit 발견 후 명명 (post-hoc). axiom 1-6 + derived 1-5 는 framework 정립 시 priori.
- **(d) Tool support**: 일부 시뮬레이션과 문헌 정리에 AI 도구 보조. 모든 이론 결정과 정직 audit 은 인간 저자 수행.
- **(e) Self-audit (32 claim) — *L409–L415 통합 정직 reframing (★ single source of truth)***: 8인팀 cold-blooded audit 으로 root framework 의 32 검증 claim 을 paper framework 로 재검증. **Raw 광고 (post-L412 28% / pre-L412 31% PASS_STRONG) 와 substantive 카운트 (13%) 를 양쪽 동시 보고** — raw 단독 광고는 σ₀=4πG·t_P 항등식 따름결과 + inheritance/consistency subset 을 inflated counting 한 것이므로 폐기. *본 §6.5(e) 가 §0 abstract / TL;DR / `claims_status.json` 의 single source of truth — 다른 위치는 모두 본 단락 참조 (L414 ATTACK A4 cross-ref drift 차단).*
  - **PASS_STRONG (raw)**: pre-L412 = 10/32 (31%); post-L412 (Λ origin → CONSISTENCY_CHECK) = 9/32 (28%) — *광고용 raw 카운트*
  - **PASS_STRONG (substantive)**: 4/32 (13%) — Newton 회복, BBN ΔN_eff, Cassini β_eff, EP η=0. σ₀ 항등식 *외* 추가 axiom 입력 (mass-action, η_Z₂ scale, Λ_UV/M_Pl, dark-only embedding) 필요. **이 4건이 진짜 falsifiable prediction.**
  - **PASS_IDENTITY (σ₀=4πG·t_P 산술 따름결과)**: 3/32 (9%) — n₀μ=ρ_Planck/(4π), ξ scaling, Λ-theorem 차원. 차원 분석으로 자동 도출, 자유도 0. *항등식 자체가 무효화되면 cascade 무효.* (L412 신설 enum)
  - **PASS_CONSISTENCY_CHECK**: 1/32 (3%) — Λ origin (ρ_q/ρ_Λ = 1.0000). n_∞ derivation 이 ρ_Λ_obs 를 input 으로 사용 (§5.2 circularity), substantive prediction 도 pure identity 도 inheritance 도 아닌 *dimensional/order-of-magnitude consistency check*. (L412 down-grade: pre-L412 PASS_STRONG raw 카운트에서 분리되어 raw 31% → 28%로 변동.)
  - **PASS_BY_INHERITANCE**: 8/32 (25%) — 기존 PASS_TRIVIAL 2 (GW170817 Lagrangian-form, LLR 공리 tautology) + INHERITANCE 4 + L409 재분류 2 (BH entropy S=A/(4ℓ_P²), Bekenstein bound — Bekenstein-Hawking 1973 prior knowledge). v=g·t_P 는 PARTIAL 로 분류 (axiom 4 causet meso 결합 필요).
  - **PARTIAL**: 8/32 (25%) — caveat 명시 (mass-action 함수형 → §2.2.1 **B1 (bilinear absorption ansatz)** single source of truth, L430; CMB θ_* shift, Q-param 정의 비유일 등)
  - **NOT_INHERITED**: 8/32 (25%) — paper framework 외부 (특히 GFT/BEC 연쇄 5건). §6.1 한계 표 #15–#22 참조
  - 🚫 **FRAMEWORK-FAIL**: **0** (paper framework 자체 내부 logical/mathematical 무모순). *주의*: 이 "0" 은 framework-internal 모순 0건을 의미하며, S_8 OBS-FAIL (관측-vs-이론 tension) 과는 별개 카테고리. README §Claims-status 의 ❌ 표기는 OBS-FAIL, 본 §6.5(e) 의 "FAIL 0" 은 FRAMEWORK-FAIL 을 가리킴 — 동일 단어 두 의미 혼동 금지.
  - **카운트 검증 (산수 무모순, L414 ATTACK A2)**: 4 substantive + 3 identity + 1 consistency-check + 8 inheritance + 8 PARTIAL + 8 NOT_INHERITED + 0 framework-FAIL = **32** ✓
  - **헤드라인 (정직 양면 표기, L415 sync)**: "**raw 28% PASS_STRONG (post-L412, 9/32; pre-L412 31% / 10/32) / 13% substantive (4건) + 9% σ₀ 산술 항등식 (3건) + 3% CONSISTENCY_CHECK (Λ origin)**". README TL;DR / abstract / claims_status.json / final summary 동기화 완료 (L415). raw 28%/31% 단독 인용 금지 (L409 ATTACK_DESIGN A1·A4·A7 reviewer 공격 회피).
  - **★ L513 headline 격하 (hidden DOF AICc penalty, L502 통합)**: L502 (`results/L502/HIDDEN_DOF_AICC.md`) 가 L495 hidden DOF 카운트 (보수 k_hidden = 9: 함수형 +1, anchor +3, Υ★ +1, B1 ansatz +1, three-regime 구조 +2, axiom-scale stipulation +1) 를 AICc capacity penalty 에 강제 차감한 결과, **PASS_STRONG (substantive) 4건 (Newton 회복 / BBN ΔN_eff / Cassini |γ−1| / EP |η|<10⁻¹⁵) 전부 ΔAICc ≥ +18 로 PASS_MODERATE 이하 강등**. applicable-only (k_h_app) 부분 차감에서도 Newton 은 ΔAICc=+4 로 즉시 강등, BBN/Cassini/EP 는 +2 의 "RETAINED 경계" — 보수 풀카운트에서는 전원 탈락. **즉 "substantive 13% (4/32)" 추정도 hidden DOF 차감 시 *0%* (PASS_STRONG 후보 0건 유지)**. 본 격하는 raw 28%/31% 광고뿐 아니라 substantive 13% 자체를 *AICc 정직 잣대 하에서 0% 로 환원* 시키며, 본 paper 의 PASS_STRONG 카테고리 단독 인용은 (raw / substantive 어느 쪽이든) AICc penalty 미적용 가정 하에서만 성립함을 명시. 상세 표·후보별 ΔAICc 는 `results/L502/HIDDEN_DOF_AICC.md` 표 §2 + `results/L513/REVIEW.md` 참조.
- **(f) "5/5 자동 통과" over-claim 격하**: 관측 5개 중 2 PASS_STRONG (Cassini β_eff, BBN 두 보호) + 2 PASS_TRIVIAL (GW170817, LLR) + 1 PARTIAL (CMB θ_* shift). 이전 "5/5 자동" narrative 폐기.

---

## 7. 7장 — 전망

### 7.1 DR3 timeline (즉시)
DESI DR3 release 2025–2026 → w_a unblinding 결정적 (KL ranking #1).

### 7.2 중기 facility map
PIXIE / LSST / Einstein Telescope / SKA (2025–2030+).

### 7.3 이론 우선순위
1. RG b, c 계수 full derivation (축 2 ★★⅓ → ★★★)
2. V(n,t) derivation (DESI 확장 모델 gate)
3. axiom 4 5번째 축 (Causet meso)
4. 5-dataset full joint MCMC

### 7.4 코드/데이터 공개
GitHub repository (영문 README master + 한국어 mirror) + Zenodo DOI + OSF 사전 등록.
DOI 발급 후 README/CITATION.cff 에 DOI 추가 commit.

---

## 8. 8장 — FAQ (★ 부록 1, 일반 독자 대상)

### Tier 1: 한 문장 답

**Q1. SQT 가 뭔가요?** → 공간을 셀 수 있는 단위로 보고, 흡수와 생성으로 중력과 우주 가속을 동시에 설명하는 가설.
**Q2. 검증되었나요?** → 4건 통과 (Λ 양 정확 일치, MOND 가속도, Bullet cluster, BBN). 단, S_8 1% 악화 정직 인정.
**Q3. 결정적 검증은?** → DESI DR3 (2025–2026) 의 w_a 측정.
**Q4. 신뢰할 수 있나요?** → 모든 코드/데이터 GitHub 공개, 22행 한계 표 본문 명시. 누구나 5초 Python 또는 30분 LLM prompt 로 재현 가능.

### Tier 2: 한 단락 답

#### Q5. 다른 이론과 뭐가 다른가요?
대부분의 modified gravity (MOND, TeVeS) 는 중력 법칙을 *수정*. SQT 는 시공간 *동역학* — 흡수/생성으로 중력과 Λ 가 *동일 axiom* 에서 도출. 이는 6 axiom 의 통합성에서 옴.

#### Q6. 약점은?
3가지 정직 인정: (a) S_8 tension 을 *오히려 악화* (1.14%, 구조적), (b) 비단조 환경 의존성은 데이터 fit 에서 발견 (postdiction, priori 예측 아님), (c) RG 계수 b, c 가 first-principle 도출 안 됨 (anchor-fit).

#### Q7. 일상에 영향이 있나요?
직접 영향 없음. SQT 는 우주 규모 (cluster ~10⁶ ly, cosmic ~10¹⁰ ly) 에서만 측정 가능. 일상 중력은 표준 Newton/Einstein 과 구분 불가.

#### Q8. 만약 맞다면?
Λ 의 기원이 처음으로 axiom 에서 도출됨 — 표준 모델의 가장 큰 미스터리 (cosmological constant problem) 부분 해결. MOND-like 현상이 시공간 동역학에서 emerge 함이 입증.

#### Q9. 만약 틀렸다면?
정직 framework 자체가 가치 — 22행 한계 표 + mock injection caveat = 어떤 식으로 틀릴 수 있는지 정량화. fit-driven 결론 다루는 case study.

### Tier 3: 학생/심화 답

#### Q10. axiom 4 (emergent metric) 의 미시 origin 이 OPEN 이라는 게 뭔가요?
공간 자체가 양자에서 emerge 한다는 axiom 은 거시 수준에서는 일반상대성과 일치하나, 미시 양자중력 (loop quantum gravity, causal set, tensor network) 중 어느 것이 정확한 underlying mechanism 인지 미정. Causet meso (coarse-grained causal set) 가 4/5 조건부 후보.

#### Q11. ρ_q/ρ_Λ = 1.0000 이 정확이라면 왜 circularity caveat?
n_∞ 정상상태 도출 시 ρ_Λ_obs 가 input. 따라서 (a) 차원 분석으로 ρ_Λ scale 재현 + (b) order-of-magnitude 자연 일치는 입증되나, ρ_Λ 절대값을 priori 예측은 아님. 5.2 절 명시.

#### Q12. 어떻게 도울 수 있나요?
GitHub issue/PR 로 결과 검증. 부록 9장 5개 Python script 직접 실행. DESI DR3 (2025-2026) 발표 시 SQT 예측 vs 실측 비교.

---

## 9. 9장 — 검증 코드 (★ 부록 2, 누구나 재현)

### 9.1 검증 철학
> "본 paper 의 모든 핵심 claim 은 *재현 가능* 해야 한다. AI 도구 (LLM prompt) 와 직접 실행 Python script 두 채널 모두 제공."

### 9.2 LLM prompt 5개

#### Prompt 1: Λ 기원 검증 (circularity 포함)
```
SQT 의 derived 4 (rho_q = n*epsilon/c^2) 를 검증하라.
H_0 = 73 km/s/Mpc, tau_q = 1/(3 H_0) 가정. n_inf 도출 과정에서
rho_Lambda_obs 가 input 으로 사용되는 *circularity* 를 명시 보고.
정직: rho_q/rho_Lambda = 1.0000 확인 후, "이는 차원 분석 일치이지
priori 예측이 아님" 을 명시.
```

#### Prompt 2: MOND a₀ 검증
```
SQT derived 5: a_0 = c*H_0/(2*pi) 도출. 1/(2*pi) 의 기하학적 기원
(disc azimuthal projection) 확인. a_0 관측값 1.2e-10 m/s² 와 sigma 비교.
```

#### Prompt 3: Monotonic 기각 검증
```
3 anchor (cosmic log_sigma=8.37, cluster 7.75, galactic 9.56) 데이터에
monotonic linear fit vs V-shape fit 적용. Delta chi^2 보고.
정직: 17 sigma 가 regime-간 gap 에만 나타나는지, SPARC 내부에서도
나타나는지 분리 보고.
```

#### Prompt 4: Mock injection false-detection
```
LCDM mock SPARC-like 200 realisations (log_a_0 = -10 ± 0.1 universal).
각 mock 에 three-regime fit 과 universal fit 적용.
three-regime 가 ΔAICc>10 으로 universal 을 이기는 false-detection rate 측정.
정직: 결과가 100% 면 "anchor 자유도가 LCDM mock 에 우위를 만듦" 정량.
```

#### Prompt 5: Cosmic shear S_8 worsening
```
SQT 의 +1.14% S_8 shift 가 xi_+(10') 에서 +2.29% (= 2 × ΔS_8) 로
나타남을 검증. Euclid n(z), LSST Y10 n(z) 두 case.
정직: SQT 가 LCDM 보다 *더 높은* xi_+ 예측 = SQT 검출 = SQT falsified.
```

### 9.3 ★ Python 검증 코드 (5개 stand-alone)

#### Script 1: `verify_lambda_origin.py`
```python
"""SQT derived 4: rho_q = n*eps/c^2 vs rho_Lambda(Planck), circularity 명시."""
import numpy as np

c = 2.998e8
G = 6.674e-11
hbar = 1.055e-34
H0 = 73e3 / 3.086e22

tau_q = 1 / (3 * H0)
eps = hbar / tau_q
rho_crit = 3 * H0**2 / (8 * np.pi * G)
rho_Lambda_obs = 0.685 * rho_crit  # ★ INPUT (circularity origin)
n_inf = rho_Lambda_obs * c**2 / eps  # ★ derived from observation

rho_q = n_inf * eps / c**2
print(f"rho_q              = {rho_q:.6e}")
print(f"rho_Lambda (Planck) = {rho_Lambda_obs:.6e}")
print(f"ratio              = {rho_q / rho_Lambda_obs:.6f}")
print(f"NOTE: This is DIMENSIONAL CONSISTENCY, not a priori prediction.")
print(f"      n_inf is derived FROM rho_Lambda_obs (axiom 3 balance).")
```

#### Script 2: `verify_milgrom_a0.py`
```python
"""SQT derived 5: a_0 = c*H_0 / (2*pi)."""
import numpy as np

c = 2.998e8
H0 = 73e3 / 3.086e22

a0_SQT = c * H0 / (2 * np.pi)
a0_obs = 1.2e-10
a0_err = 0.1e-10

dev = abs(a0_SQT - a0_obs) / a0_err
print(f"a_0 (SQT)   = {a0_SQT:.3e} m/s^2")
print(f"a_0 (obs)   = {a0_obs:.3e} +/- {a0_err:.0e}")
print(f"deviation   = {dev:.2f} sigma")
print("PASS" if dev < 2 else "FAIL")
```

#### Script 3: `verify_monotonic_rejection.py`
```python
"""anchor: monotonic vs V-shape chi^2."""
import numpy as np
from scipy.optimize import minimize_scalar, minimize

anchors = np.array([
    [-30,  8.37, 0.05],
    [-26,  7.75, 0.20],
    [-22,  9.56, 0.05],
])
x, y, err = anchors.T

def chi2_mono(slope):
    intercept = np.mean(y - slope * x)
    return np.sum(((y - (slope*x + intercept)) / err)**2)
r1 = minimize_scalar(chi2_mono, bounds=(-2, 2), method='bounded')

def chi2_V(p):
    sL, sR, vy = p
    pred = np.where(x < -26, sL*(x+26) + vy, sR*(x+26) + vy)
    return np.sum(((y - pred) / err)**2)
r2 = minimize(chi2_V, x0=[-0.2, 0.5, 7.75], method='Nelder-Mead')

dchi2 = r1.fun - r2.fun
print(f"chi^2 (monotonic) = {r1.fun:.2f}")
print(f"chi^2 (V-shape)   = {r2.fun:.2f}")
print(f"Delta chi^2       = {dchi2:.2f} (~{np.sqrt(dchi2):.1f} sigma, 1-DOF approx)")
print(f"NOTE: only at REGIME-GAP scale. SPARC galactic-internal shows opposite.")
```

#### Script 4: `verify_mock_false_detection.py`
```python
"""LCDM mock 200 -> three-regime false-detection rate."""
import numpy as np

rng = np.random.default_rng(42)
N_MOCK, N_GAL, ERR, sigma_truth = 200, 175, 0.10, 9.0

false = 0
for _ in range(N_MOCK):
    obs = rng.normal(sigma_truth, ERR, N_GAL)
    chi2_uni = np.sum(((obs - obs.mean()) / ERR)**2)
    s = np.sort(obs); t = N_GAL // 3
    g1, g2, g3 = s[:t], s[t:2*t], s[2*t:]
    chi2_3R = sum(np.sum(((g - g.mean()) / ERR)**2) for g in [g1, g2, g3])
    aicc_uni = chi2_uni + 2*1 + 4/(N_GAL-2)
    aicc_3R  = chi2_3R  + 2*3 + 24/(N_GAL-4)
    if (aicc_uni - aicc_3R) > 10:
        false += 1

rate = false / N_MOCK
print(f"three-regime false-detection rate on LCDM mock: {rate:.1%}")
print("CAVEAT: high rate => anchor-driven advantage on null data.")
```

#### Script 5: `verify_cosmic_shear.py`
```python
"""SQT +1.14% S_8 -> xi_+(10') +2.29% (toy)."""
import numpy as np

S8_LCDM = 0.832
shift_S8 = 0.0114
S8_SQT = S8_LCDM * (1 + shift_S8)

xi_LCDM = S8_LCDM**2
xi_SQT = S8_SQT**2
shift_xi = (xi_SQT - xi_LCDM) / xi_LCDM

print(f"S_8 LCDM    = {S8_LCDM:.4f}")
print(f"S_8 SQT     = {S8_SQT:.4f} (+{shift_S8*100:.2f}%)")
print(f"xi_+ shift  = +{shift_xi*100:.2f}%")
print("Detection by Euclid/LSST = SQT FALSIFIED (structural).")
```

### 9.4 재현성 체크리스트

#### 환경
- [ ] Python 3.10+, numpy 2.x (np.trapezoid), scipy 1.10+
- [ ] (선택) emcee 3.x, dynesty 2.x — full MCMC 검증
- [ ] Linux/macOS/Windows 동작
- [ ] Docker image / conda env file 제공

#### 실행
- [ ] 5 script 모두 stand-alone (각 < 5초, mock < 1분)
- [ ] LLM prompt 30분 내 응답
- [ ] 결과 본 paper 와 ±5% 일관
- [ ] 차이 발생 시 GitHub issue

#### 환경 통일
- [ ] `OMP_NUM_THREADS=1`
- [ ] `np.random.default_rng(42)` seed 고정
- [ ] CI/CD GitHub Actions 자동 검증

### 9.5 GitHub `paper/verification/` 구조
```
paper/verification/
├── README.md / README.ko.md
├── requirements.txt
├── conda_env.yml
├── Dockerfile
├── verify_lambda_origin.py
├── verify_milgrom_a0.py
├── verify_monotonic_rejection.py
├── verify_mock_false_detection.py
├── verify_cosmic_shear.py
├── ai_prompts/ (5 .md)
├── expected_outputs/ (reference output)
└── .github/workflows/verify.yml
```

---

### 9.7 verification/ vs verification_audit/ 역할 분리

> GitHub 에 두 디렉토리가 병존. *역할 차이 명시* — "어느 것이 official?" 혼란 방지.

- **`paper/verification/`**: External publish용 5 stand-alone Python script (Λ origin, MOND a₀, monotonic, mock injection, cosmic shear). README "Verify in 5 seconds" Quickstart 노출. CI/CD (`.github/workflows/verify.yml`) 자동 실행. 일반 독자/외부 reviewer 1차 진입점.
- **`paper/verification_audit/`**: Internal cold-blooded audit (8-team review) 결과. 8개 `.md` (R1–R8 보고서) + 동수의 `.py` (재현 스크립트) + `.json` (raw evidence). §6.1.2 internal-audit findings 의 raw evidence 저장소. CI/CD 비대상, README Quickstart 비노출. 학계 reviewer 가 audit 신뢰성 검증 시 참조.

**한 문장 요약**: `verification/` = 외부 Quickstart (PASS/FAIL badge), `verification_audit/` = 내부 audit raw evidence (§6.1.2 근거).

---

## 10. 10장 — 그림

### 10.1 본문 그림 일람 (필수 9개)
| # | 제목 | 시각 스타일 | 상태 |
|---|------|----------|------|
| F0 | axiom-derivation dependency graph | 화살표 도식 (6 axiom → 5 derived) | **신설 필요** |
| F1 | σ₀(env) 3-regime + 비단조 dip | log-scale, color-coded | aggregator 필요 |
| F2 | SPARC fit 예시 (3 galaxies) | 3-panel + residual | 표준화 필요 |
| F3 | a₀ = c·H₀/(2π) 도출 도식 | disc projection | Vector graphics |
| F4 | Cluster mass profile (Bullet) | X-ray + stellar + lensing overlay | 표준화 필요 |
| F5 | ρ_q evolution (Bianchi) | log-z + ratio line | 준비 완료 |
| F6 | SPARC log_σ_0 분포 (GMM) | histogram + 2-component overlay | 준비 완료 |
| F7 | Mock injection vs real fit | 2-panel ΔAICc histogram | 준비 완료 |
| F8 | IC 4종 비교 (AIC/BIC/DIC/WAIC) | grouped bar | aggregator 필요 |
| F9 | Falsifier facility timeline | horizontal Gantt | 수동 |

### 10.2 시각적 보강 (일반 독자용 infographic)
- **I1**: SQT 한 장 요약 — "흡수 vs 생성" 화살표 도식
- **I2**: regime 차이 — 우주 → 은하단 → 은하 zoom-in
- **I3**: 22행 한계 표 시각화 — heat-map (영구/ACK/RECOVERY/OPEN)
- **I4**: Falsifier timeline — 시설별 결정 시기

### 10.3 색상/접근성
- 색맹 친화 palette (viridis, cividis)
- Grayscale 인쇄 구분 가능
- Alt-text 모든 figure (시각 장애인 접근)

---

## 11. 11장 — 표 (4개)
| # | 제목 |
|---|------|
| T1 | axiom 1-6 + 동기 |
| T2 | derived 1-5 + 4 축 dependency |
| T3 | 22 예측 전체 |
| T4 | 22행 한계 |

---

## 12. 12장 — Cover Letter
5-블록:
1. 면책 사항 (5 bullet, postdiction caveat 포함)
2. 22행 한계 inventory (§6.1.1 14 own + §6.1.2 8 audit-discovered)
3. DESI 최소/확장 모델 분리
4. Methodological caveats (Λ circularity, iterative refinement)
5. 예상 반박 (prediction vs fit)

---

## 13. 13장 — Reviewer 응답 템플릿
| Reviewer | 예상 공격 | 대응 |
|----------|----------|------|
| 이론가 | derived 5 도출 엄밀성 | 4 축 + 정직 ★★⅓ |
| 관측가 | S_8 악화 | 구조적 인정, Sec 6.1 #1 |
| 통계학자 | anchor caveat | mock 100%, marginalized 0.8, 정직 |

---

## 14. 14장 — 제출 전 TODO 체크리스트

### Layer A — `README.md` (GitHub landing, ★ P0)
- [ ] Hero infographic (I1) + social preview image (1200×630)
- [ ] Language switcher 최상단 (`🇺🇸 English | 🇰🇷 한국어`)
- [ ] Status badge 4개: DOI (Zenodo) | CI | License | OSF preregistration
- [ ] OSF pre-registration badge prominent
- [ ] One-sentence headline (3초 hook)
- [ ] TL;DR 7 bullet (✅⚠️⏰❌📊) including audit-summary headline
- [ ] Verify in 5 seconds 코드 블록
- [ ] Claims status 표 (machine-readable link)
- [ ] How to cite BibTeX 즉시 복사
- [ ] Documentation 링크 (paper PDF, FAQ, verification, OSF)
- [ ] CONTRIBUTING / License 표시

### Layer B — `paper/main_en.tex` (학계 본문, ★ P0)
- [ ] 1–7장 LaTeX 본문 (영문 master + 한국어 mirror)
- [ ] F0 dependency graph 신설
- [ ] F1, F8 aggregator 작성
- [ ] I1–I4 infographic
- [ ] 17σ 정확 Δχ² 수치 삽입
- [ ] Statistical methods appendix 신설 (R3 권고)
- [ ] Dataset inventory 표 (4.2)
- [ ] DESI DR3 inconclusive band 정의 (4.4)
- [ ] 5.2 Λ origin circularity 정직 disclosure
- [ ] 6.5 Methodological caveats
- [ ] 8장 FAQ 3-tier (1 문장/단락/학생용)
- [ ] 색맹/grayscale/alt-text 검증

### Layer C — `paper/verification/README.md` (★ P0)
- [ ] 5-second quickstart 코드 블록
- [ ] 5 script 일람 표 (Time 컬럼 포함)
- [ ] CI badge README 노출 (PASS/FAIL)
- [ ] `compare_outputs.py` diff 도구
- [ ] Dockerfile + conda_env.yml 양방
- [ ] LLM prompt 대안 (`ai_prompts/`)
- [ ] `TROUBLESHOOTING.md`
- [ ] `verification_failure.md` issue template 안내

### Script 작성 규칙
- [ ] `tqdm` 진행 표시 (mock 200회 등 hang 방지)
- [ ] 80자 line wrap (모바일)
- [ ] `OMP_NUM_THREADS=1` 환경 변수
- [ ] `np.random.default_rng(42)` seed
- [ ] `requirements.txt` version pinning
- [ ] `expected_outputs/*.json` reference

### Repository 인프라 (★ P1)
- [ ] `claims_status.json` machine-readable 22행 한계 + 22 예측
- [ ] `LICENSES.md` 디렉토리별 license 표
- [ ] `CITATION.cff` Zenodo DOI 호환
- [ ] `.github/CONTRIBUTING.md`
- [ ] `.github/CODE_OF_CONDUCT.md` (Contributor Covenant 2.1)
- [ ] `.github/PULL_REQUEST_TEMPLATE.md`
- [ ] `.github/ISSUE_TEMPLATE/{bug_report,verification_failure,suggestion}.md`
- [ ] `.github/workflows/verify.yml` CI/CD
- [ ] `.github/og-image.png` social preview
- [ ] `results/INTERNAL_IDS.md` (Lxxx/Pxxx/Branch → 외부 명칭 매핑)

### 다국어
- [ ] README.md 영문 master (GitHub landing)
- [ ] README.ko.md *full mirror* (요약본 아님)
- [ ] paper/main_en.tex + main_ko.tex 병행
- [ ] FAQ EN + KO 동일 정직 강도 검증
- [ ] verification/ README EN + KO
- [ ] TRANSLATION_POLICY.md

### 모바일 친화
- [ ] 모든 README 표 4-column 이하 또는 `<details>` collapse
- [ ] 코드 블록 80자 wrap
- [ ] LaTeX 수식 → Unicode (ρ_q, σ₀, H₀)
- [ ] PDF 압축 + 페이지 수 명시

### 출판 (GitHub + Zenodo DOI 만, arXiv 안 함)
- [ ] Author list, affiliation, ORCID
- [ ] GitHub repository public (영문 README master)
- [ ] GitHub release tag (v1.0) → Zenodo 자동 연동 → DOI 발급
- [ ] DOI 발급 후 README/CITATION.cff/paper PDF 에 DOI 추가 commit
- [ ] OSF 사전 등록 (DESI DR3 발표 *전*)
- [ ] License: MIT 코드 + CC-BY-4.0 텍스트/그림 (디렉토리별 LICENSES.md)
- [ ] **★ 최종 PDF (EN+KO) + README (EN+KO) grep 검증**:
  - `L\d{2,3}` 0건
  - `P\d{1,2}` 0건
  - `Branch [AB]` 0건
  - `Pillar [1-5]` 0건
  - `F[1-3]` test 명칭 0건 (서술형 치환)
  - `loop`, `iter`, `iteration count` 0건

---

## 15. 15장 — Build pipeline (3-layer 통합)

```
내부 결과 (results/, simulations/)
    ↓ synthesis 종합
paper/base.md (한국어, 내부 작업용)
    ↓ 영문 번역 + 내부 ID 제거 + figure 생성
paper/base_en.md (대외 공개)
    ↓
┌─────────────────────────────────────────────────────────┐
│  3 layer 동시 빌드                                        │
│                                                          │
│  Layer A: README.md / README.ko.md                       │
│    └─ Hero infographic + TL;DR + 5초 quickstart          │
│       + claims_status.json (machine-readable)            │
│                                                          │
│  Layer B: paper/main_en.tex / main_ko.tex                │
│    └─ 1-7장 본문 + appendix (FAQ, verification,          │
│       statistical methods, dataset inventory)            │
│                                                          │
│  Layer C: paper/verification/README.md (EN+KO)           │
│    └─ 5초 quickstart + Docker + conda + tqdm script      │
└─────────────────────────────────────────────────────────┘
    ↓ (compile + grep 검증 + bilingual 일관성 체크 + CI/CD)
├── paper/main_en.pdf → GitHub release (v1.0 tag)
└── paper/main_ko.pdf → GitHub release
    ↓ Zenodo 자동 연동
DOI 발급 → README/CITATION.cff/paper PDF 에 DOI 추가 commit (v1.0.1)
    ↓
GitHub repository (publish)
├── README.md          (영문 landing, language switcher 최상단)
├── README.ko.md       (한국어 full mirror)
├── claims_status.json (22행 한계 + 22 예측 machine-readable)
├── LICENSES.md
├── CITATION.cff
├── .github/           (CONTRIBUTING, CODE_OF_CONDUCT, ISSUE_TEMPLATE,
│                       workflows/verify.yml, og-image.png)
├── paper/             (PDF + LaTeX + verification + figures + faq)
├── results/           (공개 + INTERNAL_IDS.md 매핑)
└── data/              (외부 데이터 mirror)
    ↓
3 사용자 시나리오 모두 5분 안에 만족:
  • 첫 방문자: README 3초 hook + claim status 표
  • 학생/시민: verification 5초 quickstart
  • 학계: paper PDF + statistical methods appendix
```

---

## 16. 16장 — 한 줄 결론

> SQT 는 falsifiable phenomenology — Λ 기원 차원 일치 (circularity caveat 포함) + Bullet cluster PASS 의 강점, S_8 악화 + 비단조 postdiction + sloppy d_eff=1 의 약점, DESI DR3 (2025–2026) 의 임박 결정.
> 8인 self-audit (32 claim) 결과 (L411 reframed, L415 sync): **substantive 13% (4) + identity 9% (3) + inheritance 25% (8) + CONSISTENCY_CHECK 3% (1, Λ origin) + partial 25% (8) + NOT_INHERITED 25% (8)** + FRAMEWORK-FAIL 0. *Raw 28% PASS_STRONG (post-L412 down-grade, 9/32) / substantive 13% (4/32) 양면 표기 — raw 단독 인용 금지.* — *cherry-pick 없이 정직 disclose*.
> GitHub 3-layer (README landing / paper 본문 / verification quickstart) + Zenodo DOI (arXiv 안 함) 로 일반인부터 학계 reviewer 까지 모두 5분 안에 검증 가능한 *open-science 모델*.

---

## 부록 A — 모호점 추적 문서 (`paper/AMBIGUITIES.md`)

본 base.md 의 D-1 ~ D-15 결정 사항 + 작성 중 발견되는 신규 모호점을 별도 *living document* 로 추적.

```
paper/AMBIGUITIES.md
├── Resolved decisions (D-1 ~ D-15 from base.md)
├── Open questions (작성 중 발견)
├── Numerical values to be looked up
└── Cross-references to verification scripts
```

작성 중 모호점 발견 시 즉시 AMBIGUITIES.md update → 결정 후 base.md 와 동기화.
