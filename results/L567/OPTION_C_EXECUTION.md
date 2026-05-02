# L567 — 옵션 C (arXiv D 격상) 실행 plan

> 작성: 2026-05-02. 단일 작성 에이전트 (Rule-A 8인 / Rule-B 4인 라운드 *미실행*).
> 입력: L565 §2 권고 (옵션 C, 결합 acceptance 0.55, 회복률 81%, trust MEDIUM 감점) + L566 D2 사전등록 (priori 회복 마지막 방어선) + L563 fabrication 확정 + L564 git forensics + L562 D4 박탈 + L549/L552 Rule-A 박탈.
> CLAUDE.md 정합: paper edit 0건, claims_status edit 0건, simulations/ 신규 코드 0줄, 신규 수식 0줄, 신규 파라미터 0개. [최우선-1]/[최우선-2] 준수 (이론 도출 0건). 결과 왜곡 금지 — fabrication / 박탈 disclosure 정직.

---

## §0 정직 한 줄 (서두)

본 L567 은 L565 옵션 C (arXiv D 격상) 의 *실행 단계 만* — 저널 선정 / 변환 plan / 8인 Rule-A 의무 disclosure (fabrication 본문 명시 포함) / DR3 도착 시 revision protocol / Companion B cross-ref 변경 — 을 정직 산출하며, 어떤 항목도 paper / claims_status / arXiv 직접 트리거가 아니고, 채택은 *모두* 후속 Rule-A 8인 라운드 결정에 종속한다. 본 문서는 acceptance 산술 재계산 / 옵션 재비교를 시도하지 않으며 (그 영역은 L565 가 권한), 변환 / disclosure / timeline 미세 조정만 다룬다.

---

## §1 저널 선정 + 사유

### §1.1 후보 저널 평가 매트릭스

| 저널 | scope 정합 | acceptance 추정 | reviewer overlap risk (MNRAS retract pool) | timeline (제출→출간) | trust 회복 가중치 |
|---|---|---|---|---|---|
| **PRD (Phys. Rev. D, regular article)** | cosmology phenomenology, DR3 falsifier, ρ-corrected 채널 → **HIGH** 정합 | 28–35% (PRD regular 평균 ~30%) | LOW (PRD reviewer pool 과 MNRAS-γ pool 거의 비공유; 단 SQMH-aware reviewer 2–3명 cluster 잔존) | 4–6mo review + 2–3mo production | MEDIUM (PRD = high-rigor signal) |
| **JCAP** | cosmology 전문, DR3 / DE 채널 → **HIGH** 정합 (PRD 대등) | 32–40% (JCAP 평균 ~35%) | LOW–MEDIUM (JCAP 와 MNRAS-γ pool 일부 공유 — DESI WG 출신 reviewer ~10–15%) | 3–4mo review + 1–2mo production | MEDIUM (JCAP = open-access cosmology 표준) |
| MNRAS (재제출) | galactic + cosmology — scope 정합하지만 **brand-bias 누적** | 18–25% (재제출 + fabrication brand 페널티) | **HIGH** (동일 pool, L563 retract 추적 가능) | 4–6mo + revision 1–2 round | LOW (MNRAS 재진입 시 trust 회복 거의 0) |
| ApJ | cosmology + galactic, scope 정합 | 25–32% (ApJ 평균 ~28%) | MEDIUM (ApJ ↔ MNRAS pool 부분 공유) | 5–7mo review (ApJ 평균 길음) | MEDIUM |
| CQG | quantum gravity, foundations — SQT axiom 측면 정합, **DR3/관측 phenomenology scope 미달** | 20–28% | LOW | 5–8mo (CQG review 길음) | MEDIUM-LOW (관측 paper 로 부적합) |

### §1.2 권고: **JCAP (1순위) > PRD (2순위) > ApJ (3순위, fallback)**

**L565 §2.3 의 PRD 1순위 / JCAP 2순위 권고를 본 L567 에서 *재정렬 권고*** — 사유:

1. **fabrication disclosure 부담 vs scope match**:
   - PRD regular 는 *"high-novelty"* 명시 요구 — Q17 partial / Hidden DOF 9–13 disclosure 가 novelty 평가에서 불리 (fabrication 발견 disclosure 가 reviewer 의 first-impression 을 음성 편향).
   - JCAP 는 *"phenomenology + falsifier"* track 친화 — DR3 preregistered falsifier (wa>−0.5 KILL) 가 JCAP scope 의 핵심 자산.
   - L565 §2.3 의 "PRD Letter 진입 영구 차단" 은 PRD regular 도 *high-novelty 요구* 에서 부분 적용 가능 → JCAP 가 더 안전.

2. **review timeline 단축**:
   - JCAP 평균 review 3–4mo vs PRD 4–6mo. DR3 (2027 Q2) 도착 전 first round 종료 가능성 JCAP 가 높음 (§4 protocol 정합).

3. **acceptance 중앙 추정**:
   - JCAP 35% × Companion B 0.42 ↔ ρ=0.10 → 결합 acceptance ≈ 0.59 (L565 §1.2 옵션 C 낙관 0.62 와 보수 0.46 사이).
   - PRD 30% 와의 차이는 Δ ≈ 0.03 — 산술 차이 작지만 trust / timeline 가중치에서 JCAP 우위.

4. **PRD 권고 유지 시 조건**:
   - Rule-A 8인 라운드가 "novelty 평가 통과" 합의 시 PRD 1순위 환원. 합의 실패 시 JCAP.
   - 본 L567 은 *재정렬 권고* — 최종 결정은 Rule-A 종속.

5. **MNRAS 재제출 명시 권고 안 함**: L565 옵션 B 가 KILL 된 것과 동일 사유 (brand-bias, F2 narrative 재구축 불가).

### §1.3 reviewer overlap 보정

- JCAP / PRD pool 과 MNRAS-γ retract pool 의 겹침은 ρ ≈ 0.10 (DESI WG 일부 + cosmology 소수). overlap 보정 acceptance 는 Companion B 와 결합 시 L565 §1.2 옵션 C 산식 그대로 유효.
- *추가 위험*: SQMH-brand-aware reviewer 2–3명 cluster — JCAP 에서 desk-reject 가능성 ≈ 5–8%. PRD 에서 ≈ 3–5%. 본 위험은 acceptance 추정 하한에 이미 반영.

---

## §2 변환 plan (arXiv D preprint → JCAP/PRD paper)

### §2.1 추가 의무 (preprint 20p → peer-review paper)

| 영역 | preprint 현재 | peer-review 변환 후 의무 |
|---|---|---|
| 본문 분량 | ~20p | 25–32p (JCAP 표준), 28–35p (PRD regular) |
| Methods §  | 압축 | full methods 분리 — 데이터 처리 / fit pipeline / convariance / systematics 4 절 |
| Figures | 4–5점 | 8–12점 — DR3 falsifier 채널 visualization 2점 추가, ρ-corrected 8.87σ residual plot, N_eff=4.44 BAO-removed posterior |
| Appendix | 1점 (reproducibility) | 3–5점 — A: full claims_status v1.x snapshot, B: hidden DOF 9–13 enumeration 표, C: fabrication disclosure (§3 참조), D: DR3 protocol, E: C28 Maggiore-Mancarella 독립성 증명 |
| Abstract | 200 단어 | 250–300 단어 — "honest headline" 6-bullet + falsifier 명시 + Hidden DOF disclosure 명시 |
| References | ~40개 | 70–100개 — Verlinde 2017, Maggiore-Mancarella, DESI DR2 / DR3, Sakstein-Jain, hi_class, CobayaSampler 전체 인용 보강 |

### §2.2 PASS_MODERATE 4 채널 + N_eff=4.44 (8.87σ ρ-corrected) 강도 유지

- **PASS_MODERATE 4 채널** (a₀ factor-≤1.5 / RAR sub-row PASS_STRONG / BTFR / 1 추가 — L482 audit 대로): §3 (verification) 에서 표 1점 + 본문 4 paragraph 으로 **강도 유지** (격하 0).
- **N_eff=4.44 (8.87σ ρ-corrected)**: §5 (pre-registered falsifiers) 에서 1 sub-section + figure 1점. *BAO 채널 제거 후 재 fit 의무* 명시 (L546 R10-Exec-B 인용). *"ρ-corrected" 정의 별도 footnote* — covariance correction 의 정확한 출처 + 재현 script 인용.
- **Hidden DOF disclosure**: §6 Limitations 에서 9–13 DOF 표 + Verlinde degeneracy + Bullet 잔존 + k_eff≈3 + a₀ universality K=1/4 (L546 §2.2 §6 와 동일 항목 7개) — *abstract line 3* 에 짧게 재명시.

### §2.3 Q17 amplitude-locking partial 의 §2 위치 격상

- L565 §2.3 / L546 의 Q17 partial 은 preprint 에서 §3 ("DR3 readiness") 에 위치. **peer-review paper 에서는 §2 (theoretical framework) 로 격상** — 사유:
  1. peer reviewer 가 *theoretical novelty* 를 §2 에서 평가. Q17 partial (Δρ_DE ∝ Ω_m) 의 *부분 도출* 이 §2 에 있어야 phenomenology 자산이 명시.
  2. 격상 시 의무 disclosure: "**partial derivation** — exact coefficient = 1 은 E(0)=1 정규화 귀결이며 dynamical derivation 아님" (CLAUDE.md L6 재발방지 직접 인용).
  3. K20 미해당 명시 — "amplitude-locking 은 이론에서 *유도됨* 이라 주장하지 않음" (CLAUDE.md 정합).
  4. C28 Maggiore-Mancarella 독립 이론 명시 — "SQT 가 C28 모델이라 주장하지 않음, phenomenological 일치만 주장" (CLAUDE.md L6).
- 격상 후 §3 은 "verification" (PASS_MODERATE 채널) 단일 주제로 정리. 구조 단순화.

### §2.4 변환 작업 단위 / 분담

- 4인 Rule-B 코드리뷰: figure 8–12점 재생성 script + appendix C/D 재현 / data load / chi² pipeline.
- 8인 Rule-A: §2 (Q17 격상), §6 (limitations), abstract, fabrication disclosure (§3 본 문서), C28 독립성 §appendix E.
- 변환 기간: L565 timeline 의 2026-06 ~ 07 (8주) 유지.

---

## §3 8인 Rule-A 필수 항목 (fabrication disclosure 포함)

> 본 §3 은 *어떤 항목이 8인 Rule-A 회의에서 합의·문서화되어야 하는가* 의 list 만. 합의 결과 자체는 본 L567 이 결정하지 않음.

### §3.1 Cross-mention 의무 4건

1. **L549 P3a 박탈 cross-mention**:
   - Appendix C ("priori derivation history") 에서 P3a (Path-3 axiom-only priori 시도) 가 Rule-A 8인 라운드에서 박탈된 사실 명시.
   - 박탈 사유 1줄 — 박탈 protocol (L549 P3A_RULE_A.md) 인용.
2. **L552 RG 패키지 박탈 cross-mention**:
   - Appendix C 동일 절. RG 패키지 (Renormalisation-Group axiom 화 시도) 가 Rule-A 박탈됨을 명시.
3. **L562 D4 박탈 cross-mention**:
   - Appendix C — D4 (primary holographic priori 경로) 박탈. 사유 (조건 4 falsifier 미명시 / 외부 framework 수입) 1줄 인용.
4. **L566 D2 사전등록 + 박탈 default cross-mention**:
   - Appendix C — D2 가 사전등록 단계에서 박탈을 기본 가정으로 둔 사실 (L566 §6) 명시. priori 회복 path 영구 종결 (L566 §5) 도 footnote 처리.

→ §3.1 종합: **paper 포지셔닝을 "priori 도출 모델" 에서 "falsifiable phenomenology with sector-selective coupling" 로 영구 전환** (L566 §5 권고 직접 상속). Abstract / §1 introduction 에서 priori 단어 사용 0건. *정의(definition) 또는 normalization choice* 로 표기.

### §3.2 fabrication disclosure (L563 발견)

- **Main MNRAS-γ 가 retract 되었음을 본문에 명시**: §1 ("scope and history") 에서 1 sub-section, Appendix C 에서 detail.
- **명시 항목**:
  1. L563 발견 (F1 narrative 정정 가능 / F2 §5.3 falsifier 채널 폐기 의무).
  2. MNRAS-γ 제출 보류 / retract 결정 (옵션 C 권고 = MNRAS-γ 보류, L565 §1.1).
  3. F2 §5.3 narrative ("framework rejects fabricated input") 의 SQT 본문 수입 0건 — 본 paper 는 F2 의존 0.
  4. F1 정정 (4-spot mismatch: 0/1000 → 0/200, RAR universality 철회, SPARC per-galaxy 0.427 dex spread 인용) 은 본 paper 본문에 *직접 반영* (L561 §7 권고 수입).
  5. fabrication 발견의 trust 영향 (L565 §1.3 −0.05 ~ −0.07) 명시 — 단, acceptance 추정에는 이미 반영되었음을 footnote.

### §3.3 L564 git untracked + active fabrication 90% confirmation disclosure

- **Appendix C 별도 sub-section** ("repository forensics"):
  1. L564 git forensics 결과 — git untracked 파일이 L539 시점 존재했음.
  2. *active fabrication* 90% confirmation (L564 conclusion) — passive error 가 아니라 의도적 수정 가능성 90% 평가 결과 명시.
  3. paper 저자가 본 발견을 disclosure 의무로 *자발적 보고* — reviewer 가 git history 에서 발견 시 trust 손실 더 큼 (L565 §2.2 옵션 B 박탈 사유와 정합).
  4. 본 arXiv-D-as-paper (JCAP/PRD) 의 모든 figure / table / chi² 는 *post-L564 상태* 에서 재생성됨을 4인 Rule-B cross-check 결과로 보증.
  5. claims_status v1.x snapshot (Appendix A) 에 git commit hash 영구 박제 — reviewer 재현 보장.

### §3.4 8인 Rule-A 회의 의제 (3.1 + 3.2 + 3.3 통합)

| 의제 | 합의 형식 | 박탈 트리거 |
|---|---|---|
| 1 priori 단어 사용 0건 합의 | 8/8 합의 | 1 인이라도 priori 표현 옹호 시 본 옵션 C 자체 재검토 |
| 2 fabrication disclosure 본문 위치 (§1 + Appendix C) 합의 | 6/8 이상 | <6/8 시 disclosure 강화 (Abstract 진입 의무) |
| 3 active fabrication 90% confirmation 자발적 disclosure 합의 | 8/8 합의 | <8/8 시 옵션 C 자체 KILL → 옵션 A (자발적 retract + 미제출) 후퇴 |
| 4 C28 Maggiore-Mancarella 독립성 명시 | 8/8 합의 | 1 인 반대 시 §appendix E 분량 확장 |
| 5 PASS_MODERATE 4 채널 격하 0 합의 | 7/8 이상 | reviewer 가 "강도 유지가 부적절" 판단 가능성 footnote |
| 6 Q17 §2 격상 + partial 명시 | 8/8 합의 | <8/8 시 §3 위치 유지 |
| 7 priori 회복 path 영구 종결 (L566 §5) 명문화 | 8/8 합의 | <8/8 시 본 옵션 C 재검토 |
| 8 저널 1순위 (JCAP vs PRD) 결정 | 5/8 이상 | tie 시 본 L567 §1.2 권고 (JCAP) 채택 |

---

## §4 timeline 재조정

### §4.1 reviewer trust 회복 충분성 평가

L565 §3.1 timeline (2026-05 즉시 / 2026-06~07 변환 / 2026-09 PRD 제출) 에 본 L567 §3 의 fabrication disclosure 부담을 추가하면:

- **2026-05 ~ 06 (Rule-A 8인 의제 §3.4 8건)**: 6–8주 소요 추정. L565 의 4–6주 추정보다 +2주.
- **2026-06 ~ 08 (변환 — §2.1 의무 figures/methods/appendix 추가)**: 8–10주. L565 의 8주 + §3.3 git forensics appendix 추가로 +2주.
- **2026-09 → 2026-10 으로 제출 슬립**: 본 L567 권고. trust 회복은 *시간 단축* 보다 *disclosure 완전성* 으로 달성.
- *결과*: JCAP 제출 2026-10 (L565 09 → 10, +1mo), 출간 예상 2027 Q3 (L565 Q2 → Q3, +1Q).

### §4.2 DR3 (2027 Q2) 도착 시 revision protocol

| 시점 | DR3 결과 시나리오 | revision 행동 |
|---|---|---|
| **2027-Q2 도착 = JCAP first round 진행 중** | (a) DR3 wa<−0.5 (PASS): supplementary note 로 첨부, paper 내 falsifier 채널 결과 요약 1 paragraph 추가, claims_status v1.y bump. **revision round 에서 자연 통합**. | 자발적 supplementary; reviewer 친화 |
| 동상 (b) DR3 wa>−0.5 (KILL): 즉시 paper 철회 권고 — JCAP editor 에 정직 보고 ("preregistered falsifier 가 KILL 트리거"). 후속 paper 로 negative-result note (1–3p) 별도 제출 — separate venue (PRD short note 또는 JCAP letter). | trust 보존 우선; framework "honest falsification" 자산 |
| 동상 (c) DR3 inconclusive (wa = −0.4 ~ −0.6): supplementary note + claims_status PASS_MODERATE → PASS_QUALITATIVE 격하 + Limitations §6 보강. | 정직 격하 |
| **DR3 도착 = JCAP review 완료 후 (2027-Q3 이후)**: 별도 후속 paper (Round 11 트랙, L546 §2.4 / L565 §3.1 끝 timeline 정합). | 본 paper 무영향 |

### §4.3 최종 timeline (L567 권고)

| 시점 | 작업 | 의존성 |
|---|---|---|
| 2026-05 즉시 | L565 옵션 C + 본 L567 → Rule-A 8인 라운드 (의제 §3.4) | (선결) |
| 2026-05 ~ 07 | Rule-A 의제 8건 합의 (6–8주) + L561 HIGH 3건 정정 4인 Rule-B 병행 | Rule-A 진행 |
| 2026-05 ~ 06 | arXiv D preprint *원본* arXiv 제출 (priority lock 자산) — 8인 Rule-A 의제 1·2·3·7 통과 시 | Rule-A 부분 통과 |
| 2026-07 ~ 09 | arXiv-D-as-paper 변환 (figures/methods/appendix/§2 격상/disclosure) — Rule-A 8인 + 4인 Rule-B 동시 | Rule-A 통과 |
| 2026-08 | Companion B (OJA) 제출 — L546 §3.4 timeline 유지 (변경 없음) | 독립 |
| 2026-10 | arXiv-D-as-paper **JCAP 제출** (1순위; PRD fallback) | 변환 통과 |
| 2027 Q1 | Companion B 출간 예상 | review |
| 2027 Q1 ~ Q2 | JCAP review (3–4mo) | JCAP 제출 |
| 2027-Q2 | DESI DR3 공개 → §4.2 revision protocol 트리거 | DR3 |
| 2027 Q3 | JCAP review 결과 + revision 통합 → 출간 예상 | review 통과 |

---

## §5 Companion B 영향 (cross-ref 변경)

### §5.1 L546 Companion B 의 Case study (SQMH 단일 adopter) 유지 가능성

L546 §3 / §4.3 의 Companion B 는 *방법론 (verification infrastructure) paper* 로, schema adoption count = 1 (SQMH 단일) 이 정직 인정된 약점. Main MNRAS-γ 폐기 후 본 약점 재평가:

- **Case study 유지 권고** — 사유:
  1. Companion B 의 SQMH case study 는 *Main MNRAS-γ 의 본문* 이 아니라 *verification 의 적용 예시*. Main 폐기는 case study 의 학술적 가치를 손상하지 않음.
  2. case study 주체를 "arXiv-D-as-paper (JCAP/PRD)" 로 *cross-ref 대상 변경* — Main MNRAS-γ 자리에 본 격상 paper 가 들어감. schema adoption count 는 여전히 1, 변동 0.
  3. fabrication 발견은 SQMH case study 의 *내부 데이터* 가 아닌 *Main paper 의 narrative* 에 한정됨 (L563 F1/F2 모두 §5.3 narrative). Companion B 는 verification script 의 PASS/FAIL 라벨만 사용 → 영향 미미.

### §5.2 cross-ref 변경 매트릭스

| Companion B 위치 | L546 cross-ref | L567 권고 변경 |
|---|---|---|
| §1 introduction | "applied to SQMH (Main MNRAS-γ)" | "applied to SQMH cosmology phenomenology (arXiv-D-as-paper, JCAP)" |
| §3 case study | Main MNRAS-γ 표 / 결과 | arXiv-D-as-paper 표 / 결과로 *대체* (PASS_MODERATE 4 채널 + N_eff=4.44 + Hidden DOF 9–13) |
| §5 limitations | "single adopter" | "single adopter; Main MNRAS-γ 가 fabrication 발견 (L563) 으로 retract — 본 paper 는 retract 사실을 disclosure 하며 case study 데이터는 post-retract 재생성본 사용" |
| §6 references | Main MNRAS-γ + arXiv D | arXiv-D-as-paper (JCAP/PRD) + arXiv D preprint (priority lock) |

### §5.3 Companion B 자체 disclosure 의무

- Companion B §5 (limitations) 에 fabrication 발견 + L564 git forensics 1 paragraph 추가 — Main paper 와 *동일 disclosure 표준*.
- 본 disclosure 추가는 OJA review 의 "정직성 보너스" 가능성 (acceptance +2~5%p). L565 §1.2 의 Companion 47% → 49–52% 가능성, 단 정량 인용 금지 (Rule-A 종속).

### §5.4 schema adoption count 가속화 권고 (L546 §3 권고 직접 상속)

- **Companion B 출간 후 6mo 내**: 외부 그룹 1팀 이상에서 schema 채택 권고 (cosmology phenomenology paper 1 + galactic dynamics paper 1). adoption count 1→3 도달 시 Round 12 portfolio 재평가.
- 본 권고는 L567 의 *권한 외부* 항목, 채택은 별도 라운드 결정.

---

## §6 정직 한 줄 (말미)

본 L567 은 L565 옵션 C (arXiv D 격상, 결합 acceptance 0.55, 회복률 81%) 의 *실행* 단계로 — 저널 권고를 **JCAP 1순위 / PRD 2순위 (L565 의 PRD 1순위에서 재정렬)** + 변환 시 **§2 Q17 격상 + Appendix C fabrication disclosure (L563 F1 정정 본문 반영, F2 §5.3 폐기, L564 active fabrication 90% confirmation 자발적 보고) + Cross-mention 4건 (L549 P3a / L552 RG / L562 D4 / L566 D2 박탈 모두 Appendix C)** + **timeline 2026-10 JCAP 제출 / 2027 Q3 출간 (L565 대비 +1Q 슬립, disclosure 완전성 우선)** + **DR3 wa>−0.5 KILL 시 즉시 철회 protocol** + **Companion B case study 주체를 arXiv-D-as-paper 로 cross-ref 변경 (count=1 유지, fabrication disclosure 추가)** 으로 정리하되, 본 plan 의 8 의제 (§3.4) 는 모두 후속 8인 Rule-A 라운드 결정에 종속하며 paper / claims_status / arXiv 직접 수정 0건 이다.

---

*저장: 2026-05-02. results/L567/OPTION_C_EXECUTION.md. 단일 작성 에이전트. paper edit 0건. claims_status edit 0건. simulations/ 신규 코드 0줄. 신규 수식 0줄. 신규 파라미터 0개. CLAUDE.md [최우선-1] / [최우선-2] / 결과 왜곡 금지 / L6 재발방지 정합. 본 문서가 제시한 모든 저널·timeline·disclosure 항목은 *방향 제시* 이며 채택은 후속 Rule-A 8인 라운드 결정.*
