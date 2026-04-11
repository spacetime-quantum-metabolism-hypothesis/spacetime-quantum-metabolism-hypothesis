# base.l7.command.md — L7 Phase-7: Submission + DR3 Response + Theory Phase-2

> 작성일: 2026-04-11. L6 Scenario B 확정 이후 설계.
> 사용자 confirm 전부 생략. 묻지 말고 끝까지 자동 진행. 언어는 Python.

---

## 실행 명령

```
/bigwork-paper base.l7.command.md 에 기재된 L7 JCAP 제출 +
DR3 대응 + CMB 완전 검증 + 이론 Phase-2 파이프라인을
끝까지 수행. 사용자 confirm 전부 생략. 묻지 말고 진행. 언어는 Python.
base.l6.result.md, simulations/l6/, paper/, base.md, CLAUDE.md,
refs/l6_*.md 전부 참고. L7 이름으로만 신규 파일 기록.
```

---

## 근본 목적 (L6 결과 → L7 처방)

**L6 정직한 자기평가에서 출발**:

L6 종료 시점 판정:
- **시나리오 B 확정**: JCAP급 정직한 현상론 + DR3 falsifier
- A12 (0-param) marginalized Δ ln Z = +10.769 — 최고 evidence
- C28 full marginalization 후 A12에 역전 (2.14 nats 뒤짐)
- amplitude-locking: Q17 부분 달성 (완전 유도 아님)
- S8/H0: 구조적 미해결 (μ_eff ≈ 1 한계)
- hi_class: 미설치 → K19 provisional 상태
- DESI DR3: 미공개 → 핵심 falsifier 대기 중

**L7 목표**:
"JCAP 현상론 논문 제출" (보장 경로) +
"DR3 결과에 따른 PRD Letter 업그레이드 또는 honest negative update" (조건부 경로)

| L6 비판 | L7 처방 | 우선순위 |
|---------|---------|---------|
| hi_class 미검증 (K19 provisional) | hi_class 설치 + 정식 CMB 검증 | ★★★ |
| JCAP 제출 미완 | 논문 최종 polish + 제출 | ★★★ |
| DR3 미공개 (핵심 falsifier) | DR3 자동 대응 파이프라인 가동 | ★★★ |
| amplitude-locking 미유도 | UV completion 시도 OR 포기 선언 | ★★ |
| S8/H0 미해결 | 섭동 레벨 새 채널 탐색 OR 한계 문서화 | ★★ |
| C11D beyond CMB 미검증 | Euclid/SKAO 예측 계산 | ★ |

### L6 → L7 분기점: 8인 패널 합의

2026-04-11 8인 패널 결론:
- 이론 완성도: 30% (동기부여 O, 유도 X)
- 관측 성적: 85% (DR2 기준, DR3 미정)
- 현재 가치: "JCAP 논문 1편 + DR3 falsifier"
- PRD Letter 조건: Q17 완전 달성 OR DR3 α시나리오 + Q14 동시

---

## 프로세스 규칙 (L6 Rule-A/B 그대로 승계)

- **Rule-A**: 이론 확장 → 8인 순차 검토 (병렬 금지)
- **Rule-B**: 코드 → 4인 순차 코드리뷰, 태그 필수

---

## Kill / Keep 기준 (L7 신규, 실행 전 고정)

**실행 시작 전** `refs/l7_kill_criteria.md` 에 아래 기준 고정.

### L7 KILL 조건

| ID | 조건 | 결과 |
|----|------|------|
| **K21** | JCAP reject (not major-revision): peer review 후 | 저널 재선택 후 재제출 |
| **K22** | DESI DR3: w_a > 0 (≥ 2σ) — SQMH wₐ < 0 예측 falsified | honest negative result 논문 작성 |
| **K23** | hi_class 정식 CMB: Δχ²_CMB > LCDM+6 (K19 formal fail) | C11D/C28 KILL — A12만 유지 |
| **K24** | UV completion 시도 후 8인팀 "수학적 불가능" 판정 | Theory 채널 포기, 현상론 브랜딩 확정 |
| **K25** | Euclid Y1 결과 (2026-2027): μ_eff 측정 μ < 0.95 OR > 1.1 → 전원 구조 불일치 | 성장섹터 falsified |

### L7 KEEP 조건

| ID | 조건 |
|----|------|
| **Q18** | JCAP accept 또는 minor revision |
| **Q19** | DESI DR3: w_a < 0 지속 ≥ 2σ (Q16 실현) |
| **Q20** | hi_class 정식 CMB: Δχ²_CMB ≤ LCDM+3 (K19 formal pass) |
| **Q21** | amplitude-locking 완전 유도 성공 (8인팀, Q17 완전 달성) |
| **Q22** | 우주론 외 채널 1개 이상: GW binary inspiral, CMB-S4 ISW, SKAO 21cm |

---

## 실행 순서

### Phase L7-0. 기준 고정 + 환경

- `refs/l7_kill_criteria.md` K21-K25, Q18-Q22 기재 후 저장
- `base.l7.todo.md` WBS 작성
- `simulations/l7/` 디렉터리 생성 (cmb/, theory/, submission/, dr3/, channels/)
- hi_class 설치 시도 (conda install hi_class 또는 git clone + compile)
  - 성공 시: L7-C 즉시 실행
  - 실패 시: "hi_class not available" §8 기재 후 L7-S 우선

---

### Phase L7-C. hi_class 정식 CMB 검증 (K19 formal)

> 4인 코드리뷰 필수.

#### L7-C1. hi_class 설치 및 C11D 파라미터 래퍼

`simulations/l7/cmb/run_hiclass_C11D.py`:
- hi_class disformal 파라미터: B_0, n_B (A'=0 → B_0만)
- C11D L5 posterior mean: Om=0.3095, h=0.6776, lam=0.8872
- 출력: C_l TT/EE/TE vs Planck 2018 likelihood
- K23 판정: Δχ²_CMB ≤ LCDM+6 → formal PASS

산출: `simulations/l7/cmb/cmb_C11D_hiclass.json` + K19 final verdict

#### L7-C2. C28 hi_class 검증

- C28 Maggiore-Mancarella: hi_class non-local gravity module
- 미지원 시: EFTCAMB 대안 시도
- 실패 시: "C28 full CMB 미검증" §8.9 명시

#### L7-C3. CMB 결과 논문 반영

- §7.6 μ_eff 표: K19 status를 "provisional" → "formal PASS/FAIL"로 업데이트
- §8.9: hi_class 검증 결과 추가

---

### Phase L7-S. JCAP 논문 제출 (보장 경로)

> L7의 1순위 목표. hi_class 결과 무관하게 진행.

#### L7-S1. 논문 최종 polish (4인 코드리뷰 + 8인 이론 검토)

체크리스트:
- [ ] §1 Abstract: L6 marginalized Δ ln Z 반영 (C11D 결과 포함)
- [ ] §7.2: L6 완전 marginalized 표 + L5 fixed-θ 표 병기 (혼동 방지)
- [ ] §7.5: Occam 실측값 (A12 > C28 by 2.14 nats) 확정 기재
- [ ] §8.4: "C28 파라미터 정당화 불가" Phase-6 실측 확인 기재
- [ ] §8.7: DESI DR3 대기 중 (falsifier 예측 2.9-3.9σ) 명시
- [ ] §8.9: 8인 패널 "주장 가능/불가" 목록 최종 확인
- [ ] §8.10: hi_class 미검증 공시 (provisional → formal pending)
- [ ] Appendix: 완전 marginalized 코드 + seed + 재현 지침

8인팀 최종 검토: 논문 전체 "주장 가능" 위반 여부 스캔.

#### L7-S2. 저널 제출

- JCAP 타깃 확정 (L6-T3 8인 합의)
- 제출 전: arXiv preprint 동시 업로드
- 산출: arXiv 번호 + JCAP submission ID

#### L7-S3. Reviewer 대응 프레임워크 사전 준비 (8인팀)

예상 심사 질문과 답변 사전 작성:

| 예상 질문 | 사전 답변 |
|---------|---------|
| "왜 erf가 SQMH인가?" | "zero-parameter 구현 예시. 실제 대표 모델은 C11D disformal" |
| "amplitude-lock 유도 안 됨" | "theory-motivated normalization consequence로 명시. §8.4 참조" |
| "C28이 SQMH 모델인가?" | "아님. Maggiore-Mancarella 독립 이론. SQMH와 현상론 일치만 주장" |
| "S8/H0 미해결" | "구조적 한계 §8.2-8.3 정직 기재. μ_eff≈1 구조임을 선언" |
| "hi_class 미검증" | "provisional K19. L7에서 formal 검증 예정. §8.10 공시" |

산출: `refs/l7_reviewer_prep.md`

---

### Phase L7-DR3. DESI DR3 대응 (DR3 공개 즉시 트리거)

> DR3 공개 시 자동 실행. 현재 준비만.

#### L7-DR3-1. 자동 재실행 (L6-D1 스크립트 가동)

```bash
bash simulations/l6/dr3/run_dr3.sh
```

추가 실행:
- C11D, A12, C28 모두 DR3 데이터로 재피팅
- DR3 vs L5 diff 전 채널 (BAO/SN/CMB/RSD) 개별 출력
- 시나리오 α~ε 자동 분류

#### L7-DR3-2. DR3 결과에 따른 분기

**α 시나리오** (w_a < 0 강화, ≥ 3σ C11D/C28 분리):
- 8인팀 긴급 소집
- PRD Letter 초안 작성 (L7-P 즉시 실행)
- arXiv preprint 업데이트

**β 시나리오** (w_a < 0 유지, < 2σ 분리):
- JCAP 논문 "DR3 consistent" 절 추가
- §8.7 업데이트: "DR3에서 유지 확인"

**γ 시나리오** (w_a ≥ 0 또는 역전):
- K22 발동: honest negative result 절 작성
- "SQMH wₐ < 0 예측이 DR3에서 falsified" 명시
- JCAP 논문을 "negative result + 방법론" 논문으로 전환
- Phase 8 재설계 필요

**δ 시나리오** (phantom crossing w < -1):
- K22 + SQMH L0/L1 구조 falsified
- Phase 8 = UV 재설계 또는 프로젝트 종료 판단

산출: `simulations/l7/dr3/dr3_L7_response.json` + `refs/l7_dr3_verdict.md`

---

### Phase L7-T. 이론 Phase-2 (8인팀 필수, 조건부)

> L7-S (제출) 완료 후 시작. 제출 지연 원인 금지.

**분기 조건**: L6-T1 결과가 "완전 유도 불가" 판정이면
아래 두 경로 중 8인팀이 선택.

#### 경로 A: UV Completion 시도 (Q21 목표)

**목표**: σ = 4πG t_P 와 Γ₀ 를 플랑크 스케일 양자중력에서 도출.

접근:
1. **Loop Quantum Cosmology (LQC) 연결**: 홀로노미 보정 E²(z)와 SQMH E²(z) 비교. Taveras 2008 / Agulló-Singh 2015 LQC background 방정식과 형태 일치 분석.
2. **Causal Dynamical Triangulations (CDT)**: Ambjorn-Jurkiewicz-Loll 격자에서 n̄(a) 추출 시도. σ effective 값이 SQMH 연속방정식과 일치하는가?
3. **GFT condensate**: Group Field Theory 응축 밀도 n̄ = ⟨φ†φ⟩ — dn̄/dt 형태가 SQMH L0와 동형인가?

8인팀 검토 후 판정:
- "유도 가능" → 수식 명시 + §2 UV completion 절 추가 → PRD Letter 가능
- "형태 유사 (동형성만)" → "LQC-inspired template" 격하 → JCAP 유지
- "무관" → Theory 채널 포기, Phase-8에서 새 접근

산출: `refs/l7_uv_completion.md`

#### 경로 B: "정직한 현상론" 브랜딩 확정 (L6-T3 확장)

L6 8인 합의를 논문 Abstract/§1/§9에 명시적으로 반영:
- "SQMH motivates but does not derive the dark energy template"
- "A12 is a zero-parameter phenomenological proxy, not a first-principles prediction"
- "Falsifiability: DR3 at 2.9-3.9σ, Euclid at Xσ"

경로 B는 항상 병행 진행 (경로 A 실패 시 fallback).

---

### Phase L7-X. 새 채널 탐색 (8인팀, 탐색적)

> L7-S 완료 후. 제출 지연 원인 금지.

**목적**: 우주론 채널 1개 의존에서 벗어나 다채널 검증.
성공 시 "5개 프로그램 통합" 재주장 가능성 열림 (현재는 금지).

#### L7-X1. GW 연성계 inspiral 채널

C11D disformal: B(φ) = B_0 → GW 전파 속도 c_T²/c² = 1/(1-B ρ_φ)
- LIGO O4 / ET 설계 감도에서 B_0 제약 도출
- SQMH wₐ < 0 에 해당하는 B_0 범위가 GW 관측과 호환?
- 8인팀: GW 제약이 C11D를 추가 제약하는가, 아니면 이미 GW170817이 A'=0 강제?

#### L7-X2. CMB-S4 / Simons Observatory ISW 채널

μ_eff ≈ 1 이지만 E²(z) 변화 → ISW effect 미세 변화
- C11D, A12 ISW power spectrum 계산 (hi_class 필요)
- CMB-S4 2027 감도에서 LCDM vs SQMH 구분 가능한가?

#### L7-X3. SKAO 21cm BAO 채널

SKAO Phase-1 (2027-2030) 21cm BAO:
- C11D/A12 E²(z) 예측 vs SKAO sensitivity
- DR3 에 이어 2차 falsification window

8인팀 평가: 각 채널이 "우주론 채널 1개" 한계를 극복하는가?

산출: `refs/l7_new_channels.md` + `simulations/l7/channels/`

---

### Phase L7-G2. S8/H0 구조적 한계 재탐색

**목적**: L6에서 Q15 전원 실패 (μ_eff ≈ 1) → L7에서 새 접근 가능한가?

#### L7-G2-1. 섭동 레벨 새 채널 (8인팀)

접근: C11D disformal에서 β_D ≠ 0 (dark-only coupled) 극한 탐색
- baryon과 분리된 DM-φ 결합: G_eff/G = 1 + 2β_D²
- Cassini 통과 + S8 개선 동시 가능한 β_D 범위?
- 경고 (CLAUDE.md): β_D ~ 0.107이면 S8 6.6 chi² 악화. β_D ≪ 0.1 필수.

8인팀 판정: "구조적으로 가능" vs "한계 확인, L7 포기"

#### L7-G2-2. H0 tension: early DE 채널 탐색

C11D early quintessence 가능성:
- lam 값에 따른 z > 3 E(z) 변화
- EDE (Early Dark Energy) 모방 여부
- Planck + BAO + H0 joint에서 h 선호값 변화

8인팀: H0 개선 가능하면 §8.2 업데이트. 불가능하면 "구조적 한계 확정" 명시.

---

### Phase L7-P. PRD Letter 업그레이드 경로 (조건부)

> **발동 조건**: 아래 중 하나 이상 충족 시만 실행.
> - Q21: amplitude-locking 완전 유도 성공 (8인팀)
> - Q19 + Q20 동시: DR3 확인 + hi_class formal PASS
> - Q22: 새 채널 ≥ 2개 실증

미충족 시 L7-P 실행 금지 — JCAP 제출로 충분.

#### L7-P1. PRD Letter 초안 (3-4 pages)

구조:
- §1 (0.5p): SQMH one-sentence + DR3 prediction
- §2 (1p): Zero-parameter evidence (A12 Δ ln Z = +10.77, 조건 충족 시 UV anchor)
- §3 (1p): DR3 OR 새 채널 결과
- §4 (0.5p): Implications + DR3/Euclid outlook
- Supplemental: 전체 L6 데이터

---

## 산출물 체크리스트

| 파일 | 조건 |
|------|------|
| `refs/l7_kill_criteria.md` | 실행 전 고정 필수 |
| `simulations/l7/cmb/cmb_C11D_hiclass.json` | hi_class 설치 성공 시 |
| `refs/l7_reviewer_prep.md` | 제출 전 필수 |
| arXiv + JCAP submission | L7-S 주요 산출 |
| `refs/l7_dr3_verdict.md` | DR3 공개 후 |
| `refs/l7_uv_completion.md` | L7-T 경로 A 시도 후 |
| `refs/l7_new_channels.md` | L7-X 탐색 후 |
| `base.l7.result.md` | 실시간 업데이트 |

---

## 시나리오 판정

**시나리오 α — PRD Letter** (조건: Q19+Q20+Q21 or Q22):
DR3 확인 + hi_class pass + UV completion OR 새 채널 ≥ 2
→ PRD Letter 제출. "Theory-motivated zero-parameter dark energy"

**시나리오 β — JCAP 게재** (기본 시나리오):
히_class pass + JCAP minor revision
→ "Honest falsifiable phenomenology" 게재 완료

**시나리오 γ — JCAP + DR3 negative update**:
DR3 w_a ≥ 0 → JCAP에 "DR3 update" 절 추가 + honest negative record

**시나리오 δ — Project pivot**:
K22 + K23 동시 발동 → Phase 8 = 새 이론 또는 프로젝트 종료
"Falsified dark energy model" 논문으로 기록 (이것도 학술 기여)

---

## 금지 사항 (L6 승계 + L7 추가)

**L6에서 승계**:
- fixed-theta evidence를 marginalized 값으로 발표 금지
- C28을 "SQMH 모델"로 주장 금지
- hi_class 미검증 상태에서 "full CMB consistent" 주장 금지
- amplitude-locking "이론에서 유도됨" 주장 금지

**L7 추가**:
- K22 (DR3 falsified) 무시하고 계속 주장 금지
- 심사자 비판을 회피용 언어로 덮기 금지
  ("이 점은 향후 연구에서..." 남발 시 §8에 정직 기재로 대체)
- hi_class 실패를 "잠정적 통과" 언어로 포장 금지
- L7-P 조건 미달 상태에서 PRD Letter 제출 시도 금지
- "DR3에서 확인될 것" 확언 금지 (예측: "2.9-3.9σ 구분 가능" 만 허용)
- `base.md` 원본 수정 금지

---

## 우선순위 (현실적 실행 순서)

```
즉시 (이론 분석, 병렬 가능):
  L7-0 기준 고정
  hi_class 설치 시도 (L7-C, 독립)
  L7-S1 논문 polish (C11D 완료 후)

병렬 (수주):
  L7-S2 JCAP 제출 ←→ L7-T 경로 B (현상론 브랜딩)
  L7-X 새 채널 탐색 (탐색적, 제출 blocking 아님)

DR3 공개 즉시 (수시간, 기계적):
  L7-DR3 자동 실행

제출 완료 후 (조건부):
  L7-T 경로 A (UV completion)
  L7-P (PRD Letter, 조건 충족 시)

Euclid Y1 결과 이후:
  K25 판정 + Phase 8 방향 결정
```

---

## 핵심 현실 인식

8인 패널 (2026-04-11) 합의 한 줄 요약:
**"지금은 '유망한 후보, 검증 중'. JCAP 논문 1편이 현재 정직한 가치."**

L7은 그 논문을 제출하는 것이 1순위.
나머지는 DR3과 hi_class 결과에 달려있다.
과장 없이, 결과가 나오는 대로 대응한다.

---

**문서 이력**: 2026-04-11 작성.
L6 Scenario B (JCAP 정직한 현상론) → L7: 제출 + DR3 대응 + 조건부 업그레이드.
Rule-A (8인 이론) + Rule-B (4인 코드리뷰) 승계.
