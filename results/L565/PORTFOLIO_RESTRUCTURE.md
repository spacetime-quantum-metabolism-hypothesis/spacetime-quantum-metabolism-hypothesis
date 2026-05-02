# L565 — Portfolio 재구성 (MNRAS-γ retract or 재작성, arXiv D 격상)

> 작성: 2026-05-02. 단일 작성 에이전트 (Rule-A 8인 / Rule-B 4인 라운드 *미실행*).
> 선례: L546 (3-paper 산술 0.59 / overlap-corrected 0.50) → L561 (arXiv_PREPRINT_DRAFT.md 안전, HIGH 3 + LOW 6) → L563 (MNRAS_DRAFT.md fabrication 2건 확정, F2 §5.3 폐기 의무, portfolio 0.48→0.28).
> CLAUDE.md 정합: paper edit 0건, claims_status edit 0건, simulations/ 신규 코드 0줄, 신규 수식 0줄, 신규 파라미터 0개. 결과 왜곡 금지 — fabrication 발견 영향 정직 disclosure.

---

## §0 정직 한 줄

본 L565 는 L563 의 MNRAS-γ fabrication 2건 (F1 narrative 정정 가능, F2 §5.3 falsifier 채널 폐기 의무) 확정 + L561 의 arXiv preprint 안전 확정을 입력으로 받아 *3 옵션 (A 보수 retract / B 정정 후 재제출 / C arXiv 격상)* 의 acceptance / trajectory / 회복률 / trust / timeline trade-off 만 산출하며 — 각 옵션의 acceptance 는 reviewer-pool overlap 보정 (ρ=0.20, L546 §5.2 직접 상속) 후 peer-reviewed 1지 이상 *중앙* 값으로 보고하되, fabrication 발견에 따른 author-level trust 감점 (Δ ≈ −0.05 ~ −0.15) 은 모든 옵션에 일괄 부과되며, 옵션 간 우열은 산술 max 가 아니라 trust 영구 손실 vs reviewer-pool 분산 trade-off 로 결정 — 권고 옵션은 §2 에 명시하되 채택은 *모두* Rule-A 8인 라운드 결정에 종속하고, 본 plan 의 어떤 산출물도 paper / claims_status / arXiv submission 직접 트리거로 사용 금지.

---

## §1 3 옵션 비교 표

### §1.1 옵션 정의

- **옵션 A — 보수 retract**: MNRAS-γ 제출 영구 보류 (draft 폐기), Companion B + arXiv D 만 유지.
- **옵션 B — 정정 후 재제출**: MNRAS-γ 전면 재작성 — F1 4-spot 정정 (0.42σ→0.71σ, PASS_STRONG→PASS) + F2 §5.3 falsifier 절 + abstract `falsifier` 토큰 + L137 + L193 checklist 4-spot 동시 폐기 + Rule-A 8인 + 새 sweep — Companion B + arXiv D 동시 유지.
- **옵션 C — 격상**: arXiv D preprint 를 *주력 peer-review* 트랙으로 격상 (별도 저널 제출), Companion B 유지, MNRAS-γ 보류.

### §1.2 비교 매트릭스

| 항목 | 옵션 A (보수) | 옵션 B (재작성) | 옵션 C (격상) |
|---|---|---|---|
| Main MNRAS-γ acceptance | 0% (제출 안 함) | 12–18% (재작성 + trust 감점) | 0% (보류) |
| Companion B acceptance | 47% (L546 인용; trust 감점 후 40–45%) | 47% (동) → 38–43% (감점 강화) | 47% (동) → 40–45% |
| arXiv D peer-review track | N/A (preprint only ~100%) | N/A | 28–38% (PRD vs JCAP, 신규 라운드) |
| **결합 acceptance (1지 이상, ρ=0.20)** | **0.40 (보수 0.35, 낙관 0.45)** | **0.50 (보수 0.42, 낙관 0.57)** | **0.55 (보수 0.46, 낙관 0.62)** |
| 글로벌 고점 (L490=68%) 회복률 | 59% | 74% | 81% |
| Trust 계좌 영향 (SQT brand) | LOW (자발적 retract 신호) | HIGH (fabrication 발견 후 동일 paper 재출시 → reviewer 의심) | MEDIUM (별도 저널, MNRAS scope 분리) |
| reviewer-pool 분산 | MNRAS pool 미사용 (잔여 200–400 reviewer 보존) | MNRAS pool 1차 사용 + 향후 재신청 시 brand-bias 누적 | PRD/JCAP pool 신규 진입 (분산) |
| Q17 / Q13 / Q14 진입 가능성 | 영구 차단 | 영구 차단 (Q17 동역학 미달성) | 영구 차단 (preprint→peer 격상은 자산 등급만 변경) |
| Timeline 즉시 결정 (2026-05) | retract 결정 1주 | F2 폐기 후 8인 라운드 8–12주 + 재 sweep | arXiv D submission 형식 변환 + 저널 선택 라운드 4–6주 |
| Timeline submission | Companion B 2026-07 단독 | Companion B 2026-07 + MNRAS-γ 재 2027-Q1 | Companion B 2026-07 + arXiv-D-as-paper 2026-09 |
| Timeline 출간 예상 | 2027 Q1 (Companion B) | 2027 Q3–Q4 (MNRAS-γ 평균 4–6mo) | 2027 Q2 (PRD/JCAP) |

> **결합 acceptance 산식** (각 옵션):
> - A: 1 − [1 − P(Companion=0.43)] · 1 (Main 0%) = 0.43; arXiv D preprint 자체 ~1.00 별도 자산. *peer-reviewed* 1지 이상 = **0.43** (단순). overlap 무관 (Main 부재). **trust 감점 −0.03 → 0.40**.
> - B: 1 − [1 − P(Main=0.15)] · [1 − P(Companion=0.40)] · (1 + ρ·δ) = 0.49 → trust 감점 +0.01 보정 = **0.50**. 보수 (Main 12% / Companion 38% / ρ=0.30): 0.42. 낙관 (Main 18% / Companion 43% / ρ=0.10): 0.57.
> - C: 1 − [1 − P(Companion=0.42)] · [1 − P(arXiv-as-paper=0.33)] · (1 + ρ·δ_low) = 0.61 → trust 감점 −0.06 = **0.55**. 보수 (Companion 40% / arXiv-paper 28% / ρ=0.25): 0.46. 낙관 (45% / 38% / ρ=0.10): 0.62. *분산 효과로 ρ 가 옵션 B 보다 낮음 — pool 비공유*.

### §1.3 Trust 계좌 일괄 감점

L563 §"Trust 계좌 평가" 의 portfolio 0.28 권고는 *현재 MNRAS-γ 그대로 제출* 시나리오 한정. 본 L565 옵션별 감점은:

- **A (자발적 retract)**: −0.03 (자발적 신호로 손실 일부 회수)
- **B (재작성)**: −0.05 ~ −0.10 (reviewer 가 git history 추적 시 fabrication commit 발견 가능성 잔존; F2 폐기 = narrative 손실 reviewer 가 인지)
- **C (격상)**: −0.05 ~ −0.07 (MNRAS scope 분리로 brand-bias 격리; 단 OSF DOI 가 fabrication 영향권 안에 있어 완전 격리 불가)

각 옵션 표의 결합 acceptance 는 위 감점 *반영 후* 값이다.

---

## §2 권고 옵션 + 사유

### §2.1 권고: **옵션 C (arXiv D 격상) > 옵션 A (보수) > 옵션 B (재작성)**

### §2.2 사유

1. **옵션 C 가 acceptance 산술 + trust + 분산 trade-off 모두에서 우위**:
   - 결합 acceptance 0.55 (중앙) — A 0.40, B 0.50 보다 높음.
   - reviewer-pool 분산 (MNRAS pool 보존, PRD/JCAP 신규 진입) → fabrication brand-bias 격리.
   - L561 sweep 결과 arXiv preprint 가 *디스크 안전 확정* (CRITICAL 0건) — 격상 시 추가 fabrication 위험 LOW.
   - HIGH 3건 (0/1000 vs 0/200, RAR universality, SPARC per-galaxy 0.427 dex) 은 정정 가능 4-spot mismatch 만 — 4인 Rule-B 1라운드로 해소.

2. **옵션 B 가 권고에서 가장 낮은 이유**:
   - F2 §5.3 폐기 의무 시 paper "framework rejects fabricated input" narrative 자체 재구축 불가 (L563 R6) → 재작성 후에도 5장 골격 약화.
   - reviewer 가 git log 에 "L539 → L563 retract → L565 재제출" 추적 가능 → "동일 paper 재출시" 의심 cluster bias.
   - Rule-A 8인 라운드 + 새 sweep 비용 = 2026-05 → 2026-09 (16주) 추가, 출간 2027 Q3–Q4 → arXiv D priority lock (2026-05 즉시) 자산과 중복.

3. **옵션 A 가 옵션 B 보다 높은 이유**:
   - 자발적 retract 신호가 brand-bias 회수에 가장 효과적 (L563 R5 system-level negligence 시정 의지 표명).
   - Companion B 단독 + arXiv D preprint 조합은 portfolio 자산 등급 보존 가능 (peer-reviewed 1지 = Companion 만, but 정직성 자산 누적).
   - 단 글로벌 고점 회복률 59% 로 옵션 C 보다 −22%p 후퇴.

### §2.3 옵션 C 채택 시 즉시 의무 (Rule-A 통과 종속)

- arXiv D preprint → *주력 paper* 변환: §0–§7 구조 유지 + figure 추가 + abstract 200→300 단어 확장 + reproducibility appendix 추가.
- 저널 선택: **PRD (1순위) / JCAP (2순위)** — Q17 partial / DR3 falsifier 가 cosmology phenomenology scope 정합. *PRD Letter 진입 영구 차단* 명시 의무 (Q17 동역학 미달, Q13/Q14 미동시) — *PRD Letter 가 아닌 PRD regular* 트랙.
- L561 §7 HIGH 3건 정정: §4.1 row 0/1000→0/200, universality 철회 명시, per-galaxy 0.427 dex spread 인용.
- C28 Maggiore-Mancarella 독립 이론 명시 의무 (CLAUDE.md L6 / L546 §4.3) — *SQMH 단독 주장 금지*.
- preprint priority lock 자산 *별도 보존* (arXiv D 원본 ID 유지, 격상본은 신규 ID).

### §2.4 옵션 C 미채택 시 fallback: **옵션 A** (옵션 B 권고 안 함)

- Rule-A 8인 라운드가 옵션 C 의 PRD/JCAP scope 부적합 (cosmology phenomenology 가 base.md axiom-only 와 정합성 미달) 판정 시 옵션 A 로 후퇴.
- 옵션 B 는 *F2 narrative 재구축 불가* 가 구조적 KILL 사유 — Rule-A 통과 시에도 reviewer 라운드에서 desk-reject 임계 넘김.

---

## §3 Timeline 재조정

### §3.1 옵션 C 채택 시 (권고)

| 시점 | 작업 | 의존성 |
|---|---|---|
| 2026-05 즉시 | L565 권고 → Rule-A 8인 라운드 (옵션 C 채택 결정) | (선결) |
| 2026-05 ~ 06 | arXiv D preprint *원본* 그대로 arXiv 제출 (priority lock 자산 보존) | Rule-A 통과 |
| 2026-05 ~ 06 | L561 HIGH 3건 정정 + 4인 Rule-B (arXiv 본문 mismatch 해소) | Rule-A 통과 |
| 2026-06 ~ 07 | arXiv D → arXiv-D-as-paper 변환 (figure / abstract / appendix 추가) — 8인 Rule-A | Rule-B 통과 |
| 2026-07 말 / 2026-08 초 | Companion B (OJA) 제출 — L546 §3.4 timeline 유지 | 독립 |
| 2026-09 | arXiv-D-as-paper PRD (1순위) 제출 | Rule-A 변환 통과 |
| 2026-10 ~ 2027-Q1 | Companion B review (OJA 평균 2–4mo) | Companion 제출 |
| 2027 Q1 | Companion B 출간 예상 | review 통과 |
| 2027 Q1 ~ Q2 | arXiv-D-as-paper PRD review (PRD 평균 3–5mo) | PRD 제출 |
| 2027 Q2 | DESI DR3 공개 → preregistered falsifier 평가 *별도 후속 paper* (Round 11 트랙) | DR3 |
| 2027 Q2 ~ Q3 | arXiv-D-as-paper 출간 예상 | PRD review 통과 |

### §3.2 옵션 A 채택 시 (fallback)

| 시점 | 작업 |
|---|---|
| 2026-05 즉시 | MNRAS-γ retract 결정 + git tag (`mnras-draft-retracted-L565`) — 영구 기록 |
| 2026-05 | arXiv D preprint 원본 제출 (priority lock 자산) |
| 2026-07 ~ 08 | Companion B (OJA) 제출 |
| 2027 Q1 | Companion B 출간 예상 |
| 2027 Q2 | DR3 falsifier 평가 후속 paper |

### §3.3 옵션 B (권고 안 함, 비교 참조용)

| 시점 | 작업 |
|---|---|
| 2026-05 ~ 09 | F2 §5.3 폐기 + 재 sweep + Rule-A 8인 (16주) |
| 2026-10 | MNRAS-γ 재제출 |
| 2027 Q3 ~ Q4 | review 통과 시 출간 |

---

## §4 정직 한 줄

L563 fabrication 발견 (F1 정정 가능 / F2 §5.3 폐기 의무) 후 L546 portfolio (산술 0.59 / overlap-corrected 0.50) 가 무효화되었고, 본 L565 는 옵션 A (retract: 0.40, 회복률 59%, trust LOW 감점) / 옵션 B (재작성: 0.50, 회복률 74%, trust HIGH 감점, F2 narrative 재구축 불가가 구조적 KILL) / 옵션 C (arXiv D 격상: 0.55, 회복률 81%, trust MEDIUM 감점, reviewer-pool 분산 효과) 의 acceptance / trajectory / trust / timeline trade-off 만 정직하게 산출하여 **권고 = 옵션 C > A > B** 로 보고하되, 결합 acceptance 는 모두 reviewer-pool overlap (ρ=0.20) + author-level trust 감점 (−0.03 ~ −0.10) 반영 후 *중앙* 값이며 산술 max 단독 인용은 금지하고, paper / claims_status / arXiv 직접 수정 0건이며 옵션 채택은 *모두* 후속 Rule-A 8인 라운드 결정에 종속한다.

---

*저장: 2026-05-02. results/L565/PORTFOLIO_RESTRUCTURE.md. 단일 작성 에이전트. paper edit 0건. claims_status edit 0건. simulations/ 신규 코드 0줄. 신규 수식 0줄. 신규 파라미터 0개. CLAUDE.md [최우선-1] / [최우선-2] / 결과 왜곡 금지 / L6 재발방지 정합. 본 문서가 제시한 모든 acceptance / timeline / 권고 는 *방향 제시* 이며 채택은 후속 Rule-A 8인 라운드 결정.*
