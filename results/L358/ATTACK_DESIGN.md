# L358 ATTACK_DESIGN — dynesty nested sampling vs emcee multimodal posterior 검출

## 목적
SQMH BAO+SN+CMB joint posterior 가 multimodal 인지, emcee 가 single mode 만 잡고 있는지 dynesty nested sampling 으로 독립 검증.

## 동기 (정직 한국어 한 줄)
emcee MCMC 는 ensemble walker 들이 시작 분포의 basin 에 갇혀 다른 mode 를 못 보는 경향이 있고, dynesty 는 prior 전역에서 출발하므로 multimodal posterior 를 발견하기 좋다.

## 핵심 차이 (dynesty multinest vs emcee)

| 항목 | emcee (affine-invariant ensemble MCMC) | dynesty (nested sampling, multi-ellipsoid) |
|---|---|---|
| 출발 분포 | walker 초기값 근방에 강하게 의존 | prior 전체에서 균등 sampling |
| Multimodal | walker 가 한 basin 에 빠지면 다른 mode 못 봄 | bounding ellipsoid 가 자동 분리 (`bound='multi'`) |
| Evidence ln Z | 직접 산출 불가 (post-hoc) | 알고리즘 자체가 ln Z 를 1차 산출 |
| 수렴 진단 | R̂, autocorr time | live point 의 ln L_max - ln L_live 잔여 |
| 비용 | walker × steps; cheap per call | nlive × niter; 비싸지만 evidence 무료 |
| 실패 모드 | 한 mode 갇힘 / R̂>1.1 | bound 가 mode 사이 gap 못 잡으면 mode 합쳐짐 |

## 대상 모델
- A12 erf-diffusion (zero-param, baseline)
- C28 Maggiore-Mancarella RR non-local (1-param: c0)
- C11D disformal IDE (1-param: γ)
- L33 sigmoid-mixture champion (Q93, 4-param: c, amp, amp_hi, Om)

## 실험 설계
1. **emcee 재실행 baseline**: 48 walker × 4000 step, seed 42, R̂ + autocorr 기록
2. **dynesty static, bound='multi'**: nlive=1000, sample='rwalk', dlogz=0.01
3. **dynesty dynamic**: nlive_init=500, nlive_batch=250, posterior-weighted
4. **mode 비교**:
   - dynesty 가 ≥2 ellipsoid 로 분리하면 multimodal 의심
   - emcee chain 의 KDE 와 dynesty equal-weight posterior 의 KDE 를 KL divergence 로 비교
   - 차이 > 0.1 nat 시 emcee 가 mode 놓쳤을 가능성

## 합격 기준 (Pass/Fail)
- **K-L358-1 (mode count)**: dynesty 가 발견한 modes 수 == emcee 가 보인 mode 수
- **K-L358-2 (ln Z 일관성)**: |ln Z_static - ln Z_dynamic| < 0.5
- **K-L358-3 (posterior agreement)**: Hellinger distance(emcee KDE, dynesty KDE) < 0.05 per param
- **K-L358-4 (champion 위치)**: dynesty MAP 와 emcee MAP 의 chi² 차 |Δχ²| < 1.0

## 위험 / 함정
- dynesty 3.0.0: `rstate=np.random.default_rng(seed)` 사용, RandomState deprecated (L5 재발방지)
- 워커당 스레드 1 강제 (`OMP/MKL/OPENBLAS_NUM_THREADS=1`)
- L33 4D 의 Om bounds [0.05, 0.50] 충분히 넓게 (low-Om mode 놓치지 말 것)
- chi2 에서 None/nan → `return -np.inf` (sentinel 합산 금지)
- multi-ellipsoid bound 가 너무 작으면 mode merging, 너무 크면 efficiency 폭락 → enlarge=1.25 권장
- 후보당 dynesty static 1000 live + 4D = 30~60 분/후보. 후보별 분리 프로세스.

## 산출
- `dynesty_<model>_static.pkl`, `dynesty_<model>_dynamic.pkl`
- `compare_emcee_dynesty.json`: ln Z, modes, Hellinger, MAP
- corner plot overlay (emcee 파랑 vs dynesty 빨강)
