# SQMH / SQT — 자주 묻는 질문 (한국어)

> `paper/base.md` §8 의 동반 부록. 3개 tier — 한 문장 답 (Q1–Q4),
> 한 단락 답 (Q5–Q9), 학생/심화 답 (Q10–Q12).
> 영문 mirror (`faq_en.md`) 와 동일한 정직 강도로 잠겨 있다.

---

## Tier 1 — 한 문장 답

**Q1. SQT 가 뭔가요?**
공간을 셀 수 있는 매질로 보고, 양자 흡수와 생성으로 중력과 우주
가속을 *같은 axiom 집합* 에서 동시에 도출하는 가설.

**Q2. 검증되었나요?**
substantive falsifiable 검증 4건 통과 (Newton 회복, BBN ΔN_eff,
Cassini β_eff, 등가원리 η = 0). Λ 기원 claim 은 `CONSISTENCY_CHECK`
로 강등됨 (차원 정합성, 예측 *아님*). S_8 은 +1.14% *구조적으로
악화* — Euclid DR1 cosmic-shear 4.4σ falsifier 로 사전 등록됨.

**Q3. 결정적 검증은?**
배경 채널은 DESI DR3 w_a (2025–2026), 섭동 채널은 Euclid DR1
cosmic-shear ξ_+ (2026–2027, 중심 4.38σ, 3σ falsification floor).
두 채널 모두 데이터 공개 *전* triple timestamp (arXiv ID + GitHub
tag + OSF DOI) 로 사전 등록.

**Q4. 신뢰할 수 있나요?**
모든 코드/데이터 GitHub 공개, 22행 정직 한계 표 본문 명시. 누구나
5초 Python 또는 30분 LLM prompt 로 헤드라인 수치 재현 가능.

---

## Tier 2 — 한 단락 답

### Q5. 다른 이론과 뭐가 다른가요?

대부분의 modified gravity (MOND, TeVeS, f(R), Galileon …) 는
*중력 법칙을 수정*. SQT 는 *시공간 동역학 자체* 를 수정한다.
6개 axiom (mass-action 흡수+생성, emergent metric, dark-only
sector embedding) 한 묶음에서 중력과 cosmological-constant-scale
ρ_Λ 가 같은 과정에서 emerge 한다. 단, Λ scale 일치는 *차원
정합성* 수준이며 (Q11 참조) 진짜 a-priori 예측은 아니다.

### Q6. 약점은?

3 가지 정직 인정. (a) S_8 가 +1.14% *악화* 됨 — fit 실패가 아닌
구조적 한계로, Euclid DR1 cosmic-shear 4.4σ falsifier 로 사전
등록 (중심 4.38σ; prediction-uncertainty quadrature 후 4.19σ;
3σ floor). (b) σ₀(t) 의 비단조 환경 의존성은 *데이터에서 발견된*
postdiction 이며 사전 예측 아님; mock injection 에서 false-detection
rate 100% caveat. (c) RG 계수 b, c 가 first-principle 도출 안 됨
— anchor-fit. 32-claim self-audit 중 **13% (4건)** 만이 진짜
substantive falsifiable prediction (Newton 회복, BBN ΔN_eff,
Cassini β_eff, EP η = 0); raw 28% PASS_STRONG 헤드라인은 항상
이 13% 와 양면 표기 의무.

### Q7. 일상에 영향이 있나요?

직접 영향 없음. SQT 는 cluster (~10⁶ ly) / cosmic (~10¹⁰ ly)
규모에서만 측정 가능. 태양계 중력과 실험실 물리는 현 정밀도
(Cassini, lunar laser ranging, MICROSCOPE) 에서 Newton/Einstein
과 구분 불가.

### Q8. 만약 맞다면?

Λ scale 이 axiom 수준에서 *부분* 도출됨 (완전 a-priori 도출은
Q11 의 circularity 로 차단됨). MOND-like 현상이 modified force
law 가 아닌 시공간 동역학에서 emerge. cosmological-constant
problem 은 *해소* 가 아니라 *재구성* 되며 — 그 재구성 자체가
측정 가능한 진보.

### Q9. 만약 틀렸다면?

정직 framework 자체가 case study 가치를 지닌다. 22행 정직 한계
표, 32-claim self-audit (raw 28% / substantive 13%), mock
injection caveat, 사전 등록 Euclid 4.4σ falsifier 가 *어떻게
틀릴 수 있는지* 정량화한다. 이론 자체가 아니라 그 구조가 후속
세대까지 이어지는 것이 목적.

---

## Tier 3 — 학생/심화 답

### Q10. axiom 4 (emergent metric) 의 미시 origin 이 OPEN 이라는 게 뭔가요?

axiom 4 는 거시 metric 이 이산 양자 substrate 에서 *emerge*
한다고 명시한다. 거시 규모에서는 일반상대성 재현이 inheritance
로 PASS (Newton, GW170817, LLR, EP). 그러나 그 미시 substrate
가 무엇인지 — loop quantum gravity, causal set, tensor network
중 어느 것 — 는 유일 결정 안 됨. coarse-grained causal-set
("causet meso") 구현이 5조건 중 4 조건부 통과. 어느 substrate
가 옳은지는 OPEN, 22행 표에 `NOT_INHERITED` 로 표기.

### Q11. ρ_q / ρ_Λ = 1.0000 이 정확이라면 왜 circularity caveat?

steady-state 수밀도 n_∞ 도출 시 ρ_Λ_obs 가 *input* (axiom 3
정규화) 이기 때문이다. 따라서 1.0000 은 단위 변환에서 따라오는
*항등식* 이지 falsifiable a-priori 예측 *아니다*. L402 audit 에서
독립 도출이 10⁶⁰ 차이로 실패함이 확인되었고, L412 review 에서
Λ origin 등급을 `PASS_STRONG` → `CONSISTENCY_CHECK` 로 강등.
남는 것은 (a) ρ_Λ scale 의 차원 분석 일치, (b) order-of-magnitude
naturalness — 둘 다 보고할 가치는 있지만 예측은 아님.

### Q12. 어떻게 도울 수 있나요?

3 가지 구체 채널. (1) 헤드라인 수치 재현 — verification 부록의
5개 Python script 직접 실행 또는 5개 LLM prompt 를 선호 모델에
붙여 넣기. 출력이 다르면 GitHub issue 제출. (2) 22행 정직 한계
표 stress test — 각 행이 falsifiable 하도록 설계됨. (3) DESI DR3
(2025–2026) 와 Euclid DR1 cosmic-shear (2026–2027) 데이터
공개 시, 사전 등록된 SQT 예측 (w_a 부호/대역; +1.14% S_8
초과 + §4.6 4-band two-sided decision rule) 을 측정값과 비교해
판정 결과를 공개 보고.
