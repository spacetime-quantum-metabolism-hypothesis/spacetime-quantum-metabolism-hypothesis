# L339 REVIEW — Cross-validation: SQT on alternative-theory mocks (사전 검토)

L329 의 22/25 cells SQT 우위 결과 + 1 cell (SymG f(Q)) 동률 위험 ⚠ 에 대한
*역방향 robustness 시험* 사전 검토. 실제 시뮬은 NEXT_STEP 권고에 따라 별도 세션에서 실행.

## 8인 자율 사전 평가

- **P** ("진정 신호 vs 자유도 분리"): L272 가 LCDM mock 에 BB 100% false detection 보였다.
  대칭으로 SymG mock 에 SQT BB 도 *wa<0 구조 부합 → 자동 fit* 가능성 높음.
  사전 추정: false-positive ~50–80%. 정직히 격하 시나리오 준비 필요.

- **N** ("SymG vs SQT 거리 metric 차이"): SymG f(Q) 의 H(z) 곡률 변화 폭이 SQT BB 3-regime 으로 거의 흡수 가능.
  → 실제 시뮬 전부터 "SQT 우위 wrongly detected" 가 *기대값* 임을 인정해야 함.
  L329 ⚠ 표기는 보수적, 실제로는 데이터 자유도 한계.

- **O** ("L208 vs L272 일관성"): L272 ΔAICc median 132.95 (LCDM mock).
  SymG mock 은 wa<0 까지 일치하므로 ΔAICc 분포 *median 0 근처* 일 가능성 — false-positive rate 30–50% 추정.

- **H** ("anchor predetermined 조건"): L272 결론과 동일. SQT σ_0 3 regime 가 *theory-prior* 로 동결되면
  false-positive rate 급감. *data-fit* 이면 100% 위험.
  L339 시뮬은 anchor freeze / free 두 모드 모두 돌려야 의미.

- **F** ("판정 기준 cutoff"): ΔAICc<−10 = strong false-positive.
  −10 ~ −2 = marginal (Occam 가능). 보고 시 둘 분리 필수.

- **G** ("MOND/TeVeS/EMG mock 가능성"): MOND/TeVeS 우주론적 거리 mock 은 nonlocality 로 ill-defined.
  EG 는 거리 자체 없음. EMG 는 galaxy-scale 만. → L339 1차는 *SymG only* 가 옳다.
  나머지는 cosmological 거리 mock 자체 부적격.

- **R** ("L329 결론 영향"): false-positive >30% 면 SymG-cell ⚠→✗, 22/25 → 21/25.
  여전히 글로벌 우위. 그러나 "5-alternative 압승" 톤 다운 필요.
  False-positive <5% 면 ✓ 승격, 23/25 — 강한 promo.

- **A** ("논문 톤"): 결과 어느 쪽이든 paper 에 별도 box 필요.
  L272 "anchor predetermined" box 와 합쳐 "two-sided mock test" 섹션 구성 권장.
  결과 왜곡 금지 (CLAUDE.md 재발방지).

## 4인 사전 코드 검토 노트 (자율 분담, 시뮬 실행 전)

- SymG f(Q) mock 생성: Frusciante 2021 원본 배경 ODE. n≥1 강제. L3 toy 절대 금지 (부호 역전).
- Forward shooting (matter era → today). Backward 금지 — phantom 경계 폭주 (CLAUDE.md k-essence 항).
- BAO 13pt 풀 공분산. D_V/D_M/D_H 분리, D_V만 fit 금지.
- DESY5 zHD + 해석적 M marginalisation (Conley 2011).
- compressed CMB θ* 0.3% theory floor.
- AICc k 비대칭 명시: k_SQT (BB amp_lo, amp_hi, rolloff 등) vs k_SymG (f_1, n).
- numpy 2.x: np.trapezoid 직접. ratio 클리핑 [1, 200] (L33 재발방지).
- multiprocessing spawn + 9 worker + thread=1 강제.

## 정직 사전 결론

- L339 의 *기대 결과* 는 SQT false-positive 30–80% 구간.
  → L329 ⚠ 표기가 사실상 ✗ 에 가까울 가능성.
- 그래도 cross-validation 실시 자체가 정직 도구 — 결과 어느 쪽이든 논문 신뢰도 상승.
- 사전에 "SQT 가 SymG mock 에 false-positive 보일 가능성 큼" 을 인정함으로써
  결과 발표 시 cherry-picking 의혹 차단.

## 한 줄 사전 판정
**시뮬 실행 권고. 결과 false-positive >30% 시 L329 SymG-cell 정직 격하, 글로벌 22/25 → 21/25 + 톤 조정.**
