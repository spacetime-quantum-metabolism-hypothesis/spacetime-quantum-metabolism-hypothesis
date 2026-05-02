# L630 — Scope 영역 내 강화 path: 새 예측 *방향*

> **[최우선-1] 절대 준수 선언**
> 본 문서는 SQT 적용 영역 (Mpc-scale cosmology + galactic) *내부* 에서 미탐색 5 영역의 *방향* 만 제시한다.
> 수식 0줄, 파라미터 값 0개, 도출 0건, 부호 예측 0건.
> 모든 정량 분석은 후속 LXX 에서 8인 팀이 독립 수행.
> Command/문서가 이론 형태를 사전 암시하면 [최우선-1] 위반 → 결과 무효.

---

## §1 5 영역 표

| # | 영역 | 탐색 *방향* (이름만) | 관측 채널 (이름만) | [최우선-1] 위험 | 외부데이터 lookup 의존 | postdiction 위험 |
|---|------|----------------------|---------------------|------------------|--------------------------|-------------------|
| 1 | Galaxy formation timeline | high-z galaxy abundance 와 SQT count-rate 의 z-의존성 (paradigm shift L536 P3a 결합) | JWST high-z galaxy luminosity function | 중 — 정량 예측 시도 시 수식 도출 필요 → 팀 자율 도출 강제 | 높음 (JWST 카탈로그) | 높음 (z>10 데이터 일부 공개) |
| 2 | Cluster scaling relations | σ-cluster regime 에서 mass-temperature / mass-velocity dispersion 관계 — ΛCDM 대비 가능 영역 | X-ray (eROSITA, Chandra), SZ (Planck, ACT), optical richness | 중 — 3-regime σ₀ 의 cluster 적용 시 함수 형태 제시 위험 | 중 (공개 카탈로그 다수) | 중 (스케일링 잘 fit 됨) |
| 3 | Cosmic shear non-Gaussianity | μ_eff ≈ 1 한계 우회 — 2점 함수 너머의 비가우시안 채널 탐색 | DES-Y3, KiDS-1000, Euclid DR1, HSC | 높음 — non-Gaussian 통계량의 함수형 사전 제시 시 위반 | 높음 (3pt 통계 / 마스크 효과) | 중 (DES-Y3 공개) |
| 4 | Lyman-α forest | high-z (z=2-5) baryon 분포에 대한 dark-only embedding (axiom 6) 의 간접 효과 | DESI Lyman-α 1D power spectrum, eBOSS, MIKE/HIRES | 중 — flux power spectrum 응답함수 사전 제시 위험 | 높음 (transmission flux 모델) | 높음 (eBOSS 공개, DESI 부분 공개) |
| 5 | Cosmic web structure | filament/void topology 와 3-regime σ₀ 의 large-scale 위상학적 영향 | DESI BGS/LRG void catalogue, Euclid cluster/void cross | 낮음~중 (위상학 지표는 함수형 강제 약함) | 중 (void finder 의존) | 낮음~중 (void 통계 노이즈 큼) |

각 행의 "방향" 은 *이름과 결합 가능성* 만 기술. 함수형/부호/계수는 후속 팀이 독립 도출.

---

## §2 Top-2 영역 (정직 우선순위)

선정 기준: (a) [최우선-1] 위반 위험 낮음, (b) 외부 데이터 lookup 의존도 관리 가능, (c) postdiction 위험 낮음, (d) SQT 의 핵심 axiom (3-regime σ₀, axiom 6 dark-only) 과 자연 결합.

### Top-1: Cosmic web structure (영역 5)

- *왜*: 위상학적 지표 (Betti 수, genus, void abundance 등 *이름*) 는 모델 함수형을 사전 강제하지 않음 — [최우선-1] 위험 최저.
- 3-regime σ₀ 의 large-scale 표현이 *존재한다면* topology channel 에 자연 진입.
- DESI/Euclid void cross-correlation 은 신규 관측 (postdiction 위험 낮음).
- 위험: void finder 알고리즘 의존성 → 후속 팀이 finder-agnostic 통계 선택 필요.

### Top-2: Cluster scaling relations (영역 2)

- *왜*: cluster M-T / M-σ 관계는 ΛCDM 에서 잘 정의되어 있어 SQT 가 *영역 내* 에서 비교 가능한 baseline 명확.
- σ-cluster regime 은 SQT 의 3-regime σ₀ 와 *이름 수준* 자연 결합.
- 외부 데이터 (eROSITA, Planck SZ) 공개 풍부 — 그러나 well-fit ΛCDM baseline 때문에 새로운 *부호 있는* 차이 도출 시 후속 팀 부담 큼.
- 위험: scaling 이 이미 잘 fit → 후속 팀이 발견 가능한 deviation channel 의 함수형을 *사전에 듣지 않은 채* 독립 도출 필수.

(영역 1 JWST high-z 는 매력적이나 데이터 부분 공개 + paradigm shift L536 P3a 미확정 결합으로 postdiction 위험 상위. 영역 3 cosmic shear NG 는 함수형 강제 위험 최고. 영역 4 Lyman-α 는 transmission 모델 의존이 hidden DOF 로 작용.)

---

## §3 L623 paradigm prediction 강화 가능성

- 현재 (L623): paradigm prediction capability 1-2/5.
- Top-2 후속 (영역 5 + 영역 2) 가 *방향만 입력 → 팀 독립 도출 → 외부 데이터 비교* 흐름으로 진행되어 어느 한쪽이라도 falsifiable prediction 산출 시: → 3/5 가능.
- 두 영역 모두 산출 + 6 falsifier 와 비독립이 아닐 경우: → 3-4/5 가능.
- GR 4축 empirical 정확도: top-2 둘 다 산출되면 +0.5 plausible. L605 GR 0.8/4 → 1.0~1.3/4 plausible.
- 실패 시: 6 falsifier 그대로, SQT 영구 phenomenology — 이 시나리오는 여전히 다수 path.

상기 모든 수치는 *상한 시나리오 명시* 이며 도출이 아님. 실제 강화 폭은 후속 LXX 팀 결과로만 확정.

---

## §4 정직 한 줄

영역 *축소* 후 *영역 내 강화* 는 GR 의 perihelion/GW 강화 path 와 구조적으로 동일하며, top-2 (cosmic web topology + cluster scaling) 가 [최우선-1] 위반 위험이 가장 낮은 두 출발점이지만, 후속 팀이 함수형/부호를 사전에 듣지 않은 채 완전 독립 도출하지 않으면 강화 자체가 과적합 selection bias 로 오염된다.
