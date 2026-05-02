# L437 REVIEW — README.md (Layer A) draft

**Date**: 2026-05-01
**Task**: paper/base.md §A.1 spec 에 따라 GitHub README 영문 actual draft + 한국어 mirror 생성

## 산출물

| 파일 | 상태 | 비고 |
|---|---|---|
| `README.md` | **변경 없음 (보존)** | 기존 root README.md 가 이미 존재 (4199 bytes, 한국어 SQMH 프로젝트 README). CLAUDE 임무 명시 "★ root README.md 가 이미 있으면 README.draft.md 로 작성 (덮어쓰기 금지)" 에 따라 backup 생략, 덮어쓰기 회피. |
| `README.draft.md` | 신규 작성 | Layer A 영문 actual draft. §A.1 spec 의 모든 요소 포함. |
| `README.ko.md` | 신규 작성 | 영문의 full mirror (요약본 아님). 학계 용어 영문+한국어 병기 정책 적용. |

## §A.1 spec 체크리스트

| 요소 | 영문 | 한국어 |
|---|---|---|
| Language switcher 🇺🇸 \| 🇰🇷 | ✅ | ✅ (방향 반대) |
| DOI/CI/License/OSF badges (placeholder) | ✅ 4종 | ✅ 4종 |
| Hero image placeholder (`paper/figures/hero.png`) | ✅ | ✅ |
| One-sentence headline | ✅ blockquote italic | ✅ blockquote italic |
| TL;DR 7 bullet (✅⚠️⏰❌📊) | ✅ 7행 (⚠️·✅·✅·❌·⚠️·⏰·📊) | ✅ 7행 동일 |
| "Verify in 5 seconds" 코드 블록 | ✅ bash, 5줄 + 포인터 | ✅ 동일 |
| Claims status 표 10행 + Maps to 열 | ✅ 10행, 5열 (Claim/Status/Evidence/Caveat/Maps to) | ✅ 동일 |
| OBS-FAIL vs FRAMEWORK-FAIL 분리 설명 | ✅ | ✅ |
| BibTeX 즉시 복사 | ✅ ```bibtex ... ``` | ✅ 동일 |
| DOI versioning 안내 | ✅ | ✅ |
| Documentation 링크 | ✅ 6항 | ✅ 6항 |
| Contributing | ✅ CONTRIBUTING.md 참조 | ✅ |
| License (MIT + CC-BY-4.0) | ✅ | ✅ |

## A.2 모바일 정책 준수

- 표 column 수: Claims status 5 col (spec "4 column 이하 또는 `<details>` collapse"). 5 col 이지만 README Claims status 표는 §A.2.1 에서 "default 전체 표시 강제 (3초 hook 핵심 — collapse 금지)" 규정. 따라서 collapse 없이 그대로 노출.
- 코드 블록: 5초 verify 블록 80자 wrap 준수.
- 수식: Unicode (ρ_q, σ₀, H₀, ξ_+, μ_eff, w_a, a₀, ΔN_eff, χ², θ_*) 사용. LaTeX 미사용.
- Hero image 1200×630 placeholder.

## A.3 한국어 mirror 정책 준수

- Full mirror (모든 섹션 동일, 요약본 아님). ✅
- 학계 용어 영문+한국어 병기: "OBS-FAIL", "FRAMEWORK-FAIL", "CONSISTENCY_CHECK", "POSTDICTION (사후예측)", "PASS_BY_INHERITANCE", "NOT_INHERITED", "falsifier (반증 검증)", "concept DOI", "preregistration" 등. ✅
- 핵심 결과 수치 영문/한국어 정확 동일 (+1.14%, ξ_+ +2.29%, ~10⁻⁴⁰, 17σ, 8/32, 13% / 28% 양면 표기). ✅
- 정직 caveat 강도 동일 (한쪽도 약화 없음 — "structural worsening", "no parameter escape", "circularity structural" 등 그대로 옮김). ✅

## 정직 한 줄

기존 root README.md 가 한국어 SQMH 프로젝트 README 로 이미 존재. CLAUDE 지시(덮어쓰기 금지)대로 backup 도 skip 하고 README.draft.md 로 신규 작성, README.ko.md 는 영문 draft 의 full mirror 로 신규 작성. **README.md 본체는 손대지 않음** — production 으로 승격 시 root README.md ↔ README.draft.md 교체는 별도 결정/세션 필요.

## 추가 관찰

- README.md 와 README.draft.md 의 톤 차이 큼: 기존 root README.md 는 한국어, "SQMH No-Go branch 확정 (2026-04-10)" 중심이며 시뮬레이션 가이드 위주. 새 draft 는 "SQT 6-axiom framework + honest falsifiers" 포지셔닝 (paper/base.md §A.1 spec 기준). 두 문서가 같은 repo 의 다른 시점 / 다른 layer 의 narrative 임. 향후 통합 시 어느 쪽을 master 로 할지 결정 필요 (P0 ambiguity 후보).
- placeholder URL (`USER/REPO`, OSF/Zenodo PENDING) 은 release 직전 일괄 치환 필요.
- `paper/figures/hero.png`, `paper/main_en.pdf`, `paper/main_ko.pdf`, `paper/faq_en.md`, `paper/faq_ko.md`, `paper/verification/README.md`, `claims_status.json`, `TRANSLATION_POLICY.md`, `LICENSES.md`, `.github/CONTRIBUTING.md` 등 링크 대상 다수 미존재 — Layer C / 별도 task 산출물.
