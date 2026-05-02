# L434 ATTACK_DESIGN — 8인 공격 (Q canonical 4-동률 미결: A/C/D/E)

**세션**: L434 (독립, L403 follow-up)
**날짜**: 2026-05-01
**정직 한 줄**: L403 의 4-동률 (A action/ℏ, C Joos-Zeh, D phase-space cells, E info levels) 을 *적대적* 으로 공격해 단일 canonical 정의를 데이터 + 이론 정합성으로 결정하기 위한 8인 공격 채널 설계. 본 문서는 *방향* 만 제공, 수식·수치 0개.

## CLAUDE.md 준수 자가 점검

- **[최우선-1] 방향만, 지도 금지**: 본 문서는 8 attack channel 의 *영역* 만 명시. 어느 정의가 winner 인지 결과를 사전 지정하지 않음. 어떤 수식·파라미터·수치도 적지 않음.
- **[최우선-2] 팀 독립 도출**: 8인이 채널 분담을 자율 결정. 본 문서는 채널 *주제* 만 제시.
- **LXX 공통 (역할 사전 지정 금지)**: A1–A8 은 자연 발생 attack 영역. 8인의 사전 역할 배정 아님.
- **AICc 패널티 명시**: canonical 결정 시 effective DOF +0/+1 분류를 attack 결과로 강제. 약한 결정 (DOF +1) 은 PARTIAL 유지 결론.
- **시뮬레이션 우선 / 코딩 버그 의심**: 본 세션은 attack 결과 *해석* 단계. 추가 simulation 발생 시 4인 코드리뷰 선행.

## 공격 표적 (L403 미결 항목)

L403 NEXT_STEP §3 의 결정 기준 표에서 **K1 PASS + K2/K3/K4/K5 미결정** 인 4 후보:

- **A** action/ℏ — K2 best, K3/K4/K5 미답
- **C** Joos-Zeh decoherence — K4 strongest (lab falsifiability), K2/K3 mid
- **D** phase-space cells — K2/K3/K4/K5 모두 mid 또는 weak
- **E** info levels — K2 weak, span_decades clip artifact, K3 미답

K3 (axiom 도출) 이 본 attack 의 *주공격면*.

## 8 attack channel — 방향만

### A1 — *Joos-Zeh standard 매칭* (decoherence rate 표준 일치성)
- decoherence rate 는 lab 측정 기준의 *de facto 표준* (Joos-Zeh 1985, Zurek 2003 review).
- 4 후보 중 lab decoherence rate 와 *직접* 동일한 dimensional form 인 것은 무엇인가?
- 공격: 비-C 후보가 표준과 어긋나면 lab 검증 채널 차단.

### A2 — *axiom-derivability* (SQT 공리 직접 도출)
- L0 ("관측은 dimensionless 비") + L1 (대사항) 만으로 4 후보 중 어느 것이 *추가 가정 없이* 자연 도출되는가?
- 공격: axiom 외부 도입 (예: thermal momentum 가정, infinite well 가정) 이 필요한 후보 탈락.

### A3 — *parsimony 재평가* (span 의 정직성)
- L403 R4 가 지적한 E 의 span_decades=302.3 clip artifact 보정 후 ranking 재정렬.
- A 의 best span (48.9 decade) 우위가 보정 후에도 유지되는지, 또는 C/D 와 격차 좁아지는지 공격.

### A4 — *prefactor O(1) 자유도* 분리 검사
- 4 후보 각각의 prefactor=1 고정이 *결과* 를 임계 시스템에서 흔드는가?
- 공격: prefactor 0.5 vs 2 swap 시 임계 시스템 (BEC, nanoparticle 1e7 amu) classification 가 깨지는 후보는 *fragile*. 표준 prefactor 가 *역사적으로 합의된* 것은 C (Joos-Zeh 1985, Schlosshauer 2007 review) 뿐.

### A5 — *generality 검사* (시스템 보편성)
- D 의 3D 가정, E 의 infinite well 가정처럼 *시스템 형태* 에 종속된 후보는 보편 정의 자격이 약하다.
- 공격: BEC (1D), 2D 박막, 광자 시스템 추가 시 어느 후보가 *형태 무관* 으로 작동하는가.

### A6 — *collapse model bridge* (B 탈락 후 잔재)
- L403 K5 에서 B (PD) 만 collapse 모델에 직결됐고 B 는 K1 탈락. 잔존 4 후보 중 GRW/CSL 와 *간접* 매핑 강도 비교.
- 공격: bridge 가 가장 약한 후보 (E?) 탈락.

### A7 — *information-theoretic 자기 정합성*
- E (info levels) 가 SQT 의 *대사 = 정보 갱신* 해석과 정합적인가, 아니면 thermal 가정으로 인해 *대사항* 과 분리되는가.
- 공격: E 가 SQT 의 자기-해석 채널 위배 시 탈락. 동시에 C (decoherence = 정보 누수율) 의 정보론적 정합성 강화 가능.

### A8 — *paper 등급 영향* (canonical 결정의 격상 효과)
- 각 후보 채택 시 paper/base.md PARTIAL → PASS_STRONG 격상 가능 여부.
- 공격: 채택해도 등급 변동이 0 인 후보 (즉 외부 가정 잔존) 는 실용 가치 없음.

## DOF 비교표 — 4 후보 × 8 채널

| ID | A1 표준매칭 | A2 axiom | A3 parsim | A4 prefactor | A5 general | A6 collapse | A7 info정합 | A8 등급 |
|----|-----------|---------|----------|-------------|-----------|------------|-----------|--------|
| A action/ℏ | indirect | TBD | best | safe (Bohr) | OK | weak | weak | conditional |
| C Joos-Zeh | **direct** | TBD | mid | **standard** | OK | mid | **strong** | strong |
| D phase-space | indirect | TBD | mid | shape-dep | weak (3D) | weak | weak | weak |
| E info levels | indirect | TBD | weak (clip) | shape-dep | weak (well) | weak | TBD | weak |

(본 표는 L403 결과 + A1–A8 채널 *질적* 평가. 정량 ranking 은 NEXT_STEP §2 8인팀 합의 산출물.)

## 공격 우선순위

1. **A1 + A2 동시 적용**: Joos-Zeh standard 매칭 + axiom 도출 가능성 — 4 후보 중 *동시* 통과 가능한 것.
2. **A4 + A5**: prefactor / shape 종속성으로 fragile 후보 절단.
3. **A6 + A7**: 잔존 후보의 collapse / information bridge 강도.
4. **A8**: 최종 격상 효과 검증.

## 산출물 인계

- 본 ATTACK_DESIGN 은 8인 공격 *방향* 만 제공.
- 다음 산출물 NEXT_STEP.md 가 8인 공격 *결과 평가 기준* 을 5축 (physical motivation, decoherence rate 표준, parsimony, axiom-derivability, lab falsifiability) 으로 정리.
- 최종 4인 실행 (REVIEW.md) 이 physical 우선 selection 을 통한 단일 canonical 결정.

## 한계 / 미해결

- 본 attack 은 *질적*. 정량 simulation 은 L403 결과 (15 시스템 × 5 정의 grid) 외 추가 미실시.
- A2 (axiom 도출) 은 8인 *이론* 검토에 의존 — simulation 으로 결정 불가.
- prefactor 자유도 (A4) 의 정량화는 별도 LXX 세션 권고.
