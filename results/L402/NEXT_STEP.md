# L402 — 8인팀 다음단계 설계 (circularity 완화 path)

## 0. 원칙 (CLAUDE.md [최우선-1, 2])

방향만 제공. 8인팀이 자율 도출. 본 문서는 "어떤 *방향* 을 시도할지" 의 list 만
제공. 구체적 수식/계수 절대 금지.

## 1. 가능한 도출 path 후보 (방향만)

### Path α — Hubble-only 채널
n_∞ 를 *현재 우주 Hubble scale* 만으로 추정. Input: H₀ (관측), Planck length,
양자 시공간 단위. ρ_Λ_obs 는 *입력에서 제외*. 결과 ρ_q 가 ρ_Λ_obs 와 비교
당시 사후적으로 일치하는지 확인.

방향만: "infrared cutoff = Hubble horizon" 류 dimensional argument 의 *SQT 공리
적합 변형* 을 8인팀이 자율 도출.

### Path β — KMS / detailed-balance 채널
Schwinger-Keldysh formalism 의 *thermal equilibrium* 조건 (KMS) 으로부터
정상상태 number density. Input: 가속우주 de Sitter 온도 (Hubble 단), 양자
시공간 dispersion. 관측 ρ_Λ 는 *후험 비교* 에만 사용.

### Path γ — Generation-absorption 자기일치 채널
Axiom 3 의 두 항 (생성, 흡수) 을 *각각 독립* 으로 micro-physics 에서 추정 후
balance 가 자발적으로 ρ_Λ scale 에 떨어지는지 확인. 양 항이 ρ_Λ 를 input 으로
공유하지 않으면 self-consistent prediction.

### Path δ — Holography / horizon entropy 채널
Bekenstein-Hawking 에 대응하는 SQT degree-counting 으로 horizon scale 에서
n_∞ 추정. ρ_Λ_obs input 배제.

### Path ε — Anthropic null 비교 (control)
ρ_Λ_obs 를 *임의 다른 값* 으로 대체 (toy: 10× 또는 1/10) 했을 때 SQT 도출이
같은 1.0000 을 유지하는지 확인 → 항진명제 / 진짜예측 구분.

## 2. 우선순위 (8인팀 합의 시뮬)

| Path | 추정 노력 | 정량검증 가능? | 우선순위 |
|------|-----------|----------------|----------|
| ε    | 30 분 (Python) | 즉시 | **1순위** (negative control) |
| α    | 1–2 일 | 부분 | 2순위 |
| β    | 1주일 | 부분 | 3순위 |
| γ    | 2–4주 | 어려움 | 보류 |
| δ    | 2–4주 | 어려움 | 보류 |

## 3. 4인팀 실행 권고

**Phase A (이번 loop):** Path ε 실행. ρ_Λ_obs 를 1/10, 1, 10 배 변동 시
verify_lambda_origin.py 산출 ρ_q/ρ_Λ 가 어떻게 변하는지 정량 측정. 결과로:
- 항상 1.0000 → 항진명제 확정 → caveat *강화* 권고
- 변동 → 진짜 prediction 채널 발견 → 추가 시도

**Phase B (다음 loop):** ε 결과에 따라 α 또는 β 진입.

## 4. 실패 시 fallback

모든 path 에서 ρ_Λ_obs input 회피 실패 시 — paper §5.2 caveat 강화 권고:

1. abstract 에서 'ρ_q/ρ_Λ = 1.0000' 문구 삭제 또는 '(consistency check)' 명시.
2. README claims-table 의 PASS_STRONG → CONSISTENCY_CHECK 등급 신설 후 이동.
3. §5.2 첫줄에 *불가피 circularity* 명시 (현재는 "부분적" 으로 약화).
4. Q11 답변에 "이는 prediction 이 아니라 dimensional consistency" 직설.

## 5. 정직 원칙 재확인

- circularity 가 회피 *불가능* 으로 확정되면, 회피 시도 자체보다 caveat 강화가
  우선.
- "1.0000 exact" 광고 유지하면서 caveat 만 추가하는 *cosmetic fix* 는 base.fix.md
  에 회피 시도로 기록 금지.
