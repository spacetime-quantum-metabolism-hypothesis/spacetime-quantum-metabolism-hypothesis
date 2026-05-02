# L655 — Submission Paper Deep Evaluation

**Date**: 2026-05-02
**Context**: 출판 가능 환경 (사용자 정정 2026-05-03). 본 문서는 portfolio 3 paper 중 어디부터 submission 할지 정직 평가.

**[최우선-1] 준수**: 수식 0줄, 파라미터 값 0개. 등급/평가만 기재.
**CLAUDE.md 정합**: paper / claims_status / 디스크 edit 0건. 산술 max 단독 인용 0건.

---

## §1. 3 Paper 비교 표

| 항목 | Paper A (Main MNRAS-γ) | Paper B (Companion B) | Paper C (arXiv-D-as-paper) |
|---|---|---|---|
| **스코프** | Galactic-only (a₀ + RAR + BTFR + Bullet) | Methodology / audit framework | Cosmological phenomenology (4 channel) |
| **자산 등급** | ★★★ | ★★★★ | ★★★★ |
| **정직성 자산** | ★★★★★+ (fabrication 90% disclosure 후) | ★★★★★+ (verify 7/7, schema v1.3, erratum dir) | ★★★★★+ (Hidden DOF, 4 priori 박탈 cross-mention) |
| **주요 강점** | Verlinde degeneracy 인정 + a₀ PASS_MODERATE | 7 verify_*.py PASS + claims_status schema | PASS_MODERATE 4 channel + 6 falsifier (DR3 conditional) + Q17 partial |
| **주요 약점** | paper/MNRAS_DRAFT.md git untracked, fabrication 90%, retraction risk | adopter count = 1 (SQMH 단독), schema novelty 약 | paradigm shift 박탈 + Q17 dynamic 미달 (PRD Letter 차단) |
| **선결 의무** | L555/L559 mismatch 9건 + 0.42σ→0.71σ + L137 H₀=100 mock 거짓 정정 | 없음 (현 상태로 제출 가능) | 4 priori 박탈 cross-mention 의무 |
| **저널 1순위** | MNRAS | Open Journal of Astrophysics (OJA) | **JCAP** |
| **저널 2순위** | ApJ | JOSS | PRD |
| **Acceptance 추정** | 18-28% (정정 후) | 40-55% (mid 47%) | **55-65%** |
| **Fabrication risk** | 높음 (정정 전) / 중 (정정 후) | 0 | 0 |
| **Timeline 부담** | 높음 (정정 작업 큼) | 낮음 | 낮음~중 |

출처: L546 §4.1 (A, B 추정), L567 옵션 C (C 추정), L564 (Paper A fabrication 90%), L565 (옵션 A retract / 옵션 B 정정).

---

## §2. Priority Order + Acceptance 추정

### 2.1 단일 paper 1순위
- **Paper C (arXiv-D-as-paper, JCAP)**.
- 근거:
  - acceptance 추정 최고 (55-65%).
  - fabrication risk 0.
  - 정직 disclosure (Hidden DOF, 4 priori 박탈) 가 reviewer 신뢰 자산.
  - JCAP scope 와 phenomenology 포지셔닝 정합.
  - PRD Letter 차단 (Q17 dynamic 미달) 은 1순위 저널 선택에서 회피 가능.

### 2.2 Portfolio 진행 순서 (timeline 분리)
1. **C → JCAP** (1순위, 가장 안전, 즉시 진행 가능)
2. **B → OJA** (병렬 가능, case study 분리하면 C 와 충돌 없음)
3. **A → MNRAS** (정정 / retraction 결정 후, 가장 마지막)

### 2.3 동시성 평가
- **C 와 B 병렬 진행 가능**: 스코프 비중첩 (cosmological phenomenology vs methodology). 단, B 의 SQMH case study 부분이 C 와 cross-reference 되도록 정렬 필요.
- **A 단독 분리**: fabrication 정정 / retraction 결정이 사용자 의사결정 사안이라 timeline 예측 불가. C/B 와 묶지 말 것.

---

## §3. Submission 결정 보조 (사용자)

### 3.1 단일 1순위
- **Paper C, JCAP 제출**.
- 보조 근거: L567 옵션 C 권고와 일치.

### 3.2 Portfolio 진행
- **C → B → A** 순.
- C 와 B 는 timeline overlap 허용. A 는 정정/retraction 결정 후.

### 3.3 Main MNRAS-γ (Paper A) 처리
사용자 결정 필요. 두 옵션:

- **옵션 A: Retract 권고 (L565)**
  - 근거: paper/MNRAS_DRAFT.md 자체가 git untracked + fabrication 90%. 정정해도 reviewer 가 retraction 사례로 인식할 risk.
  - 장점: 신뢰 자산 보존, C/B 영향 차단.
  - 단점: galactic-only 자산 (a₀, RAR, BTFR, Bullet) 의 출판 채널 상실.

- **옵션 B: 정정 후 재제출 (L565)**
  - 선결 의무: L555/L559 mismatch 9건 정정 + 0.42σ→0.71σ 정정 + L137 H₀=100 mock 거짓 정정.
  - 장점: galactic 자산 보존.
  - 단점: timeline 부담 큼, retraction risk 잔존, acceptance 18-28% 로 가장 낮음.

본 평가 권고: **사용자가 시간 자원 평가 후 결정**. 정직성 우선이면 옵션 A, 자산 보존 우선이면 옵션 B. C 와 B 의 진행에는 어느 쪽이든 영향 없음.

---

## §4. Acceptance 영향 요인

### 4.1 공통 +α (모든 paper)
- ★★★★★+ 정직성 자산 (Hidden DOF, claims_status schema, verify_*.py PASS).
- 출판 가능 환경 (사용자 정정).

### 4.2 Paper 별 고유 +α
- **Paper C**: 4 priori 박탈 cross-mention 으로 reviewer 가 "selective reporting" 의심 차단. 6 falsifier (DR3 conditional) 로 future-test 명시.
- **Paper B**: verify 7/7 PASS 로 코드 재현성 reviewer 신뢰 +α. erratum 디렉터리 사전 준비.
- **Paper A**: fabrication 90% disclosure 가 정정 후 trust 회복 +α 가능 (단, retraction risk 와 trade-off).

### 4.3 -α 요인
- **Paper A**: paper/MNRAS_DRAFT.md git untracked 상태. fabrication 90%. 정정 미실행 시 desk reject 가능성 큼.
- **Paper B**: adopter count = 1 (SQMH 단독 case study). schema novelty 약.
- **Paper C**: paradigm shift 박탈 (PRD Letter 진입 조건 미달, Q17 dynamic 부족). DR3 공개 전 falsifier 검증 불가.

---

## §5. Timeline 권고

| 단계 | 작업 | 기간 | Paper |
|---|---|---|---|
| 1 | JCAP 제출 준비 (4 priori cross-mention 정렬) | 1-2 주 | C |
| 2 | OJA 제출 준비 (case study C 와 정렬) | 1-2 주 | B |
| 3 | C 제출 | — | C |
| 4 | B 제출 (C 와 ±2주 이내) | — | B |
| 5 | A 결정 (사용자) | 미정 | A |
| 6a | A retract 결정 시 → 종료 | — | A |
| 6b | A 정정 후 재제출 시 → mismatch 9건 + 0.42σ→0.71σ + L137 정정 | 2-4 주 | A |
| 7 | A 제출 (옵션 6b 인 경우) | — | A |

**핵심**: C 가 가장 빠른 path. A 는 결정 보류 가능, C/B 진행을 막지 말 것.

---

## §6. 정직 한 줄

**출판 가능 환경에서 1순위는 Paper C (JCAP), 병렬로 Paper B (OJA), Paper A (MNRAS) 는 fabrication 정정 또는 retraction 사용자 결정 후 — 정직성 자산이 모든 paper 의 acceptance 를 +α 로 받친다.**
