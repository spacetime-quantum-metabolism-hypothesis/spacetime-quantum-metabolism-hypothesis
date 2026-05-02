# L333 — Sloppy manifold reparameterization & MBAM-style reduction

> 누적 245 loop, ★★★★★ −0.07, JCAP 91-95%.
> L323 finding: BB 3-param Fisher 의 effective dim ≈ 1, σ_cluster 만 stiff,
>   PR=1.04, κ=100 (anisotropic 100:1:1) / κ=1e4 (log-uniform).
> L324-L332 누적: multi-start global, profile likelihood, TDA 결과
>   모두 "stiff direction 1 + soft 2" 구조와 정합.
>
> L333 질문: BB 가 본질적으로 1-param model 이라면 *그렇게* 재기술하는 것이
> 더 정직하지 않은가? Sloppy combinations 의 *물리* 의미는?
> Manifold Boundary Approximation Method (MBAM, Transtrum-Sethna 2014)
> 적용으로 model 을 자연스럽게 reduce 할 수 있는가?

---

## 0. 동기 (왜 L333 인가)

- L323: PR=1.04 (effective dim ≈ 1 정량). σ_cluster 단일 stretch 가
  geodesic-to-LCDM 의 86~95% 차지.
- L281 marginalized ΔlnZ = 0.8 (= 본질 dof 가 nominal 3 보다 작아서
  Occam 12.2 가 자연스럽게 발생).
- L272 mock 100% false-detection: anchor 만으로 BB 가 "3-regime" 발견 →
  sloppy 방향이 anchor data 의 우연한 패턴을 *포섭* 가능.
- 누적 결론: nominal 3 free param 으로 보고하면 over-claim. *어떤 형태로*
  격하해야 정직한가가 L333 의 직접 과제.

핵심 질문 3종:
- (Q1) BB 의 *stiff* combination 은 어떤 물리량의 함수로 식별되는가?
- (Q2) sloppy 2 자유도는 marginalize 해도 결론이 바뀌지 않는가?
- (Q3) 1-param 으로의 reduction 은 정보 손실인가, 정직 강화인가?

---

## 1. 8인 자율 공격 vectors

A1. **Sloppy spectrum 의 물리 해석** — Fisher eigenvector 를 (σ_cosmic,
    σ_cluster, σ_galactic) 좌표로 사상해 stiff direction 의 *지배적 좌표비*
    측정. 직교화된 nuisance combinations 의 정의 가능성.
A2. **MBAM boundary 식별** — sloppy direction 따라 적분된 geodesic 이
    parameter space boundary (예: σ_galactic → 0, 또는 cosmic↔cluster
    동치한도) 에 도달하는가?
A3. **Reduced 1-param model 의 적합도** — η = stiff projection 만으로
    재구성된 모델이 원 3-param BB 대비 chi² 차이가 AICc 패널티 이하인가.
A4. **Sloppy direction marginalization** — 2 soft 자유도를 marginal 한
    profile evidence 가 nominal Bayesian evidence 와 일치하는가.
A5. **물리 invariance 검증** — η 는 좌표 재선택 (선형/로그 σ) 에 따라
    회전하지만 *방향* 의 물리 의미 (= "가장 잘 결정되는 1 조합")는 유지.
A6. **Boundary stickiness** — MBAM 적분이 boundary 에 도달 후 evaporate
    하는 자유도가 σ_galactic 인지 σ_cosmic 인지 식별.
A7. **L323 와의 정합** — 1D reduced model 의 Fisher eigenvalue 가
    L323 stiff eigenvalue 와 정량 일치하는가 (±0.1 dex).
A8. **격하 vs 보존 결정** — 8인 합의 기준: AICc(1) ≤ AICc(3) − 2 면
    공식 격하, 아니면 "3-param-with-disclosed-sloppiness" 유지.

---

## 2. 자율 분담 (사후 관찰)

토의에서 자연 발생한 분업:
- Fisher eigendecomposition 수치 (L323 Hessian 재사용) — 책임 1.
- Eigenvector → 좌표 사상, dominant component 식별 — 책임 1.
- MBAM-style geodesic ODE (sloppy direction 따라 boundary 까지 적분) — 책임 1.
- Reduced 1-param model 정의 (η = projection) 과 prior 매핑 — 책임 1.
- Profile/marginal evidence 차이 정량 — 책임 1.
- AICc / BIC 패널티 비교, 격하 결정 규칙 — 책임 1.
- 좌표 robustness (linear vs log) 재검증 — 책임 1.
- 논문 narrative 매핑 (Sec 3, Sec 6.2, Sec 6.4) — 책임 1.

8인 위반금지: 수식·파라미터·격하 임계값(2 in AICc 외 표준 통계량) 외 어떤
구체 수치도 ATTACK_DESIGN 에 미주입. 이론적 reduction 형태는 팀이 도출.

---

## 3. 측정 protocol (방향만)

1. 입력: L323 Hessian (case b "100:1:1" 와 case c "log-uniform 1e4:1e2:1"
   대표 두 케이스). 새 finite-diff 재추정도 옵션.
2. Diagonalize → eigenvector v_max (stiff), v_mid, v_min (sloppiest).
3. 좌표 사상: v_max 의 σ_cosmic / σ_cluster / σ_galactic 성분비.
4. MBAM step: θ(τ) = θ* + ∫_0^τ v_min(θ) dτ, θ_i ≥ −cutoff (= LCDM 한계)
   stop. 도달한 boundary 가 어떤 좌표축 방향인지 기록.
5. Reduced model: 원 chi² 를 v_max 1차원으로 사영 → chi²_red(η).
6. AICc(3) = chi²_min + 2·3 + 보정, AICc(1) = chi²_min + 2·1 + 보정.
7. Marginal evidence 비교: nominal 3D Laplace vs 1D reduced Laplace.
8. PASS/FAIL 표는 §4.

---

## 4. PASS / FAIL

- (P1) v_max 의 σ_cluster 성분 ≥ 0.7 (절대값) → "stiff = cluster-dominated"
  명명 정당.
- (P2) MBAM boundary 가 σ_cosmic 또는 σ_galactic 의 LCDM 한계에 도달 →
  격하 후보 자유도 식별.
- (P3) AICc(1) − AICc(3) ≤ −2 → 공식 1-param 격하 권고.
- (P4) Marginal evidence 일치 (|Δ| ≤ 0.5) → marginalize 가 reduce 와 동등.
- (P5) Linear ↔ log 좌표에서 v_max 회전각 < 15° → 좌표 robust.

만족 시: 논문 본문 BB 모델을 "1 stiff combination + 2 sloppy nuisances"
로 재기술. Sec 3 model definition 에 reduction 명시, Sec 6 limitations 에
"3-regime 명명은 phenomenological framing 이며 통계 dof 는 1" 정직 기록.

위반 시 (예: P1 만족 but P3 실패): "sloppy disclosure 유지, 격하 보류"
선택. 등급 영향 −0.005 ~ +0.005 범위.

---

## 5. 위험 / 함정

- Toy Hessian 의존성: L323 와 동일한 한계. 격하 결정은 "toy-Hessian 한계
  하에서" 명시 필수. 실측 likelihood reduction 은 L334+ 에서.
- Reduced 1-param 의 prior 정의: η 의 prior 를 어떻게 induced 하는가
  (uniform on η vs marginal of uniform 3D)? 두 방식 모두 보고.
- MBAM 의 boundary 가 numerical artifact 인지 진짜 model degeneracy 인지
  구분: cutoff 의존성 sweep 필수.
- "물리 의미" 의 over-interpretation: stiff direction 이 σ_cluster 라
  해서 "cluster scale 이 본질" 이라 단정 금지. *데이터가 그 1 축을 가장 잘
  제약* 한다는 통계적 사실일 뿐.
- Code: `np.linalg.eigh` 는 정렬 보장 X — 명시적 argsort 필수. log10 좌표
  변환 시 σ=0 한계 cutoff 통일.

---

## 6. 8인 위반금지 점검

- 수식: Fisher / AICc / Laplace 표준 정의 외 미주입.
- 파라미터: stiff/soft 비율 가정 미주입 (L323 출력 그대로 사용).
- 격하 임계값: AICc Δ=2 (Burnham-Anderson 표준) 외 미주입.
- 이론 reduction 형태: 팀이 v_max 사상에서 자율 도출.
