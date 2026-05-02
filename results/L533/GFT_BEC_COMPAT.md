# L533 — GFT BEC 채택 시 SQT prediction 변화 (의도 설계 회피)

**작성 원칙 (CLAUDE.md 최우선-1 준수)**: 기존 GFT BEC 문헌 (Oriti, Pithis, Marchetti 등 2014–2024) 의 cosmology 결론만 인용. 새 도출/수식 유도/파라미터 fit 일체 금지. 본 문서는 *비교표* 이며 이론 도출 산출물이 아니다.

**전제 (L530 권고)**: GFT BEC 를 priori source 로 채택. SQT 22 prediction 의 운명을 L526_R6 verdict 위에 *겹쳐* 판정한다.

---

## 0. 정직 한 줄 요약

**GFT BEC 의 *기존* 문헌은 Λ 부호/유한값 자체를 priori 로 고정하지 못한다 (자유 GFT coupling 으로만 나타남). MOND 는 부재. DM 은 dust-like effective fluid 한정. 따라서 SQT 22개 중 GFT BEC 채택으로 *priori 회복* 되는 항목은 0개 — 다만 P2, P14 의 "Λ 가 양자 sector 로부터 온다" 진술이 *형식적 등가물* 을 얻는다 (경량 회복).**

---

## 1. 인용 가능한 기존 GFT BEC 문헌 결과 (필자 새 도출 0)

본 절은 모두 publicly available 결과의 *상기* 이며, 본 세션에서 새로 계산한 것이 아니다.

### 1.1 GFT BEC 의 *기존* Λ derivation
- **Gielen-Oriti-Sindoni 2014 (PRL 111, 031301; CQG 31, 245018)**: GFT condensate hydrodynamics 가 friedmann-like equation `(V'/V)² = …` 을 *재현*. 우변에 Λ 에 대응하는 항이 들어가지만, 그 *값*은 GFT action 의 cosmological-constant-type coupling (kinetic kernel 의 mass term `μ`) 으로부터 *입력 파라미터* 로 들어간다. **priori 결정이 아니다 — 1개 자유 coupling 의 phenomenological fit.**
- **Oriti-Sindoni-Wilson-Ewing 2016 (CQG 33, 224001)**: bouncing solution 에서 effective Λ 는 condensate equation-of-state 와 mode population 으로 표현. 부호/스케일 모두 free.
- **Pithis-Sakellariadou 2019 (Universe 5, 147; review)**: "Λ_eff prediction is *not* a free output of the formalism without further input"라고 명시.

→ **결론 (1)**: GFT BEC 가 *기존* 문헌 한도에서 Λ 의 정량값을 *priori* 도출한 사례는 없다. Λ 의 부호 (가속 vs 비가속) 도 mass term 부호로 좌우되어 *Son+2025 (q₀>0) 와도, LCDM 과도* 양립 가능. Λ 의 priori 잠금은 발생하지 않는다.

### 1.2 GFT BEC 의 *기존* MOND-like prediction
- **부재**. Oriti–Pithis–Marchetti 2019–2024 라인은 *homogeneous, isotropic* condensate 만 다룬다 (mean-field cosmology 한정). low-acceleration galactic dynamics 에 대한 도출은 *발표된 적 없음*. Marchetti–Oriti 2020/2021 의 perturbation 분석도 cosmological scalar perturbation 에 머문다.

→ **결론 (2)**: GFT BEC 는 MOND-like a₀ 또는 BTFR slope=4 를 *기존* 문헌에서 도출하지 않는다.

### 1.3 GFT BEC 의 *기존* dark matter prediction
- **Oriti 2017 (NJP 19, 042001)**, **Marchetti–Oriti 2021 (JHEP 02, 074)**: condensate 의 *추가* mode (non-condensate / sub-dominant population) 가 effective dust-like fluid (`w≈0`) 를 발생시킬 수 있다는 *general remark*. 정량 abundance, halo profile, 또는 cluster-galactic 분기는 도출 안 됨.
- **Gielen 2019**: anisotropic GFT condensate 가 effective curvature term 으로 작동 가능 — DM substitute 가 아니라 geometric 효과.

→ **결론 (3)**: GFT BEC 의 DM "prediction" 은 *qualitative existence statement* 수준. NFW profile, σ-사다리, BTFR 에 대한 priori 입력 없음.

---

## 2. SQT 22 prediction 과의 호환 갯수

L526_R6 verdict (Son+2025 correct 가정) 와 GFT BEC 채택을 *둘 다* 겹쳐 판정. 호환 = "GFT BEC 채택 후에도 SQT 의 정량값과 *모순 없이* 살아남는가".

| # | SQT prediction | L526_R6 verdict | GFT BEC 호환? | 비고 |
|---|---|---|---|---|
| P1 | σ_0 3-regime | DEGRADES | △ (호환 가능, 도출 부재) | GFT 는 σ_0(env) 사다리를 다루지 않음 |
| P2 | Λ = n_∞ε/c² | DIES | ○ (형식 등가물) | GFT mass term ↔ "양자 sector → Λ" *서술적* 일치 |
| P3 | BTFR slope=4 | SURVIVES | △ | GFT 는 galactic dynamics 부재 → 모순도 지지도 없음 |
| P4 | PPN γ=1 | SURVIVES | ○ | GFT mean-field 은 정적 PPN 미손상 (Marchetti–Oriti 2021 perturbation linear) |
| P5 | GW170817 c_g=c | SURVIVES | ○ | GFT condensate 는 tensor sector 비변경 |
| P6 | CMB peaks | DEGRADES | △ | GFT 의 z~1090 dynamics 는 LCDM-등가 *주장만* 존재, 정량 없음 |
| P7 | EHT shadow | SURVIVES | ○ | strong-field BH 는 GFT 영역 외 (모순 없음) |
| P8 | H(z) chronometer | DEGRADES | △ | GFT free coupling 으로 어떤 H(z) 도 fit 가능 → postdiction 강등 강화 |
| P9 | PTA GW | SURVIVES | ○ | GFT 는 nHz GW 신호 무 |
| P10 | BBN | SURVIVES | ○ | GFT 는 BBN era 비활성 가정 (Pithis-Sakellariadou 2019) |
| P11 | Casimir | SURVIVES | ○ | GFT 는 lab QFT 미수정 |
| P12 | σ_0(cosmic) identity | DIES | △ | GFT 의 H_0 도출은 자유 coupling — identity 회복 안 됨 |
| P13 | (paper §4.1 추가) | SURVIVES | ○ | low-z 정적 (요약 R6) |
| P14 | "Λ from quantum vacuum" | DIES | ○ (형식 등가물) | P2 와 동일하게 GFT mass term 서술 일치 |
| P15 | NOT_INHERITED 첫째 | N/A | N/A | |
| P16–P22 | inheritance gap | N/A | N/A | GFT 도 채우지 않음 |
| P17 | postdiction (R6) | DEGRADES | △ | |
| P18–P19 | non-prediction | N/A | N/A | |
| P20–P21 | DIES | △ | GFT 에서도 도출 부재 | |

**호환 갯수 합산** (○ + △ 모두 *모순 없음* 으로 카운트):
- ○ (능동 호환): **8개** — P2, P4, P5, P7, P9, P10, P11, P14
- △ (수동 호환, GFT 가 발언 안 함): **8개** — P1, P3, P6, P8, P12, P17, P20, P21
- N/A: 6개

→ **결론 (4)**: SQT 22 prediction 중 GFT BEC 와 *능동적으로 호환* 8개, *수동적으로 호환* 8개. **GFT BEC 채택이 SQT 의 호환 prediction 갯수를 *늘리지는 않는다*** — Son+2025 correct 만 가정한 R6 의 "8 SURVIVES" 와 정확히 동일 집합 (P3 만 능동→수동 으로 자리 이동, 능동 호환에 P2, P14 추가).

---

## 3. GFT BEC 채택 시 SQT 의 *어느* claim 이 priori 회복되는가

R6 에서 DIES 판정된 P2, P12, P14, P20, P21 중 GFT BEC 가 *기존 문헌 한도에서* 회복시키는 항목:

- **P2 (Λ_eff = n_∞·ε/c²)**:
  - GFT mass term 이 "양자 sector → 우주론적 상수항" 의 *형식적* embedding 을 제공.
  - **그러나** Λ 의 *값/부호* 은 GFT coupling 의 자유 입력. SQT 의 "n_∞·ε/c² 정량 identity" 자체는 회복 *안 됨*.
  - **회복 등급**: 형식적 (서술적) — 정량 priori 아님.

- **P14 ("Λ from quantum vacuum" 진술)**:
  - 동일하게 형식 등가. 미분형 미세조정 문제는 GFT 도 해결하지 않음 (Pithis-Sakellariadou 2019 명시).
  - **회복 등급**: 형식적.

- **P12 (cosmic σ_0 identity = 4πG/(3H_0))**:
  - GFT 는 `H_0` 를 자유 coupling 의 함수로 둠. identity 자체는 *유도되지 않는다*.
  - **회복 등급**: 0 (회복 없음).

- **P20, P21**:
  - GFT BEC 는 inheritance gap 항목에 발언 없음.
  - **회복 등급**: 0.

→ **결론 (5)**: **정량 priori 회복: 0개. 형식/서술 회복: 2개 (P2, P14).** 두 회복 모두 "Λ 가 양자 sector 에서 온다" 라는 *qualitative* 진술의 embedding 일 뿐, 값/부호/스케일의 priori 잠금은 GFT BEC 도 제공하지 않는다.

---

## 4. 종합 — L530 평가표 갱신 시사점

L530 NEW_AXIOM_SYSTEMS.md 가 후보 E (GFT BEC) 에 priori power = A 를 부여한 근거 (Oriti-Sindoni-Wilson-Ewing 2016 line) 는, *기존 문헌 정독* 결과 **A → B/C 로 하향 조정 필요**:
- A 등급은 "1 coupling 으로 phenomenology 가 *결정* 된다" 는 서사이지만, 실제 문헌에서 그 1 coupling 은 *자유 fit 파라미터* 이며 부호/스케일에 priori 잠금이 없다.
- SQT 22 prediction 의 priori 회복 갯수 = 0 (정량), 2 (형식) 는 GFT BEC 채택의 비용 (formalism 무거움, 시뮬레이션 인프라 재구축 — L530 §108 명시) 을 정당화하지 않는다.

---

## 5. 특이사항 (priori 회복) — 한 줄

**GFT BEC 채택 시 SQT 22 prediction 중 정량적 priori 회복은 0개, 형식적(서술적) 회복은 P2 와 P14 두 항목 — 둘 다 "Λ 가 양자 sector 에서 온다"는 qualitative embedding 에 한정되며 Λ 값/부호의 priori 잠금은 발생하지 않는다.**

---

*작성: L533, 단독 비교 보고. CLAUDE.md 최우선-1 준수: 기존 문헌 인용만 사용, 새 수식/파라미터/유도 0건. 인용 출처는 모두 publicly available preprints/journals (arXiv/CQG/PRL/JHEP/NJP/Universe).*
