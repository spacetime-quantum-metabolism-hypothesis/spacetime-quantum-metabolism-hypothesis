# base.l38.command.md — L38 Command
# Model D 학술 발표 검증 (L37 패치 포함)

> 작성: 2026-04-20. L37 완료(ΔAICc=-8.44 Q91, L37 코드리뷰 완료) 이후.
> L37 코드리뷰 발견 패치: P1(경계감지), P2(Task1 profile), P3(H0 오차), P4(BAO k=3) 전량 L38에 반영.

---

## ■ 목표

L37에서 SQT 범위 확정. L38은 Model D Q91 결과의 학술 발표 가능성 최종 검증:

1. Bootstrap robustness (ΔAICc=-8.44 통계적 안정성)
2. Profile robustness (P2 적용: Om/H0 재최적화 grid scan)
3. Model simplification (Occam razor: k=2,3 vs k=4)
4. w₀wₐCDM 직접 비교 (CPL이 SQT를 이기는가?)
5. BAO-only 재실행 (P4: k=3, beta 고정, 과소결정 회피)
6. 잔차 분석 (ΔAICc=-8.44 어느 데이터에서 오는가?)

이론 확장 없음. 현 결과 투고 가능 수준 확정이 목표.

---

## ■ 패치 요구사항 (L37 코드리뷰 → L38 반영)

### P1: 경계 감지 유틸 (전 Task 공통)

```python
def _at_boundary(params, bounds, tol=1e-3):
    for p, (lo, hi) in zip(params, bounds):
        span = hi - lo
        if span == 0: continue
        if abs(p - lo) < tol*span or abs(p - hi) < tol*span:
            return True
    return False
```

모든 worker 반환값에 `boundary: bool` 플래그. boundary=True이면 K92 INVALID.

### P2: Task 1 Profile 방식 robustness

각 (amp, beta) 격자점에서 Om, H0 재최적화:

```python
# amp, beta 고정, Om/H0 mini-최적화
def _profile_at(amp, beta):
    def obj(p):
        Om, H0 = p
        return chi2_all(E_D(Om,amp,beta), Om, H0)
    return minimize(obj, [0.322, 66.98], method='NM', maxiter=300).fun
```

출력: profile dAICc(amp,beta) — 실제 파라미터 공간 robustness

### P3: H0 오차 profile 방식 (Task 5)

대각 Hessian 폐기. 고정 H0에서 다른 파라미터 재최적화:

```python
for H0_test in np.linspace(H0_best - 3, H0_best + 3, 25):
    def obj_fixed(p):  # Om, amp, beta만 최적화
        ...
    chi2_at_H0 = minimize(...).fun
# delta_chi2 = 1 지점 → 1sigma H0 오차
```

### P4: BAO-only k=3 (과소결정 회피)

L37 Task 3 수정: 4파라미터 BAO-only는 K92 INVALID.
L38에서는:
- beta = 3.533 고정 (L36 best)
- amp 범위 [0.5, 10.0] 확장
- 자유 파라미터: Om, H0, amp (k=3)
- 13점 vs 3파라미터 → 과소결정 아님

---

## ■ Task 목록

### Task 0: ΛCDM Baseline 재확인

L35/L36 사용값 재검증:
- ΛCDM fit: Om, H0 최적화
- chi2_BAO, chi2_CMB, chi2_SN, chi2_RSD, AICc 재확인
- 기존 AICc=1670.12 재현 확인 후 진행

### Task 1: Bootstrap Robustness

방법: Parametric bootstrap, Model D 중심, 500회 (8-worker 병렬)

데이터 섭동:
- BAO: N(theory_D, COV_BAO) multivariate (forward COV = inv(COV_INV))
- CMB: N(theory_D, diag(CMB_SIG²))
- RSD: N(theory_D, diag(FS8_SIG²))
- SN: 섭동 없음 (구현 복잡성, limitation으로 명시)

각 bootstrap 샘플:
- ΛCDM fit (k=2, 3 starts, maxiter=200)
- Model D fit (k=4, 1 start from best-fit, maxiter=300)
- ΔAICc_boot = AICc_D - AICc_LCDM on same data

판정:
- PASS: ΔAICc<-4 비율 > 90%, amp/beta 단봉 분포
- CONDITIONAL: 70-90%
- FAIL: <70%

출력: ΔAICc histogram, amp/beta scatter

### Task 2: Profile dAICc Robustness (P2)

20×20 (amp, beta) 격자, ±30% around L36 best-fit
각 점: Om/H0 재최적화 (k=2 mini-fit, 3 starts, maxiter=300)
→ profile dAICc(amp, beta)

판정:
- PASS: profile dAICc<-6 영역 >30%
- CONDITIONAL: 10-30%
- FAIL: <10%

### Task 3: Model Simplification

비교:
- D_k4: amp, beta free → L36 ΔAICc=-8.44
- D_k3_betafixed: beta=3.533 고정, Om/H0/amp free → k=3
- D_k3_ampfixed:  amp=0.8178 고정, Om/H0/beta free → k=3
- D_k2_bothfixed: amp=0.8178, beta=3.533 고정, Om/H0 free → k=2

판정: 최소 k로 ΔAICc < -4 유지되는가?

### Task 4: w₀wₐCDM 비교

CPL 모델:
E²(z) = OR(1+z)⁴ + Om(1+z)³ + OL0*(1+z)^(3(1+w0+wa)) * exp(-3wa*z/(1+z))

파라미터: Om, H0, w0, wa (k=4)
범위: Om[0.15,0.50], H0[55,82], w0[-2,0], wa[-3,3]

비교:
- ΛCDM AICc=1670.12
- CPL AICc=???
- SQT Model D AICc=1661.68

판정:
- SQT > CPL: ΔAICc(SQT-CPL) < 0 → SQT 발표 가치 확정
- SQT < CPL: ΔAICc(SQT-CPL) > 0 → 발표는 "이론 동기" 중심

### Task 5: BAO-only k=3 재분석 (P4)

beta=3.533 고정, k=3: Om, H0, amp free
amp 범위: [0.5, 10.0] (확장)
경계 도달 시 K92 INVALID 자동 판정
30 starts, 8-worker 병렬

CPL wa 추출:
- BAO-only wa vs Combined wa=+0.367 비교
- wa 역전 가설 재검증

### Task 6: 잔차 분석

Model D vs ΛCDM at best-fit:

BAO (13점):
- 각 DESI 관측량별 chi2_i = (obs-theory)²/sigma_i_marginal²
- marginal sigma = sqrt(diag(COV_BAO))
- 주의: full covariance 사용한 피팅과 불일치 → 근사값 표시

CMB (3점): (theory-obs)²/sig² 각각

SN: ΔAICc의 SN 기여 = chi2_SN(D) - chi2_SN(LCDM)

RSD (8점): (theory-obs)²/sig² 각각

판정:
- SN 고z 집중 → quintessence 일반 특성
- SN 저z 집중 → SQT 특유 거동 가능성
- BAO/RSD 개선 → 강한 물리적 지지

### Task V1a: (1-ψ) 자유 진폭 Model (정규화 미강제)

> 정규화 ρ_DE(0)=Ω_Λ₀ 미강제. 진폭 A 자유.

ρ_DE(z) = A · [1-ψ(z)]^n

- 1-ψ(z) = α(1+z)³ / [1+α(1+z)³], α = Om/OL0
- z=0: 1-ψ₀ = Om/(Om+OL0), z→∞: 1-ψ → 1 (단조 증가)
- n=2 고정, A 자유: k=3 (Om, H0, A)
- n 자유 버전도 병행: k=4 (Om, H0, A, n)
- 범위: Om[0.15,0.50], H0[55,82], A[0.01,10.0], n[0.1,5.0]
- 30 starts, 경계 감지 필수

판정: ΔAICc vs ΛCDM, vs Model D

### Task V1b: (1-ψ) 정규화 강제 Model

> 정규화 강제: ρ_DE(0) = Ω_Λ₀

ρ_DE(z) = Ω_Λ₀ · [(1-ψ(z))/(1-ψ(0))]^n

- k=3 (Om, H0, n), n[0.1,5.0]
- 30 starts, 경계 감지 필수

비교 목적: V1a(정규화 자유) vs V1b(강제) — 정규화 가정의 영향 정량화

### Task V2': V(ψ) 포텐셜 직접 유도 Model

> SQT 이론 선험: V(ψ) 하모닉 포텐셜, μ² = H₀² 고정

ρ_DE(z) = C · (1/2) · (ψ(z)-1)²

- (ψ(z)-1)² = (1-ψ(z))² (same as V1a with n=2, different prefactor)
- k=3 (Om, H0, C), μ²=H₀² 흡수로 C는 무차원 계수
- 범위: Om[0.15,0.50], H0[55,82], C[0.01,200.0]
- 30 starts, 경계 감지 필수

판정: ΔAICc vs ΛCDM, vs Model D

### Task V3: ψ/ψ₀ 하이브리드 Model

ρ_DE(z) = Ω_Λ₀ · [ψ(z)/ψ(0)] · (1 + amp·exp(-beta·z))

- ψ(z)/ψ₀ = (1+α)/(1+α(1+z)³): 단조 감소 (quintessence 방향)
- amp·exp(-beta·z): 저z 부스트 항
- 두 인자 경쟁 → phantom crossing 가능성
- k=3: beta=1.0 고정, Om, H0, amp 자유
- 범위: Om[0.15,0.50], H0[55,82], amp[-3.0,3.0]
- 30 starts, 경계 감지 필수

### Task V4: 소멸 에너지 누적 Model (A1 직접)

> SQT A1: ψ 소멸에서 에너지 방출 → ρ_DE 기여

ρ_DE(z) = A · (1+z)³ · ψ(z) = A · (1+z)³ / [1+α(1+z)³]

- z=0: ρ_DE(0) = A·ψ₀ = A/(1+α) ≈ A·OL0
- z→∞: ρ_DE → A/α = A·OL0/Om (유한 수렴)
- k=3 (Om, H0, A), A[0.01,5.0]
- 30 starts, 경계 감지 필수

판정: ΔAICc vs ΛCDM, vs Model D

---

## ■ Task V 실행 구조

- Task V (V1a, V1b, V2', V3, V4): 5 모델, pool.map으로 병렬 피팅
- Bootstrap (Task 1): V 시리즈 최우수 모델에만 선택적 적용
- 총 모델 수: Task 0~6 + V1a/V1b/V2'/V3/V4

## ■ 코드 수정사항

- L36 원복: Model D amp ∈ (-3.0, 3.0) (음수 허용, 코드리뷰 오류 수정)
- E_V1a, E_V1b, E_V2prime, E_V3, E_V4 함수 추가
- task_V 함수: 5개 모델 병렬 피팅, cpl_wa, 경계 감지
- 8-worker Pool에서 V 시리즈 통합 실행

---

## ■ AICc 패널티

n=1853: k=2(+4.004), k=3(+6.008), k=4(+8.013)

## ■ 판정 기준

| 등급 | 조건 |
|------|------|
| Q92 GAME | ΔAICc<-4 AND wa<0 AND H0_tension<4.01 |
| Q91 STRONG | ΔAICc<-2 (and not Q92) |
| Q90 PASS | ΔAICc<0 |
| K90 KILL | ΔAICc≥0 |
| K92 INVALID | boundary-pinned |

## ■ 출력 형식

```
L38 Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Task 0] ΛCDM Baseline
  AICc={LCDM_AICc:.2f} (prev: 1670.12) [CONFIRMED/CHANGED]

[Task 1] Bootstrap (N=500)
  ΔAICc median: {med:.2f}  68% CI: [{lo:.2f}, {hi:.2f}]
  ΔAICc<-4 fraction: {frac:.1f}%
  amp: {amp_mean:.4f} ± {amp_std:.4f}
  beta: {beta_mean:.4f} ± {beta_std:.4f}
  Verdict: [PASS/CONDITIONAL/FAIL]

[Task 2] Profile Robustness
  profile dAICc<-6: {frac6:.1f}%
  profile dAICc<-2: {frac2:.1f}%
  Verdict: [PASS/CONDITIONAL/FAIL]

[Task 3] Model Simplification
  D_k4 ΔAICc=-8.44  (k=4)
  D_k3_betafixed ΔAICc={:.2f}  (k=3)
  D_k3_ampfixed  ΔAICc={:.2f}  (k=3)
  D_k2_bothfixed ΔAICc={:.2f}  (k=2)
  Preferred: k={X}

[Task 4] vs w0waCDM
  ΛCDM AICc=1670.12
  CPL  AICc={:.2f}  (w0={:.3f}, wa={:.3f})
  SQT D AICc=1661.68
  SQT vs CPL ΔAICc={:.2f}
  Verdict: [SQT wins/loses vs CPL]

[Task 5] BAO-only k=3 (beta fixed)
  best: Om={:.4f}, H0={:.2f}, amp={:.4f}
  chi2_BAO={:.4f}
  CPL: w0={:.4f}, wa={:.4f}
  boundary: {boundary}  verdict: {verdict}
  wa reversal: [YES/NO]

[Task 6] Residuals
  ΔBAO  = chi2_BAO(D) - chi2_BAO(LCDM) = {:.2f}
  ΔCMB  = chi2_CMB(D) - chi2_CMB(LCDM) = {:.2f}
  ΔSN   = chi2_SN(D)  - chi2_SN(LCDM)  = {:.2f}
  ΔRSD  = chi2_RSD(D) - chi2_RSD(LCDM) = {:.2f}
  Main source: [SN/BAO/etc]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Final Publication Verdict]

Publishable: [YES/NO/CONDITIONAL]

Strong claims:
- ΔAICc=-8.44 vs ΛCDM (bootstrap confirmed: XX%)
- vs CPL: ΔAICc=XX
- Main source: XX

Honest limitations:
- wa<0: 구조적 불가 (SQT psi 구조)
- H0 tension: CMB-driven, SQT 범위 외
- sigma8: 중립 (TIE)
- SN-only 기여 비율: XX%

Next: [논문초고/L39/보류]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## ■ 실행 조건

- 8-worker spawn Pool. 순차 실행 금지.
- P1 경계 감지: 모든 worker 필수 적용
- P2 profile: 각 (amp,beta)에서 Om/H0 재최적화 필수
- P3 H0 profile: 대각 Hessian 사용 금지 → grid profile
- P4 BAO k=3: beta 고정, amp 범위 확장
- 실행 전 4인팀 코드리뷰 ×2 필수

## ■ 예상 실행 시간

- Task 0: 2분
- Task 1 Bootstrap (500회): 30-60분
- Task 2 Profile scan (400점): 20-40분
- Task 3 Simplification (4 models): 10-20분
- Task 4 CPL (1 model): 10-20분
- Task 5 BAO k=3: 5분
- Task 6 Residuals: 1분
- 총: 1.5-3시간

---

*작성: 2026-04-20. L37 완료 + 코드리뷰 P1-P4 패치 포함. 4인팀 리뷰 ×2 후 실행.*
