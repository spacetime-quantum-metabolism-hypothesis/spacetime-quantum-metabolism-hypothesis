# Adjust — 사이클별 조정 기록

## Cycle 0 (2026-04-10) — 초기 생성
- **상태**: 패키지 구조 생성 완료
- **다음**: CP1 실행 (config.py + metabolism_equation.py)
- **리스크**: DESI DR2 원시 데이터 접근 필요 — 공개 데이터 확인 필요

## Cycle 1 (2026-04-10) — CP1~CP3 실행 + 검증
- **상태**: 7개 시뮬레이션 작성 + 실행 완료. 공식 DESI DR2 데이터 적용.
- **발견된 오류 3건**:
  1. n₀μ SI 자기무모순 실패 (53자릿수 불일치)
  2. wₐ 부호 불일치 (시뮬: +, base.md: -)
  3. DESI Δχ²=-17.76 미재현 (SQMH > ΛCDM 모든 경우)
- **조치**: base_2.md 생성 (수정 5건), CLAUDE.md 재발방지 8건 기재
- **목적 전환**: illustration → verification
- **다음**: CP4 (paper/ 논문 섹션) + base_2.md 반영한 정직한 논문
