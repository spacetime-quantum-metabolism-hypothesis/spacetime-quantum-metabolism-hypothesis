# L403 ATTACK_DESIGN — Q parameter canonical definition

**세션**: L403 (독립)
**주제**: R5 audit 로 노출된 Q (양자-고전 transition) 정의 비유일성 — 8인 reviewer 가 어떻게 공격할 수 있는가, 그리고 collapse model (Penrose-Diosi, GRW, CSL) 자유도 대비 SQT 의 자유도 정량.
**날짜**: 2026-05-01
**정직 한 줄**: SQT 의 "Q 정의 비유일" 은 다섯 차원적합 표현 모두 계수 prefactor (∼1) 와 micro 파라미터 (m, L, T_obs, T_K) 의 시스템별 선택 자유도를 가지므로, "0 free parameter" 광고 (R5 audit 가 지적한) 는 부정확하다 — 본 문서는 이를 reviewer 시각에서 8개 공격면으로 정리한다.

## CLAUDE.md 준수 점검

- **[최우선-1] 방향만, 지도 금지**: 본 문서는 다섯 정의의 *이름* (action/ℏ, Penrose-Diosi, Joos-Zeh, phase-space cell, information-theoretic) 만 거론. 어떤 수치적 prefactor 도 "써라" 형태로 지시하지 않음. 결정 기준만 제시.
- **[최우선-2] 팀 독립 도출**: 본 문서는 reviewer 공격면을 재구성할 뿐, 팀이 어떤 정의를 채택할지 사전에 암시하지 않음.
- **역할 사전 지정 금지**: 8인 attack team / 4인 review team 인원 수만 명시.

---

## 1. R5 audit 가 노출한 빈자리

R5 audit 의 핵심 발견 (사용자 진술):

1. *Dimensionally-consistent* Q 후보가 5개 존재.
2. Q_macro 값이 정의에 따라 **38 자릿수** 변동.
3. paper/base.md 가 canonical 정의를 명시하지 않음.
4. 결과적으로 "0 free parameter" 라는 광고 문구는 *정의 자유도* 를 숨기는 것.

이 빈자리를 reviewer 가 어떻게 활용할지 8개 채널로 정리한다.

## 2. 8인 attack team — 공격 채널 매트릭스

| ID | 공격 채널 | 핵심 질문 | reviewer 의 무기 |
|----|----------|----------|-----------------|
| **A1** | 정의 비유일 = hidden DOF | "5개 후보 중 *어느 것* 이 SQT 인가? 데이터 본 후 고를 여지가 있다면 free parameter 가 0이 아니라 ≥1." | model-selection literature (Gelman & Rubin 2013, Kass-Raftery 1995) — *post-hoc* 정의 선택은 효과적 자유도. |
| **A2** | prefactor (∼1) 자유도 | "각 정의의 차원 표현은 동일하지만 *수치 계수* 가 자유. 'tau* = 2e4' 같은 임계값은 fitted, 즉 hidden tunable." | Penrose-Diosi 의 prefactor 1/2 vs 1/6 논쟁 (Bahrami 2014). |
| **A3** | Penrose-Diosi 와의 직접 비교 | "Penrose-Diosi 는 m, L 두 micro 파라미터로 시스템마다 lab 에서 측정 가능 (Bassi 2017 review). SQT Q 도 같은 입력을 요구하면 차별점 없다." | Bassi-Hornberger 리뷰 (RMP 2013) — 정량적 falsifiable bound. |
| **A4** | GRW 의 두 자유도 (lambda, r_C) 와 비교 | "GRW 는 명시적으로 2 free parameter (rate, localisation length) 를 인정. SQT 는 같은 정보를 다른 이름으로 숨기고 있는 것 아닌가?" | Adler 2007 lambda upper bound; Toros-Bassi 2017 r_C bound. |
| **A5** | CSL 의 mass-proportional coupling | "CSL 는 m 에 비례하는 single-parameter 추가만으로 commutativity 회복. SQT 는 m, L, T_obs, T_K 4 input 모두 사용 → CSL 보다 *더* parameter rich." | Continuous Spontaneous Localisation (Pearle-Squires 1994). |
| **A6** | Q_macro 38-decade 변동 | "정의에 따라 Q(apple) 이 1e10 ↔ 1e48. 이는 *예측력 부재* 의 직접 증거. 이론이 어떤 macro Q 를 예측하는가?" | reproducibility / robustness 비판 (Munafò 2017). |
| **A7** | decoherence rate matching 부재 | "Joos-Zeh 와 Zurek 의 정량 분석은 *시스템별* lab 측정값과 비교 가능. SQT Q 의 임계값 tau* 는 lab 측정으로 어떻게 검증되는가?" | Arndt-Hornberger 2014 matter-wave decoherence experiments. |
| **A8** | microscopic derivation 부재 | "다섯 후보 모두 *order-of-magnitude* 휴리스틱. SQT axiom 에서 어떤 정의가 *유도* 되는가?" | derivation-vs-postulation 구분 (Wallace 2012). |

### 2.1 severity triage

- **High**: A1 (정의 비유일 = hidden DOF), A6 (38-decade 예측력 부재), A8 (microscopic derivation 부재).
- **Medium**: A2 (prefactor), A3 (Penrose-Diosi 비교), A7 (lab matching).
- **Low** (defensible): A4, A5 (collapse model 비교는 sector 다름 — SQT 는 spacetime-level, GRW/CSL 은 wave-function level).

## 3. SQT vs collapse model 자유도 정량

| model | explicit free params | implicit (정의/계수) DOF | total effective DOF |
|-------|---------------------|--------------------------|---------------------|
| GRW (Ghirardi-Rimini-Weber 1986) | 2 (lambda, r_C) | 0 | **2** |
| CSL (Pearle-Squires 1994) | 2 (lambda_CSL, r_C) | 1 (mass-scaling exponent) | **3** |
| Penrose-Diosi 1996 | 0 (E_G ≡ G m²/L 고정) | 1 (numerical prefactor 1/2 vs 1/6) | **1** |
| **SQT (현재 paper/base.md)** | 0 광고 | 5 (A/B/C/D/E 정의 선택) + 4 (m, L, T_obs, T_K input scheme) + 1 (prefactor) | **≥6** (광고 0과 격차) |

→ **A1 공격이 reviewer 의 가장 강한 무기**. SQT 의 광고 "0 parameter" 는 *정의 채택* 까지 포함하면 깨진다. 이것이 R5 audit 의 핵심 지적과 일치.

## 4. defence 가능성 (선제 식별)

- **D1**: 5개 정의 중 하나를 axiom-level *유도* 로 선정 → free param 회수. (→ NEXT_STEP 의 이슈.)
- **D2**: prefactor (∼1) 는 *대수적 정의* 이지 *피팅 자유도* 아님을 textual 로 못박기 (Penrose 1996 의 1/2 prefactor 와 동일한 위상).
- **D3**: Q_macro 38-decade 변동은 정의 선택을 못 한 책임이며 단일 정의 선정 후 사라짐 (D1 종속).
- **D4**: lab matching 은 matter-wave interferometry 데이터 (C60, oligopeptide, nanoparticle) 와 직접 대조 가능 — 본 세션 simulation 으로 *검증 가능* 임을 보임.

## 5. 본 세션 simulation 의 역할

본 attack design 의 **A1, A6, A8** 직격 응답을 위해 simulation 은:

1. 5 정의 모두를 같은 benchmark set (15 시스템: electron → Earth orbit) 에서 평가.
2. classification accuracy + threshold tau* + dynamic span 측정.
3. 모든 정의가 *공통 fundamental constants* (hbar, c, G, k_B) 만 쓰고 prefactor 를 1로 고정 → 정의 자유도가 분류 능력 차이로 환원되는지 검증.
4. ranking 결과를 NEXT_STEP 결정 기준의 *입력* 으로 사용.

본 simulation 은 결정자가 아니라 *정보 제공자*. 최종 canonical 선정은 NEXT_STEP 에서 8인팀이 수행.

## 6. team 권고

- **Rule-A 8인 (이론 클레임)**: A1/A2/A3/A8 응답 (정의 선정 정당화) 은 8인 자율 분담 검토 필수.
- **Rule-B 4인 (코드)**: simulations/L403/run.py 의 5 정의 구현 및 benchmark 라벨링은 4인 자율 분담 코드리뷰 필수.

---
산출물 인벤토리는 REVIEW.md 참조.
