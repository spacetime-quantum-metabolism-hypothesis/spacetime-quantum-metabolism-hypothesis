# L346 NEXT_STEP — 비단조 prediction 강도 회복 또는 정직 격하

## 결정 트리
L346 REVIEW J1: "대부분 fit". 다음 두 경로 중 택일.

### 경로 A — 정직 격하 (보수, 즉시 실행 가능)
1. Paper Sec 3, Sec 5 의 "비단조 *예측*" 표현 검색·교체.
   - "predict" → "is consistent with" / "accommodates" / "is observed and
     compatible with the 4 pillars".
2. Sec 6 limitations 추가 (12 → 13):
   - "13. σ_0(z) non-monotonicity is data-driven; the 4 pillars permit but
     do not predict the sign change. Theory-prior strength: low (L346)."
3. Sec 7 future work 에 P17 Tier B (V(n,t) full derivation) 우선순위 격상.
4. 다음 SYNTHESIS 에서 등급 dial -0.005 ~ -0.010 반영.

비용: 본문 수정 1-2 시간. 위험: 거의 없음. JCAP 수용 영향: 중립~+1%.

### 경로 B — Prediction 강도 회복 시도 (적극, 수일~수주)
P17 Tier B 완수가 핵심 게이트. 단계:

1. **Pre-registration lock-in (DR3 unblinding 전 필수)**
   - OSF 저장소에 다음을 timestamp 등록 (수치 lock 금지 — 정성 형상만):
     - σ_0(z) 가 *부호 변화* 를 가짐 (Y/N).
     - 극값 위치 z_* 의 *허용 구간* (이론적 도출 후만, 데이터 fit 금지).
     - 4 pillar 중 *어느* pillar 가 이 형상을 강제하는지 명시.
   - 등록 미완 상태로 DR3 unblinding 후 비단조 주장 시: 자동 post-hoc.

2. **Pillar 별 derivation 보강 (방향만 — 수식 금지)**
   - RG saddle pillar: saddle structure 가 *부호 변화* 를 강제하는 조건 식별.
     "허용" 에서 "강제" 로 격상 가능한지 8인 토의.
   - Holographic pillar: boundary entropy bound 와 σ_0 sign 의 연결 가능성 탐색.
   - Z_2 pillar: 대칭점 주변 even 구조에서 *변곡 위치* 가 자연 z_* 가 되는지 점검.
   - a4 / 4번째 pillar: L337 OPEN 인 5번째 pillar 후보 탐색 (emergent metric
     micro origin). 이 pillar 가 z_* 를 dimensional 하게 예측하는 영역 진단.

3. **Counterfactual 시뮬 (코딩 버그 우선 의심 원칙 준수)**
   - 4 pillar 중 1 개씩 끈 mock 으로 σ_0(z) 가 단조로 회귀하는지 직접 시뮬.
   - 시뮬 실패 시 4인 코드리뷰 우선 (역할 사전 지정 금지). 물리 해석은
     코드 검증 후.

4. **L345 결과 회수 후 통합**
   - L345 의 proper ln Z 결과가 비단조 우세 (Δ ln Z > +2.5) 면 J2 재판정.
   - inconclusive (|Δ ln Z| < 1) 또는 단조 우세면 경로 A 자동 채택.

비용: 1-3 인주. 위험: P17 Tier B 가 또 미완으로 끝나면 격하만 추가.

---

## 즉시 (이번 주) 실행 권고

D1. **paper draft 본문 검색 — "predict" 단어 전수조사** (1 시간):
- σ_0 비단조 관련 모든 "predict" 표현을 약화어로 1차 교체.
- 변경분 git diff 로 timestamp 보존.

D2. **L67 → L346 추적성 부록 (Appendix C)** (2 시간):
- L67 발견 → L68 robust 확인 → L334 pillar 4 격하 → L346 진단 의 chain
  을 reviewer 가 직접 확인할 수 있게 명시. 정직 트레이스가 acceptance 보호.

D3. **σ_0(env) ↔ σ_0(z) mapping 점검** (반나절):
- L67/L68 의 σ_0(env) 비단조와 BAO/BB 의 σ_0(z) 비단조가 동일한 자유도인지
  확인. 다른 자유도라면 본 round 결론 강화 (4 pillar 와의 거리 더 큼).
- 동일 자유도라면 L5 alt-20 14-cluster drift 1자유도와 합쳐 효과적
  *단일 phenomenological parameter* 로 정리 가능.

D4. **P17 Tier B 진척 audit** (1 시간):
- L338 가 정의한 V(n,t) derivation gate 의 현재 상태를 단일 페이지로 정리.
- "미완" 이면 그 사실 자체를 limitation 13 으로 본문에 등록.

---

## 측정 가능한 게이트

다음 SYNTHESIS round 진입 전 Y/N:

- [ ] paper 본문 "비단조 predict" 표현 전수 약화.
- [ ] Appendix C 추적성 chain 작성.
- [ ] σ_0(env) ↔ σ_0(z) mapping 1 페이지 노트.
- [ ] P17 Tier B 진척 한 줄 진단 (미완/부분/완료).
- [ ] L345 proper ln Z 결과 회수 (inconclusive/non-mono win/mono win).
- [ ] 등급 dial 변경 권고 (보수 -0.005 vs 적극 -0.015 vs 회복 +0.005) 결정.

---

## 절대 하지 말 것 (CLAUDE.md 재확인)

- σ_0(z) 의 구체적 함수형 / 극값 위치 수치 / 진폭 값을 본 NEXT_STEP 에 기재.
- 데이터 보기 전 lock 없이 "4 pillar 가 비단조를 예측" 식 표현을 paper 에
  추가 또는 유지.
- L67 데이터 fit 발견 사실을 "이론 도출" 로 retro-frame.
- pillar 격하 회피 목적의 narrative 보정.

---

## 한 줄 요약

> **경로 A (정직 격하) 즉시 실행, 경로 B (prediction 회복) 는 P17 Tier B 완수에 의존, DR3 unblinding 전 pre-reg lock 이 게이트.**
