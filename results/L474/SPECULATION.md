# L474 Free Speculation — Non-Markovian Memory Backflow Hypothesis

비-마르코프 n-필드 메모리 커널이 cluster timescale 에서 backflow 를 일으켜 σ_0 를 약화시킨다는 가설.

---

## 1. Core Idea (한 줄)

**SQMH n-필드의 metabolic "소화" 가 즉시 완료되지 않고 유한한 시간 τ_mem 만큼 지연 응답한다면, cluster scale (L_cl ~ 1–10 Mpc, t_cl ~ τ_mem) 에서 응답함수가 음의 lobe (backflow) 를 가지면서 effective σ_0 (소멸/유입 단면적) 이 cluster 환경에서 부호 반전 또는 진폭 축소된다.**

---

## 2. Schwinger-Keldysh Framework

### 2.1 Closed-time-path 액션

n-필드를 환경 (vacuum bath) 와 접촉한 open quantum system 으로 보면, SK CTP 액션:

```
S_eff[n_+, n_-] = S_cl[n_+] - S_cl[n_-] + i ∫dt dt' n_-(t) K(t-t') n_-(t')
                                        + ∫dt dt' n_-(t) Σ_R(t-t') n_+(t')
```

- `Σ_R(t-t')` = retarded self-energy (memory kernel)
- `K(t-t')` = noise kernel (FDT 로 Σ 의 Im 부분과 연결)

Markov 한도: `Σ_R(t-t') = σ_0 δ(t-t')`. **non-Markov**: `Σ_R(ω) = σ_0 / (1 - i ω τ_mem)` (Drude-Lorentz) 또는 `Σ_R(ω) = σ_0 (1 - i ω τ_mem) / (1 + ω² τ_mem²)`.

### 2.2 Effective σ as a function of scale

스케일 k 에서 효과적 단면적:
```
σ_eff(k, ω) = Re[Σ_R(ω = c_s k)]
```
- ω τ_mem ≪ 1 (cosmological, t > Gyr): σ_eff → σ_0 (Markov 회복)
- ω τ_mem ~ 1 (cluster, t ~ Gyr): σ_eff 가 감소 + 위상 지연
- ω τ_mem ≫ 1 (galactic, t < 100 Myr): σ_eff → 0 (memory 가 응답 차단)

이 구조면 cluster dip 은 "cluster scale 만 정확히 ω τ_mem ~ 1 영역에 들어와 backflow 로 σ_0 가 약해짐" 으로 자연스럽게 등장.

---

## 3. Memory Backflow

### 3.1 정의

응답함수 χ(t) = Σ_R 의 시간영역 표현이 **t > 0 에서 부호를 바꾸면** memory backflow:
```
χ(t) = (σ_0 / τ_mem) e^(-t/τ_mem) [1 - 2 t/τ_mem]   (例)
```
이 형태는 t < τ_mem/2 에서 정방향 (소화), t > τ_mem/2 에서 역방향 (재방출/되먹임).

### 3.2 Cluster 에서 sigma 약화 메커니즘

Cluster 안의 baryon overdensity δ_b 가 n-필드를 국소적으로 끌어당겨 (소화) → τ_mem 후 일부가 다시 되돌아옴 (backflow) → net σ_eff 가 σ_0 의 ~30–60% 까지 감소.

이는 L470 에서 관측된 cluster scale 에서의 dip (σ_0 가 voids/galaxies 보다 작게 보이는 현상) 의 자연스러운 후보.

---

## 4. Timescale Matching

| 환경        | 동적 시간 t_dyn | ω τ_mem (τ_mem ~ 1 Gyr 가정) | σ_eff/σ_0 예상 |
|-------------|----------------|-------------------------------|----------------|
| Hubble flow | ~14 Gyr        | ~0.07 (Markov)                | ~1.0           |
| Cluster     | ~1–3 Gyr       | ~0.5–1                        | ~0.3–0.6 (DIP) |
| Galaxy      | ~0.1 Gyr       | ~10                           | ~0.05 (suppressed) |
| BBN         | ~10⁻¹² Gyr     | ω τ_mem ≫ 1                   | ~0 (안전)      |

τ_mem ≈ 1 Gyr 에서 cluster dip 이 자연스럽게 등장하고 BBN/early-universe 는 memory 가 무력화돼 SQMH 제약 위반 없음. **timescale matching 통과**.

τ_mem 의 미시 기원 후보: (a) n-필드의 thermal relaxation (T_dS ~ H_0), (b) dark sector 의 elastic scattering rate, (c) Planck-scale 가 cosmic scale 에서 RG-running 으로 effective 하게 부풀려진 결과.

---

## 5. Falsifiable Predictions

1. **Scale-dependent σ_0**: cluster (k ~ 1 Mpc⁻¹) 에서 ~50% 감소, galaxy (k > 10 Mpc⁻¹) 에서 ~95% 억제. RSD/cluster lensing 교차분석으로 검증.
2. **Phase lag**: cluster mass 응답이 baryon overdensity 보다 ~τ_mem (~Gyr) 지연. 고-z cluster 진화 계측에서 보일 수 있음.
3. **Non-Gaussian noise**: SK noise kernel K(ω) 가 colored 되면 dark matter velocity dispersion 의 cumulant 가 deviation 보임.
4. **Reverse correlation 신호**: backflow 는 cluster outskirts (R > R_200) 에서 over-prediction 을 만듦 — splashback radius 부근 density profile 에서 LCDM 대비 +5–15% 초과 예측.

---

## 6. 비판적 점검

- **위험 1**: τ_mem ≈ Gyr 은 fine-tuning. 미시 기원 없으면 ad hoc.
- **위험 2**: SK 형식주의는 Hermitian closed system 에 dissipation 을 도입 — SQMH n-필드의 "소화" 가 unitarity-preserving open system 으로 reformulate 가능한지 확인 필요.
- **위험 3**: Cassini PPN 위반 가능성 — cluster scale 응답이 solar system 까지 누설되면 |γ−1| 한도 침해. dark-only sector embedding (C10k 패턴) 필수.
- **위험 4**: backflow 는 H-theorem 의 monotone entropy 증가와 충돌 가능 — entropy 가 oscillate 할 수 있는지 메타-검토 필요 (FDT 만족하면 OK, 아니면 ill-defined).

---

## 7. 다음 단계 (free speculation, 강제 아님)

- Drude-Lorentz `Σ_R(ω)` 를 SQMH 연속 방정식에 삽입한 toy model 작성.
- L470 cluster dip 데이터에 σ_eff(k) ansatz fit → τ_mem 추정.
- `τ_mem` 의 microphysical derivation 시도 (n-필드 self-interaction loop 또는 dark sector elastic scattering).
- Vainshtein-style screening 과의 등가성 비교 (둘 다 scale-dependent 응답).

---

**Status**: 자유 추측. 수식은 sketch 수준이며 어떤 것도 확정 결과 아님. L474 한정 speculation document.
