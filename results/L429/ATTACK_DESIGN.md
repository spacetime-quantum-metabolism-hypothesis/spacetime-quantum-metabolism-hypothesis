# L429 ATTACK_DESIGN — #17 Jacobson δQ=TdS NOT_INHERITED 공격면 (8인)

> 본 문서는 8인팀 토의에서 *자연 발생*한 분업 결과만 기록한다. 사전 역할 지정 없음.
> CLAUDE.md [최우선-1] 준수: 수식·파라미터값·유도 경로 힌트 일절 포함하지 않음. *방향*과 *현상명*만 기재.

## 0. Scope

- 대상: paper/base.md §6.1 row 17 (Jacobson `δQ = T dS` 미상속) — L404 NEXT_STEP §3.4 에서 "어느 5번째 축 후보(Causet meso / GFT)도 단독 회복 못함" 확정.
- 잔존 근원: SQT 의 axiom 1 (물질 흡수, KMS 평형 채널) 과 Clausius 등식의 *구조적 비등가성*.
  - KMS 는 *정상상태 detailed balance* 를 정의 — 시간 비가역성 없음.
  - Clausius 는 *준정적 가역 경로 위에서의 열·온도 전환* 을 정의 — 시간 방향성 있음.
- L404 D5 attack 재방문: "GFT 등재 후에도 #17 잔존" 의 근원이 *공리 1 의 KMS 형식*에 있는지, 아니면 *온도 정의 (Unruh-like)* 의 부재인지를 분리.

## 1. 8인팀 자율 분담 결과 (토의 자연 발생)

| 공격면 ID | 공격 내용 (방향만) | 근거가 되는 정직 의문 |
|---|---|---|
| **A1** | "axiom 1 의 KMS 평형은 *국소 Rindler horizon* 의 *비평형 entropy flux* 를 정의하지 못한다. Jacobson 1995 의 핵심은 *국소 가속관성계*에서의 entropy 변화율이지, *정상상태 흡수율* 이 아니다." | 두 평형 개념 (정상상태 vs 준정적) 의 카테고리 차이 |
| **A2** | "SQT 는 *온도* 를 *온도장* 으로 도입한 적 없다 — Hawking/Unruh 채널이 axiom 1–6 안에 없다. 'T' 가 정의되지 않은 framework 에서 'TdS' 는 정의 불가." | base.md §2.1 에 온도 axiom 부재 |
| **A3** | "엔트로피 정의가 *흡수량 카운팅* 으로 환원되어 있다 (axiom 1 + axiom 5). Bekenstein-Hawking 면적-비례 entropy 와 *수치적 일치* 만 있을 뿐, 그 *통계역학적 미시 origin* 이 SQT 에 없다." | L86 `S_BH/N_q ≈ 27` 의 자연성 *역방향*: SQT 가 BH entropy 를 *예측* 하는 채널 부재 |
| **A4** | "axiom 4 가 OPEN 인 동안에는 metric 이 emergent — local Killing horizon 자체가 정의되지 않는다. Jacobson 도출은 *background metric 위에서* 진행되므로 framework 순환 위험." | 5번째 축 결정 *전*에는 #17 도출 시도 자체가 부적절 |
| **A5** | "L404 가 GFT/Causet 단독 회복 실패를 확정한 것은 *외부 5번째 축이 #17 을 풀지 못함* 만 보였을 뿐이다 — *내부* 채널(axiom 1 의 비가역 확장 또는 axiom 6 의 H-theorem 추가) 시도는 한 번도 안 했다." | "외부 축 추가" 와 "내부 axiom 미세조정" 은 별개 채널 |
| **A6** | "δQ=TdS 는 등호이지만 SQT 의 inheritance 는 *부등호 방향* 도 정직 보고해야 한다 — 흡수+생성 균형이 *항상* Clausius 우변보다 작거나 같은지, 큰지 모른 채로 'NOT_INHERITED' 라고만 적혀있다." | 정직 stance 강화: NOT_INHERITED 의 *부호 미정* 도 별도 명시 필요 |
| **A7** | "L86 (S_BH/N_q ≈ 27) 은 *cross-validation* 일 뿐 derivation 이 아니다. 비례계수 27 의 정체가 *order-unity dimensionless artifact* 인지, *27 = 27 ± 1 의 자연 상수* 인지 분리 보고 누락." | base.md row 13 의 'Λ 자릿수 일치' 와 동일한 함정: *consistency* 를 *prediction* 으로 오인 |
| **A8** | "axiom 1 의 흡수 채널이 *정보* 도 같이 흡수하는지 — 즉 black hole information paradox 와의 정합성 — 이 §6 NOT_INHERITED 표에 *공란*. #17 잔존이 더 큰 정보 paradox 잔존을 가릴 우려." | NOT_INHERITED 가 1건 잔존이 아니라 *정보 보존* 까지 묶이면 다건일 수 있음 |

## 2. 8인 합의 — 공격면 우선순위

1. **A2 (온도 부재)** — "framework 에 'T' 가 어떻게 들어오는가" 를 먼저 정직하게 답하지 않으면, *어떤* entropic derivation 시도도 임시방편(ad hoc Unruh 빌려쓰기) 이 된다. **A2 가 가장 근본**.
2. **A1 (KMS≠Clausius)** — A2 에 *부분* 답을 주는 채널 (KMS 온도 = Tolman 온도 = Hawking 온도 의 식별) 이 *내부 일관성* 을 갖는지 확인. 답이 "예" 면 #17 부분 회복 길 열림. "아니오" 면 axiom 추가 *필요* 가 명백해짐.
3. **A5 (내부 axiom 미세조정 미시도)** — 본 L429 의 NEXT_STEP 후보. *외부* 5번째 축이 아니라 *내부* axiom 1 또는 axiom 6 의 비가역 확장 (H-theorem 채널) 으로 #17 회복 가능성 검토.
4. **A4 (axiom 4 OPEN 의 순환 위험)** — 5번째 축 결정 전 #17 도출 시도는 *순환* 또는 *조건부* 결과만 산출 가능. paper 에 명시 필요.

A3, A6, A7, A8 은 부수적 정직 disclosure 채널로 §6 self-audit 보강 (paper 작업 영역).

## 3. 다음 단계 권고 (NEXT_STEP 으로 인계)

- **방향만 제시**: 공리 1 (정상상태 흡수) 과 공리 6 (선형 유지) 사이에 *비가역 정보 흐름* 을 정의하는 *내부* 채널이 존재하는지. 이는 통계역학 분야의 H-theorem 계열 논의가 닿는 곳.
- 만약 그러한 내부 채널이 존재한다면, *Clausius 로 가는 매핑* 이 가능한지를 판정. 매핑 성공 = #17 의 *조건부* PARTIAL 격상.
- 매핑 실패 = #17 의 NOT_INHERITED 가 *근원적* 임을 정직히 추가 명시 (현 base.md §6.5(e) footnote 강화).
- **결정 유보 권고**: L429 단일 세션에서 결론 낼 수 없음. 4인팀 실행은 *시도* 결과 (PASS / FAIL / 조건부) 만 산출.

## 4. 8인 자율 분담 후 합의 발견

- "5번째 축 결정과 *직교*" (L404 §6.5(e)) 는 옳지만 **불완전**: 5번째 축이 *외부* 채널이라는 *전제*에서만 직교. *내부* axiom 미세조정 채널 (A5) 을 열면 직교 해소 가능.
- "L86 cross-validation" 은 *방향* (SQT 가 BH entropy 와 모순 없음) 만 확인, *역방향* (SQT 가 BH entropy 를 *예측*) 은 미확인. paper §4 / §6 에 분리 표기 권고.
- **A2 (온도 부재)** 는 본 framework 의 *비가시* 결함 — 8인 토의에서 가장 늦게 떠오름. 이는 base.md 가 'T' 를 *암묵* 사용 (KMS 온도, Tolman 온도) 했기 때문. paper revision 시 axiom 화 또는 정직 disclosure 필요.
