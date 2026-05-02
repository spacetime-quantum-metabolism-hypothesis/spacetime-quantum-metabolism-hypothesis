# L407 NEXT_STEP — 8인팀 다음 단계 설계

## 0. L407 simulation 핵심 결과 (재인용)

`results/L407/saddle_distribution.json`:

- 자유 (a, b, c) RG cubic scan 300k:
  - P(saddle ∈ [7.5, 8.0]) = **1.36%**
  - P(saddle ∈ [7.65, 7.85] = ±0.10 of 7.75) = **0.50%**
- Constrained-anchor null:
  - Uniform between cosmic IR (8.37) and galactic UV (9.56) → P(in cluster band) = **0** (구조적)
  - Uniform extended [7.37, 10.56] → 15.7% (cluster band 가 단순히 prior 길이의 일부)
- **구조적 발견**: log σ_cluster (7.75) < log σ_cosmic (8.37). 표준 Wetterich monotone RG cubic-saddle topology (IR < saddle < UV) 와 모순.

→ § 3.1 표의 "Cluster = saddle FP" 해석은 RG topology 와 *불호환*. 두 선택:
- (A) 해석 재배치: cosmic=saddle, cluster=*deeper* IR (또는 별도 FP), galactic=UV
- (B) cubic 단일 RG 가정 폐기, 다단계/multi-coupling RG 또는 비-RG mechanism 으로 환경 의존성 설명

---

## 1. Wetterich Wilsonian truncation 으로 saddle 위치 정량 도출 시도

### 목표
β(σ) = a σ - b σ² + c σ³ 의 (a, b, c) 부호 + 크기 를 Wetterich flow equation 으로 *도출*. 위치 (saddle 의 σ 값) 는 cutoff scale identification 에 종속되므로 *완전* 도출 불가, *sign* 도출은 가능.

### Wilsonian truncation 단계
1. Effective average action Γ_k[σ] in dark-only sector (4 미시축 중 dark-only embedding 기반)
2. Local potential approximation (LPA): U_k(σ) 를 polynomial 까지 truncate
3. Flow equation: ∂_t U_k = (1/2) Tr [(Γ_k^(2) + R_k)^{-1} ∂_t R_k]
4. Anomalous dimension η_σ 1-loop
5. β-function 추출: β(σ) = ∂_t σ_min(t)

### 예상 산출
- (a) sign(b) → monotone vs non-monotone 결정: monotone 기각의 *이론적* 근거
- (b) sign(c) → asymptotic behavior
- (c) saddle 위치는 cutoff Λ_UV/Λ_IR ratio 에 log-의존 → "위치 prior" 는 매우 wide

### 8인팀 평가
- 가능성: 50–70% (Wetterich 형식주의는 표준)
- 비용: ~3–4 주 (LPA + 1-loop + numerical integration)
- 산출 등급: σ₀(env) priori "허용성 → 약 예측" 1단계 향상 (PASS_STRONG 등급 변동 없음)

---

## 2. 1-loop EFT 에서 σ_cluster band 위치 *예측* 가능성

### 목표
dark-only T^α_α coupling 의 1-loop matching 으로 environment-dependent σ₀(ρ_env) 의 1-loop running 추출. cluster ρ_env ≈ 200 ρ_crit 에서 σ_cluster 정량화.

### 단계
1. Tree-level Lagrangian: 4 미시축 (Λ_UV, β_eff, ξ-coupling, conformal-only) 명시
2. 1-loop diagrams: dark-matter vertex correction → effective σ_eff(μ_RG)
3. RG running scale = local ρ_env^{1/4} (dimensional analysis)
4. σ(ρ_cluster) 예측 → 7.75 와 비교

### 예상 결과 (선험적 추정)
- 1-loop running 만으로는 *log-running* 주는데 7.75 ↔ 8.37 (Δ ≈ 0.6 dex = factor 4) gap 은 *power-law* 필요
- 따라서 1-loop EFT 단독으로는 cluster band 직접 예측 부족
- 단, *sign* 예측 (σ_cluster < σ_cosmic) 은 dark-matter loop saturation 으로 가능할 가능성

### 8인팀 평가
- 가능성: 30–50% (sign 만)
- 비용: ~6–8 주 (full diagram + matching)
- 산출 등급: 부분 priori (sign-only). magnitude 는 여전히 anchor.

---

## 3. Holographic argument 로 cluster 영역 자연 emergence

### 목표
σ₀ = 4πG·t_P 가 holographic identity. 환경 의존성 σ₀(env) 를 holographic entropy bound 의 environment-dependent saturation 으로 도출.

### 단계
1. Bekenstein-bound 의 환경 의존: S_max(R, ρ) → σ_env ∝ S_max^{-1}
2. Cluster 영역 = entropy saturation 중간단계 (Page-curve middle)
3. σ_cluster < σ_cosmic 부호 도출 시도

### 8인팀 평가
- 가능성: 10–25% (holographic 환경 의존성은 미정립)
- 비용: ~8 주 이상 (이론 신규 개발)
- 산출 등급: speculative. sign-only 도 어려움.
- **권고**: low-priority future work. P1 + P2 우선.

---

## 4. ★ L407 발견 후속 — base.md §3.1 표 *정정 작업*

cluster anchor 7.75 가 cosmic 8.37 보다 작다. 현재 표 해석 ("Cluster = saddle FP between IR and UV") 은 RG topology 와 정합하지 않음.

### 세 옵션

**옵션 A (해석 재배치)**:
| 환경 | log σ₀ | 새 RG 해석 |
|---|---|---|
| Cluster | 7.75 | deeper IR (또는 second IR FP) |
| Cosmic | 8.37 | saddle FP |
| Galactic | 9.56 | UV FP |

→ cubic β(σ) 가 *두 IR* 를 가지려면 quintic 필요 (5 FP). RG topology 가 더 복잡.

**옵션 B (RG topology 폐기, 비단조 mechanism 외부화)**:
3-regime σ₀ 는 RG flow 가 아니라 *환경별 screening 인자* (예: Vainshtein, chameleon-like) 로 설명. RG 96.8% 호환 narrative 폐기, 다른 mechanism 도입.

**옵션 C (현 표 유지 + caveat 강화)**:
"saddle = cluster" 해석은 *symbolic* 표기 — RG topology 와의 정합은 *future work*. base.md §3.2 ★ 한 줄 추가:
> "★★ saddle 의 *위치*뿐 아니라 cubic-RG topology 적합성 자체도 미입증. cluster < cosmic 부등식 정합성은 quintic-RG 또는 다단계 flow 필요."

### 8인팀 합의: **옵션 C**
- 옵션 A 는 새 가정 추가 (quintic) — 과적합 우려
- 옵션 B 는 96.8% RG 호환 narrative 자가-부정 (이론적 후퇴)
- 옵션 C 는 정직 caveat + future work 우선순위만 격상 — 최소 변경, 최대 honesty
- paper README "Claims status" 7+1 행 의 "RG saddle 96.8% 호환" 표기 옆에 "(★ topology 정합성 future work)" 한 줄 추가 권고

---

## 5. Priority Stack (8인팀 ranking)

| 순위 | 작업 | 산출 | 기간 |
|---|---|---|---|
| 1 | base.md §3.2 ★★ caveat 추가 (옵션 C) | honesty +1 | 즉시 |
| 2 | P1 Wetterich Wilsonian truncation | sign-only priori | 3–4 주 |
| 3 | P2 1-loop EFT matching | sign-only priori | 6–8 주 |
| 4 | §3.7 13-cluster archive joint fit | anchor robustness | 4 주 |
| 5 | P3 holographic | speculative | 8+ 주 (low) |

---

## 6. Honest 결론

**priori 도출은 단기간 (1년) 내 *부분* (sign-only) 만 가능**. magnitude 는 anchor-driven 영구 가능성.

paper/base.md §3.4 caveat **유지가 정직한 baseline**. 강화 항목:
- §3.2 에 ★★ caveat 추가 (cubic-RG topology 정합성도 미입증)
- §6.1 22행 한계 표 row "RG b, c future" 를 row "RG b, c + topology future" 로 확장
- §7 future work 에서 P1/P2 priority 격상

→ REVIEW.md 로.
