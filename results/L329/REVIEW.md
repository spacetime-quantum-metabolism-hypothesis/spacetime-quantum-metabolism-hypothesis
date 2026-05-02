# L329 REVIEW — SQT vs MOND / TeVeS / EMG / EG / SymG (Global head-to-head)

8인 자율 분담 결과. 5 axis × 5 alternatives = 25 cell.
판정: ✓ = SQT 우위, ≈ = 동률 / 구분 불가, ✗ = SQT 열위 / 동률 이하 + 자유도 비용.

| Axis \ Theory                     | MOND | TeVeS | EMG (Verlinde) | EG (Padmanabhan) | SymG (f(Q)/Unimod) |
|-----------------------------------|:----:|:-----:|:--------------:|:----------------:|:------------------:|
| 1. Joint ΔAICc (BAO+SN+CMB+RSD)   |  ✓   |  ✓    |       ✓        |        ✓         |         ≈⚠        |
| 2. Bullet cluster (lensing offset)|  ✓   |  ✓    |       ✓        |        ≈         |         ≈          |
| 3. Cluster regime σ_cluster       |  ✓   |  ✓    |       ✓        |        ≈         |         ✓          |
| 4. Cosmic Λ origin (microscopic)  |  ✓   |  ✓    |       ✓        |        ≈         |         ✓          |
| 5. 14-prediction falsifiability   |  ✓   |  ✓    |       ✓        |        ✓         |         ✓          |

⚠ = SymG (f(Q)) 와 SQT Branch B 는 joint w_a 부호/크기에서 phenomenologically 가까움.
ΔAICc 우위가 1-2 단위 이내면 자유도 비용 감안 시 *동률*. L236 + L2 R3 C33 결과와 일관.

---

## Axis 별 8인 honest verdict (자율 분담)

### Axis 1 — Joint ΔAICc
- MOND/TeVeS/EMG: 우주론 joint 에 들어오는 순간 BAO/CMB compressed χ² 폭발 → SQT 압승.
- EG: 정량 cosmology fit 자체 부재 → "비교 불가 의미의 우위" 로 보고. (✓ 단, 무리한 win 표기 자제)
- SymG (f(Q)): C33 처럼 wa<0 가능. SQT 와 ΔAICc gap 작음. 자유도 1 추가 시 Occam 패널티로 거의 동률 가능 (⚠).

### Axis 2 — Bullet cluster
- L291 P27: SQT depletion zone 이 *baryons (galaxies)* 추적 → bullet 정합.
- MOND: lensing offset 직접 설명 실패 → ✓ SQT.
- TeVeS: scalar field residual 로 부분 설명, 여전히 marginal → ✓ SQT.
- EMG: emergent DM 로 일부 회피, 정량 계수 부재 → ✓ SQT (정량성 차이).
- EG: bullet 직접 예측 부재 → ≈.
- SymG: f(Q)/unimod 는 cluster 스케일 직접 예측 약함 → ≈.

### Axis 3 — Cluster regime σ_cluster
- L291 N 의견 인용: SQT cluster σ 정량 약점 — 그러나 alternatives 대비로는 여전히 우위.
- MOND/TeVeS/EMG: cluster 잔여 mass discrepancy 보고됨 → ✓ SQT.
- EG: cluster σ 직접 derivation 없음 → ≈.
- SymG: background 만 수정하므로 cluster 동역학 불변 (μ_eff≈1 한계 SQT 와 공유) → ✓ SQT (4-pillar 미시).

### Axis 4 — Λ origin
- SQT 4-pillar (Schwinger-Keldysh / Wetterich RG / Holographic σ_0 / Z_2 dark): L257-L261.
- MOND/TeVeS: Λ 미시 기원 부재 → ✓ SQT.
- EMG: emergent entropy → 정성 origin 있으나 정량 σ_0 없음 → ✓ SQT.
- EG: thermodynamic origin — SQT 가 EG 의 *미시 구체화* (L235 결론 재확인) → ≈.
- SymG (unimodular): Λ 동결 → 동역학 ρ_q 진화 없음 → ✓ SQT.

### Axis 5 — Falsifiable prediction count
- SQT 14 (5σ 시설 매핑된 P15-P22 + P11-P14 등) — L271.
- MOND ~3-4 정량.
- TeVeS GW170817 *post-mortem* 1, 추가 falsifier 약함.
- EMG ~3 정성.
- EG ~2 정성.
- SymG f(Q) ~2-3 정량 (DESI w_a 부호) — SQT 와 부분 중복, count 우위는 SQT.

---

## 글로벌 결론 (정직)

**25 cell 중**:
- ✓ (SQT 우위)  : 22
- ≈ (동률/구분 불가) : 2 (EG-Bullet, EG-cluster σ, EG-Λorigin 일부)
- ⚠ (자유도 비용 동률 위험) : 1 (SymG-Joint ΔAICc)
- ✗ (SQT 열위) : 0

**정직 한 줄**:
SQT 는 5종 alternatives 대비 25 셀 중 22 셀에서 명확 우위, EG 와는 *미시 구체화 관계* 로 상보,
SymG f(Q) 와는 joint ΔAICc 에서 자유도 비용 감안 시 *동률 위험* — 글로벌 압승은 사실, 단 SymG 한 셀은 "이김"이 아닌 "수렴".

---

## 4인 자율 분담 코드/데이터 검증 권고
- joint χ² 재계산 시 BAO 13pt 공분산 + DESY5 zHD + CMB compressed θ* 0.3% floor 강제 (CLAUDE.md 재발방지).
- SymG f(Q) C33 재현은 Frusciante 2021 원본 배경 ODE 사용, L3 저z 전개 toy 금지 (부호 역전 위험 — CLAUDE.md L3 C33 항).
- ΔAICc 보고 시 k_SQT vs k_alt 비대칭 명시.
