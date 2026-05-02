# L324 — Cross-Dataset Consistency Attack on BB σ_0

**Loop**: L324 (cumulative 236)
**주제**: SPARC + DESI BAO + Planck CMB 의 selection effect 차이 하에서
Branch-B σ_0 가 일관되게 추출되는가? — 글로벌 최적합의 핵심 검증.

---

## 0. Why this matters

L196~L321 에서 BB σ_0 = 4πG·t_P 는 단일 SPARC anchor 기반으로 검증.
글로벌 최적합 주장이 성립하려면 **셋 다른 dataset (회전곡선 / BAO / CMB)** 에서
- 동일 σ_0 값,
- 또는 selection-corrected reweighting 후 동일 통계,
이 회수돼야 한다. 회수 안 되면 SPARC-specific anchor 라는 비판이 결정타.

각 dataset 의 selection effect 가 서로 매우 다르기 때문에
"셋 모두 일관" 은 strong test, "한 dataset 에서만 보임" 은 falsifier.

---

## 1. 8인 공격 (selection-effect 중심)

### A1. SPARC selection bias
- **공격**: SPARC 175 disk galaxy 는 H I 풍부 + edge-on / inclination 30°<i<80°
  + 거리 측정 quality 컷 으로 들어옴. 즉 dynamically cold / 회전 지원 / gas-rich
  편향. BB 의 ratio 변환 (psi^n weighting) 이 이 sub-population 의
  baryonic anchor 만을 선택적으로 끌어올린 것일 수 있음.
- **요구**: SPARC 안에서 inclination / distance method / gas fraction
  3-strata jackknife — σ_0 stratum-별 변동.
- **falsifier**: σ_0(strata) 변동 > 0.5σ 면 selection-driven.

### A2. DESI BAO target selection
- **공격**: DESI 13 포인트는 BGS / LRG / ELG / QSO / Lyα — flux-limited,
  color-cut, redshift-quality 컷. 각 tracer 의 host halo 질량 / bias 가
  매우 다름 (b ≈ 1.3 ~ 2.5). BB 의 ratio 변환 인자가 tracer-bias
  와 degenerate 라면 σ_0 추출이 BAO 에서 SPARC 와 어긋남.
- **요구**: DESI 13pt 를 tracer-block (BGS, LRG1, LRG2, LRG3, ELG1, ELG2,
  QSO, Lyα) 단위로 BB-fit 분리. σ_0 tracer-별 변동.
- **falsifier**: tracer 별 σ_0 변동 > 1σ 면 BAO anchor 무효.

### A3. Planck CMB calibration
- **공격**: Planck compressed CMB (R, l_A, ω_b) 는 z*~1090 에서 ΛCDM
  reference 와 묶여 있음. SQT 배경 E(z) 가 z>3 LCDM bridge 를 사용
  (CLAUDE.md 룰) → CMB σ_0 추출이 사실상 LCDM 우선 가정에 의존.
- **요구**: bridge cut Z_CUT ∈ {2, 3, 5, 10} 에서 CMB chi2 응답.
  σ_0 추출이 Z_CUT 에 어떻게 변하나.
- **falsifier**: σ_0 가 Z_CUT 변동에 >0.5σ 민감하면 "CMB σ_0" 는 artefact.

### A4. Joint posterior shift
- **공격**: SPARC alone σ_0^S, BAO alone σ_0^B, CMB alone σ_0^C 가
  서로 inconsistent 하면 joint posterior 는 내부 tension 으로
  artificial 좁아질 수 있음 (Lin & Ishak 2017 IOI).
- **요구**: pairwise IOI(S↔B), IOI(S↔C), IOI(B↔C). triplet IOI.
- **falsifier**: 어느 pairwise IOI > 2.3σ 이면 joint 사용 정당성 붕괴.

### A5. Tension metric (Q_DMAP, suspiciousness)
- **공격**: Δχ²_joint 이 Δχ²_S + Δχ²_B + Δχ²_C 합보다 작은 경우
  (Q_DMAP test, Raveri-Hu 2019) → joint 가 fake-improvement 일 수 있음.
- **요구**: Q_DMAP = Δχ²(joint) - Σ Δχ²(single) 계산.
  suspiciousness S = log R - log I.
- **falsifier**: Q_DMAP > 9 (3σ tension) 또는 S > 5.

### A6. Selection-corrected reweighting
- **공격**: 셋 dataset 가 서로 다른 underlying galaxy/halo population 을
  볼 때, BB 의 universal σ_0 주장은 reweighting 없이는 무효.
  effective volume V_eff(z) 와 selection function S(M, z) 을 명시
  reweight 후 σ_0 extraction.
- **요구**: 각 dataset 의 V_eff 가중 chi2 재정의 후 σ_0 변화량.
- **falsifier**: reweighting 만으로 σ_0 가 변동 폭 >1σ.

### A7. Anchor cross-pull
- **공격**: SPARC anchor 가 BAO/CMB 의 자유도를 흡수해 false consistency
  를 만들 수 있음. BB 를 SPARC 없이 BAO+CMB 만으로 fit 했을 때
  σ_0 가 SPARC-only 와 별도로 회수돼야 진짜 cross-consistent.
- **요구**: leave-SPARC-out joint fit. σ_0^{BAO+CMB only} vs σ_0^{SPARC only}.
- **falsifier**: SPARC 빠지면 σ_0 unconstrained (posterior flat) 면 anchor-only.

### A8. Distance-ladder coupling
- **공격**: SPARC 거리는 TRGB / Cepheid / flow-model 혼합 (~5% systematic).
  BAO 는 r_d (sound horizon) anchor 에 의존. CMB 는 angular scale anchor.
  세 anchor 가 서로 calibration-coupled. σ_0 의 "agreement" 가
  거리 척도 cross-calibration artefact 일 수 있음.
- **요구**: SPARC 거리 ±5% perturbation 하에서 σ_0 회수 robust 한가.

---

## 2. 측정 가능한 KPI

| KPI | 통과 임계 | 강한 통과 |
|-----|-----------|-----------|
| K1 σ_0(SPARC) vs σ_0(BAO) tension | <2σ | <1σ |
| K2 σ_0(SPARC) vs σ_0(CMB) tension | <2σ | <1σ |
| K3 σ_0(BAO) vs σ_0(CMB) tension | <2σ | <1σ |
| K4 strata jackknife σ_0 (SPARC) | <0.5σ 변동 | <0.3σ |
| K5 tracer-block σ_0 (BAO) | <1σ 변동 | <0.5σ |
| K6 Z_CUT 민감도 (CMB) | <0.5σ | <0.2σ |
| K7 Q_DMAP joint | <9 (3σ) | <4 (2σ) |
| K8 suspiciousness S | <5 | <2.5 |
| K9 leave-SPARC-out σ_0 회수 | finite posterior | <1σ vs SPARC-only |

**합격 조건**: K1-K3 + K7 + K9 모두 통과 → cross-dataset consistent.
어느 하나라도 실패 → "SPARC anchor 의존성" 정직 명시 (Sec 6 추가).

---

## 3. 우선순위 (실행 가능성 + 임팩트)

1. **K1-K3 pairwise σ_0 tension** — 즉시 가능, 결정적.
2. **K9 leave-SPARC-out** — 즉시 가능, anchor 의존성 직접 시험.
3. **K4 SPARC strata jackknife** — A1 에 직격.
4. **K5 DESI tracer-block** — A2 에 직격.
5. **K6 Z_CUT 민감도** — A3 에 직격.
6. **K7 Q_DMAP** — A5 정량.
7. **K8 suspiciousness** — K7 보강.
8. **A6 V_eff reweighting** — 별도 loop 필요 (selection function 모델링).

---

## 4. 예상 결과 (사전 정직 기록)

L286 P19 Euclid 와 L302 missing-satellite 결과 비추어볼 때:

- K1 (SPARC↔BAO): **PASS 가능성 중간** (~50%).
  BAO 는 배경 E(z) level, SPARC 는 anchor pull → 다른 정보 채널.
- K2 (SPARC↔CMB): **PASS 가능성 낮음~중간** (~35%).
  CMB 는 LCDM bridge 의존이라 σ_0 응답 weak.
- K3 (BAO↔CMB): **PASS 가능성 중간** (~55%).
  둘 다 배경 dominated.
- K9 (leave-SPARC-out): **fail 위험 큼** (~60%).
  SPARC 빠지면 σ_0 posterior flat 가능성.
  → 이 경우 정직 disclosure: "BB σ_0 는 SPARC anchor-driven, BAO+CMB 만으로는
  미결정". Sec 6.5 신규.

이 예상이 맞으면 L324 결과는 negative-but-honest, 영구 limitation 1개 추가.
저널 acceptance 영향 -1~-2% (정직 disclosure 효과로 reviewer trust + 상쇄).
