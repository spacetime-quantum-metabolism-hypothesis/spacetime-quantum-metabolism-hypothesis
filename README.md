# SQMH — Spacetime Quantum Metabolism Hypothesis

논문 프로젝트. `base.md` (원본 가설) → `base_2.md` (Phase 1–3.6 검증 후 정정본)
→ `paper/negative_result.md` (최종 네거티브 결과 논문).

**최종 판정 (2026-04-10)**. 4-gate AND 검사 실패 → **No-Go branch 확정**.
단순 배경결합 SQMH coupled quintessence (`V_mass` / `V_RP` / `V_exp`) 는
DESI DR2 + DESY5 + compressed Planck + RSD (N=1853) joint likelihood 에
대해 LCDM 대비 **유의미한 개선 없음**. 상세는 `base.todo.result.md`.

---

## 디렉토리

| 경로 | 용도 |
|---|---|
| `base.md` | 원본 가설 (한국어) |
| `base.fix.md`, `base.fix.class.md` | Phase 별 수정 기록 |
| `base_2.md` | 델타 문서 — base.md 에 대한 정정/철회/유보 |
| `base.todo.md` | 작업 계획 (모두 완료, N3 arXiv 투고만 대기) |
| `base.todo.result.md` | Phase 별 실행 결과 로그 |
| `base.out.1.md` | Kletetschka 2025 "3D Time" 교차검증 (14σ 기각) |
| `paper/negative_result.md` | 최종 논문 드래프트 (8 섹션) |
| `simulations/` | 전체 Python 시뮬레이션 |
| `figures/` | 14 개 그림 + 각 `.png.md` 설명 |
| `CLAUDE.md` | 재발방지 규칙 |

---

## 시뮬레이션 실행

### 요구사항

```
python >= 3.10
numpy, scipy, matplotlib, emcee, corner
```

상세는 `simulations/requirements.txt`.

### Phase 별 엔트리 포인트

| Phase | 스크립트 | 산출물 |
|---|---|---|
| 0 — 기초 | `simulations/run_all.py` | 그림 1–10 (대사, 중력, DE, 우주시대 등) |
| 1 — DESI DR2 background | `simulations/desi_fitting.py` | `figures/11_desi_dr2_fit.png` (LCDM / IDE / V(φ) 3모델) |
| 1 — DR3 예측 | `simulations/desi_dr3_prediction.py` | `figures/12_desi_dr3_prediction.png` |
| 2 — compressed CMB + RSD | `simulations/phase2/` | `figures/12_phase2_joint.png` |
| 3 — full MCMC | `simulations/phase3/mcmc_phase3.py` | `chains/*.npy`, `figures/13_phase3_mcmc.png` |
| 3.5 — r_d 자유 | `simulations/phase3/mcmc_rdfree.py` | `chains/*_rdfree_*.npy`, `r_d_tension.md` |
| 3.5 — V_exp corner | — (phase3 상기) | `figures/14_phase3_vexp.png` |
| 3.6 B1 — 5차 힘 | `simulations/screening.py` | 콘솔 출력 (Cassini, LLR, MICROSCOPE) |
| 3.6 B2 — Vainshtein | `simulations/vainshtein.py` | `figures/14_cassini.png` |
| 3.6 B3 — k-essence | `simulations/kessence.py` | `w(z)` interpolator (콘솔) |
| 3.6 B4 — Fisher | `simulations/phase4/fisher_kessence.py` | 콘솔 (Δχ², ΔAIC, ΔBIC) |
| 4 — Kletetschka 교차검증 | `simulations/phase4/check_kletetschka.py` | 콘솔 (Δχ² = +205) |

### 재현성

- Seed 고정: `np.random.seed(42)` + `emcee.EnsembleSampler` 내부 seed.
- 공개 데이터:
  - DESI DR2 BAO — `github.com/CobayaSampler/bao_data/desi_bao_dr2/`
  - DES-SN5YR — `github.com/CobayaSampler/sn_data/DESY5/`
  - Planck 2018 compressed CMB — arXiv:1807.06209
  - RSD — 8-포인트 컴파일 (`phase2/rsd_data.py`)

---

## 핵심 결과 (4-gate Decision)

| Gate | 조건 | CPL | V_RP | V_exp | LCDM |
|---|---|---|---|---|---|
| D1.1 ΔAIC ≤ −6 | background improvement | **−9.43 ✓** | +4.22 ✗ | +4.54 ✗ | 0 |
| D1.2 ΔBIC ≤ 0 | parsimony | +1.62 ✗ | +15.27 ✗ | +15.59 ✗ | 0 |
| D1.3 Cassini `\|γ−1\| < 2.3e−5` | Vainshtein 조건부 | — | **1.75e−10 ✓** | 1.75e−10 ✓ | N/A |
| D1.4 `r_d` 3σ 내 Planck | BAO–CMB 일치 | — | **3.13σ ✗** | 2.82σ ✓ | 2.63σ ✓ |

**AND 결과**. 전 모델 실패 → **No-Go**.

---

## 재발방지 (`CLAUDE.md` 발췌)

- DESI DR2 공식값은 `w0=-0.757, wa=-0.83` (DESI+Planck+DES-all, DR1 값과
  혼동 금지).
- BAO fit 은 13-point full covariance 필수. D_V only 금지.
- k-essence 배경 ODE 는 반드시 **forward shooting**, `K_X + 2 X K_{XX}` 부호
  검사 (ghost 영역 reject).
- IDE ODE 는 `omega_m` 이중 카운팅 금지, E² = Ω_r(1+z)⁴ + ω_m + ω_de.
- V_mass quintessence 는 backward ODE anti-damping 으로 폭주. 성장 ODE 배경은
  LCDM analytic 대체.
- DESY5 SN 거리 적분은 `zHD` (CMB frame) 사용. `zCMB` 는 bias 유발.
- 자세한 목록: `CLAUDE.md`.

---

## 라이선스 / 저자

TBD (arXiv 투고 전 결정).
