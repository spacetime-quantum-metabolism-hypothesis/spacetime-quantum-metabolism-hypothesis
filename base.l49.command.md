# L49 (T22_full): SPARC 회전곡선 시뮬 프롬프트

## 환경 사양
- **하드웨어**: Mac (Apple Silicon M-series, 9코어)
- **병렬**: 8 코어 (joblib)
- **Python**: 3.11+
- **Web**: SPARC 데이터 다운로드 (curl/requests)

## 필수 패키지
```bash
pip install numpy scipy matplotlib seaborn pandas h5py tqdm \
            joblib plotly astropy requests
```

---

# T22_full 시뮬 사양

## 목적

L48 (T17/T20) 결과 검토:
- σ_sc (자기일관) ≈ 1.17×10⁸
- σ_tension ≈ 2.34×10⁸
- σ_σ8 ≈ 5.6×10⁷
- **세 값 불일치, 단일 σ_0 만족 영역 부재**

T22가 4번째 σ_0 추출 → **진단 결정**:
- T22 σ_0가 위 셋 중 하나와 일치 → 그 영역으로 수렴
- 모두와 다른 4번째 값 → 본 이론 단일 σ_0 *전면 실패*
- T22가 *영역*만 부여 (σ_0 결정 못 함) → 추가 자유도 필요

## 핵심 검증 항목

1. **a_0 추출**: 175 은하 회전곡선 적합 → β·c/τ_q 형식에서 β 추출
2. **a_0 보편성**: 은하별 a_0 분산 → 본 이론 시간 불변 시나리오 (A1) 검증
3. **σ_0 일치성**: T22 σ_0가 T17/T20 영역과 일치 여부
4. **환경 의존**: h_1 비선형 항이 SPARC 다양성 재현 가능 여부
5. **MOND/NFW 대비**: χ² 비교

## 데이터 소스

**SPARC database** (Lelli, McGaugh, Schombert 2016):
- URL: http://astroweb.cwru.edu/SPARC/
- 175 은하 (rotation curves + mass models)
- 파일: `Rotmod_LTG.zip` (모든 은하 통합)
- 형식: 각 은하당 .dat (Rad, Vobs, errV, Vgas, Vdisk, Vbul, SBdisk, SBbul)

대안: SPARC 메인 표 `SPARC_Lelli2016c.mrt`

## 본 이론 회전곡선 모델

### 가설 (재구축 III)

은하 외곽에서 양자 매질 평형:
```
∇·(n·v) = -σ_0·n·ρ_m
```

**deep-MOND 한계** (a < a_0):
```
a_total² = a_N · a_0,    a_0 = β·c/τ_q
```

**Newton 한계** (a >> a_0):
```
a_total = a_N
```

**전이 보간** (Milgrom 표준):
```
a_total = a_N · μ⁻¹(a_total/a_0)
```
또는 simple interpolation:
```
a_total = (1/2) [a_N + sqrt(a_N² + 4·a_N·a_0)]
```

### 본 이론 추가 (V11 환경)
```
a_0_local = a_0_universal · (1 + h_1·δn/n_∞)
```
환경별 미세 변동 (보편 a_0 + 보정).

### Newton baryonic
```
a_N(r) = G·M_baryonic(<r)/r²
M_baryonic = M_gas + M_disk + M_bul (Vgas² + Υ·Vdisk² + Υ·Vbul²)
```
Υ는 mass-to-light ratio (자유 파라미터, ~0.5).

---

# 단위 변환 (중요)

```
G_N = 4.302e-6 kpc·(km/s)²/M_sun
c   = 2.998e5 km/s
H0  = 70 km/s/Mpc (은하 적합용 중간값)
τ_q = σ_0/(4π·G_N_SI)  [SI: s]
a_0 = β·c/τ_q           [SI: m/s²]

단위 변환:
1 (km/s)²/kpc = 3.241e-14 m/s²
a_0_obs = 1.2e-10 m/s² ≈ 3703 (km/s)²/kpc

σ_0 추출:
σ_0 = β·c_SI·4π·G_N_SI / a_0_SI   [m³/(kg·s)]
```

---

# 수치 진단 표 (T22 완성 목표)

```
| 검증     | 요구 σ_0 (시뮬) | log σ_0 |
|---------|----------------|---------|
| T17 H_0 | 2.34×10⁸      | 8.37    |
| T17 자기 | 1.17×10⁸      | 8.07    |
| T20 σ_8 | 5.6×10⁷       | 7.75    |
| T22 a_0 | ?             | ?       |  ← L49 결과
```

T22 결과로 표 완성 → 본 이론 운명 결정.

---

# 시각화 (5-패널)

- **(a) RAR**: log a_N vs log a_obs, 본 이론/MOND 예측 곡선
- **(b) a_0 분포**: 은하별 추출 a_0 히스토그램, σ(log a_0) < 0.1 dex 조건
- **(c) χ² 비교**: SQT vs MOND vs NFW (CDF + 분포)
- **(d) 자기일관 검증**: T22 σ_0 → T17/T20/T22 4개 표
- **(e) 환경 의존**: SBdisk vs a_0, h_1 추출 (V11)

---

# 색상 표준
- 본 이론: #1f4e79 (진한 파랑)
- MOND: #2e7d32 (녹색)
- NFW/ΛCDM: #7f7f7f (회색)
- 관측치: #c00000 (빨강 + errorbar)
