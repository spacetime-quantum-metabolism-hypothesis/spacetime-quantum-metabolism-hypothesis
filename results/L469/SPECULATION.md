# L469 — SQMH n field 의 Plasma-analog Debye Screening 추측

**Status**: 자유 추측 (free speculation). 검증 안 됨. 이론 도출 아님.
**Date**: 2026-05-01

## 1. 동기 (motivation)

- L46x 시리즈에서 σ_0 (n field 자기상호작용 강도) 가 **cluster scale (~1 Mpc)
  에서 약화** 되는 "cluster dip" 패턴이 반복 관측됨.
- Cluster scale 에 *고유 길이* 가 자연적으로 나타날 메커니즘 필요.
- 추측: **n field 가 plasma 처럼 Debye screening 을 가진다**.
  이 경우 Debye 길이 λ_D 가 cluster scale 에 일치하면 dip 자동 설명.

## 2. Plasma analog 매핑

표준 plasma Debye 길이:

>   λ_D^plasma = sqrt( ε_0 k_B T / (n e²) )

SQMH n field 매핑 (free guess):

| Plasma 변수 | SQMH 대응 |
|---|---|
| k_B T (열에너지) | ε  (n field 의 "thermal/elastic" 척도) |
| n (수밀도) | n_∞ (n field VEV) |
| e² (커플링²) | σ_0 (n 자기상호작용 / SQMH coupling) |
| ε_0 (진공 유전율) | 1 (자연 단위, 또는 O(1) factor) |

→ **λ_D^SQMH ≡ sqrt( ε / (σ_0 · n_∞·μ) )**

## 3. 정량 (toy run)

CLAUDE.md 규칙 `n_∞·μ = ρ_Planck / (4π) ≈ 4.10×10⁹⁵ kg/m³` 를 고정.
ε 와 σ_0 를 (J, m⁵ kg⁻¹ s⁻²) 광범위 스캔.

### 3.1 λ_D = 1 Mpc 매칭선

`results/L469/lambda_D_scan.png` 의 빨간 contour.
log-log 평면에서 **직선** (단순 차원 관계 때문):

>   log σ_0 = log ε − 2 log(R_cl) − log(n_∞μ)

→ R_cl = 1 Mpc 고정시 σ_0 ∝ ε 의 **slope-1 직선** 위 어디든 OK.
즉 toy 는 (ε, σ_0) 둘 다 자유로워 *예측력은 낮음*. **자기 충족 가능 영역
존재** 만 확인.

### 3.2 ε ~ k_B T_CMB 가정시

ε = k_B · 2.725 K = 3.76×10⁻²³ J 라면

>  σ_0 ≈ 1.2×10⁻¹⁶⁴ m⁵ kg⁻¹ s⁻²    (λ_D = 1 Mpc 매칭)

물리적으로 *극히 작은 결합* — 이게 SQMH 어떤 코어 결합 (G, σ=4πG t_P,
psi^n 등) 과 연결되는지 보려면 추가 작업 필요.

### 3.3 Cluster dip 역추정

관측 dip ~30% 가정시 (가정값, 실제 L46x 깊이로 교체 필요):

>   exp(−1 Mpc / λ_D) = 0.70   ⇒   **λ_D ≈ 2.8 Mpc**

→ "30% dip @ 1 Mpc" 는 **λ_D 가 cluster scale 의 ~3 배** 임을 시사.
(dip 깊이 ↑ ⇒ λ_D ↓.)

### 3.4 Screening profile

`screening_profile.png` 와 results.json:

| r | σ(r)/σ_0  (λ_D=1 Mpc) |
|---|---|
| 10 kpc (galaxy core)  | 0.99 |
| 100 kpc (galaxy halo) | 0.90 |
| 1 Mpc (cluster)       | 0.37 |
| 10 Mpc (supercluster) | 4.5×10⁻⁵ |
| 100 Mpc               | ~0 |
| 1 Gpc                 | 0 |

→ **galaxy 내부는 거의 영향 無, cluster 에서 substantial dip,
supercluster 이상은 σ 사실상 0**. 이 패턴은 정성적으로
- BAO scale (~150 Mpc) 에서 σ 가 사라지는 것
- 우주론적 평균에서는 σ_0 이 약하게 들어가는 것

과 어느 정도 부합 가능 (toy 수준).

## 4. 가능성 / 한계

### 가능성 (왜 추측할 가치)
- Cluster scale 의 *고유 길이* 를 도입할 자연스러운 메커니즘 (plasma 와
  형식적 닮음).
- Yukawa-screening form 은 GR-수정 / coupled DE 모델에서 흔하므로
  hi_class / EFT-of-DE 와 접속 가능.
- σ_0 의 scale-dependence 가 자동으로 BAO < cluster < cosmic 에서 다른
  값을 낼 수 있음 → L46x cluster dip 의 **구조적 설명 후보**.

### 한계 (왜 즉시 채택 불가)
- (ε, σ_0) 둘 다 자유 → toy 는 **사실상 1자유도 redundancy** 가 있어
  λ_D 자체가 자유 파라미터. 독립 예측 없음.
- Plasma 의 ε_0, k_B 같은 dimensional anchor 가 SQMH 에는 *유도되지 않음*.
  ε 의 미시 정의 (어떤 양자장 에너지?) 가 빠져 있음.
- exp(−r/λ_D) 는 *정적 점원* 의 linearised Yukawa. 우주론적 cluster scale
  에서는 비선형 + 시간 의존성 필요.
- Cassini PPN 위반 가능성: 만약 Sun 주변에서 λ_D > AU 면 σ 가 PPN 에
  새고, dark-only 분리 (C10k 패턴) 필요.

## 5. 다음 액션 (제안만, 자동 실행 X)

1. **ε 의 미시 정의** 시도: ε = ⟨(∂_t n)² / n⟩ ~ H² · μ · (n_∞μ) 같은
   SQMH 동역학량과 연결.
2. **σ_0 의 SQMH 코어 매핑**: σ_0 ∝ G·t_P^k · μ^m 형태로 차원 잠금 시도.
   잠그면 λ_D 가 *예측*이 됨 (자유도 0).
3. **L46x cluster dip 의 실제 깊이/스케일 측정** → λ_D 역추정 후 위 매핑과
   일관성 확인.
4. **Static Yukawa 한계 너머**: Bessel-K screening (cosmological), time-domain
   plasma oscillation analog (n field 의 plasmon-like mode) 탐색.
5. **PPN 안전성**: Sun 주변 λ_D ≪ AU 또는 dark-only sector 분리 확인 필수.

## 6. 결론 (한 줄)

> n field 의 Debye-analog λ_D 가 cluster scale 과 일치하도록
> (ε, σ_0) 가 잠긴다면 cluster dip 은 자동 설명되지만, **현재 toy 는
> ε 와 σ_0 둘 다 자유 → 자기 충족 영역 존재 만 확인**. 다음 단계는
> ε 또는 σ_0 의 SQMH-내적 dimensional locking.

## Outputs

- `results/L469/lambda_D_scan.png`  — (ε, σ_0) plane 의 log λ_D 등고선
- `results/L469/screening_profile.png` — σ(r)/σ_0 = exp(−r/λ_D)
- `results/L469/results.json` — 수치 요약
- `simulations/L469/run.py` — toy 코드
