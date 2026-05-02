# L428 ATTACK_DESIGN — 8인팀 reviewer 공격 설계

**주제**: paper/base.md §6.1.2 row #16 "Volovik 2-fluid analogue 미상속 (NOT_INHERITED)" 가 §6.1.2 row #22 "5 program 구조적 동형 PASS 0/5" 의 어느 부분을 약화시키는가.
**목표**: Volovik 미상속 단일 항목이 5 program 동형 narrative 전체에 대한 reviewer 비판 채널로 어떻게 확장되는지 정리.
**방법**: 8인 자율 토의 (Rule-A). 역할 사전 지정 없음. 자연 발생한 비판 채널 8개 정리.

---

## 8인팀 자율 발생 비판 채널

### 비판 #1 — "5 program 동형" 의 Volovik 의존도
5 program (Padmanabhan / Volovik / Causet / Jacobson / GFT) 중 Volovik 은 *유일한*
응집물질-우주론 analogue 이다. Padmanabhan 은 thermodynamic, Causet 은 discrete,
Jacobson 은 entropic, GFT 는 second-quantized. Volovik 이 빠지면 "공간 BEC 응집체"
axiom 의 *실험실 검증 가능 analogue* 채널 자체가 사라진다.

### 비판 #2 — axiom 4 의 5번째 축 결정과 무관한 독립 약점
§6.1.2.1 의 "5건 (#16, #18, #19, #20, #21) 이 GFT/BEC 미채택 연쇄" 라는 root-cause
서사는 #16 을 GFT 결정 종속 항목으로 묶지만, **Volovik 분석은 GFT 와 독립 channel**
(He-3/He-4 superfluid 수치 실험은 GFT 채택 여부와 무관). #16 을 GFT 결정에 묶어
"한 번에 회복 가능" 으로 처리하는 것은 reviewer 가 거부한다.

### 비판 #3 — "공간 BEC 응집체" 광고와 Volovik 부재의 모순
SQT axiom 1–4 는 "vacuum 이 condensate 처럼 행동" 을 핵심 narrative 로 사용한다.
응집물질에서 condensate 는 *반드시* normal/superfluid 두 phase 를 가지며 Volovik
프로그램은 이를 시공간 emergence 에 매핑한 가장 발달한 frame 이다. SQT 가
Volovik 매핑 부재를 인정하면 "BEC condensate" 라는 단어 사용 자체가 *비유 수준*
으로 격하된다.

### 비판 #4 — n field 의 phase 구조 부재
SQT 의 n field (공간 양자 밀도) 는 단일 scalar 로 운영되며, normal-component /
superfluid-component 분리가 axiom 에 없다. Volovik 의 핵심은 두 component 의
존재 자체이므로, "trivial 동형 명시 또는 인용 삭제" (paper L936) 외 선택지가
좁다는 reviewer 공격이 가능.

### 비판 #5 — Z₂ vs U(1) symmetry 불일치 (#19 와 같은 root, 다른 표현)
GFT BEC 부재의 root cause 인 "Z₂ ≠ U(1)" 은 Volovik 의 He-3 (B-phase, complex
order parameter, U(1)/SO(3) 류) 와 직접 충돌. SQT 의 Z₂ scalar n field 는
Volovik 두-phase 구조를 자연 운반하지 못한다. #18/#19 와 sister gap.

### 비판 #6 — Roton minimum / second sound 부재
Volovik 의 정량 검증 가능 신호 (roton spectrum, second sound mode, vortex
quantization) 는 모두 SQT axiom 1–4 에 *예측 채널이 부재*. 즉 Volovik 미상속은
단순 인용 누락이 아니라 *예측력 누락* 이며, 5 program 동형 PASS 0/5 의 핵심 약점.

### 비판 #7 — Vacuum energy hierarchy 문제 회피 불능
Volovik 프로그램의 가장 강력한 결과는 "응집체 ground-state 에너지가 거시
관측자에게 0 으로 보이는" 메커니즘 (Volovik 2003 §29) 이다. SQT 의 Λ origin
CONSISTENCY_CHECK (§5.2 circularity) 약점은 Volovik 동형이 상속되었으면 부분적
으로 회복 가능했을 것이다. **#16 미상속이 §5.2 circularity 와 cross-link**
되면서 약점 두 개가 결합한다.

### 비판 #8 — "구조적 동형" 라는 용어의 형식 정의 부재
paper §6.1.2 row #22 는 "구조적 동형" 을 정의 없이 사용. Volovik 미상속 사례는
이 용어가 단순 *narrative parallel* 인지 *category-theoretic isomorphism* 인지
판별 불능임을 드러낸다. reviewer 는 "5 program PASS 0/5" 표기 자체에 대해
"무엇이 PASS 의 기준인가?" 라는 형식 공격을 수행한다.

---

## 8인팀 합의 결론

- Volovik NOT_INHERITED #16 은 *단순 인용 결여* 가 아니라 SQT n field 의
  phase 구조 부재 + Z₂ scalar 한계 + 응집체-emergence 매핑 부재 의 복합 약점.
- #22 (5 program 동형 PASS 0/5) 의 "동형" 정의가 추가 검증 없이는 진단 불가.
- 회복 경로: (a) trivial 동형 명시 + 인용 격하, (b) n field 에 두-component
  구조 추가 + Volovik 매핑 시도, (c) Volovik 인용 자체를 paper 에서 제거.
- 회복 실패 시 권고: §6.1.2 row #16 caveat 강화 + row #22 의 "0/5" 가
  *narrative 0* 인지 *formal 0* 인지 명시.
