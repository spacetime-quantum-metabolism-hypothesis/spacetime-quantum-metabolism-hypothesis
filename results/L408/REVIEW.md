# L408 REVIEW — V(n,t) gate 닫기 결정

4인팀 자율분담 코드리뷰 + 시뮬레이션 결과 정직 보고.

## 1. 시뮬 실행 요약

- 스크립트: simulations/L408/run.py
- 데이터: DESI DR2 13-point (CobayaSampler bao_data 미러: simulations/desi_data.py) + 13×13 full COV_INV
- 적분: scipy.integrate.cumulative_trapezoid, N_GRID=4000, z up to z_eff.max()+0.01 (CLAUDE.md L33 재발방지 준수)
- LCDM baseline: chi2=10.187, AICc=15.387 (Om=0.297, H0=69.08)
- 사전 선언된 V(n,t) candidate 2개 — pre-declared, *L33 스캔에서 차용 안 함*.

## 2. 결과 (results.json)

| Cand | chi2 | k(honest) | AICc | dAICc | w0 | wa | G2 box | G3 dAICc<-4 | Verdict |
|------|------|-----------|------|-------|-----|-----|--------|-------------|---------|
| LCDM | 10.187 | 2 | 15.387 | -- | (-1) | (0) | -- | -- | -- |
| C1 slow-roll | 7.515 | 5 | 26.086 | +10.699 | -1.181 | +1.042 | N (둘 다 박스 외) | N | FAIL |
| C2 thawing | 7.981 | 4 | 20.981 | +5.594  | -1.279 | +0.588 | N (둘 다 박스 외) | N | FAIL |

## 3. Gate 평가

| Gate | 조건 | 결과 |
|------|------|------|
| G1 axiom-derived V(n,t) | 공리 → 유일 functional form | **미충족** (NEXT_STEP 단계 (i) 미수행) |
| G2 DESI box 동시 충족 | w0 ∈ [-0.815, -0.699] AND wa ∈ [-1.04, -0.59] | **미충족** (두 후보 모두 wa>0, 부호조차 반대) |
| G3 honest dAICc < -4 (k=4~5) | k 패널티 정직 반영 시 LCDM 우위 | **미충족** (dAICc = +5.6, +10.7로 LCDM이 더 우수) |
| G4 thawing 매칭 one-to-one | 매칭 유일성 | **미충족** (NEXT_STEP 단계 (iii) 미수행) |

→ 4 gate 중 **0/4 PASS**.

## 4. 정직 결론

- L33 스캔에서 ratio_m1 / cpl_blend / cpl_mix 류가 ΔAICc ≈ -4.6 까지 도달했으나, 이는 **k=2 로 가정한 결과**. V(n,t) 의 functional shape 자유도 (template-meta) 를 정직 반영(k≥4)하면 LCDM 보다 나쁨.
- L408 의 두 motivated 후보(slow-roll analogue, thawing match) 는 fit 자체는 LCDM 보다 chi2 작음(7.5, 8.0 < 10.2)이지만 (i) 부호 반대 wa>0 — DESI 박스 절대 도달 불가, (ii) AICc 페널티 흡수 못 함.

## 5. 권고

- **gate 닫기 가능**: YES. G1·G2·G3·G4 모두 미충족.
- **Tier B (V(n,t)-extension) 사전등록**: **영구 보류** 권고.
- **Tier A (w_a=0 base + sigma8 calibration)**: 사전등록 진행 — Tier B 와 분리 보존(ATTACK Attack-7 회피).
- 미래에 Tier B 부활 조건: NEXT_STEP 단계 (i) 가 axiom 으로부터 V(n,t) 의 단일 functional class 를 도출하고, 그 class 가 *자동으로* (w0, wa) DESI 박스에 들어가는 경우만. 현 시점에 그러한 도출 부재 → vacuous.

## 6. 4인 코드리뷰 자율분담 점검표

- (a) DESI DR2 13pt + COV_INV: simulations/desi_data.py 사용. OK.
- (b) cumulative_trapezoid + N_GRID=4000 + z_grid up to z_eff.max()+0.01: OK (L33 재발방지 준수).
- (c) AICc k=k_total 정직 카운팅: OK (C1: k=5, C2: k=4 — Om, H0, amp + shape).
- (d) (w0,wa) extraction z∈[0.01, 1.2] lstsq: OK (E²↔CPL E² 직접, rho_de 음수 가드 포함).

## 7. 메모 (재발방지)

- L408 추가 재발방지: V(n,t) 류 확장은 *항상 honest k* 로 보고. L33 스캔의 k=2 AICc 를 V(n,t) 사전등록 근거로 인용 금지.
- DESI (w0, wa) 박스는 DESI+CMB+SN-all 결합 결과 (arXiv:2503.14738). BAO-only 만으로 박스 도달 주장 금지.
- Pre-declared candidate 가 fail 했을 때, post-hoc 으로 더 잘 맞는 form 을 찾아 "대체 후보" 로 올리는 행위 금지(template-zoo over-fitting).
