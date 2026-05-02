# L426 NEXT_STEP — 8인팀 다음 단계 설계

**목표**: SQT depletion-zone 의 c(M) 정량 prediction path 설계 + Diemer-Joyce / Ludlow profile 데이터 비교 준비.
**제약** (CLAUDE.md 최우선-1): 구체적 수식/파라미터 값 사전 지시 금지. 방향만.
**방법**: 8인 자율 토의 (Rule-A). 자연 분담된 path 3개로 수렴.

---

## Path (i) — depletion-zone scale → r_s 식별

**아이디어 방향**: SQT depletion-zone 의 *characteristic mass-dependent radius* 가
NFW scale radius r_s 와 *동일한 동역학 origin* 을 갖는지 검증.
isolated halo 의 turnaround radius 또는 splashback radius 가 depletion 경계와 일치하는지.

**탐색 keywords**:
- splashback radius (More-Diemer-Kravtsov 2015)
- secondary infall (Bertschinger 1985, Fillmore-Goldreich 1984) 와 depletion 의 유사성
- turnaround radius / depletion-zone outer edge 식별

**판정 기준**:
- depletion-zone 의 mass scaling 이 LCDM r_s(M) ∝ M^(1/3) / c(M) 와 일치 또는 차이.
- 차이가 ~5–10% 수준이면 distinguishing prediction 후보.
- 일치하면 "LCDM-equivalent" 결론, paper 에 명시.

## Path (ii) — modified σ(M) 채널

**아이디어 방향**: SQT 가 background H(z) 를 약간 수정한다면 (paper §4 dark-energy 항)
linear growth D(z) → σ(M, z) 가 미세 수정. peak height ν(M) = δ_c/σ(M,z) 가 mass-dependent shift.

**탐색 keywords**:
- σ_8(z) shift in modified-gravity scenarios
- ν → c mapping (Diemer-Kravtsov 2015 c=c(ν,n_eff))
- SQT background w(z) (L48 결과) 가 D(z) 에 미치는 영향

**판정 기준**:
- D(z) shift 가 σ(M, z=0) 를 ~1% 미만 수정 (LCDM 측정 정밀도 미만) 이면 c(M) 효과도 1% 미만 → 검출 불가.
- 1% 이상 shift 면 c(M) 5–10% 차이 가능, Diemer-Joyce 비교 의미 있음.

## Path (iii) — splashback / 1-halo boundary 효과

**아이디어 방향**: c(M) 의 *외부 boundary* (R_200m 정의, splashback) 에서 SQT depletion-zone 의
mass accretion rate (Γ) 영향. mainstream: c 는 Γ 와 anti-correlated (Diemer-Kravtsov 2014).

**탐색 keywords**:
- mass accretion rate Γ = d ln M / d ln a 의 SQT-체 prediction
- Γ → c (Diemer profile fitting)
- splashback radius 와 SQT depletion edge 의 일치 여부

**판정 기준**:
- SQT 가 Γ(M) 분포를 LCDM 와 구분 가능하게 수정하면 c(M) 차이 자동 발생.
- 그렇지 않으면 PASS_TRIVIAL.

---

## 8인팀 합의 — 우선순위

1. **Path (ii) 우선**: D(z) → σ(M,z) → c(ν) chain 은 *기존 SQT background 결과 (L48 H0 tension, w(z))* 를 직접 활용 가능.
2. **Path (iii) 차선**: splashback 채널은 1-halo boundary 와 SQT depletion edge 일치 검증 가능.
3. **Path (i) 후순위**: r_s 식별은 추가 axiom 요구 (depletion scale 정의), 비용 큼.

**4인팀 실행 task**:
- Diemer-Joyce 2019 Eq.(C1) 또는 Ludlow 2016 fitting formula 로 LCDM c(M) baseline 생성.
- SQT background H(z) (L48/L34 결과) 로 σ_8(z) 및 D(z) 재계산.
- ν(M, z=0) shift 추출, c(ν) mapping 으로 c_SQT(M) 예측.
- LCDM 대비 % 차이를 mass range M ∈ [10¹², 10¹⁵] M_sun 에서 plot.
- 관측 cluster c(M) (Umetsu+ 2020, Sereno+ 2017) 의 typical 0.1 dex scatter 와 비교.

**예상 결과** (사전 가설 아님, 단순 가능 시나리오):
- Δc/c ≲ 1% 면 PASS_TRIVIAL → caveat 추가.
- Δc/c ≈ 5% 면 future-distinguishing prediction → §5 예측 row 추가.
- Δc/c ≳ 10% 면 기존 관측과 충돌 위험 → SQT background 파라미터 재검토.
