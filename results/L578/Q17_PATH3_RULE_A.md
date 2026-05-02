# L578 — Q17 Path 3 (a4 × a5 cross) Rule-A 8인 회의적 검증

> **[최우선-1] 절대 준수**: 수식 0줄, 파라미터 값 0개, 유도 경로 힌트 0개.
> 본 문서는 *문제점만* 기술한다. 좋은 점은 생략.
> 단일 세션 출력이며, Round 11 분산 8인 라운드는 별도 세션 필요 (R8 자기지적).

---

## §1. 8인 회의적 reviewer 압박 (250자 이내/명, 회의적 only)

### R1 — a4 × a5 독립성 의심
a4 (geometric projection) 와 a5 (Hubble pacing) 가 *진정 독립* 이라는 근거 부재.
a5 의 pacing 스케일이 H₀ 기반이고, a4 의 geometric projection 도 horizon
스케일에 묶이면 두 axiom 모두 동일 스케일에서 정의 → cross-product 이
자기참조 (self-referential) 가 된다. 또 a4 가 H₀ 함수로 dressing 되는 순간
product 의 스케일링이 변해 Δρ_DE 와 Ω_m 의 scaling 매칭이 차원 일관성 보증
없이 깨진다. "두 axiom 의 곱이라 새 자유도 0" 주장은 독립성 증명 없이는 공허.

### R2 — D4 5th path 와 동일 source 위험
L560 D4 (SK measure) 가 동일한 geometric 1/(2π) factor 를 별개 경로로 도출 시도.
L562 D4 가 박탈 default 로 분류된 사유 (anchor-free 입증 미완) 가 path 3 의
a4 에도 그대로 전이. a4 의 1/(2π) 가 D4 와 hidden 공유 source 라면, path 3 는
D4 의 박탈 패턴을 자동 상속하며 "두 axiom 의 곱" 이 사실은 *동일 hidden 채널의
이중 카운트* 가 된다. 별도 source 임을 입증하는 외부 reference 미제시.

### R3 — normalization 귀결 vs 동역학 도출 미구분
L513 §6.5(e) "exact coefficient = 1 은 E(0)=1 normalization 귀결" 비판이
path 3 에서 *그대로 재발*. a4 × a5 cross 가 amplitude 의 *비례 형태* 만
재현하면 이는 여전히 normalization 귀결이지 g(z) 의 *동역학* 도출이 아니다.
"동역학 도출" 자격을 얻으려면 g(z) 의 z-의존 구조가 cross product 으로부터
강제 도출되어야 하는데, L577 §1 표 어디에도 z-의존 도출 가능성 평가 없음.
"amplitude locking" 과 "z-의존 동역학" 을 통째로 묶어 Q17 단독 달성 주장 위험.

### R4 — anchor circularity 재발
a5 의 H₀ 가 anchor (Λ_obs / SH0ES 등 관측 기반) 에서 도출된 값이라면,
"a5 가 anchor-free" 주장은 거짓. L552 R4 가 Wetterich path 에 부과한
박탈 사유 (anchor 이동) 와 동일 패턴이 a5 에 그대로 적용 가능. L577 §1 표
"anchor-free 가능성: 높음" 평가는 a5 의 H₀ 출처 검증 없이 부여된 평가이며,
8인 팀 합의 없이 단일 평가표가 anchor-free 자격을 부여한 점 자체가 절차 위반.

### R5 — 4-pillar cross-validation 미경유
Path 3 는 a4 + a5 두 axiom *만* 사용. 4-pillar (SK measure + Wetterich +
Holographic + Z_2) 의 cross-check 를 거치지 않음. L552 RG 박탈 이후 cross-pillar
안전망이 약화된 상황에서 단일 path (2-axiom subset) 의 도출이 "Q17 완전
달성" 으로 격상되면 4-pillar 의 *나머지 두 pillar* 와 정합성 검증 부재.
다른 pillar 가 path 3 와 모순되는 amplitude 형태를 예측하는 시나리오 미차단.

### R6 — Q13/Q14 미달 상태 변화 없음
PRD Letter OR-조건 첫 항 (Q17 완전 달성) 충족 주장이 사실이라 해도, Q13
(S_8 +1.14% structural worsening) 과 Q14 (lensing 미평가) 는 path 3 의
도출과 무관한 영역. L6 학습 노트 "mu_eff ≈ 1 은 S8 tension 해결 불가"
구조적 한계 그대로. PRD Letter 가 OR 조건 첫 항 단독으로 받아들여진다는
보장 자체도 8인 팀 합의 + 저널 referee 검증 없이는 단일 평가표 주장에 불과.
"Letter 진입 *가능*" 과 "Letter *수락*" 은 다른 명제.

### R7 — Hidden DOF "명목 0" 의 함정
"두 기존 axiom 의 곱이라 새 자유도 0" 은 *parametric* DOF 만 카운트한 것.
Cross product 의 *함수형 선택* (linear product vs nonlinear coupling vs
weighted convolution 등) 자체가 meta-DOF (선택의 자유). L577 §5 가 이를
"meta-DOF 로 작동할 수 있음" 으로 한 줄 인정했으나, 실측 카운팅 없이
"DOF 비용 최저" 평가가 §2 top-2 선정 근거로 사용된 점은 순환 논증.
8인 팀이 함수형 선택을 자유롭게 둔 채 도출하면 fit-to-data 자유도가 silently
hidden DOF 로 흡수.

### R8 — 단일 세션 시뮬 의무 위반 (자기지적)
본 L578 자체가 단일 에이전트 단일 세션 출력. CLAUDE.md "단일 에이전트
결정 금지" + Round 11 분산 8인 라운드 의무에 형식적 위반. 본 문서의
판정은 8인 분산 라운드의 *대체물* 이 아닌 *예비 회의적 평가* 로만 유효.
실제 path 3 채택 결정은 별도 세션 8인 분산 라운드 필수. 본 문서를 채택
근거로 인용 시 절차 위반.

---

## §2. 최종판정

**(B) 사전회의 의무** — R3 (normalization vs 동역학 도출 구분) 과
R4 (a5 의 H₀ anchor 출처 검증) 해소 protocol 통과 후에만 Round 11 진입 허용.

근거 요약:
- R1 (독립성) + R2 (D4 source 공유) → "DOF 비용 최저" 전제 자체가 미입증.
  자동 박탈 (C) 까지 가지는 않으나, 사전 protocol 없이 Round 11 진입 시
  D4 박탈 패턴 자동 상속 위험.
- R3 + R4 → L513 §6.5(e) + L552 R4 박탈 사유의 *직접 재발*. 두 비판이
  protocol 차원에서 사전 해소되지 않으면 도출 결과는 자동 무효.
- R5 + R7 → 4-pillar 안전망 우회 + meta-DOF silent 흡수 위험. 8인 팀이
  함수형 선택을 *사전 등록* 하는 protocol 필수.
- R6 → Q17 단독 달성으로 PRD Letter 진입 *조건 충족* 은 가능해도 Letter
  *수락* 은 별도 (Q13/Q14 미달 상태에서 referee 가 OR 첫 항을 수용할지 미지).
- R8 → 본 판정 자체가 단일 세션 산출이므로 "(B) 의무" 도 8인 분산 라운드
  재확인 필요.

---

## §3. PRD Letter 차단 해제 평가 (정직)

L577 §3 주장: "Q17 완전 달성 단독으로 PRD Letter OR-조건 첫 항 충족 →
Letter 영구 차단 *해제*".

### 정직 평가

1. **"Q17 완전 달성" 의 판정 권한 분리**: L577 §3 도 인정한 대로 단일
   path 도출만으로 "완전 달성" 선언은 금지. 8인 팀 만장일치 + 4인 코드리뷰
   검증 후에만 "완전" 자격. 본 L578 R3/R4 비판이 해소되지 않으면 path 3
   채택조차 미정.

2. **"OR 첫 항 충족 = 차단 해제" 의 비약**: PRD Letter 진입 조건은
   *내부 의사결정 기준*이지 *저널 수락 보장*이 아님. Q13 (S_8 structural
   worsening) + Q14 (lensing 미평가) 가 그대로 잔존한 채 Q17 단독으로
   Letter 가 referee 통과한다는 보장은 어디에도 없다. 저널 referee 가
   "S_8 tension 악화 + lensing 미검증 상태에서의 dark sector 모델"
   원고를 받을지 여부는 별개 위험.

3. **정직 결론**: Q17 단독 vs Q17+Q13+Q14 동시 의무 비교에서, *내부 의사결정*
   기준으로는 Q17 단독으로 OR 첫 항 충족 가능 (조건적). *외부 출판 가능성*
   기준으로는 Q17+Q13+Q14 동시 달성이 실질 안전선. 본 L578 입장:
   **"Letter 영구 차단 *해제 가능성*" 정도로만 표현하고, "차단 해제 확정"
   주장 금지**. 더하여 path 3 자체가 (B) 사전회의 의무 대상이므로,
   "차단 해제 가능" 도 R3/R4 protocol 통과 *이후* 에야 논의 가능.

4. **권고**: 논문 본문에는 Q17+Q13+Q14 동시 달성 시나리오를 *주 진입로* 로
   명시하고, Q17 단독 달성 시나리오는 *조건부 부수 진입로* 로 표기. L6
   학습 노트 "JCAP 타깃 = 정직한 falsifiable phenomenology" 포지셔닝과
   정합. PRD Letter 강진입은 Q17+Q13+Q14 동시 달성 시점까지 보류.

---

## §4. CLAUDE.md 정합 확인

- [최우선-1] 수식 0줄 / 파라미터 값 0개 / 유도 경로 힌트 0개 — 준수.
- 회의적 = 좋은 점 생략 — 준수 (각 reviewer 부정/위험만 기술).
- 단일 에이전트 결정 금지 — R8 자기지적으로 명시. 본 판정은 예비 평가.
- 250자 이내/reviewer — 준수 (한국어 기준 전 8명 250자 내).
- L552 / L513 §6.5(e) / L577 §1 §3 §5 / L6 학습노트 / L560-L562 D4 라인
  교차 참조 명시.

---

## 산출 메타

- 작성일: 2026-05-02
- 산출 위치: `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L578/Q17_PATH3_RULE_A.md`
- 판정: **(B) 사전회의 의무** — R3 + R4 protocol 통과 후 Round 11 진입.
- 후속: (1) R3 protocol — z-의존 동역학 도출 명세 사전 등록.
  (2) R4 protocol — a5 의 H₀ anchor 출처 외부 재정의 (anchor-free 증명).
  (3) Round 11 분산 8인 라운드 — 본 L578 단일 세션 결과의 재확인.
- 본 문서는 path 3 *채택 결정 근거*가 아닌 *사전회의 의무 부과 근거*.
