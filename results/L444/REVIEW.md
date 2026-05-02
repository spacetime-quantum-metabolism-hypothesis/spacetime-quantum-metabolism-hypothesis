# L444 — REVIEW (4인 자율 분담 코드/문서 리뷰)

대상: `paper/TABLES.md` (T1–T4).
모드: 4인팀 (역할 사전지정 없음). 자율 분담 결과 — A: T1/T2 정합, B: T3 falsifier 임계, C: T4 honest count, D: LaTeX 형식.

## A — T1/T2 정합
- T1 6공리는 L73 SQT_AXIOMS_FORMAL.md 와 1:1 일치. F/P 코드는 a4(emergent metric Lagrangian 보류) + a5(SM 입자 보류) → P. 정직 OK.
- T2 D1–D5 ``From'' 열은 axiom 의존성을 정확히 추적. D5 partial 표시 (1/π 모호) → T4#21 cross-link 정상.
- F1–F4 모두 V (verified). L75/L76 결과 그대로 인용. 누락 없음.
- 의견: paper/02_sqmh_axioms.md (L0/L1)과의 매핑은 별도 필요 (NEXT_STEP.md #3).

## B — T3 falsifier 임계
- 22행 채움 OK. P1–P14, G2 (15) + T17/T20/T22/T26/T35/T36 (6) + BTFR (1) = 22. 일치.
- T35 (EP)와 P3 (depletion zone)이 부분 중복 → ``T35 = EP-equivalent of P3''로 표기 명시. 중복 합리화.
- T36 (a_0(z))과 P7 동일 — ``T36 = P7-equivalent (SKA channel)''. 정직.
- Status 코드 일관 — O는 이미 통과한 것만(P5 BBN, P8 Milgrom 4.9%, P10 Ġ/G LLR, T26 GW170817, BTFR slope=4). 과대 라벨 없음.
- **주의**: P8 (Milgrom 4.9%)는 partial derivation (D5 P 코드)인데 status는 O — 도출 status와 관측 통과 status는 별개라는 점 표 캡션에 명시 권장.

## C — T4 honest count
- ``Zero free parameter'' 주장 거짓(#1) 명시 OK. CLAUDE.md ``결과 왜곡 금지'' 준수.
- τ_q 60 dex 충돌(#2): L55/L56 결과 정직 반영.
- σ_0(k)(#5), σ_0(z)(#6) 영구 폐기 — SQT_PROGRESS_SUMMARY.md 사망 강주장과 일치.
- H_0(#7), S_8(#8) 미해결 — paper §8.2/§8.3 그대로.
- DESI w_a 자연 충돌(#9): L78/L112 정직 반영.
- C26 CMB-dead(#14), C28 K13 fail(#15) — paper §8.5/§8.8 일치.
- 22행 모두 `results/` 또는 `paper/` 출처 트레이스 가능 → 정직 OK.
- 누락 의심 점검: alt-20 14-cluster degeneracy (#16), DR3 dependence (#17), K3 phantom artefact (#18), G2 ambiguity (#21), cluster hybrid (#22) 모두 들어감. 없음.

## D — LaTeX 형식
- booktabs (`\toprule`, `\midrule`, `\bottomrule`) 일관.
- `table*` (wide) — T3/T4. `table` (narrow) — T1/T2. 컬럼 폭 합리적.
- `\small` 사용 — 22행 + 7컬럼 환경에서 적절. 더 줄이려면 `\footnotesize`.
- caption + label 모두 `tab:T?_*` 패턴 — `\ref{}` 호환.
- escaping: `&` 없음, `_` 적절. 단 ``$\hat R = 1.37$''에서 escape 정상.

## 합의
모든 행 정직, 모든 출처 추적 가능, LaTeX 컴파일 가능 형태.
조건부 PASS — NEXT_STEP.md #1, #2 (bibtex / §8 동기화)는 후속 작업.

## 정직 한 줄
8인 합의 ★★★★★ - 0.20 등급(L201)에 부합하는 표를 만들었으며 22 limitations에 ``파라미터 0개'' 거짓·τ_q 60dex·H_0·S_8·DESI 충돌을 모두 1행씩 정직 기록했다.
