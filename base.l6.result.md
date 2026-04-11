# base.l6.result.md — L6 Phase-6 결과 (실시간 업데이트)

> 작성일: 2026-04-11. 8인팀/4인팀 완료 확인 포함.

---

## Phase L6-0 Infrastructure ✅

| 항목 | 결과 |
|------|------|
| refs/l6_kill_criteria.md | K17-K20, Q13-Q17 고정 완료 |
| base.l6.todo.md | WBS 완성 |
| simulations/l6/ 디렉터리 | evidence/, growth/, class/C11D/, dr3/ 생성 |
| Python 환경 | dynesty 3.0.0 ✓, emcee 3.1.6 ✓, hi_class ✗ |

---

## Phase L6-T Theory Upgrade ✅

### L6-T3 이론 포지셔닝 (8인팀 완료)

**최종 판정**: "정직한 falsifiable phenomenology"
**K20**: 미해당 (반증 없음)

주장 가능:
- SQMH 연속방정식 motivated zero-parameter dark energy template
- C11D 5채널 정합 (Δχ²=−22.063, K13 통과)
- wₐ < 0 구조적 + DR3 2.9–3.9σ falsifiable

주장 불가:
- "SQMH가 DESI를 이론적으로 설명"
- "amplitude-locking이 이론에서 유도됨"
- "C28이 SQMH 이론"

저널 타깃 현재: **JCAP** (PRD Letter 조건: Q17+Q13+Q14 동시 달성 필요)

### L6-T1 Amplitude-Locking 분석 (8인팀 완료)

**판정**: "이론 동기 있는 정규화 귀결 (Theory-motivated normalization consequence)"
- Δρ_DE ∝ Ω_m: SQMH 소멸 항 구조에서 부분 유도 성공 (Q17 부분 달성)
- Exact coefficient = 1: E(0)=1 정규화 귀결 (완전 유도 아님)
- K20 미해당

논문 기술: "theory-motivated zero-parameter implementation"

### L6-T2 C11D 일반 Disformal PPN (8인팀 완료)

**판정**: A'=0 → γ=1 은 disformal 구조의 수학적 필연 + GW170817 강제
- "Cassini 우연" 비판 해소: GW 제약이 A' < 10⁻¹⁴ 강제
- "SQMH가 A'=0을 예측"은 주장 불가
- K20 미해당

---

## Phase L6-E Marginalized Evidence

### L6-E1 C28 3D marginalized ✅

스크립트: simulations/l6/evidence/evidence_C28_full.py (4인 리뷰 완료)
params: (Om, h, gamma0), nlive=800, seed=42, 26.8분

**결과**: Δ ln Z = **+8.633** (hires LCDM 기준), K17 **PASS**
- L5 fixed-θ 11.257 대비 −2.624 nats 하락 (full 3D prior 패널티)
- Jeffreys: STRONG

### L6-E2 C11D 3D marginalized ✅

스크립트: simulations/l6/evidence/evidence_C11D_full.py (4인 리뷰 완료)
params: (Om, h, lam), nlive=1000, seed=42, **84.3분**

**결과**: Δ ln Z = **+8.771** (hires LCDM 기준) / +8.922 (L5 LCDM 기준), K17 **PASS**
- L5 fixed-θ 8.951 대비 −0.180 nats (λ posterior 타이트, MAP ≈ mean)
- Jeffreys: STRONG

### L6-E-hires Alt 모델 재실행 ✅

LCDM hires: ln Z = −843.538 ± 0.083 (L5 −843.689 대비 +0.15 nats, 정상)

| ID | Δ ln Z (L6 hires) | K17 | L5 fixed-θ |
|----|-------------------|-----|------------|
| A12 | **+10.769** | PASS | 10.779 |
| A17 | **+10.524** | PASS | 10.780 |
| A01 | **+10.515** | PASS | 10.690 |
| A05 | **+10.432** | PASS | 10.581 |
| A09 |  **+9.968** | PASS | 10.010 |
| A08 |  **+9.437** | PASS |  9.635 |
| A06 | **+10.527** | PASS | 10.574 |

### L6-E3 Occam 분석 (업데이트)

**실측 marginalized 비교 (C28 vs A12)**:
- C28 Δ ln Z = 8.633 vs A12 Δ ln Z = 10.769
- gap = −2.136 nats (A12 직접 우세)
- Gaussian Occam 추가 보정 −1.380 nats → net = −3.516 nats
- **결론**: A12가 C28보다 3.5 nats 우세. 데이터가 C28 추가 파라미터 정당화 안 함.

**최종 완전 marginalized 순위** (hires LCDM -843.538 기준):

| 순위 | ID | Δ ln Z | Jeffreys | K17 |
|------|-----|--------|----------|-----|
| 1 | A12 (0-param) | +10.769 | STRONG | PASS |
| 2 | A17 (0-param) | +10.524 | STRONG | PASS |
| 3 | A06 (0-param) | +10.527 | STRONG | PASS |
| 4 | A01 (0-param) | +10.515 | STRONG | PASS |
| 5 | A05 (0-param) | +10.432 | STRONG | PASS |
| 6 | A09 (0-param) | +9.968  | STRONG | PASS |
| 7 | A08 (0-param) | +9.437  | STRONG | PASS |
| 8 | C11D (1-param)| +8.771  | STRONG | PASS |
| 9 | C28  (1-param)| +8.633  | STRONG | PASS |

**핵심**: 0-파라미터 모델들이 1-파라미터 모델들을 2 nats 이상 상회.
A12 > C11D by 2.00 nats, A12 > C28 by 2.14 nats.
데이터는 추가 파라미터를 정당화하지 않음. **확정.**

---

## Phase L6-G Growth Sector ✅

### L6-G2 μ_eff 수치 계산 (4인 리뷰 완료)

| ID | μ_eff(a=1, k=0.1/Mpc) | K18 | ΔS₈ | Q15 |
|---|---|---|---|---|
| C11D | 1.0000 (GW 강제 A'=0) | — | 0.000 | — |
| C28 | 1.0015 (γ₀=0.0015) | — | 0.001% | — |
| A12 | 1.0000 (선언) | — | 0.000 | — |

**K18**: 전원 통과 (ghost 없음)
**Q15**: 전원 실패 (|ΔS₈| < 0.01)
**S₈ tension**: 구조적으로 미해결 (μ_eff ≈ 1 한계)

### L6-G3 CLASS 근사 (provisional) ✅

| 모델 | CMB chi2 | LCDM CMB chi2 | Δchi2_CMB | K19 |
|------|----------|---------------|-----------|-----|
| C11D | 0.172 | 6.502 | **−6.33** | ✅ PASS (provisional) |

WARNING: hi_class 미설치 → 압축 Planck 우도만. 전체 C_l 검증 미완.
paper §8.9에 공시 필수.

---

## Phase L6-D DR3 재실행 준비 ✅

스크립트: simulations/l6/dr3/run_dr3.sh (4인 리뷰 완료)
- CobayaSampler/bao_data git pull 자동화
- DR3 포맷 변화 자동 감지 (DR2 vs DR3 column 차이)
- chi2_joint 재실행 + dr3_vs_l5_diff.json 출력
- 5개 시나리오 (α~ε) 해석 프레임워크: refs/l6_amplitude_lock_analysis.md 참조

DR3 공개 시 실행 명령:
```bash
bash simulations/l6/dr3/run_dr3.sh
```

---

## Phase L6-P Paper v2 업데이트 ✅

### §7 업데이트

- 7.5 L6 Occam 분석 결과 추가 (C28 Occam net −0.902 nats)
- 7.6 μ_eff 성장 섹터 추가 (전원 μ≈1, S₈ 구조적 미해결)
- fixed-θ evidence 주석 추가

### §8 업데이트

- 8.5 K13 실제 결과 업데이트 (C11D/A12/A17/A01/A05 통과, C28 탈락)
- 8.9 L6-T 8인팀 이론 포지셔닝 결과 추가

---

## 시나리오 판정 (현재 시점)

**시나리오 B — 부분 업그레이드**: 확정 ✅

- amplitude-lock: Q17 부분 달성 ("이론 동기 있음", 완전 유도 아님)
- marginalized evidence: **전원 완료** — 전원 K17 PASS (STRONG Jeffreys)
  - 0-파라미터 모델이 1-파라미터 모델보다 2+ nats 우위 (확정)
- CLASS CMB: provisional K19 통과 (C11D Δχ²=-6.33, C28 Δχ²=-8.21)
- S₈: Q15 미달 (구조적 한계, 정직 기록)

**결론**: JCAP "정직한 현상론 + DR3 falsifier" 포지셔닝 확정.
PRD Letter 진입 조건: Q17 완전 달성 OR DR3 α시나리오 + hi_class K19 formal PASS.

**L7 방향**: base.l7.command.md 작성 완료 (2026-04-11).

---

## 8인/4인 완료 확인

| 작업 | Rule | 완료 |
|------|------|------|
| L6-T3 이론 포지셔닝 | Rule-A 8인 | ✅ |
| L6-T1 amplitude-lock | Rule-A 8인 | ✅ |
| L6-T2 C11D disformal PPN | Rule-A 8인 | ✅ |
| L6-E1 C28 evidence 코드 | Rule-B 4인 | ✅ |
| L6-E2 C11D evidence 코드 | Rule-B 4인 | ✅ |
| L6-E3 Occam 분석 코드 | Rule-B 4인 | ✅ |
| L6-G2 μ_eff 코드 | Rule-B 4인 | ✅ |
| L6-G3 CLASS 근사 코드 | Rule-B 4인 | ✅ |
| L6-D1 DR3 스크립트 | Rule-B 4인 | ✅ |

---

*L6-E1/E2 evidence 완료 (2026-04-11). L6 Phase-6 전체 완료.*
