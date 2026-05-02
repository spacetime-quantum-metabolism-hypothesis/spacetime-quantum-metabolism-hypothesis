# L313 ATTACK_DESIGN — Paper Section 3 (Branch B) Finalization

## 0. 컨텍스트
- 누적 213 loop, 등급 ~★★★★★ -0.05.
- Branch B: 3-regime σ — cosmic 10^8.37, cluster 10^7.75, galactic 10^9.56.
- 핵심 caveats: L272 mock-injection 100% false-detect, L281 marginalized ΔlnZ=0.8 (vs L196 fixed-θ 13).
- 영구 한계: anchors가 SPARC 내부가 아니라 regime-간 joint identification.

## 1. Section 3 목표 (8인 합의)
"3-regime σ 가설을 결정적 증거가 아니라 anchor-driven phenomenological structure 로 정직하게 제시하되, RG FP (L301) motivation 과 falsifiable forecast (P9/P11) 를 함께 묶어 reviewer 가 데이터-이론 거리감을 한 번에 파악할 수 있게 한다."

## 2. 8인 자율 분담 결과
- A (motivation): RG FP L301 → 3-regime 등장 자연스러움. "왜 단일 σ 가 아닌가" 단락 1.
- B (smooth alt): L195 smooth (tanh) 대안 제시. 단일 단락 + Δχ²/ΔAICc 표 1행.
- C (fitting result): σ 3값 + posterior 표. 정직히 "joint-identifying" 문구 1행 명시.
- D (LOO/CV): L276 leave-anchor-out ΔAICc 41–89 — 그러나 within-SPARC alone 은 X. caveat 단락.
- E (mock-injection): L272 false-detect 100% 결과를 결과 직후 즉시 제시 (숨기지 말 것).
- F (evidence): L281 marginalized ΔlnZ=0.8 명시, fixed-θ 13 과 분리 표기 (L6 재발방지 규칙).
- G (boundary/transition): regime boundary 가 sharp σ-step 인지 smooth crossover 인지 — 데이터로 결정 불가 명시.
- H (forecast): P9 dSph + P11 NS anchor 추가 시 σ_galactic / σ_cluster 분리 검증력 forecast.

## 3. 단락 구조 (최종 8 sub-section)
3.1 RG FP motivation (A) — 1단락.
3.2 3-regime 정의와 σ posterior (C) — 표 1, posterior corner Fig.
3.3 Mock-injection caveat (E) — 즉시 노출.
3.4 Smooth alternative + AICc 비교 (B).
3.5 LOO anchor robustness (D).
3.6 Marginalized evidence (F) — fixed-θ vs marginalized 분리표.
3.7 Regime boundary 미결정성 (G).
3.8 Future anchor expansion forecast (H).

## 4. 정직성 가드 (위반 시 섹션 reject)
- "detection" "evidence for 3-regime" 표현 금지. "phenomenological structure consistent with anchors" 만 허용.
- L196 fixed-θ ΔlnZ=13 단독 인용 금지 — 반드시 L281 marginalized 0.8 병기.
- "SPARC alone supports BB" 주장 금지. L273 GMM k=2 결과는 부분 지지로만 표기.
- mock-injection FDR 100% 를 footnote 로 강등 금지 — 본문 단락.

## 5. 산출물 체크리스트
- [ ] §3 LaTeX draft (8 sub-section).
- [ ] Table: σ posterior + 95% CI.
- [ ] Table: marginalized vs fixed-θ Δ ln Z.
- [ ] Fig: posterior corner.
- [ ] Fig: smooth-vs-step residual overlay.
- [ ] Forecast Table: P9/P11 추가 시 σ separability.

## 6. Open issue (다음 loop)
- §3.7 boundary 미결정성을 §4 (discussion) 로 이동할지 — 4인 코드리뷰에서 결정.
