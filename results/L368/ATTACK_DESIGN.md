# L368 — Sec 6 Limitations Table 14-row 확장 설계

**Loop**: L368 (독립)
**주제**: Sec 6 limitations table **12 → 14행** 확장
**상위 컨텍스트**: L341 SYNTHESIS_255 의 "영구 4 + 신규 6 + L332-L340 추가 2 = 12" 구조 위에, L342-L367 누적에서 부각된 신규 2행 추가
**원칙**: 정직 disclosure 우선. 격하 회피용 hedging 금지. 14행 모두 단일 표 안에 명시.

---

## 1. 기존 12행 (L341 확정)

### 영구 (4)
1. σ_8 structural +1.14% (background-only μ_eff≈1 한계)
2. H0 ~10% 부분 완화 only
3. n_s OOS (CMB primary 직접 예측 불가)
4. β-function full derivation (post-hoc anchored 영역 잔존)

### L322-L330 신규 6
5. 3-regime 강제성 약함 (L332 권고: 2-regime baseline)
6. Sloppy dim ≈ 1 (L333: cluster-dominant)
7. Theory-prior 부분만 (L334: pillar 4 ★★ 격하)
8. Cluster single-source A1689 (L335: 13-cluster plan, 미실측)
9. Subset Bayes factor (L336: 5-dataset full joint 미실행)
10. Micro 70-80% 상한 (L337: 5번째 pillar OPEN)

### L332-L340 추가 2
11. a4 emergent metric micro origin OPEN
12. P17 Tier B V(n,t) derivation gate 미완

---

## 2. 신규 추가 2행 (L368)

### Row 13. **Cosmic-shear / S_8 외부 채널 미검증**
- 배경 μ_eff≈1 구조 + L342-L367 누적에서 DES-Y3 / KiDS-1000 cosmic-shear 직접 fit 미수행.
- background-only 모델은 S_8 채널에서 LCDM 와 *구분 불가* — 정량 disclosure 필요.
- L5 K15 패턴 (background-only → S_8 tension 해결 불가) 의 영구 인정.

### Row 14. **DR3-class blinded validation 미수행**
- DESI DR3 / Euclid Q1 등 미공개 데이터에 대한 진정한 blind prediction 미실행.
- L332 P11 NS forecast 와 L338 P17 pre-registration 은 *plan 단계*.
- 현재 모든 fit 은 공개 데이터 대상 in-sample. OOS 진정성 입증 deferred.

---

## 3. 14-row 표 구조 (논문 Sec 6)

| # | Limitation | Status | Mitigation |
|---|-----------|--------|------------|
| 1 | σ_8 +1.14% | structural | background-only 한계, 영구 disclosure |
| 2 | H0 ~10% only | partial | full Boltzmann (Phase 6+) future |
| 3 | n_s OOS | structural | CMB primary 채널 미접근 |
| 4 | β-function full deriv | partial | post-hoc anchored, RG 1st principle 미완 |
| 5 | 3-regime 강제성 | downgraded | 2-regime baseline (L332) |
| 6 | Sloppy dim≈1 | acknowledged | cluster-dominant reparam (L333) |
| 7 | Theory-prior 부분만 | downgraded | pillar 4 ★★ (L334) |
| 8 | Cluster single A1689 | plan | 13-cluster archive (L335) |
| 9 | Subset Bayes factor | plan | 5-dataset MCMC 24-30hr (L336) |
| 10 | Micro 80% 상한 | acknowledged | 5번째 pillar OPEN (L337) |
| 11 | a4 emergent metric | OPEN | micro origin 미도출 |
| 12 | P17 Tier B V(n,t) gate | OPEN | derivation 미완 (L338) |
| 13 | **Cosmic-shear/S_8 외부 채널 미검증** | structural | background-only μ_eff≈1, future Phase 7 |
| 14 | **DR3-class blinded validation** | plan | OSF + arXiv timestamp pre-reg (L338 확장) |

---

## 4. 본 loop 산출물 명세

- ATTACK_DESIGN.md (본 문서): 14행 구성 + 신규 2행 정당화
- NEXT_STEP.md: 논문 Sec 6 본문 텍스트 초안 + 통합 체크리스트
- REVIEW.md: 8인 자율 분담 리뷰 (정직 disclosure 적정성)

---

## 5. 정직 원칙 위반 방지

- 신규 13/14 행은 *기존 격하* 의 재정리 아님 — L342-L367 누적에서 *별도로* 부각된 한계.
- "background-only structural" 표시는 영구 인정 (행 13). "future Phase X 해결" 식 hedging 금지.
- 행 14 의 "plan" 표시는 P17 pre-reg 와 *별개* 로 DR3-class 외부 데이터 진정성 강조.
