# L213 — OPEN #2: n field statistics 정량 검증

## 8인팀 공격 설계

**Target**: SQT 의 metabolism field n(x,t) 의 통계 (Gaussian? Poisson? non-Gaussian?) 미정.

### 약점 진단
1. A1: 공리 a4 가 n의 동역학 PDE 만 명시. 1점/2점 함수 부재.
2. A2: <n>=n0 평균만 정해짐. 분산 σ_n^2 미정.
3. A3: CMB non-Gaussianity (f_NL local <5, Planck 2018) 가 n의 통계와 연결되어야 함.
4. A4: large-scale density field 가 ρ_q 를 바이어스 → matter power spectrum 영향.
5. A5: simplest assumption — Gaussian fluctuations on Planck scale, central limit → smooth on cosmological scale.
6. A6: Poisson 통계 토이 (Δn/n ~ 1/√N, N=n0*V) 계산 가능.
7. A7: 만약 Poisson 이라면 cosmological scale (V~Mpc^3) 에서 fluctuation negligible (1/√(10^... huge)).
8. A8: referee: "what is the variance of n?" — 답 필요.

### KILL
- K-n1: σ_n/n0 가 cosmological scale 에서 >10^-4 면 CMB 영향 가능 → 별도 분석 필요.
- K-n2: f_NL 예측 |f_NL|>5 면 Planck 와 충돌.

### 실행
- 토이: Poisson assumption N = n0 * V, σ_N/N = 1/√N.
- V = (1 Mpc)^3 → N = n0 * V; check σ/N.
