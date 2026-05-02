# L447 ATTACK DESIGN — S_8 worsening 의 *방향* 을 PASS_STRUCTURAL 로 격상 가능성

## 목적
SQT 가 S_8 +1.14% (~OBS-FAIL, K15) 정직 인정 한 상태에서,
*방향* (worsening, ΔS_8 > 0) 자체가 dark-only μ_eff ≈ 1 + 0 채널 SQT 의
*구조적 (non-tunable) 예측* 인지 검증한다.
- 만약 구조적이면: *양면 falsifiability* (관측이 ΔS_8 ≤ 0 으로 가면 SQT 즉시 falsify;
  ΔS_8 > 0 로 가면 SQT 정합성 회복) 을 가지는 *PASS_STRUCTURAL* 로 격상.
- 만약 구조적이 아니면 (parameter tunable): K15 OBS-FAIL 그대로 유지.

## 8+4 패턴

### Stage 1 — 8 인 자유토의 (역할 사전 지정 없음)
방향만 제공. 수식/값 미제공.

자연 분담 예상 (자유 수렴):
- A. dark-only coupling 일반 정리 — 어느 SQT 분지가 baryon 분리 / DM 결합 구조를
     강제하는지 (L2 C10k 정합성 재검토). amplitude-locking Q17 부분 도출 결과 활용.
- B. 선형 성장 채널 — μ_eff = G_eff/G 가 dark sector 만 증폭할 때 σ_8 / S_8 의
     *부호* 가 결정 (감소 가능?, 증가 강제?). w(z) ≈ −1 근방, dark-only β > 0 한도.
- C. background w(z) 와 결합 — quintessence-like w(z) > −1 가 LCDM 대비
     성장 누적을 *낮추는* 효과 vs μ_eff 증폭 효과의 부호 경쟁.
- D. amplitude-locking Δρ_DE ∝ Ω_m (Q17 부분 도출, L6 재발방지 명시) 가
     S_8 증가/감소 어느 쪽으로 *기울이는지*.
- E. tunable degree of freedom 점검 — SQT 의 non-LCDM 자유 파라미터 (예: ξ_q, n)
     의 정의역에서 *모든 점* 이 ΔS_8 > 0 인지, 아니면 ΔS_8 ≤ 0 영역이 있는지.
- F. falsifiability 형식 — Popper / Mayo error-statistical 관점에서 "방향 예측"
     이 PASS_STRUCTURAL 자격을 가지려면 추가로 만족해야 할 조건 (정량화).
- G. 관측 기준선 — DES-Y3 / KiDS-1000 / HSC-Y3 의 ΔS_8 wrt LCDM 부호 / 유의도.
     향후 LSST-Y1, Euclid 의 분해능 (~σ(S_8)) 추정.
- H. 편집/판정자 — 8 인 합의 표 (CONSTRUCTIVE / NULL / DESTRUCTIVE) 와
     PASS_STRUCTURAL / OBS-FAIL 둘 중 결정.

### Stage 2 — 4 인 코드 / 식 검증
- 선형 성장 ODE δ'' + (2 + H'/H) δ' − (3/2) Ω_m(a) μ_eff δ = 0
  부호 전개 (μ_eff > 1 ⇒ δ 증대, σ_8 증가) 직접 확인.
- dark-only β embedding: μ_eff = 1 + 2 β_d² f_d² (f_d = ρ_dm/ρ_m). β_d 정의역
  [0, β_max] 에서 ΔS_8 > 0 단조성 검증.
- background w(z) > −1 (thawing) 의 ISW / late-time 성장 억제 항이 μ_eff
  증폭을 부분 상쇄 가능한지 chi^2 부호 추정 (단, full Boltzmann 없이는 정량 X).
- amplitude-locking 와 β_d 가 *독립* 자유도인지 / 종속인지 확인 (Q17 도출 한계).

### Stage 3 — Synthesis
- 합의 결정: PASS_STRUCTURAL vs OBS-FAIL 유지.
- 정직 한 줄 (REVIEW.md 끝): "*방향* 만이 구조적이어도, *크기* 가 관측 σ 안에
  들어와야 진정한 PASS. 현재 +1.14% 는 KiDS/DES 1σ 안이지만 LSST-Y1 σ ≈ 0.5%
  분해능에서 K15 재판정 필수."

## 산출물
- `results/L447/ATTACK_DESIGN.md`
- `results/L447/NEXT_STEP.md`
- `results/L447/REVIEW.md`

## 제약
- 수식/값 사전 제공 금지 (최우선-1). dark-only μ_eff 명칭, amplitude-locking 명칭,
  Q17 부분 도출 사실만 입력.
- L5 재발방지 "Background-only 수정 + μ_eff = 1 구조: S_8 tension 구조적 해결 불가"
  는 *해결* 에 대한 진술이며 *방향 예측* 에 대한 진술이 아님 — 본 격상 시도는
  이 재발방지와 충돌하지 않음. 단, 결론에서 명시 분리.
- L6 재발방지 "mu_eff ≈ 1 은 S8 tension 해결 불가, '해결한다' 주장 금지" 준수.
  본 격상은 "해결" 이 아닌 "방향 예측 적중" 주장.
- toy-level 수치 비교 금지: hi_class / CLASS Phase 3 수준 없으면 정량 결론 X.
