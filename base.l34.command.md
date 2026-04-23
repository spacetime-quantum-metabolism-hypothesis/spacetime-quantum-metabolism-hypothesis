# base.l34.command.md — L34 Command
# 목표 & 기준 — 순수 사전 설명

> 작성: 2026-04-19. L33 Q92/Q93 결과의 결합 데이터 검증.
> **수식 없음. 방향만 제시. 이론 형태는 L33 결과 파일에서 직접 로드.**

---

## ■ 왜 이 실험을 하는가?

L33에서 확인된 Q92 챔피언(tanh-weight, ΔAICc=-4.715)과 Q93 챔피언(sigmoid k=75, ΔAICc=-6.617)은
**DESI DR2 BAO 13pt 단독**으로 피팅한 결과다.

문제: Q92 챔피언의 Om≈0.115, Q93의 Om≈0.068 — ΛCDM 제약(Om≈0.3)에서 크게 벗어남.
→ CMB + SN 결합 시 이 low-Om 해가 여전히 ΛCDM보다 우수한가?
→ SQT 모델의 실제 예측력을 평가하려면 joint 분석 필수.

---

## ■ L34 팀 구성

- **인원: 8명**
- **역할 사전 지정 없음**
- 팀원들이 자율 분담으로 joint 파이프라인 구축, 검증, 분석 수행
- 코드리뷰는 4인팀 자율 분담

---

## ■ 사용할 모델

L33 결과 파일에서 직접 로드 (수식 재정의 금지):

- `simulations/l33/l33_q92_tanh_champion.json` — Q92 챔피언 (tanh-weight)
- `simulations/l33/l33_q92_exp_champion.json` — Q92 exp-weight
- `simulations/l33/l33_q93_sig_super_champion.json` — Q93 챔피언 (sigmoid k=75)
- `simulations/l33/l33_test.py` — 모델 함수(compute_tv 등) 직접 import

모델 구조는 `l33_test.py`의 함수를 import해서 사용. 독립 재구현 금지 (K92 방지).

---

## ■ 사용할 데이터셋

### 1. DESI DR2 BAO (기존)
```python
from simulations.desi_data import DESI_DR2, DESI_DR2_COV_INV
```
- 13개 측정 포인트, 13×13 full 공분산
- r_s = 147.09 Mpc 고정 (Planck 2018)

### 2. Planck 2018 압축 CMB 사전확률
```python
from simulations.phase2.compressed_cmb import chi2_compressed_cmb
```
- theta_star, omega_b h², omega_c h² 세 파라미터 제약
- omega_b h² = 0.02237 (Planck 2018 TT,TE,EE+lowE)
- omega_c h² = Om * h² - omega_b h² 로 계산 (flat universe 가정)
- k=2 유지를 위해 omega_b 고정 (피팅 파라미터 아님)

### 3. SN 데이터
우선순위 순서:
1. **Pantheon+**: `simulations/phase2/data/` 또는 CobayaSampler `sn_data/pantheonplus/` 확인
2. **DESY5** (fallback): `simulations/phase2/sn_likelihood.py`의 `DESY5SN` 클래스

SN chi2는 절대등급 M에 대해 해석적 marginalization 사용 (Conley et al. 2011).

---

## ■ 자유 파라미터 (k=2 고정)

| 파라미터 | 탐색 범위 | 비고 |
|----------|-----------|------|
| Ω_m | [0.05, 0.50] | |
| H₀ | [55, 80] km/s/Mpc | |

**이론 구조 파라미터 (k_sig, z0, c, amp 등)**: L33 챔피언 값으로 고정. 피팅 대상 아님.
→ AICc 계산 시 k=2 유지.

---

## ■ Joint χ² 계산

```
chi2_joint = chi2_BAO + chi2_CMB + chi2_SN
```

각 항목 독립 계산 후 합산. 3개 데이터셋 동시 최적화.

---

## ■ ΛCDM 기준선 (joint)

L33의 BAO-only 기준선(chi2=10.192, AICc=15.392)과 별도로,
**joint 기준선을 이 실험에서 새로 계산**:

- ΛCDM E(z) = sqrt(Ω_r(1+z)^4 + Ω_m(1+z)^3 + Ω_Λ) (flat)
- joint chi2_LCDM = chi2_BAO_LCDM + chi2_CMB_LCDM + chi2_SN_LCDM
- k=2 (Ω_m, H₀ free)
- multi-start Nelder-Mead + differential_evolution

---

## ■ AICc 계산

n = (BAO 13) + (CMB 3) + (SN N_SN) 총 데이터 포인트
k = 2

```
AICc = chi2 + 2k + 2k(k+1)/(n-k-1)
     ≈ chi2 + 4  (n >> k 이므로)
```

ΔAICc = AICc_SQT - AICc_LCDM

---

## ■ 판정 등급 (joint 기준)

| 등급 | 조건 | 의미 |
|------|------|------|
| Q94 JOINT PASS | ΔAICc_joint < -4 AND wa < -0.5 | joint 분석에서도 Q92 유지 |
| Q95 JOINT STRONG | ΔAICc_joint < -6 AND wa < -0.5 | joint에서 Q93급 |
| J90 DEGRADED | BAO-only 보다 ΔAICc 악화 | CMB/SN 제약으로 모델 손상 |
| J91 KILL | ΔAICc_joint ≥ 0 | joint에서 ΛCDM에 열세 |
| K91 KILL | 추가 상수가 피팅값 | 공정성 위반 |

---

## ■ 출력 요구사항

### 필수 보고 항목

1. **joint ΛCDM 기준선**: chi2_joint, AICc_joint, 최적 Ω_m, H₀
2. **각 SQT 모델별**:
   - joint 최적 Ω_m, H₀
   - chi2_BAO, chi2_CMB, chi2_SN 개별값
   - chi2_joint, AICc_joint, ΔAICc_joint
   - CPL w₀, wa (z∈[0.01,2] 구간 최소자승)
3. **BAO-only vs joint 비교표**: 동일 모델의 ΔAICc 변화량
4. **Om 이동 분석**: BAO-only 최적 Om vs joint 최적 Om 변화량

### 파일
- `/simulations/l34/l34_test.py` — 실행 스크립트
- `/simulations/l34/l34_results.json` — 전체 결과
- `base.l34.result.md` — 판정표 + 분석

---

## ■ 코드 필수 조건

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from simulations.desi_data import DESI_DR2, DESI_DR2_COV_INV
from simulations.phase2.compressed_cmb import chi2_compressed_cmb
```

- 병렬 실행: `multiprocessing.get_context('spawn').Pool(9)`
- `OMP_NUM_THREADS=1, MKL_NUM_THREADS=1, OPENBLAS_NUM_THREADS=1`
- L33 모델 함수: `l33_test.py`에서 직접 import (재구현 금지)
- 적분: N_GRID=4000, cumulative_trapezoid (L33 버그 재발 방지)
- SN chi2: 절대등급 marginalization 적용 (H0 편향 제거)
- 항상 `python3` 사용 (macOS에서 `python` 명령 없을 수 있음)

---

## ■ L30~L33 재발방지 (이 실험에 직접 적용)

| 실수 | L34 대응책 |
|------|-----------|
| L33: 800pt 적분 → chi2 ~0.75 과소평가 | N_GRID=4000, cumulative_trapezoid 강제 |
| L33: ratio 클리핑 누락 → 수치 폭발 | clip(psi0/psi_z, 1.0, 200.0) 필수 |
| L33: 새 함수 검증 없이 실행 | 알려진 파라미터로 단일 포인트 chi2 확인 후 실행 |
| L31~L32: Om 범위 [0.15,0.45] → low-Om 해 놓침 | joint 피팅 Om ∈ [0.05, 0.50] |
| L33: global amp 구조 버그 | rho_DE = OL0*(1+amp*g) 형태만 사용 |
| L32: wa>0 K93 대량 KILL | L33 챔피언 고정값 사용이므로 해당 없음 |
| 공통: BAO-only Om을 우주론적 Om으로 혼동 | joint Om 명시, BAO-only Om과 구분 |

---

## ■ 불변 제약 (변경 금지)

- k=2 제약 (Ω_m, H₀만 free)
- full 13×13 BAO 공분산 사용
- r_s = 147.09 Mpc 고정
- L33 모델 구조 파라미터 고정 (피팅 시 변경 금지)
- joint AICc = chi2_joint + 2k + 2k(k+1)/(n-k-1)
- ΔAICc = SQT - ΛCDM (같은 데이터셋 기준)
- omega_b = 0.02237 고정 (피팅 파라미터 아님 → k=2 유지)

---

*작성: 2026-04-19. L33 Q92/Q93 챔피언의 joint 데이터 검증. 8인 팀, 역할 지정 없음. L30~L33 재발방지 포함.*
