# base.l36.command.md — L36 Command
# SQT wa<0 복원 탐색 (L35 한계 해결)

> 작성: 2026-04-20. L35 결과(Model B Q91 STRONG, ΔAICc=-4.83, wa=+0.18) 이후.
> **핵심 목표**: wa<0 복원 가능한 SQT 구조 탐색. phantom 방향 허용 모델 검증.

---

## ■ L35 한계 요약 (재발방지)

| L35 문제 | L36 대응 |
|---------|---------|
| Model A ratio^1 → (1+z)^3 발산 | Model A': ratio^n (n=1/3), 완만 감쇠 |
| Model B wa=+0.18>0 (DESI 반대 방향) | Model B': gamma<0 허용, phantom 가능 |
| Model C amp=0.10(하한), c=3.0(상한) 경계 박힘 | Model C': 경계 재설정 + 50개 초기값 |
| Model D (신규) 미탐색 | Model D: amp<0 허용, phantom 구조 |

---

## ■ 테스트할 모델

### Model A' — 완만 감쇠 선험 (k=2 또는 k=3)

rho_DE(z) = OL0 * ratio(z)^n
- n=1/3 고정 (k=2): 고z에서 (1+z)^1 증가 (발산 제거)
- n 피팅 (k=3): 최적 power law 탐색

자유 파라미터: Om, H0 [, n]
n 초기값: 1/3; n 범위: [0.05, 1.5]

### Model B' — V(ψ) 비대칭 (k=4, phantom 허용)

c = 1.47 (고정)
g(z) = tanh(sqrt(pi/2)*c*(ratio-1)) + gamma*(ratio-1)^2
rho_DE = OL0 * (1 + amp * g)

자유 파라미터: Om, H0, amp, gamma
- amp 범위: [0.01, 3.0]
- gamma 범위: [-0.05, 0.5]  (gamma<0 → phantom 가능)
- 주의: gamma<0 + 큰 ratio에서 rho_DE<0 → E² 음수 시 자동 reject

### Model C' — 전환 구조 재최적화 (k=4)

L35 Model C와 동일 수식, 경계/초기값만 변경:
- amp 범위: [0.5, 5.0] (L35 [0.1, 5.0]에서 하한 상향)
- c 범위: [0.5, 2.5] (L35 [0.5, 3.0]에서 상한 하향)
- 초기값 50개 (L35 20개에서 확장)
- 수렴 실패 시 Powell 교차 확인

### Model D — phantom 자연 구조 (k=4)

rho_DE(z) = OL0 * (1 + amp * (ratio-1) * exp(-beta*z))

자유 파라미터: Om, H0, amp, beta
- amp 범위: [-3.0, 3.0]  (amp<0 → rho_DE < OL0 at intermediate z → phantom)
- beta 범위: [0.01, 5.0]  (감쇠 스케일)

물리: amp<0, beta>0이면 rho_DE는 중간 z에서 OL0보다 낮아졌다가 고z에서 OL0로 수렴
→ phantom (w<-1) 가능

---

## ■ 실행 우선순위

1. Model B' (phantom 허용 구조 검증) → 가장 빠른 결과 필요
2. Model D (phantom 자연 구조) → 신규 탐색
3. Model C' (수렴 재시도)
4. Model A' fixed (k=2, 빠름)
5. Model A' free (k=3, n 피팅)

---

## ■ 데이터셋 (L35와 동일)

- DESI DR2 BAO: 13pt, 13×13 full 공분산, r_s=147.09 Mpc
- Planck 2018 CMB shift: R=1.7502±0.0046, lA=301.471±0.090, Obh2=0.02236±0.00015
- DESY5 SN: 1829개, M marginalization
- RSD f·σ₈: 8pt (6dFGS~eBOSS)
- n_total = 1853, ΛCDM AICc_baseline = 1670.12 (L35에서 확정)

---

## ■ AICc 패널티 (n=1853)

- k=2: AICc = chi2 + 4.004
- k=3: AICc = chi2 + 6.008
- k=4: AICc = chi2 + 8.013

---

## ■ 판정 기준 (L35 + 추가)

| 등급 | 조건 |
|------|------|
| Q90 PASS | ΔAICc < 0 |
| Q91 STRONG | ΔAICc < -2 |
| Q92 GAME | ΔAICc < -4 AND 모든 tension 개선 |
| K90 KILL | ΔAICc ≥ 0 |
| K91 KILL | 어느 한 데이터셋에서 >3σ 악화 |
| **K92 INVALID** | **파라미터 경계 고착 (boundary-pinned)** |

tension 지표:
- wa < 0 여부
- H₀ tension (vs SH0ES 73.04, σ=1.04)
- sigma_8 tension: f·σ₈ residuals

---

## ■ 출력 요구사항

각 모델:
```
chi2_BAO, chi2_CMB, chi2_SN, chi2_RSD, chi2_total
AICc, ΔAICc (vs ΛCDM baseline 1670.12)
파라미터값 + 경계 도달 여부
w0, wa (CPL z=0.01~2)
H₀ tension (sigma)
판정
```

---

## ■ 코드 필수 조건

- chi2 함수: l35_test.py에서 import (검증 완료 버전)
- config.H_0_km = H0 (L34 버그 재발방지)
- ratio clipping [1, 200] (또는 Model A'는 clipping 없이 n=1/3으로 자연 수렴)
- E²<0 즉시 None return (rho_DE<0 region reject)
- K92 경계 도달 판정: abs(param - bound) < 1e-3 * (bound_hi - bound_lo)

---

*작성: 2026-04-20. L35 Model B Q91 STRONG (ΔAICc=-4.83, wa=+0.18) 이후 wa<0 복원 탐색.*
