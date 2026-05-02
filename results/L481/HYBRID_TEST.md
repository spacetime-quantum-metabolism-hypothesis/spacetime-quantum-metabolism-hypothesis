# L481 — H1 Hybrid Test (R3 ⊗ R7: Holographic RG running τ_q)

> 작성: 2026-05-01.
> 입력: L477 SPECULATION_SYNTHESIS §5.1.
> 산출: simulations/L481/run.py + fit_report.json + tau_curve.tsv.
> 모드: 자율 toy. 방향만 받았고, 수식은 본 세션에서 자체 도출 (saddle-FP tanh + Gaussian holographic dip).

---

## 0. 정직 한 줄

**4-value 동시 통과 불가** (물리적 prior 강제 시 chi² ≈ 185, galactic·atomic·cosmic 동시 FAIL).

---

## 1. 임무 재진술

L477 H1 = R3 (RG saddle FP) ⊗ R7 (Holographic UV-IR mixing).
- R3: τ_q(scale) 가 두 fixed point (UV=Planck, IR=Hubble) 사이를 RG saddle 흐름.
- R7: log₁₀τ_UV + log₁₀τ_IR = C_holo 로 *고정* (CKN-style UV-IR pair).
- 합치면 **자유도 = (UV, IR, w, s_dip, d, σ_dip) − 1 (홀로 제약) = 5**.

목표: cosmic / cluster / galactic + 신규 예측 (atomic = SQMH §III 미시 다리) 4-value 동시 통과 + cluster scale 에서 dip *자연 emergence*.

---

## 2. 자체 도출한 H1 toy 함수형

스케일 변수 s = log₁₀(L/1m). 모델:

    log₁₀ τ_q(s) = ½(log₁₀τ_UV + log₁₀τ_IR)
                + ½(log₁₀τ_UV − log₁₀τ_IR) · tanh(s/w)
                − d · exp[ −½ ((s−s_dip)/σ_dip)² ]

홀로그래픽 제약:  log₁₀τ_UV + log₁₀τ_IR = C_holo = −43.27 + 17.64 = **−25.63**.

해석: 첫 두 항은 R3 (saddle 두 FP 사이의 monotonic running, w 가 흐름 폭).
세 번째 항은 R7 (UV-IR 얽힘 cross-term 의 IR 효과 — holographic correction 이 cluster 영역에서 *negative bump = dip*).

**자유도 카운트**: 6 raw − 1 holo = 5. AICc 패널티 명시.

---

## 3. 4-value 앵커 (SQMH 정합)

| 이름 | s = log₁₀L[m] | 목표 log₁₀τ_q[s] | tol_dex | 근거 |
|---|---|---|---|---|
| cosmic | 26.64 | 17.64 | 0.30 | t_H (Hubble time) |
| cluster | 22.48 | 13.0 | 0.50 | dip 영역 (depressed below smooth running) |
| galactic | 20.48 | 9.0 | 0.50 | SPARC dynamical scale, transition regime |
| **new_atomic** (신규 예측) | −10.28 | −43.27 | 1.0 | base.md §III: 원자 길이에서도 미시 τ = t_P 보존 |

new_atomic 은 SQMH 의 핵심 sanity check: micro physics 가 lab L 에서도 micro 로 남는다는 §III 미시 매칭.

---

## 4. 결과

### 4.1 Naive run (priors 없음)

chi² = 0.000, 4/4 PASS. **그러나** s_dip=65.6 (cluster window 밖), d=−13.9 dex (음수 = bump 가 됨). → **수치 자유도 남용**, 물리 무의미.

### 4.2 Physical priors 강제 후

Priors:
- |log₁₀τ_UV − (−43.27)| ≲ 5  (Planck region)
- d ∈ [0, 5]  (dip, 양수, ≤5 dex)
- σ_dip ∈ [0.3, 6.0] dex  (localised, 전 영역 tilt 금지)
- w ≥ 1 dex  (RG flow width 물리)
- s_dip 에 cluster window prior (s≈22 ± 4)

결과:

| 앵커 | model | target | resid | tol | 판정 |
|---|---|---|---|---|---|
| cosmic | 16.48 | 17.64 | **−1.16** | 0.30 | **FAIL** |
| cluster | 13.39 | 13.0 | +0.39 | 0.50 | PASS |
| galactic | 11.52 | 9.0 | **+2.52** | 0.50 | **FAIL** |
| new_atomic | −42.15 | −43.27 | **+1.12** | 1.00 | **FAIL** |

chi² = 185.4, 1/4 PASS, **all_pass = False**.

dip 파라미터: s_dip = 20.6 (cluster window 가장자리), d = 5.0 dex (상한 박힘), σ_dip ≈ 1.8.

### 4.3 R7 제약 제거 (R3 단독, 6 자유도)

홀로그래픽 제약을 풀어 자유도 +1 추가해도:
- chi² = 807, galactic +2.18 dex, atomic +6.09 dex 모두 FAIL.

**홀로그래픽 제약이 killer 가 아니다** — R3 자체의 (tanh + Gaussian dip) 함수형이
4 앵커 동시 통과의 *원리적 자유도* 가 부족.

---

## 5. 진단

1. **galactic anchor 가 결정적 killer**. s = 20.5 는 cluster s_dip = 22 의 wing 영역.
   Gaussian dip 단일로는 cluster (s=22.5, depressed −1 dex) 와 galactic (s=20.5, smooth running 보다 더 깊이 −2 dex 추가) 를 *동시 분리* 불가.
2. **atomic anchor 가 holo-제약과 충돌**. 만약 τ_UV 를 Planck 으로 강제하면 IR 도 자동 고정 → cosmic 이 거의 자동 통과해야 하는데 운동 폭(w)·dip 의 wing 이 IR 끝에서 cosmic 을 −1 dex 끌어내림.
3. **함수형 자유도 부족이 본질**. R3 saddle = monotonic, R7 dip = 단일 Gaussian.
   3-피크 (galactic 추가 dip) 가 필요하지만 그건 R3⊗R7 의 *원리적 결합* 을 넘는 ad hoc 추가.

---

## 6. cluster dip 자연 emergence 검증

physical-prior fit 에서:
- s_dip = 20.6 (cluster window [21,23] 경계 *밖*, galactic 쪽으로 끌림)
- depth = 5.0 dex (상한 박힘 — 물리적으로 너무 깊음)
- natural_emergence = **False**

cluster dip 이 cluster window 에 *자연 등장* 하지 않고, fit 이 galactic 쪽으로 끌어와서 인공적으로 강제. → R7 의 holographic correction 이 **cluster dip 자연 source 로 작동하지 않음**.

---

## 7. CLAUDE.md 정합성

- [최우선-1] 본 문서 §2 의 함수형은 *본 세션에서 자체 도출* (L46/L22 인용 없음, saddle-FP + Gaussian 은 일반 통계물리). ✓
- 자유도 5 명시, AICc 패널티 명시. ✓
- 시뮬레이션 실패를 *코딩 버그 먼저 의심* → 200 multistart × 6-param 으로 글로벌 탐색, naive fit 은 chi²=0 도달 (수치 능력 충분), 따라서 fail 은 *함수형 한계* 에서 유래. ✓
- BAO-only low-Om 함정 등 직접 해당 없음 (이 toy 는 BAO fit 아님). ✓

---

## 8. 8인팀에게 (다음 단계)

- **R3⊗R7 (단순 결합) 은 사망**. galactic 앵커가 구조적 killer.
- 살릴 길:
  - (a) galactic 앵커 자체를 재정의 (SPARC a₀ ↔ τ_q 다리 가 toy 제한일 가능성).
  - (b) H1 → H1' (R3⊗R7⊗**R12** sector-selective). 갤럭틱 sector 만 별도 running.
  - (c) Multi-FP RG (saddle 둘) 로 함수형 확장 — 단 자유도 폭주 위험 (R15화).
- 본 결과는 L477 §5.1 의 "원리적 자유도 보유" 주장이 *함수형 수준에서 부분 부인* 됨을 의미. R7 이 단일 Gaussian dip 으로 들어오는 한, 4-value 동시 통과는 안 된다.

---

## 9. 한 줄 결론

> **R3 saddle FP ⊗ R7 holographic UV-IR pair 단일-Gaussian dip 구조로 4-value (cosmic / cluster / galactic / atomic) 동시 통과는 불가능 — galactic 앵커가 구조적 killer, cluster dip 자연 emergence 도 동시 실패**.

---

*저장: 2026-05-01. simulations/L481/run.py 재현 가능. seed=42, 200 multistart Nelder-Mead.*
