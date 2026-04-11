# base.l7.result.md — L7 Phase-7 종합 결과

> 작성일: 2026-04-11. Rule-A/B 검토 완료.
> 논문 제출 전 마지막 이론/수치 검증 단계.

---

## L7-0 인프라 확인

- classy 3.3.4 설치 완료 (pip3). LCDM TT/EE 계산 OK.
- L7 디렉터리 구조: simulations/l7/{cmb,channels,s8h0}/
- Kill criteria K21-K25, Keep criteria Q18-Q22 확정 (refs/l7_kill_criteria.md)

---

## L7-C CMB 정식 검증 (classy)

**방법**: TT 파워 스펙트럼 우주 분산 chi² = Σ_l (2l+1)/2 · (C_l^model/C_l^LCDM - 1)²

**결과** (BAO-최적화 h 사용):

| 모델 | h_BAO | theta_s_100_model | theta_s_100_LCDM | chi2_cv | K23 상태 |
|------|-------|-------------------|-------------------|---------|---------|
| C11D | 0.6776 | 1.048 | 1.040 | 53 | FAIL at BAO-h |
| A12 | 0.6770 | ~1.047 | 1.040 | ~40 | FAIL at BAO-h |
| C28 | 0.6789 | ~1.049 | 1.040 | ~60 | FAIL at BAO-h |

**중요한 방법론적 한계**:
- BAO-최적화 h (0.677)는 CMB-최적화 h (0.674)와 다름.
- 각 DE 모델에 대해 h를 CMB theta_s에 맞게 재최적화해야 함.
- 올바른 K23 판정: 각 후보에 대해 (Om, h, ...) 전체 CMB MCMC 필요.
- L6 compressed CMB chi² (chi2_joint 내 'cmb' 키) 기준:
  - C11D: Δchi²_CMB = -6.33 (LCDM 대비 개선) → K19 provisional PASS
  - K23 formal verdict: 전체 MCMC 재최적화 후 확정. **현재 "provisional".**

**결론**: CMB 채널에서 단순 BAO-opt 파라미터로 K23 판정 불가. L6 compressed CMB가 1차 지표. full MCMC는 PRD Letter 격상 전 필요.

---

## L7-X1 GW 중력파 제약 (C11D disformal)

**방법**: GW170817 c_T/c 제약 → disformal B_0 상한 계산
**결과** (simulations/l7/channels/gw_constraint.json):

| 제약 소스 | B_0 상한 (M_P⁻²) | C11D 킬 여부 |
|----------|-----------------|------------|
| GW170817 (|c_T/c - 1| < 5×10⁻¹⁶) | 3.67×10⁹¹ | NO (완전 비제한) |
| Einstein Telescope (500× 개선) | 7.34×10⁸⁸ | NO (여전히 비제한) |

**물리적 해석**:
- Pure disformal (A'=0) 에서 배경 γ=1 exact (Zumalacárregui-Koivisto-Bellini 2013).
- A'=0 배경은 B_0 독립. GW 제약은 배경 아닌 섭동 레벨만 제한.
- B_0 상한 3.67×10⁹¹은 플랑크 자연 스케일보다 ~90 자릿수 큼 → 완전 비제한.

**K25 판정**: 미발동. C11D background unaffected.
**Q22 기여**: GW 채널은 섭동 레벨 추가 제약. 단독으로 Q22 불충분 (주 채널은 SKAO).

---

## L7-X2 ISW 예측 (CMB-S4)

**방법**: classy CPL 근사, l=2-19 ISW 밴드 우주분산 SNR 계산
**결과** (simulations/l7/channels/isw_forecast.json):

| 비교 | ISW RMS 분율차 | CMB-S4 SNR | 구분 가능? |
|------|--------------|-----------|----------|
| C11D vs LCDM | 2.73% | **0.287** | **NO** |

**물리적 해석**:
- ISW는 l < 20 저다극자에서 우주분산 제한을 받음.
- C11D w(z)의 LCDM 대비 차이가 작고, 우주분산이 지배적.
- CMB-S4 (및 Simons Observatory) 로도 ISW 채널에서 SQMH 구분 불가.

**Q22 판정**: ISW 채널 → NO.
**논문 §8 honest limitation**: "ISW cross-correlation at CMB-S4 is predicted to be indistinguishable from LCDM (SNR = 0.29 < 1)."

---

## L7-X3 SKAO 21cm BAO 예측 (핵심 Q22)

**방법**: Bacon+2020 SKAO MID Band 1+2, Fisher 예측, 13 적색이동 구간 z=0.35-2.10
**결과** (simulations/l7/channels/skao_forecast.json):

| 모델 | SKAO SNR (총) | 2σ 구분? | Q22 달성? |
|------|-------------|--------|---------|
| C11D | **12.20** | YES | **YES** |
| A12 | **12.41** | YES | **YES** |
| C28 | **14.10** | YES | **YES** |

**구간별 신호**: z=0.4-1.0에서 D_A 방향 3.0-3.9σ, H(z) 방향 2.3-3.3σ.

**Q22 판정**: **PASS** — 우주론 외 새 채널 ≥1개 달성.
- "SKAO Phase-1 MID 21cm BAO will distinguish all SQMH candidates from LCDM at >12σ by 2027-2030."
- DR3 falsifier (2.9-3.9σ Fisher) + SKAO Q22 (12-14σ) → 이중 falsifiability 확보.

---

## L7-G2 S8/H0 구조적 한계 재확인

**결과** (simulations/l7/s8h0/s8h0_exploration.json):

### Part 1: S8 tension (beta_D 탐색)

| beta_D | G_eff/G | delta_S8 | S8_model | K15 (< 0.84) |
|--------|---------|----------|----------|--------------|
| 0.001 | 1.000002 | +0.000002 | 0.8320 | PASS |
| 0.05 | 1.005 | +0.005 | 0.8362 | PASS |
| 0.107 | 1.023 | +0.023 | 0.8506 | FAIL |
| 0.15 | 1.045 | +0.045 | 0.8694 | FAIL |

**핵심 결론**: dark-only 결합은 S8을 증가시킴 (DES-Y3/KiDS 방향과 반대).
S8 개선을 위해서는 beta_D < 0 필요 → SQMH 부호 위반. **Q15 구조적 실패 확정.**

### Part 2: H0 tension (C11D thawing)

| 지표 | 값 |
|-----|---|
| h_SQMH 사후 | 0.6776 |
| h_SH0ES | 0.732 |
| H0 gap (SQMH vs SH0ES) | 0.0544 (7.4%) |
| LCDM gap (LCDM vs SH0ES) | 0.063 (8.6%) |
| SQMH의 LCDM 대비 개선 | 13.7% (불충분) |

C11D: lam=0.8872 < sqrt(3)=1.732 → thawing (tracker 아님) → z>2 조기 DE 불가.
EDE 시나리오로 H0 해결 불가. **H0 tension 구조적 미해결 확정.**

**논문 §8**: 두 한계 모두 솔직히 기재 필수. 심사자 선제 대응.

---

## L7-T 이론 Phase-2: UV completion + 언어 체계

### UV Completion 8인 검토 결과 (refs/l7_uv_completion.md)

| QG 프레임워크 | 연결 상태 | 핵심 장벽 |
|------------|---------|---------|
| LQC | 형태적 유사만 | 현재 우주 소멸항 생성 메커니즘 없음 |
| GFT (Oriti 2017) | 부분 구조 유사 | ρ_m 결합 소멸항 미개발 |
| CDT (Ambjorn+2005) | n̄(a) ~ a⁻³ 정합 | coarse-graining 연결 미완 |
| Causal Sets | σ 개념 유사 | Λ 예측 오차 너무 큼 |

**K24 판정**: 미발동 (수학적 불가능 판정 아님 — 미개발 상태).
**Q21 판정**: 미달 (UV completion 완성 아님).

**확정 언어**: "QG-motivated phenomenology" — LQC/GFT/CDT와 형태적 연결 기술 가능.

### 정직한 현상론 언어 체계 (refs/l7_honest_phenomenology.md)

| 상황 | 허용 언어 | 금지 언어 |
|-----|---------|---------|
| 증거 서술 | "consistent with", "achieves strong evidence" | "confirms", "proves" |
| 이론 연결 | "motivated by", "QG-motivated" | "derived from", "predicted by" |
| 파라미터 | "zero additional parameters" | "parameter-free theory" |
| DR3 예측 | "DR3 sensitivity: 2.9-3.9σ" | "DR3 will confirm" |
| A12 서술 | "erf proxy for SQMH canonical drift" | "SQMH derived template" |
| C28 서술 | "Maggiore-Mancarella compatible" | "SQMH model" |

---

## L7 종합 Kill/Keep 판정표

### Kill criteria

| 기준 | 상태 | 세부 |
|-----|------|-----|
| K17 (Δ ln Z ≥ 2.5) | **전원 PASS** | A12 +10.769, C28 +8.633, C11D +8.771 |
| K19 (CMB Δchi² ≤ LCDM+6) | **provisional PASS** | C11D Δchi²=-6.33 (개선) |
| K21 (JCAP reject) | 미발동 | 미제출 |
| K22 (DR3 wa > 0) | 대기 중 | DR3 미공개 |
| K23 (classy CMB formal) | **pending** | BAO-opt h로 불완전. full MCMC 필요 |
| K24 (UV completion 불가) | **미발동** | 형태적 유사 가능, 수학적 불가 판정 안 함 |
| K25 (Euclid mu_eff) | 미발동 | Euclid 미공개 |

### Keep criteria

| 기준 | 상태 | 세부 |
|-----|------|-----|
| Q15 (S8 개선 ≥ 0.01) | **전원 FAIL** | 구조적 (beta_D 방향 반대) |
| Q17 (amplitude-locking 부분) | 부분 달성 | Exact coefficient 미유도 |
| Q18 (hi_class 검증) | 대기 | L7-C 미완결 |
| Q19 (DR3 준비) | **PASS** | 스크립트 완료 |
| Q20 (paper §8 정직) | **PASS** | 한계 목록 완성 |
| Q21 (UV completion) | **FAIL** | 형태적 유사만 가능 |
| Q22 (새 채널 ≥ 1) | **PASS** | SKAO SNR=12.20-14.10 |

---

## L7 Phase-7 최종 결론

**논문 현재 위치**:
"A zero-parameter dark energy template motivated by discrete spacetime metabolism,
achieving strong Bayesian evidence on DESI DR2 (Δ ln Z = +10.77, A12),
with concrete falsifiable predictions (SKAO >12σ by 2030, DR3 2.9-3.9σ sensitivity)
and honest acknowledged limitations (S8/H0 structurally unresolved, UV completion open)."

**제출 타깃**: **JCAP** — 8인 합의 (refs/l7_honest_phenomenology.md, 경로 B 확정).

**PRD Letter 격상 조건** (현재 미달):
- DR3 확인 (wa < 0 유지 ≥ 3σ) OR
- Amplitude-locking 완전 유도 (K20 통과)

**SKAO Q22**: SNR 12.20 (C11D), 12.41 (A12), 14.10 (C28) — 우주론 외 새 검증 채널 확보.

**DR3 대응**: simulations/l6/dr3/run_dr3.sh 준비 완료. DR3 공개 즉시 실행.

---

## L7 산출물 목록

| 파일 | 내용 | 상태 |
|-----|------|------|
| simulations/l7/cmb/cmb_chi2_L7.json | classy K23 시도 (methodology 한계 문서화) | 완료 |
| simulations/l7/channels/gw_constraint.json | GW170817 B_0 제약 | 완료 |
| simulations/l7/channels/isw_forecast.json | CMB-S4 ISW SNR=0.287 | 완료 |
| simulations/l7/channels/skao_forecast.json | SKAO SNR=12-14σ Q22 PASS | 완료 |
| simulations/l7/s8h0/s8h0_exploration.json | S8/H0 구조적 한계 | 완료 |
| refs/l7_uv_completion.md | UV completion 8인 검토 | 완료 |
| refs/l7_honest_phenomenology.md | 언어 체계 + falsifiability | 완료 |
| refs/l7_kill_criteria.md | K21-K25, Q18-Q22 정의 | 완료 |
