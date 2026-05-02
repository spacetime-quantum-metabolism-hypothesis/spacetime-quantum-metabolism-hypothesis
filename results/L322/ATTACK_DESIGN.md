# L322 — Global vs Local Optimum Attack Design

**Loop**: L322 (single)
**Target**: BB σ_0 posterior multimodality. Current single-mode (cosmic 8.37, cluster 7.75, galactic 9.56) — global or local?
**Date**: 2026-05-01

## Context

- 누적 235 loop, ★★★★★ -0.05, JCAP 93–97%
- L272 mock 100% false-detection (BB anchor flexibility)
- L281 marginalized ΔlnZ = 0.8 only
- L273 GMM: SPARC alone k=2 best (3-mode 미발견)
- L301: BB regime ↔ RG fixed point 매핑

3-regime split이 데이터에서 강제된 것인지, 아니면 우리가 사전에 박은 partition 위에 단일 mode가 얹힌 것인지 — 이게 본 loop의 핵심 질문.

## 8인 공격 (각자 독립 설계)

- **A1 (Topology)**: σ_0 3D 공간에서 likelihood surface 의 local minima 개수. Hessian eigenvalue 검사 — 현재 점이 saddle 인가?
- **A2 (Permutation)**: regime-label permutation 6가지 ((cos,clu,gal) → 5 nontrivial 재배치). 같은 χ² 달성하는 alternative assignment 존재?
- **A3 (Annealing)**: simulated annealing T=10→0.01, 100 chain, 각 random start. Global minimum 도달률 < 90% 면 multimodal.
- **A4 (Multi-start)**: ~100 LBFGS / Nelder-Mead start from Latin hypercube σ_0 ∈ [3, 15]^3. Distinct minima 개수.
- **A5 (Merger test)**: cosmic+cluster regime 병합 (2-regime 모델, σ_0 2개) ΔAICc. 병합이 더 단순한데 fit 비슷하면 3-regime 은 over-partition.
- **A6 (Boundary degeneracy)**: regime cutoff (z_cos, M_clu) 와 σ_0 사이 degeneracy. cutoff 옮겼을 때 σ_0 best-fit 이 따라가는가?
- **A7 (Nested resampling)**: dynesty multi-modal mode 옵션 ON, ndim=3 σ_0 만 free. lnZ 와 mode count 직접 추출.
- **A8 (Prior sensitivity)**: σ_0 prior U[1,20] vs U[5,12] vs Gaussian(8, 3). Posterior mean 변화 > 1σ 면 prior-driven.

## Top-3 (8인 합의)

A4 + A5 + A7. 이유:
- A4 = 가장 직접적 multimodality 증거 (computational, 빠름)
- A5 = SQMH 이론 자체에 대한 falsification 채널 (3-regime 강제성)
- A7 = Bayesian 정합성, JCAP referee R3 가 직접 요구할 가능성

## 권고

1. **A4**: 100 multi-start MAP search. distinct minima 개수, χ² 분포.
2. **A5**: 2-regime merge model 비교. ΔAICc(2-reg vs 3-reg) 부호.
3. **A7** (deferred): dynesty multimodal — L323 candidate.

## 정직 원칙

- Alternative mode 발견 시 정직 보고
- 글로벌 최적 미입증 시 그대로 명시
- L272 false-detection 기록과 정합되게 — anchor flexibility 가 multimodality 와 결합되면 더 큰 문제
