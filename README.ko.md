# 시공간 양자 이론 (Spacetime Quantum Theory, SQT)

[🇺🇸 English](README.draft.md) | 🇰🇷 한국어

[![DOI](https://img.shields.io/badge/DOI-pending-lightgrey.svg)](https://doi.org/10.5281/zenodo.PENDING)
[![CI](https://img.shields.io/badge/CI-pending-lightgrey.svg)](https://github.com/USER/REPO/actions)
[![License: MIT (code) / CC-BY-4.0 (text)](https://img.shields.io/badge/license-MIT%20%2B%20CC--BY--4.0-blue.svg)](LICENSES.md)
[![OSF preregistration](https://img.shields.io/badge/OSF-preregistered-lightgrey.svg)](https://osf.io/PENDING)

![Hero infographic](paper/figures/hero.png)

> **한 문장 요약**: *우주상수 스케일과 Milgrom의 a₀를 다루는 6공리 phenomenology 프레임워크 — hidden DOF 명시 / embedding-조건부 caveat / DR3 단일 사전등록 falsifier 와 함께 공개.*

## TL;DR
- ⚠️ ρ_q/ρ_Λ(Planck) 자릿수 일치 (CONSISTENCY_CHECK; 순환성 구조적 — §5.2; L402 회피 불가)
- ✅ a₀ = c·H₀/(2π) 자릿수 invariance (5축 factor-≤1.5; *정량* 행은 L502/L516 에 따라 PASS_MODERATE 로 격하)
- ⚠️ Bullet cluster: PASS_QUALITATIVE 한정 (Bullet/MACSJ0025/MACSJ1149 3/4; A520 dark core 모호; L509)
- ❌ S_8 tension: SQT가 ΛCDM보다 +1.14% **악화** (OBS-FAIL, 구조적 μ_eff≈1, 파라미터 회피 불가)
- ⚠️ 3-regime σ₀(env) 는 post-hoc fit; **L510**: 3개 anchor 중 진정 외부 측정 0개 (cosmic 명시 circular, cluster LCDM-bridged, galactic MOND-prior + SQT-internal)
- ⏰ **결정적 falsifier: DESI DR3 w_a (full-Y5 cosmology 발표는 LBL 2026-04 공식 안내에 따라 2027 예정; L520)** — minimal SQT는 w_a=0
- 📊 자체감사 (claim 33개, *L516 hidden-DOF 재등급*): 정직 AICc penalty 적용 시 substantive PASS_STRONG **0%**; PASS_MODERATE 5 + PASS_QUALITATIVE 1 = **18% combined PASS**; PASS_IDENTITY 3 + PASS_BY_INHERITANCE 8 + CONSISTENCY_CHECK 1 + PARTIAL 7 + NOT_INHERITED 8; FRAMEWORK-FAIL 0. 레거시 "PASS_STRONG 9/32 = 28%" 헤드라인은 *철회* — 참고용 보존만. 전문 §6.1 + raw evidence는 [paper/verification_audit/](paper/verification_audit/).
- 🎯 **독립성 audit (L498)**: 6개 사전등록 falsifier 의 **N_eff = 4.44** (participation ratio); ρ-보정 결합 검출 **8.87σ** (active 5 → 9.95σ), naive 11.25σ는 폐기.
- 📡 **JCAP majority-acceptance 추정 (L517 + L521 갱신)**: 8–19%, 중앙 **13–14%** — 조건: (abstract drift 5위치 정정 + claims_status sync + §4.1 RAR sub-row 분리 + §6 limitations 8행 추가).

## 5초 안에 검증 (Verify in 5 seconds)
```bash
git clone https://github.com/USER/REPO.git
cd REPO/paper/verification
pip install -r requirements.txt
python verify_lambda_origin.py     # Λ 기원 차원 일관성 점검
                                   # (ρ_Λ_obs 입력에 대해 순환적 — §5.2)
```
나머지 4개 스크립트는 `paper/verification/`. [Verification README](paper/verification/README.md) 참조.
내부 감사(R1–R8 cold-blooded audit + L491–L514, L517 substrate)는 [paper/verification_audit/](paper/verification_audit/) 와 [results/L518](results/L518/SYNTHESIS_v7.md), [results/L521](results/L521/SYNTHESIS_v8.md).

## Claim 상태 표 (기계 판독본: [claims_status.json](claims_status.json))

*전체 22행 한계 표(§6.1) + 11행 PASS 표(§4.1)의 요약 뷰. 각 행은 정식 표의 한 개 이상 항목을 묶은 것이며 **Maps to** 열에 교차참조.*

*문서 전체에서 사용하는 두 가지 "fail" 의미 (혼동 금지):*
- ❌ **OBS-FAIL** (관측적 악화) — SQT가 실제 데이터에 대해 구조적으로 핏을 악화 (예: S_8). 이론-데이터 tension.
- 🚫 **FRAMEWORK-FAIL** (내부 불일치) — **현재 0건** (§6.5(e)).

*L516 hidden-DOF 재등급에 따라: 모든 substantive PASS_STRONG 행은 1–2 hidden DOF 적용. L502 AICc penalty (k_h ∈ {1,2}, ΔAICc ∈ [+2,+5]) 적용 시 **AICc 정직 잣대로 PASS_STRONG 생존 0건**. 신규 등급: PASS_MODERATE / PASS_QUALITATIVE / OPEN_PROVISIONAL.*

| Claim | 상태 (post-L516) | 근거 (Evidence) | 주의 (Caveat) | Maps to |
|---|---|---|---|---|
| Λ 기원 (origin) | ⚠️ CONSISTENCY_CHECK | ρ_q/ρ_Λ 자릿수 일치 (차원 일관성, *예측 아님*) | 순환성 구조적 (n_∞가 axiom 3 통해 ρ_Λ_obs 입력); L402 Path-α 독립유도 실패 | §5.2; §6.1 row 13 |
| MOND a₀ (자릿수) | ✅ PASS_MODERATE [`RAR_a0_orderof`] | a₀ = c·H₀/(2π), 5축 factor-≤1.5 invariant; 7기준 6/7 PASS | L491 cross-form 0.37 dex (IQR 0.17); L496 LOO max\|ΔPR\|=0.089 < 0.125 | §1.2.2; §4.1 sub-row (a) |
| MOND a₀ (정량) | ⚠️ PASS_MODERATE [`RAR_a0_quantitative`] | M16 + Υ⋆ canonical; ΔAICc_honest = +4.707 (k_h=2) | L492 cross-dataset 1/4 PASS (D4 dwarf Δlog=−0.353); L503 a₀ NOT universal; L495 hidden DOF 9–13 | §4.1 sub-row (b) |
| Bullet cluster | ⚠️ PASS_QUALITATIVE | Bullet/MACSJ0025/MACSJ1149 3/4 정성 PASS | A520 dark core 모호; 4/4 정량 magnitude 도출 불가 (L509) | §4.1 row 10 |
| BBN ΔN_eff | ✅ PASS_MODERATE | ΔN_eff ≈ 10⁻⁴⁶ < 0.17; cross-experiment robust (L507) | η_Z₂ ≈ 10 MeV stipulation (k_h=1); ΔAICc_honest = +2.0 — borderline | §4.1 row 2 |
| Cassini PPN | ✅ PASS_MODERATE | \|γ−1\|≈10⁻⁴⁰, 6/8 채널 | **embedding-conditional**: channel 3 universal_phase3 (β=0.107) HARD FAIL ~1000×; dark-only / Vainshtein / chameleon screening 한정 (L506) | §4.1 row 3 |
| EP \|η\|=0 | ✅ PASS_MODERATE | MICROSCOPE 구조적 0 | LLR Nordtvedt \|η_N\|≲10⁻¹⁴ non-zero (G_N(t) drift β_dark~0.1; L508) | §4.1 row 4 |
| GW170817 c_T, LLR Ġ/G | ✅ PASS_BY_INHERITANCE | \|Δc/c\|=0; Ġ/G=0 | Lagrangian 형태 선택 + 공리 동어반복 (구 `PASS_TRIVIAL` alias); disformal 부활 ⇒ KILL | §4.1 rows 5–6 |
| 3-regime σ₀(env) | ⚠️ PARTIAL + POSTDICTION | 17σ regime-gap | **L510**: 진정 외부 anchor 0/3 — cosmic 명시 circular, cluster LCDM-bridged + Lorentzian ansatz, galactic MOND-prior + SQT-internal D1 (β=1); 1.81 dex 격차는 methodological prior 가능성 | §3.4; §6.1 rows 5–7 |
| CMB θ_* shift | ⚠️ PARTIAL | δr_d/r_d ≈ 0.7% (Planck σ × 23) | 물질기 φ 진화; Phase-2 BAO와 같은 채널 | §4.1 row 8 |
| S_8 tension | ❌ OBS-FAIL (구조적) | ΛCDM보다 +1.14% 악화 (ξ_+ +2.29%) | 구조적 μ_eff≈1, 파라미터 회피 없음 | §4.6; §6.1 row 1 |
| DESI w_a | ⏰ PENDING (DR3 full Y5 cosmology = 2027) | minimal SQT: w_a=0; V(n,t)-확장 gate OPEN | LBL 2026-04 발표: full Y5 결과 2027 예정 (L520); preprint 윈도우 12–18개월 | §4.3, §4.4, §5.4; §6.1 row 12 |
| 기초/계승 gap | ⚠️ NOT_INHERITED | 8/33 claim (singularity, Volovik, Jacobson, GFT/BEC chain) | axiom 4 5th-pillar 결정이 8개 중 5개 차단 | §6.1 rows 15–22 |

### `claims_status.json` 신규 키 권고 (L518 §3.3 + L498/L495/L502/L506/L508/L510)

다음 6 키는 *권고 추가* — 직접 적용은 L512 (Rule-A 8인 라운드) + L513 (Rule-B 4인 코드리뷰) 사후승인 후. 추적은 [results/L524/REPO_FINAL.md](results/L524/REPO_FINAL.md):

1. `RAR_a0_orderof` — PASS_MODERATE; 5축 factor-≤1.5 invariant.
2. `RAR_a0_quantitative` — PASS_MODERATE; ΔAICc_honest = +4.707, hidden DOF k≈3 (M16 + Υ⋆ canonical 한정).
3. `falsifier_Neff` — 값 4.44 (participation ratio, L498); naive 6 폐기; 결합 유의도 {all6_corr: 8.87σ, active5_corr: 9.95σ, naive: 11.25σ}.
4. `hidden_dof_audit` — 보수 9 / 확장 13 (L495); abstract drift 5위치 카탈로그.
5. `cassini_embedding_conditional` (`cassini-ppn` 의 caveat 확장) — universal β=0.107 HARD FAIL 1000×; dark-only / screening 한정 PASS.
6. `sigma0_methodological_prior` (`sigma0-three-regime` 의 caveat 확장) — 진정 외부 anchor 0/3 (L510); 1.81 dex 격차 부분/전부 methodological 가능성.

## 인용 방법 (How to cite)
```bibtex
@article{SQT2026,
  title   = {Spacetime Quantum Theory: A 6-Axiom Phenomenological Framework with Honest Hidden-DOF Disclosure and Pre-Registered Falsifiers},
  author  = {<author>},
  year    = {2026},
  version = {L524},
  doi     = {10.5281/zenodo.PENDING},
  url     = {https://github.com/genesos/spacetime-quantum-metabolism-hypothesis}
}
```

> **DOI 버전관리**: Zenodo *concept DOI*는 모든 버전 통합; *version DOI*는 특정 release. 본문 인용은 **concept DOI** 권장.

## 문서 (Documentation)
- [논문 PDF (English)](paper/main_en.pdf) | [논문 PDF (한국어)](paper/main_ko.pdf)
- [일반 청중용 FAQ](paper/faq_en.md) | [한국어 FAQ](paper/faq_ko.md)
- [검증 quickstart](paper/verification/README.md)
- [정직한 한계 표 (기계 판독본)](claims_status.json)
- [L518 Phase 1+2+3 종합](results/L518/SYNTHESIS_v7.md)
- [L520 pre-DR3 publish strategy](results/L520/PUBLISH_STRATEGY.md)
- [L521 Phase 1+2+3+4+5 종합 (v8)](results/L521/SYNTHESIS_v8.md)
- [L524 repository final-touch 결정](results/L524/REPO_FINAL.md)
- [OSF 사전등록](https://osf.io/PENDING)
- [번역 정책](TRANSLATION_POLICY.md)

## 정직성 선언 (L524)

본 README와 하부 paper 는 헤드라인 숫자 retrofit 을 명시적으로 금지한다:
- 레거시 "PASS_STRONG 9/32 = 28%" 헤드라인은 *철회*. L516 hidden-DOF 정직 분포 (AICc penalty 적용 시 PASS_STRONG **0%**) 로 대체.
- "6 독립 falsifier 11.25σ" 는 N_eff = 4.44 / 8.87σ (ρ-보정) 로 대체.
- "DR3 2025–2026" 은 LBL 2026-04 공식 안내에 따라 "full Y5 cosmology 2027" 로 정정 (L520).
- 모든 cross-channel caveat (Cassini embedding, EP LLR, σ₀ external-anchor 카운트) 는 §6.1 에서 헤드라인 표로 끌어올려 referee 가 30페이지 후에야 만나지 않도록 함.

## 기여 (Contributing)
[CONTRIBUTING.md](.github/CONTRIBUTING.md) 참조. Verification-failure 보고용 issue 템플릿은 `.github/ISSUE_TEMPLATE/`.

## 라이선스 (License)
Code: **MIT**. Text/Figures: **CC-BY-4.0**. 디렉터리별 표: [LICENSES.md](LICENSES.md).
