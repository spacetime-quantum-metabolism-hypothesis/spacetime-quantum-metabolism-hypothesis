# L526 R3 — w_0 w_a CDM Reinterpretation under Son+2025 Age-Bias Correction

**Statistician position. One honest line: Son+25 보정을 적용하면 z=0 우주는 *감속* 중이며, SQT 의 w_a<0 예측은 "DESI 의 phantom-like dark energy 약화" 가 아니라 "암흑에너지가 이미 사라지는 중" 이라는 정반대 의미가 된다.**

---

## 1. Son+2025 보정 후 w_0 / w_a 값 (논문 추출)

저장소 내 사용된 Son et al. 2025 (MNRAS 544:975) 인용 값 — `simulations/l43/l43_test.py` L73–L84, L43 run.log:

| Parameter | Value | 2σ width (used) |
|---|---|---|
| w_0  | **−0.34** | ±0.12 |
| w_a  | **−1.90** | ±0.50 |
| q_0  | **+0.18** | (deceleration) |

근거: Son+25 는 SN Ia progenitor age-bias 를 5.5σ 로 확정. 보정 후 LCDM 은 약 9σ 로 배제되고, CPL 적합값이 (w_0, w_a, q_0) ≈ (−0.34, −1.90, +0.18) 으로 이동 (L43 결과 요약, l43_test.py L5–L10).

비교점:
- DESI DR2 공식 (DR2+Planck+DES-all): w_0 = −0.757 ± 0.058, w_a = −0.83(+0.24/−0.21).
- LCDM: w_0 = −1, w_a = 0, q_0 ≈ −0.53 (가속).

→ **Son+25 보정은 w_0 를 −0.34 쪽으로 약 7σ 끌어당기고, w_a 를 더욱 음수쪽 (−1.9) 으로 끌어당긴다.**

---

## 2. "감속" 의 정확한 수학적 조건

감속 파라미터 (deceleration parameter):

    q_0 ≡ −(ä/a)/(H²) |_{t=t0}

평탄 FRW + matter + dark-energy fluid w(z) 에서

    q_0 = ½ Ω_m,0 + ½ (1 + 3 w_0) Ω_DE,0
        = ½ + (3/2) w_0 Ω_DE,0     (Ω_m + Ω_DE = 1)

따라서 *감속* (q_0 > 0) 의 정확한 조건은:

    **w_0 > −1 / (3 Ω_DE,0)**

Ω_DE,0 ≈ 0.685 (Planck) 대입 시 임계값 w_0,crit ≈ −0.487. Son+25 의 w_0 = −0.34 는 이 임계를 명백히 *위반하지 않음* (즉 q_0 > 0). 직접 계산:

    q_0 = 0.5 + 1.5·(−0.34)·0.685 ≈ **+0.151**

Son+25 가 보고한 q_0 = +0.18 과 일치 (보정/모델 선택 차이 내 ~0.03).

핵심: 가속/감속 경계 w_0 = −0.487 은 LCDM (−1) 과 Son+25 (−0.34) 사이에 위치. **Son+25 는 이 경계를 *감속 쪽으로* 넘어버린 우주**.

---

## 3. SQT 의 w_a < 0 예측 — *감속 시나리오* 에서의 해석 변화

기존 (DESI 만 본) SQT 내러티브:
- w_0 ≈ −1, w_a < 0 → "암흑에너지가 점점 phantom 에서 quintessence 로 약화" (thawing/freezing).
- 공리적 동기: 시공간 대사 (metabolism) 의 σ-소멸이 후기에 DE 를 점진 약화시킴.

Son+25 보정 시 w_a < 0 의 의미가 *질적으로* 바뀐다:

(a) **w_0 가 이미 −0.487 의 가/감속 경계를 넘어 감속쪽**. w_a < 0 은 z>0 (과거) 에서 w(z) = w_0 + w_a·z/(1+z) 가 −1 또는 그 이하로 가는 thawing-from-phantom-past 형태.

(b) z = 0 미래 외삽 (z<0, a>1):  w_a<0, z→−1 에서 w → w_0 − w_a → +1.56  (Son+25 중심값).
   → "암흑에너지가 stiff fluid 를 거쳐 *ρ_DE→0 으로 빠르게 소멸*" 시나리오.

(c) **SQT 의 w_a < 0 은 이제 "감속 우주에서 DE 의 빠른 사망 (rapid extinction)" 으로 해석되어야 한다.** "phantom 약화" 가 아니라 "이미 약화 완료, 사망 진행 중".

(d) σ-소멸 공리와의 정합성: 이 해석은 오히려 SQT 가 원래 주장했던 "metabolic decay of vacuum" 과 *더* 부합. 즉 Son+25 보정은 SQT 의 w_a<0 자체는 보존하지만 *시점* 을 z≈0 으로 당긴다.

주의 (코드 검증):
- L43 a priori 테스트에서 SQT psi^n core (D_psi2, n=2) 가 Son+25 표적에 맞춘 표본에서 dAICc=+1012.95 로 K90 KILL.
- 즉 "w_a<0 부호" 는 일치하지만 *진폭/모양* 은 Son+25 CPL 와 직접 매치 못 함. 해석 정합성과 fit 정합성을 혼동 금지.

---

## 4. DESI w_0 = −0.757 의 재해석 (Son+25 후)

DESI DR2 의 w_0 = −0.757 ± 0.058 와 Son+25 의 w_0 = −0.34 ± 0.06 (2σ/2 ≈ 0.06) 사이 거리:

    Δw_0 = 0.417,   σ_combined ≈ √(0.058² + 0.06²) ≈ 0.083
    → **약 5.0σ 불일치**.

가능한 재해석 3가지 (통계 입장):

(R1) **SN-driven shift**: DESI 결합값은 Pantheon+/DES-SN5YR 의 age-bias 미보정 SN 거리에 의해 w_0 가 인공적으로 phantom-쪽 (−1 근방) 으로 끌려갔다는 해석. Son+25 보정을 SN likelihood 에 직접 주입하면 결합 w_0 가 −0.34 쪽으로 이동할 것 (L34 joint 재실행 필요).

(R2) **BAO-only vs joint 분리**: DESI BAO-only 는 w_0 에 대한 약한 제약. w_0 = −0.757 은 SN+CMB 결합에서 나온 값. Son+25 가 SN 만 보정한다면 BAO-only 부분은 변동 미미, 결합 결과만 밀린다 → DESI 의 w_0 = −0.757 은 *artifact of SN systematic* 이라는 강한 주장 가능.

(R3) **두 가설 모두 부분적으로 맞다**: 진짜 w_0 ∈ [−0.76, −0.34] 사이 어딘가, σ 통합. 이 경우 q_0 부호는 −0.487 임계에서 결정되며, Son+25 가 옳으면 우주는 *방금 막* 감속 상태에 진입했거나 (q_0 ≈ +0.18) 가/감속 경계 근처 (q_0 ≈ 0).

**통계적으로 가장 honest 한 발언**: Son+25 와 DESI 는 w_0 에서 약 5σ 충돌. 두 결과를 동시에 인정하면 LCDM 만 부정되는 것이 아니라 *현재의 표준 SN 거리 기록 자체* 가 부정된다. SQT 가 이 둘을 "동시 설명" 한다고 주장하려면 SN systematic 의 미시 모델 (progenitor 분포의 redshift evolution) 까지 SQT 에서 도출해야 함 — 현재 SQT 는 그 단계 아님.

---

## 5. 한 줄 정직한 결론

**Son+25 가 옳다면 우리는 *이미 감속하는* 우주에 있고, SQT 의 w_a<0 은 "암흑에너지의 빠른 사망" 으로 재명명되어야 하며, DESI 의 w_0=−0.757 은 SN age-bias 미보정 systematic 으로 5σ 의심된다 — 하지만 L43 a priori 테스트에서 SQT psi^n core 가 K90 KILL 이었다는 사실은 해석 일관성과 별개로 그대로 남는다.**
