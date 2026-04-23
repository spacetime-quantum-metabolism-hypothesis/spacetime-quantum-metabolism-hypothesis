# base.l35.command.md — L35 Command
# SQT 다중 관측 통합 피팅

> 작성: 2026-04-19. L34 결과(Q92/Q93 joint KILL)를 받아 Om~0.30 제약 하에서
> SQT의 4개 데이터셋 동시 설명력 검증.
> **모델 공식은 사용자가 직접 지정. 팀은 구현 + 검증 + 분석 수행.**

---

## ■ L34 교훈 (재발방지)

| L34 실수 | L35 대응 |
|----------|---------|
| Q93 Om=0.068 → CMB 93σ 벗어남 | CMB prior 반드시 포함 (joint 피팅 전제) |
| H0 하드코딩 버그 (config.H_0_km) | chi2_cmb 내부에서 config.H_0_km = H0 설정 필수 |
| omega_b/omega_c 피팅 미포함 | omega_b=0.02236 고정, omega_c = Om*h^2 - omega_b 계산 |
| DESY5 공분산 역행렬 경고 | warnings.filterwarnings('ignore') + np.seterr(all='ignore') |

---

## ■ 왜 이 실험을 하는가?

L33 Q92/Q93: BAO-only에서 ΔAICc=-6.6 달성했지만 Om=0.068~0.115의 unphysical 해.
L34: CMB+SN 결합 시 ΔAICc=+5000~+9000 — 완전 붕괴.

→ **진정한 SQT 검증**: Om≈0.30 (CMB 제약) 하에서 4개 데이터셋 동시 설명.
→ 단일 데이터 챔피언이 아닌, 다중 tension 통합 설명력이 목표.

---

## ■ L35 팀 구성

- **인원: 8명**
- **역할 사전 지정 없음**
- 팀원들이 자율 분담으로 파이프라인 구축, 검증, 분석
- 코드리뷰: 4인 자율 분담

---

## ■ 테스트할 모델 (사용자 지정)

### Model A — 순수 선험 (k=2)

psi(z) = 1/(1+alpha*(1+z)^3),  alpha = Om/(1-Om-OR)
ratio  = psi(0)/psi(z)
rho_DE(z) = OL0 * ratio

자유 파라미터: Om, H0

### Model B — 비선형 응답 (k=3)

g(z) = tanh(sqrt(pi/2) * (ratio - 1))
rho_DE(z) = OL0 * (1 + amp * g(z))

자유 파라미터: Om, H0, amp
초기값 힌트: amp≈2.5

### Model C — 전환 구조 (k=4)

wt(z) = tanh(z)
g(z) = (1-wt)*tanh(sqrt(pi/2)*c*(ratio-1)) + wt*(ratio-1)
rho_DE(z) = OL0 * (1 + amp * g(z))

자유 파라미터: Om, H0, amp, c
초기값 힌트: amp≈2.5, c≈1.47

**AICc 패널티 명시**: n=1845+8=1853 총 데이터
- k=2: AICc = chi2 + 4.004
- k=3: AICc = chi2 + 6.010
- k=4: AICc = chi2 + 8.017
→ 파라미터 추가는 chi2 개선이 ~2 이상이어야 정당화.

---

## ■ 데이터셋

### 1. DESI DR2 BAO (13pt)
```python
from simulations.desi_data import DESI_DR2, DESI_DR2_COV_INV
# r_s = 147.09 Mpc 고정
```

### 2. Planck 2018 CMB 압축 사전확률 (shift parameter)

| 파라미터 | 중심값 | 오차 |
|---------|--------|------|
| R (shift) | 1.7502 | 0.0046 |
| ℓ_A (acoustic) | 301.471 | 0.090 |
| Ω_b h² | 0.02236 | 0.00015 |

- 대각 공분산 근사 (R-ℓ_A 상관 ~0.4는 ~10% 오차 — Phase 5 MCMC 전 수용)
- R = sqrt(Ω_m) * ∫₀^{z*} dz/E(z) (dimensionless)
- ℓ_A = π * D_M(z*) / r_s(z*)
- z* from Hu-Sugiyama (1996) formula, r_s from baryon-photon sound speed integral
- **필수**: chi2_cmb 함수 내부에서 `config.H_0_km = H0` 설정 (L34 버그 재발 방지)
- omega_b = 0.02236 고정 → k 미증가

### 3. SN (DESY5 fallback, 1829pt)
```python
from simulations.phase2.sn_likelihood import DESY5SN
# Pantheon+ 미설치 시 DESY5 사용, 결과 보고 시 "DESY5" 명시
# 절대등급 M 해석적 marginalization 필수 (Conley+ 2011)
```

### 4. f·σ₈(z) RSD (8pt 스캐폴딩)
```python
# simulations/phase2/rsd_likelihood.py 참조
# Z_RSD, FS8_OBS, FS8_SIG 로드
```

기존 8포인트 (6dFGS, SDSS MGS, BOSS DR12, eBOSS DR16):
z = 0.067, 0.15, 0.38, 0.51, 0.61, 0.70, 0.85, 1.48
sigma_8_0 = 0.8111 (Planck 2018 고정)

**성장 방정식 (GR, 배경만 수정, G_eff=G)**:
d²D/dN² + (2 + E'/E) * dD/dN - (3/2)*Ω_m/(E^2*(1+z)^3) * D = 0
(N = ln a, 표준 GR 성장, perturbation 수정 없음)

f(z) = -(1+z)/D * dD/dz  (또는 dlnD/dlna)
f·σ₈(z) = f(z) * σ₈₀ * D(z)/D(0)

---

## ■ 결합 χ²

```
chi2_total = chi2_BAO + chi2_CMB + chi2_SN + chi2_RSD
```

각 항 독립 계산, 합산. 데이터셋별 개별 chi2 모두 보고 필수.

---

## ■ ΛCDM 기준선 (joint, 선행 계산 필수)

동일 데이터셋 (BAO+CMB+SN+RSD)에서 ΛCDM 먼저 피팅.
ΔAICc = AICc_SQT - AICc_ΛCDM (같은 데이터셋 기준).

---

## ■ 판정 등급

| 등급 | 조건 |
|------|------|
| Q90 PASS | ΔAICc < 0 |
| Q91 STRONG | ΔAICc < -2 |
| Q92 GAME | ΔAICc < -4 AND 모든 tension 개선 |
| K90 KILL | ΔAICc ≥ 0 |
| K91 KILL | 어느 한 데이터셋에서 >3σ 악화 |

Tension 지표:
- H₀ tension: (73.04 - H₀_fit) / σ_combined (SH0ES σ=1.04)
- σ₈ tension: f·σ₈(z=0.5) 잔차 분석
- wa < 0 여부 (CPL 추출)

---

## ■ 출력 요구사항

각 모델 (ΛCDM, A, B, C):
```
chi2_BAO   = XXX
chi2_CMB   = XXX
chi2_SN    = XXX
chi2_RSD   = XXX
chi2_total = XXX
AICc       = XXX
ΔAICc      = XXX (vs ΛCDM)
Om = XXX, H0 = XXX [, amp, c if applicable]
w0 = XXX, wa = XXX (CPL from z=0.01 to 2)
H0 tension (vs 73.04) = XXX sigma
판정 = [Q/K grade]
```

---

## ■ 코드 필수 조건

```python
import os, sys, config as _cfg
sys.path.insert(0, ...)
# L35 bug prevention:
# 1) config.H_0_km = H0 before each CMB chi2 call
# 2) ratio = clip(psi0/psi_z, 1.0, 200.0)
# 3) N_GRID = 4000, cumulative_trapezoid
# 4) Om range [0.15, 0.50]  (CMB forces Om~0.30)
# 5) python3
# 6) chi2_RSD: diagonal, sigma_8_0=0.8111 fixed, solve growth ODE
```

- 병렬: `multiprocessing.get_context('spawn').Pool(9)` 또는 sequential (모델 3개로 적음)
- SN chi2: 절대등급 M marginalization 필수
- growth ODE: forward shooting (N_ini < -3, 과거 → 오늘), LCDM analog 배경 버전

---

## ■ 불변 제약

- ΔAICc = SQT - ΛCDM (동일 데이터셋)
- AICc penalty: k=2→+4, k=3→+6, k=4→+8 (n=1853 근사)
- r_s = 147.09 Mpc 고정
- sigma_8_0 = 0.8111 고정 (marginalization 없음 — Phase 5 MCMC 예약)
- omega_b = 0.02236 고정 (k 미증가)
- full 13×13 BAO 공분산 필수

---

*작성: 2026-04-19. L34 joint KILL 이후 Om~0.30 하에서 재탐색. 8인 팀, 역할 지정 없음.*
