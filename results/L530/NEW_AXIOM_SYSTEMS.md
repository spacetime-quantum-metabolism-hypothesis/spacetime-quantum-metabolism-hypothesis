# L530 — New Axiom System Brainstorm (정직 한 줄 모드)

목적: Son+25 age-bias 정합 + 기존 SQT 6-axiom 세트 폐기 가능 가정 하에서, 완전히 새로운 출발점 6 후보의 *priori 도출 power*, 기존 prediction 생존도, hidden DOF 를 정직 평가.

> ⚠️ 본 문서는 brainstorm 단계 (방향만). 수식/파라미터 값/유도 경로 힌트는 의도적으로 배제 — CLAUDE.md [최우선-1] 준수. 8인 팀이 이후 단계에서 독립 도출.

---

## 평가 축 (3축)

- **(1) 기존 SQT predictions 생존도**
  - SQT 가 산출한 핵심 결과 묶음 = {DESI w_a<0 부호, 저z BAO 압력, 챔피언 ratio-기반 g(z), Q93/Q95 amplitude-locking, S_8 (해결 못함), Cassini γ-1 (구조적 통과 여부)}
  - 점수: A = >75% 살아남음 / B = 30~75% / C = <30%
- **(2) priori 도출 power 회복 가능성**
  - 정의: amplitude (예: ν, α_Q, β, f_1, c0, amp 류) 가 *데이터 fit 없이* 단일 axiom 으로부터 결정되는가
  - 점수: A = 1개 axiom → amplitude 결정 / B = axiom + 1 보조 가정 / C = posterior 유도만 가능
- **(3) hidden DOF 최소성**
  - 정의: axiom 외에 추가로 가정해야 할 자유 함수/파라미터 수 (낮을수록 우수)
  - 점수: A = 0~1 hidden / B = 2~3 / C = ≥4

---

## 후보 평가

### A. Holographic-only (Planck information 단일 axiom)
- **핵심**: 시공간 sector 의 정보용량이 면적-bound 하나로 닫힘. 'tHooft-Susskind 단일 공리화.
- **(1) 생존도**: B. ratio-기반 g(z) 는 horizon 재정의로 자연스럽게 살아남고 amplitude-locking 도 면적/부피 비로 설명 시도 가능. 그러나 SQT 의 "metabolism" (재생/소멸 비대칭) 은 axiom 추가 없이 부호를 못 내놓음 → w_a<0 비자명.
- **(2) 도출 power**: B. Hubble 면적 ↔ Λ 의 유효 amplitude 1개는 axiom 으로부터 도출 가능. 시간 의존 (`wa`) 는 area-flow 추가 가정 필요.
- **(3) hidden DOF**: B (2~3). 면적 cutoff scale, IR/UV 분리, holographic surface 선택 (apparent vs Hubble vs event).
- **종합**: B/B/B — 안전하지만 SQT *고유 부호 예측력* 이 전수 보존되진 않음.
- **특이사항**: Cassini PPN 자동 통과 (지역 면적 정보 ≪ 우주론 변화) — 이건 강점.

### B. Two-fluid (Volovik analog: superfluid + normal phase)
- **핵심**: 물리적 진공이 두 상 (초유체 + 정상). 두 상의 비율이 시공간/물질 sector 의 분기 결정.
- **(1) 생존도**: A. 기존 SQT "재생/소멸" 비대칭은 두 상 사이 상전이 매개로 자연 재현. ratio g(z), amplitude-locking, w_a<0 모두 normal-phase fraction 의 단조 진화로 살릴 여지 큼.
- **(2) 도출 power**: B. 임계온도 / 상전이 scale 1개를 condensed-matter 유추로 고정하면 amplitude 도출 가능. 그러나 "유추 → 우주론" 전이는 추가 정합성 가정 필요.
- **(3) hidden DOF**: B/C 경계. order parameter, healing length, 두 상의 EOS 가 각각 추가됨.
- **종합**: A/B/B — SQT prediction 보존 최강. priori power 는 Volovik analog 의 진정성에 의존.
- **특이사항**: S_8 tension 해결 가능성이 다른 후보 대비 가장 높음 (normal-fraction 이 성장에도 직접 작용 — μ_eff ≠ 1 자연 발생).

### C. Causet meso (causal set coarse-grained, L379 계열)
- **핵심**: 이산 인과집합 + meso-스케일 평균화. 시공간이 점-사건 그래프의 통계적 극한.
- **(1) 생존도**: B. ratio g(z) 의 원천을 sprinkling 밀도의 cosmic time 의존으로 해석 가능. 그러나 SQT 의 *amplitude-locking* (예: Δρ_DE ∝ Ω_m) 은 구조적 도출이 자명하지 않음.
- **(2) 도출 power**: A 잠재력. Sorkin-style Λ ~ √N 변동은 amplitude 를 1 axiom 으로 고정 (Poisson sprinkling rate). w_a 부호도 sprinkling rate 의 시간 progression 으로 결정될 수 있음.
- **(3) hidden DOF**: B. coarse-graining scale, sprinkling 분포, manifoldlike 회복 조건.
- **종합**: B/A/B — *priori power 회복* 측면에서 가장 매력적. SQT 의 SQT-스러움(metabolism)은 일부 손실.
- **특이사항**: Son+25 age-bias 와의 정합은 매우 자연스러움 (이산 시간 → age 정의 변경). L379 의 meso-coarse 결과를 그대로 inherit 가능.

### D. Entropic emergent (Verlinde area-entropy)
- **핵심**: 중력/시공간이 entropy gradient 의 emergent 결과. 1 axiom = "면적-엔트로피 = 정보".
- **(1) 생존도**: C. SQT 의 *부호 예측* (w_a<0) 이 Verlinde 원형에서 자동 보장되지 않음. ratio g(z) 모양도 entropic force 모형에서 재현하려면 추가 가정 필요.
- **(2) 도출 power**: B. dark sector amplitude 를 horizon 엔트로피로 1축 도출하는 시도는 가능하나 (Verlinde 2016) DESI w_a<0 부호는 별도 ansatz 필요.
- **(3) hidden DOF**: A/B. 매우 minimal — 면적 scale 1개. 그러나 중력 자체가 emergent 라는 가정 가격이 큼.
- **종합**: C/B/A — minimal 하지만 SQT 핵심 부호 예측을 잃음.
- **특이사항**: H0 tension 에는 의외로 약함 (Verlinde 2016 비판 다수).

### E. GFT BEC (Group Field Theory Bose-Einstein condensate, hexagon Hamiltonian)
- **핵심**: 시공간이 GFT 양자의 condensate. hexagon (그래프 1-vertex) Hamiltonian 이 동역학 결정.
- **(1) 생존도**: A. condensate 의 배경 evolution → Friedmann 유사 방정식 자연 발생, ratio g(z) 와 amplitude-locking 양쪽이 condensate fraction 의 고유 진화로 흡수 가능. w_a<0 도 condensate depletion 부호로 자연.
- **(2) 도출 power**: A. 1개 GFT coupling → background amplitude 결정 (Oriti-Sindoni-Wilson-Ewing 2016 line). Phenomenology 가 양자중력 1차 원리에서 도출되는 가장 명료한 후보.
- **(3) hidden DOF**: B/C. group manifold 선택, mode 수 (j), interaction kernel, condensate 의 mean-field 가정 → DOF ≥ 3.
- **종합**: A/A/B — *priori power* 와 *prediction 생존* 둘 다 강함. 가격은 GFT formalism 의 무거움.
- **특이사항**: 양자 정보 < GFT < SQT 위계가 자연스러워, 후보 F (양자정보 단일 source) 와 nested.

### F. 양자 정보 단일 source
- **핵심**: 시공간/물질/Λ 모두 단일 양자 정보 channel 의 부산물. 1 axiom = "정보 = 존재".
- **(1) 생존도**: B. ratio g(z) 와 metabolism 은 channel capacity 의 시간 진화로 reframe 가능. 그러나 부호와 amplitude 모두 channel 구조 추가 가정 필요.
- **(2) 도출 power**: A 잠재력 (이상). 가장 야심찬 priori — 정보 단위 선택만 axiom. 그러나 실제로 amplitude 까지 따려면 channel 구조 (qubit count, decoherence rate) 가 hidden 로 들어옴.
- **(3) hidden DOF**: C. channel 차원, encoding map, observer/시스템 분리, 시간 emergence 메커니즘.
- **종합**: B/A/C — *철학적 priori power* 최강이지만 hidden DOF 가 cost. 단일 axiom 처럼 보이지만 실제로는 채널 구조가 숨어있음.
- **특이사항**: 후보 D (Verlinde) 와 후보 E (GFT) 의 상위 추상화. 둘 중 하나로 환원될 위험 있음 — 독립 후보로 유지 가치 의문.

---

## 종합 비교표

| 후보 | (1) SQT 생존 | (2) priori power | (3) hidden DOF | 총평 |
|-----|------------|------------------|---------------|------|
| A. Holographic-only | B | B | B | 안전, 평범 |
| B. Two-fluid (Volovik) | A | B | B | SQT 정신 보존 최강 |
| C. Causet meso | B | A | B | priori 도출 1순위 |
| D. Entropic (Verlinde) | C | B | A | minimal 하지만 부호 잃음 |
| E. GFT BEC | A | A | B/C | 야심차고 강력, 비싸다 |
| F. 양자 정보 단일 source | B | A* | C | priori 환상, hidden 비용 큼 |

`A*` = 명목상 A 이나 hidden DOF 로 인해 사실상 B.

---

## 1차 권고 (정직)

1. **추천 우선 후보 = E (GFT BEC) + C (Causet meso) 병행**.
   - E 는 priori power 와 SQT 생존 둘 다 A. C 는 priori power 가 단독 A 이며 L379 결과 inheritance 가능.
   - 두 후보는 morphism (GFT graph ↔ causal set) 으로 연결 가능 → 한 쪽이 죽어도 다른 쪽으로 회피 가능한 구조.
2. **차순위 = B (Two-fluid Volovik)**.
   - SQT prediction 생존 최강 (A). priori power 는 condensed-matter 유추가 cosmic 으로 진정 이전될 수 있는가에 달림.
3. **삭제 권고 = D, F**.
   - D (Verlinde) 는 SQT 핵심 부호 (w_a<0) 가 axiom 으로부터 자명하게 나오지 않음 → SQT 대체 후보로서 동기 약함.
   - F (양자정보 단일) 는 priori power 가 환상에 가까움. hidden DOF 가 axiom 1개에 모두 흡수되었다고 주장하나, channel 구조가 사실상 4~5개 자유도. E 또는 D 로 환원될 위험.
4. **A (Holographic-only)** 는 *baseline / null 후보* 로 유지. 모든 후보가 holographic bound 와 정합이어야 하므로 비교용 axiom 으로 활용.

---

## 특이사항 (정직 한 줄)

- **C (Causet) + L379 결과**: L379 의 meso-coarse 결과가 이미 존재한다면, C 는 *처음부터 새로 시작* 이 아니라 *재상속* 후보 — brainstorm 라기보다는 promotion. 8인 팀에 이 사실을 공지할 것 (priori 도출 검증 시 L379 의 영향력을 control 해야 함).
- **B (Volovik) 의 S_8 잠재력**: 기존 SQT 가 풀지 못한 S_8 tension 은 normal-phase fraction 이 성장 ODE 에 직접 들어가는 구조에서 자연 해결 가능. 만약 Phase 5 에서 이 점이 검증되면 후보 B 가 일등.
- **E (GFT) 비용**: GFT formalism 채택 시 코드/시뮬레이션 인프라 전면 재구축. 현 simulations/l* 트리는 ODE/CPL 기반 — GFT condensate hydrodynamics 로 전환 시 Phase 5/6 의 검증 자산 일부 폐기 위험. 비용-편익 사전 평가 필수.
- **F 의 nested 문제**: 후보 F 는 후보 D 또는 E 의 상위 메타 axiom 일 가능성이 높음. 만약 F 가 D 또는 E 로 환원된다면 독립 후보 자격 상실 — 8인 팀 첫 회의에서 환원 가능성 점검 필요.
- **모든 후보에 공통 부담**: Cassini |γ−1|<2.3e-5 자동 통과는 후보 A, D, C 에서 자연. 후보 B, E, F 는 dark-only embedding (C10k 류) 또는 disformal screening 추가 가정 필요 — L4 이래 누적된 "background-only 로 S_8 못 푼다" 교훈 (CLAUDE.md L5/L6 재발방지) 을 다음 axiom 에 강제할 것.
- **"새 axiom" 약속의 함정**: 6 후보 중 정말로 *완전히 새로운* 출발점은 E 와 C 정도. A/D/F 는 기존 SQMH 논쟁사에서 이미 등장한 형태 (Verlinde 비판, holographic 한계). 진짜 신규성을 원한다면 E + C + B (Volovik) 의 조합만 유지 추천.

---
끝.
