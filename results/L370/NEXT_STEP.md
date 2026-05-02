# L370 NEXT_STEP

**정직 한국어 한 줄**: companion paper 는 outline 단계이며 다음 세션에서 Sec 2/3/4 의 구체적 표·그림 목록을 채워야 한다.

## Immediate next (L371 후보)
1. **Sec 2 표 후보 정의**: 적분 규약 비교 (N_GRID 800 vs 4000 의 chi² 차이 ~0.75 — L33 적분 버그 사례), ODE forward vs backward shooting 폭주 사례.
2. **Sec 3 파이프라인 다이어그램**: 5-dataset → individual chi² → joint → MCMC/dynesty → posterior → CPL 추출. 데이터 소스 URL 명시.
3. **Sec 4 cluster pool 표**: L46–L56 후보 N개의 (Δχ², Δ ln Z, μ_eff, S8) 정리 + SVD 결과.
4. **Sec 5 재현 명령서**: README 수준 reproducibility script (단, 새 코드 작성 금지 — 기존 L33/L46–L56 스크립트 인용만).

## Open questions
- companion paper 저널 타깃: JCAP methods section, PRD Computer Physics, 또는 SoftwareX. 8인 팀 합의 필요.
- L48 T20 sigma8 grid scan 결과를 cluster pool Sec 4 에 포함할지, 메인 논문 본문에 둘지.
- L33 적분 버그 (2026-04-19 발견) 를 Sec 2 의 cautionary case study 로 명시 인용할지 — 정직 기록 원칙상 권장.

## Out of scope (지금 하지 말 것)
- 새 시뮬레이션 (L370 은 paper outline 전용).
- 메인 논문 본문 수정.
- DR3 스크립트 실행 (CLAUDE.md L6: DR3 공개 전 금지).

## Decision gates before drafting
- [ ] 8인 팀 Rule-A 리뷰: companion paper 분리 정당성 + 메인-companion 경계 정의.
- [ ] 4인 팀 Rule-B 리뷰: Sec 2/3 의 코드/데이터 인용 정확성.
- [ ] 저널 타깃 확정.
