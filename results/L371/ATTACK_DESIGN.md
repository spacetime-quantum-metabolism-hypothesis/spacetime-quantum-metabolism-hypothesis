# L371 ATTACK DESIGN — 285-Loop 종합 audit

## 0. 정직 한국어 한 줄
L371 단일 loop 의 임무는 새로운 이론 공격이 아니라 L342–L370 29개 loop 누적 결과를 단일 narrative 로 종합해 285-loop 누적 등급/JCAP 위치/limitation 해결 진행도를 정직하게 갱신하는 audit 이다.

## 1. 메타 원칙
- 이 loop 는 시뮬레이션을 새로 돌리지 않는다. 기존 L342–L370 산출물 (run_output.json / scan_results.json / ATTACK_DESIGN.md / NEXT_STEP.md / REVIEW.md) 만 입력으로 사용.
- CLAUDE.md 최우선-1, -2 준수. 본 문서 어떤 수식도 포함하지 않는다.
- 등급 변화·JCAP 변화는 *정직 회복* 과 *정직 격하* 양방향 모두 허용. 한쪽으로 편향 금지.

## 2. 종합 axis (방향만)

### A1 — Anchor forecast 축 (L344, L345, L346)
- P9 dSph + P11 NS saturation 동시 추가 시 3-regime 강제 가능성 forecast.
- 비단조 vs 단조 σ_0(env) 의 proper ln Z Bayes factor 설계.
- 비단조성이 *데이터 보기 전* 4 pillar 로부터 prediction 인지 후험 fit 인지 진단.

### A2 — Cluster σ 축 (L347, L348, L349, L350, L351)
- A1689+Coma+Perseus 3-cluster joint, LoCuSS 50, CLASH 25, PSZ2 selection bias, Bullet↔Abell 520 일관성.
- L335 13-cluster pool 계획의 *축 좁히기*: deep-dive (N=3) ↔ broad (N=50) ↔ selection-aware (PSZ2) 세 channel.

### A3 — RG / FP 축 (L352, L353, L354, L355, L356)
- b 1-loop, c 2-loop, Wetterich functional RG, AS Reuter NGFP 사상, Λ_UV=18MeV cutoff 자기무모순.
- L334 pillar 4 ★★ 격하의 *부분 회복* 가능성 (universal 부분만 first-principle).

### A4 — Sampling / Diagnostics 축 (L357, L358, L359, L360, L361)
- 5-dataset joint emcee spec, dynesty multimodal 검출, MCMC convergence gates,
  Q_DMAP cross-dataset tension, SQT mock injection-recovery.
- L336 5-dataset MCMC plan 의 spec 단계 진입.

### A5 — Micro pillar 축 (L362, L363, L364, L365, L368, L370)
- Causal Set Theory, Spin Foam (LQG) 가 5번째 pillar 후보 가능성.
- L337 micro 80% 상한 + a4 emergent metric OPEN 의 *부분 해결* 시도.

## 3. PASS / KILL 기준
- 누적 등급 변화: |Δ| > 0.05 면 narrative 재작성 의무.
- JCAP 변화: |Δ| > 5% 면 paper revision 추가.
- 신규 limitation 해결 진행도: "fully RESOLVED / plan only / 격하 인정 / OPEN" 4분류.
- 사용자 통찰 (3-regime 비단조) narrative 회복 여부 명시.

## 4. 산출물
- ATTACK_DESIGN.md (본 문서)
- REVIEW.md (자가 점검 + CLAUDE.md 위반 검사)
- SYNTHESIS_285.md (필수 — 29 loop 표 + 285 누적 통계 + 등급/JCAP 변화 + 진보 궤적 + limitation 진행도 + 사용자 통찰 narrative)

## 5. 위험
- L342, L343, L362, L363, L368, L370 은 ATTACK_DESIGN/REVIEW 문서가 부재 (시뮬 결과 또는 빈 디렉터리). 이들 loop 의 의미를 *과대* 또는 *과소* 평가할 위험 — 정직하게 "문서 미작성" 으로 표기.
- L344~L361 의 NEXT_STEP 가 대부분 "다음 loop 에서 실행" 이므로, 본 audit 시점에서 실측 결과는 미반영. 등급 변화는 plan 가치 제한적 반영.
