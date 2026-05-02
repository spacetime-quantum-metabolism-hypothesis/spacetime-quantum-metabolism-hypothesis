# L648 — External Review Templates

본 문서는 L620 외부 검증 path 1/2/3 을 *사용자가 즉시 사용 가능* 한 prompt template 모음.
[최우선-1] 절대 준수: 수식 0줄, 파라미터 값 0개. Template only.

배경: L620 path priority
- Path 1 (LLM cross-validation): 사용자 외부 의뢰
- Path 2 (third-party human review): 사용자 외부 의뢰
- Path 3 (time-separated self-review): 다음 세션 자연 발생

---

## §1 Template 1 — LLM cross-validation (Path 1)

대상: 다른 LLM (GPT / Gemini / 다른 Claude 버전 / Mistral 등)
조건: 본 SQT 결과 *비공개 상태* — axiom + 평가 대상만 노출

```
[Template 1] LLM cross-validation prompt
==========================================
당신은 우주론 + galactic dynamics 전문 평가자다. 다음 SQT 6-axiom 만 보고
나머지 결과 / 산출물 / paper plan 은 *전혀 보지 않은 상태* 로 평가하라.

[여기에 axiom 1-6 + B1 (basic claim) 을 사용자가 paste]

다음 paradigm shift 후보를 *결과 미인지* 상태에서 평가하라:

  1. A3 + Time emergent (t parameter 적출 가능성)
  2. Bootstrap (axiom → self-consistency closure)
  3. Self-incompleteness (multi-session 의무 구조)
  4. Scope axiom (적용 범위 자기 정의)

각 후보에 대해 *진정성 grade* (S/A/B/C/D/F) 부여 + 회의적 압박:

  - 본 SQT framework 외부 framework 차용 (string theory / LQG / CDT
    등) 발견 시 [최우선-1 = "방향만, 지도 금지"] 위반 명시
  - 좋은 점 / 가능성 / 응원 멘트 *전부 생략*
  - 박탈 trigger 만 식별 — "이 후보는 다음 사유로 박탈" 형식
  - SQT 자체 6-axiom 이외 가정 발견 시 즉시 KILL flag
  - 8인 reviewer 시뮬 형식 (Reviewer 1 ~ 8 각자 박탈 시도)

출력:
  - 후보별 grade + 박탈 trigger list
  - 8인 합의 (S/A/B/C/D/F)
  - 본 평가가 SQT framework 에 cherry-pick 되었는지 자체 점검 1줄
```

---

## §2 Template 2 — Third-party human review (Path 2)

대상: 외부 우주론 / QFT / 양자정보 연구자 (포닥 이상)
조건: NDA 권고. paper plan v3 (L634) 첨부 가능.

```
[Template 2] Third-party human review request
==============================================
SQT (Spacetime Quantum Theory) framework 의 다음 4 항목에 대한
*회의적* 검토를 의뢰드립니다. 본 검토는 paper 제출 전 외부 sanity
check 목적이며, NDA 조건으로 진행 부탁드립니다.

첨부:
  - paper plan v3 (L634)
  - 100+ 산출물 인덱스 (L600 / L622 / L624 / L647)
  - 6-axiom + B1 sheet (별첨)

검토 항목:

  1. Paradigm shift 후보 4건
     - A3 + Time emergent
     - Bootstrap
     - Self-incompleteness
     - Scope axiom
     각 후보의 *진정성* (외부 framework 차용 여부, axiom 일관성)

  2. 4 priori path 박탈 사유 (L549 / L552 / L562 / L566)
     박탈 정당성 — "박탈됐어야 하는데 살아남은" path 식별

  3. Fabrication 90% disclosure (L564)
     Disclosure 충분성 — 추가로 disclose 했어야 하는 항목 식별

  4. Hidden DOF 9-13 평가
     적절성 — DOF 수 / 종류 / 물리적 motivation

검토 형식:
  - 각 항목별 *박탈 trigger* 식별 (살리는 논거 생략)
  - 좋은 점 / encouragement 전부 생략
  - "이 paper 은 다음 사유로 reject 추천" 형식 환영
  - 익명 평가도 가능 (사용자가 anonymise 후 reflect)

기간: 2주 권장. NDA 위배 시 사용자 직접 책임.
```

---

## §3 Template 3 — Time-separated self-review (Path 3)

대상: 다음 세션 (1주 / 1달 후) 의 본인 (Claude or 사용자)
조건: 현 세션 (2026-05-02) 결과 *결과 인지 lapse* 후 재평가

```
[Template 3] Time-separated review (next session)
====================================================
본 prompt 는 2026-05-02 세션 결과를 *결과 인지 lapse* 후 재평가
용도. 최소 1주 / 권장 1달 경과 후 다음 prompt 로 시작:

"본 세션 (2026-05-02 base) 산출물을 *결과 인지 lapse* 상태에서
회의적 재평가하라. paper plan v3 (L634) + 산출물 인덱스
(L600 / L622 / L624 / L647) 정독 후 수행."

재평가 대상:

  1. Paradigm shift 4 후보 진정성
     - 1주 / 1달 후 봐도 동일 grade 유지되는가?
     - 시간 경과로 박탈되는 후보 식별

  2. 박탈 4 path 정당성 (L549 / L552 / L562 / L566)
     - 박탈 사유가 시간 경과 후에도 유효한가?
     - 부활 후보 식별

  3. Positive 자산 정직성 (★★★★★+)
     - 별점 인플레이션 의심 항목 식별
     - 강등 권고 list

  4. 새 angle 후보 (Phase 41-46)
     - 시간 경과 후 떠오른 새 angle
     - 기존 candidate 와 중복 여부 확인

판정 기준:
  - 본 세션과 *다른 결론* 도달 시 cherry-pick 입증
  - 본 세션과 *동일 결론* 도달 시 robustness 확인
  - 어느 쪽이든 정직 기록

회의 압박:
  - "1주 전의 너는 흥분해서 ★★★★★+ 줬을 수 있다" 자가 의심
  - "1달 후의 너는 sober 하게 ★★★ 로 강등할 가능성" 인정
```

---

## §4 사용자 사용 가이드 — 어느 template 부터?

권장 순서 (사용자 시간 / 비용 고려):

  1. **Template 3 먼저** (cost: 0, 시간: 1-4주 wait)
     - 가장 cheap, 가장 자연스러움
     - 시간 경과만으로 cherry-pick 자체 검출 가능

  2. **Template 1 다음** (cost: 저, 시간: 1-3일)
     - 다른 LLM API 호출만으로 가능
     - GPT-4 / Gemini / 다른 Claude 버전 추천
     - axiom + 후보 list 만 노출 (결과 비공개)

  3. **Template 2 마지막** (cost: 고, 시간: 2주+)
     - 외부 인간 연구자 cost / NDA 부담
     - paper 제출 직전 final sanity check 용도
     - Template 1+3 통과 후에만 진행 권고

조합 권고:
  - Template 3 (1주) → Template 1 (병렬) → Template 2 (final)
  - 하나라도 박탈 trigger 발견 시 paper 제출 보류 + L549/552/562/566 path 중 부활 검토

---

## §5 8인 Rule-A 의무 — Template 자체 합의

본 template 자체가 paradigm-shift 외부 검증 channel 의 핵심 도구.
따라서 template *자체* 는 Rule-A 8인 reviewer 합의 대상.

8인 검토 항목:

  1. Template 1 — LLM cross-validation
     - axiom-only 노출 충분성
     - 결과 leakage 위험 점검
     - 8인 reviewer 시뮬 형식 적절성

  2. Template 2 — Third-party human
     - NDA 조항 충분성
     - 박탈 trigger only 형식 적절성
     - 4 항목 cover 완전성

  3. Template 3 — Time-separated
     - Lapse 기간 (1주 vs 1달) 적절성
     - Cherry-pick 자체 검출 mechanism 신뢰도

  4. §4 사용 가이드 우선순위
     - Cost / 시간 trade-off 정당성
     - 조합 권고 (3 → 1 → 2) 합리성

8인 합의 결과:
  - 본 template 적용 전 사용자 명시적 승인 필요
  - 합의 미달 항목 발견 시 본 문서 v2 작성

(8인 reviewer 시뮬 본 문서 발행 전 미수행 — L648 후속 task 로 분리)

---

## §6 정직 한 줄

본 L648 template 자체 *외부 검증 부재 상태*. Template 효과성은 path 1/2/3 실제 실행 후에만 검증 가능.

---

산출 시각: 2026-05-02
Locale: L648
연관: L549 / L552 / L562 / L566 / L600 / L620 / L622 / L624 / L634 / L647
