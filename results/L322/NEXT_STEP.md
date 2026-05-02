# L322 — Next Step (8인 합의)

## 실행 계획

### Step 1: Multi-start MAP search (A4, 본 loop)

- N_start = 100. Latin hypercube on σ_0 = (σ_cos, σ_clu, σ_gal) ∈ [3.0, 15.0]^3.
- Optimizer: scipy `minimize(method='Nelder-Mead', xatol=1e-3)`.
- Objective: BB toy χ² (3-regime synthetic surface — 본 loop 내부에서 정의, fitting target = current best (8.37, 7.75, 9.56) 와 anchor flexibility 가정 mock).
- Cluster minima: distance < 0.3 unit 인 결과를 같은 mode 로 그룹화.
- 기록: 모드별 (σ_0 위치, χ², count).

### Step 2: Regime-merge ΔAICc (A5, 본 loop)

- Model M3 = 3-regime (k=3 σ_0). Model M2 = (cos+clu) merge → k=2.
- 같은 mock χ² 위에서 best-fit χ²_M2, χ²_M3.
- AICc = χ² + 2k + 2k(k+1)/(N-k-1). N = data point count.
- ΔAICc(M3 - M2) > 0 → M2 이김 (over-partition 증거).

### Step 3: Honest report

- Mode count 보고, alternative mode 가 있다면 좌표와 χ² 명시.
- Merge model 이 이기면 SQMH 3-regime 강제성 약함 — 정직 기록.

### Step 4 (deferred → L323)

- dynesty multimodal sampling, full BAO+SN+CMB+RSD likelihood. ndim=3 free σ_0.

## 코드 분담 (4인팀, 자율)

- run.py 단일 파일. Latin hypercube + multi-start + merge model + AICc 계산 + 결과 JSON dump.
- multiprocessing.spawn Pool(8) 로 100 start 병렬화.
- 워커당 OMP/MKL/OPENBLAS=1 강제.
- 출력: /Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L322/multistart_result.json

## 성공 / 실패 기준

- 성공: distinct mode = 1 AND ΔAICc(M3-M2) < -2 → 단일 global, 3-regime 정당화.
- 부분 성공: mode = 1 AND ΔAICc ∈ [-2, +2] → global 단일이지만 partition 약함.
- 실패: mode ≥ 2 OR ΔAICc > +2 → multimodal / over-partition. 정직 기록 후 논문 limitations 추가.
