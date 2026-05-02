# L473 — Cosmic Web Fractal → Homogeneous Transition 가설 (Free Speculation)

작성일: 2026-05-01
주제: cluster-scale dip 의 σ_0(z, scale) 변화가 cosmic web 의 fractal-to-homogeneous transition 에서 비롯된다는 자유 추측.

---

## 1. 출발 관측

- 갤럭시 분포의 2-점 상관함수는 r ≲ 수십 Mpc 까지 power-law `ξ(r) ∝ r^{-γ}` 와 정합. 이는 cosmic web 이 *self-similar* (fractal) 구조를 가짐을 시사하며, count-in-spheres 분석은 fractal correlation dimension D_2 ≈ 2 (Pietronero, Sylos Labini 등) 를 보고.
- 그러나 r ≳ R_H ≈ 80–150 Mpc 에서 D_2 → 3 (homogeneity) 로 *transition*. 이 R_H 가 cosmological homogeneity scale.
- L468–L472 에서 SQT/SQMH 의 cluster-scale dip (≈ 5–30 Mpc, typical cluster radius+infall region) 이 하나의 단일 σ_0 (= 4πG·t_P) 가정으로는 재현되지 않음을 확인.

> 핵심 의심: cluster scale (~ 1–20 Mpc) 은 fractal regime 의 *상단* 에 위치하며, transition shoulder R_H 의 *내측 엣지* 와 부분 겹친다. 이 기하학적 위치가 dip 의 위치와 일치하는 것이 단순 우연인가?

## 2. SQMH 측 자유 추측

SQMH 에서 σ_0 는 spacetime 흡수계수 (per-Planck-time soak rate × 4πG·t_P). 표준 가정은 "σ_0 = universal constant". 이를 다음과 같이 *coarse-graining 의존* 으로 완화:

- σ_eff(R) = σ_0 · f(D_2(R))  with  D_2(R) → 2 (R ≪ R_H), → 3 (R ≫ R_H).
- f 의 functional form 은 정하지 않음 (이론 도출은 별도 세션). 단지 D_2 의 transition 이 bulk soak volume 의 *effective measure* 를 바꾼다는 것.
- D_2 = 2 regime: matter 의 measure 가 surface-like → soak 이 boundary 적분 dominated → σ_eff(R) 감소. cluster scale 에서 dip 의 *부호* 와 정합.
- D_2 = 3 regime: bulk soak 회복 → σ_eff(R) → σ_0. 대규모 (BAO, CMB) 에서 SQMH baseline 이 손상되지 않음.

자연 예측:
1. dip 의 outer edge 가 R_H ≈ 100 Mpc 근방에서 *부드럽게* σ_0 baseline 으로 복귀해야 함 (현재 데이터: cluster-cluster 상관 자료에서 검증 가능).
2. dip 깊이 ∝ (3 − D_2(R_cluster)) 에 monotone — fractal 더 강한 영역 (filament-rich, wall-poor) 의 cluster 에서 dip 더 깊음.
3. 우주론 진화: high-z 에서 R_H(z) 가 작아지고 D_2(R_cluster, z) → 3 빨리 도달 → high-z cluster dip 약화. SQT z-dependent dip amplitude 와 직접 비교 가능.

## 3. 정량 sketch (지도 아님, 척도 추정만)

- R_H 관측치 (SDSS, 2dF, WiggleZ): 70–150 Mpc/h — wide spread, 측정법 의존.
- typical cluster virial radius R_vir ≈ 1–3 Mpc, splashback ≈ 1.5 R_vir, infall 영역 ≈ 5–20 Mpc.
- 비율 R_cluster / R_H ≈ 0.05–0.25 → fractal regime 깊숙이.
- D_2 measurement (Sylos Labini 2009, etc.): R = 20 Mpc 에서 D_2 ≈ 2.0, R = 100 Mpc 에서 D_2 ≈ 2.7–2.9.
- 이 차이 (ΔD_2 ~ 0.7–1.0) 가 σ_eff 의 fractional 변화 정도를 setting 할 후보.

(이 값들은 *방향* 만; functional 은 후속 이론 세션 도출.)

## 4. 위험 및 falsifier

- **Falsifier-A**: dip 위치가 R_H 와 *상관 없음* (예: dip 이 universal angular scale 에 잠금) — 가설 폐기.
- **Falsifier-B**: dip 이 D_2 더 높은 (homogeneous) 영역의 cluster 에서도 같은 깊이 — 가설 폐기.
- **Falsifier-C**: high-z cluster (z > 1) 에서 dip 더 *깊어짐* (반대 부호) — 가설 폐기.
- **위험-D**: cosmic web fractal claim 자체가 sample-bias artifact (Hogg 2005, Scrimgeour 2012) 라는 반론. R_H 측정 자체의 systematics 가 결론을 흔들 수 있음.
- **위험-E**: σ_0 의 R-의존성을 도입하면 SQMH 의 핵심 단순성(σ_0 = 4πG t_P universal) 이 깨짐. 이는 이론적 비용이 큼 — 도입 정당화는 dip 수치 외 *독립* 데이터 (RSD scale-dependence, weak lensing tomography) 가 추가로 같은 transition 을 가리킬 때만.

## 5. 후속 작업 후보 (이번 세션 범위 밖)

- L474: D_2(R) 관측 자료 (Sylos Labini, Scrimgeour) 디지타이즈 → SQT dip 위치/폭과 cross-plot.
- L475: 8인 팀 자유 도출 — D_2 transition 이 SQMH 동역학 (소멸항 ψ^n) 에 어떻게 들어가는지. 지도 없이 fractal measure ↔ soak rate 만 단서로 제공.
- L476: high-z cluster dip 약화 예측을 SPT-3G / eROSITA cluster 통계로 검증 가능성 평가.

---

요약: cluster dip 은 cosmic web 의 fractal regime 안에 cluster scale 이 *우연히* 박혀있어서 발생한 σ_eff 감쇠로 해석할 수 있고, R_H ≈ 100 Mpc 의 transition 이 dip 의 outer edge 를 강제한다는 것이 본 추측의 핵심.
