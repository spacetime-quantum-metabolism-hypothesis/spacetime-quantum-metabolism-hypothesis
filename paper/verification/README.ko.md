# SQT / SQMH — `paper/verification/` (한국어)

외부 reviewer 용 Quickstart. 논문 §9.3 spec 의 5개 stand-alone Python
script — 각 **< 5 초** (mock 만 < 1 분) 실행, 의존성은 `numpy`, `scipy`
뿐.

> 내부 냉혹 audit (R1–R8 보고서 + raw evidence) 는
> `paper/verification_audit/` 에 분리. 역할 차이는 논문 §9.7 참조.

---

## 빠른 실행

```bash
pip install -r requirements.txt
python verify_lambda_origin.py        # Lambda 기원 CONSISTENCY_CHECK
python verify_milgrom_a0.py           # MOND a_0 PASS_STRONG
python verify_monotonic_rejection.py  # regime-gap V-shape vs 단조
python verify_mock_false_detection.py # 정직한 false-positive caveat
python verify_cosmic_shear.py         # Euclid / LSST 구조적 falsifier
```

기준 출력은 `expected_outputs/*.json`. 새 환경에서 재실행 시 명시된
허용오차 내에서 재현되어야 함 (확률적 부분은 seed=42 고정).

---

## 스크립트 목록

| # | 스크립트 | 판정 / 역할 | 실행시간 |
|---|---------|------------|--------|
| 1 | `verify_lambda_origin.py` | `rho_q / rho_Lambda = 1.000000` — **CONSISTENCY_CHECK** (L412 에서 PASS_STRONG → 강등; `rho_Lambda_obs` 에 대한 circularity, §5.2) | < 1 s |
| 2 | `verify_milgrom_a0.py` | `a_0 = c * H_0 / (2 * pi)` — **PASS_STRONG**, ~0.7 sigma | < 1 s |
| 3 | `verify_monotonic_rejection.py` | 3-anchor V-shape vs 단조 — `Delta chi^2 ~ 148` (regime-gap 한정, SPARC-internal 아님) | < 2 s |
| 4 | `verify_mock_false_detection.py` | LCDM mock x 200 → 3-regime false-detection rate = 100 % — SPARC `Delta AICc` 이점에 대한 **정직한 caveat** | < 1 min |
| 5 | `verify_cosmic_shear.py` | `+1.14 %` S_8 → `+2.29 %` `xi_+(10')` — Euclid / LSST **구조적 falsifier** | < 1 s |

---

## 정직 한 줄 노트

- **Script 1** 은 a priori 예측이 **아니다**. `n_inf` 가
  `rho_Lambda_obs` 로부터 유도되므로 `ratio = 1` 은 항등식.
- **Script 3** 의 sigma 는 `Delta chi^2` 기반 1-DOF 근사. 논문 본문의
  `~17 sigma` 는 다른 anchor / 오차 가정. 둘 다 단조 모델을 5σ 이상
  기각.
- **Script 4** 는 **caveat 재현**이지 승리 결과가 아니다. null 데이터에
  100 % false-positive 가 나온다는 것은 SPARC `Delta AICc` 이점을 이
  baseline 위에서 해석해야 한다는 의미.
- **Script 5** 가 가장 깨끗한 **falsifier**. Euclid / LSST 가
  `xi_+(10')` 를 LCDM 와 < 2 % 수준에서 일치시켜 측정하면 현재
  파라미터화의 SQMH 는 기각.

---

## 재현성 체크리스트

- [x] Python 3.10+ (3.11 / 3.13 검증), numpy >= 2, scipy >= 1.10
- [x] GPU / MPI / MCMC 불필요
- [x] script 4 에 `rng = np.random.default_rng(42)` 고정
- [ ] CI: `.github/workflows/verify.yml` (TODO)
