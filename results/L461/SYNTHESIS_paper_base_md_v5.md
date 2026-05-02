# L461 — SYNTHESIS paper/base.md v5 (L442 ~ L460 종합)

Date: 2026-05-01
Scope: results/L442 ~ results/L460 (19 directory) 를 paper/base.md §14 (제출 전 TODO 체크리스트) 대비 종합.
Method: 각 디렉터리 직접 ls + 존재하는 모든 .md 직접 read. 추론·외삽 금지.

---

## 0. 정직 disclosure (★ 가장 중요)

요청은 "L442 ~ L460 19 loop 의 REVIEW.md Read" 라고 명시했으나
**실제 파일 시스템에는 REVIEW.md 가 6 개 디렉터리 (L445, L450, L452, L453, L457, L459) 에만 존재한다.**
나머지 13 디렉터리의 상태는 다음과 같다.

| 디렉터리 | 실제 내용 |
|---|---|
| L442 | ATTACK_DESIGN.md (REVIEW.md 부재) |
| L443 | make_figures.py 만 (문서 0건) |
| L444 | **빈 디렉터리** |
| L446 | **빈 디렉터리** |
| L447 | ATTACK_DESIGN.md (REVIEW.md 부재) |
| L448 | ATTACK_DESIGN.md (REVIEW.md 부재) |
| L449 | **빈 디렉터리** |
| L450 | ATTACK_DESIGN + NEXT_STEP + REVIEW (3건) |
| L451 | **빈 디렉터리** |
| L454 | **빈 디렉터리** |
| L455 | **빈 디렉터리** |
| L456 | **빈 디렉터리** |
| L458 | **빈 디렉터리** |
| L460 | **빈 디렉터리** |

따라서 본 종합문은 **"19 loop verdict 표"** 가 아니라
**"6 개 REVIEW + 3 개 ATTACK_DESIGN-only 의 9 개 loop 종합 + 10 개 미실행/미완료 loop 표시"** 가 정확하다.
이를 19 loop 라고 보고하는 것은 결과 왜곡 (CLAUDE.md "결과 왜곡 금지" 위반) 이다.

---

## 1. 9 loop verdict 표 (실제 산출물 기준)

| Loop | 임무 | 산출물 | Verdict (해당 loop 자체) | paper/base.md §14 매핑 |
|---|---|---|---|---|
| **L442** | Statistical Methods Appendix 설계 (R3 reviewer 응답) | ATTACK_DESIGN.md | DESIGN 단계만 — 부록 본문 미작성 | §14 Layer B "Statistical methods appendix 신설" — **미완료** |
| **L443** | (figure 생성 스크립트) | make_figures.py | 코드 존재, 산출 figure / 검증 문서 부재 | §14 Layer B "I1–I4 infographic" — **부분** |
| L444 | — | (없음) | **미실행** | n/a |
| **L445** | base.md §X.Y cross-reference audit | REVIEW.md + CROSS_REF_AUDIT.md | **PASS** — 87 ref / 22 anchor / broken 0 (§9.6 numbering gap 만 advisory) | §14 미명시 (자체 점검) — **CLEAN** |
| L446 | — | (없음) | **미실행** | n/a |
| **L447** | S_8 worsening 의 *방향* 을 PASS_STRUCTURAL 로 격상 시도 (8+4 패턴) | ATTACK_DESIGN.md | DESIGN 단계만 — 8 인 토의 / 4 인 검증 미실행 | §6.5 methodological caveats 보강 후보 — **미완료** |
| **L448** | BTFR zero-point a_0 a priori 측정 | ATTACK_DESIGN.md | DESIGN 단계만 — SPARC fit 코드 미작성 | §3.5 / §4.1 SPARC 채널 — **미완료** |
| L449 | — | (없음) | **미실행** | n/a |
| **L450** | 6×6 Modified Gravity 비교 (TeVeS / EMG / MOG / Verlinde / RVM / k-essence vs SQT) | ATTACK_DESIGN + NEXT_STEP + REVIEW | SQT: PASS 2 / PARTIAL 2 / FAIL 2 (Λ-origin + BBN 강점, S_8 + a_0 약점 — 정직 노출) | §5.7 / §6.1.2 비교표 — **요약 1 줄만 존재, 표 본체 부재** |
| L451 | — | (없음) | **미실행** | n/a |
| **L452** | verification Dockerfile + conda_env.yml | REVIEW.md | **PASS (artifact-only)** — 빌드/실행 검증 미수행 정직 명시 | §14 Layer C "Dockerfile + conda_env.yml 양방" — **artifact 생성 / 검증 미완료** |
| **L453** | .github/workflows/verify.yml CI 작성 | REVIEW.md | **PASS (artifact + local smoke)** — verify_milgrom_a0.py stdout substring 일치 확인 | §14 Layer C "CI badge README 노출" / Repo 인프라 ".github/workflows/verify.yml" — **PASS** |
| L454 | — | (없음) | **미실행** | n/a |
| L455 | — | (없음) | **미실행** | n/a |
| L456 | — | (없음) | **미실행** | n/a |
| **L457** | .github/ISSUE_TEMPLATE/* + PULL_REQUEST_TEMPLATE.md | REVIEW.md | **PASS (artifact-only)** — CLAUDE.md 재발방지 항목 PR 체크박스로 강제, 실사용 효과 미검증 정직 명시 | §14 Repo 인프라 ".github/ISSUE_TEMPLATE/* + PULL_REQUEST_TEMPLATE.md" — **PASS** |
| L458 | — | (없음) | **미실행** | n/a |
| **L459** | CITATION.cff + .zenodo.json | REVIEW.md | **PASS (artifact-only)** — DOI 는 placeholder, Zenodo deposit 미수행 정직 명시 | §14 Repo 인프라 "CITATION.cff Zenodo DOI 호환" / 출판 "Zenodo 자동 연동" — **PASS (artifact), DOI 발급 미완료** |
| L460 | — | (없음) | **미실행** | n/a |

**범례**:
- PASS = 산출물 + 자체 검증 + 정직 한 줄 모두 충족
- PASS (artifact-only) = 파일 생성 완료, 통합 / 외부 검증은 별 단계
- DESIGN 단계만 = 8+4 패턴의 Stage 1 명세만, 실행 미완료
- 미실행 = 디렉터리 비어 있음 (loop 자체가 동작하지 않음)

---

## 2. paper/base.md §14 publish-readiness 체크리스트 대비

(`-` = §14 항목, 옆은 L442~L460 산출물 기반 상태)

### Layer A — README.md (GitHub landing) — **0 / 11 PASS**
- [ ] Hero infographic + social preview — **미착수** (L443 figure script 만)
- [ ] Language switcher — **미착수**
- [ ] Status badge 4 개 (DOI / CI / License / OSF) — **부분** (L453 CI verify.yml 존재 → CI badge endpoint JSON 생성 가능, 실제 README 삽입 0)
- [ ] OSF pre-registration badge — **미착수**
- [ ] One-sentence headline — **미착수**
- [ ] TL;DR 7 bullet — **미착수**
- [ ] Verify in 5 seconds 코드 블록 — **미착수**
- [ ] Claims status 표 — **미착수**
- [ ] How to cite BibTeX — **미착수** (L459 CITATION.cff 만, BibTeX 발췌 별도)
- [ ] Documentation 링크 — **미착수**
- [ ] CONTRIBUTING / License 표시 — **미착수** (PR template 만 L457)

### Layer B — paper/main_en.tex (학계 본문) — **0 / 11 PASS**
- [ ] 1–7 장 LaTeX 본문 (영문 master + 한국어 mirror) — **미착수**
- [ ] F0 dependency graph — **미착수**
- [ ] F1, F8 aggregator — **미착수**
- [ ] I1–I4 infographic — **부분** (L443 make_figures.py 만)
- [ ] 17σ 정확 Δχ² 수치 삽입 — **미착수**
- [ ] Statistical methods appendix — **DESIGN 만** (L442)
- [ ] Dataset inventory 표 (4.2) — **미착수**
- [ ] DESI DR3 inconclusive band 정의 (4.4) — **미착수**
- [ ] 5.2 Λ origin circularity disclosure — **미착수** (L450 6×6 표는 비교만)
- [ ] 6.5 Methodological caveats — **부분** (L447 S_8 PASS_STRUCTURAL 시도는 DESIGN 만)
- [ ] 8 장 FAQ 3-tier — **미착수**
- [ ] 색맹 / grayscale / alt-text — **미착수**

### Layer C — paper/verification/README.md — **2 / 8 PASS**
- [ ] 5-second quickstart — **미확인** (회귀 verify_milgrom_a0.py 동작은 L453 smoke test 에서 1건만 확인)
- [ ] 5 script 일람 표 — **미확인**
- [x] **CI badge** — L453 .github/workflows/verify.yml + endpoint JSON artifact PASS
- [ ] compare_outputs.py — **미착수**
- [x] **Dockerfile + conda_env.yml** — L452 PASS (artifact, 빌드 미검증)
- [ ] LLM prompt 대안 — **미착수**
- [ ] TROUBLESHOOTING.md — **미착수**
- [ ] verification_failure.md issue template — **PASS (L457 ISSUE_TEMPLATE/verification_failure.md)** ← 사실상 +1

→ Layer C 실제 카운트: **3 / 8**

### Script 작성 규칙 — **미평가** (verify_*.py 본체 이번 loop 범위 아님)

### Repository 인프라 — **3 / 9 PASS**
- [ ] claims_status.json — **미착수**
- [ ] LICENSES.md — **미착수**
- [x] **CITATION.cff** — L459 PASS (placeholder DOI)
- [ ] .github/CONTRIBUTING.md — **미착수**
- [ ] .github/CODE_OF_CONDUCT.md — **미착수**
- [x] **.github/PULL_REQUEST_TEMPLATE.md** — L457 PASS
- [x] **.github/ISSUE_TEMPLATE/{bug_report, verification_failure, suggestion}.md** — L457 PASS
- [x] **.github/workflows/verify.yml** — L453 PASS
- [ ] .github/og-image.png — **미착수**
- [ ] results/INTERNAL_IDS.md — **미착수**

### 다국어 — **0 / 6 PASS**
모두 미착수.

### 모바일 친화 — **미평가** (README/PDF 자체 미작성)

### 출판 — **0 / 7 PASS** (모두 README/PDF/Zenodo deposit 후행)
- L459 CITATION.cff + .zenodo.json 은 deposit 직전 단계 artifact.
- DOI 는 `10.5281/zenodo.PLACEHOLDER` 그대로 (실제 발급 안 됨).

### Layer B 출판 전 grep 검증 — **미실행**
PDF 자체가 없으므로 `L\d{2,3}` / `P\d{1,2}` / `Branch [AB]` / `Pillar [1-5]` / `F[1-3]` / `loop` grep 검증 0건 수행.

### 종합 publish-readiness 카운트

| Layer | PASS | 전체 | 비율 |
|---|---|---|---|
| A (README) | 0 | 11 | 0% |
| B (paper/main_en.tex) | 0 | 12 | 0% |
| C (verification) | 3 | 8 | 38% |
| Repo 인프라 | 4 | 10 | 40% |
| 다국어 | 0 | 6 | 0% |
| 출판 | 0 | 7 | 0% |
| **전체** | **7** | **54** | **13%** |

(Script 작성 규칙 / 모바일 / grep 검증은 종속 항목이라 카운트 제외.)

---

## 3. 학계 acceptance 재추정

### 3.1 직전 추정 vs 현재
- 직전 (L432 / L441 부근 추정): 8 인 합의 "JCAP 정직 falsifiable phenomenology" 포지셔닝, PRD Letter 진입 조건 미달.
- 현재 L442~L460: 추가 *내용* 진전 없음. **인프라(Layer C + Repo)** 만 진전. 본문 0%.

### 3.2 현재 acceptance 정직 추정 (정량 평가가 아닌 구조적 평가)

| 저널 | 진입 조건 (paper/base.md §14, L6 재발방지) | 현 상태 | Acceptance 재추정 |
|---|---|---|---|
| **PRD Letter** | Q17 완전 달성 OR (Q13 + Q14) 동시 — L6 미달 명시 | 미해소 | **rejected at editorial screening** (본문 부재) |
| **PRD regular** | 본문 + 통계 부록 + 재현 환경 + 22 한계 정직 | Layer B 0%, Layer C 38% | **현재 desk-reject** (manuscript 부재). Layer A/B 작성 후 50% 가능 |
| **JCAP** | "정직 falsifiable phenomenology" 포지셔닝 (8 인 합의) | Layer C 인프라 일부 + REVIEW 다수 정직성 유지 | **submission-ready 상태로 진입은 가능** (Layer A/B 작성 후), 현재 **0%** (본문 부재) |
| **MNRAS Letter** | SQT BAO+SN+CMB 결합 단일 figure 핵심 | L443 make_figures.py 산출 figure 부재 | **rejected at editorial** (figure 부재) |
| **arXiv preprint** | 본문 자체 | (paper/base.md 채택 정책 = 미사용) | **N/A — 정책상 arXiv 안 함** (§14 기재) |
| **Zenodo + GitHub** (정책상 메인 출판 채널) | repo public + DOI + CITATION + verify CI | Repo 인프라 4/10 + Layer C 3/8 + DOI placeholder | **soft-launch 가능 (v0.x)**. v1.0 release 는 README + PDF + DOI 교체 후 |

### 3.3 정직 한 줄 acceptance 평가
- **"19 loop 후 학계 acceptance 가 상승했다"** 는 주장은 데이터 기반 근거 없음 (본문 manuscript 0%).
- 실제 진전은 **재현성 인프라 (Docker, conda, CI, issue/PR template, CITATION.cff)** 4 건 PASS.
- Layer A (README) 와 Layer B (paper) 작성 없이는 **어떤 저널/preprint 채널로도 acceptance 평가 자체가 시작되지 않는다.**
- L444/L446/L449/L451/L454/L455/L456/L458/L460 의 **9 개 빈 loop** 는 "실행되었지만 결과 없음" 이 아니라 **"실행 자체가 일어나지 않음"** 이다 — 향후 base.fix.md 또는 INTERNAL_IDS.md 에 "blank loop" 로 기록 필요 (L6 재발방지 "결과 왜곡 금지" 적용).

---

## 4. L461 권고 (다음 step)

우선순위는 paper/base.md §14 의 P0 항목 기준.

1. **P0 — Layer A README.md 초안** (en + ko) — 현 0% 상태 해소가 가장 큰 acceptance gain.
2. **P0 — Layer B paper/main_en.tex 1~7 장 골격** — base.md → tex 변환 (수식/figure 채움 후행).
3. **P0 — L450 6×6 비교표 본체** (REVIEW 1 줄만 존재 → 표 + 캡션 + §5.7 삽입) — 작은 작업으로 §5.7 실질 채움.
4. **P1 — L442 statistical methods appendix 본문** (R3 reviewer 응답 직결 항목).
5. **P1 — L447 S_8 PASS_STRUCTURAL 8+4 실제 실행** (DESIGN → REVIEW).
6. **P1 — L448 BTFR zero-point 코드 + 결과** (DESIGN → REVIEW).
7. **P2 — L443 figure 산출 검증 + I1~I4 5 종 figure 확정**.
8. **P2 — Zenodo deposit + DOI 교체** (L459 placeholder 해소).
9. **P2 — L444/L446/L449/L451/L454/L455/L456/L458/L460 9 개 빈 loop**: base.md / INTERNAL_IDS.md 에 "skipped — reason" 기록 또는 임무 재할당.

---

## 5. 정직 한 줄

요청한 "19 loop 종합" 은 사실은 **6 REVIEW + 3 DESIGN-only + 10 빈 loop** 의 9 loop 종합이며, paper/base.md §14 publish-readiness 는 13% (재현성 인프라만 진전, 본문 0%) — 학계 acceptance 평가는 현재 시작조차 못 한 상태다.
