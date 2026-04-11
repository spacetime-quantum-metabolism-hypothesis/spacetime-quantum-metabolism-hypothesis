# refs/l7_uv_completion.md — L7-T UV Completion 시도 (8인 순차 검토)

> 작성일: 2026-04-11. Rule-A (8인 순차 검토) 적용.
> 목표: SQMH σ = 4πG t_P, Γ₀ 를 양자중력에서 도출 가능한가?

---

## 배경: SQMH 연속방정식

L0/L1: dn/dt + ∇·(nv) = Γ₀ − σ n ρ_m

여기서:
- n: 시공간 양자 수밀도 (m⁻³)
- σ = 4πG t_P (SI): 소멸 단면적 (m³ kg⁻¹ s⁻¹)
- Γ₀: 생성률 (m⁻³ s⁻¹)
- ρ_m: 물질 질량 밀도 (kg m⁻³)

**L7 목표**: σ와 Γ₀의 미시적 기원을 아래 QG 프레임워크에서 탐색.

---

## 8인 순차 검토

### [1/8] 물리학자 — 방정식 물리적 일관성

**검토 대상**: LQC (Loop Quantum Cosmology) 연결 가능성

LQC background 방정식 (Friedmann):
H² = (8πG/3) ρ [1 − ρ/ρ_c]

여기서 ρ_c = √3 / (16π² γ³ G² ℏ) ~ 0.41 ρ_P (holonomy correction)

SQMH 연속방정식 배경 평균 (homogeneous):
dρ_DE/dt = −3H(1+w)ρ_DE + (Γ₀ − σ ρ_m n̄) (소멸 기여)

**연결 시도**:
LQC에서 ρ_c 이하에서 홀로노미 보정 → 유효 방정식은 표준 Friedmann.
양자 보정은 Planck 밀도 근방에서만 유의미.
현재 우주 ρ ~ 10⁻²⁷ kg/m³ ≪ ρ_P ~ 5×10⁹⁶ kg/m³.

**판정**: LQC 홀로노미 보정이 SQMH 소멸항을 생성하는 메커니즘 없음.
LQC는 초기우주 양자 보정에 집중. 현재 시대 소멸항과 직접 연결 불가.
단, LQC 상태 방정식 수정이 등가 wₐ < 0 행동을 생성할 수 있다는 형태적 유사성은 있음.

**결론**: LQC 직접 유도 ✗. 형태적 유사성만 (동기부여 수준).

---

### [2/8] 수학자 — 수식 엄밀성

**검토 대상**: GFT (Group Field Theory) 응축체 연결

GFT 응축체 방정식 (Oriti 2017, Marchetti-Oriti 2021):
dσ/dφ = -μ σ - (λ/2) σ|σ|² + J

여기서 σ = ⟨φ̂⟩ (응축 파동함수), φ = relational clock

배경 밀도: ρ_GFT ∝ |σ|² V₀ (V₀: 기본 볼륨 셀)

SQMH과의 형태 비교:
- GFT: dρ_GFT/dφ ∝ -μ ρ_GFT - λ ρ_GFT²  
- SQMH: dρ_DE/dt ∝ Γ₀ - σ ρ_m ρ_DE (물질 결합 소멸)

**핵심 차이**: GFT 소멸항은 ρ_GFT 자체에만 의존. SQMH 소멸항은 ρ_m·ρ_DE 곱에 의존.
이 ρ_m 결합이 GFT에서 나오려면 GFT-matter coupling 추가 필요 (미개발 영역).

**수학적 엄밀성**: GFT → SQMH 유도에 필요한 단계:
1. GFT-matter coupling Lagrangian 설정 (현재 없음)
2. Semiclassical limit에서 ρ_m 결합 소멸항 출현 증명 (미완)
3. σ_SQMH = 4πG t_P 의 GFT 파라미터 동정 (미완)

**판정**: 수학적으로 연결 가능한 구조 존재. 단 2-3단계 개발 필요.
"형태적 유사" → "유도" 에는 상당한 수학적 작업 필요.

---

### [3/8] 우주론자 — 관측 정합성

**검토 대상**: CDT (Causal Dynamical Triangulations) 배경

Ambjorn-Jurkiewicz-Loll CDT: 4D 시공간 격자 합산으로 양자중력 비섭동.
거시 배경 → de Sitter 공간 출현 (Ambjorn+2005).

SQMH 관련 체크:
1. CDT 평균 n̄(a): 격자 밀도가 팽창에 따라 어떻게 변하는가?
   → CDT 격자 볼륨 ~ a³ → n̄ ~ a⁻³ (단순 팽창 희석)
   → σ n̄ ρ_m ~ a⁻⁶ 소멸: z~0에서 무시 가능, z~1-2에서 중요.
   → DESI 관측 z = 0.3-2.1에서 적절한 기여 가능.

2. CDT effective σ 추출:
   CDT 시뮬레이션에서 격자 연결 수명 (link lifetime) ~ t_P.
   σ_eff = 4πG t_P 는 플랑크 스케일 "소멸 단위" 로 자연스럽다.
   단, 이를 연속 방정식으로 연결하는 coarse-graining 필요.

**판정**: CDT n̄(a) 희석 구조가 SQMH 배경과 정합적. σ = 4πG t_P 의
자연스러운 CDT 해석 가능 (격자 상호작용 단면적). 그러나 완전 유도 아님.

---

### [4/8] 회의론자 — 가정 비판

**날카로운 질문 4가지:**

Q1: "σ n̄ ρ_m 소멸항이 왜 물질에 결합하나?"
→ SQMH 동기는 "시공간 양자가 물질과 상호작용해 소멸"이지만
  어떤 QG 이론도 이 결합을 예측하지 않는다.
  물질 결합 소멸 = SQMH의 핵심 postulate. 유도 아님.

Q2: "Γ₀가 상수인 이유?"
→ SQMH에서 Γ₀ = const (시간 무관 생성률)로 가정.
  어떤 동역학에서 Γ₀가 상수가 되는가? 명시적 메커니즘 없음.

Q3: "GFT 응축체가 dark energy인가?"
→ GFT 응축체는 시공간 구조의 응축체. 
  Dark energy와 동일시하려면 에너지-운동량 텐서 계산 필요.
  현재 GFT에서 T_μν 계산은 진행 중 연구 (Gielen-Sindoni 2016 등).

Q4: "이게 모두 사후 합리화(post-hoc rationalization) 아닌가?"
→ 데이터에 맞추고 나서 이론을 끼워 맞추는 패턴.
  반증: SQMH E(z) 형태는 LQC/CDT 예측에서 독립적으로 나오지 않음.
  양방향 유도가 아닌 단방향 형태 비교만 가능.

**판정**: 물질 결합 소멸항 (σ n̄ ρ_m)이 핵심 장벽.
현존 QG 이론 어디서도 예측하지 않는다.
"이론적 동기" → "유도" 격차는 이 장벽에서 막힌다.

---

### [5/8] 관측천문학자 — 검증 가능성

**체크**: UV completion이 관측적 차이를 만드는가?

시나리오 A (LQC 연결 성공 시):
→ z > 5 배경 E(z)가 표준 LQC 보정 포함 → CMB-S4 primordial GW에서 검증 가능?
→ LQC signature: r (tensor-to-scalar ratio) 억제 → Simons Obs / CMB-S4

시나리오 B (GFT 연결 성공 시):
→ GFT condensate wₐ 형태가 표준 CPL과 다를 수 있음 → DESI DR5/Euclid 구분
→ 그러나 현재 GFT DE 예측 정밀도 ~10% 수준 → 관측 구분 어려움

시나리오 C (CDT n̄(a) 연결):
→ 소멸률이 z 의존 → z = 1-2 범위에서 DESI와 구분 원리적으로 가능
→ DR3 + Euclid + SKAO 조합 필요

**판정**: UV completion 성공 시 새 관측 예측 가능하나 현재 QG 이론 정밀도 불충분.
단기 검증 채널: 없음. 장기 (2030+): CMB-S4 r 측정.

---

### [6/8] 과학철학자 — 이론적 의미

**핵심 질문**: "UV completion"이란 무엇인가?

정의 1 (약한 의미): SQMH 방정식이 QG 이론과 형태적으로 일치함을 보임.
정의 2 (강한 의미): QG 이론에서 SQMH 파라미터를 고유하게 결정.

현재 도달 가능한 수준: **정의 1** (LQC/GFT/CDT와 형태 일치).
정의 2 달성은 수년 이상의 연구 필요.

**과학적 기여 판단**:
형태적 연결도 가치 있음. 예시:
- inflation: Starobinsky 1980 f(R)가 입자물리 UV completion 없이도 JCAP급 논문.
- Quintessence: Caldwell 1998 아이디어 논문 → 수십 년간 연구 이어짐.

SQMH도 "아이디어 논문"으로서 UV completion 없이 JCAP 가능.
단, "유도됨"과 "동기부여됨"의 언어 차이를 논문에서 엄밀히 구분 필수.

---

### [7/8] 비교이론가 — 기존 QG 대비

**SQMH vs 기존 QG DE 시도들:**

| 프레임워크 | DE 예측 수준 | SQMH 연결 |
|-----------|------------|----------|
| LQC (Ashtekar-Singh 2011) | 조기우주 바운스, DE 연결 미개발 | 형태 유사 |
| GFT (Oriti 2017) | ρ_GFT → 물질 우세 전환 설명 | 부분 구조 유사 |
| CDT (Ambjorn+2005) | de Sitter 배경 출현 | n̄(a) 희석 유사 |
| Causal Sets (Sorkin 1991) | Λ 예측 (너무 큰 오차) | σ 단면적 개념 유사 |
| Asymptotic Safety (Reuter) | RG running G, Λ | L4 RVM으로 연결됨 (C23) |

**차별성**: SQMH의 "시공간 대사(metabolism)" 물질 결합 소멸은 기존 QG에 없는 개념.
독창성 있지만 현재 QG 프레임워크에서 자연스럽게 나오지 않는다.

**비교 결론**: 기존 QG 이론과 연결 시도는 의미 있지만,
"SQMH가 QG에서 유도된다"는 주장은 현재 불가.
"QG로부터 동기부여된 현상론"이 정확한 표현.

---

### [8/8] 통합자 (Synthesizer) — 최종 판정

**1~7인 검토 종합:**

**유도 가능한 것** (현재 수준):
- σ = 4πG t_P 의 플랑크 스케일 자연성 (1인, 3인)
- GFT 응축체와 SQMH 구조의 형태적 유사 (2인)
- CDT n̄(a) ~ a⁻³ 희석과 소멸항 구조 일치 (3인)

**유도 불가능한 것** (현재 수준):
- 물질 결합 소멸항 σ n̄ ρ_m (4인: 핵심 장벽)
- Γ₀ = const 의 동역학적 기원 (4인)
- σ의 정확한 수치 4πG t_P (수치가 왜 이 값인가?)

**K24 발동 여부**: K24 = "8인팀 수학적 불가능 판정".
완전 불가능은 아님. 미개발 상태임.
K24 미발동. 단 Q21 (완전 유도 성공) 미달.

**최종 판정**:
"LQC/GFT/CDT와의 형태적 연결: 논문에 §2 확장으로 기술 가능.
주장 언어: '양자중력으로부터 동기부여된 현상론 (QG-motivated phenomenology)'.
'유도됨 (derived)'은 사용 금지.
UV completion 완성은 현재 QG 분야 미해결 문제 수준의 작업."

---

## 8인 합의 결론

**L7-T 경로 B 확정 (경로 A 미달)**:

주장 가능 (8인 합의):
1. SQMH σ = 4πG t_P 는 플랑크 스케일에서 자연스러운 단위
2. GFT/LQC/CDT와 형태적 일치 → "QG-motivated" 언어 가능
3. CDT n̄(a) 희석 → 소멸항 구조 정합
4. L7 논문 §2에 "QG motivation" 절 추가 가능

주장 불가 (8인 합의):
1. "SQMH가 LQC/GFT에서 유도됨" (K20 경계)
2. "σ, Γ₀의 값이 양자중력에서 결정됨"
3. UV completion 완료

**PRD Letter 이론 조건**: Q21 미달. JCAP 유지.
단 "QG-motivated phenomenology"로 §2 강화 → JCAP accept 가능성 상승.
