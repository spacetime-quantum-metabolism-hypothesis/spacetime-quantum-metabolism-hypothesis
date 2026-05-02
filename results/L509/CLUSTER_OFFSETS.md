# L509 — Bullet PASS_STRONG cross-sample robustness audit

## 정직 한 줄
SQT 의 "lensing peak ≡ collisionless component" 정성 진술은 Bullet/MACS J0025/MACSJ1149 에서는 자연 통과하지만 Abell 520 (train wreck) 의 "dark core" 에서 정성-수준에서도 *직접 충돌* — 4 샘플 cross-validation 결과 **PASS_QUALITATIVE_ONLY 유지, PASS_STRONG_QUANTITATIVE 격상은 4/4 모두 불가** (magnitude 가 SQT 외부 gas/ICM 동역학 입력에서 결정됨).

---

## 1. 사전 조건 (L417 요약)

L417 결정:
- SQT 가 *독자적으로 예측* 하는 것: peak_lens − peak_galaxy ≈ 0 (depletion zone tracks collisionless component / galaxies).
- SQT 가 예측 *못 하는* 것: peak_lens − peak_gas magnitude. 150 kpc 는 gas ram-pressure 입력의 echo.
- 결과: `PASS_QUALITATIVE_ONLY` (paper §4.1 row 10).

본 L509 는 이 정성 진술이 Bullet 외 *다른* dissociative 클러스터에서도 유지되는지 cross-sample 검증.

---

## 2. 4 샘플 정성 검증

### 2.1 Bullet (1E 0657-558, Clowe+ 2006)
- 관측: 두 lensing 피크가 두 galaxy 그룹 위치와 일치, gas (X-ray) 와는 ~150 kpc 분리.
- SQT 정성 진술: `peak_lens ≡ peak_galaxy` ✓
- SQT 정량 진술 (magnitude): gas ram-pressure stripping 으로부터 분리량이 들어옴 — *외부 입력*.
- 판정: **PASS_QUALITATIVE** (재확인, L417 일치).

### 2.2 MACS J0025.4-1222 (Bradač+ 2008)
- 관측: z=0.586 의 두 클러스터 정면 충돌. 두 lensing 피크가 두 galaxy 농도와 ~ 일치, gas (X-ray) 는 중심부에 잔류.
- SQT 정성 진술: `peak_lens ≡ peak_galaxy` ✓ (Bullet 과 동일 구조).
- 판정: **PASS_QUALITATIVE** — Bullet 의 *독립* replication.
- Cross-sample 의의: SQT depletion zone 이 collisionless 트레이서를 따른다는 진술이 한 사례 의존이 아님을 보여줌.

### 2.3 MACSJ1149.5+2223 (Smith+ 2009; Limousin+ 2016)
- 관측: substructure 가 풍부한 다중 충돌 클러스터. lensing 피크가 BCG/galaxy 광도 분포와 잘 일치. 관측된 'dissociative' 분리는 Bullet/MACS J0025 보다 약함 (충돌 기하 복잡).
- SQT 정성 진술: `peak_lens ≡ peak_galaxy` — **약 PASS** (다중 substructure 로 single-pair 비교가 모호; offset magnitude 도 작음).
- 판정: **PASS_QUALITATIVE_WEAK** — Bullet/MACSJ0025 보다 falsification power 약함. SQT 에 대한 검증력 자체가 낮은 시스템.

### 2.4 Abell 520 ("train wreck", Mahdavi+ 2007; Jee+ 2012, 2014)
- 관측: lensing 피크 *하나* 가 galaxy density 가 *낮은* 영역, X-ray gas 근처에 위치 — 이른바 "dark core". collisionless trace 진술과 직접 충돌.
- 후속 (Clowe+ 2012; Peel+ 2017; Andersson+ 2018): WL re-analysis 로 dark core 유의성이 1–3σ 수준으로 약화/모호해짐. 현재 관측 측에서도 robust 결론 미정.
- SQT 정성 진술: `peak_lens ≡ peak_galaxy` — **dark core 가 진짜라면 FAIL**, 의문이라면 *데이터 미해결*.
- 판정: **AMBIGUOUS / POTENTIAL_TENSION** — SQT depletion zone 형식론은 Bullet 과 동일 구조로는 dark core 를 자연 생성 못 함.

---

## 3. SQT 의 dark core 처리 가능성

### 3.1 직접 SQT 도출 (Plummer/depletion-zone 1D)
불가. L417 의 σ_0(t) collision-modulation 채널은 ad hoc DEP_RATIO 도입 없이는 collisionless ↔ baryon 분리 magnitude 자체를 도출 못 함. dark core 처럼 lensing 이 *galaxy 와도 분리* 되는 경우는 더더욱 자연 도출 불가.

### 3.2 가능한 SQT 보조 설명
- (a) **Filament line-of-sight projection** (Clowe+ 2012): 추가 mass concentration 이 시선 방향. SQT 와 무관, 일반 ΛCDM 도 동일 회피 경로.
- (b) **Sub-cluster substructure pre-merger**: A520 은 4-way 충돌. multiple collision phase → depletion zone 이 어느 collisionless 성분을 따르는지 모호. SQT 가 정량 예측 못 함.
- (c) **Self-interacting dark sector** (CDM ↔ depletion): SQT 안에서 추가 σ 도입은 P14 axiom 외부 — over-fit.

⇒ SQT 가 A520 dark core 를 *자연스럽게* 설명하는 channel 없음. (a) projection 회피만 ΛCDM 과 동일하게 사용 가능.

---

## 4. Cross-sample 종합

| 시스템 | 관측 분리 | SQT 정성 (lens≡gal) | SQT 정량 magnitude | 판정 |
|---|---|---|---|---|
| Bullet | ~150 kpc | PASS | 외부 입력 (ram-pressure) | PASS_QUALITATIVE |
| MACS J0025 | ~190 kpc | PASS | 외부 입력 | PASS_QUALITATIVE |
| MACSJ1149 | 작음/모호 | weak PASS | n/a | PASS_QUALITATIVE_WEAK |
| Abell 520 | dark core | AMBIGUOUS/FAIL | n/a | TENSION (관측 자체 미해결) |

- **정성 진술 통과율**: 3/4 명확 PASS, 1/4 데이터 모호.
- **정량 magnitude 도출**: 4/4 모두 SQT 미도출 (외부 gas 동역학 입력).
- **PASS_STRONG_QUANTITATIVE 격상**: 4/4 모두 불가.

---

## 5. paper/base.md §4.1 row 10 권고

현재 라벨 `PASS_QUALITATIVE_ONLY` 유지. 다음 caveat 한 줄 추가:

> "Cross-sample (Bullet, MACS J0025, MACSJ1149, A520) 검증: 정성 진술 (lensing tracks collisionless) 은 3/4 PASS, A520 dark core 는 SQT depletion-zone 형식론 안에서 자연 설명 불가 — 관측 측 dark core 유의성 자체가 1–3σ 수준이라 falsification 미확정 (L509)."

PASS_STRONG → PASS_STRONG_QUANTITATIVE 격상은 cross-sample 에서도 정직하게 불가.

---

## 6. 한계 / hidden DOF

- 본 audit 는 *재시뮬 없음*. L417 1D Plummer toy 의 다른 시스템 일반화는 추가 작업 (L510+).
- A520 lensing reconstruction 의 systematic 은 본 audit 범위 밖. 관측 결정 시 SQT 에 대한 진짜 falsification.
- DEP_RATIO 등 σ_0(t) channel 의 ad hoc 파라미터는 4 샘플 모두에서 미도출 — universal SQT axiom 부재.

## 7. 출처
- Clowe, D. et al. 2006, ApJ 648, L109 (Bullet).
- Bradač, M. et al. 2008, ApJ 687, 959 (MACS J0025).
- Smith, G.P. et al. 2009; Limousin, M. et al. 2016, A&A 588, A99 (MACSJ1149).
- Mahdavi, A. et al. 2007, ApJ 668, 806; Jee, M.J. et al. 2012, ApJ 747, 96; 2014, ApJ 783, 78 (A520 "dark core").
- Clowe, D. et al. 2012, ApJ 758, 128; Peel, A. et al. 2017; Andersson, A. et al. 2018 (A520 reanalysis, dark core 유의성 약화).
- Project internal: results/L417/REVIEW.md, results/L495/HIDDEN_DOF_AUDIT.md, results/L496/GLOBAL_CV.md, paper/base.md §4.1.
