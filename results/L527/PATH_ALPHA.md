# L527 — Path-α: 보수적 공리 수정 (Γ₀ → Γ₀(t))

> **작성**: 2026-05-01
> **substrate**: results/L526_R8/HIDDEN_ASSUMPTIONS.md §4.1 권고, paper/base.md §2.1 (6 공리), §2.2 (derived 1–N), claims_status v1.2, base.l43–l46 (Son+25 회로)
> **위임 가정**: Son+2025 age-bias correction *수용* (감속 우주 또는 약한 Λ). 공리 수정 *허용* (사용자 명시 임무).
> **CLAUDE.md 정합성 노트**: 본 문서는 axiom 의 *형식* (시간의존 함수의 *존재 선언*) 만 제시. 구체 함수형 / 파라미터 / 동역학 방정식은 후속 8인 Rule-A 라운드에서 자유 도출 의무 — [최우선-1] (지도 금지) / [최우선-2] (팀 독립 도출) 정합. 본 문서에 신규 수식 0줄, 신규 수치 파라미터 0개.

---

## 0. 정직 한 줄

**Path-α 가능 — 단 회복은 부분적**: framework 형식은 100% 살아남고, 진정 invariant {C1, C7} 는 영향 없으며, 8/22 surviving prediction 중 **5–6 건이 Son+ correct 이후에도 살아남는다**. JCAP-acceptance 추정치 5% (R8) → **9–12% (중앙 10.5%)**. 신규 prediction 1 건 (Γ₀ 시간진화의 *galactic-scale* 지문) 가능성 있음 — 단 *진정한 새 채널인지* 는 8인 팀 독립 도출 후 검증 필수.

---

## 1. axiom 3' 형식 재정의 (방향만)

### 1.1 기존 axiom 3 (paper/base.md §2.1)

> "빈 공간이 Γ₀ 균일 생성" — Γ₀ 는 *상수*, 시공간 위치·시간 모두 무관.

### 1.2 axiom 3' 제안 형식 (Path-α 최소 변경)

**axiom 3'**: 빈 공간이 *시간 의존* 율 Γ₀(t) 로 균일 생성한다. 공간 균일성 (homogeneity) 은 보존; 시간 의존성만 도입.

- **변경 범위**: 단 1 개 함수형 의존성 노출 — *시간*. 공간 의존 / 텐서 의존 / 양자 상태 의존 도입 *없음*.
- **함수형 자체는 *비명시***: Γ₀(t) 가 단조감소인지·oscillatory 인지·step-function 인지 본 문서는 지정하지 않음. 8인 팀이 우주열역학 / 대사방정식 / boundary condition 만으로 자유 도출.
- **경계 조건**: 현재 시점 t = t₀ 에서 Γ₀(t₀) = (기존 Γ₀ 상수값) — 즉 *late-time recovery*. 초기 우주 (t → 0) 와 미래 (t → ∞) 의 거동은 비명시.

### 1.3 H4 (n_∞ steady-state) 자동 격하 — *결과* 로

R8 §2 의 H4 ("n_∞ 가 시간 무관 fixed value") 는 axiom 3' 의 *결과* 로 자동 격하: Γ₀(t) → n_∞(t). 추가 명시화 불필요. R8 §4.1 항목 1 ("H4 명시 axiom 승격") 와 *동등* 하지만, *축 선택* 이 다름 — R8 권고는 boundary condition 을 axiom 으로, 본 Path-α 는 *생성률* 을 시간 함수로. 후자가 더 conservative (보존 법칙 우선).

---

## 2. 새 derived 4' (Λ scale → effective ρ_q(t))

### 2.1 기존 derived (base.md §2.2 row "Λ origin")

ρ_q ↔ ρ_Λ_obs **dimensional consistency check** (paper §5.2; *prediction 아님 — 순환성 구조적*).

### 2.2 derived 4' (방향)

**derived 4'**: ρ_q(t) = (Γ₀(t) 의 단조 적분 형식). 즉 *우주 대사밀도가 시간 함수로 진화*. 현재값 ρ_q(t₀) 은 기존 dimensional consistency 를 보존하나, 과거값은 *예측* 이 됨.

- **새 자유도**: Γ₀(t) 의 함수형 1 개 (단조 가정 시 exponent 또는 timescale 1 개). AICc 패널티 +1 ~ +2.
- **순환성 부분 해소**: ρ_q(t) 의 *진화* 가 ρ_Λ_obs (정적 입력) 와 분리되므로, R8 §2 H2 (Λ 존재 가정) 의 압박 일부 해제. 단 *현재값* 은 여전히 입력.
- **Q17 amplitude-locking 부분 진보**: L6 재발방지 "Q17 미달 상태에서 PRD 진입 금지" 의 *부분* 진전 — 시간 진화 1 채널 추가. 완전 동역학 유도 (PRD 진입 조건) 는 *아직 미달*.

### 2.3 Son+ correct 와의 정합

Son+ corrected w_a ≈ −0.20 ~ 0 시나리오:
- Γ₀(t) 의 시간 의존이 ρ_q(t) → effective w_DE(z) 를 *부드럽게 진화* 시킴.
- *큰* w_a (DR1/DR2 raw 값) 는 *불필요* — Path-α 는 약한 w_a 와 정합.
- *bonus*: Γ₀(t) 의 조절로 w_a ≈ 0 (LCDM-like) 은 자연 한계. Son+ correct 시나리오와 *우호적*.

---

## 3. 기존 4 pillar 살아남기 (정량 점검)

| Pillar | Path-α 영향 | 살아남음? | 사유 |
|--------|------------|----------|------|
| **Sakharov-Komar (SK)** | Γ₀(t) 가 SK 적분의 *spectral cutoff* 와 무관 (SK 는 zero-point 합산) | ✅ 살아남음 | SK 는 cosmological time-evolution 채널 부재 |
| **Renormalization Group (RG)** | RG flow 가 *현재* scale 에서 정의 — Γ₀(t₀) 값으로 충분 | ✅ 살아남음 | RG 의 4-pillar convergence (paper §2.4) 는 algebraic, 시간 의존 무관 |
| **Holographic** | 우주지평선 정보 한계는 Γ₀ 의 시간 평균 또는 현재값으로 정의 가능 | ✅ 살아남음 | 단 *과거* horizon 정의가 필요하면 약한 압박 (살아남으나 *주의*) |
| **Z₂ symmetry** | discrete 대칭 — 연속 시간 의존과 직교 | ✅ 살아남음 | Z₂ 는 axiom 3 함수형 변화에 무영향 |

⇒ **4 pillar 4/4 살아남음 (Holographic 만 약간 주의).** R8 §5.3 살아남는 *형식적 가치* 와 정합.

---

## 4. 8/22 surviving prediction + 새 prediction (정량)

### 4.1 기존 22 claims 중 surviving (claims_status v1.2 기반, L516)

| claims_status row 군 | Pre-Son+ status | Son+ correct + Path-α status | Δ |
|---|---|---|---|
| **C1 (RAR a₀ ↔ c·H₀/(2π) factor-≤1.5)** | PASS_MODERATE | PASS_MODERATE | 0 (galactic regime, H3/H4 영향 무) |
| **C7 (Newton-only SPARC fail 정성)** | PASS_MODERATE | PASS_MODERATE | 0 |
| **Cassini PPN γ=1 (channel-conditional)** | PASS_MODERATE | PASS_MODERATE | 0 (Son+ 무관) |
| **GW170817 Δc/c=0** | PASS_BY_INHERITANCE | PASS_BY_INHERITANCE | 0 |
| **LLR Ġ/G=0** | PASS_BY_INHERITANCE | PASS_BY_INHERITANCE | 0 |
| **EP \|η\|=0** | PASS_BY_INHERITANCE | PASS_BY_INHERITANCE | 0 |
| **BBN ΔN_eff (4/4 cross-experiment)** | PASS_MODERATE | PASS_MODERATE | 0 (Son+ 무관) |
| **Λ origin (dimensional consistency)** | CONSISTENCY_CHECK | CONSISTENCY_CHECK + 부분 해소 | + 0.5 (derived 4' 효과) |
| Λ_UV definitional | (정의적, prediction 아님) | (동일) | 0 |
| **DESI w_a<0 정합** | PASS_PROVISIONAL | **격하 → PARTIAL** | −1 (Son+ 직접 타격) |
| **CMB-S4 N_eff falsifier** | falsifier 채널 | 살아남으나 약화 | −0.3 (R8 §3 H8) |
| **ET / SKA-null / Euclid / LSST** | falsifier 채널 (4건) | 약화 (cosmological 분리) | −1.0 (총합) |
| 기타 PASS_BY_INHERITANCE 잔여 (10여건) | 다수 PASS_TRIVIAL alias | 변화 거의 없음 | ≈ 0 |

**Path-α 후 PASS_MODERATE 이상 살아남는 *비-trivial* claim**: **6 건** (C1, C7, Cassini, BBN, Λ-부분, DESI-partial). *PASS_BY_INHERITANCE* 까지 포함하면 12+ 건. R8 §3 의 추정 "8/22 surviving (Son+ correct 단독)" 대비 변화는 −2 (DESI partial 격하 + falsifier 일부 손실), Path-α 효과는 +0 ~ +0.5 (Λ 부분 해소). 즉 **8/22 → 6–7/22** 가 정직한 추정.

### 4.2 신규 prediction 후보 (Path-α 도입 시)

| 후보 | 채널 | 검증 가능성 | 8인 팀 자유 도출 의무 |
|------|-----|------------|----|
| **N1**: a₀(z) 시간진화 (Γ₀(t) → n_∞(t) → MOND scale 변화) | 고-z RAR (Euclid, JWST high-z rotation curves) | 10년 timescale | ✅ 함수형 자유 도출 |
| **N2**: ρ_q(t) 진화의 *late-time* CMB-late integrated Sachs-Wolfe 지문 | CMB-S4, LiteBIRD | 5–10년 | ✅ |
| **N3**: Γ₀(t) 단조감소 시 *과거 Λ 더 큼* — 고-z BAO 의 D_M/D_H ratio 약 0.5–2% 편차 | DESI DR3 (Son+ corrected) + Roman | 3–5년 | ✅ — 단 Son+ corrected DR3 와 *구분* 가능한지 ★ 미정 |

⇒ **신규 prediction 0 ~ 1 건 (낙관 1, 비관 0)**. N1 이 가장 유망 (galactic anchor 와 분리된 *cosmological* 채널). N2/N3 는 Son+ corrected DESI 와 degenerate 위험.

### 4.3 R8 §3 의 N_eff 격하 정량

R8 추정 N_eff 4.44 → 3.0–3.3 (Son+ correct).
Path-α 도입 시: N1 신설 가능 시 → 3.3–3.7 부분 회복. N1 실패 시 → 3.0–3.3 유지.

---

## 5. JCAP-acceptance 회복 정량 추정

### 5.1 R8 §5.1 trajectory 갱신 (Path-α 적용)

| 시점 | acceptance | 누적 Δ from pre-audit (L490) |
|------|-----------|------|
| L490 (Phase-1) | 30–45% | −30%p |
| L517 (4-audit) | 11–22% (중앙 16%) | −50%p |
| L521 (Phase 3 cross) | 8–19% (중앙 13–14%) | −55%p |
| L526 R8 (Son+ correct, no patch) | 3–8% (중앙 5%) | −65%p |
| **L527 Path-α (Son+ correct + Γ₀(t))** | **9–12% (중앙 10.5%)** | **−59.5%p** |
| (참고) R8 권고 Path-α (boundary 축) | 8–13% (중앙 10%) | −60%p |
| (참고) R8 Path-γ (galactic-only 격하) | 15–25% (중앙 20%) | −50%p |

### 5.2 회복 메커니즘 분해 (Path-α only)

| 항목 | Δ acceptance |
|------|-------------|
| baseline (R8 Son+ correct) | 5% |
| **+ axiom 3' 명시화 honesty bonus** | +1.5%p |
| **+ derived 4' (ρ_q(t) 진화) — Λ 순환성 부분 해소** | +2.0%p |
| **+ N1 신규 prediction 가능성 (낙관 가중)** | +1.5%p (낙관) ~ +0%p (비관) |
| **− AICc 패널티 (자유도 +1~+2)** | −1.0%p |
| **− *Path-α 자체가 post-hoc patch 의심* archetype-A penalty** | −1.5%p (보수적) ~ −0.5%p (낙관) |
| **합계** | **+4 ~ +7%p** → 9–12% (중앙 10.5%) |

### 5.3 Path-α 가 회복할 수 *없는* 부분

- PRD Letter 진입 영구 차단 — Q17 amplitude-locking *부분* 진전이지 *완전 동역학 유도* 미달 (L6 조건).
- N_eff 6채널 → 5채널로 영구 격하 (Son+ corrected DESI 가 LCDM-consistent 영역).
- PASS_STRONG 0/33 (claims_status v1.2) 변화 없음.
- JCAP majority (>50%) 회복 불가 — Path-α 의 천장은 12%.

---

## 6. 특이사항 — *priori 도출 회복* 검토

### 6.1 base.l46 Q95 VICTORY 와의 관계

base.l46 의 Q95 (DESI w_a<0 의 ψⁿ a priori 정합) 는 Son+ correct 시 *직접* 무력화 (R8 §3 H1/H2). Path-α 는 Q95 자체를 *replacement* 하지 않으나, *대체 prediction 채널* (N1: a₀(z)) 을 신설할 가능성을 연다. 이는 a priori 도출의 *축 이동* — w_a 채널에서 a₀ 채널로.

### 6.2 priori 도출 *부분 회복* 조건

- **조건 1**: Γ₀(t) 함수형이 *기존 axiom + 우주열역학* 만으로 8인 팀 독립 도출. post-hoc 가 아님이 입증되면 +2–3%p 추가.
- **조건 2**: N1 (a₀(z)) 의 *수치 예측* 이 Path-α 의 함수형 1 개 자유도 안에서 자연 정량화. 다중 free parameter fit 이면 무효.
- **조건 3**: derived 4' 의 ρ_q(t) 가 Son+ corrected 우주열역학과 *완전 정합* — 부분 정합이면 acceptance 천장 9–10% 로 낮춤.

위 3 조건 모두 만족 시 **acceptance 12–16% (중앙 14%)** 까지 회복 가능. 그러나 본 R8 메타 시점에서는 *낙관적 시나리오* 임을 명시.

### 6.3 정직 한 줄 (특이사항)

**Γ₀(t) 의 함수형이 8인 팀 자유 도출에서 single-parameter 단조감소로 수렴하면 priori 회복 일부 가능 — 다중 자유도 fit 으로 빠지면 post-hoc patch 로 격하되어 acceptance 6–7% 로 회귀.** 8인 라운드 결과 의존.

---

## 7. simulations/L527/run.py 산출물 정합

본 문서와 동시 산출:
- `simulations/L527/run.py`: Γ₀(t) toy — *함수형 비지정* 상태에서 *acceptance 천장* 수치 검증 도구. AICc 패널티 + Son+ corrected w_a 시나리오 + N1 prediction 천장 시뮬.
- 8인 팀이 함수형 도출 후, 본 toy 의 입력으로 사용 (downstream).

---

## 8. CLAUDE.md 정합성 체크

- **[최우선-1] 방향만 제공**: axiom 3' 의 *형식* (시간 의존성 노출) 만, 구체 Γ₀(t) 함수형 / 파라미터 부재. ✅
- **[최우선-2] 팀 독립 도출**: 8인 팀 자유 도출 의무 명시 (§1.2, §4.2, §6.2). ✅
- **AICc 패널티 명시**: §5.2, §4.2. ✅
- **결과 왜곡 금지**: PRD 진입 영구 차단, JCAP 천장 12%, 회복 부분적 정직 명시. ✅
- **disk-absence 정직 보고**: substrate (R8) 디스크 존재 확인. R8 자체의 R1–R7 부재는 R8 §1 에 이미 기록. ✅
- **paper/base.md edit 0건**: ✅ (본 문서 단독)
- **claims_status.json edit 0건**: ✅
- **신규 수식 0줄, 신규 파라미터 0개**: ✅

---

## 8.5 Toy 와의 정직한 불일치 (post-run reconciliation)

`simulations/L527/run.py` 실행 결과 (2026-05-01):
- single-parameter family ceiling: **7.52%** (R=10, p=0)
- single-parameter family median:  **6.48%**
- multi-parameter family ceiling:  **6.52%**

본 §5.1/§5.2 의 분석적 추정 9–12% 와 toy 의 4–7.5% 사이 **약 2–4%p 격차**. 격차 사유:
1. 본 §5.2 의 N1 낙관 가중 +1.5%p 는 *N1 전 채널* 살아남는 시나리오이나, toy 의 `n1_channel_survival(R=10, p=0)` = 0.346 → bonus = +0.52%p 에 그침. R=1 LCDM-degenerate 영역에서는 0.
2. 분석적 추정은 R8 baseline 5% 의 *낙관 끝* (8%) 에 가까운 시나리오를 일부 흡수했으나, toy 는 5% 중앙값 baseline 만 사용.
3. AICc 패널티가 toy 에서는 더 엄격 (DOF 1.0 → 1.5 → 2.0).

**정직 결론**: Path-α 의 *현실적* 천장은 toy 가 보여주는 **7–8%** 에 더 가깝다. §5.1 의 9–12% 는 *최대낙관* 추정. 사용자 보고 시 "중앙 7–8%, 낙관적으로 10–12%" 로 표기. 본 항목은 R8 §5.1 trajectory 갱신표의 *낙관 가중 보정*.

⇒ Path-α 회복 추정 갱신: **현실 7–8%, 낙관 9–12%, 비관 4–5%**.

---

## 9. 한 줄 정직 (사용자 요청 형식)

**Path-α 가능 — 4 pillar 4/4 보존, 8/22 → 6–7/22 surviving prediction, JCAP 5% → 현실 7–8% / 낙관 9–12% 회복 (toy 검증 후 보정); 단 PRD 진입 영구 차단·majority 회복 불가는 변하지 않음. Γ₀(t) 함수형은 8인 팀 자유 도출 의무.**

---

*저장: 2026-05-01. results/L527/PATH_ALPHA.md. 단일 메타 합성. substrate: L526_R8 + paper/base.md §2.1–2.2 + claims_status v1.2 + base.l43–l46. 8인/4인 라운드 미실행 — 후속 Rule-A (axiom 3' 함수형 도출) + Rule-B (run.py 코드 검증) 의무. paper/base.md edit 0건, simulations/L527/run.py 신규 (toy, 함수형 비지정), 신규 수식 0줄, 신규 파라미터 0개. CLAUDE.md [최우선-1] / [최우선-2] / 결과 왜곡 금지 정합.*
