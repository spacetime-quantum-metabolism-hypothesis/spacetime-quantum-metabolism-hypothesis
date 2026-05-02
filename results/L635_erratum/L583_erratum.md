# L583 Erratum — Q17_R3R4_PROTOCOL.md 어휘 정정 매핑

**대상 산출물**: `results/L583/Q17_R3R4_PROTOCOL.md`
**위반/주의 건수**: 5건 (PRD Letter target 1건, PASS_STRONG schema 잔존 2건, priori 폐기 맥락 1건, falsifier 어휘 1건 — L596 §2 권고 sync)
**원 산출물 본문 edit**: 0건. 본 erratum 만 추가.
**Cross-ref**: L591 §8 어휘 가이드, L596 §1~§2 표.

---

## 라인별 정정 매핑

### L583 lines 33-34 (PRD Letter target)
- **현재 어휘**: "PRD Letter 진입 조건 재고 / PRD Letter 진입 조건이 더 멀어졌음"
- **정정 어휘 (재독해)**: "내부 OR-게이트 재고 / 내부 OR-게이트 양쪽 모두 추가 박탈 (출판 시도 영구 금지 sync)"
- **카테고리**: PRD Letter target
- **메모**: §6 결론 톤 수정. "더 멀어졌음" → "양쪽 모두 추가 박탈" 로 *내부 게이트* 어휘에 정합.

### L583 lines 49-50 (PASS_STRONG schema 잔존)
- **현재 어휘**: "PASS_STRONG enum 영구 0 명시화" / "PASS_STRONG 인스턴스 0…"
- **정정 어휘 (재독해)**: enum 키 자체는 schema 호환 위해 유지 (변경 불요). 단 *헤드라인 어휘* 사용 영구 금지 명시 + `current_count: 0` 영구 불변 주석 — L591 §8 와 정합.
- **카테고리**: PASS_STRONG (schema 잔존 OK, 헤드라인은 위반)
- **메모**: 본 라인 자체는 schema 잔존 맥락이므로 본문 변경 불요. claims_status.yaml 주석 보강 (L596 §3 옵션 C) 권고만 별도.

### L583 line 77 (priori 폐기 맥락)
- **현재 어휘**: "priori 도출 / derived a priori" — mass redef 종결로 도출 주장 근거 소멸
- **정정 어휘 (재독해)**: 그대로 *폐기 맥락* 유지 (인용 형태). paper 본문 0회 등장 sync 명시 보강
- **카테고리**: priori derivation (단, 폐기 맥락 — 위반 아님, sync 보강만)
- **메모**: 폐기 맥락 인용은 L591 §8 위반 아님. 본 라인 자체는 변경 불요.

### L583 line 93 (PASS_STRONG schema 잔존)
- **현재 어휘**: "PASS_STRONG enum 항을 유지하되 current_count: 0…"
- **정정 어휘 (재독해)**: 변경 불요 (schema 호환 잔존 OK, L591 §8 정합)
- **카테고리**: PASS_STRONG (schema 잔존 OK)
- **메모**: lines 49-50 와 동일 원칙.

### L583 §4 (falsifier 어휘 — L596 §2 권고)
- **현재 어휘**: "falsifier 등록" / "사전등록 falsifier"
- **정정 어휘 (재독해)**: "출판 무관 plan 단계 falsifier (사전등록 — 내부 락인)"
- **카테고리**: 사전등록 어휘 (paper-bound 함의 분리 필요)
- **메모**: 사전등록 자체는 plan 단계로 유지. 단 *출판과 분리* 한정자 명시 필요.

---

## 정직 한 줄

L583 의 5건은 PRD Letter target 본문 1건 (lines 33-34, §6 결론) + PASS_STRONG schema 잔존 2건 (변경 불요) + priori 폐기 맥락 1건 (변경 불요) + falsifier 사전등록 어휘 1건. 실제 어휘 교체가 필요한 것은 §6 결론 톤 + §4 falsifier 한정자 명시 — 나머지는 schema 호환/폐기 인용 맥락으로 L591 §8 와 이미 정합.
