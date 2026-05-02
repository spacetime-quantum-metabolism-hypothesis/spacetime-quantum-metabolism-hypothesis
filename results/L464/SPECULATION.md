# L464 — Free Speculation: τ_q × cluster anti-resonance

> **상태**: 자유 추측 (free speculation). 이론 도출 아님, 직관 탐색용 토이.
> CLAUDE.md 최우선-1 규칙에 따라 본 문서의 토이 수식은 phenomenological
> placeholder 이며 SQMH 공리 도출이 아님을 명시한다.

## 1. 가설 한 줄

cluster 스케일 dip (관측에서 보고되는 ~Mpc 영역 power 결손)이 **τ_q (Planck time)
와 cluster 동역학 시간 사이의 anti-resonance** — 즉 빠른 micro-driver 의 stochastic
spectrum 이 cluster 대역에서 destructive interference 를 일으키기 때문이라는 추측.

## 2. 시간 척도

| 양 | 값 |
|---|---|
| τ_q (Planck time) | 5.39 × 10⁻⁴⁴ s |
| t_cluster_cross (R~1 Mpc, σ~10³ km/s) | ~1 Gyr ≈ 3.16 × 10¹⁶ s |
| t_cluster_dyn (M~10¹⁵ M⊙) | ~2.5 Gyr ≈ 7.89 × 10¹⁶ s |
| t_H | ~14.4 Gyr ≈ 4.55 × 10¹⁷ s |
| **log₁₀(t_cluster_dyn / τ_q)** | **≈ 60.17** |
| log₁₀(t_H / τ_q) | ≈ 60.93 |
| log₁₀(t_cluster / t_H) | ≈ −0.76 |

핵심 관찰:
- τ_q 와 cluster 시간 사이에 **약 60 decade** 의 스케일 갭. resonance/anti-resonance
  를 직접 시뮬레이션하기엔 dynamic range 가 너무 큼 → coarse-graining (stochastic
  averaging) 이 필수.
- cluster 시간 ≈ 0.17 × t_H. 두 거시 모드 (Hubble vs cluster) 는 동일 자릿수에 있고,
  micro mode (τ_q) 는 그보다 60 decade 빠름.

## 3. Anti-resonance 메커니즘 후보

**(a) Two-mode destructive interference.**
거시 응답이 두 oscillator (ω_H ≈ 1/14 Gyr⁻¹, ω_cl ≈ 0.4 Gyr⁻¹) 의 합성으로 표현
가능하다고 가정. 두 모드가 **반대 위상 (mix = −1)** 으로 driver 에 결합하면 두
자연주파수 사이에서 응답에 dip 발생 가능. 토이 결과: 두 자연주파수 사이 내부에서
ω_dip ≈ 0.29 Gyr⁻¹ 근처에 응답 변형이 나타나지만, **이 좁은 band 에서 destructive
응답은 constructive 대비 ~5.3 배 *증폭됨*** (반-위상 합성이 두 자연주파수 사이에서
여전히 보강될 수 있음). 즉 *순수 두-모드 destructive coupling 만으로는 cluster dip
설명이 자연스럽지 않다.* (정직한 음성 결과)

**(b) Spectral hole in micro driver.**
τ_q 척도의 micro driver 가 white-noise-like 하지 않고 **cluster 대역에 spectral
hole 을 갖는다**고 가정. Stochastic averaging (Bogoliubov-Mitropolsky) 적용 시
slow-mode variance ⟨A²⟩ ∝ S(ω_slow)/(γω_slow²). hole 깊이 0.7, log-width 0.5 인
토이에서 cluster 대역 ⟨A²⟩ 가 reference 대비 **~0.90 배** 까지 억제됨.
관측되는 cluster dip 깊이를 재현하려면 더 깊은 spectral hole 또는 추가 채널 필요.

**(c) Phase-coherence 손실.**
τ_q 단위로 시간이 양자화된 메트릭 (SQMH 의 "공간시간 양자" 가설)에서, cluster
crossing time 이 τ_q 의 **정수배가 아닌 영역** 에 시스템이 머무르면 위상 정보가
diffuse 해서 long-range correlation 이 억제될 수 있음. 이는 spectral hole 을
효과적으로 만드는 미시 메커니즘 후보.

## 4. Stochastic averaging 논변 (heuristic)

빠른 driver ξ(t) 가 시간 척도 τ_q, slow mode q(t) 가 시간 척도 t_cl 일 때,
방정식
  q̈ + γ q̇ + ω_cl² q = ξ(t)
의 long-time variance 는
  ⟨q²⟩ = (1/2γω_cl²) S_ξ(ω_cl) ,
즉 micro spectrum 의 cluster 주파수 값에 비례. 따라서 **cluster dip ⇔ S_ξ(ω_cl)
의 dip**. 이것이 본 추측의 핵심 등가관계.

이 등가는 *미시 spectrum 의 cluster-band hole 의 기원* 으로 문제를 옮긴다.
SQMH 맥락에서는 (i) anti-resonance 결합 그래프, (ii) 위상 양자화의 commensurability
(arithmetic gap), (iii) 대사항 (metabolism rate) 의 cluster-band 부재, 같은
정성적 후보가 있으나 *모두 본 단계에서는 이름뿐*. 도출은 별개 작업.

## 5. 토이 시뮬레이션 결과 (`simulations/L464/run.py`)

- Two-mode coupled oscillator: destructive mix 가 cluster band 에서 자동 dip 을
  생성하지 않음 (suppression_ratio ≈ 5.3, 즉 *증가*). Anti-resonance 는 단순
  반-위상 결합만으로 부족.
- Stochastic averaging + spectral hole: cluster 대역 ⟨A²⟩ 비율 0.90 (10% 억제).
  hole 깊이/너비 튜닝으로 더 큰 dip 가능하지만 ad hoc.
- 결론: 본 토이는 *anti-resonance 자체가 cluster dip 을 자동 산출하지 않음* 을
  보여줌. 추가 구조 (sector-selective coupling, phase quantisation 등) 없이는
  cluster dip 의 자연스러운 origin 으로 채택 불가.

## 6. Falsifiable 예측 후보 (only direction names)

- **Power spectrum dip 의 위치 vs 적색이동**: anti-resonance 라면 redshift 진화
  (clustering scale 변화) 가 dip 위치를 이동시켜야 함.
- **Mass-dependence**: cluster 동역학 시간이 M 에 의존 (∝ ρ⁻¹/²) → dip 깊이가
  cluster mass bin 에 따라 변할 가능성.
- **Cross-spectrum phase**: 두 모드 destructive coupling 이라면 galaxy-galaxy 와
  matter-matter cross-spectrum 의 위상이 cluster 대역에서 reverse 되어야 함.

이상은 "탐색 방향"의 이름일 뿐이며, 본 추측을 정량 이론으로 격상하려면 별도
도출 단계가 필요.

## 7. 한계 / 정직한 기록

- cluster dip 의 관측 신호 자체에 대한 인용은 본 문서에 포함하지 않음 (자유 추측
  단계). 후속 단계에서 source 데이터 (CMB lensing × cluster, kSZ, weak lensing
  3pt 등) 와 정확한 dip 정의 필요.
- L33/L34 등 BAO 분석과는 무관. SQT background 결과를 cluster 채널로 옮기지 않음.
- 본 토이에서 destructive mix 가 dip 을 만들지 못한 결과는 "가설 기각" 이 아니라
  "단순 토이 부족" 으로 해석. 다음 단계에서 sector-selective 결합 구조 또는
  phase-quantisation toy 로 확장하는 것이 자연스러운 후속.
