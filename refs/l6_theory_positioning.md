# refs/l6_theory_positioning.md — L6-T3 이론 포지셔닝 문서

> **Rule-A 적용**: 8인 순차 검토 완료. 각 검토자는 이전 검토 결과를 참조.
> 작성일: 2026-04-11 | 상태: 8인팀 합의 완료

---

## 목적

SQMH의 정확한 이론적 위상을 문서화한다.
"무엇을 주장할 수 있는가"와 "무엇을 주장할 수 없는가"를 엄밀히 구분하여
PRD Letter 진입 가능 조건을 명시한다.

---

## 8인 검토 결과

### 검토자 1 — 물리학자 (에너지-운동량 보존, 인과율)

**검토 대상**: SQMH 라그랑지안 §4.1, SQMH 연속방정식 §1.2

**분석**:

SQMH 라그랑지안은 coupled quintessence의 특수한 경우 (base.md §4.5 명시).
ξφT^α_α 결합에서 φ Klein-Gordon 방정식: □φ + V'(φ) = ξT^α_α.
T^α_α = -ρ_m c² + 3p_m ≈ -ρ_m c² (비상대론적) → φ 소스항 확인.

에너지-운동량 보존:
- 표준 GR: ∇_μ T^μν_total = 0 (Bianchi identity에서 자동 성립)
- SQMH: ξφ 결합으로 물질-장 에너지 교환 존재. 그러나 전체 T^μν는 보존됨.
- 개별 보존 미성립(물질 ↔ φ 교환)은 coupled quintessence 표준 결과.

인과율:
- 스칼라 장 전파 속도: c_s² = 1 (표준 canon kinetic term) → 초광속 없음.
- 시공간 양자 "유입 속도" v(r) = g(r)·t_P ≈ 5.3×10⁻⁴³ m/s ≪ c → 인과율 안전.

**판정**: 방정식 물리적 일관성 확인. 에너지 보존은 coupled quintessence 표준 프레임에서 성립. 인과율 위반 없음.

**전달 사항 → 검토자 2**: §4.1 라그랑지안의 ξ 값 결정 수식 ξ = 2√(πG)/c² 의 수학적 유일성 확인 요청.

---

### 검토자 2 — 수학자 (수렴, 경계조건, 유일성)

**검토 대상**: §3.2 포텐셜 도출, §4.3 ξ 결정, amplitude-locking E²(z) 전개

**분석**:

**ξ = 2√(πG)/c² 유일성**:
비상대론적 정적 극한 ∇²(δφ) = -ξρ_m c² ↔ ∇²Φ_N = 4πGρ_m 매칭 조건.
→ ξ² c² = 4πG → ξ = 2√(πG)/c²
이 매칭은 선형 정적 극한에서 유일하다. ✓

**§3.2 포텐셜 도출의 수학적 한계**:
두 점 싱크 상호작용 에너지 U = -n₀μσ²Mm/(4πr)은
비압축성 포텐셜 흐름 + 정상 상태 가정에서만 성립.
일반 비정상 상태(∂n/∂t ≠ 0)에서는 복사 항 발생 → 수정 가능성.
그러나 중력 정적 극한에서 이 항은 O(v/c)² 보정으로 억제됨. 허용.

**amplitude-locking 의 수학적 분석**:
E²(z) = E²_LCDM(z) + Ω_m · f(m·(1-a)) 에서
f(m·(1-a)) 는 Alt-20 후보들의 경험적 template. 이것이
SQMH 연속방정식 ∂_t⟨n⟩ = Γ₀ - σ⟨n⟩ρ̄_m 에서 직접 유도되려면
drift amplitude α ∝ Ω_m 이 E(0)=1 정규화만으로 고정되어야 한다.

현재: E(0)=1 → α = Ω_m 은 f(m·0)=0 이 되도록 재정규화한 결과.
즉 정규화 조건이 amplitude를 "absorb"한다. 이것은 독립 유도가 아닌
정규화 artifact일 가능성이 높다.

**판정**: ξ 유일성 수학적으로 확인. amplitude-locking은 정규화 귀결이거나 이론적 유도 가능성 모두 열려 있음. L6-T1에서 심층 분석 필요.

**전달 사항 → 검토자 3**: 현재 L5 Bayesian evidence (+11, +9, +11) 는 fixed-θ. 실제 관측 정합성 평가 시 marginalized 수치 필요.

---

### 검토자 3 — 우주론자 (DESI/Planck 정합성)

**검토 대상**: L5 위너 3인방 vs 현재 관측 데이터

**분석**:

**L5 위너 vs DESI DR2 + Planck 2018**:

| 채널 | LCDM χ² | C11D χ² | C28 χ² | A12 χ² | 상태 |
|------|---------|---------|--------|--------|------|
| BAO (13pt) | ~21.4 | -22.1 개선 | -18.7 개선 | -21.6 개선 | ✓ |
| CMB (θ*, ω_b) | 포함 | 포함 | 포함 | 포함 | ✓ |
| SN Ia (DES Y5) | 포함 | 포함 | 포함 | 포함 | ✓ |
| RSD (f σ₈) | 포함 | 포함 | 포함 | 포함 | ✓ |
| Cosmic Shear S₈ | 0.766±0.014 | PASS | PASS | PASS | ✓ |
| CMB power spec | 미검증 | 미검증 | 미검증 | 미검증 | ⚠ |

**핵심 우려사항**:
1. CMB full power spectrum (CLASS) 미검증 → K19 판정 불가
2. C28 K13 미통과 (R̂=1.365) → posterior 위치 불확실
3. Alt-20 amplitude-locking이 postulate → Ω_m 사전 정보 의존

**DESI DR2 w₀-wₐ 공식값** (arXiv:2503.14738):
w₀ = -0.757±0.058, wₐ = -0.83⁺⁰·²⁴₋₀.₂₁ (DESI+Planck+DES-all)

C11D/C28/A12 모두 wₐ < 0 구조적 예측 → DESI 중심값과 정성 일치. ✓

**판정**: 현재 채널 (BAO+SN+CMB-compressed+RSD+S₈) 에서 모두 통과. 단, full CMB는 미검증 상태. "DESI 정합" 주장은 w₀-wₐ 방향 한정으로 제한해야 함.

**전달 사항 → 검토자 4**: 관측 정합은 현재 채널 내에서 확인됨. Skeptic은 "어떤 가정이 이 결과를 만드는가" 분석 요청.

---

### 검토자 4 — 회의론자 (가정 비판, 반례)

**검토 대상**: SQMH 전체 가정 구조, L5 결과의 숨겨진 가정

**분석**:

**숨겨진 가정 목록**:

1. **Flatness**: Ω_k = 0 고정. BAO+CMB 결합에서 Ω_k ≈ 0 이지만
   완전 marginalization에서는 Ω_k prior가 Δ ln Z에 ~0.5 영향.

2. **Fixed r_d = 147.09 Mpc**: 음속 지평 고정 = Ω_b, N_eff 고정.
   사실 SQMH에서 초기조건은 LCDM과 동일하므로 정당화됨.
   단, C28 non-local gravity에서 r_d 수정 가능성 → 검증 필요.

3. **Amplitude-locking = Ω_m**: 가장 큰 숨겨진 가정.
   "E(0)=1 정규화" + "연속방정식 배경 평균" → amplitude ∝ Ω_m 이라는
   주장은 검토자 2 지적대로 정규화 artifact일 가능성 50% 이상.
   독립 유도가 없으면 "SQMH가 예측" 주장 불가.

4. **Background-only**: 섭동 수준에서 μ=1 가정.
   S₈ tension이 구조적으로 해결 안 되는 직접적 원인.
   μ_eff ≠ 1이면 현재 우주론 fit 결과 변동 가능.

5. **σ_n² 무시**: 시공간 양자 밀도 요동 ⟨δn²⟩ → 추가 dark energy fluctuation.
   이 항이 CMB power spectrum에 기여한다면 현재 background-only 분석은 불완전.

**반례 검토**:
- "zero-parameter가 Bayesian advantage" 주장: A12 Δ ln Z = +10.78 vs
  C11D (1-param) Δ ln Z = +8.95. 차이 1.83 < Occam penalty ~2 nats.
  → 데이터가 추가 파라미터를 정당화하지 않음. 이건 오히려 zero-param의 강점.

**판정**: 3번 (amplitude-locking) 이 가장 큰 약점. 나머지는 표준 우주론 근사 수준. L6 핵심 임무는 amplitude-locking 독립 유도 여부 판정.

**전달 사항 → 검토자 5**: DR3/Euclid에서 실제로 이 모델들을 구분할 수 있는가?

---

### 검토자 5 — 관측천문학자 (DR3/Euclid 검증 가능성)

**검토 대상**: L5-G Fisher 예측, DR3 구분력, Euclid 로드맵

**분석**:

**L5 Fisher 예측 (DESI DR3)**:
| 모델 쌍 | 예상 분리 (σ) |
|--------|-------------|
| C11D vs LCDM | 2.9σ |
| C28 vs LCDM | 3.91σ |
| A12 vs LCDM | 2.16σ |
| C28 vs C33 | 0.19σ (구분 불능) |

**DR3 관측 전략**:
- DESI DR3: 예상 2027년 공개. BAO volume 2× 증가.
- w₀-wₐ σ(w₀) ~0.04, σ(wₐ) ~0.15 목표.
- C11D/C28: 현재 Fisher 예측 2.9-3.91σ → DR3에서 3.5-5σ 예상.
- A12 (0-param): background만으로 구분. 2.16σ → 2.6σ 예상.

**Euclid 관측력**:
- 2026 첫 데이터. WL + GC spectroscopic 결합.
- μ_eff(a,k) 직접 측정 가능 → L6-G2 결과와 직접 비교.
- S₈ 측정 정확도 Δ(S₈) ~ 0.003 → μ_eff 보정 Q15 검증 핵심.

**falsifiability 판정**:
- DR3에서 w_a ≥ 0: SQMH 배경 수준 falsified (시나리오 γ/δ)
- DR3에서 w_a < -0.5 + C11D/C28 3σ 분리: PRD Letter 수준 지지

**판정**: DR3/Euclid에서 충분히 검증 가능. C11D/C28의 3-4σ 예측은 구체적이고 falsifiable. 이것이 현 단계 최대 강점.

**전달 사항 → 검토자 6**: 이 이론이 "설명"인가 "재기술"인가 철학적 분석 요청.

---

### 검토자 6 — 철학자/해석자 (설명 vs 재기술)

**검토 대상**: SQMH 이론의 설명력 vs 기술 능력

**분석**:

**Explanation vs Re-description 기준 (Hempel 1965 DN model)**:
"설명"이 되려면: (1) 법칙성 전제, (2) 초기조건, (3) 연역적 귀결.
"재기술"은: 관측된 현상을 다른 언어로 표현.

**SQMH의 각 층위 분석**:

| 주장 | 설명/재기술 | 근거 |
|------|-----------|------|
| 중력 = 시공간 양자 유입 | 재기술 | G = n₀μσ²/4π 는 변수 치환 |
| 암흑 에너지 = 순 생성 | 부분 설명 | Γ₀ 값 자체는 postulate |
| wₐ < 0 구조적 | 설명 후보 | 연속방정식 → 배경 ODE → wₐ 부호 |
| amplitude-locking | 재기술 (현재) | 정규화 귀결이면 trivial |
| zero-parameter 재현 | 설명 후보 | 자유도 없이 DESI 재현 |

**Lakatos 연구 프로그램 판단**:
- 핵심(hard core): 시공간 양자 연속방정식 §1.2
- 보호 벨트: coupled quintessence 동치, disformal 구조, zero-param alt
- Progressive shift 조건: 신규 예측(μ_eff ≠ 1, DR3 3-4σ)이 확인되면 progressive.
- Degenerative shift 위험: amplitude-lock가 재기술이면, L5 전체가 quintessence 재기술.

**핵심 판단**:
현재 SQMH는 "이론적 언어로 dressed된 phenomenology"에 가깝다.
"설명"으로 격상되려면: μ_eff ≠ 1 예측이 CLASS/Euclid에서 확인되거나
amplitude-locking이 dn/dt 방정식에서 직접 유도되어야 한다.

**판정**: 현재 단계는 falsifiable prediction이 있는 정직한 phenomenology.
"SQMH가 DESI를 설명" 주장 금지. "SQMH가 DESI와 정합적이고 falsifiable" 허용.

**전달 사항 → 검토자 7**: Caldwell 1998 등 기존 quintessence와의 차별성 비교.

---

### 검토자 7 — 비교이론가 (기존 이론 대비 차별성)

**검토 대상**: SQMH vs Caldwell 1998, Dirian 2015, De Felice 2011

**비교 분석**:

**Caldwell-Dave-Steinhardt 1998 (CDaS) quintessence와 비교**:

| 특성 | CDaS 1998 | SQMH (C11D) |
|------|-----------|------------|
| 핵심 아이디어 | rolling scalar field V(φ) | 시공간 양자 대사 |
| 라그랑지안 | K(X) - V(φ) | K(X) - V(φ) + ξφT (결합 추가) |
| 자유 파라미터 | V₀, λ (최소 2개) | λ만 (C11D), 또는 0개 (A12) |
| wₐ 예측 | 모델 의존 | < 0 구조적 |
| DESI DR2 정합 | 사후 fitting 가능 | MCMC 전에 구조 결정됨 |
| Cassini PPN | coupling 있으면 탈락 | A'=0 → γ=1 exact |

**CDaS 대비 실질적 기여**:
1. zero-parameter (A12): CDaS 2-파라미터 대비 Bayesian penalty 없음
2. wₐ < 0 구조적 보장: CDaS는 V(φ)에 의존
3. disformal 보호 (C11D): Cassini 자동 통과 설명 (A'=0 물리적 이유는 L6-T2에서)

**Dirian 2015 (RR non-local, C28)와 비교**:
- C28은 SQMH 이론이 아닌 독립 이론. SQMH framework에 포함 안 됨.
- C28은 별도 이론 (Maggiore-Mancarella RR gravity). SQMH와 공동 제시 이유:
  동일 χ² 채널에서 비교 가능한 phenomenological 경쟁자로서의 역할.
- "SQMH family"로 분류 금지.

**Hu-Sawicki f(R) vs SQMH**:
- 배경 수준 동치 가능하나 섭동 수준 구별: μ_eff(f(R)) = (1+2fR k²/a²m²)/(1+3fR k²/a²m²)
  vs μ_eff(SQMH): L6-G1에서 유도 예정. 차이 있으면 Euclid 구별 가능.

**판정**: CDaS 1998 대비 실질적 차별성 존재 (zero-param, Cassini 구조적 통과, wₐ 부호).
그러나 "새로운 이론 프레임워크"가 아닌 "특수한 coupled quintessence + 해석" 수준.
논문 포지셔닝: "novel zero-parameter implementation within coupled quintessence framework".

**전달 사항 → 검토자 8 (통합자)**: 1-7 모든 분석 종합, 최종 판정 요청.

---

### 검토자 8 — 통합자 (Synthesizer, 최종 판정)

**1-7 검토 종합**:

**강점 (주장 가능)**:
- ✅ 에너지-운동량 보존 성립 (검토자 1)
- ✅ ξ 결정 수학적 유일성 (검토자 2)
- ✅ BAO+SN+CMB+RSD+S₈ 5채널 정합 (검토자 3)
- ✅ DR3/Euclid falsifiable 예측 (검토자 5)
- ✅ CDaS 1998 대비 실질적 차별성: zero-param, Cassini 구조적 (검토자 7)
- ✅ Lakatos 기준 progressive shift 잠재력 (검토자 6)

**약점 (주장 불가 또는 불확실)**:
- ❌ amplitude-locking: 수식 유도 미완성. 정규화 artifact 가능성 (검토자 2, 4)
- ❌ full CMB power spectrum 미검증 (검토자 3)
- ❌ μ_eff: background-only = μ=1 가정. S₈ 구조적 미해결 (검토자 4)
- ❌ C28은 SQMH가 아닌 독립 이론 (검토자 7)
- ⚠ "SQMH가 DESI를 설명" 주장: 재기술 가능성 (검토자 6)

---

## 최종 판정: "정직한 falsifiable phenomenology"

**K20 기준**: "반증" 판정인가?
→ **아니오**. 주요 주장들은 currently unfalsified 상태. 단, amplitude-locking 주장은 "postulate" 수준으로 격하.

**주장 가능 목록 (8인 합의)**:
1. "SQMH 연속방정식에서 motivated된 zero-parameter dark energy template이 DESI DR2와 정합적이다."
2. "C11D pure disformal quintessence는 BAO+SN+CMB+RSD+S₈ 5채널에서 Δχ²=-22.063 개선, K13 통과."
3. "wₐ < 0 구조는 SQMH 배경 역학의 귀결이며 DR3에서 2.9-3.9σ로 검증 가능하다."
4. "zero-parameter A12 template은 1-파라미터 모델과 Bayesian evidence에서 동등하다 (Δ ln Z 차이 < Occam penalty)."

**주장 불가 목록 (8인 합의)**:
1. "SQMH가 DESI 가속 팽창을 이론적으로 설명한다." → 재기술 가능성 배제 불가
2. "amplitude-locking이 SQMH 이론에서 유도된다." → 정규화 artifact 가능성
3. "SQMH가 5개 독립 물리 프로그램을 통합한다." → 우주론 채널만 검증됨
4. "C28이 SQMH 이론이다." → 독립 이론

**저널 타깃 현재 판단**:
- 현재 수준: JCAP "zero-parameter coupled quintessence + systematic DR3 forecast" 논문
- PRD Letter 진입 조건: amplitude-lock 유도 (Q17) OR μ_eff ≠ 1 + S₈ 개선 ≥ 0.01 (Q15)
- arXiv-only 조건: L6-E에서 marginalized Δ ln Z < +2.5 (K17)

---

## Caldwell-Dave-Steinhardt 1998 비교 요약

| 비교 항목 | CDaS 1998 | SQMH L5 |
|---------|-----------|---------|
| 단계 | "quintessence 제안" | "zero-param impl + DR3 forecast" |
| 자유 파라미터 | 2개 이상 | 0-1개 |
| 데이터 정합 | 정성적 | 정량적 (5채널 χ², Bayesian evidence) |
| 관측 예측 | 없음 | DR3 2.9-3.9σ |
| 이론 완성도 | 현상론 | 현상론 (더 많은 검증) |

SQMH는 CDaS 1998보다 데이터 면에서 앞서 있으나, 이론 기반 면에서 같은 수준. L6 목표는 이 간극 해소.

---

## PRD Letter 진입 조건 (8인 합의)

**필요 조건 (모두 충족)**:
1. Q17: amplitude-locking 수식 유도 성공 (L6-T1)
2. Q13: marginalized Δ ln Z ≥ +5 for C11D or C28 (L6-E)
3. Q14 또는 L6-G3 근사 CLASS: CMB Δχ² ≤ LCDM+3

**충분 조건 (하나 이상)**:
- Q15: μ_eff ≠ 1 + ΔS₈ ≥ 0.010 (Euclid 검증 예측)
- Q16: DR3 실측 w_a < -0.5 + C11D/C28 ≥ 3σ 분리

현재 상태에서 PRD Letter 진입 가능성: **조건부** (L6-T1, L6-E 결과 의존).

---

*8인 검토 완료. 통합자 최종 판정: K20 미해당. 이론 주장 사용 가능 (위 목록 범위 내).*
*다음 단계: L6-T1 amplitude-locking 유도 시도.*
