# L328 — Bayes factor stability across data subsets

## 질문
ΔlnZ(BB vs LCDM) 가 어떤 데이터 subset 에서나 일관되는가 (global preference),
아니면 특정 subset 의 anchor leverage 가 만든 artifact 인가 (subset-specific)?

## 8인 공격 벡터
A1: SPARC-only marginalized ΔlnZ — Occam 후 BB 가 살아남나?
A2: SPARC + cluster anchor 만으로 ΔlnZ — single-anchor leverage.
A3: SPARC + galactic anchor (P3 등) — anchor 종류별 isolated lift.
A4: SPARC + cosmic anchor — 가장 큰 ΔAICc=89 의 marginalized 잔존량.
A5: 3 anchor 모두 (cluster + galactic + cosmic, no SPARC) — anchors-only 이론 구분력.
A6: Full joint (175 SPARC + 3 anchor) — L281 baseline +0.8 재현.
A7: ΔlnZ vs subset 크기 (N) — log N 스케일 (BIC penalty) 진단.
A8: Per-anchor leverage decomposition — ΔlnZ = Σ contribution_i ?

## 우선순위 Top 3
**A1** (SPARC-only): L276 ΔAICc=0 와 marginalized ΔlnZ 일치 확인 → BB 의 global 주장 falsifier.
**A6** (Full joint): L281 +0.8 baseline anchor.
**A8** (Per-anchor decomposition): subset-specificity 정량.

## 권고 (실행 시 디자인)
1. Laplace approximation 으로 각 subset 별 ln Z 계산 (L281 방식 재사용).
2. 동일 prior box: BB 3-param + LCDM equivalent 2-param baseline.
3. Subset 정의:
   - S0: SPARC only (175 pts, 3-out 와 동치)
   - S1: SPARC + cluster anchor
   - S2: SPARC + galactic anchor
   - S3: SPARC + cosmic anchor
   - S4: anchors only (3 pts)
   - S5: full joint (S0 + 3 anchors)
4. ΔlnZ_subset 분포가 Jeffreys scale 어디 (0.8 이상/이하/음수) 에 박히는지.
5. AICc 와 marginalized lnZ 의 subset-별 일치도 검증.

## 가설
- L276 1-out (anchor 하나 제거) ΔAICc 41-89 → ΔlnZ ≈ +0.5~+1.5 (Occam 후) 잔존.
- L276 3-out (SPARC only) ΔAICc=0 → marginalized ΔlnZ < 0 (BB 가 disfavored).
- 결론: subset-specific. anchor 가 거의 모든 evidence 를 만든다.
