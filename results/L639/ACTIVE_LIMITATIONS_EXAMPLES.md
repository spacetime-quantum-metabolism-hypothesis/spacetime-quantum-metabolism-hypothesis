# L639 — Active Limitations 본문 예시 (paper plan §6 only)

> **본 문서는 PAPER_PLAN_V3.md §6 의 본문 예시 텍스트** 만을 담는다.
> **실제 paper / claims_status / 디스크 파일 어떤 것도 edit 하지 않는다.**
> **수식 0줄, 파라미터 값 0개, 새 prediction 0건.**

---

## §1. §6.1 ~ §6.7 본문 예시 (각 paragraph 250자 이내)

### §6.1 — 4 priori path 박탈 (L549/L552/L562/L566)

> 본 framework 가 a priori 도출 채널을 통해 background 함수형을 *유도* 하지 못한 사례는
> 우리 진행 기록(L549, L552, L562, L566)에 4건 누적되어 있다. 각 시도는 변분원리, 대칭성 인자,
> 차원분석, 한계 정합성을 차례로 동원했으나, 데이터 적합 단계에서 채택된 함수형을 *예측* 하는
> 데에는 모두 실패했다. 우리는 이 4건을 본 모형이 phenomenological 단계에 머물러 있음을
> 보여주는 가장 직접적인 internal 증거로 본문에 명시한다.

### §6.2 — fabrication 90%

> 사후 자체 점검(L564)에서 우리는 본 모형의 background 함수 형태가 데이터 적합 결과를
> 보고 *역설계* 된 비율을 약 90% 수준으로 평가한 바 있다. 이는 제안된 함수형이 이론으로부터의
> 강제(forced) 결론이라기보다, 가용 dataset 의 잔차 패턴에 대한 적응적 선택이었음을 의미한다.
> 본 한계는 모형의 falsifiability 자체를 부정하지는 않으나, 현재 보고되는 적합도 개선의
> 해석에는 반드시 이 fabrication ratio 가 함께 첨부되어야 한다.

### §6.3 — 회의적 4중 0/4 (L578/L587/L588/L589)

> 우리는 자체 회의적 점검을 4 라운드(L578, L587, L588, L589) 시행했고, 각 라운드는
> 독립적인 falsification 기준을 통과했는지를 묻는 4개의 질문을 부과했다. 결과는 4/4 모두
> *통과 실패* 였다. 어떤 단일 라운드에서도, 본 모형이 LCDM 대비 데이터-주도 우월성을
> 회의 기준을 만족시키며 보이지 못했다. 이 0/4 결과는 본문 conclusion 의 톤을 직접
> 결정하며, 우리는 이 사실을 §6 에 그대로 인용한다.

### §6.4 — hidden DOF 9–13

> 본 모형의 background 함수와 회의 보정 항을 모두 풀어보면, 데이터 적합 과정에서 사실상
> 고정·선택된 hidden degree of freedom 의 수가 약 9에서 13개 사이로 추정된다. 명목상의
> free parameter 보다 훨씬 큰 이 수는, 함수형 선택, mask 경계, 정규화 규약, prior 폭 등에서
> 누적된다. 우리는 본문에서 이 hidden DOF 추정을 정직히 보고하며, AICc/BIC 패널티가
> 명목 자유도만 반영한다는 한계도 함께 명시한다.

### §6.5 — mass redef 영구 종결 (L582)

> L582 에서 우리는 mass scale 재정의 경로를 *영구* 종결했다. 해당 경로는 매번 새로운 적합
> 시도마다 mass 재정의를 통해 잔차를 흡수하는 구조였고, 이는 falsifiability 의 점진적
> 침식이라는 반복 패턴을 만들었다. 본 종결 결정은 회의적 단계에서 자체 부과된 제약이며,
> 본문 §6 에는 종결의 사유와, 종결 이후로 새로운 mass 재정의가 도입되지 않았음을
> 검증 가능한 형태로 기록한다.

### §6.6 — 외부 검증 의무 (multi-session, L599/L615)

> 본 보고에서 inferred 결과는 단일 세션 내부 self-consistency 만을 통과했다. L599 와 L615 에
> 명시된 바와 같이, 우리는 *동일 데이터 / 동일 코드 / 다른 세션 / 다른 검토자* 네 축 모두에서
> 외부 multi-session 재현이 통과되기 전까지는 어떠한 결과도 확정 결론으로 제시하지
> 않는다. 본 §6 의 외부 검증 의무는 paper 의 conclusion 강도를 강제로 제한하는 절차적
> 게이트로 취급된다.

### §6.7 — paradigm shift 박탈 risk (Phase 31–40)

> 마지막으로, Phase 31–40 의 결과 패턴을 종합할 때, 본 framework 가 paradigm shift 수준의
> 결론을 주장할 권리는 *현 시점 박탈* 되어 있다. background 함수가 fabrication ratio 가 높고,
> a priori 유도 4/4 실패, 회의 0/4, hidden DOF 9–13, 외부 검증 미통과 — 이 다섯 조건이
> 결합된 상태에서 paradigm shift 표현은 학술적 정직성과 충돌한다. 본문 §6 는 이 박탈을
> 해제하기 위해 구체적으로 무엇이 더 필요한지의 조건도 함께 명시한다.

---

## §2. 어휘 가이드 (L591 / L596 / L635 sync)

본 §6 에서 사용 *허용* 되는 표현:

- "현 시점 박탈된다" / "현 단계에서 정당화되지 않는다"
- "phenomenological" / "data-adaptive"
- "fabrication ratio" / "hidden degree of freedom"
- "외부 multi-session 재현 미통과"
- "회의 라운드 0/4"
- "a priori 유도 채널 미작동"

본 §6 에서 사용 *금지* 표현 (L591/L596/L635 합의):

- "paradigm shift" / "revolutionary"
- "novel mechanism" / "from first principles" (a priori 유도 미작동 상태에서)
- "tension resolved" (외부 검증 통과 전)
- "predicts" — 이미 데이터에서 보인 결과를 사후 fitting 으로 재현한 경우
- "universal" — sector-selective embedding 미확정 상태에서

이 어휘 가이드는 L591 (limitations 분량 확대), L596 (정직 톤),
L635 (positioning) 와 상호 sync 된 상태로 유지된다.

---

## §3. 8인 Rule-A 의무

본 §6 본문 예시 7 paragraph 는 *plan 문서 내 예시* 일 뿐이다. 실제 paper §6 본문에
진입시키려면 다음 절차가 *필수* 다:

1. **Rule-A 8인 순차 리뷰** — 7 paragraph 각각에 대해 8인 팀이 다음 5축을 점검:
   - (a) 사실관계(L 번호와 실제 사건 일치 여부)
   - (b) 어휘 가이드(§2) 준수 여부
   - (c) 250자 분량 제약 준수
   - (d) hidden DOF / fabrication ratio 등 수치적 진술의 출처 명시 여부
   - (e) paper 의 다른 섹션(§3 results, §5 discussion)과의 톤 정합성
2. **8인 합의** — 7/8 이상 합의가 있는 paragraph 만 paper 본문 진입 후보로 승격
3. **승격 후** — 별도 commit 으로 PAPER_PLAN_V3.md §6 → paper §6 반영
4. **이 문서(L639) 자체는 plan 보조자료로 남기며 paper 본문에 직접 복사 금지**

본 §3 의무는 [최우선-1] 및 L591/L596/L635/L599/L615 의 누적 제약을 그대로 계승한다.

---

## §4. 정직 한 줄

> 본 §6 예시들은 우리가 *지금까지 실패한 모든 것* 을 paper 가 외면하지 않게
> 만들기 위한 장치이며, 이 한계 7항이 해소되기 전까지 본 framework 의 결론
> 강도는 phenomenological 수준을 넘을 수 없다.
