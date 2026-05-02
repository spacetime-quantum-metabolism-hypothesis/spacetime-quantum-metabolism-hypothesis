# L361 — 5-dataset mock injection-recovery (L272 follow-up)

## 배경
L272 는 *LCDM mock* 에 BB 를 적용해 100% false-detection (overfitting artefact) 을 확인했다.
대칭 질문이 남는다: **SQT mock 에 BB 를 적용하면 truth 를 회수할 수 있는가?**
회수 실패면 BB 식별력 자체가 무력 — 회수 성공이라야 L272 의 "anchor predetermined" 처방이 의미를 가진다.

## 8인 공격
A1: "SQT truth 가 입력일 때 BB 가 truth 파라미터를 1σ 안에 회수하지 못하면, 실데이터 BB 우위는 운에 불과."
A2: "5-dataset (BAO+SN+CMB+RSD+SPARC-like) joint likelihood 의 cross-dataset tension 이 mock 에서 인공적으로 완화돼 coverage 과대평가 위험."
A3: "Posterior coverage 68/95 % nominal vs empirical — under-coverage 1.5×↑ 면 reviewer kill."
A4: "SQT injection seed N=100 충분한가? √N 통계 noise 가 ±5% 라 PASS 경계에서 위험."
A5: "Anchor σ_0 를 mock 마다 *theory-prior* 로 고정 vs *data-fit* 으로 풀어줄 때 회수율 차이 — L272 처방 검증."
A6: "MCMC convergence (R̂<1.05) 100 회 모두 통과? 일부 비수렴 chain 을 silent drop 시 selection bias."
A7: "BB vs universal 모델선택 reversal: SQT injection 인데 universal 이 우위 나오면 prior volume artefact."
A8: "Time-budget: 100 mock × 5-dataset MCMC ≈ 5 시간/mock × 100 = 500h. 병렬 9-core 에서 ~55 시간 — 실현 가능?"

## Top 3
- A1 (truth recovery — 핵심 정량)
- A3 (coverage calibration — reviewer kill 라인)
- A5 (anchor 처방 검증 — L272 와 직결)

## PASS 기준
- BB recovery rate (truth 1σ 안): ≥ 68% (nominal coverage)
- 95% credible interval coverage: 90–98% empirical
- ΔAICc(BB-universal) median > 0 (BB 우위 회복)
- Anchor *theory-prior* 고정 시 회수율 ≥ data-fit 시 회수율 — L272 처방 정당화

핵심 한 줄: SQT mock 에서 BB recovery rate 가 nominal coverage 와 일치하는지가 BB 식별력의 사활.
