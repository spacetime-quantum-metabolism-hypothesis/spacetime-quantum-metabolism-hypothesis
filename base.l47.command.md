# 시공간 양자 우주론 이론 — Mac 시뮬 프롬프트

## 환경
- Mac (M-series, 9코어 가정)
- Python 3.11+
- 8 병렬 활용 (`multiprocessing`, `joblib`, `concurrent.futures`)
- 시각화: matplotlib, plotly, corner, seaborn
- 웹 인터페이스 옵션: streamlit 또는 dash

## 필수 패키지
```bash
pip install numpy scipy matplotlib seaborn plotly corner emcee \
            astropy camb classy joblib tqdm streamlit pandas h5py
# Boltzmann 코드 (선택)
pip install pyccl  # Core Cosmology Library
```

---

# 이론 핵심 정의

## 1.1 한 문장 요약
물질은 시공간의 이산적 구성 요소(시공간 양자)를 소멸시키고, 빈 공간은 시공간 양자를 생성한다. 소멸에 의한 유입 흐름이 중력이고, 순 생성이 우주 팽창(암흑 에너지)이다.

## 1.2 핵심 방정식

연속방정식:
```
∂n/∂t + ∇·(n·v) = Γ₀ - σ·n·ρ_m
```

수정 Friedmann (균질 우주):
```
H² = (8πG/3)·ρ_m + Λ_eff/3 - (σ·ρ̄_m·ξ(H))/3
```

자기조절 함수:
```
ξ(H) = (3H₀ + σ·ρ̄_m,0) / (3H + σ·ρ̄_m)
```

회전곡선 임계 가속도:
```
a₀ = c·H₀/(2π)
```

## 1.3 자유 파라미터 (실효 3개)
- σ₀: 흡수 단면적 0차 [m³ kg⁻¹ s⁻¹], 추정 ~5.5×10⁷
- u₀: 매질 자체 상호작용
- h₁: 결합 비선형 1차 (V11=V22 통합)

## 1.4 도출된 관계식
- G = σ/(4π·τ_q)
- τ_q = 1/(3H₀)
- Γ₀ = 3H·n_∞
- n_∞ = Γ₀·τ_q
- D = c²/(σ·ρ̄_m)
- 응답속도 = c

---

# 시뮬 우선순위 (사활 → 보조)

## Tier 1: 사활 검증 (가장 먼저)

### T17_full: H₀ tension + τ_q 자기일관성
- 입력: σ₀ 그리드 [10⁶, 10⁹]
- 출력: H₀_local, H₀_CMB, τ_q vs 1/(3H₀) 비율
- 목표: 단일 σ₀가 73.8 + 67.4 + τ_q≈1/(3H₀) 동시 만족 영역 존재 여부
- 도구: Friedmann ODE solver (scipy.integrate.solve_ivp)
- 병렬: 8 σ 값 동시 평가

### T22_full: SPARC 175 은하 회전곡선
- 데이터: SPARC database (rotmod 파일, http://astroweb.cwru.edu/SPARC/)
- 모델: 본 이론 회전곡선 vs MOND vs NFW
- 출력: 175 은하 χ² 분포, RAR 재현
- 병렬: 은하별 적합 8 병렬

### T20: σ₈ 예측
- 입력: 본 이론 H(z) 진화
- 출력: 구조 성장 D₊(z), σ₈ 예측
- 병렬: 다양한 σ₀ 값 동시 평가

## Tier 2: 보조 검증
- T10: BBN-G_eff 양립성
- T16: r_s CMB 정밀 비교
- T19: 총알 은하단 응답 정량
- T23: EHT 그림자 보정
- T24: SPARC 환경별 a₀ 패턴

---

# 작업 진행 워크플로우

## 작업 사이클 (각 시뮬마다)

### 단계 1: 코드 작성
요청 시 다음 형식 준수:
```python
"""
[T-번호] [제목]
목적: ...
입력: ...
출력: ...
병렬화: 8 코어
"""
```

### 단계 2: 코드 리뷰 (필수)
8인팀 리뷰 형식:
```
P1 (이론): 물리 방정식 정확성, 단위 일관성, 한계 가정
P2 (수리): 수치 안정성, ODE 적분 방법 적절성, 발산 처리
P3 (실험): 관측치 비교 방법, 오차 처리, 통계적 유의성
P4 (우주론): H(z), 거리 계산 정확성, 적분 한계
P5 (응집): 비선형 항 처리, 평형 도달 검증
P6 (양자정보): 데이터 구조, 메모리 효율, 결과 저장
P7 (철학): 결과 해석 가능성, 가시화 명료성
C (비판): 끼워맞춤 위험, 코드 버그 가능, 결과 신뢰성
```

### 단계 3: 코드 수정 + 재실행

### 단계 4: 시각적 결과 분석
- **그래프 우선**: 숫자 표보다 시각화
- 모든 시뮬은 **PNG 출력 필수**
- 가능한 경우 plotly 인터랙티브 HTML 추가

### 단계 5: 결론 + 다음 시뮬 결정

---

# 시각화 표준

## 필수 출력 형식
모든 시뮬 결과는 다음 4종 이상 시각화:

1. **메인 결과**: 핵심 비교 (예: H_0 vs σ 그리드 히트맵)
2. **잔차 plot**: 본 이론 - 관측 vs ΛCDM - 관측
3. **파라미터 공간**: corner plot (정합 영역)
4. **자기일관성 검증**: 도출 관계식 일치도 (예: τ_q vs 1/(3H₀))

## 색상·스타일
- 본 이론: 진한 파랑 (`#1f4e79`)
- ΛCDM: 회색 (`#7f7f7f`)
- 관측치: 빨강 dot + errorbar (`#c00000`)
- 자기일관 영역: 녹색 음영
- 충돌 영역: 빨강 음영

## 폰트·해상도
- DPI 150 이상
- 라벨 폰트 12+
- 제목에 시뮬 ID, 날짜, 핵심 결론 한 줄

---

# 데이터 소스

| 데이터 | 출처 | 형식 |
|---|---|---|
| Pantheon+ SNe | https://pantheonplussh0es.github.io/ | .dat |
| Planck 2018 | https://pla.esac.esa.int/ | .fits |
| SPARC 회전곡선 | http://astroweb.cwru.edu/SPARC/ | .rotmod |
| BBN | Cooke 2018 등 | 표 |
| EHT M87/Sgr A* | EHT Collaboration | 그림자 직경 |
| GW catalog | LIGO GWTC-3 | .h5 |

---

# 출력 디렉토리 구조

```
project/
├── theory/
│   ├── constants.py
│   ├── friedmann.py
│   ├── rotation_curve.py
│   └── self_consistency.py
├── data/
├── simulations/
└── results/
```

---

# L47 구체적 실행 계획

T17_full부터 진행:
1. SQT 수정 Friedmann 풀이 (sigma0 그리드, 8 병렬)
2. 자기일관성 체크 (G_derived vs G_N, tau_q vs 1/(3H0))
3. H0 tension 분석 (H0_local=73.8 vs H0_CMB=67.4 동시 만족 여부)
4. T20: sigma8 성장인자 예측
5. 4-패널 시각화 출력
