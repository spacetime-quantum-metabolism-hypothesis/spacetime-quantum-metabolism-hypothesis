# L447 REVIEW — *방향* 격상 시도의 자체 비판

## 핵심 주장 (격상 시도)
S_8 +1.14 % worsening 의 *부호* 가 dark-only μ_eff ≥ 1 SQT 분지의 구조적
귀결이라면, 양면 falsifiability (방향 적중 OR ΔS_8 ≤ 0 시 dead) 를 가지므로
PASS_STRUCTURAL 자격이 있다.

## 8 인 / 4 인 자체 비판

### B1. 부호 단조성은 정말 *구조적* 인가?
- δ'' + (2 + H'/H) δ' − (3/2) Ω_m μ_eff δ = 0 에서
  μ_eff > 1 ⇒ δ_today / δ_LCDM > 1 ⇒ σ_8 / σ_8^LCDM > 1.
  ⇒ Ω_m 고정 시 ΔS_8 > 0 *필연* (부호 lock-in).
- 그러나 SQT 는 Ω_m 도 fitting 시 LCDM 와 다르게 나옴. Ω_m 이 LCDM 보다
  *낮게* fit 되면 S_8 = σ_8 √(Ω_m / 0.3) 이 *상쇄* 될 수 있음.
- 즉 "구조적" 주장은 (Ω_m, μ_eff) 합성에서 부호가 lock 되어야 성립.
- L5 C33 f(Q) 사례: Ω_m = 0.340 으로 *증가* + S_8 ∝ √(Ω_m/0.3) 동반 상승
  로 K15 fail 확정. SQT 도 Ω_m fit 결과에 의존.
- ⇒ **B1 결론**: μ_eff 부호 lock 은 구조적, 그러나 Ω_m 이동 부호는 데이터
  기반이라 *전체* ΔS_8 부호 단조성은 *부분 구조적, 부분 경험적*. PASS_STRUCTURAL
  조건은 절반만 만족.

### B2. amplitude-locking 의 도출 등급
- L6 재발방지 명시: "Amplitude-locking '이론에서 유도됨' 주장 금지. Q17 부분
  달성. Exact coefficient = 1 은 E(0)=1 정규화 귀결이며 동역학적 유도 아님."
- ⇒ amplitude-locking 을 PASS_STRUCTURAL 의 *근거* 로 쓰면 Q17 미달성 영역을
  과대주장하는 것. **B2 결론**: amplitude-locking 은 본 격상 근거에서 빼야 함.
  μ_eff = 1 + 2 β_d² (Cassini-evading dark-only embedding) 부분만 사용 가능.

### B3. β_d 자유도 존재
- β_d > 0 정의역 *전체* 에서 ΔS_8 > 0 단조 ⇒ 부호 PASS_STRUCTURAL.
- 단, β_d = 0 은 LCDM 와 등가 ⇒ ΔS_8 = 0. SQT 가 β_d > 0 을 *강제* 한다는
  도출이 없으면 (β_d 는 free), "방향 예측" 도 사실은 1 자유 파라미터의 부호
  예측에 불과.
- ⇒ **B3 결론**: β_d > 0 강제 도출이 없으면 PASS_STRUCTURAL 미만.
  현재 SQMH 는 β_d > 0 *부호* 를 요구 (matter → DE 방향, L4 RVM family
  wrong-sign 사례 와 대비). 부호는 강제, 크기는 free.

### B4. 양면 falsifiability 의 진짜 강도
- "ΔS_8 ≤ 0 시 SQT dead" 는 LSST-Y1 / Euclid σ(ΔS_8) ≈ 0.005 분해능에서만
  의미. 현재 KiDS / DES σ ≈ 0.02 에서는 ΔS_8 = 0 ± 1σ 도 SQT 와 정합.
- ⇒ **B4 결론**: 격상은 "현재" PASS 가 아니라 "미래 LSST 시점에 검증 가능한
  P_S8_sign prediction" 의 정식 등재.

### B5. L5 / L6 재발방지 충돌 점검
- L5: "Background-only + μ_eff = 1 의 S_8 tension 구조적 해결 불가" — 본 격상은
  *해결* 이 아닌 *방향 예측* 이므로 충돌 없음. (단 본문 명시 필수)
- L5: "ΔS_8 < 0.01 % 전원 FAIL (Q15)" — Q15 는 *완화* (resolve) 채점, 본
  격상은 *방향* 채점, 다른 지표.
- L6: "mu_eff ≈ 1 은 S8 tension 해결 불가, 해결 주장 금지" — μ_eff = 1 + 2 β_d²
  은 정확히 ≈ 1 이 아닌 약간 큰 값, 그리고 *해결* 주장 안 함, *방향* 만 주장.
  충돌 없음.

## 합의 결정
- *방향* PASS_STRUCTURAL 격상은 **부분 합리적** 이지만 **현재 라벨 단계에서는
  채택 보류**.
- 채택을 위한 선결 조건:
  1. β_d > 0 부호 강제 도출 (현재 SQMH 부호 규약에서 충족 — 약 PASS).
  2. ΔS_8 부호 단조성 분석 증명 (B1: 부분 구조적 — 약 PASS).
  3. Ω_m 이동 부호 점검 (SQT joint fit 에서 Ω_m ≷ 0.3 ?) — *데이터 의존*,
     misPASS 위험 → **재 시뮬 필요** (Case C, δ-ODE toy + joint fit).
  4. PREDICTIONS.md 에 P_S8_sign 등재 시 falsifier 임계값 / 미래 데이터셋 / σ
     명시.

## 정직 한 줄
*방향* 만의 격상은 미래 검증 가능한 P_S8_sign 등재 (PASS_FUTURE) 까지가
정직한 한계이며, 현재 K15 OBS-FAIL 상태를 PASS_STRUCTURAL 로 격상하는 것은
Ω_m 이동 부호의 데이터 의존성 때문에 *과대주장* 이다.
