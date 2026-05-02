# L344 ATTACK DESIGN — P9+P11 anchor 추가 시 3-regime vs 2-regime ΔAICc forecast

## 상위 컨텍스트
- L341 등급 carry-over: ★★★★★ -0.08 (본 loop 독립, 등급 변경 목적 아님).
- L332 결정 baseline: 현 데이터에서 ΔAICc(2→3) = +0.77 (2-regime 우세). 3-regime
  강제성 약함, P11 단독 추가 시 mid-forecast ΔAICc ≈ -1.8 ± 2.0.
- L344 임무: **P9 (dSph) + P11 (NS saturation) 동시 추가** + 기존 4개 anchor
  유지 시 (총 5-6 anchor) 3-regime 분리가 *강제* 가능한지 정량 forecast.

## 핵심 질문
> 4-5 anchor 동시 운용 시 3-regime 강제 가능?
> 즉, ΔAICc(2→3) ≤ -2 (실질) 또는 ≤ -5 (강함) 에 도달하는 시뮬 fraction.

## 8인 독립 공격 (방향만, 수식 금지)

### A1 (anchor 정보 채널 분리)
- P9 dSph: 저-ψ regime (ratio ~1.0-1.1) curvature. **regime 1↔2 경계** 정보.
- P11 NS sat.: 고-ψ regime (ratio > 50) saturation/turnover. **regime 2↔3 경계**
  정보. 두 anchor 의 정보 채널이 *직교*에 가까움 → 누적 ΔAICc 가 단순 합산보다
  살짝 강할 수 있음 (cross-term ~ 10-20% bonus, regime 분리 자체가 명확해질 때).
- 결합 형태에서 P9 단독 +0.3, P11 단독 -1.8 의 직선 합 -1.5 보다 더 음수로
  ~ -1.7 ~ -2.3 가 합리적 중심값.

### A2 (자유도 패널티 재정렬)
- 3-regime 가 추가하는 자유도: regime-경계 위치 2 + regime-별 amp 분리 1 = +3
  실효 (이미 weight smoothing 흡수분 제외하면 +2).
- AICc 추가 패널티 ~ 4 ~ 6 (k 차이 2-3, 표본 N ≥ 25 가정).
- 즉 Δχ²(2→3) > 4-6 이어야 ΔAICc < 0. P11 단독 -1.8 (Δχ² ≈ 6 정도) 에 P9
  미세 +0.3 더해도 임계 도달은 *경계*.

### A3 (P9 dSph 정보 부족 위험)
- dSph kinematics 에서 SQT g(rm1) 곡률 신호는 H0 prior 와 강한 degeneracy.
  marginalize 후 effective 자유도 ↓ → P9 의 ΔAICc 기여가 +0.3 에서 -0.5 ~ +0.5
  로 spread.
- P9 가 *regime 1↔2 경계를* 직접 강제하는지 vs 단순 H0 추가 prior 인지 구분 필수.

### A4 (sigmoid-weight 모델 한계)
- 현 2-regime sigmoid-weight 가 이미 mid-high transition 을 일정 부분 흡수.
  P11 신호가 saturation **shape** (sigmoid 와 다른 turnover) 을 요구할 때만
  3-regime 가 강제됨. pure-amp 차이만이면 sigmoid-weight 가 흡수.
- 즉 P11 의 *형태* 가 sigmoid 와 다른 정도가 ΔAICc 의 핵심 driver.

### A5 (글로벌 입증 가능성 정량)
- L332 P11 단독: 30-40%.
- P9+P11 동시: cross-channel bonus + sample boost 로 **40-55%** 추정.
- 4-5 anchor 시 3-regime *강제* 가능성: 중심값 **45%**, 1σ ±15%.

### A6 (체계 오차 위험 강화)
- P9 dSph: stellar mass-to-light 불확실성 ~30%, anisotropy degeneracy.
- P11 NS sat.: EOS systematic 0.1-0.2 M_sun.
- 두 systematic 동시 marginalize 시 effective DOF ↓ → ΔAICc 신호 **15-25% 약화**.
- 보정 후 P9+P11 forecast 중심값: -1.5 ~ -2.0 (현실적).

### A7 (mock 시뮬 설계 권고)
- FIM forecast 1차: 1000 mock realization, P9+P11 noise 모델 양 설정 (낙관/중립/
  비관). 2-regime fit, 3-regime fit, AICc 차이 분포.
- 95% 시뮬에서 ΔAICc(2→3) < -2 면 강제 가능 결론. < 50% 면 baseline 유지.

### A8 (sequencing & kill switch)
1. P9 mock + P11 mock 독립 forecast (재확인).
2. 결합 mock joint fit (cross-term 측정).
3. EOS + dSph systematic marginalize 후 robust ΔAICc.
- Kill switch: 결합 forecast median ΔAICc(2→3) > -1 이면 3-regime 강제 단념,
  L332 의 2-regime baseline 결정 그대로 유지. 본 loop 는 negative result 로
  종결.

## 정량 forecast 합의 (8인 중앙값)

| Scenario | ΔAICc(2→3) 중심 | 1σ | 강제 (<-2) 확률 |
|----------|-----------------|----|----|
| 기존 4 anchor | +0.77 | ±0.5 | ~5% |
| +P11 단독 (5) | -1.8 | ±2.0 | ~35% |
| +P9 단독 (5) | +0.5 | ±1.0 | ~10% |
| +P9+P11 결합 (6) | **-1.7 ± 2.2** | ±2.2 | **~40-45%** |
| +P9+P11+systematic 보정 | -1.5 ± 2.5 | ±2.5 | ~35-40% |

## 핵심 답
> **4-5 anchor (P9+P11 포함) 시 3-regime 강제 가능 확률 ~40-45%**, systematic
> 보정 후 ~35-40%. P11 이 dominant driver, P9 는 보조. 글로벌 입증은 *조건부*
> 가능, 무조건 입증은 아니다. 2-regime baseline 유지 권고는 변하지 않음 — 단
> P11 실측 후 재평가 권장.

## 종합 판정
- 등급 carry-over ★★★★★ -0.08 (본 loop 등급 변경 없음).
- 3-regime 강제 forecast: *경계* (40-45%, systematic 보정 시 35-40%).
- 권고: P11 NS saturation 실측 우선. P9 dSph 는 H0 prior 보강 보조 anchor 로
  활용. 두 anchor 동시 도입해도 강제 입증은 *coin flip 보다 약간 유리* 수준.
- L332 2-regime baseline 결정 유지. P11 결과 도착 후 본 forecast 재판정.
