# L420 NEXT_STEP — 8인팀 다음 단계 설계

**목표**: Λ_UV ≈ 18 MeV 를 SQMH axiom 또는 SM-내부 동역학에서 *priori 도출* 하는 경로 설계.
**제약** (CLAUDE.md 최우선-1): 구체적 수식/파라미터 값 사전 지시 금지. 방향만 제시.
**방법**: 8인 자율 토의 (Rule-A). 자연 분담된 도출 path 3개로 수렴.

---

## Path (i) — UV completion = Z₂ SSB scale 일치

**아이디어 방향**: paper/base.md L692 의 Z₂ SSB scale (η_Z₂) 와 Cassini scale (Λ_UV) 가
*같은 microscopic mass scale 의 두 표현* 인지 검증.

**탐색 keywords**:
- 스칼라장 Z₂ 모델의 Coleman-Weinberg radiative scale
- BBN bound η ≲ 10 MeV 와 Cassini-derived Λ_UV ≈ 18 MeV 의 ratio (≈ 2)
- O(1) loop factor 또는 vev/mass ratio 가 18/10 일치를 *prediction* 으로 변환할 수 있는지

**판정 기준**:
- η_Z₂ 와 Λ_UV 의 ratio 가 SQMH axiom (L0–L4) 에서 closed-form 으로 나오는가?
- 한쪽 scale 만 외부 입력이고 다른 쪽이 도출되면 axiom 1개 절약 → PASS_STRONG 강화.

## Path (ii) — RG flow 도출

**아이디어 방향**: 공간-BEC 응집체 axiom 의 effective Lagrangian 에서
β-function 의 IR fixed point 또는 dimensional transmutation scale 로서 Λ_UV 식별.

**탐색 keywords**:
- BEC mean-field action 의 Wilsonian RG
- Goldstone-mode coupling 의 IR running
- σ₀ 항등식 (paper §3) 에서 dimensional 분석으로 추출 가능한 single mass scale

**판정 기준**:
- M_Pl → Λ_UV 흐름이 SQMH lattice spacing 또는 μn₀ 결합에서 자연 출현하는가?
- 18 MeV 가 *coupling 임의 선택* 없이 나오는가? 손으로 g≈0.15 를 넣어야 하면 실패.

## Path (iii) — Holographic / IR-UV 혼합

**아이디어 방향**: AdS/CFT-like correspondence 또는 Cohen-Kaplan-Nelson 류
holographic bound 에서 (Λ_DE, M_Pl, H₀) 의 dimensional combination 으로 Λ_UV 출현 여부.

**탐색 keywords**:
- CKN bound: Λ_UV² × L_IR ~ M_Pl (L_IR = 1/H₀)
- 't Hooft anomaly matching scale
- Lambda_DE^a · M_Pl^b · H_0^c 의 (a+b+c=1) 조합에서 18 MeV 재현
- 사전 Python toy 결과: (Λ_DE² · M_Pl)^(1/3) ≈ 24.6 MeV 가 가장 근접 (factor 1.4)

**판정 기준**:
- holographic 조합이 SQMH axiom 의 *대사 평형* 조건에서 *유도* 되는지, 단순 dimensional fit 인지.
- O(1) 계수가 자연 발생하면 PASS_STRONG 격상 후보.

---

## 8인팀 합의 — 우선순위

1. **Path (i) 우선**: 이미 paper 에 등장한 두 scale (η_Z₂, Λ_UV) 의 일치 검증이 가장 economical.
2. **Path (iii) 차선**: holographic 조합 toy 가 factor-O(1) 까지 수렴하면 axiom 격상 후보.
3. **Path (ii) 후순위**: SQMH 에 EFT cutoff 구조 부재 → RG 도출은 framework 확장 요구.

**실패 시 정직 권고**: §6.1 row #13 caveat 을 다음 표현으로 강화.
> "Λ_UV ≈ 18 MeV 는 Cassini |γ-1| 관측에서 역산된 *effective scale* 이며,
> SQMH axiom L0–L4 에서 RG-유도되지 않는다. 따라서 Cassini PASS_STRONG 는
> *conditional pass* 이며 prediction 이 아닌 postdiction 으로 분류된다."
