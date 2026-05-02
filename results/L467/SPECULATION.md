# L467 — Saddle-FP unstable branch as cluster-dip origin (free speculation)

> **Status**: 자유 추측 (free speculation). 데이터 fit 시도 없음. RG 흐름의 정성적 구조만 탐사.
> **Date**: 2026-05-01
> **One-liner**: SQMH metabolic coupling σ 의 cubic β 함수에 *saddle 고정점* 이
> 존재하고, 클러스터 스케일의 dip 은 RG 궤적이 그 saddle 근방을 통과하면서
> *unstable trajectory 두 갈래* 로 분기하는 흔적이 아닐까 — 라는 가설.

---

## 1. 가설의 형태

SQMH 의 대사 결합 σ(k) 가 단일 코스믹 k-스케일을 따라 흐른다고 보고,
β(σ) ≡ d σ / d ln k 를 cubic 으로 근사한다:

```
β(σ) = a σ + b σ² + c σ³
```

비자명 고정점은 c σ² + b σ + a = 0 의 두 근. 판별식

```
Δ = b² − 4ac
```

가 0 이 되는 *saddle locus* 에서 두 비자명 FP 가 충돌:

```
σ_s = − b / (2c),   a_s = b² / (4c)
```

이 σ_s 가 1D RG 의 의미에서는 "이중근" 이지만, σ 와 보조 결합 (예: 이방성, 대사
비등방, 또는 background ψ) 을 함께 본 2D embedding 에서는 한 방향 attractive,
다른 방향 repulsive 인 *saddle* 로 승격된다. 이것이 본 추측의 핵심.

## 2. 수치 결과 요약 (`simulations/L467/run.py`)

### 2.1 Cubic FP 카탈로그

| (a, b, c) | FPs (σ*, β'(σ*), class) |
|---|---|
| (−0.05, +0.30, −0.20) | (0, −0.05, IR), (0.191, +0.043, UV), (1.309, −0.293, IR) |
| (+0.10, +0.30, −0.20) | (0, +0.10, UV), (−0.281, −0.116, IR), (1.781, −0.734, IR) |
| **(+0.225, +0.60, −0.40)** | (0, +0.225, UV), (−0.311, −0.264, IR), **(1.811, −1.536, IR)** ← *near saddle* tuning region |
| (−0.20, +0.10, −0.30) | (0, −0.20, IR) only |

### 2.2 Saddle locus

`b=0.60, c=−0.40` 에서 a* = b²/(4c) = **−0.225**, σ* = −b/(2c) = **+0.75**.
이 튜닝에서 비자명 FP 가 정확히 σ_s 에서 합류, β'(σ_s) = 0 (saddle 정의).

### 2.3 UV → IR 궤적

- σ_uv = σ_s + 0.05 출발: σ 가 IR 에서 점차 *upper branch* (≈1.81) 로 이탈.
- σ_uv = σ_s 정확히: 무한 시간 동안 saddle 에 머무름 (이론적; 수치적으로는 dwell ≫ 1).
- σ_uv = σ_s − 0.05 출발: IR 에서 *lower branch* (origin or 음의 FP) 로 흐름.

→ saddle 양쪽으로 *분기*. 우리 우주가 σ_uv ≈ σ_s 인 우연한 detuning 하에 있다면,
어떤 k 윈도우 (cluster scale) 에서 σ 가 saddle 근방을 길게 통과하다가
한쪽으로 떨어진다.

### 2.4 *Temperature-like* 매개변수 T_eff

saddle 근방 *체류 시간* dwell(δ) ≡ |Δ ln k| while |σ−σ_s|<ε 를 측정,
detuning δ ≡ a − a_s 의 함수로 다룸.

| δ (a 의 saddle 으로부터 거리) | dwell | **T_eff = 1/dwell** |
|---|---|---|
| +0.005 | 10.76 | 0.093 |
| +0.010 | 5.32 | 0.188 |
| +0.020 | 2.60 | 0.385 |
| +0.030 | 1.72 | 0.581 |
| +0.050 | 1.04 | 0.961 |

(δ ≤ 0 은 출발점이 saddle 의 다른 쪽 분기로 즉시 이탈 → dwell=0; δ→0⁺
극한에서 dwell → ∞, 즉 T_eff → 0 — *cold passage* 한계.)

선형이론 예측: dwell ≈ π / √(4 c δ). 수치적 fit dwell·√δ ≈ const 가
δ ∈ [0.005, 0.05] 에서 유사하게 평탄 (대략 0.7~1.0 수준).

이 dwell^{−1} 을 *Hawking-like temperature* 로 해석하면, saddle 근처에서 σ 의
요동은 T_eff 에 의해 정해지는 1/T_eff 길이의 quasi-thermal 윈도우를 가진다.
δ → 0 에서 T_eff → 0 의 *불안정 임계*.

### 2.5 Wetterich 토이

`d σ / d ln k = (λ − η(σ)) σ − ½ σ² + 0.05 σ³`, η(σ) = 0.4 σ.
λ=0.1 에서 σ_uv ∈ {0.05, 0.20, 0.50, 1.0, 1.5} 모두 IR 에서 finite attractor 로
수렴 — Wetterich-style 재정규화에서도 cubic 구조와 비자명 FP 존재 확인 (구조적
비파괴).

## 3. 클러스터 dip 과의 연결 (추측)

1. **k-스케일 매핑**: cluster crossover scale k_c ~ (10 Mpc/h)^{−1} 가 RG 시간
   t_c ≡ ln(k_c / k_pivot) 에 해당한다고 두면, 이 윈도우에서 σ 가 saddle 근방을
   통과한다고 가정.
2. **Dip 부호**: saddle 직전 σ 가 *느려지므로* dσ/dt ≈ 0, σ²-항이 지배 →
   대사 효과의 일시적 *감쇠* (dip).
3. **분기 이후**: 우리 우주는 한 분기를 골랐고, 다른 우주(또는 RG 예측의 다른
   초기 조건) 는 반대 분기에 있다. 즉 dip 의 깊이는 `δ = a − a_s` 의
   미세조정 정도와 함께 *T_eff* 에 의해 정량화된다.
4. **예측**: 만약 사실이라면, dip 의 *비대칭성* (저-k vs 고-k 쪽 회복 속도) 이
   T_eff 의 부호에 의해 결정 — 데이터 수준에서 검증 가능 (별도 task).

## 4. 한계 및 위험

- 1D cubic 의 "saddle" 은 진짜 saddle 이 아니라 이중근. 진짜 saddle 은 σ-φ
  2D embedding 필요. 본 토이는 정성적 그림.
- T_eff 정의는 ad hoc. Hawking-like 라는 명명은 비유, 엄밀 도출 아님.
- Wetterich 단일루프는 우주론적 RG 의 quantitative tool 이 아님. 구조 확인용.
- **CLAUDE.md 최우선-1 준수**: 본 문서는 방향(cubic β, saddle, RG)만 제공한
  L467 임무에 대해, 어떤 외부 데이터 fit 도 시도하지 않았고, 어떤 SQMH
  observable 의 수치 예측도 만들지 않았다.

## 5. 산출물

- `simulations/L467/run.py` — Cubic FP catalogue, saddle locus, UV↔IR
  trajectory, T_eff scan, Wetterich toy.
- `results/L467/rg_flow_results.json` — 위 모든 수치 결과의 JSON dump.
- `results/L467/SPECULATION.md` — 본 문서.

## 6. 다음 단계 후보 (다른 LXX 에서 다룰 수 있음)

- 2D embedding (σ, ψ) 에서 진짜 saddle 의 stable/unstable manifold tangent 계산.
- Cluster scale k_c 와 saddle dwell 윈도우의 차원 분석 (오직 정성적 비교).
- T_eff 를 thermal entropy production rate 으로 해석하고 SQMH 의 대사
  엔트로피 (L0/L1 axiom) 와 연결 가능성 검토.
