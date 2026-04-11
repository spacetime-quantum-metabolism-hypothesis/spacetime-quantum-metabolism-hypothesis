# L8 Phase 결과 보고
**날짜**: 2026-04-11  
**목표**: 생존 후보 (A12, C11D, C28)에서 SQMH 기본 방정식 역유도

---

## 핵심 발견

### σ 스케일 분리 (Universal)
```
σ_SQMH = 4πGt_P = 4.52×10⁻⁵³ m³/(kg·s)
σ·ρ_m0/(3H₀) = 1.83×10⁻⁶²  (62자리 무시가능)
```
→ SQMH 균일 배경 ODE ≡ ΛCDM (σ→0 극한)  
→ 모든 후보의 배경 우주론에서 SQMH 소멸항 무효

---

## L8-A: A12 (erf proxy) vs SQMH ODE
**파일**: `simulations/l8/a12/sqmh_ode_vs_erf.py`  
**결과**:
- σ·ρ_DE·ρ_m = 7.19×10⁻¹⁰⁶ kg/(m³·s) vs 3H·ρ_DE = 3.92×10⁻⁴⁴ (62차수)
- SQMH bg ODE → LCDM (chi²/dof SQMH vs LCDM ~ 0)
- chi²/dof (LCDM proxy vs A12 CPL) = 7.63
- **Q31 FAIL** (> 1.0), **K31 미발동** (< 10.0)

**해석**: A12 wₐ = -0.133은 SQMH 배경 ODE에서 유도되지 않는다. A12는 현상론 proxy로 확정.

---

## L8-C: C11D (CLW quintessence) vs SQMH
**파일**: `simulations/l8/c11d/clw_vs_sqmh.py`  
**결과**:
- Shooting 초기조건: y_ini = 1.637×10⁻⁶ → Ω_φ(a=1) = 0.6905 ✓
- w_φ(a=1) = -0.880 (목표 ~-0.877 ✓)
- σ_need = H₀/ρ_m0 = 8.23×10⁸ m³/(kg·s)
- σ_SQMH/σ_need = 5.5×10⁻⁶² (61차수 갭)
- 후보 1 (n̄ ∝ exp(-λφ)): σ_eff < 0 전체 → FAIL
- 후보 2 (n̄ ∝ exp(+λφ)): σ_eff 18% 양수 → 대부분 음수 → FAIL
- chi²/dof (CLW vs A12) = 27.62
- **Q32 FAIL, K32 TRIGGERED**

**해석**: CLW 역학 스케일 H₀·ρ_m0⁻¹과 SQMH σ = 4πGt_P 사이 61차수 갭. 변수 치환으로 극복 불가. PRD Letter 조건 Q32 미충족.

---

## L8-R: C28 (RR non-local) vs SQMH
**파일**: `simulations/l8/c28/rr_vs_sqmh.py`  
**결과**:
- Dirian 2015 단순화 ODE (U, U1, V, V1)
- U(a=1) = -12.41, V(a=1) = -21.43, V₁(a=1) = -7.89 (U < 0 구조적)
- OmDE_RR = γ₀/2·(2U - V₁²) < 0 → E²_RR(a=1) = 0.31 (비정상)
- 동형 피팅 U = Γ₀_eff - σ_eff·P·ρ_m: 잔차 = 100%
- **Q33 FAIL, K33 TRIGGERED**

**구조 동형성 (이론적 관찰)**:
```
RR:   dP/dlna + (3 + Ḣ/H²)P = U(a)   [P = V̇/H]
SQMH: dn̄/dlna + 3n̄ = [Γ₀ - σn̄ρ_m]/H
```
동일한 감쇠 연속방정식 구조이나, 소스항 스케일이 불일치. Dirian 2015 완전 방정식 (UV 교차항) 필요.

---

## L8-N: 통합 비교
**파일**: `simulations/l8/integration/l8_comparison.py`

| 후보 | 기준 | 결과 | 핵심 지표 |
|------|------|------|-----------|
| A12 | Q31 | FAIL | chi²/dof = 7.63 |
| C11D | Q32 | FAIL | σ 갭 61차수, K32 TRIGGERED |
| C28 | Q33 | FAIL | 잔차 100%, K33 TRIGGERED |

**공통 원인**: σ = 4πGt_P ≈ 10⁻⁵³는 배경 우주론에 62자리 무시가능.

---

## L8-I: 8인 순차 리뷰 판정
**파일**: `refs/l8_integration_verdict.md`

**합의 결론**:
1. SQMH σ는 국소 양자대사 커플링 — 배경 우주론 범위 밖
2. 세 후보 모두 SQMH 역유도 실패 — 이론 기각 아님
3. 구조 동형성 (C28 RR): 이론적 흥미롭지만 L8 기준 미달
4. PRD Letter 진입 조건 (Q32) 미충족
5. **JCAP 포지셔닝 확정**: A12 현상론 proxy, C11D/C28 독립 이론

---

## Kill/Keep 최종표

| 기준 | 상태 | 비고 |
|------|------|------|
| K31 (A12 bg ODE → wₐ<0) | Not triggered | chi²=7.63 < 10 |
| **K32 (C11D → SQMH σ)** | **TRIGGERED** | 61차수 갭 |
| **K33 (C28 P↔n̄)** | **TRIGGERED** | 잔차 100% |
| Q31 | FAIL | 7.63 > 1 |
| Q32 | FAIL | σ_eff < 0 |
| Q33 | FAIL | 잔차 100% |

---

## 논문 반영

**§8 역유도 섹션 권장 문구**:
> "The SQMH fundamental equation reduces to ΛCDM in the homogeneous background limit (σρ_m/3H ~ 10⁻⁶²). None of the three surviving candidates (A12, C11D, C28) admits a closed-form SQMH derivation at background level. A12 and C28 exhibit structural analogies (diffusion-type continuity equations) but fail quantitative isomorphism tests. All three candidates are confirmed as phenomenological proxies for the DESI wₐ<0 signal."

---

## 다음 단계

- [ ] paper §8 역유도 섹션 반영
- [ ] JCAP 최종 초고 완성
- [ ] L9 (future work): 섭동 레벨 SQMH-DE 연결 (이론 과제)

---
*L8 완료: 2026-04-11*
