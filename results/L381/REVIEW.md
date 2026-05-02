# L381 — 4인 review (cosmic shear xi_+(10') SQT vs LCDM)

## 결과 요약 (실측, simulations/L381/run.py)

| 미션      | f_sky | xi_+(10')_LCDM | xi_+(10')_SQT | Δxi/xi   | σ(xi_+)   | SNR  |
|-----------|-------|----------------|----------------|----------|-----------|------|
| Euclid    | 0.364 | 2.857e-05      | 2.922e-05      | +2.29%   | 4.22e-07  | 1.55σ|
| LSST Y10  | 0.436 | 2.762e-05      | 2.825e-05      | +2.29%   | 3.71e-07  | 1.71σ|

- xi_+(10') 절대값은 KiDS/DES 의 ~3e-5 수준과 1차 일치 (sanity check 통과).
- Δxi/xi = +2.29% = 2 × ΔS_8(=+1.14%) — 선형 이론 (P ∝ σ_8², xi_+ ∝ P) 의 직접 결과.
- 양 survey 모두 단일 theta=10' bin 에서 1σ 를 넘지만 3σ 에는 미달.

## 4인 review

- **P (positivist)**: SNR 1.5–1.7σ 는 단일 bin / single source-bin / linear-only 가정 하의 **하한**. 실제 Euclid/LSST 의 tomographic 3x2pt 분석은 ~10× 정보량 → 이 SQT shift 는 **rejection 가능**.
- **N (negativist)**: SQT 가 LCDM **위쪽** 으로 xi_+ 를 밀어버린다 (+2.29%). DES-Y3 / KiDS-1000 데이터는 이미 LCDM 에 비해 **낮은** S_8 을 선호 (S_8 tension). 따라서 SQT 는 데이터 에서 **더 멀어지는** 방향. L286 결론 (SQT = worsen) 재확인.
- **O (observer)**: μ_eff = 1 (dark-only structural, GW170817 호환) 가정은 L242/L286 에서 합의된 보수적 선택. 만약 SQT 가 μ_eff(k,z) ≠ 1 을 일으킨다면 결과가 달라질 수 있으나 그 경로는 현재 SQT 형식주의에 없음.
- **H (historian)**: L286 P19 결과 (Euclid σ_8 sensitivity 0.005, ΔS_8=+1.14%) 의 **real-space xi_+ projection**. cosmic shear 분야에서는 power-spectrum 보다 xi_+/xi_- 가 직접 데이터, 따라서 이 정량이 falsifier 로 더 직접적.

## 확인 / 재발방지

- LSST Y10 n(z): 처음 Smail (z0=0.28, alpha=0.9, beta=2) 사용 시 z_med=0.22 (비현실적). 수정: DESC SRD form n(z)∝z² exp(-(z/0.11)^0.68), z_med=0.86. 결과 sanity-check 후 채택.
- xi_+ 분산: Joachimi 2008 single-bin Gaussian (cosmic variance + shape noise). tomographic / non-Gaussian 무시 — **lower bound on σ**.
- linear-only P(k) + halofit (Smith 2003). theta=10' 에서 baryon feedback 는 % 수준 영향, 본 분석은 LCDM↔SQT 차이만 비교하므로 cancel.

## 정직 한 줄

xi_+(10') SQT−LCDM = +2.29% (S_8 +1.14% 의 P∝σ_8² 직접 결과); Euclid 1.55σ, LSST_Y10 1.71σ 단일 bin 검출 가능 — **그러나 SQT 는 LCDM 보다 데이터에서 멀어지는 방향**, 검출 = SQT falsify (L286 결론 정량 재확인).
