# refs/l6_amplitude_lock_analysis.md — L6-T1 Amplitude-Locking 유도 시도

> **Rule-A 적용**: 8인 순차 검토 완료.
> 작성일: 2026-04-11 | 상태: 8인팀 합의 완료

---

## 목적

Alt-20 템플릿의 핵심 구조:

$$E^2(z) = E^2_{\rm LCDM}(z) + \Omega_m \cdot F(a; m_{\rm shape})$$

에서 **드리프트 진폭이 Ω_m에 잠기는 이유**가
(1) SQMH L0/L1 공리에서 수식 유도되는가,
(2) E(0)=1 정규화의 귀결인가,
(3) 순수 수치적 우연인가를 판정한다.

---

## 출발: Alt-20 템플릿 구조 분석

`simulations/l4_alt/runner.py`에서:

```python
OL0 = 1.0 - Om - OMEGA_R           # Omega_DE,0
r   = f_ratio(a, Om)               # A01: 1 + Om*(1-a)
rho_de = OL0 * r

E² = Omega_r*(1+z)^4 + Om*(1+z)^3 + OL0*r
```

A01 정규화 확인: r(a=1, Om) = 1 + Om*0 = 1 → rho_de(a=1) = OL0 → E(0)=1 ✓

**드리프트 항** (A01):
$$\Delta E^2 \equiv E^2 - E^2_{\rm LCDM} = \Omega_{\rm DE,0} \cdot \Omega_m \cdot (1-a)$$

드리프트 진폭 = Ω_DE,0 · Ω_m = (1-Ω_m) · Ω_m ≈ Ω_m (Ω_m~0.31에서 Ω_DE,0~0.69이므로)

여기서 "amplitude ∝ Ω_m"은 **템플릿 f 인수에 Om이 들어가기 때문**이다.
왜 Om인가? → 이것이 본 분석의 핵심 질문.

---

## 접근 1: SQMH 연속방정식 적분

### 배경 방정식

SQMH 균일 등방 우주론 (base.md §1.2 배경 평균):

$$\frac{d\bar{n}}{dt} + 3H\bar{n} = \Gamma_0 - \sigma\bar{n}\bar{\rho}_m$$

암흑 에너지 밀도와의 관계 (§V 대사 균형):

$$\rho_{\rm DE} = \mu \cdot \bar{n} \quad \Rightarrow \quad \frac{d\rho_{\rm DE}}{dt} + 3H\rho_{\rm DE} = \mu\Gamma_0 - \sigma\rho_{\rm DE}\bar{\rho}_m$$

우변 첫째 항 μΓ₀ = 생성 기여, 둘째 항 = 소멸 기여.

### e-폴딩 수 N = ln a 로 변환

$$\rho_{\rm DE}' + 3\rho_{\rm DE} = \frac{\mu\Gamma_0}{H^2} - \frac{\sigma}{H}\rho_{\rm DE}\bar{\rho}_m$$

여기서 ' = d/dN.

**LCDM 근사** (0차): ρ_DE ≈ ρ_Λ = const, H² ≈ H₀²E²_LCDM(a)

**1차 보정** Δρ_DE = ρ_DE - ρ_Λ:

$$\frac{d(\Delta\rho_{\rm DE})}{dN} + 3\Delta\rho_{\rm DE} \approx -\frac{\sigma}{H}\rho_\Lambda\bar{\rho}_m$$

$$= -\frac{\sigma\rho_\Lambda}{H_0 E_{\rm LCDM}}\cdot\Omega_m\rho_{c,0}e^{-3N}$$

### 적분 (N=0: 오늘 → N<0: 과거)

$$\Delta\rho_{\rm DE}(a) = \frac{\sigma\rho_\Lambda\Omega_m\rho_{c,0}}{H_0}\int_a^1 \frac{a'^{-3}}{E_{\rm LCDM}(a')} e^{3(\ln a - \ln a')} d\ln a'$$

**핵심 구조**: 적분 인수에 **Ω_m이 multiplicative factor로 등장**.

$$\Delta\rho_{\rm DE}(a) = C \cdot \Omega_m \cdot G(a)$$

여기서 C = σρ_Λρ_{c,0}/H₀는 상수, G(a)는 적분 결과.

**결론**: Δρ_DE ∝ Ω_m 은 SQMH 연속방정식의 **소멸 항 ρ_DE · ρ_m에서 ρ_m ∝ Ω_m 으로 인해 자동 성립**.

### amplitude-locking의 물리적 원인

소멸률 = σ · n̄ · ρ̄_m에서 **ρ̄_m ∝ Ω_m** 이 증폭 인수로 진입.
더 많은 물질 (큰 Ω_m) → 더 많은 소멸 → DE 더 많이 감소 (음의 피드백) OR
wₐ < 0 방향의 drift. 부호는 소멸항의 부호.

E(0)=1 정규화는 전체 스케일(C)을 흡수하여 템플릿을 무차원화.
결과: amplitude = C·G(1)/OL0 = Ω_m (정규화 후).

---

## 접근 2: E(0)=1 강제 + 에너지 보존

### 두 조건

1. E(0)=1: Σ Ω_i = 1 → OL0 = 1 - Ω_m - Ω_r
2. 에너지 보존: dρ_tot/dN + 3ρ_tot(1+w_tot) = 0 (Bianchi identity)

### 독립 파라미터 계산

SQMH drift ansatz: ρ_DE(a) = OL0 * [1 + α*(1-a)]

자유 파라미터: α (drift amplitude)

E(0)=1 적용: α*(1-1) = 0 → 자동 만족. α 미결정.

에너지 보존은 α에 대한 추가 조건을 주는가?

$$\frac{dE^2}{dN} = -4\Omega_r e^{-4N} - 3\Omega_m e^{-3N} + OL0\cdot\alpha e^N$$

에너지 보존은 E² 값에 조건을 주지 않고 E²의 구조 자체.
→ **에너지 보존만으로는 α 결정 불가**.

**결론**: α 결정은 소멸 결합 강도 σ에서 온다 (접근 1).
E(0)=1은 정규화 조건일 뿐, α를 uniquely fix하지 않는다.

---

## 접근 3: CLW Attractor (C11D 해석)

### V(φ) = V₀ exp(-λφ) tracker 해

Copeland-Liddle-Wands 1998 autonomous system:
x' = -3x + √6/2 λy² + 3x(1 + x² - y²)
y' = -√6/2 λxy + 3y(x² - y²) + ... 

tracker 해 (λ² < 3): Ω_φ = 3(1+w_m)/λ² (radiation/matter 지배 시대)

**현재 시대 (matter→DE 전환)**: Ω_φ → 1, tracker에서 이탈.

Ω_m 의존성: tracker 해 Ω_φ = 3/λ²에서 직접 Ω_m 의존성 없음.
단, 현재 초기조건 (a=1에서 Ω_φ = OL0 ≈ 1-Ω_m)이 ODE를 통해
wₐ에 Ω_m 의존성 간접 주입.

**결론**: CLW tracker에서 amplitude ∝ Ω_m 의 직접 유도는 없음.
C11D의 λ=0.888은 데이터에서 결정되며 이론에서 고정되지 않음.

---

## 접근 4: 정규화 Artifact 가능성 분석

Alt-20 f(a, Om): f(a=1, Om) = 1 by construction (모든 템플릿).
이것은 **Om이 f에 들어가는 방식에서 f(1, Om)=1 이 되도록 설계된 것**.

A01: f = 1 + Om*(1-a) → f(1) = 1 ✓ (Om 값과 무관하게)
A12: f = 1 + erf(Om*(1-a)) → f(1) = 1 + erf(0) = 1 ✓

즉 **어떤 template이라도 f(a=1)=1이 되도록 설계하면 Om이 자동 amplitude로 들어간다.**
이것은 E(0)=1 정규화의 직접적 귀결.

**그러나**: 데이터가 왜 Om을 amplitude로 "선택"하는가?
Om/2, 2*Om, Om² 등으로 대체하면 chi² 증가.
→ Om = amplitude 는 단순 정규화가 아니라 **데이터에서 선택된 값**.

---

## 종합 분석

| 접근 | 결론 | 신뢰도 |
|------|------|--------|
| 1. SQMH 연속방정식 | Δρ_DE ∝ Ω_m (소멸항 ρ_m ∝ Ω_m) | 높음 — 구조적 |
| 2. E(0)=1 + 보존 | α 미결정 (E(0)=1만으로 부족) | 확정 — 보존만으로 부족 |
| 3. CLW attractor | Ω_m 직접 의존성 없음 | 낮음 — C11D에 한정 |
| 4. 정규화 artifact | 정규화 + 데이터 선택의 조합 | 중간 |

**핵심 결론**:
amplitude ∝ Ω_m 은 **SQMH 연속방정식의 소멸 항 구조에서 반정성적으로 동기화**된다.
그러나 **결합 강도 σ의 정확한 값** (템플릿의 정규화된 계수 = 1)은
이론에서 고정되지 않고 E(0)=1 정규화 + 데이터 최적화의 결과다.

---

## 8인 검토 결과

### 검토자 1 — 물리학자

소멸 항 σ·n̄·ρ̄_m에서 ρ̄_m ∝ Ω_m이 직접 drift amplitude를 결정한다는 메커니즘은
물리적으로 타당하다. 더 많은 물질 → 더 많은 DE 소멸 → DE 밀도 감소 = wₐ < 0 방향.
방향성 (부호)은 이론에서 결정됨. **크기(정확한 amplitude)는 결합 강도 σ 의존**.
σ = 4πG·t_P 는 고정값이지만, 정규화된 계수 1 (= Om으로 표현)은
배경 E(0)=1 조건에서 흡수된 결과.

**판정**: 메커니즘 타당. amplitude 크기는 "E(0)=1 흡수 후 데이터 선택".

### 검토자 2 — 수학자

접근 1의 적분 구조 확인:
Δρ_DE(a) = C·Ω_m·G(a) 에서 Ω_m은 multiplicative factor로 등장.
그러나 C는 σρ_Λρ_c,0/H₀이며 이 값이 OL0로 정규화되면 coefficient = Ω_m이 됨.
이것은 C·Ω_m = OL0·Ω_m (수치적 coincidence at Ω_m≈0.31이 아닌 구조적).
수식 유도 완결성: 부분적 유도. Δρ_DE의 **형태** ∝ Ω_m은 유도됨.
**exact coefficient = 1** (즉 α = Ω_m 정확히)은 E(0)=1 정규화 흡수.

**판정**: 부분 유도 성공. "amplitude의 Ω_m 의존성"은 이론 귀결.
"exact amplitude = Ω_m"은 정규화 귀결.

### 검토자 3 — 우주론자

L5 결과와 연결: A01~A20 14개 클러스터 모두 동일 물리 효과 (SVD n_eff=1).
즉 F(a)의 정확한 형태는 데이터가 구별 못함. 공통 구조 = Ω_m 곱.
이것이 우주론 관측에서 선택되는 이유: Ω_m ≈ 0.31에서 drift가 관측 범위 내.
Ω_m² (≈0.096) 이나 √Ω_m (≈0.56) 이면 chi² 유의미하게 증가.

**판정**: 우주론적으로 Ω_m amplitude는 데이터가 "자연스럽게 선택"한 결과.

### 검토자 4 — 회의론자

가장 강한 반론: **왜 정확히 Ω_m인가?**

SQMH 연속방정식 접근으로 Δρ_DE ∝ Ω_m의 형태는 나오지만,
exact coefficient가 1인 이유는 이론에서 나오지 않는다.
이것은 마치 "물질이 많으면 DE가 줄어든다"고 말하는 것과
"DE가 정확히 Ω_m만큼 줄어든다"고 말하는 것의 차이.

전자는 이론, 후자는 데이터 fitting.

**반례**: 같은 구조로 ρ_m/ρ_crit,0 = Ω_m*(1+z)^3 (진화하는 amplitude)를 쓰면
다른 chi² 결과가 나온다. 왜 z=0 값 Ω_m을 쓰는가?
→ E(0)=1 정규화가 z=0 snapshot을 amplitude로 고정하기 때문.

**결론**: "Ω_m이 amplitude인 이유"의 50%는 이론, 50%는 정규화 artifact.

### 검토자 5 — 관측천문학자

DR3/Euclid 관점: amplitude가 Ω_m인 것이 관측적으로 검증 가능한가?

C11D: λ=0.888이 데이터에서 결정되고 이론 예측값이 없다면
"파라미터 없는 예측"이 아닌 "1-파라미터 피팅".
A12 (zero-param): amplitude = Ω_m, 이 관계 자체가 예측이 됨.

Euclid에서 Ω_m을 독립 측정하면 amplitude와 비교 가능.
만약 amplitude ≠ Ω_m (Euclid), SQMH 예측 falsified.
→ falsifiable 예측 존재. 현재 단계 강점.

### 검토자 6 — 철학자

Ω_m-locking이 "설명"인가 "재기술"인가:
- 이론 측면: DE 소멸이 물질에 비례한다 (인과적 설명 구조)
- 정규화 측면: E(0)=1이 amplitude를 Ω_m으로 정의 (관례)

Quine-Duhem 문제: 어떤 가정을 바꿔도 관측과 일치하도록 이론 조정 가능.
현재 amplitude-locking은 "이론적 동기 있는 정규화 선택" 수준.

**판정**: 완전 설명과 완전 재기술 사이. "이론 동기 있는 phenomenology".

### 검토자 7 — 비교이론가

기존 이론과 비교:
- Wetterich 1995 growing neutrino: coupling ∝ ρ_ν. SQMH: coupling ∝ ρ_m.
  같은 구조. amplitude는 결합 상수로 결정.
- Barrow-Clifton 2006: dark energy drift ∝ Ω_m - 비슷한 경험적 선택.
- Amendola 2000 coupled DE: Q = βHρ_m에서 β가 자유 파라미터.
  SQMH는 β ↔ Ω_m (데이터 선택). 구조 동일.

SQMH의 차별성은 "amplitude = Ω_m"이 아니라 "zero-parameter 구현".
즉 **β를 자유 파라미터로 두지 않고 Ω_m으로 고정하는 것이 핵심**.
이 고정이 E(0)=1 + SQMH 연속방정식 구조에서 motivated됨.

### 검토자 8 — 통합자 (최종 판정)

**1-7 종합**:

amplitude ∝ Ω_m 의 **정성적 기원** (이론 유도 가능):
- SQMH 연속방정식 소멸 항 σ·n̄·ρ̄_m에서 ρ̄_m ∝ Ω_m → Δρ_DE ∝ Ω_m (검토자 1, 2 확인)
- 물질이 DE 소멸을 유도한다는 인과 구조 (검토자 1, 6)
- 관측에서 자연스럽게 선택됨 (검토자 3, 5)

amplitude = exactly Ω_m 의 **정량적 기원** (postulate 귀결):
- exact coefficient 1은 E(0)=1 정규화 + 데이터 선택 (검토자 2, 4 지적)
- 결합 강도 σ의 값이 이론에서 고정되더라도 정규화 과정에서 흡수됨 (검토자 4)

---

## 최종 판정

**K20 기준**: "반증" 판정인가? → **아니오**.

**최종 등급**: "이론 동기 있는 정규화 귀결 (Theory-motivated normalization consequence)"

- "Δρ_DE ∝ Ω_m" → **이론에서 유도됨** (Q17 부분 달성)
- "amplitude exact = Ω_m" → **E(0)=1 + 데이터 정규화의 귀결** (postulate 수준)

**논문 §2 기술 방법 (8인 합의)**:

> "The amplitude-locking α = Ω_m arises naturally from the SQMH annihilation
> term σ·n̄·ρ̄_m ∝ ρ_m ∝ Ω_m, which drives dark energy drift proportional to
> the matter density parameter. The exact coefficient unity is absorbed into the
> E(0)=1 normalization, rendering the template parameter-free. This constitutes
> a theoretical motivation rather than a first-principles derivation."

**주장 가능**: "amplitude의 Ω_m 의존성은 SQMH 연속방정식에서 동기화됨"
**주장 불가**: "amplitude = Ω_m 이 SQMH에서 정확하게 유도됨"

**Q17 판정**: **부분 달성** — "이론 동기 있음"은 성립, "완전 유도"는 불성립.
논문에서 "theory-motivated zero-parameter implementation"으로 기술.

*8인 검토 완료. 최종 판정: K20 미해당. 이론 동기 주장 허용.*
