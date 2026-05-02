# L419 NEXT_STEP — 8인팀 다음 단계 설계

**목적**: η_Z₂ ≈ 10 MeV scale 의 a priori 도출 시도 (Foundation 4 = Z₂ SSB), β_eff = Λ_UV/M_Pl 의 정확 numeric verify. 본 NEXT_STEP 은 *방향만* 제시 — 구체 수식/유도경로 hint 는 [최우선-1] 에 따라 금지.

**산출 좌표**:
- §2.4 row 4 (Foundation 4) 의 "η ≲ 10 MeV 제약" 을 priori 도출 path 로 강화하거나 *명시적 caveat* 추가.
- §4.1 row 2 narrative 를 단일-scale margin 표현으로 정정.
- §6.1 row 새로 등재: η_Z₂ priori 도출 OPEN 명시.

---

## 1. 방향 (수식·유도경로 미제공)

### D1 — η_Z₂ scale 의 priori path 후보 enumeration
- **방향**: Foundation 4 (Z₂ SSB) 의 potential 형태에서 vev 가 *어떤 SM scale 에 의해 결정되는가* 의 후보 enumeration.
- **탐색 영역 (방향만)**:
  - 차원 분석에 의한 *기하 평균* 후보 (axion 계열의 √(f × m) 패턴 일반화).
  - QCD-induced effective potential (instanton 또는 chiral condensate 결합).
  - Cosmological constant scale 결합 (Λ_obs × M_Pl 의 power 조합).
  - See-saw 형태 (m_ν × M_high 의 power).
- **금지**: 특정 Lagrangian 형태 지정, vev 공식 작성, "이 mechanism 이 옳다" 결론.
- **검증 수단**: L419 simulation [3] 의 11 후보 표 — 0.02 dex 내 매치 발견은 *후보* 이지 derivation 아님.

### D2 — β_eff 정의 명시화
- **방향**: paper §4.1 row 3 의 β_eff = Λ_UV / M_Pl 에서 Λ_UV 의 *해석* 을 §2 또는 §6.1 에 명시. 본 simulation [1] 결과 (full M_Pl → 90 MeV, reduced → 18 MeV) 가 η_Z₂ 와 동일 scale 임을 명시 정직.
- **금지**: 새로운 Λ_UV 도출 경로 작성. "Λ_UV ≡ η_Z₂" 라는 *정의* 의 명시화만 허용.

### D3 — 두 mechanism redundancy disclosure
- **방향**: §4.1 row 2 narrative 정정. 현재 "η ≫ T_BBN + β_eff² 두 보호" 는 *동일 scale 의 두 표현* 임. "single-scale 17-dex margin" 또는 동치 정직 표현으로 변경.
- **검증**: L419 simulation [2] B-only 단독 ΔN ≤ 3.8e-18 << 0.17.

### D4 — PASS_STRONG 등급 유지 정당화
- **방향**: §6.5(e) 의 "η_Z₂ scale, Λ_UV/M_Pl" 을 추가 axiom 입력으로 분류한 기존 분류와 정합되게, BBN PASS_STRONG 를 *structural margin* (B-only 17 dex) 이 보장한다는 1 단락 추가.
- **금지**: 등급 자체 변경 (격상/강등) 결정 — 본 NEXT_STEP 범위 외.

### D5 — 5번째 axiom (Causet/GFT) 결정과 연계
- **방향**: §2.5 5번째 축 미정 상태 — Foundation 4 (Z₂ SSB) 의 micro-derivation 이 어느 5번째 축 후보와 더 호환되는지 future plan 등재.
- **금지**: 어느 5번째 축이 옳다는 결정.

---

## 2. 8인팀 합의 권고 (이론 클레임 — Rule-A 필요)

| # | 권고 | 우선 | 비고 |
|---|------|------|------|
| R1 | §4.1 row 2 narrative 를 single-scale margin 표현으로 정정 | 높음 | A2/A5 공격 직접 답변 |
| R2 | §6.1 한계 표에 "η_Z₂ priori OPEN" 신규 row 추가 | 높음 | A1/A4/A7 공격 답변 |
| R3 | β_eff 정의에 Λ_UV ~ η_Z₂ identification 명시 | 중간 | A2 공격 답변 |
| R4 | PASS_STRONG 등급 유지 (B-only 17 dex margin 정당화) | 중간 | A8 권고 수용 |
| R5 | √(m_e × Λ_QCD) candidate 표를 *후보 only* 로 등재 | 낮음 | derivation 으로 over-claim 금지 |

## 3. 4인팀 코드리뷰 권고 (Rule-B 필요)

- **L419 run.py** 의 다음 항목 4인팀 자율 분담 검토:
  - constants 정확성 (PDG 2024 vs paper 인용값)
  - Boltzmann suppression 공식 (m/T)^{3/2} exp(-m/T) 의 적용 영역
  - Gamma/H 의 dimensional 근사 한계 (loop factor, log term 누락)
  - candidate scale enumeration 의 누락 (ChPT, dilaton, etc.)
- 검토 완료 전 paper §4.1, §6.1 수정 금지 (CLAUDE.md L6 규칙).

## 4. 정직 한 줄

> 다음 단계는 (a) η_Z₂ priori 도출의 OPEN 명시 등재, (b) β_eff 의 Λ_UV ~ η_Z₂ identification 명시, (c) "two-mechanism redundancy → single-scale 17-dex margin" narrative 정정. 등급 변경 결정은 본 단계 범위 외.
