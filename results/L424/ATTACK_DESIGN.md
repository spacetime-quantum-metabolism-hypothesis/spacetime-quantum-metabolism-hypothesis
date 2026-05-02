# L424 ATTACK_DESIGN — 8인팀 reviewer 공격 설계

**주제**: dSph (dwarf spheroidal) σ₀ saturation 예측을 P9 anchor pool 추가 시
paper §3.4 "three-regime σ₀(env)" (BB three-regime parameterization) 의
*강제력* (forcing) — 즉, dSph anchor 추가가 monotonic 단조 모델 기각의
**구조적 강제** 인지, 아니면 anchor pool 확대의 자유도-숫자 우위인지.

**선행**: L405 ATTACK/NEXT_STEP/REVIEW (Δln Z=0.8 R-grid + P9/P11 forecast).
L420 (Cassini Λ_UV postdiction caveat 강화).
paper/base.md L918 row #5 "Three-regime 강제성 약함 (anchor 4-5개 필요), dSph + NS 추가".

**원칙**: CLAUDE.md [최우선-1, 2] 준수. 8인 자율 토의 (Rule-A).
역할 사전 지정 없음. dSph σ₀ "예측값" 은 paper 가 실제로 priori 산출한 적 *없음*
— 단지 §3.4 three-regime 의 cosmic regime extrapolation 으로 *암묵적* 구간 ⟨0.4–1.0⟩
정도가 시사될 뿐. 이 비대칭이 본 ATTACK 의 핵심 고리.

---

## 8인팀 자율 발생 비판 채널 (B1–B8)

### B1 — "saturation prediction" 의 출처 부재
"dSph σ₀ saturation" 이 SQMH axiom L0–L4 로부터 a priori 도출된 적 없음.
paper §4 22-예측 표 P9 row 자체가 *qualitative* 한 위치-지정 (low-ρ_env regime
재진입) 에 그치며, 정량 예측 구간 (예: σ₀_dSph ≲ X) 부재.
→ "saturation prediction" 이라는 본 L424 주제 명칭은 *post-naming*.
L420 Λ_UV 사례와 동일 구조: prediction-실패 → caveat 강화로 정직 처리해야.

### B2 — three-regime 강제력 ≠ anchor pool 확대
P9 dSph 추가가 ΔAICc / Δln Z 를 개선해도, *그 개선이 "단조 모델 기각의 강화"
인지 "free-parameter 모델의 fitting 우위" 인지* 분리 불능.
L405 mock injection (LCDM mock 200개) 에서 three-regime 의 false-detection rate
100% — 자유도 우위가 null data 에서도 작동. dSph anchor 추가는 이 false-rate
를 *낮추는 방향이 아니라 높이는 방향* 일 수 있음 (k=5 패널티 대비 N 증가 미미).

### B3 — dSph σ₀ 측정 자체의 ρ_env 정의 모호
dSph 는 (a) 자체 stellar density (kpc 안쪽) ~ +3 ~ +4 (galactic-internal regime),
(b) Local Group 환경 ρ_env (kpc 바깥) ~ -1 ~ 0 (cluster-cosmic 사이) 으로
*regime 양다리*. anchor x-축 (log10 ρ_env) 에 어느 값을 넣을지 자체가 모델
선택. 어느 쪽을 넣느냐에 따라 ΔAICc 부호가 뒤집힐 위험.

### B4 — 측정 σ₀ 와 모델 σ₀ 의 대응 불명
paper §3.4 three-regime 의 σ₀ 는 "σ = 4πG·t_P 정상화 후 지역 보정 인자"
[CLAUDE.md SI 정의]. dSph 의 "σ₀ 측정값" 은 (a) stellar dynamics → M/L,
(b) gas-poor → MOND-style a₀ 추정, (c) Spitzer/Gaia DR4 운동학.
이 어느 것도 *직접* SQMH σ₀ 를 측정하지 않음 — 변환식 (proxy → σ₀) 자체가
paper 에 없음. anchor 로 쓰려면 변환 prior 추가 필요 → axiom 경제성 페널티.

### B5 — Local Group sample selection bias
Draco / UMi / Sculptor / Fornax / Carina / Leo I / Leo II / Sextans 8개 dSph
중 어느 것을 anchor pool 에 넣을지 사전 등록 (pre-registration) 없으면
사후 cherry-picking. L405 NEXT_STEP "1개월 내 P9 dSph 후보군 문헌 정리"
는 *3개* (Draco, UMi, Scl) 만 명시 — 나머지 5개를 *왜 제외* 했는지 기준 부재.
sample 선정 자유도 = 사후 우위 source.

### B6 — "saturation" 부등식의 부호 미지정
P9 가 *상한* (σ₀_dSph ≲ X) 인지 *하한* (σ₀_dSph ≳ X) 인지 *구간* 인지 paper
미정. saturation 은 통상 "한 방향으로 평탄화" — 하지만 어느 방향?
cosmic→cluster→galactic 방향 monotonic-down 인지, V-shape down-up 인지에
따라 dSph 위치 (low-ρ_env) 가 cosmic regime (high σ₀) 인지 cluster regime
(mid σ₀) 인지 결정. 사전 부호 없는 "saturation" 은 falsifier 비-기능.

### B7 — Forecast Δln Z 의 toy-기반 위험
L405 simulations/L405/run.py 에서 EXTRA_ANCHORS["P9_dSph"] = (-0.3, 0.85, 0.12)
은 *합성값*. 실제 dSph 측정치 분포 (가용한 stellar dynamics 추정) 와 비교
검증 없음. forecast Δln Z 가 toy-가정 의존 — 실 측정 시 σ_err 가 0.12 보다
훨씬 클 수도. "forecast 강화" 결과를 paper 본문 인용 시 toy caveat 필수.

### B8 — Falsifier 활성화 조건 부재
L405 NEXT_STEP "추가 anchor 일치 시 Δln Z 측정, 불일치 시 3-regime 기각"
은 정성. 어느 χ² 임계 (예: 1-out LOO χ² > X) 에서 기각으로 판정? 사전 임계
없으면 사후 변경 가능. dSph anchor 가 P9 falsifier 로 기능하려면 임계
*수치* 등록 필요.

---

## 8인팀 합의 결론

- dSph σ₀ "saturation prediction" 은 SQMH axiom 도출 prediction 이 아니라
  three-regime 의 *cosmic regime 재진입* 시사. P9 anchor 추가의 강제력은
  (i) 측정값 정확도, (ii) ρ_env 매핑, (iii) 변환 prior, (iv) sample selection,
  (v) falsifier 임계 5축에 *모두* 의존하며, 어느 한 축이 미해결이면
  *post-hoc dredging* 위험.
- P9 anchor pool 추가 시 paper §6.1 row #5 (강제성 약함) 는 *해결되지 않음*
  — 새 ACK_REINFORCED 가 추가됨 (위 5축).
- 정직 권고: dSph anchor 사용 시 sample (3개 명시), x-매핑 (regime
  내부/외부), σ₀ 변환 prior, falsifier 임계 4가지를 paper 본문에 사전등록.
- 강제력 검증은 (a) Δln Z(R-grid) 가 dSph 추가로 R 의존성이 *약화* 되는지
  (즉 Lindley fragility 감소), (b) mock injection false-rate 가 *낮아지는지*
  두 지표로만 인정. ΔAICc 단독 우위는 자유도-우위 cherry-pick 로 거부.

---

## NEXT_STEP / REVIEW 로 이행

- NEXT_STEP: 8인팀이 합의한 (a)–(b) 두 지표를 측정 가능한 형태로 task list 화.
- REVIEW: 4인팀이 Python forecast (simulations/L424/run.py) 로 (a)–(b) 실행,
  dSph anchor 3 시나리오 (compat / tension / null) × R-grid {2,3,5,10} 매트릭스
  + mock injection rate 측정.
