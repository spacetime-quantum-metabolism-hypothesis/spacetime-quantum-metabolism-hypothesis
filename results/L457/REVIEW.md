# L457 Review — GitHub Issue/PR Templates

## 산출물
- `.github/ISSUE_TEMPLATE/bug_report.md` — 일반 버그 보고용. OS/Python/commit hash + 영향 범위 필드.
- `.github/ISSUE_TEMPLATE/verification_failure.md` — output 불일치 보고용. expected vs observed 표 + 의심 원인 체크리스트 (적분 그리드, 단위, 데이터 버전, 부호 규약).
- `.github/ISSUE_TEMPLATE/suggestion.md` — 새 후보/분석/도구 제안용. SQMH 정합성 + AICc 패널티 항목 포함.
- `.github/PULL_REQUEST_TEMPLATE.md` — CLAUDE.md 재발방지 체크리스트(적분, DR2, 부호, zHD, cp949, trapezoid, base.fix.md, AICc, 8인/4인 리뷰) 통합.

## 설계 원칙
1. **CLAUDE.md 재발방지 항목 직접 반영**: 반복 발생한 실수(L33 적분 버그, DESI DR1/DR2 혼동, xi_q 부호, zHD, cp949 등)를 PR 체크박스로 강제.
2. **Verification failure를 별도 템플릿으로 분리**: 본 프로젝트는 재현성이 핵심 — 일반 버그와 "결과 숫자 차이"를 구분 보고.
3. **정직 원칙**: PR 템플릿 마지막에 "하지 않은 것 / 불확실한 것 한 줄" 강제 필드.
4. **8인/4인 리뷰 규칙**: PR 체크리스트에 명시해 이론/코드 변경 시 절차 준수 유도.

## 한계 / 미포함
- GitHub Actions CI 워크플로우 (lint, smoke test) 는 본 임무 범위 밖.
- Issue form(YAML) 형식이 아니라 markdown 형식 사용 — 임무 사양에 .md 명시.
- 한국어/영어 혼합. 프로젝트 기존 문서 톤(한국어 주도)을 따름.

## 정직 한 줄
템플릿 자체의 실사용 효과는 PR/이슈 발생 전까지 검증 불가 — 첫 사용 시 누락 필드 발견되면 즉시 보강 필요.
