# L408 NEXT STEP — 8인팀 자율 분담 설계

CLAUDE.md 최우선-1/2 준수: 수식, 파라미터 값, 유도 경로 힌트 일절 금지.
방향(direction)과 분야명(field name)만 제시. 8인 팀이 독립 도출.

---

## 단계 (i) V(n,t) functional form 의 *axiom-derived* 도출 시도

### 방향
- L0/L1/L2 SQMH 공리 — 특히 시공간 양자 대사 항 — 에서 출발해 V 가 (n,t) 두 변수에 의존해야만 하는 *필요성* 을 먼저 도출. 없는 경우 V(n) 단변수로 후퇴.
- Noether 시간평행성 위반의 발생 메커니즘이 공리 내부에서 강제되는지 검토. 위반이 강제되지 않으면 V(n,t) 는 ad-hoc.

### 8인 자율 분담 (역할 사전 지정 없음, 토의에서 발생)
- 8명이 각자 독립적으로 axiom→V 도출 시도. 결과가 *서로 다른 functional class* 로 갈라지면 over-determined → 가설 자체 약화. *동일 class* 로 수렴하면 G1 충족 가능성.

### KILL 조건
- 8명 중 4명 이상이 V 도출 실패 → G1 영구 미충족 → Tier B 사전등록 *영구 보류*.

---

## 단계 (ii) slow-roll inflation analogue 매칭

### 방향
- inflation 에서 slow-roll 파라미터 (ε, η) 가 V(φ) 와 V'(φ) 의 비율로 정의되는 구조를, late-time DE 에 대응시킬 때 V(n,t) 의 (n, t) 가 어떤 inflation 변수에 mapping 되는지 *후보 매핑* 만 열거.
- mapping 이 *one-to-one* 인지, *one-to-many* 인지 확인. one-to-many 면 underdetermined → 매칭 불가 결론.

### 산출물
- 매핑 표 (수식 없이 변수명 대응만): "(n,t)" ↔ "(φ, N_e-fold)" / "(φ, H_inflation)" 등.
- 8인이 동일 매핑에 수렴하는지 voting.

---

## 단계 (iii) thawing quintessence template 매칭

### 방향
- thawing quintessence (Caldwell-Linder 2005 분류) 의 freezing-late, thawing-late 두 attractor 중 SQMH 가 어느 쪽에 *공리상* 강제되는지 결정.
- thawing 이 강제되면, 매칭은 V(φ) ∝ φ^a 또는 V(φ) ∝ exp 류 중 하나로 좁혀짐. SQMH 공리가 a 또는 exp 지수를 결정해야 G4 충족.

### KILL 조건
- 공리가 thawing/freezing 을 결정하지 못하면 매칭은 phenomenological → G4 영구 미충족.

---

## 단계 (iv) Python 시뮬: V(n,t) form scan vs DESI DR2

### 방향
- (i)-(iii) 에서 살아남은 functional class 만 toy fit. 살아남은 class 가 0 이면 시뮬레이션 자체 불요.
- L408 run.py 가 이미 두 motivated class (slow-roll analogue, thawing CPL match) 를 honest k=4~5 AICc 로 평가. 결과는 정직 보고.

### 4인 코드리뷰 (역할 사전 지정 없음)
- L408 run.py 에 대해 4명이 자율 분담:
  (a) DESI DR2 13pt + COV_INV 사용 검증
  (b) cumulative_trapezoid + N_GRID=4000 검증
  (c) AICc k=k_total 정직 카운팅 검증
  (d) (w0, wa) extraction 의 z-range 와 lstsq 안정성 검증

---

## 사전등록 (pre-registration) 권고

- **Tier A** (w_a=0 base, sigma8 calibration): **사전등록 진행** — 이미 23행 표 #12 가 가능 명시.
- **Tier B** (V(n,t)-extension): G1+G2+G3+G4 *동시* 충족 시에만 가능. L408 시뮬결과 기준 G2/G3 즉시 미충족 → **영구 보류** 권고.
- Tier B 가 미래에 부활할 단 하나의 경로: 단계 (i) 가 axiom-derived 단일 functional class 를 도출, 그 class 가 자동으로 G2 box 에 들어가는 경우. 이는 L408 시점에서 vacuous (해당 class 미존재).
