# base.l20.command.md — 8인 리뷰 비판 수용 재건

> 작성: 2026-04-12
> 목적: L19 8인 외부 리뷰의 비판 4건을 정면 수용, 각 gap을 독립적으로 해소
> 원칙: LXX Command 공통 필수 원칙 전체 적용 (CLAUDE.md).

---

## L19 리뷰 비판 요약

| 항목 | L19 자체 등급 | 리뷰 실제 등급 | 핵심 비판 |
|------|-------------|-------------|---------|
| B = 2π/ln(2) | A | B | "4 독립 경로"가 동일 가정의 재서술 |
| A₂ = 2 | A | C | orientation reversal → A₂=2 연결 불투명 |
| S_cl = π | A | C+ | TFT 이론 미명시, n=0 근거 없음 |
| 전체 A | A | C+ | 물리적 연결 (Euclidean → Lorentzian) 없음 |

---

## L20 Phase 구조

### Phase 1: B의 독립성 감사 (8인, 5회)

**목표**: "4 독립 경로"가 진짜 독립인지 감사.

제공 정보:
- B = 2π/ln(2)의 기존 4경로 원문
- 감사 질문: "각 경로의 가정 목록을 명시하라. 공유된 가정이 있는가?"

수렴 기준:
- 각 경로의 전제 목록 명시
- 공유 전제가 있으면: 실제 독립 경로 수 = ?
- 독립 경로 수 ≥ 2이면 B등급 유지, = 1이면 강등

---

### Phase 2: A₂=2 독립 재유도 (8인, 10회)

**목표**: orientation reversal → A₂=2의 논리 경로를 처음부터 명시적으로 재구성.

비판 수용:
- 이전 논증은 "Z_{+1}=Z_{-1} → A₂=2" 연결이 불투명
- normalization convention 의존성 가능성

제공 정보 (최소):
- EE2 공식의 A 위치: A = A₂ × e^{-S_cl}
- 관측값: A = 0.089 ± 0.037
- 질문: "A₂를 결정하는 물리적 원리는 무엇인가? normalization convention과 무관하게."

금지:
- orientation reversal 힌트 제공 금지
- 이전 결론 사전 제시 금지

수렴 기준:
- A₂=2의 convention-independent 도출 경로 확립 시 A등급
- 실패 시 "A₂는 자유 매개변수" 로 솔직히 기록

---

### Phase 3: S_cl=π — TFT 명시 + n=0 정당화 (8인, 10회)

**목표**: 두 개의 구체적 gap 해소.

**Gap 1**: Z(RP⁴) = (-1)^{∫w₂²}는 어떤 이론에서 오는가?
- 가설 A: topological gravity with signature term
- 가설 B: d=4 bosonic SPT (Chen-Gu-Liu-Wen 2013)
- 가설 C: pin⁻ cobordism invariant (Kapustin et al. 2015)
- 작업: 정확한 참조 이론 확정, 공식 유도 명시

**Gap 2**: S_cl = π + 2πn에서 왜 n=0?
- 질문: n=0이 물리적으로 선택되는 이유
- 후보: dilute gas approximation, semiclassical limit, holography

수렴 기준:
- Gap 1 해결: 정확한 TFT와 공식 도출 명시
- Gap 2 해결: n=0의 물리적/수학적 정당화

---

### Phase 4: 물리적 연결 (Euclidean → Lorentzian) (8인, 5회)

**목표**: 가장 근본적 비판 대응.

비판: "왜 Euclidean S⁴/RP⁴의 위상수학이 오늘날 우주의 dark energy 상태방정식을 결정하는가?"

제공 정보:
- EE2 공식은 Lorentzian H(t)의 함수
- 이론 유도는 Euclidean S⁴에서 수행됨
- 질문: "이 연결의 물리적 메커니즘은?"

작업:
- 표준 QFT 교과서에서 Euclidean → Lorentzian 연결
- 우주론에서 instanton → 포텐셜 기여의 표준 경로
- EE2 공식에서 이 경로가 어떻게 cos 항을 생성하는가

수렴 기준:
- 표준 QFT/우주론 교과서 수준의 경로 명시 시 통과
- 실패 시 "Euclidean → Lorentzian 연결 미확립" 솔직히 기록

---

### Phase 5: 전제 목록 감사 (4인 코드리뷰 형식, 1회)

**목표**: "0 free parameters" 주장의 실제 전제 목록 작성.

작업:
- B 도출의 전제 목록
- A₂=2 도출의 전제 목록
- S_cl=π 도출의 전제 목록
- 각 전제가 A1+A2 공리에서 도출되는가, 아니면 추가 가정인가?

결과물:
- 전제 목록 (자유 매개변수와 동등한 것 포함)
- 수정된 "자유 매개변수 수" 주장

---

### Phase 6: 결론 (base.l20.result.md)

| 항목 | L19 등급 | L20 수정 등급 | 근거 |
|------|---------|-------------|------|
| B | A | ? | Phase 1 결과 |
| A₂ | A | ? | Phase 2 결과 |
| S_cl=π | A | ? | Phase 3 결과 |
| Euclidean→Lorentzian | 미검토 | ? | Phase 4 결과 |
| 자유 매개변수 수 | 0 | ? | Phase 5 결과 |

**원칙**: 등급이 낮아지면 솔직하게 낮춰 기록. 결과 왜곡 금지 (CLAUDE.md).

---

## 실행 순서

1. Phase 1: B 독립성 감사 (빠름)
2. Phase 2: A₂=2 재유도 (핵심)
3. Phase 3: TFT + n=0 (핵심)
4. Phase 4: 물리 연결 (근본)
5. Phase 5: 전제 감사 (마무리)
6. Phase 6: 결론

---

## 성공 기준

**최선**: 모든 gap 해소 → 진짜 A등급 확정
**현실적**: 일부 gap 해소 + 남은 gap 정직 기록 → 논문의 "한계" 섹션 작성
**최소**: gap 목록 명확화 → 다음 연구 방향 확정

결과가 L19보다 낮은 등급으로 수정되더라도 이것이 과학적 진보.

---

*작성: 2026-04-12. 즉시 실행 대기.*
