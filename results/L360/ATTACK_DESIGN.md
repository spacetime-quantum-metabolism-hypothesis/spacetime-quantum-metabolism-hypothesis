# L360 ATTACK DESIGN — Q_DMAP Cross-Dataset Tension (SQT σ_0)

## 목표
SQMH/SQT 의 핵심 파라미터 σ_0 (또는 Σ ≡ n0·μ 등 SQT amplitude proxy) 가
서로 다른 관측 채널 — **갤럭시 회전곡선 (SPARC)** vs **BAO+RSD (DESI DR2)** vs
**CMB compressed (Planck 2018)** — 에서 일관된 값으로 추정되는지 검증한다.
일관성 부재 = SQT σ_0 가 cross-scale universal 이 아니라는 falsification.

## 도구: Q_DMAP (Raveri & Doux 2021, PRD 104, 043504)
- 정의 (요약): tension metric `Q_DMAP = sqrt(2 [ -ln L_joint(θ̂_joint) + ln L_A(θ̂_A) + ln L_B(θ̂_B) ])`
  - 즉 두 데이터셋의 개별 MAP 적합도와 결합 MAP 적합도의 차이를 σ-환산.
- 임계: **Q_DMAP > 5 → 심각 tension (5σ 수준), >3 주의, <2 일관**.
- 장점: posterior Gaussianity 가정 불필요, prior-volume effect 면역
  (DKL 기반보다 robust). 비-Gaussian σ_0 posterior 에 적합.

## 데이터셋 (3채널)
- **A: SPARC** — 175 disk galaxies rotation curves (Lelli+ 2016).
  σ_0 / Σ 추출은 SQT-modified MOND-like force law `g(g_N)` 을 회전곡선에 fit.
- **B: DESI DR2 BAO+RSD** — 13 BAO points + RSD fσ8 set.
  σ_0 가 background w(z) / growth modification 에 들어가는 SQT 임베딩 사용
  (L33/L34 pipeline 재활용).
- **C: Planck 2018 compressed** — (R, l_A, ω_b) shift parameters.
  σ_0 가 sound horizon / late-ISW 로 들어감.

## 페어와이즈 비교
- pair (A,B): SPARC vs DESI    — **갤럭시 vs 우주론 거리·성장**
- pair (A,C): SPARC vs Planck  — **갤럭시 vs 초기우주**
- pair (B,C): DESI vs Planck   — **late vs early universe** (control: H0/S8 tension 와 별개로 σ_0 채널만)

## 분석 단계 (8인 자율, 사전 역할 미지정)
1. **σ_0 임베딩 정의 통일** — 세 채널에서 동일 SQT 변수 (예: A_SQT ≡ n0·μ·t_P²)
   가 서로 다른 식으로 들어가는지, 아니면 single scalar 인지 합의.
2. **각 채널 단독 MAP 추출** — `θ̂_A, θ̂_B, θ̂_C` (σ_0 + nuisance).
3. **페어와이즈 joint MAP** — `θ̂_{AB}, θ̂_{AC}, θ̂_{BC}`.
4. **Q_DMAP 계산** — 위 공식. negative-radicand 시 (joint 가 더 좋은 fit) Q=0 보고.
5. **삼중 joint** — `θ̂_{ABC}` 도 계산해 cumulative tension.
6. **부트스트랩 / profile likelihood** — non-Gaussian σ_0 일 때 MAP 안정성 점검.

## 합격 / 실패 기준 (사전 등록)
- **PASS**: 세 페어 모두 Q_DMAP < 2  → SQT σ_0 cross-scale universal claim 보존.
- **WATCH**: 한 페어라도 2 ≤ Q_DMAP < 5 → 추가 nuisance / scale-dep σ_0 검토.
- **FAIL (KILL)**: 한 페어라도 Q_DMAP > 5 → 단일 σ_0 claim falsified.
  σ_0 를 scale-dependent 로 일반화하거나 이론 재구성.

## 과적합 패널티
- 채널마다 nuisance 추가 시 AICc 패널티 명시.
- 핵심 이론 자유도는 σ_0 단 하나여야 한다 (universal claim 의 정의).

## 회피해야 할 함정 (CLAUDE.md 재발방지 적용)
- BAO 거리 단위 (Mpc 일관), DESI DR2 공식값 wa=-0.83 사용.
- numpy 2.x: `np.trapezoid` 직접 호출.
- BAO-only low-Om 결과를 joint 결론으로 끌어 쓰지 말 것 (L33 재발방지).
- Planck CMB compressed θ* 에 0.3% theory floor.
- `matplotlib.use('Agg')` 를 corner import 보다 먼저.
- emcee/dynesty 시드 고정 + Windows OpenMP=1.

## 산출물
- `results/L360/qdmap_pairwise.json` — 세 페어 + 삼중 Q_DMAP, MAP 값.
- `results/L360/qdmap_corner.png` — σ_0 marginal (3채널 + joint).
- `results/L360/profile_sigma0.png` — profile likelihood (3채널 비교).
