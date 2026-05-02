# L359 NEXT STEP

## 즉시 (Day 0–1)
1. `tools/mcmc_diag.py` 작성 — chain HDF5/npz 입력 → Rhat/ESS/τ/PPC 출력 JSON.
2. 기존 chain 인벤토리 작성: L4 C10k/C11D, L5 A12/C28, L6 fixed-θ/marginalized, L33 Q93, L34 joint.
3. 인벤토리 chain 일괄 진단 (병렬, multiprocessing 9 worker).

## 단기 (Day 2–4)
4. PASS/WARN/FAIL 분류표 산출 → `results/L359/diagnostics_summary.csv`.
5. WARN chain은 chain length ×4 연장 후 재진단.
6. FAIL chain은 dynesty NS로 대체 실행 검토.

## 중기 (Day 5–7)
7. Posterior Predictive: 각 PASS chain에서 200 draw 추출 → joint chi^2 분포 plot, 관측치 위치 표시.
8. 논문 supplementary 표 초안: 후보×진단 grid.

## 산출물 파일
- `tools/mcmc_diag.py`
- `results/L359/diagnostics_summary.csv`
- `results/L359/ppc_plots/`
- `results/L359/REVIEW.md` (본 세션 산출)

## 게이트
PASS 비율 ≥ 70% 미달 시 L360에서 sampler 전면 재설계 (dynesty 또는 nautilus 도입).

## 한국어 한 줄
정직: 기존 chain 다수가 임계 미달일 가능성이 높아 재실행 비용 부담을 감수해야 한다.
