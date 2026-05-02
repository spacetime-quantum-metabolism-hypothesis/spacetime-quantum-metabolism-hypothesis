# L360 NEXT STEP

## 즉시 (D+0 ~ D+1)
1. **σ_0 임베딩 통일 노트** 작성 — 8인 팀 자율 토의로 SPARC / DESI / Planck
   각 채널에서 SQT 어떤 변수 (n0·μ, t_P, σ=4πG·t_P) 가 어디로 들어가는지
   단일 페이지 매핑 표. (CLAUDE.md SI 단위 + sigma=4πG·t_P 규칙 준수.)
2. **데이터 로딩 dry-run** — SPARC (Lelli 2016 머신리더블), DESI DR2 BAO 13pt
   (CobayaSampler/bao_data 공식), Planck compressed (Chen+18 R, l_A, ω_b).
   단위·z 정렬 assertion 추가.

## 단기 (D+2 ~ D+5)
3. **Pair 1: SPARC ↔ DESI** — 가장 위험한 cross-scale 페어부터 (kpc vs Gpc).
   - 각 채널 dynesty (or emcee) MAP — N_walkers ≥ 48, n_steps ≥ 4000.
   - joint MAP — 동일 sampler, σ_0 공유.
   - Q_DMAP 산출. 5σ 초과 시 즉시 KILL 보고.
4. **Pair 2: DESI ↔ Planck** — control. late-vs-early σ_0 일치 여부.
5. **Pair 3: SPARC ↔ Planck** — 가장 약한 사전제약 페어.
6. **삼중 joint (ABC)** — cumulative tension.

## 중기 (D+6 ~ D+10)
7. **Profile likelihood σ_0** — non-Gaussian 검증, 4인 코드리뷰.
8. **민감도** — SPARC galaxy quality cut, DESI BAO 부분집합 (LRG-only,
   BGS-only), Planck θ* 0.3% floor on/off.
9. **REVIEW.md 갱신** — 8인 합의로 GO / NO-GO 판정.

## 장기 (D+11+)
10. Q_DMAP > 5 시: σ_0 → σ_0(k) scale-dep 일반화 가설 수립 (별도 LXX).
11. Q_DMAP < 2 시: PRD/JCAP 본문 "cross-scale universality" 섹션 진입.

## 운영 규칙
- 병렬: `multiprocessing.get_context('spawn').Pool(9)`, OMP/MKL/OPENBLAS=1.
- 후보별 분리 세션 (L4 MCMC 예산 교훈).
- 코드리뷰 4인 자율 분담, 역할 사전 미지정.
- 결과 base.md 와 다르면 base.fix.md 정직 기록.
