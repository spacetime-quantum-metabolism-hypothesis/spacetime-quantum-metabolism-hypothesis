# L430 — ATTACK DESIGN (8인팀 공격, PARTIAL #1: bilinear mass-action 함수형)

세션: L430 (독립)
날짜: 2026-05-01
주제: PARTIAL #1 — derived 1 (Newton's G 회복) 에 *암묵적으로* 들어가 있는
**bilinear (σ · n_quanta · ρ_matter) mass-action 함수형 가정** 의 명시화 공격.
참조 컨텍스트: §6.5(e) "PARTIAL 8/32 (25%) — caveat 명시 (mass-action 함수형, ...)"
및 L409 NEXT_STEP §(ii) N1 단락.

---

## 0. 공격 한 문장

> "현재 paper/base.md §2.2 derived 1 행은 'depletion-zone gradient → 1/r²' 만 적고
> 흡수율의 **선형곱(bilinear) 함수형** 가정을 본문 어디에도 *명시적으로* 입력
> 하지 않는다. 이 가정은 paper postulate 도, axiom 1–6 의 결론도 아닌
> **숨은 5번째 공리 (hidden axiom)** 이다."

---

## 1. 공격 (8인팀, 자율 분담)

### A1. "depletion-zone gradient → 1/r²" 는 untold step 을 감추고 있다

§2.2 의 한 줄 sketch 는 다음 *암묵 사슬* 을 isol.

1. axiom 1 (matter absorbs spacetime quanta) → 흡수율 R(x)
2. **암묵 가정** : R(x) = σ · n(x) · ρ_m(x)  (bilinear 곱)
3. continuity: ∂_t n + ∇·j = Γ₀ − R
4. 정상상태 + 구형대칭 + 흡수 dominance → ∇²Φ ∝ ρ_m → 1/r²

axiom 1 은 *"흡수가 일어난다"* 만 진술하지 *"흡수율의 함수형이 σ·n·ρ_m"* 을
진술하지 않는다. 다른 함수형 (σ·n²·ρ_m, σ·n·ρ_m^(1/2), σ·n^a·ρ_m^b · f(∇n) …)
도 axiom 1 만으로 *동등하게* 호환된다.

### A2. SK (Schwinger-Keldysh) vertex 는 함수형을 *고정* 하지 않는다

미시 4 축 #1 (SK open-system) 은 KMS PASS 만 한다 (§2.3). 그런데 KMS 조건은
*detailed balance* 를 강제할 뿐, 4-vertex 의 형태 (예: `g · ψ̄ψ · n`,
`g · (ψ̄ψ)² · n`, `g · ψ̄ψ · n²`) 자체는 자유. SK 미적분만으로는
"왜 곱이 1×1 = bilinear 인가" 가 도출되지 않는다.

### A3. paper postulate 표 부재 — reviewer 가 한 줄로 reject 가능

§2.1 6 axiom 표에 "absorption rate is bilinear in (n, ρ_m)" 가 *없다*.
referee 가
> "What is the explicit functional form of the absorption rate? Where is it
> postulated? If it is not in axioms 1–6, derived 1 is not a derivation, it is
> a fit ansatz."
한 줄로 보내면, 현 §2.2 sketch 만으로는 답할 수 없다.

### A4. 차원 분석은 bilinear 를 *허용* 할 뿐 *고정* 하지 않는다

R [1/(m³·s)] = σ [m³/(kg·s)] · n [1/m³] · ρ_m [kg/m³]
은 차원 OK. 그러나
R = σ' [m⁶/(kg²·s)] · n² · ρ_m
도 차원 OK (σ' 재정의). 차원 분석은 *univalent* 함수형을 못 골라낸다.

### A5. 1/r² 자체가 bilinear 를 *전제* 한다 (circular sketch)

§2.2 행은 "depletion-zone gradient → 1/r²" 라고 적지만, 1/r² 이 나오려면
연속방정식 우변이 ρ_m 에 *선형* 이어야 한다. 따라서 sketch 는
"bilinear → ∇²Φ ∝ ρ_m → 1/r²" 의 *결론 부분* 만 적고 *전제* 를 생략.
독자에게는 sketch 가 trivial 도출처럼 보이지만, 실은 bilinear 가 *입력* 이다.

### A6. RG running 와의 cancellation 도 bilinear 가정에 의존

L409 N1: "유한 t_P 에서 1/r² 회복은 axiom 2 (mass-action 함수형) + RG running
의 **비자명 cancellation** 을 요구." — 여기서 "axiom 2 (mass-action 함수형)"
이라고 *적혀* 있는데, 정작 §2.1 의 axiom 2 진술은 "에너지 보존" 이다.
**L409 NEXT_STEP 자체가 axiom 번호와 mass-action 가정의 placeholder 를 혼용**
하고 있어, paper 본문에 들어가면 cross-reference inconsistency.

### A7. PARTIAL 분류 자체가 부족 — "함수형 미명시" 는 PARTIAL 보다 더 깊다

§6.5(e) 는 "mass-action 함수형" 을 PARTIAL 8 중 한 줄로 묶지만, 실제로는
*derived 1 의 entire chain 이 이 가정 위에 서 있다*. PARTIAL 이 아니라
**"hidden postulate"** 로 분류해야 정직하다. 현재 분류는 caveat 만족이 안 됨.

### A8. SPARC 회복 17σ 광고 와 bilinear 미명시 의 비대칭

§4.1 row 1 은 σ₀ regime 구조 PASS_STRONG (postdiction caveat) 으로 광고
하지만, 그 회복의 *수학적 입력* 인 bilinear 함수형이 paper 어디에도
postulate 로 적혀 있지 않다. 18σ 광고와 hidden postulate 의 비대칭은
JCAP referee A-list (Solà, Frusciante, Sakstein) 누구라도 1 라운드에 지적한다.

---

## 2. 공격 종합

| 코드 | 공격 요지 | 격하 등급 |
|------|-----------|----------|
| A1 | derived 1 sketch 가 bilinear 가정을 감춤 | PARTIAL → "hidden postulate" |
| A2 | SK vertex 가 bilinear 를 a priori 고정 못함 | 미시 축 #1 보강 필요 |
| A3 | §2.1 axiom 표에 함수형 진술 부재 | reviewer 즉시 reject 위험 |
| A4 | 차원 분석은 함수형 유일성 미보장 | bilinear 는 *추가* 입력 |
| A5 | 1/r² 도출 자체가 bilinear 전제 | sketch circular |
| A6 | L409 의 "axiom 2 = mass-action" 표기 와 §2.1 의 "axiom 2 = 에너지 보존" 충돌 | cross-ref inconsistency |
| A7 | PARTIAL 분류 부족 | "hidden postulate" 재분류 권고 |
| A8 | 17σ 광고 vs hidden postulate 비대칭 | abstract/§3.4 추가 정직 의무 |

---

## 3. 합의 결론 (8인 → 4인 위임 전)

- **즉시 paper 수정 1단계** (4인 실행 — REVIEW.md):
  derived 1 행 sketch 컬럼에 bilinear 가정 *명시* + §2.2 직후 단락에
  "absorption-rate functional ansatz (B1: bilinear)" 1단락 추가.
  paper postulate 로 등록 — 단, *임시 ansatz* 임을 정직 표기.
- **즉시 paper 수정 2단계** (4인 실행):
  §6.5(e) PARTIAL 8 항목 중 첫 줄 "mass-action 함수형" 옆 cross-link
  (§2.2 derived 1 + 신설 단락) 삽입.
- **다음 8인팀 단계** (NEXT_STEP.md):
  bilinear 를 SK 4-vertex / axiom 1 / 미시 축 #1 의 KMS detailed balance
  로부터 *도출* 시도 (Phase 5+).
