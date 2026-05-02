# L373 ATTACK DESIGN — SPARC log_a0 distribution: monotonic σ vs V-shape, marginalized lnZ

**컨텍스트**: L342 의 3-anchor LRT 가 Δχ²=288 (17σ formal) 을 보고했으나 cluster
single-source 의존이 caveat 로 남아 있다. L371 등급 −0.12 의 핵심 원인 중 하나는
"실측 데이터에 비단조성을 직접 검증하지 않았다" 였다. L373 은 SPARC 163 galaxy
per-galaxy `log_a0` 분포를 사용해 *데이터 내부에서* 단조 vs 비단조 함수형 비교를
정직 marginalized lnZ (Laplace) 로 정량화한다.

---

## 8인 자유 사고 (요지)

- **데이터 정직성**: SPARC 는 *galactic regime 단일* — cosmic/cluster 비교 불가. x 축
  으로 `log_Vmax` (intra-galactic env-density proxy) 사용. 즉 본 loop 는 L342 의
  17σ 를 *재현* 하는 게 아니라, "galactic 내부에서도 비단조 흔적이 있는가" 를 묻는다.
- **모델 선택**:
  - M1: linear `y = A + B x` (k=2, monotonic)
  - M2 sym: V-shape `y = A + B|x − x0|` (k=3, vertex 1개)
  - M2 asym: 비대칭 V `y = A + B_L(x0−x), x<x0; A + B_R(x−x0), x≥x0` (k=4)
- **likelihood**: per-galaxy gaussian, σ_y = L69 residual_std = 0.567 dex 일정.
- **prior**: 평탄 box. A∈[−15,−5], B,B_L,B_R ∈[−5,5], x0 ∈ [x.min()+0.05, x.max()−0.05].
- **lnZ**: Laplace, `ln Z = −χ²_min/2 + (k/2) ln 2π − ½ ln det(½H_χ²) − ln V_prior`.
- **AICc/BIC**: parallel reporting.
- **L342 비교**: Δχ²=288 (3 anchor, cluster-driven) 와 Δχ²_SPARC 직접 대조.
- **B-team 도전**: x = log_Vmax 가 진짜 env density 와 monotone 1:1 인가? 아니면 sub-
  selection bias 가 V-shape 을 인공 생성? — Z-stress 로 sigma 인플레이션 추가
  실험 권고 (본 loop 는 baseline 만).
- **B 등급 위험**: V-shape 의 vertex 가 데이터 경계에 박히면 ill-defined → x0 box
  내부로 강제 (x0_lo+0.05).

## 합의 핵심 디자인 (8/8)

1. **x = log_Vmax**, y = log_a0, σ_y = 0.567 dex (L69 residual_std).
2. **모델 3종** 비교 (M1, M2sym, M2asym).
3. **점수**: χ², AIC, BIC, AICc, **Laplace ln Z** (marginalized).
4. **L342 대조**: 동일 prior 형태로 Δχ², ΔlnZ 동시 보고.
5. **정직 한 줄 명시**: SPARC 는 galactic-only — L342 의 cluster gap 은 SPARC 만으로
   는 검증 불가.

## Q-question

- **Q-L373**: "galactic regime 내부에서 σ(ρ) 비단조 흔적이 marginalized lnZ 로
  유의하게 선호되는가?" — Δ ln Z > +1 이면 약한 선호, > +3 이면 강한 선호.
