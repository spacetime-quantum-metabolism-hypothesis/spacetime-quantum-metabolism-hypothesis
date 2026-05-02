# L336 NEXT STEP

## 즉시 (today, ~3 hr)

1. **SPARC ϒ⋆ analytic marginalizer 작성**
   - 파일: `simulations/l336/sparc_marg.py`
   - 갤럭시 i 의 v_obs(r) = sqrt( ϒ_d v_d² + ϒ_b v_b² + v_gas² + v_SQT(θ,r)² )
   - ϒ_d, ϒ_b 가 v² 에 선형 → χ²(ϒ) 가 ϒ 에 quadratic → 닫힌 형식 marginal.
   - lognormal prior 0.11 dex 는 Gaussian-in-lnϒ 근사 (한 번만, 필요시 1D quadrature).
   - 단위테스트: ϒ_d=1 fix vs marg 결과가 LCDM mass model 에서 동일 ln L_max 재현.

2. **5채널 결합 likelihood 빌드**
   - 파일: `simulations/l336/joint_likelihood.py`
   - 기존 모듈 재사용: `desi_fitting.py` (BAO), `sn_desy5.py` (SN, zHD), `cmb_compressed.py` (R, l_A, theta_*), `rsd_growth.py` (fσ8).
   - chi² 실패시 -np.inf return, sentinel 금지 (L4).
   - blobs: chi2_bao, chi2_sn, chi2_cmb, chi2_rsd, chi2_sparc.

3. **Smoke test (100×200)**
   - emcee, walker=100, step=200, 9-pool.
   - 측정: time/call, R̂_partial, walker acceptance fraction (0.2–0.5 정상).
   - acceptance < 0.1 → stretch a parameter 조정 또는 DE-MC 전환.

## 단기 (this week, ~24 hr wall)

4. **Production emcee** 1000 walker × 10000 step.
   - HDF5 backend, checkpointing every 500 steps.
   - 9-pool, OMP/MKL/OPENBLAS=1.
   - np.random.seed(42) emcee 내부.
   - 후보 모델: L335 까지 살아있는 SQT variant 1개 + LCDM null.

5. **dynesty evidence run** (cosmology-only, ϒ⋆ marg 적용).
   - dynamic, nlive_init=500, nlive_batch=250, dlogz=0.05.
   - rstate=np.random.default_rng(42).

6. **Diagnostics + Tension**
   - corner plot, R̂ table, IAT table.
   - Q_DMAP for SQT and LCDM.
   - SPARC-only vs cosmology-only Bayes factor 따로 계산 (L328 모순 추적).

## 중기 (다음 loop, L337–L338)

7. **F1–F4 판정**
   - 통과 → paper section "Joint Constraints" 작성, 8인 리뷰.
   - Fail (특히 F4) → SPARC ↔ cosmology tension 의 출처 분석:
     - 후보 a: SQT 가 SPARC 에서 v_SQT(r) shape 부적합 (radial slope 문제).
     - 후보 b: cosmology 채널이 SQT ψ^n term 을 SPARC 와 다른 부호로 선호.
     - 후보 c: Yukawa-like screening 누락.

8. **Cluster + anchor 채널 추가 (D6, D7)**
   - SH0ES H0 prior 추가시 H0 tension 영향 quantify.
   - DES-Y3 cluster counts (S_8) — L5 재발방지: μ_eff ≈ 1 SQT 는 S_8 변경 거의 없음, expected null.

## 의존성 / 리스크

- macOS python3 (CLAUDE.md). multiprocessing spawn context 강제.
- emcee + Python 3.14 — `np.bool_` json 직렬화 깨짐 → `_jsonify` 변환기 재사용 (L4).
- dynesty 3.x rstate (L5 재발방지).
- SPARC 데이터 경로 확정 필요 (Lelli+16 official text). 기존 L20x 에서 사용한 경로 재활용.

## 정직 budget 예상

- Stage A–C: ~4 hr 인적 + ~30 min 컴퓨트.
- Stage D (production emcee): **18–24 hr 컴퓨트** (analytic-marg 적용 가정 6 hr; 미적용 시 28 hr).
- Stage E (dynesty): 6 hr 컴퓨트.
- 총 wall: **24–30 hr**, CLAUDE.md 가 명시한 12–24 hr 상단에서 살짝 초과 가능.
- 초과시 step 5000 으로 단축 또는 walker 500 으로 축소.
