# L436 REVIEW — `claims_status.json` machine-readable 생성

**Loop**: L436 (독립)
**Date**: 2026-05-01
**Spec source**: `paper/base.md` line 480ff (`claims_status.json` schema v1.1)
**Single source of truth**: `paper/base.md` §6.5(e)
**Output**: `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/claims_status.json`

## 1. 임무 요약

paper/base.md L402–L415 reframing 결과를 단일 machine-readable JSON 파일로 산출.
- 32 claim 분포 (PASS_STRONG 4 + PASS_IDENTITY 3 + PASS_BY_INHERITANCE 8 + CONSISTENCY_CHECK 1 + PARTIAL 8 + NOT_INHERITED 8 + FRAMEWORK-FAIL 0)
- 22 limitations (§6.1.1 14 own + §6.1.2 8 audit-discovered)
- 11-value status enum 적용, legacy `PASS`/`PASS_TRIVIAL` 미사용
- 각 항목 inline `i18n.en` / `i18n.ko` (label + status_label) 포함

## 2. 산출물 검증

```
$ python3 -c "..."
claim count: 32
claim status dist: {'PASS_STRONG': 4, 'PASS_IDENTITY': 3, 'CONSISTENCY_CHECK': 1,
                    'PASS_BY_INHERITANCE': 8, 'PARTIAL': 8, 'NOT_INHERITED': 8}
limitations count: 22
SPEC MATCH: True
```

산수 검증: 4 + 3 + 8 + 1 + 8 + 8 = **32 ✓** (FRAMEWORK-FAIL 0)
한계 검증: §6.1.1 14 + §6.1.2 8 = **22 ✓**

i18n drift assertion (모든 항목 `en/ko/label` 양쪽 존재): **OK**

## 3. 32-claim 매핑 근거

`paper/base.md` 및 `results/L411/SYNTHESIS_paper_base_md_v2.md` 의 분포 명세를 따라 매핑:

- **PASS_STRONG (4, substantive)**: Newton 회복, BBN ΔN_eff, Cassini PPN, EP η=0 — 명시적으로 §6.5(e) 에 4건 열거.
- **PASS_IDENTITY (3, σ₀=4πG·t_P 산술 따름)**: n₀μ=ρ_Planck/(4π), ξ scaling, Λ-theorem 차원 — §6.5(e) 명시.
- **PASS_BY_INHERITANCE (8)**: 구 PASS_TRIVIAL 2 (GW170817 Lagrangian-form, LLR 동어반복) + 표준 QFT/사전지식 inheritance 4 (Lorentz/KMS, uncertainty, CPT, wavefunction) + L409 재분류 2 (BH entropy S=A/(4ℓ_P²), Bekenstein bound). L411 SYNTHESIS 의 "PASS_TRIVIAL 2 + INHERITANCE 4 + L409 재분류 2 = 8" 분해와 일치.
- **CONSISTENCY_CHECK (1)**: Λ origin (§5.2) — L412 PR P0-1 down-grade.
- **PARTIAL (8)**: σ₀ three-regime (postdiction caveat), CMB θ_*, Bullet cluster (L417 caveat), Q parameter transition (L403), v=g·t_P (L409 PARTIAL 재분류), three-regime anchors, sloppy d_eff, theory-prior anchor postdiction.
- **NOT_INHERITED (8)**: §6.1.2 row 15–22 (singularity, Volovik, Jacobson, GFT BEC, BEC nonlocality, DESI ξ_q joint fit, 3자 정합성, 5-program 동형).

## 4. 22-row limitations 매핑

- **§6.1.1 paper-framework 14 entries** (rows 1–14): S_8 (OBS-FAIL permanent), H₀ ~10%, n_s 외부, β-function 계수, three-regime 약함, sloppy d_eff, theory-prior anchor, cluster single-source (RECOVERY-PROGRESS), subset Bayes factor, micro completeness 80%, axiom 4 발현 metric, DESI V(n,t) gate, Λ_UV definitional, **Cosmic-shear Euclid DR1 4.4σ pre-registered falsifier**.
- **§6.1.2 internal-audit 8 entries** (rows 15–22): NOT_INHERITED 8건 — claims 의 NOT_INHERITED 8 과 1:1 대응.

## 5. 정직 한 줄

claims/limitations 분포는 `paper/base.md` §6.5(e) 명세와 산수 일치하나, 32 claim 의 *항목별* 단일 canonical 리스트가 base.md 본문에 enumeration 으로 존재하지 않아 PASS_BY_INHERITANCE 8 의 4 standard-inheritance 슬롯 (Lorentz/KMS, uncertainty, CPT, wavefunction) 은 `verification_audit/audit_result.json` 의 13 test 결과와 L411 SYNTHESIS 의 분해 ("PASS_TRIVIAL 2 + INHERITANCE 4 + L409 재분류 2") 를 결합해 *복원 매핑* 한 결과이며, base.md 에 직접 인용 없는 보강 식별이다. 향후 base.md 에 32 claim id 를 본문에 명시 등재하는 것이 drift 방지에 권고됨.
