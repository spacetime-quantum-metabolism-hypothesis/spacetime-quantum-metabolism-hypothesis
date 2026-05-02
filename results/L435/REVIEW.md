# L435 — `paper/verification/` stand-alone scripts (REVIEW)

**Date:** 2026-05-01
**Scope:** paper §9.3 spec 5 script 실제 파일화 + expected_outputs +
README (en/ko) + requirements.

## 산출물

- `paper/verification/verify_lambda_origin.py` — CONSISTENCY_CHECK
  (L412 down-grade 명시, ratio = 1.000000)
- `paper/verification/verify_milgrom_a0.py` — PASS_STRONG, 0.71 sigma
- `paper/verification/verify_monotonic_rejection.py` — Delta chi^2 = 147.62
- `paper/verification/verify_mock_false_detection.py` — false-positive 100 %
  (seed=42, 0.07 s 측정)
- `paper/verification/verify_cosmic_shear.py` — xi_+ +2.29 %
- `paper/verification/expected_outputs/*.json` (5)
- `paper/verification/requirements.txt`
- `paper/verification/README.md` + `README.ko.md`

## 실행 검증 (macOS, Python 3.x)

| script | runtime | spec budget | 합 |
|--------|--------:|------------:|---|
| lambda_origin | 0.05 s | < 5 s | OK |
| milgrom_a0    | 0.05 s | < 5 s | OK |
| monotonic     | 0.20 s | < 5 s | OK |
| mock_false    | 0.07 s | < 60 s | OK |
| cosmic_shear  | 0.05 s | < 5 s | OK |

모두 stand-alone, deps = `numpy + scipy` 만.

## 정직 노트 (한 줄)

`verify_monotonic_rejection.py` 는 spec 의 anchor / err 그대로 사용하면
`Delta chi^2 = 147.6` (~12.1 sigma 1-DOF 근사) 가 나오며, 본문 §9.3
표의 `17 sigma` 와 차이가 있음 — README 와 expected_outputs JSON 의
`note` 필드에 둘 다 monotonic 을 5σ 이상으로 기각함을 명시 (cherry-pick
없이 정직 disclose).
