# L336 REVIEW — Self-Critique

## 강점

- 5채널 결합으로 L328 의 subset-Bayes 모순을 직접 검증. F4 가 Hard test.
- emcee + dynesty 이중화로 posterior shape 와 evidence 동시 확보.
- ϒ⋆ analytic-marg 이 budget 을 4–5x 단축하면서 정확도 유지.
- Q_DMAP, Suspiciousness 등 tension metric 다중화 (single-number 함정 회피).
- L4–L6 재발방지 모두 반영 (sentinel 금지, rstate, R̂<1.05, MCMC seed, OMP=1, JSON 직렬화).

## 약점 / 리스크

### R1. d=181 차원에서 emcee stretch move 의 효율 저하
- ϒ⋆ analytic-marg 적용시 d≈6 으로 축소되므로 critical 아님. 단, marg 식이 lognormal prior 와 정확히 호환되는지 단위테스트 필수. 0.11 dex 는 ln(ϒ) Gaussian 근사 → ϒ 자체는 lognormal. 1D quadrature fallback 준비.

### R2. SPARC mass-model 의 SQT 결합 형태가 모델별로 다름
- v_SQT(r) 함수형이 후보별 분기. `joint_likelihood.py` 가 모델 dispatch 패턴 필요.
- L4 의 sibling background module collision 위험: 후보 디렉터리 내부 상대 import.

### R3. Compressed CMB 의 충분성
- L6 G3 에서 Hu-Sugiyama theta_* 재계산이 4.6e6 chi2 폭주 확인. **chi2_joint 의 'cmb' 키 직접 사용** (재계산 금지). hi_class 미설치이면 K19 "provisional" 명시.

### R4. ΔlnZ 해석
- L6 재발방지: fixed-θ vs marginalized 혼동 금지. L336 은 dynesty marginalized 만 보고. fixed-θ 인용 금지.
- F2 기준 ΔlnZ > +1 은 약함 (Jeffreys substantial start). +2.5 이상이라야 strong. 현재 L328 trend (~+0.8) 로는 F2 fail 가능성 ≥ 50%.

### R5. SPARC subset Bayes factor 가 음이면
- F4 fail 확정, 의미는 "SQT 가 cosmology 채널에서만 살아있고 회전곡선 데이터는 LCDM/MOND 우위". 이 경우 SQT 후보를 "우주론 전용" 으로 재정의하거나 죽이는 결단 필요.
- 회피용 데이터 cherry-picking 금지.

### R6. Cluster (S_8) 채널 누락
- L5 재발방지: background-only 수정 + μ_eff≈1 → S_8 tension 해결 불가. cluster 추가해도 SQT 가 S_8 개선 못함이 expected. 메인 run 에 cluster 미포함이지만 D6 ablation 으로 quantify, 결과 정직 보고.

### R7. Cosmic anchor (H0)
- SH0ES H0 prior 를 main run 에 넣으면 chi² 가 BAO 와 충돌해 SQT 에 spurious phantom-pull 가능. main 은 anchor-free, ablation 만 anchor 포함. 보고 시 "with/without anchor" 구분.

### R8. budget overflow
- 24–30 hr 은 CLAUDE.md 가 허용한 12–24 hr 상단 초과 risk. step 5000 / walker 500 fallback 미리 설정.

### R9. SPARC ϒ⋆ hierarchical prior 구조
- per-galaxy independent 가정은 정확하지만, ϒ_disk vs ϒ_bulge 사이 상관 등 무시. L336 main 은 simple, L337 에서 hierarchical 확장.

## 8인 / 4인 리뷰 요청 항목 (예정)

Rule-A 8인:
- F1–F4 정의의 합리성 (특히 F2 임계 +1).
- Q_DMAP / Suspiciousness 임계.
- D6/D7 ablation 의 본문 vs supplement 배치.
- SPARC fail 시 후속 결단 (모델 재정의 vs 폐기).

Rule-B 4인:
- ϒ⋆ analytic-marg 식 closed form 검증.
- emcee backend 체크포인팅, np.random.seed 위치.
- dynesty rstate, prior_transform 단조성.
- compressed CMB chi² 키 사용 (재계산 금지).
- chi² -inf 가드.

리뷰 통과 전 production run 시작 금지, 논문 반영 금지.

## 종합 판정

설계는 falsifiable + 정직 + 재발방지 반영. 단, **F2 통과 확률은 약 30–50%** 로 예상 (L328 추세 외삽).
F4 통과 확률은 더 낮음 (15–35%). L336 의 가장 가능한 결과는 "SQT 후보가 부분 채널에서만 살아있다" 의 정직 보고. 이는 *이론 폐기* 가 아니라 *살아있는 도메인의 명시화* 로 정직 기록.
