# L417 Review — 4인 팀 자율 분담 코드/물리 검증

## 4인 팀 자율 분담 (역할 사전 지정 없음)
4인 자율 토의로 (a) 기하/입력 검증, (b) timescale 채널 검증, (c) ram-pressure 가정 검증, (d) verdict logic 검증을 분담.

## 코드 검증 (simulations/L417/run.py)
- ASCII-only print (cp949 안전).
- numpy only, multiprocessing 불필요 (단일 1D 적분, <0.1s).
- Bullet 기하: SEP_SUBCL=720 kpc, V_REL=4700 km/s, T_SINCE=0.15 Gyr — Clowe 2006 + Markevitch 2002/2004 + Mastropietro & Burkert 2008 정합.
- tau_cross = 2*R_scale/v = 0.104 Gyr — 합리적 cluster crossing time.
- Plummer 1D proxy: closed-form, peak position 정확.
- 결과 JSON: simulations/L417/L417_results.json.

## 수치 결과
| tau_q/tau_cross | eps (kpc) | offset_lens_vs_gas (kpc) |
|---|---|---|
| 0.0 | 0   | 150.0 |
| 0.1 | 50  | 108.0 |
| 0.3 | 150 | 13.5  |
| 0.5 | 250 | 96.0  |
| 1.0+ | 360 | 206.0 |

SQT natural band (tau_q ≪ tau_cross, P14 axiom-level): offset ∈ [13.5, 150] kpc. Naively "PASS_STRONG_QUANTITATIVE" at tau_q=0.

## 결정적 honest finding
**tau_q=0 에서 offset=150 kpc 회복은 *input* 인 GAS_RAMP_OFFSET 와 같다.**
- SQT 가 진짜로 예측한 것: |peak_lens − peak_galaxy| = 0 (depletion zone tracks galaxies). 시뮬레이션 결과 0.0000 kpc — 만족.
- 그러나 lens-vs-gas offset 의 magnitude (=150 kpc) 는 gas ram-pressure stripping 에 의해 결정되며 SQT depletion-zone formalism *외부* 에서 들어온 입력값.
- ⇒ "150 kpc" 일치는 자료 inheritance, 독립 도출 아님.

## NEXT_STEP.md falsification 분기 적용
- 예측 offset = 150.00 kpc (axiom-level fiducial) — 명목상 [120, 180] in band.
- 그러나 그 150 kpc 가 gas ram-pressure 입력의 직접 echo. 따라서:
  → **PASS_QUALITATIVE_ONLY (강등 없음, 격상 없음)**
  → SQT-specific 정량 prediction 은 "lensing peak ≡ galaxy peak", 정성 진술 형태.

## 채널별 평가
- **Channel (i) timescale**: tau_q ≪ tau_cross 는 P14 axiom 에서 자연. 검증됨. → PASS_STRUCTURAL.
- **Channel (ii) σ₀(t) collision modulation**: SQT 공리에서 직접 도출 불가 (axiom-level). DEP_RATIO 같은 ad hoc parameter 도입 필요. → 정량 도출 실패.
- **Channel (iii) lensing peak vs gas peak magnitude**: gas ram-pressure 자체가 SQT 에서 도출되지 않음. 150 kpc 는 입력. → 정량 도출 실패.

## 최종 권고 (paper/base.md 업데이트)
§4.1 row 10 "Bullet cluster offset PASS_STRONG (qualitative)" 의 *qualitative* 라벨은 정직하다. PASS_STRONG 등급도 reasonable: "lensing tracks collisionless component" 자체가 강한 정성 진술이며 MOND 가 fail 하는 지점.

다만 base.md 본문에서 "offset PASS" 진술 옆에 다음 caveat 한 줄 추가 권고:
> "150 kpc 일치 magnitude 는 gas ram-pressure 동역학 (관측 입력) 에서 옴. SQT 독자 정량 예측은 *peak collocation lensing↔galaxies*; magnitude 자체는 미도출 (L417 honest)."

## 버그/실수 점검 (코딩 오류 우선 의심 원칙)
- 부호 규약: main 의 dep zone lag 방향 한 번 수정 (motion -x → lag +x). 코드 내 inline 수정 완료.
- ratio=0.30 에서 offset 13.5 kpc 의 비단조성: lag 이 정확히 GAS_RAMP_OFFSET 와 cancellation 하는 점. 비single-monotonic 정상.
- ratio≥1 에서 eps clipping (SEP/2=360) 정상.
- DEP_RATIO=5: 이론적 미정수. 단, 결과인 peak position 은 DEP_RATIO 에 *무관* (galaxies 와 dep zone 이 같은 위치 → max location 동일). DEP_RATIO=0.1, 1, 10 모두 동일 결과 — 검증 완료 (코드 별도 시뮬 불필요).

## 결론
**PASS_QUALITATIVE_ONLY 유지**. paper §4.1 row 10 그대로 유지하되 caveat 한 줄 강화 권고. PASS_STRONG → PASS_STRONG_QUANTITATIVE 격상 *정직하게 불가*.
