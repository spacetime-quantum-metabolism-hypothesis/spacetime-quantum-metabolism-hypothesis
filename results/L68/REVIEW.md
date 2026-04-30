# L68 — 측정 오염 가설 3-Phase 검증

## 결과 요약

| Phase | 검증 | 결과 | 상세 |
|-------|------|------|------|
| 1 | SPARC V_max binning | **부분 PASS / 전체 FAIL** | high-V 0.376 dex, low-V 1.085 dex |
| 2 | Systematics inflation | **FAIL** | 0.89 dex required vs 0.06 literature (15x) |
| 3 | AICc 비교 | A 단조+systematics 우승 | 단, 모든 모형 χ²>>dof |

---

## Phase 1 — SPARC V_max binning

```
전체:               σ(log a_0) = 0.784 dex (n=175)
V_max < 68:         std = 1.085 dex (n=43)  ← 왜소 은하, fit 노이즈 dominant
V_max [68,100]:     std = 0.730 dex (n=43)
V_max [100,186]:    std = 0.626 dex (n=45)
V_max ≥ 186:        std = 0.376 dex (n=44)  ← 거대 은하, *3배 감소*
평균 within-bin:    0.704 dex
분산 감소:          19.3%
```

**핵심 발견 1**: 거대 은하 (V_max≥186 km/s) σ_0 spread = **0.376 dex** — 거의 PASS 임계.
→ 측정 노이즈 일부 제거 가능. 사용자 가설 *부분 지지*.

**핵심 발견 2**: 그러나 거대 은하 평균값 a_0 ≈ 10^(-9.98) m/s² → σ_0 ≈ 2.4e9
T17 (cosmic) σ_0 = 2.34e8 와 여전히 **10배 차이** (1 dex).
→ 노이즈 제거 후에도 *비단조성 robust*.

## Phase 2 — Systematics inflation

```
log_sigma_T17 = 8.37
log_sigma_T20 = 7.75
log_sigma_T22 = 9.52  (data-driven)
spread       = 1.77 dex (T22 - T20)

요구 systematic / 채널: 0.89 dex
문헌값:                  ~0.06 dex
배율:                    14.8 x
```

**결론**: 어떤 표준 systematics 합산도 1.77 dex 격차 흡수 불가능. 단순 측정 오염 가설 *FAIL*.

## Phase 3 — AICc model comparison

```
Model A (단일σ_0 + 경로-systematics, k=2):  χ²=188.3, AICc=204.3 ← 1위
Model C (공명 peak, k=2):                   χ²=255.2, AICc=271.2  Δ=+66.9
Model B (단조 sigmoid 게이팅, k=1):         χ²=871.6, AICc=877.6  Δ=+673
```

**Model A 우승, 그러나 χ²/dof = 188** — 절대적으로는 모든 모형 *심한 미스핏*.
"Best of bad" 상황.

---

## 4인팀 사후 비판

### **P (이론)** — 부분 옹호

✓ Phase 1 거대 은하 결과는 *부분 지지*: 측정 노이즈가 일부 dwarf 분산 만듦.
✗ 그러나 노이즈 보정 후에도 1 dex 격차 남음 → 단조 σ_0 *불가능*.
✓ Model A 우승은 *path-systematics 가 단일 σ_0 을 부분 구원* 의미.

### **N (수치)** — 수치 점검

✓ SPARC fit 175/175 OK. 1.3s 만 소요 (joblib 8 worker).
✓ V_max bin 등분위 적절, n≥43 통계적 충분.
⚠ Phase 3 χ²>>dof — *어떤 모형도 데이터에 적합 안 됨*. 기저 자유도 부족 가능성.
⚠ Model A 의 path-systematics 가중치 w_path={1.0, 0.5, 0.0} 는 *추측* — 정당화 필요.

### **O (관측)** — 결정적 분석

✓ V_max binning 통계 robust.
> "거대 은하만 본다면 σ_0 ≈ 2.4e9 (T22). dwarf 노이즈 제거 후도 T17 (2.3e8) 과 *10배* 차이."
> "이 *10배* 차이는 systematics 로 흡수 불가능. *진짜 비단조성*."
✗ 사용자 측정 오염 가설은 *부분 노이즈 설명* 가능하나 *spectrum 비단조성* 못 설명.

### **H (자기일관 헌터, 강력 모드)** — 사전 예측 검증

> **"사전 예측 적중**:
> (1) Phase 1 PASS partial — 적중 (high-V std 0.376, low-V 1.085).
> (2) Phase 2 FAIL — 적중 (systematics 부족).
> (3) Phase 3 우승은 path-systematics 의 *부분 구원* — 새 발견."
>
> **"중요한 깨달음**: Model A 우승은 절대값 PASS 가 아니라 *상대 비교*. 모든 모형 χ²>>dof, 절대적으로는 *전부 사망*."
>
> **"진정한 결론**: σ_0 비단조 spectrum 은
> (a) 일부 fit 노이즈 (Phase 1 dwarf bin)
> (b) 일부 path-systematics (Model A 부분 우승)
> (c) **남은 ~1 dex 잔차는 진짜 물리적 비단조성**"

---

## 8인팀 합의 — 정직한 결론

### 사용자 가설 평가

✓ **부분 옹호**: Phase 1 dwarf 노이즈 + Phase 3 path-systematics 효과 = ~0.5 dex 흡수 가능.
✗ **전체 FAIL**: 남은 ~1 dex 격차 → 진짜 물리적 비단조성 *robust*.

### 본 이론 위치 갱신

```
가능성 분배 (사후):
- 단순 단조 σ_0 + 측정 오염       :  20%  (부분만 작동)
- 진짜 비단조성 (필요 신규 공리)  :  60%  (지배적)
- 본 이론 자체 폐기               :  20%  (남은 가능성)
```

### 다음 단계 권고

**옵션 A** — 비단조 공리 본격 시뮬 (L69):
- 🅜 공명, 🅟 곡률 부호, 🅠 위계 깊이, 🅢 차원 적응 통합
- 1.77 dex spread 정량 적합 시도

**옵션 B** — 부분 모델 격하 (L68 받아들임):
- T22 a_0 high-V_max 단일 σ_0 ≈ 2.4e9 채택
- T17 cosmic 부분 ΛCDM 분리 (SQT 비기여)
- 본 이론 = "거대 은하 SQT + ΛCDM 우주" 부분 모델

**옵션 C** — σ_0 spectrum 의 *진짜 형태* 탐색:
- 175 SPARC galaxy 별 σ_0(V_max, distance, type) 회귀
- T20, T17 분리 재추출
- σ_0(env) 함수 형태 *데이터 직접 추출*

**옵션 D** — 정직 종료:
- L48~L68 종합 보고서
- 본 이론 *큰 틀* 폐기, MOND 변형 지위만 남김

**8인팀 합의**: **옵션 C → A 순차** (데이터 우선, 그 후 이론).
