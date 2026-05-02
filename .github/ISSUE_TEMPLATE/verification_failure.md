---
name: Verification failure
about: 시뮬레이션/계산 output이 보고된 값과 다를 때 사용
title: "[VERIFY] "
labels: verification, reproducibility
assignees: ''
---

## 검증 대상
- LXX 세션 / 후보 코드 (예: L46 Q93, L34 joint, L33 standalone scan):
- 원본 결과 파일 경로:
- 원본 commit hash:

## 보고된 값 (expected)
| 지표 | 값 | 출처 (파일:라인 또는 docs 경로) |
|------|----|-----|
| chi2 |    |     |
| dAICc |    |     |
| w0, wa |   |     |
| 기타  |   |     |

## 재현 결과 (observed)
| 지표 | 값 | 차이 (Δ) |
|------|----|---------|
| chi2 |    |         |
| dAICc |    |         |
| w0, wa |   |         |

## 재현 환경
- OS / Python / 패키지 버전:
- 실행 명령:
  ```
  python3 ...
  ```
- 입력 데이터 출처/체크섬 (BAO, SN, CMB, RSD):
- 시드 / N_GRID / 적분기 옵션:

## 의심 원인 후보
- [ ] 적분 그리드 / 누적합 방식 (참고: L33 N_GRID=4000, cumulative_trapezoid)
- [ ] 단위 변환 (c, H0, Mpc)
- [ ] 데이터 파일 버전 차이 (DESI DR1 vs DR2, DESY5 zHD vs zCMB)
- [ ] 부호 규약 (xi_q, beta, nu)
- [ ] backend / 부동소수 정밀도
- [ ] 기타:

## 영향
- 결과 무효화 범위:
- base.fix.md 기록 필요 여부:

## 첨부
- 재현 로그 (전체):
- 비교 플롯 (가능하면):
