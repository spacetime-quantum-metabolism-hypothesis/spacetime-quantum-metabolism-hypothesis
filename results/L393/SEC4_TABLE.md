# Section 4 — Predictions Table v2 (22 항목)

라벨 정의:
- **PASS**: 현존 데이터로 SQT 예측이 통과 (chi2/dof < 1.5 또는 |측정-예측| < 1σ)
- **PARTIAL**: 자릿수 수준 일치 또는 일부 데이터셋 통과, 다른 데이터셋과 tension 잔존
- **UNRESOLVED**: 미래 측정 대기 또는 toy-level 만 가능 (full Boltzmann 미실시)
- **falsifier**: 어떤 측정값이 어느 임계 초과 시 SQT 폐기

분포: PASS 9 / PARTIAL 5 / UNRESOLVED 8

| #  | 영역       | 예측                                                            | 상태       | Falsifier (임계 초과 시 폐기)                                    | vs 대안                          | 출처                  |
|----|------------|-----------------------------------------------------------------|------------|------------------------------------------------------------------|----------------------------------|-----------------------|
| P1 | Galactic   | sigma_0 regime: cluster sigma < galactic sigma factor ~60       | PARTIAL    | DES Y6 S8 측정이 LCDM 와 정확 일치 시                           | LCDM, MOND                       | L48 T17/T20           |
| P2 | Cosmology  | Λ_eff = (n_∞·ε)/c² ≈ 6.91e-27 kg/m³                             | PARTIAL    | 정확 계수 예측 → 측정과 >5σ 불일치                              | LCDM (input)                     | D4                    |
| P3 | Galactic   | BTFR slope = 4                                                  | PASS       | SPARC 후속 표본 slope < 3.5 또는 > 4.5 (>5σ)                    | LCDM (3.5–3.8)                   | Lelli+2016, L119      |
| P4 | Solar sys  | PPN γ = 1 (|γ-1| < 1e-5)                                        | PASS       | BepiColombo / GAIA |γ-1| > 1e-5                                | Verlinde, MOND-disformal         | L89, L389             |
| P5 | GW         | GW170817: |c_g - c|/c < 1e-15                                   | PASS       | 차세대 GW |c_g - c|/c > 1e-15                                  | TeVeS, Galileon (killed)         | L87                   |
| P6 | Cosmology  | CMB acoustic peaks at recombination = ΛCDM                      | PASS       | Planck PR4 / Simons Obs Δ(D_l) > 2σ                             | EDE, ΛCDM 동치                   | L106                  |
| P7 | Strong grav| EHT M87* / SgrA* shadow                                         | PASS       | ngEHT shadow 직경 > 5% 편차                                      | LCDM (GR) 동치                   | L99                   |
| P8 | Cosmology  | H(z) cosmic chronometer 32 pts, chi²/dof = 0.84                 | PASS       | Moresco DR2 chi²/dof > 2.0                                       | LCDM (chi²~0.9 동급)             | Moresco+2022, L88     |
| P9 | GW         | PTA contribution ~10⁻²⁷ << 10⁻¹⁵ (SMBHB compatible)             | PASS       | NANOGrav 20yr SMBHB 배제 + non-LCDM 신호                         | EDE, cosmic strings              | L107                  |
| P10| Particle   | BBN ΔN_eff < 6e-32 << 0.3                                       | PASS       | CMB-S4 ΔN_eff 측정 > 0.05                                        | LCDM (ΔN_eff = 0)                | L83                   |
| P11| Lab        | Casimir effect: 표준 QED 보존                                   | PASS       | 차세대 Casimir 정밀도 1% 에서 편차 발견                          | Verlinde (예측 충돌)             | L102                  |
| P12| Galactic   | a_0(z=2)/a_0(0) ≈ 3.03 at SKA Phase 1                           | UNRESOLVED | SKA-1 측정값 < 1.5 또는 > 5.0                                    | MOND constant (=1.00)            | L175                  |
| P13| Galactic   | a_0(disc)/a_0(spheroid) = π/3 ≈ 1.05                            | UNRESOLVED | ATLAS-3D + SAMI 비율 < 0.95 또는 > 1.20 (>2σ)                    | MOND universal (=1.00)           | L175                  |
| P14| Galactic   | Void galaxy a_0 ≈ 0.07 × normal                                 | UNRESOLVED | 2027+ void surveys: 비율 > 0.30                                  | MOND constant                    | L175                  |
| P15| Cosmology  | DESI DR3: w_a < 0 (sigmoid-weight g 함수)                       | PARTIAL    | DR3 w_a posterior 99% 가 w_a > 0                                | LCDM (wa=0), DR1 (wa>0)          | L33 (BAO-only)        |
| P16| Cosmology  | H0 조기-후기 cross-check 잔존 tension < 1σ in SQT 자체 보정     | UNRESOLVED | SH0ES + Planck SQT-fit 시 H0 잔존 tension > 3σ                   | LCDM (5σ tension)                | L6-Q15 log            |
| P17| Cosmology  | sigma8 / S8 tension SQT 자체로 해결 불가 (mu_eff≈1)              | PARTIAL    | DES Y6 + KiDS-1000 S8 측정이 LCDM 정합 시 SQT 차별 없음          | LCDM (tension), EDE              | L5 Q15 FAIL log       |
| P18| Cosmology  | omega_m joint posterior 0.30~0.33 범위                          | UNRESOLVED | DR3 + Planck + DES joint omega_m < 0.27 또는 > 0.36              | LCDM (0.315)                     | L33 (BAO-only=0.068 별도) |
| P19| GW         | BBH ringdown overtone 진동수 GR 일치 (deviation < 1%)           | UNRESOLVED | LISA / CE / ET ringdown deviation > 1%                           | LCDM/GR 동치, ECO 다름           | (L99 연관)            |
| P20| GW         | Stochastic GW background normalization 자릿수 SMBHB 일치        | PASS       | LISA SGWB amplitude > 10× SMBHB 예상                             | EDE, primordial BH               | L107                  |
| P21| Strong grav| EHT polarimetry phase: GR 일치                                  | UNRESOLVED | ngEHT polarization map > 10% 편차 from Kerr                      | GR 동치                          | L99                   |
| P22| Particle   | DE-photon coupling: CMB spectral distortion 무시할 수준          | UNRESOLVED | PIXIE / Voyage μ-distortion > 1e-7 from non-LCDM 채널            | LCDM (없음)                      | (paper Sec 6)         |
| P23| Astro      | FRB DM-z relation: SQT 우주론 정합                              | UNRESOLVED | CHIME FRB DM(z) chi²/dof > 2.0 vs SQT H(z)                       | LCDM 동급                        | (L88 연관)            |
| P24| Lab        | Atom interferometer / torsion balance: 5th force 무                | PASS       | Eot-Wash / MICROSCOPE Δa/a > 1e-15 발견                           | Verlinde (예측 가능)             | L102 연관             |
| P25| Astro      | UDG (ultra-diffuse galaxy) dynamics: low-sigma regime 정합       | PARTIAL    | DF2 / DF4 후속 표본 sigma 측정 > MOND a_0 한계 일관 위반          | MOND, LCDM (DM 필요)             | (L48 연관)            |
| P26| Astro      | Dwarf galaxy core/cusp: SQT regime 의존 prediction              | PARTIAL    | THINGS / LITTLE THINGS sample > 80% cusp                         | LCDM (cusp), SIDM (core)         | (L119 연관)            |
| P27| Astro      | Cluster lensing convergence profile: lower S_8 정합              | PARTIAL    | DES Y6 / Euclid lensing convergence LCDM 정확 일치                | LCDM (S8 tension)                | L48 T17               |

---

## 정직 한 줄

22개 예측 중 9개 PASS 는 대부분 LCDM 도 통과하는 약한 제약이며, SQT 의 결정적 차별성은 P12~P14 (a_0 evolution / 기하), P15 (DR3 w_a), P19 (ringdown) 의 미래 측정에 달려 있다 — 현 시점 LCDM 대비 "이미 이긴 예측" 은 없다.
