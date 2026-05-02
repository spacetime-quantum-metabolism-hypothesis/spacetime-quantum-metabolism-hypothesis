# L335 — ATTACK DESIGN: Cluster anchor 다중화로 single-source dominance 해소

## 배경
L327 진단:
- L208 ΔAICc=99.49 의 anchor χ² 의 ~98% 가 cluster A1689 단일 포인트.
- Tukey biweight (cluster outlier 제거) ΔAICc=4.85 → "strong" 컷 미달.
- f_crit (anchor σ inflation, ΔAICc=10) ≈ 2.53.
- L331 신규 honest limitation #8 등록.

진정한 글로벌 입증 부재: anchor evidence 의 single-cluster 의존.

## 공격 목표
N=1 → N≥10 cluster anchors 로 확장 시 single-source dominance 가 해소되는가?
어떤 cluster 에서 σ_cluster (= a0 등가 가속도 스케일, BB의 cluster-regime 정상화) 를
독립 추출할 수 있는가? 일관성은? 데이터 가용성은?

## 가설 (8인 자유도 분담, 역할 사전 지정 없음)

### A1. Anchor 후보 풀 식별
대상: Coma (A1656), Perseus (A426), Virgo, A2029, A2142, A2218, A1835,
MS1054.4-0321, 1E0657-558 (Bullet, P27 PASS), A2390, A2744, RXJ1347-1145.
각 cluster 에 대해 (z, M_500, σ_v, T_X, weak/strong lensing, SZ flux) 가용성 표.

### A2. Joint multi-probe σ_cluster 추출
세 가지 독립 probe:
- (i) Strong + weak lensing convergence profile → M(<r) → a(r)
- (ii) X-ray hydrostatic equilibrium (Chandra, XMM) → M_HSE(<r)
- (iii) Sunyaev-Zeldovich pressure profile (Planck, ACT, SPT) → P_e(r)
세 probe 를 결합해 cluster 별 a0_eq 또는 BB regime-3 normalization scale 추출.

### A3. Cluster-by-cluster χ² 분포
N=10 anchor 에서 LCDM 의 χ² 분포가 reduced χ²/dof ~ O(1) 이면 single-source
artifact. A1689 만 outlier (z>5σ) 면 cluster ensemble 에서도 진짜 신호.
Stouffer/Fisher combined p-value 로 ensemble significance 평가.

### A4. Single-source dominance metric
Participation ratio PR_anchor = (Σ χ²_i)² / (n · Σ χ²_i²).
N=1: PR=1 (정의상 single).
N=10 후보: PR_target ≥ 5 (정직 기준). PR=10 이면 fully resolved.
A1689 단독에서는 L323 PR=1.04 와 일관.

### A5. Cluster σ 일관성 검증
N anchor 의 σ_cluster 추정치들이 universal value 에 일관 (σ_inter / σ_mean < 0.3) 인가?
일관 → BB cluster regime 보편성 확증.
불일관 → cluster 마다 다른 a0 → universality 가정 자체 falsified.

### A6. Forecast: ΔAICc(N) 와 robust stats 회복
N=1 → N=4 → N=10 으로 늘릴 때:
- Naive ΔAICc(N) ≈ N · ΔAICc_per_cluster (anchor 별 σ_v ≈ A1689 σ_v 가정)
- Tukey biweight ΔAICc(N): outlier 1개 제거해도 N-1 이 남음.
- Huber: cap 영향 dilute.
정량 forecast: N_min 즉 "single-source dominance 해소 + Tukey ΔAICc>10" 만족 N.

### A7. Telescope/archive 데이터 가용성
실제 가용 archive:
- LoCuSS, CLASH, Frontier Fields (HST lensing)
- Chandra Cluster Cosmology Project (X-ray)
- Planck SZ catalog (PSZ2), ACT-DR5, SPT-3G (SZ)
- ACCEPT, REXCESS, XMM-Newton heritage (X-ray dynamics)
가용 sample size, σ_cluster median uncertainty.

### A8. Honest 한계
- Cluster non-equilibrium (mergers, sloshing) → σ_cluster 추출 bias.
- Hydrostatic mass bias (1-b ≈ 0.85 ± 0.1).
- Strong/weak lensing systematic (substructure, line-of-sight).
- Bullet (1E0657) 는 ongoing merger → equilibrium 가정 위반, but P27 PASS 의 reason.
- 따라서 N=10 중 *equilibrium-clean* subset 일 가능성 — 실효 N_eff < 10.

## 산출
- `simulations/L335/run.py` — anchor expansion forecast (N scan, PR, ΔAICc)
- `results/L335/REVIEW.md` — 8인 자율 분담 평가
- `results/L335/NEXT_STEP.md` — L336+ 계획
- `results/L335/ATTACK_DESIGN.md` — 본 문서
