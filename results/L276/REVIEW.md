# L276 — 4인 review (LOO CV)

시뮬: 3 anchors + 175 SPARC, 1-out and 2-out cross-validation.

## 결과 (analytic, simulations/L276/run.py)
- Leave-cosmic-out: ΔAICc(LCDM-BB) = 56 → 여전히 BB 우위
- Leave-cluster-out: ΔAICc = 89 → 거의 변화 없음 (cluster anchor 약함)
- Leave-galactic-out: ΔAICc = 41 → BB 우위 약화
- 2-out: ΔAICc 5-15 → 유의미 임계
- 3-out (all): SPARC alone, ΔAICc=0 (univeral) → BB 무의미

## 4인
- P: 1-out 에서 ΔAICc 41-89 유지 — robust.
- N: 2-out 에서 임계, 3-out 에서 collapse — anchors 의존성 정량 확인.
- O: 더 많은 anchors (P9 dSph, P11 NS) 추가 시 robustness 향상.
- H: L208 anchor caveat 와 *완전* 일관.

정직: BB 정당성 = anchors 다중성. SPARC alone 부족 (L187 finding 재확인).
