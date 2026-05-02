# L405 — 8인팀 다음 단계 설계 (Δln Z 강화 path)

세션 일자: 2026-05-01
선행: L405/ATTACK_DESIGN.md (B1–B10)
원칙: CLAUDE.md [최우선-1, 2] — 방향만 기술, 수식/파라미터값 미지정.

---

## 1. 8인팀 토의 시뮬 (요약)

**P1:** "Δln Z 강화는 (a) likelihood 증대 (anchor 추가) 또는 (b) prior volume
패널티 감소 (R 좁힘) 두 길 뿐. (b) 는 자의 의심 — (a) 가 정도다."

**P2:** "추가 anchor 후보는 paper §4 22-예측 표의 P9 dSph (Draco/Sculptor 류
저밀도 dwarf, log10 ρ_env ~ -0.5) 와 P11 NS (중성자별 표면, log10 ρ_env ~ +6).
두 점은 현재 anchor 8개 (galactic+cluster+cosmic) 의 *공백* 영역 — 새 anchor 는
4-axis 미시 σ₀(env) 모델 의 추가 *test* 점."

**P3:** "통계 forecast 두 시나리오: (S_compat) 새 anchor 가 3-regime 예측과
일치 → Δln Z 증대. (S_tension) 새 anchor 가 monotonic 쪽으로 쏠림 → 3-regime
기각. 둘 다 *데이터 후 판단* 이 아닌 *사전 등록* 으로 이행해야 신뢰."

**P4:** "prior R sensitivity 는 R={2,3,5,10} 4점 grid 가 표준. R=2 는 narrow
overfitting 위험, R=10 은 Lindley wide-prior collapse 위험. Δln Z 곡선이
R 의 함수로 어떻게 변하는지가 referee 가 보고 싶어 하는 표."

**P5:** "Laplace 근사는 Hessian 양정치 가정에 의존. 3-regime threshold 파라미터
t1, t2 근처 likelihood 가 *불연속* 인 hard step 모델은 Laplace 가 underestimate.
dynesty (nested sampling) 으로 full posterior 적분 필수 — 본 L405 run.py 의
smoke test 가 첫 단계."

**P6:** "철학적으로 — Δln Z 강화 시도가 *post-hoc dredging* 이 되지 않으려면
(a) 추가 anchor 선정 기준을 새 데이터 보기 *전* 에 등록, (b) tension 시나리오
falsifier 를 명시. P9 dSph σ₀ 가 monotonic 예측과 +1σ 이상 일치하면 3-regime
기각, 등."

**P7:** "JCAP timeline: PAPER submission *전* 에 본 R-grid 표 추가는 minimum.
추가 anchor 실측 (P9 dSph: Gaia DR4 stellar dynamics + Spitzer 잔존물; P11 NS:
NICER X-ray timing) 은 2026-2028 timeline — pre-registration 하고 paper 본문
에서 'gated falsifier' 로 명시."

**P8 (synthesizer):** "다음 단계 합의:
(a) 즉시 (이번 세션): R={2,3,5,10} grid + 추가 anchor forecast (S_compat
    /S_tension) + dynesty smoke test. → simulations/L405/run.py.
(b) 1주 내: 실 SPARC + cluster + cosmic anchor 데이터로 full dynesty MCMC
    (ndim=5, nlive≥500). budget 추정: ~수시간 단일 후보당. L406 분리.
(c) 1개월 내: P9 dSph 후보군 (Draco, Ursa Minor, Sculptor) σ₀ 추정치
    문헌 수집. P11 NS (J0740+6620) NICER 결과 인용 가능성 확인.
(d) pre-registration: GitHub release tag — '추가 anchor 일치 시 Δln Z 측정,
    불일치 시 3-regime 기각' 사전 명시."

---

## 2. 다음 단계 task list

| # | task | 즉시? | budget |
|---|------|------|--------|
| N1 | R={2,3,5,10} Laplace grid scan (toy → 실 anchor) | YES (toy) | <1min |
| N2 | extra anchor (P9 dSph, P11 NS) forecast (S_compat / S_tension) | YES | <1min |
| N3 | dynesty smoke test (toy 3-regime, nlive=80) | YES | ~1min |
| N4 | dynesty production (실 데이터, nlive=500, 4 model) | NO (L406) | 수시간 |
| N5 | P9 dSph σ₀ 후보군 문헌 정리 (Draco/UMi/Scl) | NO (L407) | 1 day |
| N6 | P11 NS (NICER J0740) σ₀ 정량 가능성 검토 | NO (L407) | 1 day |
| N7 | pre-registration GitHub tag (추가 anchor falsifier) | NO (L408) | 0.5 day |
| N8 | paper §3.6 재작성 (B1, B2, B7, B10 회피) | NO (paper-side) | 별도 |

본 세션은 N1–N3 (즉시 task) 만 수행 — simulations/L405/run.py.

---

## 3. 회복 가능성 정직 판정

- Δln Z 가 R-grid 전체에서 양수로 안정 + 추가 anchor 일치 시 → 0.8 → ~2-3
  영역 (Jeffreys "substantial") 진입 가능.
- R-grid 에서 Δln Z 가 R=10 에서 음수로 떨어지면 Lindley fragility 확정, paper
  §3.6 본문 회복 *불가능* — 3-regime 자체 framework-FAIL 사전 인정 필요.
- 추가 anchor 가 tension 시나리오 (monotonic 쪽 일치) 면 3-regime 기각, paper
  §3.4 caveat (postdiction) 가 falsifier 로 활성화.

→ **본 L405 run.py 결과** (results/L405/run_log.txt + report.json) 가 Δln Z
회복 path 의 *첫 진단* 임. REVIEW.md 에서 4인팀이 결과 해석 자율 분담.
