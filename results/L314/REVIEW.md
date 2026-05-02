# L314 — 4인 코드/문서 리뷰

**대상**: ATTACK_DESIGN.md 및 Section 4 framing.
**4인**: 자율 분담 (역할 사전 지정 없음).

---

### R1. Inventory 정합성 검토
- A1의 "11 SQT-specific" 카운트는 L205 audit과 일치 확인 OK.
- 단, A1에서 P21/P22가 "Extension"으로 분류되었는데 본문 4.6에서 P21을 *primary 5σ falsifier*로 격상 — 분류 정합성 보강 필요. **권고**: P21을 Tier-S로 명시 추가 (이미 A2에 반영됨, OK).

### R2. σ_8 Disclosure 정직성 검토 — 핵심
- A5의 "SQT predicts σ_8≈0.83–0.84" 수치는 L286 결과와 일치. **회피 표현 없음 확인**.
- 그러나 본문 abstract/intro에서 σ_8 fail이 누락될 위험 있음 — **권고**: abstract에 "SQT does *not* alleviate the S_8 tension" 한 문장 명시.
- L6 Q15 인용은 적절. CLAUDE.md "mu_eff ≈ 1 은 S8 tension 해결 불가" 정합.

### R3. Bullet Cluster (P27) 주장 강도
- A4에서 "qualitative WIN vs MOND"로 표현 — 정직.
- 그러나 "natural offset" 표현이 *quantitative* 일치를 암시할 수 있음. **권고**: "offset의 부호와 order-of-magnitude는 SQT framework에서 자연스럽게 발생하나, weak-lensing peak amplitude의 정량 일치는 perturbation-level 후속 작업"으로 한정.
- L291 결과는 toy-level. Sec 4.3은 *plausibility argument*로 위치 명확화 필요.

### R4. Head-to-head Table 검토 (A3)
- P15 wₐ<0의 "~2.5σ 선호" 수치는 L48/L34 joint fit 결과 인용 — 출처 본문 cite 필수.
- P19 Δχ²-equiv = -0.6은 marginal — "선호" 표현 금지, "consistent" 사용 권고.
- **수정 필수**: "fσ_8 slight excess" 방향 — L286 데이터 재확인 필요. 만약 excess가 데이터 대비 *높은* 쪽이면 RSD에서도 SQT 약간 worse. honest framing 적용.

### R5. Falsifier Timeline (A7)
- DESI DR3 시점 "2026 Q4"는 공식 일정 기반 — OK. 단 CLAUDE.md L30~L33 재발방지 "DR3 공개 전 스크립트 실행 금지" 준수 확인 (본 loop는 framing만).
- LISA 2035, ELT 2040은 conservative — OK.
- **권고**: 각 시점에 "expected sensitivity to SQT signal"을 1-line으로 추가 (Fig 4.3 caption).

### R6. Tier 분류 일관성
- Tier-S 3개 (P19, P21, P15) 중 P19는 동시에 Tier-C(unfavorable)로 분류됨 — 한 prediction이 두 tier에 존재. **권고**: P19를 fσ_8 (Tier-S/marginal)와 S_8 (Tier-C/honest fail)로 *분리 명시*.

### R7. Risky vs Safe 정의
- "Risky"가 "near-term + decisive"로 정의되어 있으나 표준 용법 (high prior odds against)와 다름. **권고**: Sec 4.6 정의 box 추가, "risky = where SQT and LCDM diverge measurably within 5 yr".

### R8. Dropped Predictions (P23/P24, P12–P14)
- A1에서 P23/P24 drop 명시 OK. P12–P14를 부록으로 이전한다는 결정도 OK.
- **권고**: 본문에서 "P12–P14 are degenerate with LCDM at current data quality and shifted to Appendix B" 한 줄로 투명성 확보.

### R9. Figure Plan 검토
- Fig 4.1–4.4 plan 적절. Fig 4.2 (σ_8 정직 비교)가 가장 중요 — SQT가 LCDM보다 *위*에 위치하는 그림 명시 권고.
- Fig 4.4 Bullet schematic은 qualitative 표시 — caption에 "schematic, not to scale" 필수.

### R10. 최종 Go/No-Go
- **Go**: A1, A4 (Bullet 한정 표현 추가 후), A5 (abstract 반영 후), A7, A8.
- **수정 후 Go**: A2/A3 (P19 split), A4 (quantitative claim 한정), R7 (risky 정의).
- **Blocker 없음**: 본 ATTACK_DESIGN으로 Sec 4 초안 진행 가능. 4인 합의.
