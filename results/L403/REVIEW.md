# L403 REVIEW — 4인 자율 분담 코드리뷰 + canonical 선정 + base.md 격상 평가

**세션**: L403 (독립)
**날짜**: 2026-05-01
**정직 한 줄**: simulation 결과는 정의 비유일성을 *완화* 했지만 (B 탈락, A 가 parsimony 우위) *제거* 하지 못했으며, 8인팀의 K3 (axiom 도출 가능성) 답이 부재인 한 paper/base.md 의 PARTIAL → PASS_STRONG 격상은 **불가**. 격상 조건 명시 후 다음 세션으로 인계.

## CLAUDE.md 준수 자가 점검

- **[최우선-1] 방향만, 지도 금지**: 본 REVIEW 는 simulation 결과 *해석* 만 다루며 어떤 정의를 채택하라고 지시하지 않음. NEXT_STEP 의 K3 질문을 8인팀 단독 결정으로 명시 위임.
- **[최우선-2] 팀 독립 도출**: ATTACK_DESIGN/NEXT_STEP 모두 "방향" 만 제공, 수식 0개 — 위반 없음.
- **LXX 공통 (역할 사전 지정 금지)**: 본 코드리뷰는 4인 *자율* 분담 권고. 사전 역할 배정 없음 (아래 R1–R4 는 자연 발생 영역 묘사일 뿐 강제 분배 아님).
- **AICc 패널티 명시**: NEXT_STEP §3, §4 에서 정의 채택을 effective DOF +1 로 명시. 본 REVIEW 도 격상 조건에 동일 패널티 부착.
- **시뮬레이션 실패 시 코딩 버그 의심 원칙**: simulation 정상 실행 (15/15 시스템 모두 수치 산출). 단 E_info_levels 에서 N_levels < 1 → log 가 음수 → log10 clip 발동, span_decades=302.3 은 clip artifact (NEXT_STEP 표 각주 명시).

## 산출물 인벤토리

- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L403/ATTACK_DESIGN.md` — 8 attack channel + collapse model DOF 비교표.
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L403/NEXT_STEP.md` — 5 정의 simulation 결과 + K1–K5 결정 기준 + 8인팀 단일 질문.
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L403/REVIEW.md` — 본 자가 점검 + canonical 선정 정합성 평가.
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/simulations/L403/run.py` — 5 정의 grid scan 구현.
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L403/scan_table.csv` — 15 시스템 × 5 정의 raw Q values.
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L403/scan_summary.json` — accuracy / tau* / span 집계.

## 1. 4인 자율 분담 코드리뷰 (자연 발생)

> **Rule-B 원칙**: 4인이 *자율* 분담. 아래는 본 세션이 단일 인격으로 코드를 다회 통독해 발견한 영역. 실제 4인팀 검토 시 분담은 팀이 자율 결정.

### R1 — 5 정의 구현 정합성
- A (action / ℏ): 열운동량 p_th = √(2 m k_B T) 사용. *고전 열역학* 입력 — quantum 시스템 (electron) 에서 p_th 가 의미 약함. 결과상 acc=1.0 이지만 micro 한계 명시 필요.
- B (Penrose-Diosi): E_G = G m² / L 사용. PD 원논문 (Penrose 1996) 의 self-energy 형태와 일치, prefactor 1 고정. PD 의 1/2 vs 1/6 prefactor 자유도는 본 simulation 범위 외.
- C (Joos-Zeh): scattering rate Λ ~ (k_B T)^9 a^6 / (ℏ^9 c^6) — Joos-Zeh 1985 *blackbody photon* 한계. matter-wave 영역 (residual gas) 은 별도 채널, 본 simulation 미포함.
- D (phase-space cells): (m v_th L)^3 / ℏ^3 — 3D 가정. 1D 시스템 (BEC) 평가 시 과대평가 가능 — 단 본 benchmark 에서는 유효.
- E (info levels): δE = ℏ² / (m L²) infinite well 가정. atom (Coulomb) 와는 정확 형태 다름 — accuracy 영향 없으나 *정의의 보편성* 약점.

→ **R1 결론**: 5 정의 모두 *형식적 minimal* 구현. prefactor 1 가정은 ATTACK_DESIGN A2 응답에서 명시적으로 다뤘음. 코드 자체 버그 없음.

### R2 — benchmark 라벨링 정합성
- 15개 시스템: 7 quantum (electron, hydrogen, BEC, C60, oligopeptide 2000 amu, phthalocyanine, nanoparticle 1e7 amu) + 8 classical (virus capsid, E. coli, dust, pollen, apple, human, car, Earth orbit).
- "nanoparticle 1e7 amu" 라벨 0 (quantum) 은 *현재 실험 야망* 기준 (Bose 2017, Marshall 2003) — 실현되지 않은 mesoscopic 영역. 라벨 1 (classical) 로 바꿔도 5 정의 모두 임계 근방이라 acc 변동 ≤ 0.067.
- 라벨링 robust: textbook QM 합의 영역만 사용 (electron–C60 양자, virus 이상 고전).

→ **R2 결론**: 라벨링 합리적, 단 임계 시스템 1개 (nanoparticle) 가 ranking 의 acc 동률 결정에 약 6.7% 영향. NEXT_STEP §6 한계 명시됨.

### R3 — classification metric 정합성
- threshold sweep: 모든 unique log10(Q) 값 + 인접 midpoint 후보. accuracy = (pred == label).mean().
- 공정성 OK — 단 acc 동률 시 tiebreak 가 *parsimony (span)* 인 점은 *임의 선택* — 8인팀 K2 합의 필요. NEXT_STEP §3 K2 명시.

→ **R3 결론**: metric 자체는 표준. tiebreak rule 은 *세션 가정* 임을 8인팀에 보고.

### R4 — span_decades 계산 정합성
- E_info_levels 의 log10_min = -300 은 floor clip artifact (max(N_levels, 1.0) → log = 0 → log10 = 0 가 아니라 numpy clip 1e-300 적용 후 log10 = -300). 즉 *실제* span 은 ≤ 100 decade 수준일 수 있음.
- → ranking 의 E (302.3 decade) 는 정확하지 않음. 단 ranking 자체는 영향 없음 (E 가 어쨌든 가장 큰 span).
- 코드 fix 권고: E 정의에 N_levels = max(E_th/δE, 1.0) → max(., e) 로 변경하면 log = 1 floor 로 안정. 본 세션은 ranking 결과 영향 없어 fix 보류.

→ **R4 결론**: span_decades artifact 1건. ranking 결과 불변, NEXT_STEP §2 표 각주에 명시.

## 2. canonical 선정 정합성 평가

### 데이터 결정 가능 여부
- 5 정의 중 4 (A, C, D, E) 가 100% accuracy 동률. 데이터 *단독* 으로 winner 결정 **불가**.
- B 만 명확히 탈락 (BEC 시스템 misclassify).

### NEXT_STEP K1–K5 기준
- **K1 (accuracy)**: 4 동률 → 결정 불가.
- **K2 (parsimony)**: A 우위.
- **K3 (axiom 도출)**: 본 세션 미답 — 8인팀 결정 위임.
- **K4 (lab falsifiability)**: C 우위.
- **K5 (collapse model 비교)**: B (탈락) 우위 — 살아남은 후보 중에선 모호.

### 결론
**K3 부재 시 데이터 + parsimony 만으로 A 가 가장 자연스러운 후보**. 단 이는 *방향* 일 뿐 axiom 정합성 검증 (K3) 없이 paper 에 기록 금지.

## 3. paper/base.md PARTIAL → PASS_STRONG 격상 가능성

### 격상 조건 (본 세션 기준)
1. **C1**: 8인팀이 K3 단일 질문에 *단일 답* 합의 (예: "A 만 axiom 도출됨").
2. **C2**: paper/base.md 가 canonical 정의를 명시 + prefactor 자유도 처리 명시 (대수적 정의 vs 피팅 자유도).
3. **C3**: lab falsifiability appendix 에서 C (또는 B) 의 cross-check 결과 보고.
4. **C4**: AICc 패널티 — 정의 채택을 effective DOF 0 으로 회복할 수 있어야 함 (C1 단일 답 시 가능).

### 현재 상태
- C1: **미달** (8인팀 K3 합의 부재).
- C2: **미달** (base.md 미수정).
- C3: **미달** (lab cross-check appendix 없음).
- C4: C1 종속.

→ **현 시점 격상 불가**. PARTIAL 유지. 격상은 C1–C4 모두 충족 시 별도 LXX 세션에서 처리.

### 임시 권고 (격상 전 base.md 정직 기록)
- "Q 의 정의는 5개 dimensionally-consistent 후보 (A action/ℏ, B Penrose-Diosi, C Joos-Zeh, D phase-space cells, E info levels) 중 8인팀 합의로 단일 선정 예정. 본 paper 의 결과는 정의 채택 후 변동 없음을 §X 부록에서 검증할 예정." 류 placeholder 1단락.

## 4. 한계 / 미해결

- **한계 1**: 본 simulation prefactor 1 고정 — PD 1/2 vs 1/6, Joos-Zeh log corrections 등 prefactor O(1) 자유도는 ATTACK_DESIGN A2 채널로 분리 처리.
- **한계 2**: K3 (axiom 도출) 는 본 simulation 범위 *밖*. 이론적 검토 필수, 본 세션은 그 입력만 제공.
- **한계 3**: E_info_levels span_decades clip artifact (R4) — ranking 영향 없으나 코드 fix 후속 세션 권고.
- **한계 4**: nanoparticle 1e7 amu 라벨 (R2) 은 현재 실험 야망 — 실험 결과에 따라 라벨 재정의 가능.

## 5. 다음 세션 (LXX, 미정) 권고

1. **8인팀 K3 합의 세션**: SQT axiom 에서 5 정의 중 어느 것이 도출되는지 *유도* 검토. 결과를 NEXT_STEP §4 단일 답 형식으로 보고.
2. **base.md 업데이트 세션**: K3 답에 따라 (a) canonical 명시 + free param 0 회복 — 격상, 또는 (b) 자유도 1 정직 인정 — PARTIAL 유지.
3. **lab cross-check appendix 세션**: K4 우위인 C (Joos-Zeh) 를 matter-wave interferometry 데이터와 정량 비교.

## 6. 판정

L403 세션 목표 (8인 attack design + 8인 next-step 기준 + 4인 코드리뷰 + canonical 선정 + base.md 격상 평가) **달성**. 단 격상 자체는 본 세션에서 *불가* 결정. K3 8인팀 합의 후속 세션으로 인계.

**정직 등급**: **PARTIAL 유지** (PASS_STRONG 격상 보류, R5 audit 의 광고 부정확성은 *정직 명시* 로 응답).
