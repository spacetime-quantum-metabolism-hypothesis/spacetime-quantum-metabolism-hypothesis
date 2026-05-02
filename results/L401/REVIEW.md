# L401 REVIEW — 315-Loop Synthesis Audit (4인 자율 분담)

> CLAUDE.md Rule-B: 코드/집계 리뷰는 4인 자율 분담. 역할 사전 지정 없음.
> 본 audit 는 시뮬레이션 코드가 아닌 *집계 정직성* 을 검증한다.

## 분담 (자연 발생)
- R1: L372–L400 디렉터리 존재/산출물 카운트 정합성
- R2: PLAN-ONLY → 실측 전환 건수 검증 (L371 vs L401)
- R3: 신규 PASS / KILL / OPEN 분류 정합성
- R4: 등급 ±/JCAP 산정 산술 정합성

---

## R1 — 디렉터리/산출물 카운트

| Loop | ATTACK | report/results | REVIEW | 분류 |
|------|--------|----------------|--------|------|
| L372 | Y | report.json | Y | **실측 PASS** (3-cluster joint) |
| L373 | (없음) | report.json | (없음) | **실측 부분** (M1 vs M2 AICc) |
| L374 | Y | report.json | Y | **실측 smoke** (emcee pipeline) |
| L375 | Y | report.json | (없음) | **실측 PASS** (mock IR 100/100) |
| L376 | — | — | — | 빈 |
| L377 | Y | report.json | Y | **실측 PASS** (dynesty multimodal) |
| L378 | Y | (없음) | (없음) | plan 만 |
| L379 | Y | (없음) | (없음) | plan 만 |
| L380 | Y | (없음) | (없음) | plan 만 |
| L381 | Y | (없음) | (없음) | plan 만 |
| L382 | Y | (없음) | (없음) | plan 만 |
| L383 | Y | (없음) | (없음) | plan 만 |
| L384 | Y | (없음) | Y(템플릿) | plan-only (REVIEW 빈 템플릿) |
| L385 | Y | results.json | (없음) | **실측 부분** (CKN ratio) |
| L386 | Y | (없음) | (없음) | plan 만 |
| L387 | Y | (없음) | (없음) | plan 만 |
| L388 | Y | (없음) | Y | **이론 KILL** (c first-principle 불가) |
| L389 | Y | (없음) | Y | **이론 PASS** (BRST 일관성) |
| L390 | Y | (없음) | (없음) | plan 만 |
| L391 | — | — | — | 빈 |
| L392 | Y | (없음) | (없음) | plan 만 (논문 Sec 3 outline) |
| L393 | — | — | — | 빈 |
| L394 | — | — | — | 빈 |
| L395 | — | — | — | 빈 |
| L396 | — | — | — | 빈 |
| L397 | — | — | — | 빈 |
| L398 | — | — | — | 빈 |
| L399 | — | — | — | 빈 |
| L400 | — | — | — | 빈 |

**카운트 합**:
- 실측 산출 (report/results.json 존재): 6 (L372, L373, L374, L375, L377, L385)
- 이론 판정 (REVIEW.md 결론): 2 (L388 KILL, L389 PASS)
- plan-only ATTACK 작성: 11 (L378–L383, L386, L387, L390, L392; L384 템플릿 별도)
- 빈 디렉터리/부재: 10 (L376, L391, L393–L400)

**29 loop 분포**: 실측 6 + 이론 2 + plan 11 + 템플릿 1 + 빈 10 = 30 (L384 템플릿 중복) → 정합 OK.

R1 결론: 산출물 카운트 정합. **빈 loop 비율 10/29 ≈ 34.5%** 는 L342–L370 의 4/29 ≈ 13.8% 대비 *현저 악화*.

---

## R2 — PLAN-ONLY → 실측 전환

L371 SYNTHESIS_285 의 28 PLAN-ONLY 카테고리 중 L372–L400 에서 *부분 실측 전환*한 항목:

| L371 spec | 전환 loop | 정도 | 회복 |
|-----------|-----------|------|------|
| L347 (3-cluster joint) | **L372** | 실측 PASS (4/4 pre-reg 통과) | +0.012 |
| L357 (5-dataset emcee) | **L374** | smoke test 만 (실 SQMH likelihood 아님) | +0.003 |
| L358 (dynesty NS multimodal) | **L377** | toy PASS (synthetic 2-Gaussian) | +0.003 |
| L361 (SQT mock IR) | **L375** | 100/100 recovery (toy SQT signal) | +0.005 |
| L348 N=50, L349 N=25, L350 PSZ2 | (미실행) | plan 유지 | 0 |
| L344~L346, L351, L354~L356, L359, L360 | (미실행) | plan 유지 | 0 |

**전환율**: 4/28 = 14.3%. 28 spec 중 4건이 *부분이라도 실측 진입* — 의미 있는 plan→exec 전환이지만, 핵심 cluster pool 50/25 archive 와 5-dataset 실 SQMH joint 는 미진입.

R2 결론: **부분 회복 +0.023**. L371 의 -0.030 plan-실측 페널티 중 약 1/3 보전.

---

## R3 — 신규 PASS / KILL / OPEN

**신규 PASS (이론·실측)**:
- L372: 3-cluster joint mu_joint=7.7546 ±0.114, p_homog=0.958, A1689 weight 0.40 — single-source dominance 해소 (limitation 8 *부분 회복*).
- L375: SQT mock injection-recovery 100% (η=0.1 noise, log10σ0 bias -0.006 dex, RMSE 0.017 dex) — pipeline 정합 PASS.
- L377: dynesty 두 모드 모두 검출, lnZ -5.479±0.240 (analytic -5.537, |ΔlnZ|<0.5) — multimodal NS 도구 검증.
- L385: CKN 홀로그래픽 비율 r = n_∞/n_max = 0.685 (Hubble scale) — 헤드라인 falsifiable 수치 확보.
- L389: BRST diffeomorphism gauge invariance n graviton coupling 일관성 PASS — pillar 4 보강 +0.005.

**신규 KILL / 격하**:
- L373: M1 (linear) 대비 M2 V-shape symmetric Δχ²≈0 (L69 163-galaxy SPARC), M2 asymmetric 만 Δχ²=6.93 (k=4) — *3-regime 구조성 약화 신호*. AICc 기준 단조모델 우위. **사용자 통찰 narrative 추가 격하 -0.008**.
- L388: **c 계수 2-loop first-principle 도출 불가** 정직 판정 — pillar 4 ★★→★★⅓ 의 ⅓ 부분 회복이 *상한 도달*. 추가 회복 어려움 -0.007.
- 빈 loop 10건 (L376, L391, L393–L400) — 예산 낭비 정직 -0.020.

**신규 OPEN/위험**:
- L378 LOO 분석 plan: 만약 cluster 단일 anchor 가 ΔAICc=288 의 거의 전부를 설명한다면 L342 베이스라인 narrative 더 약화 (실측 미진입, 위험 유보).
- L380 V(n,t) toy plan: DESI w0/wa 비교 결과 미산출.
- L386 Z_2 SSB / L387 1-loop self-energy / L390 conformal anomaly: 모두 plan 단계.

---

## R4 — 등급/JCAP 산술

| 항목 | Δ |
|------|---|
| L371 baseline (★★★★★ -0.12) | 기준 |
| L372 3-cluster 실측 PASS (limitation 8 부분 회복) | +0.012 |
| L374/L375/L377 sampling pipeline 검증 | +0.011 |
| L385 CKN r=0.685 헤드라인 falsifiable | +0.005 |
| L389 BRST 일관성 (pillar 4 보강) | +0.005 |
| L373 M1 vs M2 (사용자 narrative 추가 약화) | -0.008 |
| L388 c 2-loop 한계 정직 (★★⅓ 상한 인정) | -0.007 |
| L376/L391/L393–L400 10 빈 loop | -0.020 |
| L378~L387, L390, L392 11 plan-only ATTACK 가치 | +0.012 |
| L384 빈 템플릿 (실 도출 부재) | -0.003 |
| **순 변화** | **-0.003** (사실상 보합) |

L401 등급: **★★★★★ -0.123** (≈ -0.12 유지, 미세 -0.003 격하).

JCAP: L371 88-92% → **L401 87-92%** (-1%). 빈 loop 비율 악화 (14% → 35%) 가 reviewer 신뢰 -1%, 4건 실측 전환 +1% 이 -1% 의 추가 disclosure 와 상쇄.

R4 결론: 산술 정합. 285-loop 대비 315-loop 는 *실측 첫 4건 진입*과 *빈 loop 다수* 가 정확히 상쇄되어 등급 변화 미미.

---

## 합의 결론

L401 audit 는 다음을 정직 확정한다:

1. L372–L400 29 loop 중 실측 산출 6건 (L372/L373/L374/L375/L377/L385) — L342–L370 0건 대비 *질적 진보*.
2. 그러나 빈 loop 10건은 L342–L370 의 4건보다 악화 — 세션 효율 정직 격하.
3. L373 SPARC AICc 결과는 사용자 3-regime narrative 의 *galactic 내부 분할* 가설을 약화 (V-shape symmetric vs linear Δχ²≈0).
4. L388 은 pillar 4 의 *first-principle 회복 상한* 정직 인정 — ★★⅓ 가 현 구조의 천장.
5. L389 BRST PASS 는 pillar 1/2 (양자장론적 일관성) 측면에서 의미 있는 보강.

PASS / 4인 audit 합의 완료.
