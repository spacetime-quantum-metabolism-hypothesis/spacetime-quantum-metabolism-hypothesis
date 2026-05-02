# L384 ATTACK DESIGN — Wetterich LPA' Truncation (Independent)

**Date**: 2026-05-01
**Session**: L384 (independent of L383)
**Topic**: Wetterich functional renormalisation group, second-order derivative truncation (LPA'), with comparison against the L383 LPA result.

---

## 0. 최우선 원칙 준수 선언

본 Command 는 **방향만 제공**한다. 수식, 파라미터 값, 유도 경로 힌트는 한 줄도 포함하지 않는다.
L383 의 LPA 결과(고정점 위치, critical exponents, 수치값) 는 본 문서에서 인용하지 않는다.
8인 팀은 본 방향만 듣고 LPA' 도출을 **완전 독립**으로 수행한다.
위반 판정 시 세션 결과 전면 무효.

---

## 1. 탐색 방향 (이름만)

### 1.1 이론 프레임
- **Wetterich exact renormalisation group equation** (functional flow of effective average action)
- **Local potential approximation extended (LPA')** — 두 번째 차수 derivative expansion
- **Wave-function renormalisation Z_k** 의 scale dependence 도입

### 1.2 도출 대상 (수식 금지, 이름만)
- **Anomalous dimension** η — wave-function renormalisation 의 logarithmic flow 로부터
- **Non-trivial fixed point (NGFP)** 위치 — dimensionless coupling 공간 내
- **Critical exponents** — fixed point 주변 stability matrix eigenvalues

### 1.3 비교 대상
- L383 의 LPA 결과 (별도 세션, 본 문서 비공개)
- 두 truncation 의 **fixed point 좌표 이동량**, **critical exponent 수정량**, **η 의 자기무모순성**

### 1.4 SQMH 정합성 채널 (방향만)
- Asymptotic safety 시나리오에서 효과적 RG 흐름이 우주론적 dark sector phenomenology 에 남기는 흔적
- L2 R2 C23 재발방지 항목과의 부호/등급 정합성 확인

---

## 2. 팀 구성 (역할 사전 지정 금지)

### 8인 이론 팀 (Rule-A)
- 인원: 8명
- **역할 사전 배정 없음**. Wetterich FRG, derivative expansion, asymptotic safety, 수치 RG flow, 우주론 정합성 등 영역에 대해 자율 분담.
- 토의 중 자연 발생하는 분업만 인정. "η 담당", "FP 담당" 식 사전 지정 금지.

### 4인 코드리뷰 팀 (Rule-B, 수치 검증 단계)
- 인원: 4명
- **역할 사전 배정 없음**. RG flow ODE 수치, 고정점 root-finder, stability matrix 수치, plot/검증 스크립트 등 자율 분담.

---

## 3. 진행 단계

1. **독립 도출**: 8인 팀이 LPA' 의 구조와 η, NGFP, exponents 를 방향만 듣고 자체 유도.
2. **수치 검증**: 4인 코드리뷰 팀이 도출 결과의 RG flow 수치 구현을 자율 분담 점검.
3. **L383 LPA 비교**: 두 결과를 동일 표 형식에서 병치. 차이의 부호와 크기를 보고.
4. **SQMH 정합성**: 우주론적 함의가 있을 경우 L2 R2 C23, L4 RVM family 재발방지와의 부호 정합 확인.
5. **REVIEW.md 작성**: 8인 합의 등급 (A/B/C) + 4인 코드리뷰 PASS/FAIL.

---

## 4. 과적합 방지

- LPA' 는 LPA 대비 자유도 (η) 가 추가됨. **AICc 패널티 명시**.
- LPA' 가 LPA 대비 fit/정합성 개선폭이 패널티 미만이면 **LPA 채택** 으로 결론.
- L383 결과를 "개선" 하기 위해 형태를 가져오는 행위 금지 (최우선-1 위반).

---

## 5. 시뮬레이션 실행 규칙

- 수치 RG flow 가 필요할 경우 **multiprocessing spawn Pool, 최대 9 워커, 워커당 단일 스레드** (OMP/MKL/OPENBLAS=1) 강제.
- 실패 시 **코딩 버그 우선 의심** → 4인 코드리뷰 → 재실행. 물리 해석은 코드 검증 후.
- numpy 2.x: `np.trapezoid` 만 사용.
- print 에 유니코드 금지 (cp949 안전).

---

## 6. 산출물 합의 형식

`REVIEW.md` 에 다음 항목을 채운다 (수치는 팀 도출 결과만 기재, 본 문서에는 비공개):
- 8인 합의 LPA' 구조 요약 (자체 표현)
- η 도출 결과 (자체 부호와 크기, 자기무모순성 검토)
- NGFP 위치 (LPA 대비 이동량, 자체 좌표)
- Critical exponents (LPA 대비 수정량)
- LPA vs LPA' 비교표 (단일 표, 8인 합의)
- 4인 코드리뷰 PASS/FAIL 항목별 정리
- 최종 등급 A/B/C 와 정직 한 줄

---

## 7. 정직 한 줄 (의무)

REVIEW.md 말미에 정직 한 줄을 반드시 넣는다. 결과가 부정적이면 부정적이라고 적는다. 결과 왜곡 금지 (CLAUDE.md 재발방지).
