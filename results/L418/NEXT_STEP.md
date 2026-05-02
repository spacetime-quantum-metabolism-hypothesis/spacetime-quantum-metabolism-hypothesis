# L418 — NEXT_STEP (8인팀 다음 단계 설계)

> **CLAUDE.md 최우선-1·-2 준수**: 본 문서는 *방향*과 *물리 현상의 이름*과 *수학 분야의 이름* 만 제공.
> 8인팀이 SQT axiom 으로부터 μ-distortion 을 *자율 도출* 한다.
> 수식·파라미터·유도 경로 힌트 *금지*. ATTACK_DESIGN 의 verdict 가 통과(또는 부분 통과)한 항목만 본 단계 진행.

## 임무
SQT framework 안에서 μ-distortion 의 *동역학적* 도출 사슬을 닫는다. base.md §4.3 의 1.02×10⁻⁸ 라는 표제값이 σ₀·n_∞·ε 만으로 닫히는지(또는 추가 입력 필요한지) *명시* 하고, 닫힌다면 어느 산술 의존성에서 닫히는지 PASS_STRONG / PASS_IDENTITY 분류 보고.

## 단계 (i, ii, iii)

### (i) Photon 에너지 흡수율 estimation — *방향만*
- 관련 물리: 흡수 sink Q (axiom 3 흡수항), photon 자유도와의 결합 채널, dark-only embedding (§4.1 EP) 의 photon-차단 여부, conformal-only Lagrangian 형태 (§4.1 GW170817).
- 관련 수학: open-system 형식 (Schwinger-Keldysh, 본 framework derived 1), KMS 균형 (axiom 6), 비가역 entropy 흐름.
- 공격 핵심: photon 채널이 *닫혀 있는지(→ μ ≡ 0 구조)* vs *열려 있는지(→ μ ≠ 0 가능)* 부터 결정. 닫혀 있다면 1.02e-8 은 표제 오도.

### (ii) z = 10⁵–10⁶ 에서의 σ₀ effective 계산 — *방향만*
- 관련 물리: μ-window redshift band (Sunyaev-Zeldovich 1970, Hu-Silk 1993 영역), 이 시기 SQT 의 σ₀(z) regime 분류 (cosmic vs cluster vs galactic 중 어느 regime 인가), redshift dependence 가 axiom 에서 강제되는가 vs anchor-fit 인가.
- 관련 수학: regime-transition 함수형, 비단조 σ₀(z) (§6.2 postdiction caveat), 차원분석.
- 공격 핵심: σ₀(z=10⁵–10⁶) 가 "추가 anchor" 없이 σ₀(z=0)·n_∞·ε 와 *우주론 expansion* 만으로 결정되는가? Anchor 추가 필요시 PASS_IDENTITY 카테고리.

### (iii) Compton y vs μ 비
- 관련 물리: 두 분포 왜곡 type 의 redshift 분기 (Sunyaev-Zeldovich), 열화 timescale (Compton-y → kinetic 평형 → μ 누적), kSZ/tSZ 와의 분리.
- 관련 수학: photon Boltzmann kinetic eq, distortion mode 분해 (μ, y, residual r-type — Chluba-Sunyaev 2012 분류 *이름만*), Bose-Einstein chemical potential.
- 공격 핵심: SQT 가 μ-channel 과 y-channel 중 어느 쪽으로 에너지를 흘리는지 *axiom 에서* 결정되는가? 결정 못하면 1.02e-8 은 임의 분기 선택의 부산물.

## 4인팀 코드리뷰 팀에 넘기는 정량 task (simulations/L418/run.py)
다음 *수치* 만 4인팀이 자율 분담으로 산출:
- (Q1) σ₀, n_∞, ε 표준값에서 Q (sink rate) 단위·차원 산출.
- (Q2) μ-window 적분 영역에서 ΛCDM standard μ baseline (Chluba 2016 ≈ 2×10⁻⁸ 인용) 과 비교.
- (Q3) PIXIE noise σ_μ ≈ 1×10⁻⁹ 가정에서 SQT *추가분* Δμ_SQT 의 SNR 곡선.
- (Q4) galactic dust + CIB foreground monopole 차감 후 잔차에서 1.02e-8 검출 가능성 (component separation 가정 — 단순 ILC 한계 5×10⁻⁹ 사용).
- (Q5) y/μ 비가 SQT 도출 사슬에서 강제되는지 *수치적* 확인 (강제되지 않으면 free parameter 로 NaN 보고).

## 결정 트리 (NEXT_STEP 종료 조건)
- (i),(ii),(iii) 모두 axiom 으로 닫힘 + (Q1–Q5) 모두 OK → **PASS_STRONG 후보**, base.md §4.1 표 수정 권고.
- 일부만 닫힘 → **PARTIAL 유지**, base.md §4.3 에 caveat 한 줄 추가 권고.
- 닫힘 실패 또는 photon 채널 차단 확인 → **PENDING 또는 NOT_INHERITED**, base.md §4.3 표제값 격하 권고.
- (Q5) y/μ 비 NaN → falsifier 부호 임의 선택 노출, falsifier 자격 박탈.

## 사전 등록 권고
DESI DR3 (§4.7) 와 동일 패턴으로, μ-distortion falsifier 도 PIXIE/BISOU 발사 *전* OSF 사전등록 + GitHub release tag.
