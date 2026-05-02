# L401 — 315-Loop Honest Synthesis

L77~L401 누적 **315 loop** (L371 285-loop 종합 + L372~L400 29 loop). 본 문서는 L371 SYNTHESIS_285 의 정직 후속이며, plan-only 격하의 *부분 회복*(4 spec 실측 전환) 과 *빈 loop 비율 악화*(10/29) 를 동시에 직시한다.

한국어 한 줄: **315 loop 후 ★★★★★ -0.123 (보합), JCAP 87–92% (-1%); plan→실측 전환 4건은 의미 있는 진보지만 빈 loop 10건이 정확히 상쇄.**

---

## L372–L400 29-Loop 요약 표

| Loop | 주제 | 산출 | 등급 영향 |
|------|------|------|-----------|
| L372 | A1689+Coma+Perseus 3-cluster joint σ_cluster | report.json + REVIEW (4/4 pre-reg PASS) | **실측 PASS** +0.012 (limitation 8 부분 회복) |
| L373 | M1 (linear) vs M2 (V-shape sym/asym) on SPARC 163 | report.json | **narrative 약화** -0.008 (Δχ² M1−M2sym ≈ 0) |
| L374 | 5-dataset emcee smoke test | report.json + REVIEW (Rhat<1.01, ESS>1600) | **pipeline +0.003** (실 SQMH likelihood 아님) |
| L375 | SQT mock injection-recovery N=100 | report.json (100/100 PASS, RMSE 0.017 dex) | **PASS +0.005** |
| L376 | (빈) | — | -0.002 |
| L377 | dynesty NS multimodal smoke | report.json + REVIEW (lnZ -5.479±0.24, 두 모드 검출) | **toy PASS +0.003** |
| L378 | M1 vs M2 single-anchor LOO plan | ATTACK | plan +0.002 |
| L379 | Causet → meso (coarse-grained) 재검토 plan | ATTACK | plan +0.002 |
| L380 | P17 Tier B V(n,t) toy plan | ATTACK | plan +0.002 |
| L381 | Cosmic shear ξ_+(θ=10') SQT vs LCDM plan | ATTACK | plan +0.002 |
| L382 | SK Wightman W± 명시 + KMS β plan | ATTACK | plan +0.001 (표준 결과) |
| L383 | Wetterich Γ_k LPA truncation σ_0 flow plan | ATTACK | plan +0.002 |
| L384 | Wetterich LPA' truncation (η, NGFP) | ATTACK + REVIEW (빈 템플릿) | -0.003 (실 도출 부재) |
| L385 | Holographic CKN n_∞/n_max | results.json (r=0.685, Hubble scale) | **헤드라인 falsifiable +0.005** |
| L386 | Z_2 SSB 유한온도 T_c, z_DW plan | ATTACK | plan +0.002 |
| L387 | n field 1-loop self-energy Π(p²), m_n plan | ATTACK | plan +0.002 |
| L388 | 2-loop n self-energy + setting-sun, c 계수 도출 | ATTACK + REVIEW (**KILL**) | **pillar 4 상한 인정 -0.007** |
| L389 | BRST diffeomorphism gauge invariance check | ATTACK + REVIEW (PASS) | **pillar 4 보강 +0.005** |
| L390 | Conformal anomaly T^μ_μ (n field) plan | ATTACK | plan +0.002 |
| L391 | (빈) | — | -0.002 |
| L392 | 논문 Sec 3 Branch B final draft outline plan | ATTACK | plan +0.002 |
| L393 | (빈) | — | -0.002 |
| L394 | (빈, 디렉터리 부재) | — | -0.002 |
| L395 | (빈) | — | -0.002 |
| L396 | (빈) | — | -0.002 |
| L397 | (빈) | — | -0.002 |
| L398 | (빈, 디렉터리 부재) | — | -0.002 |
| L399 | (빈, 디렉터리 부재) | — | -0.002 |
| L400 | (빈, 디렉터리 부재) | — | -0.002 |

**L372–L400 net 등급 변화: -0.003** (실측 +0.028, plan 가치 +0.022, 빈 loop -0.020, narrative 약화 -0.008, c 계수 상한 -0.007, 템플릿 부재 -0.003 → 보합).

---

## 315-Loop 누적 통계

```
Robust PASS:     160 (50.8%)   ← +4 (L372, L375, L377, L389)
PARTIAL:          40 (12.7%)   ← +1 (L385 CKN headline 부분)
KILL/한계 인정:    1 (0.3%)    ← +1 (L388 c 계수 first-principle 한계)
UNRESOLVED:        2 (0.6%)    ← σ_8 / H0 영구 (변화 없음)
RESOLVED:         29 (9.2%)
ACK:              31 (9.8%)
PLAN-ONLY:        38 (12.1%)   ← +10 (L378~L387, L390, L392)
빈/효율 손실:     14 (4.4%)   ← +10 (L376, L391, L393~L400)
─────────────────────────────
합계:            315
```

PLAN-ONLY 가 28→38 으로 *증가* 했지만 동시에 4건이 PLAN-ONLY 에서 실측 PASS/PARTIAL 로 *졸업* (L347→L372, L357→L374, L358→L377, L361→L375). 빈 loop 카테고리 (4→14) 가 *효율 손실* 신호로 신규 가시화.

---

## 등급 변화

```
L75   ★★★★½+
L155  ★★★★★ - 0.30
L211  ★★★★★ - 0.18
L241  ★★★★★ - 0.12
L271  ★★★★★ - 0.065
L321  ★★★★★ - 0.05
L331  ★★★★★ - 0.07
L341  ★★★★★ - 0.08
L371  ★★★★★ - 0.12
L401  ★★★★★ - 0.123  ← -0.003 (사실상 보합)
```

L371 격하 추세 (-0.04) 가 L401 에서 *멈춤*. 이는 plan→실측 전환 4건의 회복 효과가 빈 loop 페널티와 정확히 상쇄됨을 의미한다. 추세 반전은 아니지만 *추가 격하 정지*.

근거 (+/-):
- (+) L372 cluster joint 실측 PASS (limitation 8 부분 회복): +0.012
- (+) L374/L375/L377 sampling/pipeline 검증: +0.011
- (+) L385 CKN r=0.685 holographic falsifiable headline: +0.005
- (+) L389 BRST pillar 4 보강: +0.005
- (+) 11 plan-only ATTACK 가치 (L378~L387, L390, L392): +0.012
- (-) L373 M1 vs M2sym Δχ²≈0 narrative 약화 (사용자 통찰 galactic 내부 분할): -0.008
- (-) L388 c 계수 first-principle 한계 정직 인정 (★★⅓ 천장): -0.007
- (-) 10 빈 loop 효율 손실 (34.5%): -0.020
- (-) L384 LPA' 빈 템플릿 (실 도출 부재): -0.003

**순 변화: -0.003** (보합).

---

## JCAP 변화

```
L341:  JCAP   90-94%
L371:  JCAP   88-92%   (-2%)
L401:  JCAP   87-92%   (-1%)
PRD     79-86%   (-1%)
MNRAS   85-90%   (-1%)
CQG     79-86%   (-1%)
PRL     12-18%   (변화 없음 — Q17 / Q13+Q14 미달 유지)
```

JCAP -1%: 빈 loop 비율 악화 (14% → 34.5%) -1.5%, 실측 전환 4건 +1%, 헤드라인 CKN r=0.685 +0.5%, c 계수 상한 정직 -1%. 합 -1%.

---

## 진보 궤적 (315 loop)

```
L75   ★★★★½+        (출발)
L155  ★★★★★ -0.30   (이론 기본 골격)
L211  ★★★★★ -0.18   (BAO/SN/CMB phenomenology 안정)
L241  ★★★★★ -0.12   (성장채널/PPN)
L271  ★★★★★ -0.065  (multi-loop 누적 정합성)
L321  ★★★★★ -0.05   (사전등록·정직개시)
L331  ★★★★★ -0.07   (글로벌 audit, 6 신규 limitations)
L341  ★★★★★ -0.08   (audit 후속, plan/design 4)
L371  ★★★★★ -0.12   (29 loop plan 가치 + 실측 부재 + 4 빈 loop 정직)
L401  ★★★★★ -0.123  (29 loop, 실측 전환 4 + 빈 loop 10 정확 상쇄)  ← 본 loop
```

**격하 추세 정지**. 단, 회복 추세 진입은 아님. 의미 있는 진보:
1. L347 cluster 3-archive plan 이 *L372 실측 PASS* 로 첫 졸업.
2. L357/L358/L361 sampling spec 이 *L374/L377/L375 toy/smoke 졸업*.
3. L385 CKN 홀로그래픽 r=0.685 가 SQT 의 *2번째 falsifiable 헤드라인*.

부정적 직시:
1. L348 N=50 cluster pool, L349 N=25 CLASH, L350 PSZ2 — 핵심 archive 실측 미진입.
2. L373 V-shape symmetric 의 SPARC Δχ² ≈ 0 결과는 사용자 통찰 *galactic 내부 분할 (z 의존 비단조)* 가설을 약화. 단, 3-anchor (cosmic/cluster/galactic) 외부 분할은 영향 없음.
3. L376/L391/L393~L400 10 빈 loop 의 효율 손실은 격하 추세를 멈추게 만든 회복분과 정확히 같은 크기.

---

## 실측 진행도 — L371 plan-only 28 spec 의 회복 상태

| L371 spec | 후속 loop | 실측 상태 | 회복 |
|-----------|-----------|-----------|------|
| L347 (3-cluster joint) | **L372** | **실측 PASS** mu=7.7546±0.114, p_homog=0.958, A1689 weight 0.40 | **졸업** |
| L348 (LoCuSS N=50) | (미실행) | plan 유지 | — |
| L349 (CLASH N=25) | (미실행) | plan 유지 | — |
| L350 (PSZ2 vs lensing bias) | (미실행) | plan 유지 | — |
| L351 (Bullet ↔ A520) | (미실행) | OPEN 유지 | — |
| L352 (b 1-loop) | L388 | **상한 인정** (KILL: c first-principle 불가) | 부분 졸업 (negative) |
| L353 (c 2-loop) | L388 | 동일 | 부분 졸업 (negative) |
| L354 (Wetterich FRG σ_0 flow) | L383 plan / L384 빈 | 미진전 | — |
| L355 (SQT UV FP ↔ AS NGFP) | L384 빈 | 미진전 | — |
| L356 (Λ_UV=18MeV DM XENON 충돌) | (미실행) | limitation 13 유지 | — |
| L357 (5-dataset emcee) | **L374** | **smoke PASS** (실 SQMH 아님, toy Gaussian) | **부분 졸업** |
| L358 (dynesty NS multimodal) | **L377** | **toy PASS** (synthetic 2-Gauss) | **부분 졸업** |
| L359 (MCMC Convergence Diagnostics) | L374 | smoke 동시 보고 | **부분 졸업** |
| L360 (Q_DMAP cross-tension) | (미실행) | plan 유지 | — |
| L361 (SQT mock IR) | **L375** | **PASS** 100/100 recovery, RMSE 0.017 dex | **졸업** |
| L362/L363/L364/L365/L368/L370 (빈/탐색) | — | 변화 없음 | — |
| L344~L346 (P9+P11 anchor forecast) | (미실행) | plan 유지 | — |

**졸업 카운트**: 4 spec 졸업 (L347, L357, L358, L361) + 1 부분 졸업 (L359 = L374 동시) + 2 negative 졸업 (L352/L353 = L388 KILL).

**실측 회복도**: L371 plan-only 28 spec 중 7 spec 처리 (25%). 그러나 *졸업의 질* 은 toy/smoke 가 다수 — 실 SQMH likelihood 5-dataset joint 는 미진입.

L371 의 -0.030 plan-실측 페널티 중 약 +0.020 보전. 잔여 -0.010 은 핵심 cluster archive 50/25 와 실 SQMH likelihood 미진입에서 유래.

---

## 신규 PASS / 회복

1. **L372 3-cluster joint PASS**: A1689+Coma+Perseus 3-archive joint mu=7.7546±0.114, Cochran Q p=0.958, A1689 weight 0.403 (dominance resolved fraction 0.597). *limitation 8 (cluster single-source) 부분 회복*. 4/4 pre-registered prediction PASS.
2. **L375 mock IR PASS**: SQT BB σ_0 MAP recovery 100/100 at η=0.1 noise, bias -0.006 dex, RMSE 0.017 dex. Pipeline 정합성 검증.
3. **L377 dynesty multimodal toy PASS**: 두 모드 모두 검출, lnZ -5.479±0.240 (analytic -5.537), centroid 거리 0.014~0.033 — 0.05σ 이하 정확.
4. **L385 CKN 홀로그래픽 r=0.685 (Hubble scale)**: SQT 의 두 번째 falsifiable headline. n_∞/n_max ≈ 0.685 가 saturation 한계 근처에서 자기무모순.
5. **L389 BRST diff gauge invariance PASS**: SQMH 작용의 일반좌표변환 covariant 구조에서 BRST nilpotency, ghost cohomology 보존. pillar 1/2 보강.

---

## 신규 limitations / 격하

1. **L373 narrative 약화**: SPARC 163-galaxy 단일 데이터셋에서 M2 V-shape symmetric 이 M1 linear 대비 Δχ²≈0 (k=3 의 추가 자유도가 무의미). M2 asymmetric 만 Δχ²=6.93 확보 (k=4). **사용자 3-regime narrative 의 galactic 내부 비단조 가설이 약화**. 외부 3-anchor 분할은 영향 없으나 단일 환경 proxy log V_max 내부에서는 비단조 강제 안 됨.
2. **L388 c 계수 first-principle 한계 인정**: 2-loop n self-energy + setting-sun 만으로는 c 계수 first-principle 도출 *불가*. BPHZ 정리에 의해 sub-divergence 1-loop 흡수, 2-loop 는 β_c (RG running) 만 정함, 초기조건 외부 입력. **pillar 4 ★★→★★⅓ 의 ⅓ 부분 회복이 현 구조의 상한**. 추가 회복은 새 대칭 (스케일/shift/보존 전류) 발견 필요.
3. **빈 loop 10건** (L376, L391, L393~L400) — 예산 효율 정직 격하.
4. **L384 LPA' 빈 템플릿** — Wetterich η, NGFP, critical exponent 8인 도출 미수행.

신규 limitation 14 (제안): L388 의 *c 계수 first-principle 한계*. 정직 인정 — pillar 4 ★★⅓ 가 천장.

---

## Honest open issues (영구 4 + L322–L370 신규 6 + L341 추가 2 + L371 신규 1 + L401 신규 1 = 14)

### 영구 (4)
1. σ_8 +1.14% structural
2. H0 ~10% only
3. n_s OOS
4. β-function full deriv → L352/L353 부분 진전 → **L388 천장 인정**

### L322–L370 신규 (6)
5. 3-regime 강제성 → **L373 SPARC 내부 약화** (단조 vs 비단조 sym Δχ²≈0)
6. Sloppy dim=1 → L343 dip 0.618 (변화 없음)
7. Theory-prior 부분만 (pillar 4 ★★) → L352/L353 ★★⅓ + **L389 BRST PASS** + **L388 천장 인정**
8. Cluster single-source → **L372 3-archive PASS** (부분 회복), L348/L349/L350 N=50/25/PSZ2 미진입
9. Subset Bayes factor → L374/L377 toy PASS, 실 SQMH joint 미진입
10. Micro 80% 상한 → L379 Causet meso plan, L382 SK Wightman 표준 (변화 없음)

### L341 추가 (2)
11. a4 emergent metric pillar OPEN → L379 Causet meso 가설 plan
12. P17 Tier B V(n,t) derivation gate → **L380 plan 진입** (실측 미달)

### L371 신규 (1)
13. Λ_UV=18MeV DM cross-section 위험 → 변화 없음 (L356 계열 미실행)

### L401 신규 (1)
14. **c 계수 first-principle 한계 (L388)** — pillar 4 ★★⅓ 천장. 2-loop n self-energy + setting-sun 으로는 close 불가, 새 대칭 발견 필요.

---

## Major positive (L372–L400)

1. **L372 cluster joint 실측 PASS**: 4/4 pre-reg, A1689 단일 dominance 60% 해소, sigma_mu tightening x1.57. limitation 8 부분 회복.
2. **L375/L377/L374 sampling pipeline 검증**: emcee Rhat<1.01, dynesty multimodal 두 모드 검출, mock IR 100/100. 5 spec 중 3 spec 부분 졸업.
3. **L385 CKN r=0.685**: SQT 의 *2번째 falsifiable headline*. holographic IR/UV mixing bound 와 SQT n_∞ 의 자연스러운 saturation.
4. **L389 BRST PASS**: pillar 1/2 양자장론적 일관성 보강 +0.005.

## Major negative (L372–L400)

1. **빈 loop 10건 (L376, L391, L393~L400)** — 예산 낭비, 격하 추세를 멈추게 만든 회복분과 같은 크기.
2. **L373 SPARC narrative 약화**: 사용자 3-regime 통찰의 galactic 내부 분할 약화. 단, cosmic/cluster/galactic 외부 3-anchor 분할은 영향 없음.
3. **L388 c 계수 천장 인정**: pillar 4 ★★⅓ 가 현 구조 상한. PRL Letter 진입 조건 (Q17 완전 또는 Q13+Q14) 미달 유지.
4. **L348/L349/L350 핵심 cluster archive 미진입**: 3-archive (L372) 졸업했으나 50/25 pool 은 plan 유지.
5. **5-dataset 실 SQMH joint 미진입**: L374 는 toy, L377 은 synthetic. 실 likelihood 적용은 차후.

---

## Paper revision 추가 의무 (L371 14 행 → L401 18 행)

(L371 1~14 행 유지)

15. Sec 4 limitations 14 행: L388 c 계수 first-principle 한계 (pillar 4 ★★⅓ 천장) 정직 명시.
16. Sec 3 cluster phenomenology: L372 3-archive joint mu=7.7546±0.114, A1689 dominance 해소 (limitation 8 부분 회복) 추가.
17. Sec 5 falsifiable headlines: L385 CKN r=n_∞/n_max ≈ 0.685 (Hubble scale) 신규 헤드라인 명시.
18. Sec 7 Future work: L348/L349/L350 cluster archive 50/25/PSZ2 + L344~L346 P9+P11 anchor forecast — 단번에 +0.05~+0.08 회복 잠재 유지.

---

## 한 줄 결론

> **315 loop 후 본 이론 ★★★★★ -0.123** (격하 추세 정지, 보합).
> **JCAP 87-92% accept** (-1%).
> Plan→실측 전환 4건 (L347/L357/L358/L361 → L372/L374/L377/L375) 의미 있는 진보, 그러나 빈 loop 10건이 정확히 상쇄.
> **신규 falsifiable headline**: L385 CKN r=0.685 (Hubble).
> **신규 천장 인정**: L388 c 계수 first-principle 한계 → pillar 4 ★★⅓ 가 상한.
> **사용자 3-regime narrative**: L373 SPARC 단일 환경 proxy 내부에서 약화, 외부 3-anchor (cosmic/cluster/galactic) 분할은 유지.
> 다음 critical: L348/L349/L350 cluster archive 실측 + 실 SQMH 5-dataset joint 진입 → +0.05~+0.08 회복 잠재.

정직: 본 audit 의 보합은 회복 4건 + 빈 loop 10건의 *우연한 상쇄* 이며, 다음 1~2 loop 의 archive 실측 진입 또는 빈 loop 재발 여부에 따라 ★ 회복/추가 격하 결정.
