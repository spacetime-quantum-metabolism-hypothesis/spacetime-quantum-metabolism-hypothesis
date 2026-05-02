# L462 SPECULATION — cluster σ₀ dip 의 critical phase transition 가설

> **위상**: 자유 추측 (free speculation). 본 문서의 어떤 수치도 SQMH 핵심 예측에
> 들어가지 않으며, 후속 팀 토의에서 *방향성 입력* 으로만 사용 가능하다.
> CLAUDE.md [최우선-1] 준수: 팀에 사전 지도 (수식, 파라미터 값) 를 *강제* 하지 않으며,
> 아래 toy expression 들은 모두 phenomenological placeholder 이다.

작성: 2026-05-01 · 임무: L462 자유 추측

---

## 0. 출발점 (관측된 정황)

이전 L4xx 라인에서 cluster ρ ∼ 10⁻²⁶ kg/m³ 영역에서 σ₀ (n field 결합 강도) 가
국지적으로 *깊어지는* 현상 (이하 "σ₀ dip") 이 시뮬레이션에서 반복 관찰되었다.
지금까지의 작동 fit 은 V-shape (in log ρ) 였으나, 이것이 **유일한** 모양일
이유는 없다. 본 추측은:

> **σ₀ dip 은 n-field 의 Z₂ 대칭 자발 깨짐 (SSB) 가 cluster 평균밀도 근방에서
> 임계점 (critical phase transition) 을 통과하기 때문이다.**

라는 가설을 자유롭게 탐색한다.

---

## 1. Dimensional argument: 왜 ρ_c ∼ 10⁻²⁶ kg/m³ 가 "특별" 할 수 있는가

n-field 가 Planck 스케일 UV 이론 (ρ_P ≈ 5.2×10⁹⁶ kg/m³) 과 우주론 IR 스케일
(ρ_crit0 ≈ 8.5×10⁻²⁷ kg/m³) 사이의 어떤 RG flow 의 *고정점* 에 앉아 있다고 하자.
두 스케일의 dimensionless 비는

  ρ_P / ρ_crit0 ≈ 6×10¹²² (cosmological constant 문제의 본 모습)

순수 dimensional 조합 후보 (toy 추정):

| 조합                              | 값 [kg/m³]  |
|-----------------------------------|-------------|
| ρ_P                               | 5.2×10⁹⁶    |
| ρ_crit0                           | 8.5×10⁻²⁷   |
| 200·ρ_crit0 (virial overdensity)  | 1.7×10⁻²⁴   |
| (ρ_P · ρ_crit0)^(1/2)             | 2.1×10³⁵    |
| ρ_P^(1/3)·ρ_crit0^(2/3)           | 7.2×10¹⁴    |
| ρ_P^(1/4)·ρ_crit0^(3/4)           | 4.2×10⁴     |

**관찰**: ρ_crit0 자체가 (그리고 그 ×200 배인 cluster virial 평균이) "10⁻²⁶ ∼ 10⁻²⁴
kg/m³" 대역의 두 끝을 정확히 둘러싼다. 즉:

> **ρ_c ≈ ρ_crit0** 또는 **ρ_c ≈ Δ_vir·ρ_crit0** 라는 *동시적* identification 이
> 자연스럽다.

후자가 맞다면 이는 단순히 "오늘 우주의 평균밀도" 라는 우연이 아니라 **구조 형성
임계 (collapse threshold)** 와 n-field 임계점이 *같은* 스케일을 공유한다는 뜻
이고, 이는 SQMH 의 metabolism ↔ collapse 결합과 정합성이 있다.

또 하나 흥미로운 우연:

  ρ_P · t_P² = 1/(4πG) (자연단위 in plane), 그리고 cluster crossing time
  τ_cross ∼ 1 Gyr ≈ 6×10⁵⁹ t_P 의 inverse-square 가
  ρ_P / τ_cross² ∼ 10⁻²³ kg/m³ 정도로 떨어진다.

이는 "Planck density 를 cluster dynamical time 으로 dilute 한 값이 cluster
virial 밀도 근방" 이라는 (취약하지만) 차원적 짝맞음을 준다. **검증 가능 path:**
다른 dynamical time (galaxy ∼ 100 Myr, void ∼ 10 Gyr) 에서 dip 위치가 τ⁻²
스케일링으로 이동하는지 본다.

---

## 2. Universality class 후보

n-field 가 Z₂ 대칭 (n ↔ −n) 을 가정한다면 가장 자연스러운 후보:

| class           | d  | order param      | ν     | β     | γ     | η      |
|-----------------|----|------------------|-------|-------|-------|--------|
| mean-field      | ≥4 | scalar           | 0.500 | 0.500 | 1.000 | 0.000  |
| 3D Ising        | 3  | Z₂ scalar        | 0.630 | 0.326 | 1.237 | 0.036  |
| 3D XY           | 3  | U(1) (vector 2D) | 0.671 | 0.349 | 1.318 | 0.038  |
| 3D Heisenberg   | 3  | O(3) vector      | 0.711 | 0.366 | 1.396 | 0.037  |

**판별 path** (8인 토의에서 자유 도출하길 권장하는 *방향*):

1. **공간 차원**: cluster 환경이 "3D bulk" 인지 "filament 의 quasi-2D core" 인지에
   따라 effective d 가 달라진다. 2D Ising 은 ν=1 (정확) 로 distinct.
2. **n field 표현론**: Z₂ 단일 → Ising. complex n field (phase 자유도) → XY.
   isospin-like O(3) → Heisenberg.
3. **Long-range vs short-range**: 만약 n-field 결합이 1/r^(d+σ) 형태 long-range
   라면 LR-Ising 가 따로 와서 ν 가 σ 의존.
4. **mean-field 회귀 조건**: upper critical dimension d_uc=4 이상 또는 fluctuation
   이 작은 한계 (n_field 가 다체 결합 → Ginzburg criterion 깨짐) 면 MF 회귀.

SQMH 의 metabolism 메커니즘은 비국소 (소멸항 ∝ ρ) 이므로 **long-range 로 의심
되며**, 이 경우 effective ν 가 short-range Ising 과 다를 수 있다 — 이것이
"V-shape" 가 잘 작동했던 이유의 한 후보일 수 있다 (3절 참조).

---

## 3. Critical exponent 가 dip 모양을 정량 예측하는가

phenomenological dip 모양을 두 family 로 비교:

- **(A) V-shape**: σ₀(ρ) = a + b·|log₁₀(ρ/ρ_c)|
  → 커스프 (cusp) at ρ_c, 양 측 logarithmic.
- **(B) Critical scaling**: σ₀(ρ) = a − b·|1 − ρ/ρ_c|^ν
  → ν<1 이면 cusp, ν=1 이면 V (linear), ν>1 이면 smooth.

`simulations/L462/run.py` 결과:

- 9개 측정점 (ρ ∈ 10⁻²⁸..10⁻²⁴, 2% 정밀도) 에서 **mean-field (ν=0.5) 와
  3D-Ising (ν=0.630) 의 χ² 차이가 ~10⁵ 수준** (수백 σ). 즉 **충분한 정밀도가
  확보되면 universality class 가 직접 측정 가능**.
- "V-shape mock data 를 critical 모양으로 fit" 했을 때 best mimicking ν 는
  grid 끝 ν=0.2 로 박힘 → V-shape 는 critical 모양으로 보면 **logarithmic
  singularity (ν→0⁺)** 에 가장 가깝다. 이는 2D Ising 의 specific heat 가
  log 발산하는 경계 사례와 형식적으로 같은 자리.

**해석 (자유 추측)**:

1. 만약 실제 n-field 가 **2D-like effective dimensionality** 를 가진다면
   (예: cluster sheet/filament 위에 n field 가 갇힘) → ν→0⁺ log 거동이
   자연스러우며 V-shape 가 *근본 모양* 이 된다.
2. 만약 진짜 3D-Ising 이라면 ν=0.630 → dip 이 V 보다 약간 *덜 뾰족*. 현재
   simulation 으로는 이 차이가 보일 만큼 정밀하지 않아서 "V" 로 fit 됐을 가능성.
3. mean-field (ν=0.5) 는 V 보다 더 둥근 dip → 향후 cluster 표본 확장 시 dip
   바닥의 곡률로 구분 가능.

---

## 4. ρ_c 가 cluster 영역과 일치할 수 있는 *동역학적* 이유

순수 차원 일치는 우연일 수 있다. 비-우연일 후보 메커니즘 (방향만 제시):

1. **Friedmann 결합 RG**: n-field self-coupling λ(ρ) 의 beta 함수가 ρ ≈ ρ_crit0
   근방에서 0 을 가지면 그 자리에서 SSB 임계가 일어남. 우주가 어떤 era 에서든
   ρ_crit(t) 를 통과하므로 "현재의 ρ_crit0" 은 단순히 "지금 우리가 보는" 상호
   교차점.
2. **Holographic IR cutoff**: de Sitter horizon volume 안의 평균 에너지밀도가
   ρ_crit0 인 것은 자명. n-field 가 horizon-bounded mode 만 본다면 임계는
   horizon 밀도에 자동 lock.
3. **Cluster as nucleation seed**: virial collapse 가 첫 번째로 ρ ≫ ρ_crit0 를
   만들면 그 경계 (cluster outskirt) 에서 n-field 가 broken ↔ unbroken 의
   *phase boundary* 를 가로지른다 → dip 은 phase boundary 의 잔향.

3번이 가장 falsifiable: **cluster outskirts (virial radius 1∼2배) 에서 dip 이
가장 깊고, 중심부 (ρ ≫ ρ_c) 와 void (ρ ≪ ρ_c) 양쪽에서 동시에 옅어져야 함.**
현재 관측이 이 비대칭을 검증할 수 있는지가 즉시 가능한 다음 단계.

---

## 5. 즉시 가능한 후속 검증 path

자유 추측이지만 *어떻게* 검증할지는 가능한 한 구체적으로:

| 단계 | 행동 | 산출 |
|------|------|------|
| P1 | 기존 cluster σ₀ 측정 grid 에서 V-shape 와 ν=0.5/0.63/0.71 critical 모양 chi² 비교 | model selection ΔAICc |
| P2 | dip 깊이의 redshift 의존성 (ρ_crit(z) 추적) — 임계가 동시 이동하는지 | locking test |
| P3 | filament vs node 환경 분리 분석 (effective d 변화) | 2D-like vs 3D-like ν 분기 |
| P4 | n-field 가능 후보 Lagrangian 후보군에서 RG β 함수 자유 도출 (8인 팀, 지도 없이) | universality 예측 |
| P5 | mean-field 회귀 조건 (Ginzburg criterion) 수치 평가 | MF 정당성 |

---

## 6. 위험 / 자기비판

- **우연 가능성**: 200·ρ_crit0 ≈ 1.7×10⁻²⁴ 는 "cluster 정의" 가 정확히 그
  overdensity 로 잡힌 것이라 *동어반복* 위험. 진짜 비-우연이려면 **cluster
  정의와 무관한 다른 환경 (큰 isolated halo, void wall) 에서도 같은 ρ_c 가
  나와야** 한다.
- **L33 적분 버그 같은 함정 재발 우려**: critical scaling 은 ρ→ρ_c 근방에서
  수치 발산. 추후 fit 시 |ρ−ρ_c|<ε 영역의 cutoff 를 명시하지 않으면 chi²
  과소평가/과대평가 양쪽 위험.
- **universality 주장은 보편적이지 않다**: n-field 가 만약 1차 상전이를 한다면
  ν 자체가 정의되지 않고 latent heat 와 metastability 가 본질. dip 모양도
  step-like 가 되어야 하는데 현재 V-shape 는 그쪽이 *아니다*. 즉 *2차* SSB
  가정이 들어 있다는 점을 명시.
- **수식 placeholder**: 본 문서의 형태들은 이론에서 도출된 것이 아니다.
  팀 자유 도출 시 본 문서를 *지도* 로 사용하면 [최우선-1] 위반.

---

## 7. 한 줄 결론 (추측)

> **σ₀ dip 의 V-shape 는 n-field SSB 의 *2D-like (log-divergent) 임계* 그림자이고,
> ρ_c ≈ ρ_crit0·(1∼Δ_vir) 의 일치는 우주의 horizon density 와 n-field RG 고정점이
> 같은 곳에 있기 때문이라는 가설은 ν 정밀 측정으로 향후 falsify 가능하다.**

산출물:
- `simulations/L462/run.py` — V-shape vs critical toy + ν fit landscape
- `simulations/L462/shape_compare.png` — 모양 비교 그림
- (본 문서) `results/L462/SPECULATION.md`
