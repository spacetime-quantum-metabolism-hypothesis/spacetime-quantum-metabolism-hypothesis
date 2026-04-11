# base.l13.command.md — L13 Phase-13: 논문 약점 직공 (ODE 정밀화 / wₐ 보정 / 진폭 도출 / DR3 예측 / Γ₀ 새 제약)

> 작성일: 2026-04-12. L12 완료 + 8인 재검토 이후 설계.
> 사용자 confirm 전부 생략. 묻지 말고 끝까지 자동 진행. 언어는 Python.

---

## 실행 명령

```
/bigwork-theory base.l13.command.md 에 기재된 L13
논문 약점 5개 파이프라인을 끝까지 수행.
사용자 confirm 전부 생략. 묻지 말고 진행. 언어는 Python.
base.l12.result.md, base.l11.result.md, base_2.md §7, refs/l8_new_findings.md,
simulations/l5/A01/mcmc_production.json, simulations/l4_alt/runner.py, CLAUDE.md 전부 참고.
L13 이름으로만 신규 파일 기록.
```

---

## 근본 목적

**8인 재검토에서 식별된 3대 약점**:

1. **Γ₀ 이론적 기원 미완** — L12-B에서 Bekenstein → K72 KILL. 새 각도 필요.
2. **wₐ 수치 갭** — A01 예측 wₐ≈−0.13 vs DESI 중심값 −0.64. 2σ 내이지만 불안.
3. **이론-현상론 서사 미완** — A01 = "1차 근사"라는 설명 불충분. 왜 Ωm이 진폭인가?

**추가 약점 (검토자 6, 7 지적)**:

4. **Ωm 진폭 고정 근거 없음** — Alt-20 스캔에서 경험적으로 설정됨. 이론 도출 필요.
5. **DR3 예측 미문서화** — SQMH의 구체적 DR3 예측값 없음. 검증 타임라인 불명확.

**L13 전략**:
L12가 "62자리 우회 경로 탐색"이었다면,
L13은 "현재 A01이 갖는 내부 구조를 파고들어 약점을 강점으로 전환한다."

---

## L12 → L13 핵심 변화

| 항목 | L12 | L13 |
|------|-----|-----|
| 전략 | 62자리 우회 신규 경로 탐색 | A01 내부 구조 정밀 해부 |
| 목표 | σ/Γ₀ 이론 결정 or 양자 채널 | wₐ 개선, 진폭 도출, DR3 예측 |
| 기대 게임체인저 | Q72/Q73 (전부 KILL됨) | Q83 (wₐ 2차 보정 ≥0.3) or Q85 (DR3 3σ 예측) |
| 접근 | 양자/엔트로피 | 해석 해 + ODE 수치 + 섭동 전개 |

---

## 프로세스 규칙

- **이론 검토**: 서로 중복되지 않은 8인팀. 수단과 방법을 가리지 않고 동시에 병렬 및 상호토의를 통해 유도. 결과를 취합하여 최종 판정.
- **코드**: Rule-B 4인 순차 코드리뷰, 태그 필수.
- **주장 언어**: L7~L12 언어 체계 승계
  - 성공 시: "2nd-order SQMH correction shifts wₐ by X"
  - 금지: "SQMH explains the full DESI wₐ" (과장 금지)
- **게임체인저 기준**: Q83 or Q85 달성 시 논문 §4 재구성 트리거

---

## Kill / Keep 기준 (L13 신규, 실행 전 고정)

**실행 시작 전** `refs/l13_kill_criteria.md` 에 아래 기준 고정.

### L13 KILL 조건

| ID | 조건 | 결과 |
|----|------|------|
| **K81** | 전체 SQMH ODE 수치 적분 Δchi² = A01 Δchi² ± 0.5 | A01 근사가 충분. 1차 근사 논문 사용 정당화. |
| **K82** | Ωm 진폭이 정규화 조건(E(0)=1)에서만 나옴 → 이론 구조 아님 | 진폭 도출 실패. "amplitude locking = normalization artifact" 논문 명기 필요. |
| **K83** | wₐ 2차 보정 크기 < 0.1 | 섭동론으로 wₐ 갭 해소 불가. DR3 신규 데이터 필요. |
| **K84** | 진공 에너지 안정성 조건에서 Γ₀ 범위 > 20자리 | Γ₀ 결정 새 경로도 실패. NF-27 완전 확정. |
| **K85** | DR3 Fisher 예측: A01 vs ΛCDM 구분 SNR < 2σ | DR3로도 판가름 어려움. Euclid/CMB-S4 필요. |

### L13 KEEP 조건

| ID | 조건 | 결과 |
|----|------|------|
| **Q81** | 전체 ODE Δchi² > A01 Δchi² + 2 → 1차 근사에서 누락 있음 | 논문에서 전체 ODE 수치 결과를 메인으로 격상. |
| **Q82** | Ωm 진폭이 SQMH 평형 조건 n̄_eq = Γ₀/(3H+σρ_m) 에서 이론적으로 나옴 | 진폭 도출 성공. "Ωm은 이론 예측" 논문 핵심 주장 추가. |
| **Q83** | wₐ 2차 보정 ≥ 0.3 → DESI 중심값 방향으로 이동 | wₐ 갭 이론적으로 부분 해소. 논문 §3 업그레이드. |
| **Q84** | 진공 에너지 안정성 → Γ₀ 범위 ≤ 5자리 제약 | NF-27 부분 해소. Γ₀가 자연스러운 값임을 제한적 설명 가능. |
| **Q85** | DR3 Fisher: A01 vs ΛCDM 구분 SNR ≥ 3σ (특정 z-bin) | SQMH 명확한 검증 타임라인 확보. 논문 §5 추가. |

---

## 실행 순서

### Phase L13-0. 기준 고정 + 문서 준비

- `refs/l13_kill_criteria.md` K81-K85, Q81-Q85 기재 후 저장
- `base.l13.todo.md` WBS 작성
- `simulations/l13/` 디렉터리 생성 (ode/, amplitude/, wwa/, gamma0/, dr3/)

---

### Phase L13-O. 전체 ODE vs A01 근사 정밀 비교

> 이론: 서로 중복되지 않은 8인팀.

**배경**:
A01은 SQMH ODE의 1차 근사:
  ρ_DE(a) = ΩΛ × [1 + Ωm×(1−a)]
전체 ODE를 그대로 수치 적분하면 정확히 같은가, 다른가?
다르다면 어떤 항이 빠졌고, 그게 wₐ에 영향을 주는가?

**탐색 경로**:
1. **전체 SQMH ODE 수치 적분**:
   dρ_DE/dz = [Γ₀m_eff − σρ_DEρ_m − 3H(z)ρ_DE] / [−(1+z)H(z)]
   Friedmann: H²(z) = H₀²[Ωr(1+z)⁴ + Ωm(1+z)³ + ρ_DE(z)/ρ_crit]
   연립 ODE: odeint로 z=0→3
2. **A01 근사 H(z)와 비교**:
   H_ODE(z) vs H_A01(z) → 상대 오차 δH/H
3. **BAO 거리 차이**:
   D_M_ODE(z) vs D_M_A01(z) → chi² 차이
4. **DESI 직접 chi² 비교**:
   chi²_ODE vs chi²_A01 = 1655.78
   K81 판정: 차이 ≤ 0.5 → 근사 충분
   Q81 판정: 차이 > 2 → 전체 ODE 필요

**수치**: `simulations/l13/ode/full_ode_vs_a01.py`
- SQMH 전체 ODE odeint 구현
- Γ₀ normalization: ρ_DE(z=0) = ΩΛ × ρ_crit
- chi² 계산 및 A01 비교
- w(z) 추출 및 CPL 피팅

산출: `refs/l13_ode_derivation.md` + `simulations/l13/ode/full_ode_vs_a01.py`

---

### Phase L13-A. Ωm 진폭 도출 — 이론 vs 정규화

> 이론: 서로 중복되지 않은 8인팀.

**배경**:
A01: f(a) = 1 + Ωm×(1−a)
진폭 = Ωm. 이게 SQMH 방정식에서 나오는가, 아니면
E(0)=1 정규화에서 오는 artifact인가?

**탐색 경로**:
1. **SQMH ODE 1차 섭동 전개**:
   n̄(t) = n̄_eq(t) + δn̄(t)
   n̄_eq(t) = Γ₀/(3H + σρ_m) ≈ Γ₀/(3H) [σρ_m << 3H]
   δn̄(t) = 초기 조건에서 오는 이완 항
2. **ρ_DE 표현**:
   ρ_DE(t) = m_eff × n̄(t) = ρ_DE,eq(t) + m_eff×δn̄(t)
   ρ_DE,eq(t) = (Γ₀×m_eff)/(3H(t))
3. **ρ_DE,eq(z) 전개**:
   H²(z) ≈ H₀²[Ωm(1+z)³ + ΩΛ] (ΛCDM 근사)
   ρ_DE,eq(z) = C/H(z) → 스케일 인자 a로 표현
4. **z=0 정규화**:
   ρ_DE,eq(0) = ρ_DE,0 = ΩΛρ_crit → Γ₀m_eff = 3H₀×ΩΛρ_crit 결정
5. **결론 판정**:
   δρ_DE(z)/ρ_DE,0 의 선두 계수 = Ωm인가?
   → SQMH 평형 구조에서 나오면 Q82
   → E(0)=1 normalization에서만 나오면 K82
6. **물리적 해석**:
   Ωm이 진폭인 이유: "시공간 생성률 Γ₀가 오늘 ρ_DE를 설명하려면,
   과거 ρ_m이 많았을 때 소멸이 많았고 그 보정이 Ωm 크기"

**수치**: `simulations/l13/amplitude/amplitude_derivation.py`
- 해석적 전개 수치 검증
- 계수 계산: 실제 계수 vs Ωm
- 정규화 의존성 분리 테스트

산출: `refs/l13_amplitude_derivation.md` + `simulations/l13/amplitude/amplitude_derivation.py`

---

### Phase L13-W. wₐ 2차 보정 → DESI 중심값 방향

> 이론: 서로 중복되지 않은 8인팀.

**배경**:
A01(1차): w(z) = -1 + Ωm(1-a)/(3[1+Ωm(1-a)]) → wₐ ≈ -0.13
DESI 중심: wₐ ≈ -0.64
갭 = 0.51. DESI σ(wₐ) ≈ 0.6이므로 1σ 미만이지만 불안함.
2차 SQMH 보정이 wₐ를 얼마나 바꾸는가?

**탐색 경로**:
1. **2차 섭동 전개**:
   ρ_DE = ρ_DE^(0) + ε×ρ_DE^(1) + ε²×ρ_DE^(2) + ...
   여기서 ε = σρ_m/(3H) ~ Ωm×H₀t_P << 1
   ρ_DE^(1) = A01의 드리프트 항
   ρ_DE^(2) = 2차 보정
2. **2차 w(z) 계산**:
   w^(2)(z) = -(d ln ρ_DE^(2)/dt)/(3H)
   이게 A01의 w에 더해지는 보정
3. **비평형 초기 조건 보정**:
   n̄_init/n̄_eq ~ 10⁸³ (L11-R4 인플레이션 시나리오) 의 이완 기여
   n̄(t) = n̄_eq + (n̄_init − n̄_eq)×e^(-t/τ_relax)
   τ_relax = 1/(3H + σρ_m) ≈ 1/(3H)
   이완 기여가 wₐ에 어느 방향으로 작용하는가?
4. **wₐ 방향 분석**:
   2차 보정 wₐ^(2)의 부호는?
   → DESI 방향(-0.64)으로 이동하면 Q83
   → 반대 방향이면 K83
5. **결합 wₐ 예측**:
   wₐ_total = wₐ^(1) + wₐ^(2) + wₐ^(initial)
   DESI와의 비교: 갭이 줄었는가?

**수치**: `simulations/l13/wwa/wwa_second_order.py`
- 2차 ODE 수치 해
- wₐ 보정 계산
- 인플레이션 초기 조건 이완 효과
- DESI 비교

산출: `refs/l13_wwa_derivation.md` + `simulations/l13/wwa/wwa_second_order.py`

---

### Phase L13-Γ. 진공 에너지 안정성 → Γ₀ 새 제약

> 이론: 서로 중복되지 않은 8인팀.

**배경**:
L12-B: Bekenstein → Γ₀ 범위 43자리 → K72 KILL.
새 각도: 진공 에너지 안정성(vacuum energy stability) 조건.
현재 우주의 ρ_DE가 안정적으로 존재하려면 Γ₀는 어떤 값이어야 하는가?

**탐색 경로**:
1. **SQMH 평형 조건**:
   n̄_eq = Γ₀/(3H₀ + σρ_m0)
   n̄_eq × m_eff = ΩΛρ_crit (오늘 ρ_DE와 일치)
   → Γ₀ = 3H₀ × ΩΛρ_crit / m_eff + σρ_m0 × ΩΛρ_crit / m_eff
2. **안정성 조건**:
   d²V/dn̄² > 0 at n̄ = n̄_eq (Lyapunov 안정)
   이건 이미 NF-12로 증명됨 → Γ₀ > σρ_m0 × n̄_eq 필요
3. **더 강한 제약**: 양자 요동 안정성
   <δn̄²>/n̄_eq² < 1 (상대 요동 < 100%)
   → Poisson 요동: <δn̄²> = n̄_eq (NF-28)
   → n̄_eq > 1 필요 → Γ₀ > 3H₀/m_eff
   → m_eff가 플랑크 질량이라면? 원자 질량이라면?
4. **우주 나이 안정성**:
   τ_relax = 1/(3H + σρ_m) >> H₀⁻¹ (우주 나이보다 긴 이완 시간)
   → 이 조건에서 Γ₀ 하한?
5. **Stochastic 안정성 (Kramers)**:
   탈출 시간 τ_escape >> H₀⁻¹
   → Γ₀ / (σρ_m0) > 임계값

**수치**: `simulations/l13/gamma0/vacuum_stability.py`
- 안정성 조건별 Γ₀ 범위 계산
- 가장 강한 제약이 몇 자리를 주는가
- K84 판정: 범위 > 20자리 → KILL
- Q84 판정: 범위 ≤ 5자리 → PASS

산출: `refs/l13_gamma0_derivation.md` + `simulations/l13/gamma0/vacuum_stability.py`

---

### Phase L13-D. DR3 예측 문서화 + 검증 타임라인

> 이론: 서로 중복되지 않은 8인팀.

**배경**:
DESI DR3 예상 공개: 2026년 하반기.
A01 (순수 SQMH)의 구체적 DR3 예측이 없으면
논문의 "falsifiability" 주장이 약함.

**탐색 경로**:
1. **A01의 BAO 거리 예측**:
   SQMH ODE 수치 적분 → H(z) → D_M(z), D_H(z), D_V(z)
   DR3 예상 z-bins: z=0.295, 0.51, 0.706, 0.93, 1.317, 1.491, 2.33
   각 bin에서 A01 vs ΛCDM 예측 차이 계산
2. **DR3 Fisher 예측**:
   DR3 예상 정밀도 σ_DM(z), σ_DH(z) (DR2의 √2 개선 가정)
   A01 vs ΛCDM 차이 / σ_DR3 = SNR per bin
   합산 SNR: 3σ 이상이면 Q85
3. **가장 민감한 z-bin 식별**:
   어느 적색편이에서 A01 신호가 가장 강한가?
   → 관측 전략 제안
4. **wₐ 방향 테스트**:
   DR3가 wₐ → -0.64 확인하면 A01(wₐ=-0.13) KILL?
   DR3가 wₐ → 0 방향이면 ΛCDM KILL?
   SQMH가 살아남는 DR3 시나리오 분류
5. **문서화**:
   SQMH DR3 예측표 작성 (논문 Table 형식)
   "DR3에서 이 값이 나오면 SQMH 3σ 지지 / 이 값이면 2σ 반증"

**수치**: `simulations/l13/dr3/dr3_prediction.py`
- A01 BAO 거리 함수 계산
- DR3 예상 오차로 SNR 계산
- K85 판정: 합산 SNR < 2σ → KILL
- Q85 판정: 특정 bin SNR ≥ 3σ → PASS
- 논문 Table 자동 생성

산출: `refs/l13_dr3_prediction.md` + `simulations/l13/dr3/dr3_prediction.py`

---

### Phase L13-I. 통합 판정 + 논문 §4/§5 재구성

> 8인팀 전체 합의. 병렬 토의 후 취합.

**핵심 질문**:
1. K81 여부: 전체 ODE와 A01이 같은가? → 논문 메인 결과 결정
2. K82 여부: Ωm 진폭이 이론에서 나오는가? → §2 이론 섹션 강도 결정
3. K83 여부: wₐ 2차 보정이 0.3 이상인가? → §3 주요 주장 결정
4. K84 여부: Γ₀ 새 제약이 있는가? → NF-27 수정 여부
5. K85 여부: DR3 3σ 예측이 있는가? → §5 검증 섹션 유무

**산출**:
- `refs/l13_integration_verdict.md`
- `base.l13.result.md`
- 논문 서사 재구성 제안 (§2~§5)

---

## 산출 파일 목록

| 파일 | 내용 |
|------|------|
| `refs/l13_kill_criteria.md` | K81-K85, Q81-Q85 |
| `refs/l13_ode_derivation.md` | 전체 ODE vs A01 8인 토의 |
| `refs/l13_amplitude_derivation.md` | Ωm 진폭 이론 도출 8인 토의 |
| `refs/l13_wwa_derivation.md` | wₐ 2차 보정 8인 토의 |
| `refs/l13_gamma0_derivation.md` | 진공 안정성 → Γ₀ 제약 8인 토의 |
| `refs/l13_dr3_prediction.md` | DR3 예측 + 검증 타임라인 |
| `refs/l13_integration_verdict.md` | 8인 통합 판정 |
| `simulations/l13/ode/full_ode_vs_a01.py` | 전체 ODE 수치 |
| `simulations/l13/amplitude/amplitude_derivation.py` | 진폭 도출 수치 |
| `simulations/l13/wwa/wwa_second_order.py` | wₐ 2차 보정 수치 |
| `simulations/l13/gamma0/vacuum_stability.py` | 진공 안정성 수치 |
| `simulations/l13/dr3/dr3_prediction.py` | DR3 예측표 수치 |
| `base.l13.result.md` | L13 최종 결과 |
| `base.l13.todo.md` | WBS 체크리스트 |

---

## 기대 결과 시나리오

**최선 시나리오 (Q82+Q83+Q85 모두)**:
- Ωm 진폭이 SQMH 평형에서 이론 도출됨
- wₐ 2차 보정이 DESI 방향으로 0.3 이상 이동
- DR3에서 특정 z-bin 3σ 구분 가능
→ 논문 JCAP 상급 → PRD Letter 재검토 트리거

**중간 시나리오 (K81+K82+Q85)**:
- 전체 ODE ≈ A01 (근사 충분)
- 진폭은 정규화 artifact
- DR3 3σ 예측은 살아남음
→ "자유 파라미터 없이 DR3 3σ 예측이 있는 이론" — 여전히 JCAP 게재 가능

**최악 시나리오 (전부 KILL)**:
- 전체 ODE = A01
- 진폭 = 정규화
- wₐ 보정 < 0.1
- Γ₀ 범위 > 20자리
- DR3 SNR < 2σ
→ "A01 = Ωm 정규화 artifact, DR3 구분 불가" — 논문 재포지셔닝 필요

---

## 8인 재검토 약점 → L13 대응표

| 약점 | 담당 Phase | 예상 해소 가능성 |
|------|------------|-----------------|
| wₐ 수치 갭 (-0.13 vs -0.64) | L13-W | 중간 (2차 보정이 방향은 맞을 수 있음) |
| Ωm 진폭 이론 근거 없음 | L13-A | 높음 (평형 조건에서 나올 가능성) |
| 이론-현상론 서사 미완 | L13-O + L13-A | 높음 (전체 ODE = A01 확인 + 진폭 도출) |
| Γ₀ 기원 미완 (NF-27) | L13-Γ | 낮음 (L12도 실패, 완전 해소 어려움) |
| DR3 예측 미문서화 | L13-D | 매우 높음 (계산만 하면 됨) |

---

*작성: 2026-04-12. L12 10라운드 완료 + 8인 재검토 이후. 실행 보류.*
