# L359 ATTACK DESIGN — MCMC Convergence Diagnostics

## 목적
SQMH 후보 모델의 MCMC posterior가 "수렴됨"으로 간주될 수 있는 정량적 임계 spec을 정의하고, 모든 L4~L33 산출 chain에 대한 사후 진단 절차를 표준화한다.

## 진단 4종 (병렬 적용)
1. Gelman-Rubin Rhat (split-chain, rank-normalized)
2. Effective Sample Size (ESS-bulk, ESS-tail)
3. Autocorrelation time τ_int (emcee `get_autocorr_time`)
4. Posterior Predictive p-value (PPC) — joint chi^2 분포 대비 관측 chi^2 위치

## Convergence Threshold Spec (PRIMARY 산출물)

| 진단 | 통과 임계 | 경고 영역 | 실패 |
|---|---|---|---|
| Rhat (split, rank) | ≤ 1.01 | 1.01–1.05 | > 1.05 |
| ESS-bulk (per param) | ≥ 400 | 100–400 | < 100 |
| ESS-tail (per param) | ≥ 400 | 100–400 | < 100 |
| τ_int 대비 chain length | N/τ ≥ 50 | 20–50 | < 20 |
| Burn-in 폐기 | ≥ 2τ_max | 1–2τ | < 1τ |
| PPC p-value | 0.05 ≤ p ≤ 0.95 | 0.01–0.05, 0.95–0.99 | < 0.01 또는 > 0.99 |
| MCSE / posterior std | < 0.05 | 0.05–0.10 | > 0.10 |

PASS 판정: 모든 파라미터에서 Rhat ≤ 1.01 AND ESS-bulk/tail ≥ 400 AND N/τ ≥ 50.
WARN: 한 항목이라도 경고 영역이면 chain 연장 후 재진단.
FAIL: 한 항목이라도 실패 영역이면 결과 인용 금지.

## 적용 대상
- L4~L6 emcee (48 walker × 2000 step) joint MCMC chain
- L33~L34 BAO/joint scan chain
- L46~L56 최근 simulation chain

## 도구
- `arviz.rhat`, `arviz.ess(method="bulk")`, `arviz.ess(method="tail")`
- `emcee.EnsembleSampler.get_autocorr_time(tol=0)`
- PPC: posterior draw별 chi^2 재계산 (BAO+SN+CMB+RSD), 관측 chi^2 분위수.

## 정직성 원칙
임계 미달 chain의 posterior 수치 인용 금지. 논문 본문 표는 PASS chain만 인용, WARN/FAIL은 supplementary에 별도 표기.

## 한국어 한 줄
정직: 다수 L4~L6 emcee chain은 N/τ < 50로 본 spec의 PASS 기준에 미달할 가능성이 높다.
