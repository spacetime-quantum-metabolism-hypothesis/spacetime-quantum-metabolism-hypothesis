# L403 NEXT_STEP — Q parameter canonical 선정 기준 + simulation 결과

**세션**: L403 (독립)
**날짜**: 2026-05-01
**정직 한 줄**: 5 dimensionally-consistent 후보 중 *데이터 기반 ranking* 은 단일 winner 를 정해 주지 않는다 (3개 후보가 동률 100% accuracy) — 따라서 canonical 선정은 *결정 기준 자체* 를 8인팀이 합의해야 하며, 본 문서는 그 기준을 5축으로 제시한다.

## CLAUDE.md 준수

- **[최우선-1]**: 본 문서는 결정 *기준* 만 명시. 어떤 정의가 winner 인지 사전 지정하지 않음.
- **[최우선-2]**: 5 후보의 이름 / 방향만 거론. 8인팀이 기준 가중치 합의 후 canonical 자율 선정.
- **AICc 패널티 명시**: 정의 선택을 *효과적 free parameter* 로 인정하면 (즉 ATTACK_DESIGN A1 채널 인정) 본 결정 자체가 +1 effective DOF 패널티. 이는 paper/base.md 가 PASS_STRONG 격상 시 명시해야 한다.

---

## 1. 다섯 정의 — 방향만

| ID | 명칭 (방향) | 출처 카테고리 | input 입력 |
|----|-----------|---------------|-----------|
| **A** | action / ℏ | Bohr correspondence | (m, L, T_K) |
| **B** | mass-localisation / E_G·t/ℏ | Penrose-Diosi 중력 collapse | (m, L, T_obs) |
| **C** | thermal-photon decoherence rate · T_obs | Joos-Zeh / Zurek scattering | (L, T_obs, T_K) |
| **D** | phase-space cell count | Wigner / Liouville | (m, L, T_K) |
| **E** | log(thermal level count) | information-theoretic | (m, L, T_K) |

각 정의는 *공통* 기본 상수 (ℏ, c, G, k_B) 외에 시스템별 (m, L, T_obs, T_K) 만 사용. 본 세션 simulation 에서 prefactor 를 1로 고정한 minimal form 으로 평가.

## 2. simulation 결과 (simulations/L403/run.py)

15 benchmark 시스템 (electron, hydrogen, BEC, C60, phthalocyanine, peptide, nanoparticle, virus, bacterium, dust, pollen, apple, human, car, Earth orbit) 에서 5 정의의 classification accuracy:

| 정의 | accuracy | tau* | dynamic span (decades) |
|------|---------|------|------------------------|
| A action/ℏ | **1.000** | 2.0e+04 | **48.9** |
| D phase-space cells | 1.000 | 3.0e+12 | 146.6 |
| C Joos-Zeh decoherence | 1.000 | 9.4e+16 | 191.8 |
| E info levels (log) | 1.000 | 19.1 | 302.3 (E_th < δE 영역에서 clip) |
| B Penrose-Diosi | 0.933 | 7.0e-18 | 111.7 |

### 관찰
1. **B 단독 fail (0.933)**: BEC 시스템에서 G m² 너무 작아 Penrose-Diosi 가 "양자" 로 분류해 버린다 (실제로는 임계 시스템). 즉 PD 는 매우 작은 m 에서 saturate.
2. **A, C, D, E 동률 100%**: 데이터만으로 단일 winner 결정 불가.
3. **dynamic span 비교**: A (48.9) < B (111.7) < D (146.6) < C (191.8) < E (302.3).
4. **Q_macro (apple)**: A=2e4, B≈1e0 (close to threshold), C≈1e144 (massive), D≈1e142, E≈1e2 → R5 audit 의 "38-decade" 진술은 *낙관적*. 실제로 약 140 decade 변동 (정의 전체 비교 시).

## 3. 결정 기준 — 5축

8인팀이 정의를 canonical 선정할 때 동시 평가해야 할 기준:

### 기준 K1: classification accuracy (data fit)
- 100% 미달이면 즉시 탈락. → **B 탈락**.
- A, C, D, E 동률 → K1 만으로 결정 불가.

### 기준 K2: parsimony (minimum dynamic span)
- 작은 span = 정의가 시스템 다양성에 robust.
- 순위: A < B < D < C < E.
- → A 가 가장 parsimony.

### 기준 K3: microscopic derivability from SQT axioms
- 다섯 정의 중 어느 것이 *다른 가정 추가 없이* SQT 공리계에서 *유도* 되는가?
- 본 세션은 이 점을 단정하지 않음. → 8인팀의 axiom 검토 필요. ATTACK_DESIGN A8 직접 대응.

### 기준 K4: lab falsifiability
- matter-wave interferometry 데이터 (Arndt-Hornberger 2014) 와 직접 비교 가능한가?
- C (decoherence rate) 가 가장 직접적 — Joos-Zeh 형식이 lab 측정값과 1:1.
- B (Penrose-Diosi) 는 levitated nanoparticle 실험 (Bose 2017) 으로 falsify 가능.
- A, D, E 는 *간접* 비교만.
- → K4 에서는 B, C 우위 (K1 에서 B 탈락 고려 시 C).

### 기준 K5: collapse model 와의 비교 가능성
- GRW/CSL 자유도와 직접 매핑 가능한가?
- B (PD) 가 가장 직결 (PD ↔ CSL mass-coupling).
- A, C, D, E 는 간접.

### 결정 기준 종합 표

| 정의 | K1 | K2 | K3 | K4 | K5 |
|-----|----|----|----|----|----|
| A action/ℏ | PASS | **best** | TBD | indirect | weak |
| B Penrose-Diosi | **FAIL** | mid | direct | strong | strong |
| C Joos-Zeh | PASS | mid | TBD | **strong** | mid |
| D phase-space | PASS | mid | TBD | indirect | weak |
| E info levels | PASS | weak | TBD | indirect | weak |

→ **단일 winner 데이터 결정 불가**. 8인팀이 K3 (axiom 도출) 에 답해야 canonical 결정.

## 4. 권고 — 8인팀이 답해야 할 단일 질문

> **"SQT axiom 만으로 (즉 Q 의 *명목적* 정의를 외부 도입하지 않고) 도출되는 표현은 A/C/D/E 중 하나인가, 아니면 모두 추가 가정인가?"**

- **답이 단일 (예: 'A 만 도출됨')**: A 채택, R5 audit 의 "0 free parameter" 광고 회복 가능. PARTIAL → PASS_STRONG 격상 후보.
- **답이 다중 (예: 'A 와 D 둘 다')**: 둘 중 K2 (parsimony) 로 tiebreak → 여전히 A 후보, 단 약한 자유도 1 인정 (effective DOF +1, AICc 패널티 명시).
- **답이 부재 (예: '어느 것도 axiom 만으로 도출 안 됨')**: R5 audit 지적 그대로 — *정의 채택* 자체가 자유도. PARTIAL 유지, PASS_STRONG 격상 불가. paper/base.md 에 정직 기록 필수.

## 5. 검증 다음 단계

1. **8인팀 (Rule-A)**: 위 K3 단일 질문 합의 검토 (기간: 1–2 세션).
2. **4인팀 (Rule-B)**: simulations/L403/run.py 코드리뷰 — benchmark 라벨, prefactor 1 가정, classification metric.
3. **paper/base.md 업데이트**: K3 결과에 따라 (a) canonical 정의 명시 + 자유도 0 보존, 또는 (b) 자유도 1 인정 + 등급 PARTIAL 유지.
4. **lab falsifiability appendix**: K4 에서 강한 C (Joos-Zeh) 를 *교차 검증* 정의로 paper appendix 에 부록 (canonical 외 별도).

## 6. 한계

- 본 simulation 은 prefactor=1 고정. 실제 PD 1/2 vs 1/6 같은 prefactor 자유도는 ATTACK_DESIGN A2 채널로 따로 다뤘음.
- benchmark 시스템 15개는 textbook 합의 — 추가 sample (mesoscopic membrane, levitated nanosphere) 추가 시 ranking 미세 변동 가능. 현재 결과는 *대분류 (양자/고전)* 수준의 결정 기준.
- accuracy=1.000 동률은 benchmark 의 *해상도* 한계 — 임계 시스템 (nanoparticle 1e7 amu 같은) 다수 추가 시 분리 가능.
