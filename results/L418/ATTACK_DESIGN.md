# L418 — ATTACK_DESIGN (8인팀 공격 설계)

> **CLAUDE.md 최우선-1 준수**: 본 문서는 *방향만* 제공. 수식·구체값·유도경로 힌트 금지.
> 8인팀이 base.md §4.3 "PIXIE μ-distortion 1.02×10⁻⁸" 라인을 *처음부터* 검증한다.
> 1.02e-8 라는 숫자는 base.md 표에만 등장 — 본문 어디에도 *도출* 없음. 이 공백이 공격 표적.

## 목적
PIXIE μ-distortion 1.02×10⁻⁸ 예측을 PASS_STRONG 으로 승격할 수 있는지 판정.
승격 조건: (a) 도출 경로가 σ₀, n_∞, ε 외 *추가 입력* 없이 닫혀 있고, (b) circularity(§5.2 Λ-input) 에 *재의존* 하지 않으며, (c) 전경(galactic dust + CIB + free-free) 분리 후 검출 가능성이 1σ 이상.

## 8인팀 구성 (자율 분담)
- 8명. 역할 사전 배정 *없음*. 토의 중 자연 발생하는 분업만 인정.
- 가능한 자율 분담 클러스터(예시, 강제 아님): 열역학 / 우주재결합 이전 photon-baryon 결합 / SQT axiom 회로 / 전경 잡음 / 통계 / 문헌 반례 / Λ-circularity 재발 / falsifiability gate.

## 공격 벡터 (방향만)
**A1. 도출 폐쇄성 공격.**
- "1.02e-8" 가 σ₀, n_∞, ε 만으로 닫히는가? 아니면 BBN 시점 baryon-photon 비, recombination 광학두께, μ-window redshift band 등 *추가 우주론 입력* 이 잠입해야 닫히는가? 잠입이 있다면 PASS_STRONG 자격 박탈, PARTIAL/PENDING 유지.

**A2. 산술 항등식 의심 (PASS_IDENTITY 위험).**
- L409 §6.5(e) 가 σ₀=4πG·t_P 류 산술 항등식 따름결과를 PASS_STRONG 에서 격하한 패턴이 μ-distortion 에서 재발할 가능성. 1.02e-8 가 axiom 의 차원분석 자동 결과인지, 아니면 동역학적 sink Q 가 photon 영역에 *진짜로* 에너지를 흘려넣어 발생하는 분포 왜곡인지 분리 판정.

**A3. Λ-circularity 재발 공격.**
- §5.2 의 "n_∞ ← ρ_Λ_obs input" 순환성이 μ 도출에 *재상속* 되면, μ 수치는 Λ 관측치의 또 다른 표현일 뿐. 도출 사슬에서 ρ_Λ_obs 의 *2차 사용* 흔적을 추적.

**A4. μ vs y 분기점 공격.**
- COBE/FIRAS 가 이미 μ < 9×10⁻⁵, y < 1.5×10⁻⁵ 상한. SQT 가 μ-window (z ≈ 5×10⁴–2×10⁶) 와 y-window (z < 5×10⁴) 사이에서 어느 쪽에 에너지를 더 많이 흘리는가? y/μ 비가 SQT 구조에서 자연 도출되는가? y 쪽이 더 크다면 1.02e-8 표제는 오도.

**A5. 흡수율 vs 생성률 비대칭 공격.**
- SQT 는 흡수 sink Q 가 핵심. photon-에너지 흡수가 *전자기장 자유도* 에 직접 작용하는 채널이 axiom 에 있는가, 아니면 dark-only embedding (§4.1 EP 보호) 때문에 photon 채널이 차단되는가? 차단된다면 μ-distortion 은 *구조적 0* 이고 1.02e-8 는 모순.

**A6. 전경 분리 공격.**
- 1.02e-8 < galactic dust monopole(≈ 10⁻⁶~⁻⁵ 영역). 전경 분리 component-separation (ILC/MILCA/NILC/HILC 등) 후 잔차에서 검출 가능한가? "전경 대비 2σ" (base.md §4.3) 의 출처 문서화.

**A7. PIXIE 감도 가정 공격.**
- "노이즈 대비 10σ" 가 PIXIE 1×10⁻⁹ 감도를 가정. PIXIE 가 실제로 비행 승인되었는가, 아니면 후속 mission (PRISM, BISOU, Voyage 2050) 인가? facility 미확정 시 falsifier timeline 자체가 표류.

**A8. SQT-vs-표준 분리 공격.**
- ΛCDM 의 표준 μ 예측 (silk damping + adiabatic dissipation) 이 ≈ 2×10⁻⁸ 영역. SQT 가 이 baseline 위에 *추가* 1.02e-8 를 얹는가, 아니면 SQT *총합* 이 1.02e-8 인가? 만약 후자라면 표준-미달이라 falsifier 부호가 뒤집힘.

## 승급/격하 결정 트리
- A1·A3·A5 중 하나라도 *잠입/재상속/차단* 발견 → PENDING 유지, 가능시 NOT_INHERITED 로 강등.
- A2 가 PASS_IDENTITY 로 판정 → §6.5(e) "31% raw vs 13% substantive" 양면표기 패턴에 추가, PASS_STRONG 박탈.
- A4·A8 가 부호/baseline 모순 → base.md §4.3 표 수정 필수.
- A6·A7 만 통과 못하면 falsifier *timeline* 이슈 (이론은 살아있음).
- 모두 통과 → PASS_STRONG 승격 후보, NEXT_STEP 으로 정량 도출 진행.

## 산출 요건
8인팀 토의 후 각 공격 벡터별 verdict {PASS / PENDING / FAIL / NOT_APPLICABLE} 한 줄과 근거 한 단락.
수식·수치 결과는 4인 코드리뷰 팀의 simulations/L418/run.py 결과로 *후행* 검증.
