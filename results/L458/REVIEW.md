# L458 REVIEW — LICENSES.md + LICENSE

Date: 2026-05-01
Scope: 라이선스 메타데이터 정비 (독립 세션, 단일 작업).

## 산출물

- `/LICENSE` — MIT 본문 + dual-license note (코드 MIT, 텍스트/그림 CC-BY-4.0,
  upstream 데이터 별도)
- `/LICENSES.md` — 디렉토리별 라이선스 표 + upstream 데이터 표
- `/results/L458/REVIEW.md` — 본 문서

## 정책 요약

- 코드 (`paper/verification/*.py`, `simulations/**/*.py`, `*.sh`, `Dockerfile`,
  `requirements.txt` 등) → **MIT**
- 텍스트/그림 (`paper/*.md`, `paper/figures/*`, `figures/*`, `refs/*.md`,
  `results/L*/*.md`, top-level `*.md`) → **CC-BY-4.0**
- 참고문헌 메타데이터 (`paper/references.bib`) → CC0-1.0 (사실 데이터)
- Upstream 데이터 (SPARC, DESI BAO, Pantheon+, DES-Y5, Planck, RSD) →
  upstream 라이선스 유지. 현재 레포에는 `data/` 디렉토리 미존재 (런타임
  fetch). SPARC 항목은 프로젝트가 SPARC 곡선을 참조하므로 미래 vendor 시
  대비해 표에 포함.

## 검토 결과

- L458은 단일 메타데이터 작업으로 8인/4인 리뷰 트리거 없음 (이론/코드 수정
  아님).
- 기존 `LICENSE` 부재 확인 후 신규 생성.
- 표는 실제 디렉토리 구조 (`paper/`, `simulations/`, `refs/`, `figures/`,
  `results/`, top-level) 기준. 미존재 디렉토리 (`data/`) 는 별도 NOTE 처리.
- Dual-license 충돌 가능 디렉토리 (`paper/verification/`, `simulations/`,
  `results/L*/`) 는 "code MIT / prose CC-BY-4.0 / per-file basis" 명시.

## 정직 한 줄

데이터 디렉토리 (`data/`) 는 현재 레포에 없으며 SPARC 항목은 미래 vendor 대비
선언일 뿐 — 현 시점 redistributed upstream 파일은 0개임을 LICENSES.md NOTE
에 명시함.
