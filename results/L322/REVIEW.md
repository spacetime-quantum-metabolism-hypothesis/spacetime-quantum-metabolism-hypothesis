# L322 — 4인 P/N/O/H Review

## 시뮬레이션 결과 (정직)

```
n_start = 100, n_success = 100
n_modes = 2
mode 0: sigma = (8.37, 7.75, 9.56), chi2 = -0.001, count = 97
mode 1: sigma = (9.47, 7.75, 8.46), chi2 = +3.90, count = 3
delta AICc (M3 - M2) = +0.77   (M2 merge marginally preferred)
```

L272 anchor-flex 가정을 인코딩한 합성 χ² 표면 위에서, 100개 시작점 중 97개가 정답 모드(8.37, 7.75, 9.56)에 수렴, 3개가 cosmic↔galactic permutation 부근의 secondary mode (Δχ² ≈ +3.9, 약 2σ) 에 수렴.

## P (Positive — 합격 근거)

- 단일 dominant mode 97% 점유 — global optimum 강하게 시사.
- Secondary mode 가 Δχ² ≈ +3.9 (2σ floor) 위 — 통계적으로 배제 가능 영역.
- Multi-start LBFGS-style 검색에서 spurious mode 폭주 없음.
- Cluster regime σ_clu = 7.75 두 모드에서 동일 — cluster anchor 는 잘 고정됨.

## N (Negative — 위험)

- **2-regime merge model 이 ΔAICc = +0.77 만큼 이김**. 3-regime 강제성 약함 — JCAP referee R3 (statistician) 가 직접 공격 가능.
- Secondary mode 가 정확히 cosmic↔galactic swap — anchor flexibility 가 permutation-symmetric 일 가능성. L272 false-detection 100% 와 정합.
- 합성 surface 사용 — real BAO+SN+CMB+RSD pipeline 미반영. 실제 데이터에서 mode 구조가 다를 수 있음.
- 100 start 는 3D 공간에서는 충분하지만, σ_0 prior 범위 [3, 15]^3 외부 mode 미탐색.

## O (Open — 불확실)

- ΔlnZ 와 ΔAICc 가 일관된가? L281 marginalized ΔlnZ = 0.8 vs 본 loop ΔAICc = -0.77 (M2-M3) — 부호 일치하지만 amplitude 비교 불완전 (서로 다른 모델 비교).
- Secondary mode 의 물리적 의미: cosmic↔galactic swap 이 RG fixed point 매핑 (L301) 위에서 dual 인가, 단순 anchor artifact 인가?
- dynesty multimodal full likelihood 결과는 다르게 나올 수 있음.

## H (Honest — 정직 보고)

- **글로벌 최적 단일성: 부분 입증**. 97% 점유는 강력하지만 secondary mode 존재는 사실. JCAP 논문 limitations 섹션에 추가 권고.
- **3-regime over-partition 우려**: ΔAICc = +0.77 (M2 vs M3) 은 통계적으로 미미하지만 부호가 M2 쪽. 데이터가 3-regime 을 강제하지 않음. L272 anchor flexibility 와 결합 시 더 큰 우려.
- **합성 surface 한계 명시**: 본 결과는 anchor-flex 인코딩한 toy. L323 dynesty multimodal full pipeline 으로 재확인 필수. 본 loop 결론은 "글로벌 단일성 제안적 증거 + 3-regime 약한 정당성".

## 권고 (다음 loop)

1. **L323**: dynesty (nlive=2000, sample='rslice', bound='multi') full likelihood ndim=3 σ_0. 실제 mode count 와 lnZ.
2. JCAP 논문에 "alternative cosmic↔galactic permutation mode at Δχ²≈4" 한 줄 추가 정직 기록.
3. 3-regime 강제성 약함 — 논문 6.4 limitations 에 "regime partition is phenomenological; 2-regime merge yields ΔAICc within ±1" 명시.
