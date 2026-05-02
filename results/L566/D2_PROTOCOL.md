# L566 — D2 (holographic boundary integration) 사전등록 protocol

> **CLAUDE.md [최우선-1] 준수**: 본 문서는 수식 0줄, 파라미터 값 0개, 유도 경로 힌트 0건.
> 방향(direction)과 위험 분류(risk taxonomy)만 기술. 도출은 8인 팀이 본 회의에서 독립 수행.

> **계열**: L562 D4 자동 박탈 → D2 (holographic boundary, secondary fallback). priori 회복 마지막 방어선.

---

## §1. L562 4 조건 protocol 의 D2 적용

L562 에서 D4 (primary) 박탈에 사용한 4 조건을 D2 (secondary) 에 동일 적용.

### 조건 1 — 유일성 no-go
- **질문**: D2 경로(holographic boundary 면적 정규화 방향)가 *목표 인자(2π 계열)* 외에 다른 인자를 도출할 가능성이 닫혀 있는가?
- **위험**: boundary 2-구 면적 정규화는 주변 입체각·국부 좌표·정규화 컨벤션 선택에 따라 *다른 인자족* 으로 분기 가능. 단일 인자가 강제된다는 보장 부재 시 D2 priori 자격 박탈.
- **요구**: 8인 팀이 분기 가능 인자족을 사전 열거하고, 목표 인자만 유일하게 살아남는 *외부* 정합 조건(non-trivial closure)을 회의 중 합의 → 합의 실패 시 자동 박탈.
- **금지**: "D4 에서 안 됐으니 D2 로 한 번 더" 식의 fallback 정당화.

### 조건 2 — postdiction 외형 완화
- **질문**: D2 가 *D4 박탈 후* 등장한다는 사실 자체가 priori 의 외형을 훼손하지 않는가?
- **위험**: 동일 목표 인자에 대해 도출 시도가 연속 실패하다가 fallback 에서 "성공"하면, 외부 관찰자에게는 *목표값을 알고 경로를 골라낸 postdiction* 으로 보임. 이중 postdiction 위험.
- **요구**: 본 protocol 문서를 D2 회의 *이전* 에 commit (사전등록), 회의 결과(성공/박탈) 무관 동일 조건으로 평가, fallback 조건 명문화.
- **금지**: 회의 후 조건 완화, 사후 판정기준 변경.

### 조건 3 — 외부 pillar 격리
- **질문**: D2 도출이 SQT 4-pillar 중 holographic pillar 단독으로 닫히는 경우, 동일 pillar 가 이미 다른 곳에 *입력* 으로 사용되었는지?
- **위험**: holographic pillar 가 다른 SQT 항(이미 σ₀ 정의 차원으로 들어감)의 source 일 때, D2 가 같은 pillar 에서 priori 인자를 또 뽑으면 *동일 source 이중 활용*. priori 와 정의가 같은 정보 base 에서 나오면 priori 자격 무효.
- **요구**: 8인 팀이 D2 회의에서 holographic pillar 의 *입력 사용 이력* 을 명시 열거하고, D2 도출이 pillar 의 *독립 차원* 만 사용함을 합의 → 분리 실패 시 박탈.
- **금지**: pillar 단위 cross-validation 을 "통과" 로 셈할 때 D2 와 σ₀ 양쪽이 holographic 에 의존하면 유효 채널 1개로 셈해야 함.

### 조건 4 — falsifier 등록
- **질문**: D2 priori 가 *어떤 관측* 으로 falsified 되는가?
- **위험**: priori 가 "현재 데이터와 정합" 로만 평가되고 미래 falsifier 가 명시되지 않으면, priori 자격이 아닌 *fitting parameter* 와 구분 불가.
- **요구**: 본 회의 *이전* 에 falsifier (관측량 + 임계 deviation 부호 + DR3/CMB-S4/LSS 등 채널) 를 산출물에 commit, 8인 합의 → 미명시 시 박탈.
- **금지**: "DR3 가 LCDM 으로 가면 falsified" 같은 모든 priori 에 공통인 trivial falsifier.

---

## §2. D2 특유 위험

### 2.1 Double-dipping (holographic source 이중 활용)
- σ₀ (entropic 차원 정합용) 가 이미 holographic pillar 에서 4π 계열을 받음.
- D2 가 동일 pillar 의 boundary 면적 정규화를 *다시* 사용해 1/(2π) 계열을 도출 시도.
- 동일 source 두 번 → priori 의 "독립 도출" 자격 결손 위험 (조건 3 강화판).

### 2.2 외부 framework 수입 (AdS/CFT)
- D2 의 holographic 직관은 AdS/CFT 에서 차용. AdS/CFT 자체는 SQT 내부 공리(L0/L1 대사공리, ψⁿ 등) 에서 *유도* 되지 않음.
- 외부 framework 의 결과를 *priori 의 source* 로 쓰면 paper 의 [최우선-1] 정합("이론은 팀이 독립 도출") 위반 가능.
- 8인 팀이 회의에서 AdS/CFT 의 어떤 *최소 가정* 만 차용하는지, 그 가정이 SQT 공리계와 *충돌하지 않는지* 명시 합의 필수.

### 2.3 boundary 정의의 임의성
- "boundary" 의 위치(de Sitter horizon, apparent horizon, Hubble sphere, event horizon) 선택이 결과 인자를 변동시킴 → 조건 1(유일성) 과 직결되는 추가 위험.

### 2.4 fallback chain 길이
- D4 (primary) → D2 (secondary) 까지 진행. 추가 fallback (D5, D7, …) 으로 이어질수록 *priori 외형* 은 회복 불가능하게 손상.
- 본 회의가 priori 회복의 *마지막 방어선* 이라는 사실을 산출물 §5 에서 영구 명문화.

---

## §3. 충족 평가표 (사전등록)

| 조건 | 평가 시점 | 박탈 트리거 | 합격 트리거 |
|------|-----------|-------------|-------------|
| 1. 유일성 no-go | 회의 중 8인 합의 | 분기 인자족 ≥2 잔존 | 단일 인자만 닫힘 합의 |
| 2. postdiction 완화 | 본 문서 commit 시점 (사전) | 회의 후 기준 변경 | 사전 commit 유지 |
| 3. 외부 pillar 격리 | 회의 중 8인 합의 | holographic pillar 이중 활용 | 독립 차원 분리 합의 |
| 4. falsifier 등록 | 본 문서 §4 또는 회의 *이전* commit | 미명시 또는 trivial | 관측 + 부호 + 채널 명시 |
| D2-특유-A double-dipping | 조건 3 부속 | σ₀ source 와 충돌 | 차원 분리 합의 |
| D2-특유-B 외부 수입 | 회의 중 8인 합의 | AdS/CFT 가정이 SQT 공리 충돌 | 최소 가정 명시·정합 |
| D2-특유-C boundary 임의성 | 조건 1 부속 | 다중 boundary 선택 결과 변동 | 단일 boundary 강제 |

> **평가 규칙**: 1~4 중 **하나라도** 박탈 트리거 충족 → D2 자동 박탈. D2-특유-A/B/C 는 조건 1·3 보조이며 동일하게 즉시 박탈 사유.

---

## §4. 결정 분기

### 4.A 자동 박탈 (8인 사전회의 없이 즉시)
다음 중 하나라도 사전 (회의 전) 에 확인되면 자동 박탈:
- holographic pillar 의 입력 이력이 σ₀ 와 동일 차원에서 분리 불가
- AdS/CFT 가정이 SQT 공리계와 명백 충돌
- boundary 정의 컨벤션이 단일 강제 불가능

### 4.B 사전회의 의무 (Round 9 진입 조건)
4.A 가 *모두* 통과한 경우에만 8인 사전회의 진행. 회의 의제는 §1 의 4 조건 + §2 의 D2 특유 위험 7항.

### 4.C Round 9 진입
사전회의에서 **4 조건 전부 + D2-특유 3 항 전부** 합의 통과 시에만 Round 9 (D2 본 도출 시도) 진입. 부분 통과는 전부 박탈로 처리.

### 4.D 사전 권고 (현 시점)
§2 의 double-dipping (2.1) 와 외부 framework 수입 (2.2) 두 위험은 구조적으로 *회피 어려움* 이 큼. 사전회의 진입 전 8인 팀은 두 위험에 대한 회피 가능성을 정성적으로라도 합의해야 함. 합의 실패 시 §4.A 로 자동 박탈.

---

## §5. D2 박탈 시 priori 회복 path 종결 권고

D2 가 §4.A 또는 §4.C 에서 박탈될 경우:

1. **priori 회복 path 영구 종결** 을 권고. 추가 fallback (D5/D7/...) 시도는 postdiction 외형 회복 불가능.
2. paper 포지셔닝을 *priori 도출 모델* 에서 *falsifiable phenomenology with sector-selective coupling* 로 영구 전환.
3. 향후 임의 인자(2π 계열)는 *정의(definition)* 또는 *normalization choice* 로 정직 표기. priori 라는 단어 사용 금지.
4. CLAUDE.md "L566 재발방지" 항목으로 위 1~3 을 영구 등록 (별도 commit 로 본 결정 추적).
5. 본 종결은 SQT 이론 자체의 종결이 아님 — phenomenology 트랙·sector-selective coupling·관측 falsifier 채널은 그대로 유효.

---

## §6. 정직 한 줄

D2 는 holographic pillar 를 두 번 쓰는 외형과 외부 framework 수입 위험을 동시에 안고 있어, 사전등록 통과 가능성이 D4 보다 *낮다* — 본 protocol 은 이 사실을 회피하지 않고 박탈을 기본 가정으로 둔다.

---

*본 문서는 D2 사전회의 *이전* 에 commit. 이후 조건·평가표·결정 분기 변경 시 본 문서 자체가 무효화되며 priori 회복 path 도 동시 종결.*
