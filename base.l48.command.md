# 시공간 양자 우주론 — Mac 시뮬 프롬프트 (재구축 III 기준)

## 환경 사양
- **하드웨어**: Mac (Apple Silicon M-series, 9코어 가정)
- **병렬**: 8 코어 활용 (1 코어는 OS/IDE)
- **Python**: 3.11+
- **Web**: 데이터 다운로드 + 결과 인터랙티브 viewer

## 필수 패키지 설치
```bash
pip install numpy scipy matplotlib seaborn pandas h5py tqdm
pip install joblib plotly corner
pip install astropy emcee getdist
pip install camb pyccl  # 선택
pip install streamlit   # 선택
```

---

# 이론 요약 (재구축 III 후)

## 1. 공리 (정직 6개)
```
a1: 양자 + 물질 → 소멸 (메커니즘)
a2: 양자 에너지 = 흡수된 에너지 (보존)
a3: 평균 우주공간 균일 생성 (등방성)
a4: 공간 = 양자 패턴 (β-해석)
a5: 물질 = 안정 양자 패턴 (실체)
a6: 패턴 유지율 ∝ 패턴 에너지 (선형 흡수)
```

## 2. 핵심 ODE 시스템 (3개 변수)
```
dn/dt = Γ_0 - 3Hn - σ_0·n·ρ_m
dρ_m/dt = -3Hρ_m + σ_0·n·ρ_m·ε/c²
H² = (8πG/3)(ρ_m + n·ε/c²) + Λ_eff/3
```

## 3. 결정 관계식
```
G = σ_0/(4π·τ_q)         # τ_q 매질 고유 (시나리오 A)
Λ_eff = 8πG·n_∞·ε/c²    # 우주상수 자동 차수 일치
a_0 = β·c/τ_q            # 시간 불변 (시나리오 A1)
n_∞ = Γ_0·τ_q            # 정상상태
```

## 4. 자유 파라미터 (정직 6개)

| 파라미터 | 의미 | 단위 |
|---|---|---|
| σ_0 | 흡수 단면적 | m³ kg⁻¹ s⁻¹ |
| τ_q | 매질 고유 시간 | s |
| Γ_0 | 생성률 | m⁻³ s⁻¹ |
| u_0 | 매질 자체 상호작용 | (시뮬에서 정의) |
| h_1 | 결합 비선형 | 무차원 |
| β | a_0 비례계수 | 무차원 |

## 5. 시나리오 분기
- **X**: n_∞ ~ 10²⁵ m⁻³ (양자 ~ 원자 척도)
- **Y**: n_∞ ~ 10⁴¹ m⁻³ (양자 ~ 핵 척도)

---

# 시뮬 우선순위

## Tier 1 (사활)

### T17_full: H_0 tension + 동역학 ODE
- ODE 시스템 풀이 (위 3개 변수)
- σ_0 × Γ_0 그리드 (각 20점, 총 400 조합)
- H_0_local (z<0.1) vs H_0_CMB (z=1100) 추정
- **목표**: σ_0 영역에서 73.8 + 67.4 동시 만족

### T22_full: SPARC 175은하 회전곡선
- 데이터: SPARC database 다운로드
- 본 이론 모델 vs MOND vs NFW
- **목표**: ΛCDM+NFW 대비 χ² 동등 또는 우월

### T20: σ_8 정량
- 본 이론 H(z)에서 구조 성장 D_+(z) 풀이
- **목표**: σ_8 ≈ 0.81 (Planck) 또는 0.76 (KiDS)

---

# L48 실행 계획

## T17_full 구체적 단계

1. SQT ODE 풀이 (sigma0 x Gamma0, 20x20, 8 병렬)
2. 자기일관성: G_derived = sigma0/(4pi*tau_q) vs G_N, tau_q vs 1/(3H0)
3. H0 tension: H0_local=73.8 vs H0_CMB=67.4 동시 만족 영역
4. T20 sigma8 성장인자 계산
5. 4-패널 시각화 (H0_local 등고선, H0_CMB 등고선, 교차영역, 최적 H(z))

## 시각화 표준
- 본 이론: #1f4e79 (진한 파랑)
- ΛCDM: #7f7f7f (회색)
- 관측치: #c00000 (빨강 + errorbar)
- 자기일관 영역: #90ee90 음영
- 충돌 영역: #ffcccc 음영
