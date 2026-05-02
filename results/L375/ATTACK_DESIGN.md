# L375 ATTACK_DESIGN — SQT mock 100개 injection-recovery (BB σ_0 회수율)

## 배경
L361 은 5-dataset 풀버전 (BAO+SN+CMB+RSD+SPARC) joint MCMC injection-recovery 를 설계했으나
wall-clock ~55h 의 부담으로 본격 실행 전 단계에 머물렀다. L375 는 그 핵심만 잘라낸
**축약형(독립) injection-recovery**: BB anchor σ_0 단일 파라미터의 MAP 회수율을
100 개 SQT mock 으로 정직하게 측정한다.

## 8인 공격 (역할 사전 지정 없음)
- A1: SQT generative 와 BB recovery 모델이 **구조적으로 동일하면** 회수율 100% 인공물 — 두 모델이
  미세하게 어긋나야 정직.
- A2: σ_0 가 1D 지만 likelihood 가 평탄하면 회수율이 prior 폭에 좌우 — 좁은 prior 는 인공 PASS.
- A3: ±0.1 dex 임계는 ~26% bin (즉, log10 단위로 ±0.1) — Gaussian likelihood 폭과 동급이면
  회수율 자체가 noise σ 의 함수가 됨, 검정력 낮음.
- A4: N=100 → √N≈10 → 회수율 ±10pt 통계 noise. PASS 경계 68% 에서 56–80% 변동 가능.
- A5: MAP 만 보면 posterior tail/skew 정보 손실. 그래도 본 task 는 MAP 한정 — 정직 표기.
- A6: SQT 와 BB 모두 **toy** 로 구현 (실제 cosmology 데이터 미사용). 결과는 BB 메서드의
  *self-consistency check* 이지 SQMH 실데이터 우위 주장 아님 — 정직 표기.
- A7: numpy seed 분리. 각 mock seed 독립, fitter seed 별도 — silent collision 방지.
- A8: 회수율 외 **bias / RMSE** 도 동시 보고. PASS criteria 는 회수율 한정이지만 bias>0.05 dex 면
  계통 오류 시그널.

## Top 3
- A1 (모델 미스매치 — 인공 PASS 방지)
- A4 (N=100 통계 noise — 경계선 신뢰도)
- A6 (toy 한정 — 실데이터 주장 금지)

## 디자인 결정
- **SQT generative**: σ(z) = σ_0 · ψ(z), ψ(z)=1+α·z+β·z² (smooth growth template, 정해진 α=0.05, β=0.01).
  관측 데이터 d_i = σ(z_i)+ε_i, ε_i ~ N(0, η·σ_true(z_i)), η=0.10.
- **BB fit 모델**: σ(z) = σ_0_fit · ψ_fit(z), ψ_fit 동일 구조이지만 α_fit=0.07, β_fit=0.005 로
  의도적 미세 mismatch (A1). **σ_0 만 free**, α/β 는 anchor-fixed (L361 Branch P 처방).
- **Truth**: log10(σ_0_true) = 0.0 (즉 σ_0_true=1.0 dimensionless toy unit).
- **Mock 표본**: z grid {0.1, 0.3, 0.5, 0.8, 1.2, 1.6, 2.0} (7 점), 100 mock seed=0..99.
- **MAP**: scipy.optimize.minimize_scalar (bounded [-1, 1] in log10), Brent.
- **Recovery 임계**: |log10(σ_0_MAP) - log10(σ_0_true)| ≤ 0.1 dex.

## PASS / FAIL
- PASS: recovery rate > 68%.
- FAIL: ≤ 68%.

## 정직 한 줄
이 결과는 BB MAP 회수 self-consistency 의 toy 검증이며, SQMH 실데이터 우위와는 무관하다.
