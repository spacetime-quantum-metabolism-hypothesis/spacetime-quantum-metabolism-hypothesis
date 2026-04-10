# Phase 3 — MCMC Joint Likelihood (DESI + Planck + DESY5)

## 목적

base.fix.class.md Phase 3. Phase 2 CLASS 패치 후:

1. **Full posterior** — xi_q, V_params, 6개 LCDM + 13개 nuisance 동시 MCMC
2. **Marginalized constraints** — 1D/2D 분포, w0-wa 평면
3. **Tension 정량화** — Planck-DESI, Planck-SN 간 tension
4. **DR3 대비** — Phase 3 결과가 DR3 발표(2026말-2027초) 전 나와야 함

## 도구

**Cobaya** (권장): `github.com/CobayaSampler/cobaya`
- CLASS/CAMB 통합 네이티브
- Planck 2018 + DESI DR2 + DESY5 likelihood 내장
- MontePython 대비 YAML 간결, 병렬 MCMC 쉽게

**MontePython** (대안): `github.com/brinckmann/montepython_public`
- 전통적, 많은 레퍼런스 논문 재현용

## 파이프라인 개요

```
Phase 2 CLASS-SQMH 패치 완료
  -> cobaya-install cosmo
  -> sqmh_theory_wrapper.py (theory class: wraps classy)
  -> sqmh_planck_desi.yaml (config)
  -> cobaya-run -r 4 sqmh_planck_desi.yaml (4 MCMC chains)
  -> chains/sqmh_planck_desi.*.txt
  -> GetDist analysis -> corner plots, marginalized Delta_chi2
```

## 파일 구조

```
simulations/mcmc/
|-- README.md                  # 이 문서
|-- sqmh_planck_desi.yaml      # Cobaya config 스텁
|-- sqmh_theory_wrapper.py     # CLASS-SQMH → Cobaya theory class
|-- run_mcmc_stub.py           # 실행 진입점 (Phase 2 완료 후 활성화)
|-- analyze_chains.py          # GetDist 후처리 (corner, constraints)
```

## 실행 단계 (Phase 2 완료 후)

### 단계 1: Cobaya 환경 구축
```
pip install cobaya getdist
cobaya-install cosmo -p ~/cobaya_packages
# DESI 2025 + DESY5 + Planck 2018 모듈 자동 다운로드
```

### 단계 2: theory wrapper 구현
`sqmh_theory_wrapper.py`:
- `from cobaya.theories.classy import classy`
- `SQMHClassy(classy)` subclass
- `must_provide`, `calculate` override하여 xi_q, V_params 전달

### 단계 3: MCMC 실행
```
cobaya-run sqmh_planck_desi.yaml --resume
# 4 chains, Gelman-Rubin R-1 < 0.05 수렴 조건
# 예상: ~24시간 x 4 코어
```

### 단계 4: 분석
```
python analyze_chains.py chains/sqmh_planck_desi
# 출력:
#  - 1D/2D marginalized posteriors
#  - Best-fit chi2, Delta_chi2 vs LCDM
#  - AIC, BIC
#  - w0-wa 평면 타원 (DESI paper 재현용)
```

## 목표 산출물

1. **figures/13_sqmh_mcmc_posterior.png** — corner plot (xi_q, n, Omega_m, H0, sigma_8)
2. **figures/14_sqmh_w0_wa.png** — w0-wa 평면 (LCDM 대비 SQMH 타원, DESI 공식 타원 오버레이)
3. **tables/phase3_constraints.md** — marginalized 68%/95% CL 테이블
4. **base.md §15.1 #6 최종 갱신** — Phase 3 결론 반영

## 판정 기준 (Phase 3 결과별)

| Delta_chi2 (Phase 3) | Delta_AIC (13+22 params) | 판정 | base.md 갱신 |
|---------------------|-----|------|-------------|
| < -10 | < -6 | **SQMH-RP 강력 지지** | §15.1 #6 "해결됨" |
| -10 ~ -4 | -6 ~ 0 | 약한 개선, 결론 보류 | DR3 대기 |
| > -4 | > 0 | **Path F 반증** | §XVII 반증 사례로 이동 |

## 리스크

1. **계산 비용**: Planck + DESI + DESY5 joint MCMC = 수일~수주. 병렬 4-8 chain 필수.
2. **Prior dependence**: xi_q, V_params의 prior 선택이 posterior shape에 영향. log-uniform vs uniform 비교.
3. **Nuisance degeneracy**: xi_q와 sigma_8 사이 degeneracy 가능. lensing amplitude로 breaking.
4. **DR3 일정**: 2026말-2027초 DR3 발표 전 Phase 3 완료가 critical path.

## 참고 문헌
- Torrado & Lewis, "Cobaya: Code for Bayesian Analysis of hierarchical physical models", 2005.05290
- DESI Collaboration, arXiv:2503.14738 (DR2 BAO)
- DES Collaboration, arXiv:2401.02929 (DESY5 SN)
- Planck 2018 Results VI, arXiv:1807.06209
