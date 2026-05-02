# L374 REVIEW — 4인 코드리뷰 (자율 분담)

> CLAUDE.md 원칙: 역할 사전 지정 금지. 4인이 자율적으로 검토 영역을 분담.
> 본 문서는 Rule-B (코드 리뷰) 자율 분담 결과 정리본.

## 분담 결과 (자연 발생)
- **R1**: 시드/스레드/재현성 — `run.py` 환경설정 전반.
- **R2**: 토이 likelihood 수학적 일관성 — chi^2, prior, 양정부호.
- **R3**: emcee 사용법 + chain 축 처리 + autocorr 호출.
- **R4**: 진단 지표 (R-hat, ESS) 계산 정합성 + JSON 직렬화.

---

## R1 — 환경/재현성
- `OMP/MKL/OPENBLAS_NUM_THREADS=1` 을 `import numpy` 이전에 설정 → CLAUDE.md 시뮬레이션 원칙 준수.
- `np.random.seed(SEED)` + `default_rng(SEED)` 양쪽 모두 고정. emcee stretch move 가 전역 `np.random` 을 쓰므로 둘 다 필요 (CLAUDE.md 재발방지).
- `np.seterr(all='ignore')` Windows/Py3.14 안정화.
- 결론: PASS.

## R2 — 토이 likelihood
- `inv_sigma = A.T @ A + 0.5 I` → 양정부호 보장 (ridge term).
- prior: 박스 |θ|<5 + N(0,1) Gaussian. 박스가 충분히 넓어 walker 절단 없음.
- 5 dataset chi^2 합산으로 6D Gaussian posterior 가 형성. 알려진 unimodal 분포 → smoke test 적격.
- 결론: PASS. (단, 실제 SQMH 물리 likelihood 가 아님은 ATTACK_DESIGN.md 에 명시.)

## R3 — emcee 사용
- `EnsembleSampler(N_WALKERS, NDIM, log_prob)` 표준 사용.
- `get_chain()` 기본 shape (n_steps, n_walkers, ndim) → swapaxes 로 (walkers, steps, ndim) 변환 후 burn-in 잘라냄. 축 처리 명시적이고 정확.
- `get_autocorr_time(tol=0)` — 200 step 은 권장 50*tau 미달 가능성이 있어 tol=0 으로 raise 회피, exception 시 NaN 후 보고. smoke test 목적상 적절.
- progress=False (조용한 실행).
- 결론: PASS.

## R4 — 진단 + 직렬화
- Gelman-Rubin: walker 를 2 등분하여 split-Rhat 계산. `var_hat = (1-1/n)W + B/n; Rhat = sqrt(var_hat/W)`. 표준 공식.
- ESS = n_walkers * (n_steps - burn) / tau — 표준 정의.
- pass criteria: R-hat<1.2 (smoke 느슨), τ<n_steps/2, ESS>50.
- `jsonify()` 재귀 변환기로 `np.bool_/np.floating/np.ndarray/NaN→null` 처리 (CLAUDE.md L4 재발방지).
- 결론: PASS.

---

## 실측 결과 (run.py 실행)
- elapsed: 0.33 s (10코어 단일 프로세스, 200x200 chain, 6D).
- acceptance_fraction: 0.517 (이상적 범위 0.2~0.5 상단, OK).
- R-hat max: 1.0089 (전 6 파라미터 < 1.01) — 기준 1.2 대비 압도적 통과.
- autocorr_tau max: 17.81 step — 기준 100 (n_steps/2) 통과.
- ESS min: 1684.3 — 기준 50 대비 33배 여유.
- convergence_pass: **true**.

## 종합
4 인 자율 분담 리뷰 결과 코드/수치 모두 이상 없음. emcee 파이프라인은 5-dataset joint
chi^2 toy 에서 200x200 chain 으로 충분한 수렴(R-hat<1.01, ESS>1600) 을 달성.

## 정직 한 줄
이건 emcee 파이프라인 smoke test 의 통과일 뿐, SQMH 물리에 대한 어떤 주장도 아니다.
