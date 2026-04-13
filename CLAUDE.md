# SQMH Project Rules

## ⚠️ 최고 우선 원칙 — 위반 시 결과 전체 무효 ⚠️

> **이 원칙은 CLAUDE.md의 모든 다른 규칙보다 우선한다.**
> **Command 파일 작성, 에이전트 프롬프트, 팀 토의 지시 모두에 적용.**

### [최우선-1] 방향만 제공, 지도 절대 금지

- **허용**: 탐색 방향, 물리 현상의 이름, 수학 분야의 이름
- **금지**: 구체적 수식, 파라미터 값, 유도 경로 힌트, "A = ..." 형태의 어떤 수치도
- **금지**: L14/L22 등 과거 결과에서 이론 형태를 가져와 "개선"하는 행위
- **금지**: "이 방정식을 써라", "이 상수를 고정해라" 류의 지시
- **위반 판정**: Command에 수식이 한 줄이라도 있으면 즉시 전면 재작성
- **이유**: 지도 제공은 과적합 이론 선택 편향을 만들어 결과를 오염시킨다

### [최우선-2] 이론은 팀이 완전히 독립 도출

- 8인 팀은 방향만 듣고 수식을 스스로 유도한다
- Command 파일에 수식이 있으면 팀의 독립성이 파괴된다
- 이론 도출 결과를 사전에 암시하는 어떤 힌트도 금지

---

## ⚠️ LXX Command 공통 원칙 — CRITICAL (L17 이후 전체 적용) ⚠️

> **아래 원칙들은 모든 Command 파일, 에이전트 프롬프트, 팀 구성에 CRITICAL로 적용된다.**
> **위반 시 해당 세션 결과 전체 무효.**

- **이론 도출**: 방향만 제공. 지도(유도 경로 힌트) 극단적으로 금지. (→ 최우선-1)
- **팀 구성**: 역할 사전 지정 금지. 인원 수만 지정. 서로 중복되지 않는 자유 접근. 토의에서 자연 발생하는 분업만 인정. 코드리뷰 팀도 "데이터 로딩 담당", "chi² 담당" 등 역할 사전 배정 금지 — 팀이 자율 분담.
- **과적합 방지**: 시뮬레이션에서 파라미터 수 증가 시 AICc 패널티 명시. 개선이 패널티보다 작으면 단순 모델 채택.
- **시뮬레이션 실패 시**: 무조건 코딩 버그를 먼저 의심. 4인팀 코드리뷰 후 재실행. 물리 해석은 코드 검증 후.
- **코드리뷰**: 4인팀이 자율 분담으로 전체 코드 검토. 역할 사전 지정 없음.

## 시뮬레이션 최우선 실행 원칙

- **병렬 실행 최우선**: 시뮬레이션은 항상 multiprocessing으로 병렬 실행. 순차 실행 금지.
- **환경**: 10코어 CPU 사용 가능. 최대 9개 병렬 프로세스 허용 (1코어는 메인 프로세스 확보).
- **구현**: `multiprocessing.get_context('spawn').Pool(n)` 사용. 각 워커는 데이터를 독립 로드.
- **워커당 스레드 고정**: `OMP/MKL/OPENBLAS_NUM_THREADS=1` 강제 (워커 내부 멀티스레드 방지).
- **모델 독립성**: 모델별 worker function 분리, 전역 singleton 의존 금지.

## 재발방지

- DESI BAO 데이터: 반드시 github.com/CobayaSampler/bao_data 공식 파일 사용. 임의 추정값 절대 금지.
- BAO 거리 D_H = c/(H0*E(z)) 계산 시 단위: c[m/s] / (H0[s^-1] * E * Mpc[m]) = Mpc. 중간 km/s/Mpc 변환 하지 말 것.
- BAO 피팅은 D_V(BGS) + D_M/D_H(나머지) 13포인트 + 전체 공분산행렬 사용. D_V만으로 피팅 금지.
- print()에 유니코드(✓₀μ³⁻ 등) 사용 금지 → cp949 에러. matplotlib 라벨은 OK.
- n₀, μ 개별값은 SI에서 자기무모순 안됨. 곱 n₀μ만 물리적 의미 있음.
- w(z) 선도차수 2체결합만으로는 wₐ>0. wₐ<0 주장하려면 V(phi) 역학 필수.
- numpy 2.x: trapz → trapezoid.
- 시뮬레이션 결과가 base.md 주장과 다르면 정직하게 base.fix.md에 기록. 결과 왜곡 금지.
- IDE ODE convention: 변수는 omega=rho/rho_crit_0 (물리적 밀도). E^2=Omega_r(1+z)^4+omega_m+omega_de. **절대 omega_m*(1+z)^3 이중카운팅 금지.**
- E(z) 계산은 반드시 coupled ODE solver (odeint) 사용. ad hoc perturbative 근사 금지.
- IDE 피팅 시 xi_q 양수/음수 모두 탐색 + scipy.optimize 사용. 수동 grid scan만으로 결론 금지.
- xi_q<0은 w<-1 (phantom) → SQMH 물리 위반. 피팅 결과 보고 시 반드시 SQMH 정합성 (xi_q>0) 분리 표기.
- DESI w0-wa 타원은 DESI+CMB+SN 결합 결과. BAO-only 비교 시 반드시 "결합 분석" 명시.
- DESI DR2 공식값: w0=-0.757+/-0.058, wa=-0.83+0.24/-0.21 (DESI+Planck+DES-all). wa=-1.27은 DR1 혼동 오류.
- DESI DR1→DR2 값 변경 주의: DR2에서 wa가 크게 변동. 항상 arXiv 번호로 출처 명시.
- **sigma = 4*pi*G*t_P (SI)**. sigma = 4*pi*G 는 플랑크 단위 전용. SI에서 sigma[m³kg⁻¹s⁻¹] ≠ 4piG[m³kg⁻¹s⁻²].
- n₀μ = rho_Planck/(4pi) ≈ 4.1e95 kg/m³. 이전값 6.6e-44는 sigma=4piG 오류에서 파생, 사용 금지.
- v(r) = g(r)*t_P (유입속도 = 중력가속도 x 플랑크시간). v(r) = GM/r² 표기는 속도/가속도 혼동.
- 문서 작성 시 유니코드 깨짐 주의: 파일 저장 후 반드시 인코딩 확인.
- `quintessence.py`의 `Om_m`은 fractional Omega_m(a) 아니고 **dimensionless omega_m = rho/(3H0²)**. 성장방정식 입력 시 **반드시 E²로 나눠** 분수로 변환.
- Backward ODE with V_mass (thawing): N_ini < -3 (z > 20) 이면 anti-damping 폭주. 성장 계산은 N_ini = -3 한계.
- Hu-Sugiyama z_* fit formula 정확도 ~0.3% (Planck 측정 σ=3e-6 보다 100배 큼). Compressed CMB θ* 에 theory floor 0.3% 반드시 더하기.
- Phase 2 CMB 적분은 z~1100 까지 필요. desi_fitting.py 의 `solve_sqmh_Ez`는 z_max=3 이므로 **고z 구간은 LCDM 스케일링 bridge 사용**. cubic extrapolation 금지.
- 공개 실측 데이터는 CobayaSampler 공식 저장소 우선 (bao_data, sn_data). DES-SN5YR 경로: `sn_data/DESY5/`.
- scipy.optimize 다중 start loop 에서 `best=(1e8, None)` 초기화 시 **모든 start 실패 대비 `if best[1] is None` 방어 필수**. NoneType unpack 금지.
- Coupled-quintessence 성장방정식에 drag term `-β·φ_N·δ_N` (Di Porto-Amendola 2008 eq 3) 포함 필수. `G_eff/G = 1+2β²` 만으로는 불완전. RSD 결합 전 반드시 수정.
- LCDM BAO-only 최솟값은 Om~0.326 에서 χ²≈21.4 (DESI DR2 13pt). 고정 Om=0.315 에서는 ~30.7. Regression 비교 시 fixed-Om 값과 best-fit 값 혼동 금지.
- Fluid IDE fit 결과가 phantom branch (ξ_q<0) 로 갈 경우 **SQMH-consistent branch (ξ_q≥0)로도 별도 피팅** 해서 같이 보고. ξ_q≥0 branch 가 경계 0 에 붙으면 "LCDM 로 수렴" 해석.
- numpy in-place 함정: `D = sol.y[0]; D /= D[-1]` 는 `sol.y[0]` 원본까지 수정함. 정규화 전에 `.copy()` 필수. f = dlnD/dlnN 는 **정규화 전 raw 값**에서 계산.
- Coupled-quintessence 성장방정식 배경은 반드시 **LCDM 아날리틱** 으로 대체. `quintessence.py` backward ODE 는 phi_N → √6 (phantom 경계) 로 폭주해 E(N), Omega_m_frac 모두 왜곡. 성장용으로 직접 쓰면 f(z=0)≈0.65 처럼 틀린 값 나옴 (정답 0.527).
- 성장 ODE 의 phi_N 은 slow-roll 근사 `phi_N ≈ √(2/3)·β·Ω_m(a)` 사용. 작은 |β|<0.4 에 대해 factor ~2 정확. backward ODE φ_N 직접 사용 금지.
- V_family/extra_params 가 성장 ODE 에 들어가는 경로는 오직 `beta` 와 `G_eff/G = 1+2β²` 뿐 (Phase 2 근사). 전체 V(φ) 트래커 반영은 Phase 3 CLASS 레벨.
- DESY5 SN 거리 적분은 **반드시 `zHD`** (peculiar-velocity corrected CMB frame) 사용. `zCMB` 는 ~0.001 저z bias 유발. `(1+zHEL)` 인자는 헬리오센트릭. CobayaSampler DESY5 규약.
- Coupled-quintessence β (V_RP, V_exp) bounds 는 **[0, ...] 양수 강제**. β<0 은 matter→φ 에너지 이동 (SQMH 부호규약 위반). `fit_quintessence` bounds lower 0.0 필수. 멀티스타트 시드도 음수 제거 (`b0 >= 0.01`). **V_mass** 도 동일 (세 family 모두 적용).
- MCMC log-likelihood 에서 chi2 실패 시 **sentinel 값 (1e6 등) 합산 금지**. `tot = _safe(c_bao)+... ; -0.5*tot` 는 walker 를 logp≈−5e5 의 유한 basin 에 가둠. 반드시 None/nan 발견 즉시 `return -np.inf` 로 reject.
- 하드코드 index 로 공분산 블록을 덮어쓰는 패턴 (e.g. phase3 `_BOSS_IDX=(2,3,4)`) 은 Z 배열 재정렬 시 silent 오배치. 반드시 `assert np.all(np.diff(Z)>0)` + index→z 매핑 assertion.
- `np.fromfile(f, count=N*N)` 후에는 반드시 `vals.size == N*N` 검사. count 는 상한이지 최소값 아님, 파일 truncation 시 silent 부족 채움.
- `matplotlib.use('Agg')` 는 **`import corner` / `import ...matplotlib*` 이전에** 호출. corner 등은 내부에서 pyplot 를 초기화해 backend 를 고정하므로 나중에 use() 호출 시 silent 무시, headless 환경에서 figure 저장 실패.
- emcee 재현성은 walker 초기값 seed 만으로 부족. `emcee.EnsembleSampler` 의 stretch move 는 `np.random` 전역을 사용하므로 `run_mcmc` 내부에 `np.random.seed(...)` 추가 필수.
- Compressed CMB 용 `_HighZBridge` 는 **pure LCDM tail** (z>Z_CUT) 사용, 절대 low-z 와 high-z 를 `e_low/e_high` 로 rescale 금지. backward ODE 가 phi_N→√6 근방으로 가면 rescale factor 가 theta* 적분에 spurious 곱수로 들어가 sound horizon 오염.
- Growth ODE 결과 검증 시 `D_today>0` 만 검사 금지. `D_raw>0 전체`, `D_N_raw finite`, `D_today finite` 모두 확인해야 f=D_N/D, D/D_today 에서 nan 전파 방지.
- Phase 별 중복 상수 (RSD 데이터, index) 는 **import 시 assertion 으로 drift guard** 걸어 둔다. `assert np.allclose(phase3.X, phase2.X)`.
- k-essence / quintessence 배경 ODE 는 **forward shooting** (N_ini<0 matter era → N_end=0 today) 강제. Backward (오늘→과거) 는 `phi_N → √6` phantom 경계 폭주로 w(z), Om_phi 왜곡. `phase3.6 B3 kessence.py` 참조.
- k-essence `K(X,phi) = X + g X^2/M^4` 에서 **분모 `K_X + 2 X K_{XX} = 1 + 6 g X` 부호 검사** 필수. 음수면 ghost 영역이므로 return None 으로 즉시 reject. 소리속도 `c_s^2 = K_X / (K_X + 2 X K_{XX})` 양수 조건과 동치.
- Unscreened coupled-quintessence `|gamma-1| = 2β²/(1+β²)` 은 Cassini `|γ-1|<2.3e-5` 과 `|β|<3.4e-3` 에서 충돌. Phase3 posterior `β~0.1` 시 Vainshtein 가정 (cubic Galileon `M^4~M_P² H_0²`) 없이는 **죽음**. screening 없이 β 자유화 시도 금지.
- **L2 재설계**: universal ξφT^α_α coupling 은 Cassini 자동 984× 위반. C10k (sector-selective dark-only) 또는 C11D (disformal `g̃=Ag+B∂φ∂φ`) 구조만 C1-C4 4/4 통과. baryon 을 Einstein frame 에 분리 유지 필수.
- RVM `Λ(H²)=Λ₀+3νH²` 수정 Friedmann 에서 `w_a` **부호는 ν 부호와 동일**. DESI `w_a<0` 정합성 위해서는 ν<0 branch (Gómez-Valent-Solà ApJ 975 64 2024). ν>0 (Solà 2022 원본) 은 부호 반대.
- Chern-Simons gravity `bRR̃` 의 정적 구형 PPN 기여는 Pontryagin 소멸로 0 (Schwarzschild 는 Type D, 자기 Weyl = 0). Kerr rotation 있는 경우만 gravitomagnetic 수정.
- Disformal coupling `g̃=Ag+B∂φ∂φ` 는 `A'=0` pure disformal 한도에서 정적 γ=1 exact (Zumalacárregui-Koivisto-Bellini 2013). A'≠0 conformal 부분이 γ-1 주원인.
- Python 식별자에 공백 금지. `R_rir j` 같은 변수명은 SyntaxError.
- `print('ν')` 처럼 non-ASCII 유니코드 print 는 cp949 환경에서 깨짐 (`��` 출력). 변수명은 ASCII, 라벨만 유니코드.
- **C10k (dark-only) 수락은 PPN 한정**. `G_eff/G = 1+2β_d²` 로 DM linear growth 증폭 → `β_d~0.107` 이면 `sigma_8` 2.3% 상승, S_8 tension `+6.6 chi^2` 악화. "Cassini 통과"와 "S_8 완화"를 동일시 금지.
- Disformal IDE toy `w(z)` 에 `np.sign(...)` 같은 ad hoc phantom flip 금지. `w_a` 부호 주장은 반드시 full Boltzmann (hi_class disformal branch) 또는 Sakstein-Jain 해석 공식 직접 인용 필요. Leading-order exp template 은 `w_a>0` 방향으로 편향.
- RVM ν 스캔 BAO-only 는 `|nu|~0.006` 에서 `Delta chi2 ~ -1.6` 개선. Phase 3 joint (BAO+SN+CMB+RSD) 에서는 CMB 제약으로 `|nu|<0.001` 로 축소 가능 — BAO-only 결과를 joint 결론으로 혼동 금지.
- **L2 R2 C23 Asymptotic Safety**: effective RG parametrisation `nu_eff * (H^2/H0^2 - 1)` 에서 `nu_eff<0` 만 `w_a<0` 생성. Bonanno-Platania 2018 의 `k=ξH` identification 은 effective 수준 선택이며 ξ=O(1) 가정. `|nu_eff|~0.035` 는 Sola unitarity bound `|ν|<0.03` 을 **살짝 초과** — Phase 5 MCMC 에서 bound 재확인 필수.
- **L2 R2 C26 Perez-Sudarsky diffusion**: `J^0 > 0` (matter → Λ drift) 방향만 `w_a<0`. `J^0<0` 은 DESI 반대 부호. Toy ansatz `J^0 = α_Q ρ_c0 (H/H0)` 에서 `α_Q~0.22` 가 DESI `wa=-0.83` 재현. α_Q 미시 기원 (CSL, 대사공리 L0/L1) 은 Phase 5 이론 정합성.
- **L2 R2 C27 Deser-Woodard non-local**: `f(X)=c0 tanh(...)` template 의 `w_a` 는 **c0 에 독립** (log 비 미분에서 상수 소거). Amplitude 는 `X_shift` 등 shape 파라미터로만 제어. 정적 `γ=1` 은 Schwarzschild `R=0` → auxiliary X frozen (Koivisto PRD 77 123513 2008), Vainshtein 과 무관.
- **L2 R2 C28 RR non-local** 의 leading-V 근사 (`ρ_DE ∝ h²V/4`) 는 `w_a` **부호 반전** — `+0.55` vs Dirian 2015 `-0.19`. 정확 계산은 Dirian Eq 2.5~2.8 full 배경 방정식 (U, V, UV cross-term) 필수. leading-V toy 로 "structural wa<0" 주장 금지.
- **Non-local gravity 모델 (C27, C28)** 의 정적 PPN γ=1 은 auxiliary 필드 frozen 이 원인이지 screening 이 아님. 해석 혼동 금지.
- numpy 2.x: `trapz → trapezoid` 는 `from numpy import trapz` 구문에서도 에러. 직접 `np.trapezoid` 호출만 안전. (이미 기재된 규칙이나 L2 R2 에서 재발 확인됨 → 강조.)
- **L2 R3 C33 f(Q)**: `f(Q)=Q+f_1 H_0^2 (Q/6H_0^2)^n` 에서 `(1-1/(2n))` 인자는 `n=0.5` 에서 0 → 전 `f_1` 무효. `n≥1` 에서만 검증 의미. 또한 `w_a<0` 부호는 **`f_1>0` branch** (수치 검증). 수식 유도로 `f_1<0` 예측 시 부호 오해석 — Python toy 필수 재확인.
- **L2 R3 Chaplygin family 폐기**: vanilla GCG 와 Modified Chaplygin (`p=Bρ-A/ρ^α`) 모두 실제 스캔 `(A,B,α)` 전 범위에서 `w_a>0` 만 생산. L2 C4 구조적 불통과 확정. 신규 토이에서 Chaplygin 변종 재탐색 금지.
- **L2 R3 Wetterich fluid IDE**: coupled continuity `dρ_m/dN=-3ρ_m+3βρ_DE, dρ_DE/dN=-3βρ_DE` 토이는 **`β≤0.05` 선형 regime** 에서만 유효. `β=0.107` (Phase 3 posterior) 대입 시 CPL fit `w0=+4.3, wa=-25` 로 발산. Phase 3 β 직접 상속 주장은 full Boltzmann (hi_class IDE) 필수.
- **L2 R3 Mimetic**: `(∂φ)²=-1` 제약은 **bare mimetic 에서만** `γ=1` (scalar 비전파). Chamseddine 2014 HD extension `L ⊃ α(□φ)²` 은 propagating scalar 부활 → Cassini 위반. "Mimetic 계열" 뭉뚱그려 C1 PASS 주장 금지, "bare vs HD" 명시 필수.
- **L2 수식 예측 ≠ 수치 검증**: R3 에서 C33 부호 예측 오류 + C37 전면 실패 발생. 모든 L2 후보는 해석 유도만으로 등급 부여 금지, 반드시 Python toy 로 `w_a` 부호 실측 후 `A/B/C` 판정.
- **L3 배경 fit 에서 ODE 폭주는 해석 toy 로 교체**. `solve_ivp` 기반 C26 (Perez-Sudarsky diffusion), C41 (Wetterich coupled continuity), C33 (f(Q) self-consistent Newton) 가 고z 경계에서 blow-up. 해석 drift / closed-form particular+homogeneous / 저z 전개 로 대체하면 수렴.
- **L3 CPL 추출 시 `rho_de_eff = E²-Om(1+z)³` 음수 artifact 주의**. IDE (C10k, C41) 는 matter ↔ DE 재분배 때문에 이 bookkeeping 차이가 z~1.9 근처에서 음수로 넘어가 `d ln rho_de / d ln a` 발산. `w0, wa` 는 반드시 **E²(z)↔ CPL E²(z) 직접 least_squares fit** (z∈[0.01, 1.2]) 으로.
- **L3 optimiser boundary 박힘**: Om∈[0.20, 0.40], h∈[0.60, 0.78] 넓은 bounds 는 Nelder-Mead 를 경계로 밀어버림. `Om∈[0.28, 0.36], h∈[0.64, 0.71]` LCDM baseline 근방 tight box + 파라미터 클리핑 + smooth penalty 로 교체.
- **L3 Fluid-level toy 는 배경 w_a=0 구조적**. C10k `ρ_DE ∝ a^(-3β_d)` 는 w=const. K2 `|w_a|<0.125` 로 구조 탈락. 이런 모델은 **성장 채널 (G_eff/G, RSD Δχ²) 기준**으로 재평가해야 함.
- **L3 K2 경계값 0.125 에 ±0.01 이내 탈락은 toy 제한일 가능성**. C11D |w_a|=0.1149 로 0.009 미달 kill — hi_class full 에서 재판정 필수. 프레임워크 탈락 ≠ 이론 탈락.
- **L3 C33 f(Q) 부호 재역전**: L2 R3 에서 수치 검증한 `f_1>0 → w_a<0` 이 L3 저z 전개 toy `rho_de=OL0[1+f_1(a^α-1)]` 에서는 `f_1<0 → w_a<0` 로 역전. **Toy 선택이 부호를 바꿀 수 있음**. Phase 5 는 Frusciante 2021 원본 배경 방정식만 신뢰.
- **L3 RVM 계열 (C5r, C23, C6s) joint 에서 ν→upper bound 박힘**. BAO-only 의 ν<0 선호가 SN+CMB+RSD 와 joint 에서 희석 → LCDM 등가로 나타남. 정상 현상이며 RVM 가 "죽은 것" 이 아니라 "데이터가 LCDM 와 구분 못함" 을 의미.
- **L3 에서 C26 분석 toy**: `ρ_m(a)=Om·a^(-3)(1-α_Q(1-a³)), ρ_Λ(a)=OL0+α_Q·Om·(1-a³)` drift form 은 α_Q>0 에서 w_a≈-1.0 을 직접 재현. Phase 5 full diffusion ODE 대체 전 안전한 배경 수준 proxy.
- **L4 C27 붕괴**: Deser-Woodard `f(□⁻¹R)` tanh 토이의 w_a<0 은 **full localised (U,V) 전개에서 posterior 가 c0→0 으로 붕괴**. 비국소 leading-V 또는 tanh-f 토이 부호는 full-field 없이 인용 금지.
- **L4 C26 K10 fail**: `J^0=α_Q ρ_c0 (H/H0)` ansatz 는 full ODE 적분에서 exponential depletion → LCDM 복귀. L3 closed-form drift 는 저차 선형 전개. 재공식화 `J^0=α_Q H ρ_m` 시도 필요.
- **L4 RVM family 전원 wrong-sign**: C5r/C6s/C23 모두 joint posterior ν ≈ +0.009 (SQMH 기대 ν<0 과 반대). RVM 계열 SQMH 후보 사용 전 **사전 joint posterior 부호 확인** 필수.
- **L4 universal fluid IDE Cassini 구조 위반**: C41 의 `G_eff/G = 1+2β²` 은 `|γ−1| ≈ 5×10⁻³` 로 자동 탈락. 반드시 dark-only embedding 필요.
- **L4 C11D K3 template artifact**: thawing CPL `w_0=−1+γ²/3, wa=−(2/3)γ²` 저차 전개는 phantom crossing 인공물 생성. K3 hard kill 전 hi_class full 또는 Sakstein-Jain exact 배경 재판정 필수.
- **L4 MCMC 예산 현실**: joint chi² ≈ 100 ms/call → 48×2000 은 후보당 30–60분. 여러 후보 동시 Windows 실행 timeout. **후보별 분리 세션** 필수.
- **Python 3.14 + emcee 안정화**: (1) `np.bool_/np.float_` `json.dump` 깨짐 → `_jsonify` 재귀 변환기. (2) Windows OpenMP 멀티스레드 silent death → `OMP/MKL/OPENBLAS_NUM_THREADS=1` + `np.seterr(all='ignore')` + emcee 내부 `np.random.seed(42)`.
- **sibling background module collision**: 여러 `simulations/*/background.py` 동시 sys.path 시 Python 이름 충돌. 후보 디렉터리 내부 상대 import 또는 파일명 분리.
- **K10 정의 주의**: K10 (toy↔full 일치) 은 **w_a 부호** 기준. underlying 파라미터 (ν, f_1 등) 부호 역전해도 w_a 동일 부호면 formally PASS 하지만 SQMH 해석은 실패 — 별도 `sqmh_sign_consistent` 플래그 필요.
- **phantom_crossing numerical guard**: LCDM 근방 (w≡−1) 에서 `np.gradient` 수치 노이즈로 false phantom cross 발생. `common.phantom_crossing` 에 `|w+1|>1e-3` 양측 threshold 필수.

## L5 재발방지 (Phase-5 추가)

- **L4 K3 phantom crossing KILL 은 CPL 템플릿 아티팩트 가능성 필수 재판정**. thawing 저차 전개 `w_0=−1+λ²/3, wa=−(2/3)λ²` 는 구조적으로 phantom 근방 노이즈 생성. 배경 exact ODE (Sakstein-Jain / CLW 1998) 로 재확인 필수.
- **Pure disformal (A'=0) 은 배경에서 minimally coupled quintessence 와 정확히 동일** (ZKB 2013). hi_class 없어도 CLW autonomous system 이 faithful 구현.
- **C26 Perez-Sudarsky 확정 KILL**: 모든 `J⁰ = α_Q·f(H, ρ_m)` 형태 ansatz 가 non-zero α_Q 에서 CMB sound horizon 폭발. SQMH unimodular diffusion 은 background-only 로는 dead, 섭동-레벨 새 채널 필수.
- **C33 f(Q) cosmic shear 실패**: Ω_m=0.340 best-fit 이 S_8 ∝ √(Ω_m/0.3) 를 상승시켜 DES-Y3 3σ 상한 초과. background-only f(Q) 계열은 S_8 tension 악화 위험 상존 — K15 check 필수.
- **Background-only 수정 + μ=1 구조**: S_8 tension 은 구조적으로 해결 불가. parametric Ω_m 이동으로 인한 숫자상 개선은 artefact. 논문 본문에 정직 기록.
- **Alt-20 14-cluster canonical drift class**: SVD n_eff=1, participation ratio 1.017. 15 후보를 15 independent theory 로 보고 금지. 단일 대표 (A12 erf diffusion) 로 축약.
- **DR3 pairwise discrimination 0.19σ (C28↔C33)**: Fisher 예측에서 mainstream 2 이 DR3 으로도 구분 불능. "multiple winning families" 주장 시 Fisher pairwise 확인 필수.
- **Production MCMC budget**: 100ms/call × 48 × 2000 = 5–6 시간/후보. budget-limited K13 fail 은 posterior 위치 문제 아님. 고성능 환경 재실행 전까지 "formal K13 미통과" 명시 필수.
- **dynesty 3.0.0**: `rstate` 는 `np.random.default_rng(seed)` 로 전달. `np.random.RandomState` deprecated.
- **dynesty 병렬 run_one.py 패턴**: `OMP/MKL/OPENBLAS_NUM_THREADS=1` 강제 + 후보별 별도 프로세스. `wait $(pgrep ...)` 는 다른 쉘 자식이 아니면 동작 안 함 — Python subprocess.Popen + poll loop 사용.
- **Zero-parameter alt vs 1-parameter 이론 Bayesian 우열 없음**: Δ ln Z gap (A12 vs C28) = 0.48, Occam penalty ≈ 0.5. 데이터가 자유도 추가를 정당화하지 않음. 논문에서 "extra parameter preferred by data" 주장 금지.
- **chi2_joint_with_shear 는 S_8 WL 추가 채널**. 기본 chi2_joint 는 BAO+SN+CMB+RSD 만. 결과 보고 시 어떤 버전 썼는지 항상 명시.

## L6 재발방지 (Phase-6 추가)

- **Occam-corrected evidence vs fixed-θ evidence 혼동 금지**: L5 fixed-θ Δ ln Z 는 extra param 을 MAP 에 고정한 값. L6 fully marginalized Δ ln Z 는 반드시 낮음 (Occam 패널티). 보고 시 어느 쪽인지 명시 필수. "fixed-θ" 없이 L5 숫자 인용 금지.
- **Compressed CMB chi2 는 chi2_joint 내 'cmb' 키 직접 사용**. Hu-Sugiyama θ* 재계산 시도는 4.6e6 chi2 오류 발생 확인 (L6-G3). hi_class 미설치 시 chi2_joint 'cmb' 만 사용, K19 "provisional" 명시.
- **Occam 정당화 판정식**: `net_gain = delta_logz_gap + occam_diff; justified = net_gain > 0`. `abs(gap) > abs(occam_diff)` 는 틀린 공식 — C11D 가 잘못 "정당화"되는 버그 발생 확인 (L6-E3).
- **Amplitude-locking "이론에서 유도됨" 주장 금지**: Δρ_DE ∝ Ω_m 은 SQMH 소멸항 구조에서 부분 도출 (Q17 부분 달성). Exact coefficient=1 은 E(0)=1 정규화 귀결이며 동역학적 유도 아님. K20 미해당.
- **C28 K13 fail 은 5D 비혼합 문제**: R̂=1.3653, MCMC Δχ²=+5.272 는 신뢰 불가. C28 주요 지표는 Bayesian evidence (fixed-θ +11.257, marginalized +8.784). "C28 Δχ² = +5.272" 를 물리적 결론으로 인용 금지.
- **C28 은 Maggiore-Mancarella 독립 이론**: "C28 이 SQMH 모델" 주장 금지. 8인 팀 합의 (L6-T3). SQMH 와 phenomenological 일치만 주장 가능.
- **JCAP 타깃 조건**: 8인 합의 "정직한 falsifiable phenomenology" 포지셔닝. PRD Letter 진입 조건: Q17 완전 달성 OR (Q13 + Q14) 동시 달성. 조건 미달 상태에서 PRD Letter 제출 금지.
- **DR3 스크립트 실행 금지 (DR3 공개 전)**: simulations/l6/dr3/run_dr3.sh 는 DESI DR3 공개 후에만 실행. 미공개 상태에서 실행 시 bao_data 저장소에 DR3 디렉터리 없어 즉시 exit 1.
- **mu_eff ≈ 1 은 S8 tension 해결 불가**: 모든 L5 winner 가 μ_eff ≈ 1 (GW170817 + background-only 구조). "SQMH 이 S8 tension 을 해결" 주장 금지. ΔS8 < 0.01% (Q15 전원 FAIL).
- **L6 8인/4인 규칙**: 이론 클레임 (amplitude-locking, disformal PPN, 포지셔닝) → Rule-A 8인 순차 리뷰 필수. 코드 (evidence 스크립트, 성장 계산, CLASS 근사) → Rule-B 4인 리뷰 필수. 리뷰 완료 전 결과 논문 반영 금지.
