# L70 — M4 공명 정밀 검증 + Cross-Validation

L69 의 Branch A vs B 동률 (ΔAICc=0.33) 결판. 4인팀 비판 모드.

---

## OPTION (1) — Dwarf 정밀 검증

```
in-band  V_flat ∈ [12, 48] km/s : n=6   median log_sigma=9.888 (std 1.287)
out-band V_flat ≥ 120 km/s      : n=63  median log_sigma=9.389 (std 0.412)

observed difference = +0.499 dex   ← M4 예측과 부호 일치
M4 predicted        = +0.663 dex
95% CI bootstrap    = [-0.114, +2.995]   ← 영(0) 포함

VERDICT: AMBIGUOUS — sign correct, magnitude close,
         but CI crosses zero due to n_in=6 (small sample)
```

핵심: in-band 표본 부족 (n=6) 으로 통계적 결정 불가. 그러나 **부호와 크기 모두 M4 예측과 일치**.

---

## OPTION (4) — 100-fold 50/50 Cross-Validation ⭐

```
Test χ² (median, n_test=65 갤럭시):
─────────────────────────────────────
  M1 const        273.89  per-dof=4.214  ← 일반화 실패
  M2 linear-V     292.50  per-dof=4.500  ← 일반화 실패
  M4 peak-V        73.74  per-dof=1.134  ★ 일반화 성공
  M7 3-regime      72.37  per-dof=1.113  ★ 일반화 성공

M4 V_peak 안정성 (100 splits):
  median = 1.382, std = 0.004   ← 매우 안정!
  Stability: STABLE

M4 vs M7 paired:
  M4 wins 48/100 splits (≈50/50)
  median(M4 - M7) = +0.33 (M7 미세 우위)
```

**결정적 발견**:

1. **🔥 M4 V_peak 매우 안정** (std=0.004 dex across 100 splits): peak 위치는 데이터 *robust* 신호. *우연 아님*.
2. **🔥 비단조 모형만 일반화**: M4·M7 test χ²/dof ≈ 1.13, 단조 (M1·M2) 4.21~4.50 → 일반화 못 함. L69 결과 *교차검증 강화*.
3. **△ M4 vs M7 통계 동률**: 50/50 paired wins, ΔAICc median +0.33 → 데이터 구분 불가.

---

## 4인팀 사후 비판

### **P (이론)**

> "V_peak std=0.004 dex 는 *놀라운* 안정성. peak 구조는 *진짜 신호*."
> "그러나 M4 와 M7 통계 동률 → 'peak 가 있다' 와 '3-regime 이 다른 σ_0' 이 같은 데이터에서 구분 안 됨."

### **N (수치)**

✓ 100-fold CV — stable.
✓ V_peak std 0.004 → 데이터가 *peak 위치를 정확히 결정*.
⚠ in-band n=6 너무 작음. 결정적 검증 불가 (현재 SPARC).
- 추가 데이터 필요: dwarf SPARC extension, MaNGA dwarf disk fits.

### **O (관측)**

> "in-band V=12-48 km/s 영역 표본 n=6 — *결정적 데이터 부족*. SPARC 확장 또는 LITTLE THINGS / SHIELD survey 통합 필수."
> "관측 부호: in-band 가 +0.5 dex 높음 — *M4 예측과 일치하는 방향*. 통계 유의 부족하나 *반증되지 않음*."

### **H (자기일관 헌터, 강력 모드)**

> **"L70 사전 예측 검증**:
> (1) V_peak 안정성 std<0.20 → *적중* (실제 std=0.004)
> (2) in-band excess >0.1 dex → *부분 적중* (관측 +0.5, 그러나 CI 영 포함)
> (3) M4 vs M7 동률 → *적중* (50/50)"
>
> **"본 이론 H 판정**:
> - peak 구조 *robust* — 우연 아님
> - 그러나 데이터가 *공리 (M4) 와 phenomenology (M7)* 구분 못 함
> - **Branch A 살아있음 (반증되지 않음)**, Branch B 동률 (가능)"
>
> **"권고**:
> - 결정적 결판 위해 추가 데이터 필수
> - 그 동안 Branch B (parsimonious) 채택, Branch A 살아있음 보존"

---

## 최종 판정

```
FINAL VERDICT: TIE
- Branch A (🅜 공명 M4)와 Branch B (3-regime M7) 통계적 동률
- M4 V_peak 매우 안정 (std=0.004) → peak 구조 진짜
- in-band excess 부호 일치 — but n=6 통계 부족
- parsimony 원칙으로 Branch B 1차 채택
- Branch A 반증되지 않음 — 추가 데이터 대기
```

---

## 본 이론 위치 (L70 후)

```
공리 명료성:        ★★★★☆
도출 사슬 견고성:   ★★★☆☆
자기일관성:         ★★★☆☆
정량 예측:          ★★★★☆ (M4 peak 위치 매우 안정)
관측 일치:          ★★★☆☆
파라미터 절감:      ★★☆☆☆
미시 이론 완성도:   ★★☆☆☆
반증 가능성:        ★★★★★ (V_flat~24 dwarf 영역 추가 데이터)

종합:               ★★★☆☆ (L69 후 ★★★ 유지)
```

---

## 다음 단계 권고 (L71 후보)

### 즉시 가능

**(A) L71-1 — Branch B 정착 + 결정적 신규 예측 (3 hours)**
- 3-regime σ_0 동결
- T35 환경 의존 관성, T36 a_0(z), T26 GW 분산 정량 예측
- SKA / ET / MICROSCOPE 미래 데이터 대비

**(B) L71-2 — 추가 SPARC dwarf 데이터 통합 (open)**
- LITTLE THINGS, SHIELD survey 통합
- in-band 표본 n_dwarf > 30 으로 확장
- M4 vs M7 *결정적* 검증

**(C) L71-3 — V_peak ≈ 24 km/s 미시 도출 (open)**
- 동역학 scale 의 SQT 의미 탐색
- a_0 ~ V²/r 연결 → 양자 미시
- 라그랑지안 가설 시도

### 8인팀 합의

**즉시**: (A) Branch B 정착 + 신규 예측. 가장 안전·결정적·생산적.

**병렬**: (C) 미시 도출 — 이론 작업.

**보류**: (B) 추가 데이터 — 외부 catalog 작업 부담.

---

## 산출물

```
results/L70/
├── L70_main.png  — 6 패널 (dwarf precision + CV)
├── REVIEW.md     — 이 문서
└── l70_report.json
```
