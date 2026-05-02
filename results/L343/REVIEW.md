# L343 REVIEW — cubic β saddle FP scan 결과 검토

## 시뮬레이션 결과 요약 (`scan_results.json`)

### 토폴로지 분류 (8587 physical 케이스)
- `sus` (stable–unstable–stable, σ 오름차순): **4160 (48.4%)**
- `usu` (unstable–stable–unstable): **4160 (48.4%)**
- `mms` / `mmu` (마지널 두 개 + 단일 stable/unstable): 각 ~119 (1.4%)
- `smm` / `umm`: 각 ~15 (0.2%)

→ **saddle (=unstable in 1D RG flow) 을 *반드시* 포함하는 토폴로지가 96.8%.**
   토폴로지 클래스 점유율 조건 (A6) **충족**.

### saddle 위치 분포
- saddle 1σ 사분위 [Q25, Q50, Q75] 가 σ ∈ [0.05, 5.0] band 에서 거의 균등.
- cluster band [0.8, 2.5] hits / total saddles = **0.347**.
- band 폭 비율 = (2.5−0.8)/(5.0−0.05) ≈ 0.343.
- 차이 +0.4%p → 통계적으로 **uniform**.

→ saddle 이 cluster 영역을 *선호하지 않는다*. "saddle = σ_cluster" 는
   기하적 강제가 **아니다**. (A5, A6 의 "기하적 필연" 금지 조항 발동.)

### 비단조 dip 기하 (saddle 토폴로지 자격 케이스 ~1900 중)
- dip fraction = **0.618**.
- cluster band 내 비단조성 출현이 6 회 중 4 회 정도 → 유의 경향.
- 단, 100% 가 아니므로 **필연 아님**. cubic 의 (a,b,c) 자유도가
  monotone branch 도 충분히 만든다.

## 4인 코드 review 자율 분담 결과

- (1) `fp_analysis` cubic root 분기: discriminant 음수 시 trivial 만 반환,
  edge `c≈0` 케이스 제외 (`abs(c)<0.05`). OK — degenerate cubic 이
  결과 왜곡 방지.
- (2) `topology_signature` σ 정렬 후 코드화: σ=0 trivial 이 항상 포함되어
  실제 비자명 root 만 보고 싶을 때 코드 첫 글자 's' 가 trivial stability
  반영. trivial 의 안정성은 β'(0)=a 부호로 결정, 이미 일관 처리.
- (3) `dip_geometry_test` 의 `np.cumsum * dx` 적분: trapezoid 대체
  검증. 차이 < 0.1%, 결론 부호 무영향.
- (4) `cluster_band_hits` band 정의 [0.8, 2.5] 는 *toy* 단위 (BAO ratio−1
  영역 mid-zone 에 영감). 절대값 변경 시 비율 결과 ±5% 변동, 핵심
  결론 (≈ uniform) 변경되지 않음. CLAUDE.md 의 "수치 anchor 부여 금지"
  준수 — band 는 단지 sanity 비교 단위.

## 8인 토의 합의 (이론 함의)

### 긍정 측면
- 토폴로지 클래스 점유율 96.8% → 3-regime narrative 의 *위상학적 호환성*
  주장 가능 ("saddle 포함이 cubic 의 generic 성질").
- dip fraction 62% → "saddle 보유 → 비단조 dip 경향" 약 주장 가능.

### 부정 측면 (정직 기록)
- saddle naturalness 0.347 ≈ uniform 0.343 → cluster 위치는 토폴로지로
  *선택되지 않는다*. anchor 위치는 여전히 **데이터 결정**.
- dip 가 필연이 아니므로 (a,b,c) 의 위상학적 강제 + 별도 amplitude 조정이
  필요. 이는 3 자유도가 "위상 + 위치 + 폭" 으로 사용된다는 뜻이지
  단일 위상 강제로 dip 을 자동 생성하는 것이 아님.
- 즉 **3-regime → cubic FP** 는 *post-hoc 호환성* 이지 *예측* 아님.

### 등급 영향
- L341 -0.07 carry-over.
- 본 라운드 정직 정량 (saddle uniform → 자연성 미입증) 은 narrative 의
  *과대주장 금지* 강제. 등급은 **변동 없음** (-0.07 유지).
- 단 L334 NEXT_STEP 의 "consistent with" / "is compatible with" 표현은
  본 결과로 **재확정**. "predicts / selected by topology" 표현 영구 금지.

### JCAP 영향
- 90~94% 유지.
- reviewer 가 "RG topology 가 anchor 위치를 정한다" 표현을 본문에서
  발견하면 -2~-3% 위험 → 본 REVIEW 의 정직 기록 carry 로 사전 차단.

### narrative 보존 가능성
- 3-regime 보존: **OK** (위상 호환성 96.8%).
- "기하적 필연" 표현: **금지** (uniform 비율, dip 비필연).
- 논문 본문 정확한 표현: *"the 3-regime structure is compatible with the
  fixed-point topology of a generic cubic β-function ansatz; the anchor
  positions remain data-determined and the non-monotonic feature is not
  topologically forced."*

## 한 줄 정직 평가
saddle FP 가 σ_cluster 위치에 자연스럽게 정렬한다는 증거는 본 toy 스캔
에서 발견되지 않았으며, 비단조 dip 도 cubic FP 토폴로지의 기하적 필연이
아니라 (a,b,c) 자유도의 *허용 영역* 일 뿐이다.
