# L574 — 공리 질량 정의 모호성 + 기본입자 재정의 8인 회의적 검증

작성일: 2026-05-02
대상: paper/02_sqmh_axioms.md (axiom 2: mass-action absorption σ n ρ_m)
규약: [최우선-1] 수식 0줄 / 좋은 점 생략 / 문제점만 / 분산 8인 Round 10 의무

---

## R1 — 현재 모호성 적출 (회의자: 정의 명료성 검열관)

axiom 2 본문에서 ρ_m 은 단어로 한 번도 종류가 명시되지 않는다. "matter annihilates these quanta" 의 matter 가 (a) FLRW background 의 macroscopic energy density 인지, (b) baryonic + CDM 합인지, (c) SM 입자 mass eigenstate 의 sum 인지 미정. 이 미정 자체가 reader 가 임의로 채워 넣을 수 있는 *interpretive degree of freedom* — hidden DOF 로서 +1 카운트 정당. §2.1 의 "rest mass μ" 도 동일 모호성 (bare? dressed? Higgs 후?). 모호성 = 결과 fitting 시 사후 selection 자유도.

## R2 — Higgs mass 분리 의무

SM 모든 fermion mass 는 Yukawa·v_H, gauge boson mass 는 g·v_H. SQT axiom set 은 Higgs sector 를 외부에 두고 ρ 를 사용 — Higgs VEV (246 GeV) 와 Yukawa spectrum (전체 SM 의 13개 free) 이 axiom 외부 hidden input. "zero free parameter" 주장이 Higgs sector silent import 로 무너짐. axiom 2 가 Higgs-후 mass 라면 SM 13 DOF 차용 명시 의무, Higgs-전 bare 라면 RAR a₀ 의 SPARC mass 와 mismatch.

## R3 — binding / kinetic mass 차이

a₀ derivation 에서 사용하는 macroscopic galaxy mass (SPARC M_bary) 는 nucleon mass 의 합 — 이 중 99% 는 QCD binding (gluon field + quark KE), 1% 만 Higgs Yukawa. ρ 가 "rest energy / c²" 라면 QCD-dressed, "Higgs-coupled bare" 라면 1% 만 sink. 두 해석 사이 ~100× factor 차. paper 어디에도 어느 쪽인지 진술 없음 — RAR 정합 결과는 사후적으로 macroscopic 해석을 *암묵 채택* 하되 명시 안 함. silent assumption.

## R4 — dark matter mass 정의

axiom set 에 dark sector 가 SM Higgs mechanism 을 공유하는지 별도 mass-generation (Z_2 SSB?) 인지 진술 없음. σ n ρ_m 의 ρ_m 이 baryon+CDM 합이라면 두 sector 의 mass-generation 메커니즘이 동일 sink 에 들어가는 *추가 가정* — axiom 2 에 implicit assumption "all mass species couple identically to n" 가 숨음. CDM 이 Higgs-blind 이면 Yukawa·v_H 비례 결합 가정 자동 위반.

## R5 — 3-regime 양립

σ_galactic / σ_cluster / σ_cosmic 3-regime 은 ρ 의 *조성 차이* (bary/DM/Λ ratio) 에 의존. 단일 σ = 4πG·t_P 가 세 regime 모두 작동하려면 "ρ 의 종류와 무관, total energy density 만이 sink rate 결정" 가정 필수. 이 universality 는 axiom 외부 hidden assumption (mass species blindness). regime 별 σ 다르면 hidden DOF +2.

## R6 — 관측 anchor mass scale 불일치

RAR 의 a₀ 는 SPARC photometric M_*/L (stellar mass, mostly H/He) + HI gas. BBN η_b 는 baryon number density (proton + neutron). Cassini PPN 은 Sun mass (electron 무시 가능). 세 anchor 의 ρ 가 *동일 σ 에 동일 방식* 으로 들어간다는 가정의 정당성 미증명. cross-anchor consistency 가 우연 일치라면 prediction 이 아닌 retro-fit.

## R7 — 재정의 비용

axiom 2 의 ρ 를 SM 입자 단위 (Yukawa-weighted, QCD-dressed, dark sector separated) 로 재정의 시: (i) axiom 2 텍스트 직접 수정 → [최우선-1] "지도 제공" 위험 영역, 유도 경로 사전 고정 위험. (ii) mass spectrum 13~17 DOF 가 axiom 으로 흡수 → "zero free parameter" 슬로건 폐기. (iii) 4-pillar (RAR/BBN/Cassini/Λ) 모두 새 ρ 정의 하에 재도출 의무 — 8인 분산 Round 10 풀세션 + 검증 라운드 추가. 비용 무겁다.

## R8 — 재정의 효과

성공 시: (a) a₀ 의 ρ 단위 명시 → R3 의 QCD/Higgs 모호성 해소 → hidden DOF -1. (b) dark sector mass-generation 별도 명시 → R4 implicit assumption 명시화 → -1. (c) 3-regime universality 가정 명시화 → R5 의 -2 중 -1 회수. 그러나 (d) Higgs sector 의 13 DOF 흡수로 +13. 순효과 -3 vs +13 = **net +10 hidden DOF**. PRD Letter 진입조건 (Q17 OR Q13+Q14) 더 멀어짐.

---

## §최종판정

**(B) 재정의 필요 + 비용 ≥ 효과 → 정직 disclosure 로 한정**

사유:
- R7 의 비용 (axiom 텍스트 수정 + Higgs 13 DOF 흡수) 이 R8 의 효과 (모호성 -3) 를 초과
- [최우선-1] 위반 risk: axiom 직접 수정은 분산 8인 독립 도출 정신 훼손
- 현실적 해법: paper §6 limitations 에 "ρ_m 는 FLRW background macroscopic energy density 로 해석되며, Higgs mechanism 및 QCD binding 의 micro-level 분해는 본 framework 의 scope 외" 단어 수준 명시
- Round 10 안건 등재는 *재정의가 아니라 disclosure 문구 합의* 로 한정

## §hidden DOF 영향

현재 9-13 → 옵션 (B) 채택 시 **9-14** (R1 모호성 명시 disclosure 가 +1 인정).
옵션 (A) 채택 시: 표면 -3, 실질 +10 (Higgs 흡수) → **19-23**, PRD Letter 자격 박탈.
옵션 (C) 단어 명시만으로는 R3/R4/R5 의 silent assumption 미해소 → **부정직**, 권고 안 함.

## §glob optima 회복 path 영향

옵션 C portfolio (0.55) 와의 관계: portfolio 0.55 는 "ρ 정의 통일" 가정 위에서만 성립. 옵션 (B) disclosure 채택 시 portfolio 점수에 직접 영향 없음 (limitations 명시는 점수 항목 외). 옵션 (A) 채택 시 zero-parameter pillar 붕괴 → portfolio 점수 0.55 → ~0.30 추정. **옵션 (B) 가 portfolio 보존**.

## §분산 8인 Round 10 안건 (정합)

- 안건 제목: "axiom 2 ρ_m 정의 명시 disclosure 문구 합의"
- 결정 사항: §6 limitations 에 1~2 문장 추가 가부
- 금지: axiom 본문 수정, mass spectrum DOF 흡수, σ 재정의
- [최우선-1] 준수: 수식 추가 0건, 단어 수준 disclosure 만

---

정직 한 줄: 본 세션은 *방향* 만 식별. 실제 disclosure 문구 작성과 채택은 분산 8인 Round 10 의무이며 본 single-session reviewer 는 트리거 권한 없음.
