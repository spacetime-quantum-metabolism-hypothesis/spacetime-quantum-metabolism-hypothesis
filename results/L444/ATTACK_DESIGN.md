# L444 — ATTACK_DESIGN

작성: 2026-05-01. 임무: T1–T4 LaTeX-ready 표 작성.

## 공격 면 (어떤 방향으로 표를 짜야 약점이 노출되는가)

1. **T1 axioms a1–a6**: 자연어 → 수학 형식. 핵심 노출 — a4/a5는 partial (Lagrangian/UV 미완). a4-a5 순환(L55 §1.2 C 항목)은 표 자체로는 못 메우므로 status 컬럼에 P 표시 + Phase 6 deferment 명시.
2. **T2 derived D1–D5 + foundations F1–F4 + dependency**: D5는 partial (1/π vs 1/(2π) ambiguity, T4#21에 잡힘). F1–F4는 verification 결과. dependency는 텍스트형 그래프 + ``From'' 열 동시.
3. **T3 22 predictions**: SQT-unique 14개(P1–P14, G2) + 표준 검증(T17/T20/T22/T26/T35/T36) + BTFR. 22행 채우는 데 부족하면 T35/T36 분리 + BTFR 추가. ``Threshold''는 falsifier 임계, ``Status''는 O/P/A/C 코드로 정직 분류.
4. **T4 22 limitations**: L48–L201 누적에서 honest gap만 골라 Severity H/M/L. ``zero free parameter'' 주장 거짓(#1), τ_q 60 dex 충돌(#2), σ_0(k)/σ_0(z) 사망(#5,#6), H_0/S_8 미해결(#7,#8), DESI w_a 자연 충돌(#9), Lagrangian partial(#11), 3-regime empirical(#13), D1 31× off in cross-regime(#19), NS regime 결손(#20), G2 1/π 모호(#21), cluster DM hybrid(#22) 모두 반영.

## 정직 검증 포인트
- T1/T2가 paper §2와 충돌 없는가 — 02_sqmh_axioms.md의 L0/L1 구조는 a1+a3+D2의 통합 표현. T1은 더 세분화되지만 동등.
- T3 22 predictions 중 ``zero parameter'' 주장 사용 금지 — T4#1과 충돌.
- T4가 paper §8과 일관 — §8.1~§8.10 전부 매핑.

## 출력 형태
- TABLES.md 단일 파일에 4 표 모두. LaTeX `\begin{tabular}` 직접 paste.
- table*는 T3/T4 (wide), table은 T1/T2 (narrow).
- booktabs 가정 — 코멘트로 PRD ruled 변형 명시.

## 안 한 것 (정직)
- 새 시뮬 없음. 기존 결과 인용만.
- 표의 수치는 모두 인용 (L73 SQT_AXIOMS_FORMAL.md, SQT_PROGRESS_SUMMARY.md, 08_discussion_limitations.md).
- Bibtex 키 부착은 안 함 — paper/references.bib 항목과 매핑 분리 작업 필요.
