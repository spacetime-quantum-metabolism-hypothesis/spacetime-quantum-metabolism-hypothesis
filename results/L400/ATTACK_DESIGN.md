# L400 — Simulated Reviewer Final Response Template (R1/R2/R3)

**Loop**: L400 (independent)
**Target journal**: JCAP (with PRD Letter as fall-back if Q17 + Q13/Q14 conditions met)
**Submission**: SQMH/SQT paper, second-round revision
**Date**: 2026-05-01
**Predecessor**: L320 (first-round simulated referee response)
**정직 한 줄**: L320 이후 L342–L391 에서 새로 발견된 한계와 회복을 모두 incorporated 한 final-round response 템플릿이며, 새로 추가된 검증과 새로 노출된 약점을 함께 정직하게 반영한다.

---

## 0. Why a final-round template

L320 이 first-round (major-revision-grade) 응답을 만든 시점 이후, L342~L391 에서 다음과 같은 신규 발견·검증이 누적되었다. 이 attack design 은 final-round response 가 다뤄야 할 새 공격면과 새 회복면을 reviewer 별로 매핑한다.

## 1. L342–L391 incorporation map

### 1.1 신규 회복 (defense-strengthening)

| 세션 | 발견 | reviewer 채널 |
|------|------|---------------|
| L342 | σ_0(ρ_env) non-monotonicity 의 Bayes-factor 정량화 (3-anchor) | R3 (model selection) |
| L350 | PSZ2 cluster σ vs lensing-selected cluster σ 의 selection-bias 검증 설계 | R2 (observational systematics) |
| L360 | Q_DMAP cross-dataset tension (SPARC × DESI × Planck) 프로토콜 | R3 (statistics) + R2 (consistency) |
| L370 | Companion paper outline 으로 method/data 디테일 외부화 | 모든 reviewer (재현성) |
| L380 | V(n,t) thawing toy 의 DESI w0/wa 부호 검증 | R2 + R1 (배경 dynamics) |
| L385 | CKN holographic bound r(R_H) ≈ O(1) saturation 정량화 | R1 (theoretical embedding) |
| L388 | 2-loop n self-energy / setting-sun 구조 분석 | R1 (UV completion) |
| L389 | BRST diffeomorphism gauge invariance check | R1 (consistency) |
| L390 | Conformal anomaly T^μ_μ (n field) 평가 | R1 (theoretical control) |

### 1.2 신규 한계 (concession-required)

| 세션 | 한계 | reviewer 채널 |
|------|------|---------------|
| L342 | N=3 anchor 로 인한 AICc 정의 영역 끝 — 3-regime 모델 채택은 보수적으로 reserve | R3 |
| L350 (전망) | PSZ2 hydrostatic mass bias (1−b) 가 σ_cluster 추정에 잔존 영향 가능 | R2 |
| L360 (전망) | Q_DMAP > 3 이 한 채널이라도 나오면 cross-scale universality 부분 falsification | R2 + R3 |
| L385 | 서브-Hubble (lab/AU/kpc) 스케일에서 r ≪ 1 (10^-52 ~ 10^-7) → "saturation" 주장은 R_H 에 한정 | R1 |
| L388 | 2-loop 에서도 c 계수의 first-principle 닫힘 미달 가능성 — 정직 보고 | R1 |
| L389/L390 | 게이지·anomaly 검증 결과가 free coefficient 를 남기면 자유도 카운팅에 추가 | R1 + R3 |
| L370 | Companion paper 미작성 상태에서 메인 본문 전개 시 referee 재현성 질문 | 모든 reviewer |

## 2. Final-round attack vectors per reviewer

### R1 (Theorist) — 추가/심화 공격

- **A1.5** (신규, L385) "CKN saturation r(R_H) ≈ O(1) 는 우주론적 스케일에서만 성립한다. 그것이 SQT 의 *예측* 인가, 아니면 Λ_obs 가 입력으로 들어간 *순환 논증* 인가?"
- **A1.6** (신규, L388) "1-loop 에서 닫히지 않은 c 계수가 2-loop 에서도 닫히지 않는다면, 이론은 EFT 로서 self-contained 한가?"
- **A1.7** (신규, L389) "BRST 변환 하의 nilpotency 가 n-graviton expansion 의 어느 차수까지 명시적으로 검증되었는가?"
- **A1.8** (신규, L390) "Conformal anomaly T^μ_μ 의 n-field 기여가 Λ_eff 에 들어가는가? 들어간다면 D2 (FLRW background) pillar 가 anomaly-clean 이라는 주장은 수정되어야 한다."

### R2 (Observer) — 추가/심화 공격

- **A2.5** (신규, L350) "PSZ2-기반 cluster σ 가 lensing-selected sample 과 일관한가? hydrostatic bias (1−b) 보정 후 잔차는?"
- **A2.6** (신규, L360) "SPARC σ_0 와 DESI σ_0 와 Planck σ_0 가 같은 모수를 가리키는가? Q_DMAP > 3 채널이 있으면 universality 주장 무효."
- **A2.7** (신규, L380) "V(n,t) thawing toy 가 DESI w0=−0.757, wa=−0.83 와 정량적으로 일관하는가? 부호만 맞추는 toy 라면 'falsifier 통과' 라 부를 수 없다."
- **A2.8** (L320 의 R2.2 심화) "S_8 1% worsening 이 L342 σ(ρ) non-monotonicity / L360 Q_DMAP 결과와 함께 보면 SQMH 의 *systematic* signature 인가, 아니면 isolated regression 인가?"

### R3 (Statistician) — 추가/심화 공격

- **A3.5** (신규, L342) "σ_0(ρ_env) 비단조성의 BIC/Bayes-factor 정량은 보고할 수 있으나, N=3 anchor 에서 AICc 정의 영역을 벗어난다. 통계적 결론을 어떤 metric 으로 닫을 것인가?"
- **A3.6** (신규, L360) "Q_DMAP 자체가 reviewer-novel metric. 본 paper 가 Q_DMAP 를 critical evidence 로 사용한다면, Raveri-Doux 2021 인용 외에 sensitivity 분석 (posterior non-Gaussianity 효과) 이 필요하다."
- **A3.7** (L320 의 R3.2 심화) "fixed-θ ΔAICc=99 vs marginalized ΔlnZ=0.8 분리 보고는 수용. 그러나 L385 / L388 의 자유도 추가 (CKN saturation, 2-loop c 계수) 가 marginalized evidence 를 *더* 약화시키는가?"
- **A3.8** (신규, L370 관련) "Companion paper 가 method detail 을 모두 흡수한다면, 메인 paper 에서 reproducibility 채널을 어떻게 보장하는가?"

## 3. Defense matrix (final round)

### 3.1 핵심 방어 원칙 (L320 계승)

- Honesty-first. 모든 신규 한계를 Sec 6.4 (확장된) limitations 로 직접 기재.
- 7 falsifiers + 신규 K-conditions (K_holo_1, K_brst_n, K_anomaly) 를 offensive weapon 으로 유지.
- 'Falsifiable phenomenology' 포지셔닝 유지 (L6 8인 합의, JCAP 타깃).

### 3.2 새로 추가되는 방어 채널

- **CKN R_H saturation (L385)**: r(R_H) ≈ O(1) 은 *post-dictive consistency check* 라고 명시. SQT 가 Λ_obs 를 *예측* 했다고 주장하지 않음. 입력 → 일관성 → 기각 안됨, 의 정직한 framing.
- **2-loop status (L388)**: c 계수가 2-loop 에서도 free 라면 EFT 로서 정당화는 *Wilsonian truncation* 으로 framing. 닫힘 주장 포기, 자유 파라미터 카운트 명시.
- **BRST/anomaly (L389/L390)**: 검증된 차수만 보고. 미검증 차수는 future work 로 정직 표기. anomaly contribution 이 0 이 아니면 D2 pillar text 수정.
- **Q_DMAP (L360)**: 결과가 어느 방향이든 (PASS/FAIL) Sec 7 에 그대로 기재. PASS → cross-scale universality 보강. FAIL → SQMH σ_0 가 scale-dependent 임을 인정 (SPARC vs DESI 별도 fit 채널 표기).
- **PSZ2 selection bias (L350)**: cluster σ_cluster anchor 의 systematic 채널을 quantify 후 anchor uncertainty 에 흡수. cluster σ 결론이 selection-driven 임이 드러나면 σ(ρ) non-monotonicity 의 강도 약화 정직 기재.
- **Companion paper (L370)**: 메인 paper 와 동시 submission 또는 near-simultaneous arXiv post 로 reproducibility 보장.

## 4. Severity triage (final round)

| 신규 attack | severity | resolution path |
|-------------|----------|-----------------|
| A1.5 (CKN circularity) | High | 'consistency check' framing, Λ_obs 입력 명시 |
| A1.6 (2-loop c 닫힘) | High | EFT/Wilsonian framing, free 파라미터 명시 |
| A1.7 (BRST 차수) | Med | 검증 차수까지만 claim, 나머지 future |
| A1.8 (anomaly Λ_eff) | Med | D2 pillar text 수정 검토 |
| A2.5 (PSZ2 bias) | Med | L350 결과로 anchor uncertainty 보강 |
| A2.6 (Q_DMAP universality) | High | 결과 그대로 기재, FAIL 시 채널 분리 표기 |
| A2.7 (V(n,t) DESI 정량) | High | toy → 정량 chi^2 보고. 부호만 맞으면 'consistent in sign, not amplitude' 정직 기재 |
| A2.8 (S_8 systematic?) | Med | 'background-only μ_eff≈1 구조적 한계' 강화 |
| A3.5 (N=3 metric closure) | Med | BIC + Bayes factor + Δχ² 동시 보고 |
| A3.6 (Q_DMAP sensitivity) | Med | posterior non-Gaussianity 점검 보고 |
| A3.7 (자유도 추가 → ΔlnZ) | High | 자유 파라미터 추가시 marginalized evidence 재계산 후 보고 |
| A3.8 (companion 분리시 재현성) | Low | companion arXiv 동시 게시 |

## 5. Response template structure (L320 계승 + 확장)

각 reviewer 별로:
1. Thank.
2. Quote concern verbatim.
3. State: (a) addressed in revision / (b) clarified / (c) future work / (d) honest concession (신규 카테고리).
4. Point to specific section/eq/figure/appendix.
5. Paste the new paragraph if textual change.
6. **신규**: L342–L391 인용이 들어가는 자리는 항상 세션 번호 + 정확한 산출물 경로를 부기 (재현성).

## 6. CLAUDE.md 준수 자가 점검

- [최우선-1] 방향만, 지도 금지: 본 attack design 은 "방어 *방향*" 만 제시. 수식·파라미터 값·유도 경로 일절 없음.
- [최우선-2] 이론은 팀 독립 도출: 본 attack 은 이론 도출이 아닌 reviewer-response 구조만 다룸.
- 역할 사전 지정 금지: response letter 작성 팀 (8인) 의 자율 분담 원칙 명시.
- 결과 왜곡 금지: 신규 한계 (S_8 systematic 의심, CKN sub-Hubble under-saturation, 2-loop c 닫힘 미달, Q_DMAP 잠재 FAIL) 모두 그대로 reviewer 채널에 매핑.
- "fixed-θ" vs "marginalized" 구분 (L6): 본 design 의 A3.7 에서 명시.
- 'falsifiable phenomenology' 포지셔닝 (L6 8인 합의): 유지.
- DR3 스크립트 미실행 원칙: 본 세션 코드 실행 없음 — 위반 없음.
