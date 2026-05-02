# L357 NEXT STEP

정직 한국어 한 줄: 다음 단계는 spec 의 5개 데이터 로더 + ϒ-marginalized SPARC chi2 + joint log_likelihood 모듈을 분리 구현하고 short-chain (n_steps=200) smoke test 까지만 통과시키는 것이다 (이번 단계 산출은 코드 0줄, spec 만).

---

## 단계 분해

### Step A — 데이터 lock (코드 0줄)
1. SPARC 175 갤럭시 raw table 경로 확정 (CobayaSampler 미보유 → 별도 공식 출처 확정).
2. DESI BAO DR2 13pt + cov 파일 경로 확인 (`bao_data` 공식).
3. Planck compressed CMB 3-vector + cov 출처 확정 (Chen-Huang-Wang 또는 Planck 2018 official).
4. cluster pool: 어떤 stack/관측량 사용할지 8인 합의 후 lock.
5. cosmic anchor: H0 SH0ES vs BBN ω_b 중 택일 후 lock.

→ 산출: `results/L357/DATA_LOCK.md`.

### Step B — 모듈 골격 (4인 자율 분담)
- `simulations/l357/data_loaders.py`: 5개 로더, 각 `load_*() -> (obs, cov_or_sigma, meta)` 통일 인터페이스.
- `simulations/l357/chi2_terms.py`: 5개 chi2 함수, 각 `chi2_*(theta, data) -> float|None`.
- `simulations/l357/sparc_marginal.py`: ϒ analytic marginalization closed form + 단위 테스트.
- `simulations/l357/log_post.py`: `log_prior`, `log_likelihood`, `log_posterior`. -inf 처리 명시.
- `simulations/l357/run_emcee.py`: spawn Pool, 48 walker, n_steps=200 smoke test → 5000 production toggle.

4인 자율 분담 (역할 사전 지정 금지, CLAUDE.md 최우선 원칙).

### Step C — Smoke test 통과 조건
1. n_steps=200, 48 walker, 8 worker spawn pool.
2. acceptance fraction 0.2~0.5 범위.
3. 5개 dataset chi2 가 worker 안에서 각각 finite 로 계산되는지 로그 출력.
4. ϒ marginalization 결과가 갤럭시별 brute-force 2D ϒ 그리드 적분과 1e-3 상대오차 이내 일치 (3개 갤럭시 샘플로 검증).

→ 통과 시 production run (5000 step) 진입 승인.

### Step D — Production run
- 8인 합의로 prior box 확정 후 실행.
- chain 저장 + dataset 별 pull plot + corner plot.
- R̂ < 1.01, τ×50 < n_steps 미달 시 step 연장.

### Step E — 결과 보고
- `results/L357/REPORT.md`: dataset 별 chi2, dAICc, marginal posterior 표.
- 5개 채널 cross-scale 일관성 진단 (하나라도 큰 tension 이면 정직 기록).

---

## 의존성 / Blocker

- SPARC 데이터 raw 접근 경로 미확정 → Step A 우선.
- cluster pool 정의 미합의 → 8인 토의 필요 (Rule-A).
- ϒ closed form 유도는 팀 독립 도출 — spec 에 수식 미제공.

## 즉시 실행 항목 (이번 세션 외)

다음 세션에서:
1. Step A 데이터 5개 lock + DATA_LOCK.md 작성.
2. 8인 토의로 cluster pool / anchor 선택 1회.
3. Step B 모듈 골격 4인 분담 시작.

본 세션은 spec 3 문서 (ATTACK_DESIGN, NEXT_STEP, REVIEW) 까지로 종료.
