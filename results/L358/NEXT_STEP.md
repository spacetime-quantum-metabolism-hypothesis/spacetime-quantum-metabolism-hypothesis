# L358 NEXT_STEP — dynesty vs emcee 실행 계획

## 정직 한국어 한 줄
emcee 가 single-mode posterior 만 보고 있을 위험을 dynesty nested sampling 으로 독립 확인하고, 차이가 크면 L5/L6 의 evidence 결론을 재검토한다.

## Step 1 — 환경 점검 (10 분)
- `python3 -c "import dynesty; print(dynesty.__version__)"` ≥ 2.1
- emcee, numpy, scipy 버전 확인
- joint chi² 함수 (BAO+SN+CMB+RSD) 가 None/nan 시 -inf 반환하는지 확인 (L4 재발방지)
- `_jsonify` 재귀 변환기 준비 (np.bool_/np.float_ json 깨짐 방지)

## Step 2 — emcee baseline 재현 (후보당 ~30 분, 4 후보 병렬)
- 48 walker × 4000 step, burn 1000, seed 42
- 모델: A12, C28, C11D, L33-Q93
- R̂, τ_autocorr, MAP, ln L_max 기록
- `multiprocessing.get_context('spawn').Pool(4)` 사용

## Step 3 — dynesty static run (후보당 ~30~60 분, 4 후보 분리 프로세스)
```python
import os
os.environ['OMP_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
os.environ['OPENBLAS_NUM_THREADS']='1'

import dynesty, numpy as np
rng = np.random.default_rng(42)
sampler = dynesty.NestedSampler(
    loglike, prior_transform, ndim=ndim,
    nlive=1000, bound='multi', sample='rwalk',
    enlarge=1.25, rstate=rng,
)
sampler.run_nested(dlogz=0.01)
```
- subprocess.Popen + poll loop (L5 재발방지: `wait $(pgrep)` 금지)
- 후보별 별도 디렉터리 (sibling background.py 충돌 회피)

## Step 4 — dynesty dynamic run (선택, multimodal 의심 시만)
- nlive_init=500, nlive_batch=250
- `wt_kwargs={'pfrac':1.0}` posterior-우선

## Step 5 — 비교 분석 (~30 분)
- `dynesty.utils.resample_equal` 로 emcee 동등 weight chain 생성
- 각 파라미터별 KDE → Hellinger distance, KL divergence
- bounding ellipsoid 개수 = `sampler.results['bounditer'][-1]` 그러나 multimodal 진단은 `dyplot.cornerbound` 시각 확인 + manual GMM(n=2) BIC vs GMM(n=1) BIC
- corner plot overlay 저장

## Step 6 — 합격 판정 + 보고
- K-L358-1~4 표 작성
- emcee MAP 와 dynesty MAP 의 chi² 비교
- L5 winner (A12, C28) 의 ln Z 가 dynesty 에서 변동 시 L5 결론 재검토 트리거
- multimodal 발견 시 → L359 후속 (full posterior 재해석)

## Step 7 — 코드리뷰 (4인 자율 분담, CLAUDE.md 규칙)
- prior_transform 정확성
- chi² -inf 핸들링
- rstate 시드 통제
- json 직렬화 안정성

## 시간 예산
- 환경 + emcee baseline: 1 시간
- dynesty static 4 모델 (분리 프로세스): 2~4 시간
- 분석 + 리뷰: 1~2 시간
- **총 4~7 시간 / 1 GPU 불필요, 10코어 CPU 충분**

## 중단 기준
- dynesty efficiency < 0.001 (10시간 추정) → enlarge 1.5 또는 sample='rslice' 전환
- ln Z 분산 > 1.0 → nlive 2000 으로 증가
- multi-ellipsoid 가 1 개로만 수렴 → 'balls' bound 시도
