# L349 NEXT STEP

**날짜**: 2026-05-01
**상태**: ATTACK_DESIGN 작성 완료, 데이터 수집 및 8인 팀 독립 이론 도출 단계 진입 대기.
**한 줄 (정직)**: CLASH 25 클러스터 mass profile 데이터를 확보하고 8인 팀에 σ_cluster 도출 방향만 전달하는 것이 다음 액션이다.

---

## 1. 즉시 액션 (T+0 ~ T+1d)

1. **데이터 확보**
   - Umetsu+ 2016 ApJ 821 116 의 stacked Σ(R), ΔΣ(R), full covariance 다운로드.
     - 우선 archive: ApJ supplementary + Umetsu 개인 페이지.
   - Merten+ 2015 ApJ 806 4 의 κ(r) SL+WL joint map (FITS).
   - Zitrin+ 2015 ApJS 219 4 (CLASH SL 모델) 보조.
   - 저장 경로: `data/clash25/` (신규 디렉터리).
   - 공식 출처만 사용 (CLAUDE.md 재발방지: 임의 추정값 금지).

2. **8인 팀 독립 도출 세션 준비**
   - Command 파일 초안에는 다음 **방향만**:
     - "CLASH 25 mass profile 데이터에서 클러스터 스케일 SQMH 보정의 단일 진폭 파라미터 σ_cluster 와 1σ 를 도출하라."
     - "baseline 은 자유 선택. 수식 사전 제공 없음."
   - **금지**: NFW/Einasto 우선순위 힌트, ψ 함수형, 이전 L 결과 인용.
   - 8인은 토의 중 자연 분업.

3. **코드리뷰 4인팀 사전 환경**
   - `simulations/l349/` 디렉터리.
   - multiprocessing spawn + OMP/MKL/OPENBLAS=1 강제 템플릿.
   - numpy 2.x trapezoid, ASCII identifier 만.

## 2. 단기 (T+1d ~ T+5d)

4. **Joint fit 1차 구현**
   - 25 클러스터 × per-cluster (M_vir, c_vir) + 공통 σ_cluster.
   - emcee 또는 dynesty 선택은 4인팀 자율.
   - `np.random.seed(42)` + Windows OMP 가드.
5. **Sanity check**
   - σ_cluster=0 고정 NFW joint chi² 출력. LCDM-NFW baseline 으로 표지.
   - per-cluster c_vir vs M_vir 관계가 Niikura+ 2015 c-M 와 정합.
6. **Boundary 박힘 검사**
   - M_vir, c_vir prior 가 boundary 에 박히는 클러스터 식별.
   - 박히면 prior 범위 확장 후 재실행.

## 3. 중기 (T+5d ~ T+14d)

7. **결과 보고**
   - σ_cluster best-fit ± 1σ.
   - Δχ² (σ_cluster vs 0).
   - AICc, BIC 양쪽 보고.
   - K-CL1/K-CL2/P-CL1/P-CL2 판정.
8. **Cross-check**
   - LoCuSS (Okabe+ 2016) 또는 HSC-XXL (Umetsu+ 2020) stack 으로 σ_cluster 재추정.
   - Selection bias (X-ray vs SZ vs lensing-selected) 비교.
9. **REVIEW.md 갱신**.

## 4. L350 분기 조건

- P-CL1 충족 시: σ_cluster 를 강체 채널로 승격, L350 에서 BCG-mass / IGM-temperature 와 cross-correlation.
- K-CL1/K-CL2 시: 클러스터 채널 KILL 명시 후 SQMH paper draft 의 "scale of validity" 섹션 갱신.

## 5. 사전 차단 (재발방지 인용)

- BAO-only low-Om 결과를 joint 결론으로 혼동하지 않듯, **CLASH 만으로 σ_cluster 를 우주론적 결론으로 인용 금지**. 반드시 LoCuSS/HSC 와 joint 후 결론.
- Hu-Sugiyama θ\* fit formula 정확도 0.3% 처럼, NFW c-M relation 의 systematic floor (~10%) 를 σ_cluster 불확실성에 반드시 추가.
- print() 유니코드 금지, 변수명 ASCII.
- CLAUDE.md L4 K3 phantom-crossing 인공물 사례처럼, σ_cluster 음수 branch 도 동등 탐색 후 SQMH 부호 정합성 (양수) 별도 표기.

## 6. 산출 파일 (예상)

- `data/clash25/Umetsu2016_DSigma.fits`
- `data/clash25/Umetsu2016_cov.fits`
- `data/clash25/Merten2015_kappa.fits`
- `simulations/l349/joint_fit.py`
- `results/L349/sigma_cluster_posterior.json`
- `results/L349/sigma_cluster_corner.png`
- `results/L349/REVIEW.md` (이 세션 첨부)
