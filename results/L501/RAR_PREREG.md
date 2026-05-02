# L501 — RAR PASS_STRONG 격상 Pre-Registration (DRAFT v0)

> **작성**: 2026-05-01
> **상태**: DRAFT v0 — 8인 라운드 / 4인 코드리뷰 *전* 단계 사전 등록 문서.
> **목적**: L482 RAR (a₀ ≈ c·H₀/(2π) 일치) 의 *글로벌 고점* 격상 (PASS_MODERATE → PASS_STRONG) 자격 심사를 *분석 전* 에 등록한다. 본 문서가 등록되기 *이전* 의 어떤 fit 결과도 격상 근거로 인용 불가.
> **소스 통합**:
> - L497 INVARIANTS.md — PASS_STRONG → PASS_MODERATE 격하 권고 (functional-form / Υ★ / anchor / cuts / H₀ 5축 비-invariance)
> - L495 HIDDEN_DOF_AUDIT.md — "0 free parameter" 광고 false, 보수 9 ~ 확장 13 hidden DOF
> - L492 RAR_DATASET_AUDIT.md — cross-dataset PASS 1/4, dwarf D4 에서 0.353 dex 편차
>
> **CLAUDE.md 정합성**: 본 pre-reg 는 *방향과 등록 항목 카탈로그* 만 — 신규 수식 0줄, 신규 파라미터 도입 0개. 후속 8인팀이 자율 분담으로 fit 수행. ([최우선-1], [최우선-2] 준수.)

---

## 0. 정직 한 줄

**L482 단일 dataset (SPARC 175, M16, Υ canonical, Planck H₀) 한정 a₀ 일치는 격상 근거로 불충분하다 — 글로벌 고점 PASS_STRONG 을 주장하려면 (i) 5+ 사전 등록 함수형 모두에서 a₀ ≤ factor-1.5 invariant, (ii) Υ★ choice prior 를 사후 선택 없이 명시, (iii) 4 개 anchor (SPARC 175 / Q=1 / dwarf / bright) 에서 동시 보고, (iv) hidden DOF 3개 (함수형 + Υ★ + anchor pick) 명시 패널티 후 ΔAICc, 4 sub-criteria 가 *동시* 통과해야 한다.**

---

## 1. 사전 등록 함수형 (≥5 종) — *fit 수행 전 lock*

본 등록 이후 어떤 함수형 추가/제거/대체도 *post-hoc* 분류되어 격상 무효.

| ID | 함수형 이름 | 출처 | 자유 파라미터 (hidden DOF 카운트) |
|----|-----------|------|---------------------------------|
| F1 | M16 (McGaugh-Lelli-Schombert 2016) | McGaugh+16 ApJL 836 L20 | a₀ (free) |
| F2 | simple-ν | Famaey-McGaugh 2012 LRR 15 10 | a₀ (free) |
| F3 | standard-μ (Bekenstein 1984 분모형) | Bekenstein-Milgrom 1984 ApJ 286 7 | a₀ (free) |
| F4 | exponential interpolation | Famaey-Binney 2005 MNRAS 363 603 | a₀ (free) |
| F5 | Bekenstein 2004 | Bekenstein 2004 PRD 70 083509 (TeVeS μ) | a₀ (free) |

선택 사유:
- F1–F3 은 L497 §A2 audit 에서 a₀ spread 16% (0.064 dex) 발생을 실측한 세 함수형. 본 등록은 이를 *명시적으로 포함* 해 cross-form invariance 를 직접 검증.
- F4, F5 는 SPARC RAR fit 문헌 표준 4번째/5번째 함수형. 임의 선택이 아니라 Famaey-McGaugh 2012 LRR Table 1 에 등록된 carrier set.
- 5 종 lock 이후 함수형 *교체* 시 본 pre-reg 갱신 필요 (L502+ 신규 등록).

**기각 함수형**: power-law n free, polynomial expansion, neural-net carrier — 모두 자유 파라미터 ≥2 → hidden DOF 폭증, 본 pre-reg 범위 외.

---

## 2. Υ★ choice prior (사전 등록)

| 항목 | 값 | 출처 |
|------|---|------|
| Υ_disk canonical | 0.50 (M_⊙/L_⊙ at 3.6 μm) | SPARC convention (Lelli+16 §3) |
| Υ_bul canonical | 0.70 | SPARC convention |
| Υ_disk prior range | [0.30, 0.80] uniform (Bayesian marginalization 시) | Li+18 ApJ 854 L13 |
| Υ_bul prior range | [0.50, 0.90] uniform | Li+18 |
| **Galaxy-wise Υ marginalization** | **선택** — Li+18 hierarchical Bayes 방식 | L497 §7-3 권고 |

**lock 규칙**:
- 본 pre-reg 등록 시점 이후 Υ canonical 값 변경 금지.
- Bayesian marginalization 결과만 main fit 으로 채택; canonical-fixed 는 *비교 reference* 로만 보고.
- Υ★ 사후 조정 (예: a₀ 더 일치하는 Υ 선택) 명시 금지 — 본 절 위반 시 격상 무효.

---

## 3. Anchor / subset (4 개 동시 보고 의무)

| Anchor ID | 정의 | n_galaxies | 출처 |
|-----------|------|-----------|------|
| A1_SPARC175 | SPARC 175 전체 | 175 | L482 baseline (D1_full) |
| A2_Q1 | Q=1 high-quality | 99 | L492 D2 |
| A3_dwarf | V_flat ≤ 60 km/s **AND** T ≥ 8 (LITTLE THINGS proxy) | 17 | L492 D4 |
| A4_bright | V_flat ≥ 150 km/s | 54 | L492 D5 |

**보고 의무**:
- 4 anchor × 5 함수형 = **20 fit 결과 모두 동시 보고**. 일부만 보고 시 cherry-pick 으로 자동 격상 무효.
- A1 만 PASS 인 경우 ("L482 단일 dataset 한정") 격상 불가 — L492 에서 이미 PASS 1/4 확인.
- "subset 별 a₀ best-fit + σ + χ²/dof + Δlog vs SQT" 4 컬럼 표 의무.

---

## 4. ΔAICc 명시 패널티 (Hidden DOF 3개)

L495 hidden DOF audit 보수 카운트 9 중, RAR 채널이 *직접 흔드는* 3개를 본 격상 심사에 명시 적용:

| Hidden DOF | 설명 | k_extra |
|------------|------|---------|
| HD1 | 함수형 선택 (5 후보 중 1개 pick) | +1 |
| HD2 | Υ★ choice (canonical pick or Li+18 prior pick) | +1 |
| HD3 | Anchor / subset pick (4 후보 중 어느 것을 main 으로 보고할지) | +1 |
| **총 k_extra** | | **+3** |

**ΔAICc 계산 규칙**:
```
ΔAICc(SQT vs free-a₀) = AICc_SQT − AICc_free
AICc_free = χ²_min + 2·(k_data + 3) + correction
AICc_SQT  = χ²_SQT  + 2·(k_data + 0) + correction   (a₀ 는 prior c·H₀/(2π) 로 lock)
```

여기서 `+3` 패널티는 free-a₀ 모델의 hidden DOF (함수형 / Υ★ / anchor pick) 를 *명시 카운트* 하기 위해 추가. SQT-locked 측에는 이 3개가 *동일하게 적용* 되지만 — 함수형/Υ★/anchor 선택은 양쪽 모델 공통이므로 ΔAICc 계산에서는 *상쇄*. **단, 본 pre-reg 에서 패널티 명시는 "free-a₀ 측 ΔAICc 우위가 hidden DOF 자유도 덕인지 진정 fit quality 인지 분리" 검증 목적**.

→ 즉, **격상 자격 ΔAICc 임계값을 +2 → +5** 로 상향 (보수). |ΔAICc| ≥ 5 (substantial evidence, Burnham-Anderson 2002) 인 경우만 SQT-prior 우위 인정.

---

## 5. 진정 PASS_STRONG 조건 — 4 sub-criteria *동시* 통과

> **AND 조건**. 하나라도 실패 시 PASS_MODERATE 유지. 사후 임계값 완화 금지.

### S1. Cross-functional invariance (factor ≤ 1.5)

```
max_F (a₀_fit[F]) / min_F (a₀_fit[F]) ≤ 1.5
```

5 함수형 (F1–F5) 전체에서 best-fit a₀ 비율 ≤ 1.5. L497 §A2 에서 M16/simple-ν/standard-μ spread 16% (≈ 1.45 ratio) 가 경계 — 5종 확장 시 1.5 초과 가능성 실측.

### S2. Cross-anchor invariance (Δlog ≤ 0.10 dex)

```
max_A |log₁₀(a₀_fit[A] / a₀_SQT)| ≤ 0.10  (모든 4 anchor 에서)
```

L492 결과: A1=+0.011, A2=+0.077, A3=−0.353, A4=+0.081 → A3 (dwarf) 가 0.353 dex 로 *현재 FAIL*. 본 sub-criterion 통과를 위해서는 dwarf scale RAR 자체의 재분석 필요 (예: Iorio+17 LITTLE THINGS Υ 재추정).

### S3. SQT-locked χ²/dof ≤ 1.6 (모든 4 anchor)

```
χ²(a₀ = c·H₀/(2π) prior, F1–F5 평균) / dof ≤ 1.6  (모든 A1–A4)
```

L492 결과: A1=1.30, A2=1.01, A3=2.51, A4=0.86 → A3 FAIL.

### S4. ΔAICc-패널티 통과

```
ΔAICc(SQT − free) ≤ −5  (4 anchor × 5 functional 평균, hidden DOF +3 패널티 후)
```

L482 단일 cell (A1 × F1) ΔAICc = +0.70 (free-a₀ 측 미세 우위, 통계 동등). 5종 함수형 + 4 anchor = 20 cell 평균에서 −5 이하 도달은 *현재 데이터 수준에서 사실상 불가능* — 본 pre-reg 의 격상 임계값이 *의도적으로 보수적* 임을 명시.

---

## 6. 사전 결과 예측 (분석 전 정직 기록)

본 pre-reg 등록 시점에서 *예상 결과*:

| Sub-criterion | 예상 | 사유 |
|---------------|------|------|
| S1 (cross-form ≤ 1.5) | △ marginal PASS or FAIL | L497 3 함수형 spread 16% (≈1.45). F4/F5 추가 시 1.5 초과 가능성 |
| S2 (cross-anchor ≤ 0.10) | **FAIL** | L492 D4 (dwarf) 0.353 dex |
| S3 (χ²/dof ≤ 1.6) | **FAIL** | L492 D4 χ²/dof = 2.51 |
| S4 (ΔAICc ≤ −5) | **FAIL** | L482 단일 cell ΔAICc=+0.70, 격상 임계 −5 도달 구조적 어려움 |

→ **현재 데이터 + 5 함수형 등록만으로는 PASS_STRONG 격상 불가 예상**. 본 pre-reg 의 의도는 격상 *통과* 가 아니라 "어떤 dataset 확장 / 함수형 제한 / Υ Bayesian marginalization 이 들어와도 임계값을 사후 변경할 수 없도록 *지금 lock*" 하는 것.

격상 통과 시나리오:
1. dwarf RAR 데이터 갱신 (Iorio+17 / Read+17 / Oh+15 LITTLE THINGS Υ 재추정 → A3 Δlog 감소).
2. Bayesian Υ marginalization (Li+18 hierarchical) 으로 모든 anchor 내부 Υ 시스테매틱 흡수.
3. 함수형 후보를 "physically motivated" 하위 집합 (M16, simple-ν 만) 으로 *사전* 축소 — 단 이는 본 pre-reg 의 5종 lock 위반이므로 **L502 신규 pre-reg 필요**.

---

## 7. 격상 무효 사유 (자동 trigger)

다음 중 하나라도 발생 시 본 격상 심사 무효:

1. 5 함수형 중 일부만 보고 (cherry-pick).
2. Υ★ canonical 값 사후 변경.
3. 4 anchor 중 일부만 보고.
4. ΔAICc 임계값 −5 → −2 등 사후 완화.
5. hidden DOF 패널티 +3 → +1 등 사후 축소.
6. dataset 확장 후 임계값 *상향* (S2 0.10 → 0.05 등 — 격상 통과 강화) 도 금지: pre-reg 는 *상향/하향 모두* 사후 변경 금지.
7. 본 pre-reg 등록 *이전* 에 수행된 fit 결과를 격상 근거로 인용.

---

## 8. 등록 메타데이터

| 항목 | 값 |
|------|-----|
| Pre-reg 등록일 | 2026-05-01 |
| 데이터 freeze | SPARC 175 (Lelli+16 AJ 152 157), Q/Vflat catalog as of 2025-12 release |
| H₀ anchor lock | Planck 2018 H₀ = 67.4 km/s/Mpc → a₀_SQT = 1.0422 × 10⁻¹⁰ m/s² |
| 대안 H₀ (Riess H₀ = 73.0 → a₀_SQT = 1.1294 × 10⁻¹⁰) | *비교 reference 로만* 보고; main S1–S4 판정은 Planck anchor |
| σ_log floor | 0.13 dex (L482 baseline) |
| 코드 freeze | L482 simulations/ + L492 simulations/L492/run.py |
| 후속 라운드 | 8인 Rule-A (S1–S4 합의) → 4인 Rule-B (코드 검증) → fit 실행 |

---

## 9. 후속 라운드 권고

1. **8인 라운드 (Rule-A)** — *fit 실행 전*:
   - S1–S4 임계값 합의 (본 pre-reg 임계값을 채택할지, 더 보수/완화할지).
   - 5 함수형 final lock (F4/F5 대체 후보 검토 후 freeze).
   - hidden DOF +3 의 ΔAICc 적용 방식 합의 (대칭 상쇄 vs 비대칭 적용).
   - Bayesian Υ marginalization 강제 vs canonical-fixed 허용.
2. **4인 코드리뷰 (Rule-B)** — fit 실행 직전:
   - simulations/L501/run.py 구현 (5 functional × 4 anchor = 20 cell fit + Υ marginalization).
   - 단일 포인트 검증 (L482 baseline 과 A1×F1 cell 일치 확인).
   - SPARC 데이터 무결성, Q-cut 적용, V_obs filter 일관성.
3. **fit 실행** (Rule-A/B 통과 후):
   - 20 cell 결과 표 + 4 sub-criteria 판정 + 격상/유지 verdict.
   - 결과를 results/L501/RAR_GRADE.md 에 기록.
4. **paper 반영**:
   - PASS_STRONG 통과 시: §4.1 RAR row 갱신 + abstract drift 차단 (L495 §5).
   - PASS_MODERATE 유지 시: §4.1 row "L501 pre-reg 4 sub-criteria 중 X/4 통과, hidden DOF +3 패널티 후 격상 보류" 정직 기록.

---

## 10. CLAUDE.md 정합성 점검

- **결과 왜곡 금지**: 예상 결과 (S2/S3/S4 FAIL) 를 *분석 전* 정직 기록. ✓
- **[최우선-1] 방향만 제공, 지도 금지**: 본 문서 신규 수식 0줄, 신규 파라미터 도입 0개. 함수형 5종, Υ prior, anchor 4개 모두 *기존 문헌 등록* 항목. ✓
- **[최우선-2] 팀 독립**: 본 pre-reg 은 임계값 *후보* 만 제시. 8인팀이 자율 분담으로 final 임계값 / 가중치 / Bayesian vs fixed 결정. ✓
- **paper 직접 수정 금지**: 본 문서 권고만, edit 0건. ✓
- **시뮬레이션 병렬 실행 원칙**: simulations/L501/run.py 는 multiprocessing.Pool(9) 패턴 + OMP/MKL/OPENBLAS_NUM_THREADS=1 강제 (4인 라운드에서 검증). ✓
- **재발방지 (numpy 2.x)**: trapezoid 사용; print 유니코드 금지; matplotlib 라벨만 유니코드. ✓
- **재발방지 (BAO-only ↔ joint 혼동 금지)**: 본 pre-reg 는 RAR 전용. BAO/SN/CMB joint 결과는 본 격상 판정에 사용 금지. ✓

---

## 11. 한 줄 종합

**L501 pre-reg 는 L482 RAR 의 PASS_STRONG 격상을 위한 4 sub-criteria (S1 cross-form invariance ≤ 1.5, S2 cross-anchor Δlog ≤ 0.10 dex, S3 χ²/dof ≤ 1.6, S4 ΔAICc ≤ −5 with hidden DOF +3 패널티) 를 *분석 전* lock 한다. 5 함수형 (M16/simple-ν/standard-μ/exponential/Bekenstein2004) × 4 anchor (SPARC175/Q1/dwarf/bright) = 20 cell *동시* 보고 의무. 사후 임계값 변경 / cherry-pick / Υ★ 재선택 발생 시 격상 자동 무효. 현재 데이터 (L492 cross-dataset PASS 1/4) 로는 S2/S3/S4 FAIL 예상 — 격상 통과는 dwarf RAR 데이터 갱신 + Bayesian Υ marginalization 후에만 가능.**

---

*저장: 2026-05-01. results/L501/RAR_PREREG.md (DRAFT v0). 본 문서는 pre-registration 카탈로그이며 simulations/ 신규 코드 0줄, paper/ 직접 수정 0건. 8인/4인 라운드 전 단계.*
