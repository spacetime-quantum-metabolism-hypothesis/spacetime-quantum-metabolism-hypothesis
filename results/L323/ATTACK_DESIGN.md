# L323 — Information geometry of BB parameter space

> 235-loop 누적 + L272 false-rate 100% + L281 marginalized ΔlnZ=0.8 의 패턴은
> **likelihood landscape 가 sloppy (flat directions 다수) + 잘못된 anchor 에 자기조정** 되었을 가능성을 시사.
> Fisher / Riemannian 정보 기하로 정량 검증한다. 8인 자율 분담.

---

## 0. 동기 (왜 L323 인가)

- L272 mock 100% false-detection → BB 가 LCDM mock 에서도 3-regime "발견" → 모델 공간이 anchor 에 *지나치게* 적응한다.
- L281 fixed-θ ΔlnZ=13 → marginalized 0.8 → posterior volume 이 Hessian 추정의 ~e^{12} 배.
  이는 효과 차원이 nominal 3 보다 훨씬 작다는 sloppy-model signature.
- L321 등급 -0.05 가 sloppy 보정 후에도 유지되는지 확인 필요.

핵심 질문: **"global 최적합" 이 진짜 well-defined point 인가, 아니면 manifold 위 한 좌표일 뿐인가?**

---

## 1. 8인 자율 공격 vectors

A1. Fisher 행렬 condition number κ — κ ≫ 1 이면 sloppy direction.
A2. Eigenvalue spectrum 의 log-uniform 분포 (Sethna sloppy signature).
A3. Effective parameter dimensionality — participation ratio
        d_eff = (Σ λ_i)^2 / Σ λ_i^2.
A4. Geodesic distance to LCDM (BB → 0 한계) 에서 info metric.
A5. Reparameterization invariance — log-σ 좌표에서도 같은 결과인가.
A6. Local convexity — Hessian PD?  saddle 가능성?
A7. Global landscape — 다중 basin? mock-injection 100% 와 연결.
A8. Posterior volume / Laplace mismatch — L281 의 Δ=12.2 를 정량 설명.

---

## 2. 자율 분담 (사후 관찰)

토의 결과 자연 발생한 분업:
- Fisher matrix 수치 추정 (finite-difference, central) — 책임 1.
- 좌표계 선택 (linear σ vs log σ) — 책임 1.
- Eigen-spectrum, condition number, participation ratio — 책임 1.
- Geodesic 적분 (LCDM 한계점은 σ_cluster - σ_galactic - σ_cosmic 동일점) — 책임 1.
- Posterior volume Monte-Carlo (3D adaptive grid) — 책임 1.
- 결과 검증 (재현, AICc penalty 일관) — 책임 1+.

---

## 3. 측정 protocol

1. 데이터: L321 SYNTHESIS 의 BB 3-regime anchor set 을 toy 로 모사.
   실측 anchor 를 직접 가져오는 대신, **L196/L272 와 일관된 toy chi² surface**:
        chi²(σ) = chi²_min + (σ-σ*)^T H (σ-σ*)
   에서 H 는 L196 reported Hessian (또는 finite-diff 재추정).
   이 toy 는 "Hessian 으로 본 local geometry" 만 평가하며,
   global multimodality 는 별도 multi-start 로 측정.

2. Fisher I_ij = -<∂_i ∂_j ln L>  ≈  0.5 · ∂²chi²/∂θ_i∂θ_j  (Gaussian 가정).

3. metrics:
   - λ_max / λ_min  →  κ
   - PR = (Σλ)² / (Σλ²)  →  d_eff
   - geodesic L = ∫ √(dθ^T g dθ)  along straight line θ(t)=θ*+t(θ_LCDM-θ*)
   - V_Laplace / V_posterior(MC)  →  L281 격차 진단

4. 좌표 robustness: linear σ vs log σ 두 좌표 모두 보고.
   재파라미터 invariant 인 d_eff·κ 의 비율은 좌표 독립이어야 함.

---

## 4. PASS / FAIL

- d_eff < 2 (즉 nominal 3 보다 1+ 차원 sloppy)  →  L281 의 Akaike-weight 격하 정당.
- κ > 100  →  3-param 중 1+ 가 사실상 자유.
- geodesic L 이 σ_cluster 단독 stretch 보다 짧음  →  LCDM 이 manifold 의 "구석" 이 아니라 "가장자리".

만족 시: BB 파라미터 사실 ≈2 차원, Branch B 의 3-regime 주장은
"3 개 free param" 이 아니라 "1 개 sloppy + 2 개 stiff" 로 재기술해야 함.
이는 논문 Sec 3 / Sec 6 정직 disclosure 항목 추가 의무.

위반 시 (모두 well-conditioned 으로 나옴): L281 의 ΔlnZ=0.8 은 sloppiness 가 아니라
prior volume 에서 오는 것이므로, sloppy 비판 무력화 — 등급 +0.005.

---

## 5. 위험 / 함정

- toy Hessian → 실측 chi² surface 보존 안 함. 결과는 "local" 지표로만 인용.
- log-coord 사용 시 σ→0 (LCDM) 한계에서 metric 발산 — geodesic 은 σ_cutoff (예: 1e-3 dex) 에서 잘라 finite 보고.
- finite-difference step h 의존성 — h ∈ {1e-2, 1e-3, 1e-4} 세 값 모두 시도, 안정성 확인.
- 8인 위반금지: 수치/수식은 *여기까지* (Fisher 정의 외) 명시 안 함.
