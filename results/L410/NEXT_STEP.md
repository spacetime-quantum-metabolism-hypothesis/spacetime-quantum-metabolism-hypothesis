# L410 — Next Step Design (8인팀)

목표: paper §6.1 row 8 RECOVERY 가속. single-source dominance 59.7% → 가능한 최저값.
산출 평가: dominance 지표 < 30% 달성 시 RECOVERY → CLOSED (조건부) 전환 후보.

---

## (i) 13-cluster archive pool — published value 가용성 검토

### 기준
- 모든 후보는 *published* σ_cluster anchor (또는 동등 σ₀(ρ_env) 측정) + 명시적 systematic budget 보유.
- σ₀ 추출 channel: weak-lensing mass profile (NFW) 또는 X-ray hydrostatic 환경밀도 vs σ_v dispersion.

### Tier-1 (즉시 사용 가능, weak-lensing)
| Cluster | Source | Method | Note |
|---------|--------|--------|------|
| A1689 | Limousin et al. 2007 | strong+weak | 현재 anchor (baseline) |
| A1703 | Oguri et al. 2012, Umetsu+ 2016 | strong+weak | LoCuSS |
| A2218 | Smith et al. 2005 | weak | LoCuSS |
| MACS J1149 | Umetsu+ 2016 | weak (CLASH) | high-z |
| MACS J0717 | Limousin+ 2016 | weak | merging — ★ heterogeneity flag |
| RXJ1347 | Bradač+ 2008 | weak | CLASH |
| A2261 | Coe+ 2012 | weak | CLASH |
| MS2137 | Donnarumma+ 2009 | strong+weak | — |

### Tier-2 (X-ray hydrostatic, systematics 분리 fit 필요)
| Cluster | Source | Method | Note |
|---------|--------|--------|------|
| Coma | The+ 1986, X-ray Reiprich+ 2002 | X-ray | 현재 anchor |
| Perseus | Simionescu+ 2011 | X-ray | 현재 anchor |
| A1795 | Vikhlinin+ 2006 | X-ray | — |
| A2029 | Walker+ 2012 | X-ray | — |
| A478 | Sun+ 2003 | X-ray | — |

### Tier-3 (PSZ2 SZ-selected, random-mass dynamic range 보강)
| Cluster | Source | Method | Note |
|---------|--------|--------|------|
| PSZ2 G091 | Planck collab. 2015 | SZ + WL follow-up | random selection |
| PSZ2 G144 | Planck collab. 2015 | SZ | — |

### 핵심 건전성 체크
- weak-lensing sub-pool (Tier-1, A1689 포함 8 cluster) → A2 systematics 공격 직접 방어
- X-ray sub-pool (Tier-2, 5 cluster) → 별도 fit, cross-method consistency 검증
- PSZ2 (Tier-3, 2+ cluster) → A3 selection bias 공격 방어 (random-mass)

---

## (ii) Dominance ≥90% 해소 forecast

### Forecast 가정 (sample-size scaling)
- single-source dominance proxy: variance share s_i = σ_i^{-2} / Σ σ_j^{-2}
- 동질 systematics 가정 시: max s_i ≈ 1/N (대략).
- 이질 systematics 가정 시: max s_i ≈ w_i / Σ w_j 로 cluster-별 weight 의존.

### 시나리오
| Pool 크기 N | 가정 | max dominance forecast |
|------------|------|----------------------|
| 3 (현재) | Mixed | 59.7% (실측) |
| 5 | Tier-1+1 보강 (8→5 sub-select) | ~30–40% |
| 8 | Tier-1 full (homogeneous WL) | ~15–25% |
| 13 | Tier-1+2+3 | ~10–18% |

### Threshold 사전 설정 (8인 합의)
- < 30% 도달 시: RECOVERY → CLOSED (조건부) 후보. 단 A2 systematics 분리 fit 필수 통과.
- 30–50%: RECOVERY 진행중 유지.
- ≥ 50%: dominance metric 정의 다중 보고 + 정직 ACK.

### 정량 검증 채널 (Phase 4인 실행 단계)
- 정의 1 (variance share): max σ_i^{-2}/Σ σ_j^{-2}
- 정의 2 (χ²-leverage): Cook's distance 변종, 한 cluster 제거 시 Δχ² / total χ²
- 정의 3 (LOO Δθ): 한 cluster 제거 시 best-fit σ₀(env) 회귀 계수 변화율

3 정의가 모두 < 30% 일 때 강한 회복.

---

## (iii) 정량 시뮬레이션 spec

`simulations/L410/run.py` 에서 수행:

1. 입력: cluster pool (3, 5, 8, 13 단계) — published 값 부재시 *plausible mock* (정직 명시)
2. multi-cluster joint fit: σ₀(env) 회귀 (단조 / three-regime / non-monotonic generic)
3. dominance 3 정의 동시 산출
4. LOO leave-one-out + leave-two-out
5. mock injection (LCDM mock 200) 하의 FDR 곡선 (N-scaling)
6. AICc 비교 (단조 vs three-regime) — 파라미터 패널티 명시 [CLAUDE.md 공통원칙]

### 정직 한 줄
- 본 시뮬은 published 값 부재시 mock 으로 진행 → 결과는 *forecast* 이지 RECOVERY 확정 아님.
- 실제 published 값 수집은 별도 LXX (archive crawl) 위임.
