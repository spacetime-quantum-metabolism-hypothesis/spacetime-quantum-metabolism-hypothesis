# L583 — Q17 Path 3 R3+R4 Protocol 사전등록 (방향 only)

상태: pre-registration (도출 0건, 파라미터 0개, 수식 0줄).
근거: L578 `Q17_PATH3_RULE_A.md` 의 통과 조건 = R3 + R4 protocol 통과.
정합: CLAUDE.md [최우선-1] 절대 준수 — 방향만, 지도 금지.

---

## §1. R3 protocol — z-의존 동역학 도출 분리 (방향)

**비판 핵심 (L513 §6.5(e))**: amplitude 비례성만으로는 단순 normalization 귀결과
구분되지 않는다. 진정한 g(z) 의 z-의존 동역학이 도출되어야 한다.

**회피 방향 (수식 0)**:

1. **Blind derivation 절차** — 도출 측과 검증 측 분리.
   - 도출 측: g(z) 의 함수형태를 SQT 1차원리에서 유도. 결과 봉인 (sealed).
   - 검증 측: 봉인 상태에서 관측 데이터에 amplitude-only normalization 적합.
   - 봉인 해제 후 z-shape 비교. shape 일치 = z-의존 동역학 실재.
   - shape 일치 안 함 = normalization artefact 가능성, R3 미통과.

2. **Cross-z prediction 절차** — 단일점 fit vs 다점 동시 예측.
   - 두 개 이상의 redshift bin 에서 *동일 파라미터* 로 예측 산출.
   - 단순 amplitude normalization 이면 1 점만 fit, 나머지 점 무작위.
   - 진짜 동역학이면 모든 점이 동일 파라미터 하에서 정합.
   - 척도: 1점 fit vs 다점 fit 의 잔차 비.

3. **Null model 비교** — z-의존성 *제거* 한 flat 모델 (g(z)=상수) 와의 evidence 비교.
   - 데이터가 z-의존성을 요구하는지 정량화 (Bayesian).
   - flat null 이 더 선호되면 R3 자동 미통과.

4. **외부 데이터 격리** — 도출에 사용된 데이터 vs 검증 데이터 분리.
   - 도출 anchor 가 z=0 데이터면 z>0 검증으로 cross-validate.
   - 동일 데이터 재사용 시 R3 무효.

R3 통과 = (1)+(2)+(3) 모두 만족 + (4) 데이터 격리.

---

## §2. R4 protocol — anchor-free H₀ 도출 (방향)

**비판 핵심 (L552)**: anchor circularity. SQT 의 a5 (또는 등가 파라미터) 가
관측 H₀ (SH0ES, Λ_obs) 로부터 역산되면 H₀ 예측은 자기참조.

**회피 방향 (수식 0)**:

1. **Anchor-free 도출 시도** — H₀ 자체를 SQT 내부 무차원 조합으로 환원.
   - 입력 anchor: 플랑크 단위 또는 microphysics 상수만 허용.
   - 우주론 관측값 (SH0ES, Planck Λ) 일체 미사용.
   - 출력: H₀ 예측 + 불확실성. 관측과 사후 비교.

2. **Anchor independence 증명** — H₀ 를 input 으로 명시 인정한 경우.
   - 서로 다른 anchor 후보 (SH0ES / Planck-Λ / TRGB / megamaser) 각각으로 a5 도출.
   - cross-product 예측 (예: w_a, growth shape) 이 anchor 선택과 무관해야 함.
   - anchor-dependent → R4 미통과 (L552 비판 그대로 적용).

3. **k_IR anchor 회피** — L552 가 지적한 "anchor 가 Λ_obs → k_IR 로 옮겨감" 패턴 차단.
   - k_IR (또는 등가 IR 스케일) 가 Λ_obs 로부터 fitting 되면 동일 circularity.
   - k_IR 도 anchor-free 도출 또는 microphysics 입력에서 fix.

4. **Falsifiable prediction surface** — anchor 선택 외부에서 검증 가능한 예측 명시.
   - cross-product 가 anchor 와 *수학적으로* 독립함을 사전 증명.
   - 수식 0 원칙 → 구조적 독립성 argument 만 등록 (도출은 별 세션).

R4 통과 = (1) 또는 ((2)+(3)+(4)) 만족.

---

## §3. L562 4 protocol 와의 통합

L562 4 protocol = (a) 유일성, (b) postdiction-free, (c) 외부 격리, (d) falsifier.

| L562 | R3 (z-동역학) | R4 (anchor-free) | 중복 |
|------|---------------|-------------------|------|
| (a) 유일성 | g(z) 함수형태가 SQT 에서 유일 도출인가 | H₀ 도출이 유일한가 | 부분 중복 |
| (b) postdiction-free | blind derivation 으로 보장 | anchor-free 로 보장 | 강한 중복 |
| (c) 외부 격리 | 도출/검증 데이터 분리 | 도출에 우주론 관측 미사용 | 강한 중복 |
| (d) falsifier | cross-z prediction | anchor-independent prediction | 부분 중복 |

**통합 protocol 가능**: R3+R4 는 L562 4 protocol 의 *우주론 채널 특화 버전*.
공통 골격 = blind + cross-validate + null compare + falsifier.

통합 후 단일 protocol 명: **"BCNF protocol"** (Blind, Cross-validate, Null-compare, Falsifier) — 명명만, 구조는 미정.

L562 의 일반 4 protocol 는 모든 SQT 예측에 적용. R3+R4 는 Q17 Path 3 (DESI w_a) 채널 특화. 별도 운용하되 핵심 원칙은 공유.

---

## §4. Falsifier 등록 (3건)

R3+R4 통과를 가정한 Q17 Path 3 의 사전등록 falsifier:

1. **DESI DR3 w_a 측정** — Q17 Path 3 가 예측하는 amplitude 와 부호.
   - DR3 posterior 가 예측 outside → Q17 Path 3 falsified.
   - 통과 임계: 사전등록된 amplitude 범위 내 (구체값 별 세션).

2. **Cross-z growth (RSD) shape** — R3 의 z-의존 g(z) 가 RSD fσ8(z) shape 에 남기는 흔적.
   - DESI / Euclid / LSST RSD 측정으로 z-shape 직접 시험.
   - shape 일치 안 함 → R3 사후 위반, Q17 Path 3 falsified.

3. **Independent H₀ measurement** — R4 의 anchor independence 가 보장하는 cross-anchor 일관성.
   - JWST TRGB, gravitational-wave standard siren, megamaser H₀ 신규 측정.
   - SQT a5 가 anchor 별로 다른 값 산출 → R4 사후 위반, Q17 Path 3 falsified.

각 falsifier 는 *사전등록* 시점에서 통과 범위 fix 후 봉인. 사후 조정 금지.

---

## §5. R3+R4 미통과 시 fallback (Path 4 Wetterich)

**Path 4 = Wetterich-class growing-neutrino 또는 fluid IDE.**

R3+R4 미통과 시 Path 3 자동 박탈은 L578 합의. Path 4 안전성 검토:

1. **Wetterich 자체의 R3+R4 부담**: Wetterich 도 amplitude artefact 위험 + ν-mass anchor circularity 가능. R3+R4 protocol 동일 적용해야 함.

2. **L583 fallback 운용 원칙**:
   - Path 4 fallback 시 *동일* R3+R4 (또는 BCNF) protocol 통과 의무.
   - "Path 3 가 망했으니 Path 4 는 약식 통과" 금지.
   - Path 4 가 R3+R4 못 넘기면 Q17 자체 dead, SQT 재구조화.

3. **CLAUDE.md L4 재발방지 정합**: "L4 RVM family 전원 wrong-sign" 사례처럼 fallback 도 사전 부호/구조 검증 필수. blind acceptance 금지.

4. **Path 5 ghost option**: Path 3, Path 4 모두 미통과 시 — Q17 자체를 Path 1/2 (배경+성장 channel) 로 후퇴. amplitude-locking 주장 자체 폐기.

---

## §6. 정직 한 줄

L583 은 R3+R4 protocol 의 *방향* 만 등록한다 — Q17 Path 3 가 단순 normalization
artefact 가 아닌 진짜 동역학임을 검증하기 위한 blind / cross-z / anchor-independent
구조의 사전 약속이며, 도출과 수치는 단 하나도 포함하지 않는다.
