# L377 ATTACK DESIGN — dynesty NS smoke test

## 목적
3-파라미터 BB(Black-Body / bimodal-bowl) 합성 likelihood 위에서 dynesty static
nested sampling 이 멀티모달 posterior 를 검출하고 ln Z 를 안정적으로 산출하는지
smoke test. SQMH 본 분석 (joint cosmology MCMC) 에 dynesty 도입 가능성 평가.

## 설계
- 데이터: 합성 (실측 데이터 없음). 3D 가우시안 두 개의 등가중치 혼합.
  - mode A center = (-2, -2, -2), mode B center = (+2, +2, +2), sigma=0.5 isotropic
  - 두 모드 간 분리 ~6 sigma → bona-fide multimodal
- 파라미터: theta = (x, y, z), uniform prior U(-5, +5)^3
- ln Z 해석값: ln Z = ln[(2*(2π)^(3/2) sigma^3) / 10^3]
  = ln[2 * 15.7496 * 0.125 / 1000] = ln(0.003937) ≈ -5.537
- live points = 100, sampler='rwalk' (multimodal 안전), tol=0.1
- mode count: dead-points 위치를 KMeans(2) 로 분리 후 각 mode 의 weight 비교

## 합격 기준
- C1: dynesty 정상 종료, ln Z 추정값 finite
- C2: |ln Z - (-5.537)| < 0.5 (live=100 의 expected error)
- C3: posterior sample 의 cluster 2 개 모두 weight > 0.2 (둘 다 발견)

## 정직 한 줄 약속
실측 데이터 없는 합성 toy. 본 분석 (BAO+SN+CMB) 에 그대로 적용 금지.
