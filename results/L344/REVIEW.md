# L344 REVIEW — P9+P11 forecast 종합

## 본 loop 요약
- 독립 loop, L341 등급 -0.08 carry-over (변경 없음).
- 주제: P9 (dSph) + P11 (NS saturation) anchor 동시 추가 시 3-regime vs 2-regime
  분리 ΔAICc 정량 forecast.
- 산출 형태: **forecast only** (실측 없음, FIM/mock 미실행, 8인 사전 분석 기반).

## 핵심 forecast (8인 합의)

| Anchor 구성 | ΔAICc(2→3) 중심 | 1σ | 강제 (≤-2) 확률 |
|-------------|------|----|----|
| 4 anchor (현 baseline) | +0.77 | ±0.5 | ~5% |
| 5 anchor (+P11) | -1.8 | ±2.0 | ~35% |
| 5 anchor (+P9) | +0.5 | ±1.0 | ~10% |
| **6 anchor (+P9+P11)** | **-1.7 ± 2.2** | ±2.2 | **~40-45%** |
| 6 anchor + systematic 보정 | -1.5 ± 2.5 | ±2.5 | ~35-40% |

## 핵심 결론
1. **P11 이 dominant driver** (regime 2↔3 saturation 신호).
2. **P9 는 보조** (regime 1↔2 곡률, H0 degeneracy 로 effective 정보 ↓).
3. **결합 cross-term bonus 10-20%**, 단 systematic marginalize 시 상쇄 가능.
4. **3-regime 강제 입증 확률 ~40%** — coin flip 보다 약간 유리, 무조건 입증 아님.
5. L332 의 **2-regime baseline 결정 유지**. P11 실측 도착 후 재판정.

## 정직 limitation
- 본 forecast 는 8인 사전 분석 기반, FIM mock 미실행. 실 시뮬 후 ±50% 변동 가능.
- P9 의 dSph kinematics 신호가 H0 prior 와 분리 가능한지 정량 미검증.
- P11 NS saturation 의 turnover 형태가 sigmoid-weight 가 흡수 못 하는 차이를
  실제 만드는지 확실치 않음.
- EOS + dSph M/L systematic 동시 marginalize 시 effective DOF 감소 정확히 미정량.

## 논문 영향 (carry-over 권고)
- Sec 3 baseline 표기: "2-regime, 3-regime 부록" 유지 (L332 권고 변경 없음).
- Sec 7 future work: "P9+P11 동시 anchor 추가 시 3-regime 강제 가능성 35-45%
  forecast (FIM 기반, 미실측)" 추가.
- Sec 6 limitation 13 신규: "anchor 확장 후에도 3-regime 강제 *조건부*, 무조건
  입증 어려움" 정직 기록.

## 등급 영향
- 본 loop: forecast only, 새 데이터/이론 없음 → 등급 변경 없음.
- 등급 carry-over: ★★★★★ -0.08 (L341 그대로).
- JCAP carry-over: 90-94% (L341 그대로).

## 다음 step
- L345 P11 mock 재실행 → L346 P9 mock → L347 joint → L348 systematic robust
  → L349 kill-switch 판정.
- kill switch: joint forecast median > -1 시 3-regime 강제 단념.

## 한 줄 (정직 한국어)
> P9+P11 동시 추가해도 3-regime 강제 입증 확률 ~40%, 무조건 입증은 아니다 — P11 단독 forecast(-1.8) 이 사실상 driver이며 P9 는 보조 역할에 그친다.
