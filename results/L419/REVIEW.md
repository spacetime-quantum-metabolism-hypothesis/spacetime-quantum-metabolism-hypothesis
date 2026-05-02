# L419 REVIEW — 4인팀 코드리뷰 + 결과 요약

**대상**: simulations/L419/run.py + results/L419/L419_quant.json + L419_scales.png
**규칙**: CLAUDE.md Rule-B (4인팀 자율 분담, 역할 사전 지정 금지). 본 REVIEW 는 자율 분담 결과를 통합 기록.

---

## 1. 코드 검증 (4인 자율 분담)

### V1 — Constants & units
- M_Pl (full) = 1.221e19 GeV, M_Pl (reduced) = 2.435e18 GeV — PDG 2024 일치.
- T_BBN = 0.1 MeV (deuterium bottleneck), T_BBN_max = 1 MeV (n/p freezeout) — Cyburt 2016 정합.
- Λ^{1/4} = 2.846e-3 eV — Planck 2018 best-fit 정합.
- 단위 일관성: 모든 에너지 eV. SI 변환 미사용 — cp949 안전, 유니코드 print 없음 ✓.
- **결론**: PASS.

### V2 — Boltzmann suppression formula
- 사용 공식: n_φ/n_rel ≈ (x/2π)^{3/2} exp(-x), x=m/T (non-rel approximation).
- 적용 영역: x>3 에서 유효. 본 sim x=10 (T_onset), x=100 (T_BBN) 모두 영역 내.
- 단점: pre-factor 계수가 *species-dependent*; 상세 BBN 코드 (PArthENoPE/AlterBBN) 의 정확값과 O(1) factor 차이 가능.
- **결론**: order-of-magnitude 수준에서 PASS. 정확 ΔN_eff 인용 시 BBN code linkage future work.

### V3 — Gamma/H ratio (mechanism B)
- 사용 공식: Γ ~ β_eff² × T_BBN, H ~ T²/M_Pl (radiation era).
- 한계: Gamma 의 phase space, log enhancement, particle multiplicity 누락 — O(10²) factor 가능.
- 보수성: simulation 결과 Γ/H = 6.7e-18 — 보수 추정으로도 << 1, freeze-in 영역 명확.
- 17 dex margin 의 robustness 는 O(10²) factor 누락에 영향 없음.
- **결론**: PASS.

### V4 — Candidate scale enumeration
- 11 후보 포함: cosmological, particle masses (e/π/μ), QCD scale, geometric means, see-saw, EW, GUT.
- 누락 후보: ChPT condensate <q̄q>^{1/3} ≈ 270 MeV (≈ Λ_QCD 와 redundant), dilaton f_a (free parameter), instanton density Λ_QCD × exp(-S) (모델 의존).
- √(m_e × Λ_QCD) ≈ 10.53 MeV: log10(ratio) = +0.022 — 0.02 dex 매치는 *후보* 이지 derivation 아님 (NEXT_STEP D1 명시).
- **결론**: 누락 후보 추가는 future. 현 enumeration 은 main candidate 포함.

---

## 2. 결과 요약 (4인팀 합의)

### F1 — β_eff reverse engineering
| Planck mass 정의 | Λ_UV 추정 | η_Z₂ 비 |
|------------------|-----------|---------|
| Full (1.221e19 GeV) | 90.4 MeV | 9.0× |
| Reduced (2.435e18 GeV) | 18.0 MeV | 1.8× |

**해석**: paper 의 β_eff = 7.4×10⁻²¹ 은 reduced M_Pl 사용 시 Λ_UV ≈ 18 MeV — η_Z₂ ≈ 10 MeV 와 동일 scale (factor 1.8). **Λ_UV ~ η_Z₂ identification 이 implicit**.

### F2 — Two-mechanism redundancy
| Mechanism | ΔN_eff 단독 상한 | Planck bound 대비 dex 여유 |
|-----------|------------------|-----------------------------|
| A — Boltzmann m/T | 5.2×10⁻⁵ | 3.5 dex |
| B — β_eff² portal | 3.8×10⁻¹⁸ | 17.4 dex |
| A × B 결합 | 3.5×10⁻²² | 21.4 dex |
| (paper 인용) | 10⁻⁴⁶ | 45.8 dex |

**해석**: B (portal) 단독으로 17.4 dex 여유 — A (Boltzmann) 가 추가로 13 dex 보너스. **두 mechanism 은 redundant**. paper 인용값 10⁻⁴⁶ 은 본 sim 의 dimensional 근사보다 24 dex 더 작음 — paper 가 추가 loop/phase-space suppression 적용한 것으로 추정 (정확 BBN code linkage future).

### F3 — η_Z₂ priori candidate
| 후보 SM scale | log10(value/η_Z₂) |
|---------------|-------------------|
| **√(m_e × Λ_QCD)** | **+0.022** ⭐ |
| m_μ | +1.024 |
| m_π | +1.146 |
| m_e | -1.291 |
| Λ_QCD | +1.337 |

**해석**: 기하 평균 √(m_e × Λ_QCD) ≈ 10.53 MeV 가 0.02 dex 내 일치. 단 *Lagrangian derivation* 이 아닌 *후보* 매치 — Foundation 4 의 priori 도출은 OPEN 유지.

---

## 3. 정직 한계 (4인 합의)

| # | 한계 | 영향 |
|---|------|------|
| L1 | dimensional 근사 (loop factor 누락) | O(10²) factor — 17 dex margin 무영향 |
| L2 | pre-factor species-dependent | O(1) — 정성 결론 무영향 |
| L3 | √(m_e × Λ_QCD) match 는 *후보 only* | derivation 으로 over-claim 금지 |
| L4 | paper 의 ΔN ≈ 10⁻⁴⁶ 와 본 sim 의 10⁻²² 차이 | 24 dex — 별도 BBN code re-derivation future |
| L5 | priori path enumeration 누락 후보 | ChPT, dilaton, instanton — 향후 보강 |

---

## 4. 코드리뷰 verdict (4인 합의)

- **PASS** — simulation 은 BBN PASS_STRONG 의 *structural robustness* (B-only 17 dex margin) 를 정량 확인.
- **권고**: NEXT_STEP D1–D5 를 paper 에 반영하기 전 8인팀 Rule-A 이론 리뷰 (claim level) 필수.
- **공유 권고**: paper §4.1 row 2 narrative 정정 (single-scale margin), §6.1 한계 row 추가 (η_Z₂ priori OPEN), §4.1 row 3 Λ_UV ~ η_Z₂ identification 명시.

---

## 5. 정직 한 줄

> BBN PASS_STRONG 는 단일-scale Λ_UV ≈ η_Z₂ ≈ 10 MeV 에서 portal coupling β_eff² 만으로 17 dex 통과. "두 보호 mechanism" narrative 는 redundancy 정정 필요. priori 도출은 √(m_e × Λ_QCD) 후보 외 OPEN.
