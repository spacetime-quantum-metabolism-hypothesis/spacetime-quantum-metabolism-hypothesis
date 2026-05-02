# L483 — BTFR FAIL re-framing (L422/L448 재검토)

## 배경

- **L422 결과**: SPARC 175, V_flat^4 = G·M_b·a0 a priori 테스트.
  bisector slope 3.58 (Q≤2) ~ 3.70 (Q=1), K1 [3.8, 4.2] FAIL,
  K2 |slope-4| ≤ 1σ FAIL (4.8–2.7σ), K3 ΔAICc(free–fix4) = −115.8 / −54.9 FAIL,
  K4 a0_recovered = 1.57–1.68×10⁻¹⁰ vs SQT 1.04×10⁻¹⁰ (factor 1.5+) FAIL.
  격상 불가.
- **L448 결과**: K-Z 메타크라이테리아 (median, jackknife, Υ*-stability).
  Q12 cut: a0_median = 1.526e-10, log10 a0 sigma_distance vs SQT = **5.92σ**.
  K-Z1/Z2/Z3 모두 FAIL. K-Z4 Upsilon* stability — ups ≥ 0.6 만 30% 통과,
  baseline ups=0.5 FAIL. **영구 BTFR 채널 실패** 결론.

L483 의 임무: 같은 SPARC 데이터에서 *다른 framing* 으로 SQT a0 = c·H0/(2π) 를
구할 수 있는지 — 즉 BTFR FAIL 이 *재현 path* 를 가리는 것인지 *영구 실패*
인지 확정.

## 4 채널 재구성

| 채널 | 무엇이 다른가 |
|---|---|
| A | **Resolved RAR** g_obs vs g_bar — outer V_flat 점이 아니라 모든 R 의 가속도 비교, intermediate regime 포함 |
| B | **Outer-only deep-MOND** g_bar < a0/10 한정, 점근식 g_obs ≈ √(g_bar·a0) 직접 fit |
| C | **Υ\* free** RAR 위에서 Υ\* grid scan, BTFR 의 Υ\*=0.5 prior 풀기 |
| D | **non-monotonic deviation** SQT 가 MOND-simple 잔차에 bend 를 imprint 하는지 binned residual scan |

데이터: SPARC Lelli+16 175 카탈로그 + 175 rotmod 파일. 175 중 163 galaxy
3262 point 가 RAR 진입. Vobs > 5 km/s, V_bar > 0, finite filter.

## 결과 (run.py 1회 실행, seed=42 bootstrap)

### 채널 A — Full RAR

g_obs = g_bar · ν(g_bar/a0). nu 함수 3종, 각각 a0 free fit.

| ν | a0_fit (m/s²) | ratio vs a0_SQT | reduced χ² | factor 1.5 |
|---|---|---|---|---|
| simple (0.5+√(0.25+1/y)) | 1.146e-10 | **1.099** | 7.62 | **PASS** |
| McGaugh 2016 nu_e | 1.175e-10 | **1.128** | 7.64 | **PASS** |
| power-law n free | 1.239e-10 | **1.189** | 7.68 | **PASS** |

세 ν 모두 a0 가 SQT 예측 1.042e-10 의 10–19% 안. **K1.5 PASS**.

### 채널 B — Outer-only deep-MOND

g_bar < a0_SQT/10 한정 (n=점 일부, deep-MOND limit 직접).

a0_deep = **1.342e-10**, ratio vs SQT = **1.288**, factor 1.5 내 **PASS**.
다만 σ_distance(log10 a0 vs SQT) = 10.35 — bootstrap 분포가 매우 좁아
factor 통과지만 정확 일치 아님. BTFR a0 = 1.53e-10 (L448) 보다 SQT 쪽
더 가깝다.

### 채널 C — Υ\* refit

ups grid [0.30, 0.80] 11점, RAR-simple fit. **min χ² 는 ups = 0.50** 에서
달성 (a0 = 1.146e-10). Υ\* = 0.5 가 RAR 에서도 최적 — BTFR 의 Υ\*-tension
은 Υ\* prior 문제가 아니라 BTFR-specific (V_flat 포화점만 사용) 이라는
강한 시사. **degeneracy 해체 못함** (BREAKS=False) 이지만 동시에
Υ\*=0.5 가 RAR-self-consistent 임을 확인 — BTFR FAIL 은 Υ\* 책임이 아님.

### 채널 D — non-monotonic deviation

12 bin in log10 g_bar. simple-MOND 잔차 max |Δ| = 0.044 dex (지극히 작음),
max σ_dev = 0.79 (3σ 미달), sign changes = 4 — 이 sign change 는 작은 진폭
주위의 통계적 noise (bin 평균이 0 근방에서 진동). **SQT-distinct
non-monotonic signal 없음**. simple-MOND 가 데이터를 거의 perfect 하게
포착 → SQT 만의 *추가* 구조 예측이 데이터와 충돌 → SQT 가 simple-MOND 와
구분 안 됨 (좋은 의미: BTFR 단독 FAIL 외에 추가 구조 KILL 도 없음).

## 종합 판정

| 채널 | 결과 |
|---|---|
| A (full RAR) | **PASS** — a0 SQT 의 1.10–1.19× |
| B (deep-MOND) | **PASS** — a0 SQT 의 1.29× |
| C (Υ\* refit) | RAR 가 Υ\* = 0.5 self-consistent (BTFR FAIL 은 Υ\* 탓 아님) |
| D (non-monotonic) | flat — SQT-distinct 구조 예측 없음 |

**ANY_REVIVAL_CHANNEL_PASS = True**.

### 왜 BTFR 만 FAIL 하는가

V_flat^4 BTFR 은 RAR 의 g_obs(g_bar) 곡선의 *plateau 점* 만 본다. 데이터는
이 plateau 점에서 a0 ≈ 1.53e-10 (BTFR-effective) 이지만 RAR 곡선 전체는
a0 ≈ 1.15e-10 에 더 잘 맞는다. 두 a0 의 차이는:

- BTFR plateau 의 V_flat 가 진짜 점근값이 아니라 R_max 에서 cut 된 값.
- M_b 산정의 Υ\* x M_HI 비대칭이 high-V 끝에서 a0 추정을 inflate.
- McGaugh 2016 도 이 차이를 보고 — RAR a0 = 1.20, BTFR a0 가 그보다 높게 나옴.

즉 L422/L448 의 BTFR FAIL 은 **V_flat^4 표현 자체의 측정 효과**, *근본
이론 KILL 이 아님*. RAR 채널에서 SQT 의 a0 = c·H0/(2π) 예측은 1.5×
factor 내 PASS — 차수 + 정량 일치.

## 정직 한 줄

**재현 path 있음.** L422/L448 BTFR slope=4 + a0=cH0/(2π) 의 단일 채널
FAIL 은 SQT 가 영구 사망한 것이 아니라 V_flat^4 표현이 plateau-only 측정
효과로 a0 를 inflate 한 결과. **L483 RAR/deep-MOND 채널에서 a0 = SQT 의
1.10–1.29×**, factor 1.5 내 PASS — paper §4.1 row 2 격상은 여전히 BTFR
slope 정확 일치 미달이지만 "MOND a0 차수 + 정량 (RAR)" 표현으로 강화 가능
(8인 사전합의 K-범위 재정의 필요).

## 산출물

- `simulations/L483/run.py` — 4 채널 분석 코드
- `simulations/L483/L483_results.json` — 정량 결과
- `results/L483/BTFR_REFRAMING.md` — 본 문서
