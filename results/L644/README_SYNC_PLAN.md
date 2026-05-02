# L644 — README.md / README.ko.md 갱신 plan

**작성일**: 2026-05-02
**상태**: PLAN ONLY — README edit 0건, 디스크 다른 파일 edit 0건
**작성자**: L644 세션 (단일 에이전트)
**선행 의존**: L549/L552/L562/L564/L566/L568/L569/L582/L591/L593/L623/L633/L634/L635/L637/L638
**[최우선-1] 준수**: 본 plan 에는 수식 0줄. README 본문 어휘 변경만 다룸.

---

## §1. 현재 상태 grep 결과 — 무엇이 잔존하는가

### §1.1 README.md (English/한국어 혼합 — 99줄, 구버전)

레포 최상위 `README.md` 는 본 세션 산출물 기준으로 **심각하게 stale** 함.

| 항목 | 현재 README.md 진술 | 실제 상태 (L568/L593/L623/L634) |
|---|---|---|
| 헤드라인 | "최종 판정 (2026-04-10). 4-gate AND 검사 실패 → No-Go branch 확정" | 폐기됨. L568 ★★★★ -0.05 / L623 정직성 ★★★★★+ trajectory 미반영. No-Go 어휘는 Phase 4 시기 결론. |
| 가설 명칭 | "SQMH — Spacetime Quantum Metabolism Hypothesis" | 현재 표기는 SQT (Spacetime Quantum Theory). README.ko.md 는 갱신, README.md 는 미갱신. |
| 디렉토리 표 | `base.md`, `base_2.md`, `paper/negative_result.md`, `base.todo.result.md` | 현행 paper 구조 (`paper/main_en.pdf`, `paper/verification/`, `claims_status.json`, `results/L5xx`, `results/L6xx`) 미반영. |
| Phase 표 | Phase 0–4 (DESI DR2, MCMC, k-essence, Kletetschka) | Phase 22-46 (L491-L644) 78+ 산출물 미반영. |
| 4-gate 표 | CPL/V_RP/V_exp/LCDM AND 결과 | L501 이후 prediction → phenomenology 재포지셔닝, 6 falsifier pre-registration (L498) 미반영. |
| 라이선스 | "TBD (arXiv 투고 전 결정)" | (a) 출판 시도 영구 금지 사용자 새 제약 위배. (b) README.ko.md 는 MIT + CC-BY-4.0 명기. |
| 금지 어휘 | grep 결과 "통합 이론" / "0 free parameter" / "단일 이론" / "free parameter" 모두 **0건** (이미 없음 — 다만 갱신 시 재유입 방지 필요). | — |

### §1.2 README.ko.md (현행, 111줄, L524 라벨)

L524 까지 sync 완료된 *상대적으로* 최신 버전. 그러나 본 세션 (L568 이후) 산출물 미반영:

| 누락 항목 | 출처 | README.ko.md 현 상태 |
|---|---|---|
| Status ★★★★ -0.05 / 정직성 ★★★★★+ 트라젝토리 | L568 / L593 / L623 | "L516 hidden-DOF 재등급" 까지만 명시; L568 이후 없음. |
| 4 priori path 박탈 disclosure | L549 / L552 / L562 / L566 | 부분적 — Path-α 만 본문 1회 언급. 4개 path 전체 박탈 사실 없음. |
| Active fabrication 90% disclosure | L564 | 전무. fabrication 어휘 0건. |
| Mass redef 영구 종결 | L582 | 전무. |
| 6 falsifier pre-registration 카탈로그 | L498 / L644 plan 항목 | falsifier_Neff 메타값만 있음, 6개 항목 자체 카탈로그 없음. |
| Multi-session derivation 의무 | L633 H2 | 전무. |
| 출판 시도 영구 금지 | 사용자 새 제약 (본 세션) | 정반대 — JCAP majority-acceptance 13–14% 헤드라인 잔존 (라인 23). |
| paper plan v3 cross-ref | L634 | 전무. |
| claims_status v1.3 plan cross-ref | L638 | claims_status.json 링크만 있음 (L638 v1.3 plan 미링크). |
| erratum 디렉터리 cross-ref | L635 | 전무. |
| verify_*.py 7/7 PASS | L637 | "나머지 4개 스크립트는 paper/verification/" 만 — 7개 스크립트로 갱신 + PASS 카운트 없음. |
| "통합 이론" / "0 free parameter" 영구 폐기 선언 | L569 / L591 | 본문 부재 (= 잠재적 재유입 위험). 명시적 폐기 선언 필요. |

---

## §2. 갱신 항목 표 (README.md / README.ko.md 공통)

> 아래 표의 각 행은 **plan 만**. 실제 edit 은 L644 후속 세션 (Rule-A 8인 라운드 + Rule-B 4인 코드리뷰 통과 후) 에서 수행.

| # | 갱신 위치 | 변경 종류 | 출처 라벨 | 우선순위 |
|---|---|---|---|---|
| U1 | README.md 전면 | rewrite — README.ko.md 의 L524 구조를 영문 mirror 로 가져오고 L644 baseline 으로 갱신 | L568/L623 | P0 (gating) |
| U2 | 헤드라인 status 라인 | "★★★★ -0.05 / 정직성 ★★★★★+" 추가; trajectory 한 줄 (L568 → L593 → L623) | L568/L593/L623 | P0 |
| U3 | TL;DR 섹션 | "통합 이론" / "0 free parameter" / "zero free parameter" / "single unified theory" 어휘 영구 폐기 명시 | L569/L591 | P0 |
| U4 | TL;DR 섹션 | mass redef (질량 재정의) 영구 종결 disclosure 1줄 | L582 | P0 |
| U5 | 정직성 선언 블록 | 4 priori path (Path-α/β/γ/δ) 박탈 사실 + 박탈 사유 한 줄씩 (총 4줄) | L549/L552/L562/L566 | P0 |
| U6 | 정직성 선언 블록 | active fabrication 90% disclosure — 본 세션 자가감사 결과 한 줄 | L564 | P0 |
| U7 | TL;DR / Falsifier 섹션 | 6 falsifier pre-registration 카탈로그 표 (이름, 조건, DR3 conditional 여부) | L498 / L644 | P1 |
| U8 | 정직성 선언 블록 | multi-session derivation 의무 — single-session 도출 금지 사유 1줄 | L633 H2 | P1 |
| U9 | 라이선스 / 인용 섹션 | **출판 시도 영구 금지** 선언 (JCAP / arXiv / PRD 등 모든 외부 투고 금지). 인용 BibTeX 는 internal-citation 용 보존. | 사용자 새 제약 (본 세션) | P0 |
| U10 | TL;DR 라인 23 (JCAP 13–14%) | **삭제** — U9 와 충돌. 외부 투고 추정 어휘 완전 제거. | 사용자 새 제약 | P0 |
| U11 | 문서 섹션 | paper plan v3 cross-ref (`results/L634/PAPER_PLAN_v3.md` 또는 해당 경로) | L634 | P1 |
| U12 | Claim 상태 표 | claims_status v1.3 plan cross-ref (`results/L638/CLAIMS_STATUS_v1.3_PLAN.md`) | L638 | P1 |
| U13 | 문서 섹션 | erratum 디렉터리 cross-ref (`results/L635_erratum/`) | L635 | P1 |
| U14 | "5초 안에 검증" 섹션 | verify scripts 7/7 PASS 명시 + 7개 스크립트 명단 | L637 | P0 |
| U15 | 디렉토리 표 (README.md) | `base.md` 라인 → `base.md` (원본, 보존) + `base_2.md` (정정본) + `paper/`, `claims_status.json`, `results/`, `simulations/` 의 현행 구조로 재작성 | 본 세션 ls 결과 | P0 |
| U16 | Phase 표 (README.md) | Phase 0–4 표 → Phase 22-46 또는 L4xx-L6xx 라벨 기반 표로 교체. (raw 78+ 산출물을 묶어 8–10 그룹으로 축약) | 본 세션 results/ 디렉토리 | P1 |
| U17 | 4-gate 표 (README.md) | 삭제 또는 "Phase 4 legacy snapshot" 라벨로 격하. 현행 결정 표는 §6.1 (paper) + claims_status.json 으로 위임. | L501 재포지셔닝 | P0 |
| U18 | 헤더 명칭 | README.md 의 "SQMH" → "SQT" 통일 (README.ko.md 와 정합) | L501 명명 | P0 |

---

## §3. README.ko.md 동기 항목 (한국어 mirror)

README.md 갱신 후 **동시 commit** 으로 README.ko.md 도 동기화 필요. 동기 항목:

1. U2 — 헤드라인 status 라인 (한국어 표현으로): "★★★★ -0.05 / 정직성 ★★★★★+; L568→L593→L623"
2. U3 — "통합 이론" / "0 free parameter" 어휘 영구 폐기 (한국어 명시) — 라인 위치: TL;DR 또는 정직성 선언 직전
3. U4 — Mass redef 영구 종결 한국어 1줄
4. U5 — 4 priori path 박탈 disclosure (Path-α/β/γ/δ 박탈) — 정직성 선언 블록 라인 99-106 확장
5. U6 — Active fabrication 90% disclosure (한국어)
6. U7 — 6 falsifier pre-registration 카탈로그 표 (DR3 조건부 표기)
7. U8 — Multi-session derivation 의무 (한국어 1줄)
8. U9/U10 — 라인 23 JCAP majority-acceptance 13–14% **삭제**; "출판 시도 영구 금지" 선언 라인 추가 (라이선스 직전)
9. U11/U12/U13 — 문서 섹션 (라인 87-98) 에 paper plan v3 / claims_status v1.3 plan / erratum 링크 추가
10. U14 — "5초 안에 검증" 섹션 (라인 25-34) 에 verify_*.py 7/7 PASS 명시 + 7개 스크립트 명단
11. U17 — README.md 4-gate 표 격하/삭제와 정합되게 README.ko.md §6.1 caveat row 보존 확인
12. README.draft.md 도 README.md edit 시 동시 갱신 (영문 lineage 보존용) — 단, draft 가 실제 게시 README 가 아니면 우선순위 P2

번역 일관성 정책: `TRANSLATION_POLICY.md` 참조. 핵심 용어 매핑:
- "active fabrication" → "능동적 조작 (active fabrication)" (영문 병기 첫 등장 시)
- "priori path" → "사전 (priori) 경로"
- "publication ban" → "출판 시도 영구 금지"

---

## §4. 8인 Rule-A 의무

본 plan 의 실제 README edit 시점에 **Rule-A 8인 순차 리뷰** 강제. 사유:

- U3 (어휘 영구 폐기), U5 (priori path 박탈 disclosure), U6 (active fabrication 90%), U9 (출판 영구 금지) 는 모두 **이론적/정책적 클레임** → Rule-A 적용 (CLAUDE.md L6 항목 "이론 클레임").
- U14 (verify 7/7 PASS) 는 코드 검증 결과 인용 → **Rule-B 4인 코드리뷰** 병행 (verify_*.py 7개 실제 PASS 재확인).
- U10 (JCAP 라인 삭제) 는 사용자 새 제약 직접 반영이므로 8인 리뷰 PASS 후 즉시 적용 가능.

권장 순서:
1. Rule-B 4인 — verify_*.py 7개 재실행 + PASS 카운트 확인 (U14 근거 확보)
2. Rule-A 8인 — U2/U3/U4/U5/U6/U7/U8/U9/U17 9개 항목 순차 합의
3. README.md / README.ko.md 동시 edit (single commit)
4. paper plan v3 / claims_status v1.3 plan / erratum 디렉터리 실제 경로 확인 후 cross-ref 링크 삽입

---

## §5. 정직 한 줄

본 plan 은 **plan 일 뿐**이며, README 의 stale 함을 시인하는 자체가 정직성의 일부다 — "stale 한 채로 두는 것이 가장 큰 부정직" (L623 정직성 ★★★★★+ trajectory 와 정합). 다만 **출판 시도 영구 금지** (U9) 라는 새 제약 하에서, README 갱신의 목적은 *외부 referee 설득* 이 아니라 *내부 lineage 일관성 + 자기감사 추적성* 임을 명시한다.

---

## 부록 A — 현재 README 어휘 grep 결과

```
$ grep -niE "통합|0 free|zero free|integrated|단일 이론|free parameter" README.md README.ko.md
README.ko.md:85: (DOI 관련 — false positive)
```

→ "통합 이론" / "0 free parameter" 등 금지 어휘는 현재 README **본문 0건**. 다만 본 plan 의 U3 는 *재유입 방지용 영구 폐기 선언* 을 명시적으로 추가하는 것이며, 현재 부재 ≠ 향후 차단 보장 아님.

## 부록 B — 본 세션 위반 0건 자가감사

- README.md edit: 0
- README.ko.md edit: 0
- README.draft.md edit: 0
- paper / claims_status / 다른 results 디렉터리 edit: 0
- 본 plan 내 수식: 0줄
- [최우선-1] 위반: 0건

산출물 단일 경로: `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L644/README_SYNC_PLAN.md`
