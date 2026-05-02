# L520 — Pre-DESI DR3 Publish Strategy

**Date**: 2026-05-01
**Status**: Strategy memo (8-team review pending before any submission action)
**One-line honesty**: DR3 풀 Y5 cosmology 결과는 2027년 발표 예정 — pre-DR3 publish 윈도우는 약 12–18개월로 충분히 넓다. 하지만 paper 자체가 publish-ready 가 아니다. 전략은 "윈도우 맥싱" 이 아니라 "윈도우 안에서 정직하게 falsifiable 한 형태로 OSF + arXiv preprint 락인" 이다.

---

## 1. DESI DR3 Timeline 확정

| 사건 | 날짜 | 출처 |
|---|---|---|
| DESI DR1 (Y1) cosmology | 2024-04 | LBL |
| DESI DR2 (Y3) cosmology | 2025-03-19 | desi.lbl.gov DR2 page |
| DR2 cosmology chains 공개 | 2025-10-06 | desi.lbl.gov |
| DESI 5-year mapping 완료 | 2026-04-15 | LBL Newscenter |
| **DR3 (Y5) full cosmology** | **2027 (분기 미확정)** | LBL April 2026 announcement |
| DESI 연장 (Y5+) → 17000 deg² | 2026–2028 운용 | LBL |

**핵심 정정**: 사용자 임무 명시 "DR3: 2025-2026 release" 는 사실이 아님. 4월 2026 LBL 공식 발표 ("first dark energy results from full five-year survey expected in 2027"). 실제 윈도우는 **2026-05 ~ 2027 Q1/Q2 (12–14개월 보수, 18개월 낙관)**.

---

## 2. Paper 현재 상태 (audit 후 publish-ready 시점 추정)

L6 8인 합의 + L46–L56 audit/decision 기록 종합:

### 미해결 critical gaps
- **Q17 amplitude-locking**: 부분 도출 (Δρ_DE ∝ Ω_m). exact coefficient=1 은 E(0)=1 정규화 귀결, 동역학적 유도 미달.
- **Q13/Q14**: 미달성. PRD Letter 진입 조건 (Q17 OR Q13+Q14) 미충족.
- **Q15 (S8 tension)**: 전원 FAIL. background-only 구조상 불가, paper 본문에 정직 기록 필요.
- **K13 / 5D mixing**: C28 R̂=1.3653 — Bayesian evidence (fixed-θ +11.257) 만 신뢰, Δχ² 인용 금지.
- **K19 (compressed CMB)**: hi_class 미설치 → "provisional" 명시 필수.
- **DR3 falsifier**: 핵심 falsifier 가 외부 데이터 의존. paper 안에 *예측*만 락인 가능.

### Publish-ready 시점 추정
- **JCAP "정직한 falsifiable phenomenology" 포지션** (L6-T3 8인 합의 권고 라인): 현 audit 반영 + 8인 순차 리뷰 + 4인 코드 리뷰 + reproducibility 패키지 + DR3 예측 사전등록 → **2026-08 ~ 2026-10** 도달 가능 (3–5개월).
- **PRD Letter 라인**: Q17 완전 달성 또는 Q13+Q14 동시 달성 필요 → 추가 이론 작업 6–9개월. **2027-01 이후**, 즉 DR3 와 거의 동시 — pre-DR3 우선권 의미 사라짐.

→ **현실적 publish-ready 윈도우는 JCAP 라인 한정**.

---

## 3. Pre-DR3 vs Post-DR3 trade-off

| 축 | Pre-DR3 (2026-08~2027-Q1) | Post-DR3 (2027-Q2~) |
|---|---|---|
| Priority claim | 락인 (DR3 데이터 안 본 상태에서의 예측 = 진정한 falsifier) | 사후 fitting 의심 영구 노출 |
| 데이터 reach | DESI DR2 + Pantheon+ + DESY5 + Planck compressed | + DESI DR3, 가능하면 Euclid Q1, CMB-S4 prelim |
| Falsifiability 강도 | 최대 (paper 가 "DR3 가 wa>−0.5 면 KILL" 명시 가능) | 약 (이미 결과 보고 작성한 의심) |
| Scoop 위험 | 낮음 (universal fluid IDE 는 mainstream 비핵심 트랙) | 높음 (DR3 후 RVM/IDE 재해석 paper 폭증) |
| 통계 power | DR2 13pt + 동반 데이터로 충분 (Δχ² 5–10 수준 식별 가능) | DR3 ~30pt 로 향상 |
| Q15/Q17 미달 노출 | 현재 그대로 노출 (정직 라인) | DR3 결과 따라 갱신/은폐 유혹 |
| 8인 권고 (L6-T3) | **이 라인 채택** | 비권고 |

**판정 (L520 단일 작성자 의견, 8인 리뷰 전)**: **Pre-DR3 publish 권고**. 단, 조건은 (a) JCAP 포지션 고수, (b) DR3 falsifier 정량 예측을 paper 본문 + OSF 사전등록 에 동시 락인, (c) Q15/Q17 미달성을 limitations section 에 정직 기재.

---

## 4. arXiv preprint timing 전략

### 권고 시퀀스
1. **2026-05 ~ 2026-07** (3개월): audit 반영 + 8인 순차 리뷰 (Rule-A) + 4인 코드 리뷰 (Rule-B) + reproducibility 패키지 finalize.
2. **2026-08 초** (T-0): OSF pre-registration 등록 (DR3 예측 + analysis pipeline freeze).
3. **2026-08 중순** (T+2주): arXiv preprint 제출 (OSF DOI 명시). JCAP 동시 동시 submission.
4. **2026-08 ~ 2027-Q1**: peer review 진행. DR3 출시 전 published version 락인 목표.
5. **2027 Q2 (DR3 후)**: companion paper "DR3 confirmation/falsification of L520 predictions" — original paper 수정 금지, 별도 letter.

### arXiv 단독 제출 vs 저널 동시 제출
- **arXiv-first** (저널 제출 전): priority 락인 가장 강력. 단, peer review 공식 검증 없음 → 학계 인용 약함.
- **저널 동시 제출** (권고): arXiv timestamp = priority, 저널 = validation. JCAP 처리 시간 평균 4–6개월 → DR3 (2027) 전 published 가능성 높음.

### 미루지 말아야 할 임계점
- **2026-12 마지노선**: 이 시점까지 arXiv preprint 미제출 시 priority claim 약화. DR3 가 빠르게 (2027-Q1 초) 나오면 사후 fitting 비난 회피 어려움.
- **2027-03 절대 마지노선**: DR3 발표 전 preprint 필수.

---

## 5. OSF pre-registration 의 publish-priority 효과

### OSF 의 가치
- **이론적 효과**: pre-registration timestamp + frozen analysis pipeline → 사후 fitting 의심 차단. open science 표준.
- **법적/공식적 priority**: arXiv 와 비교해 약함. 학계는 arXiv DOI 를 1차 priority 로 인정.
- **JCAP/PRD reviewer 인식**: positive (특히 falsifiable prediction 포함 시). open science badge 부여 가능.

### 실질 효과 추정
- arXiv 단독: priority 100, falsifiability credibility 50.
- arXiv + OSF: priority 100, falsifiability credibility **95**.
- OSF 단독: priority 30 (학계 비인정), credibility 70.

→ **OSF 는 arXiv 의 보완재이지 대체재가 아니다**. priority 자체에 OSF 가 미치는 영향은 작지만, "DR3 데이터 안 본 상태 예측" 의 신뢰성 확보에 결정적. 두 트랙 병행 필수.

### OSF 등록 항목 (사전 락인 필수)
1. SQMH 이론 핵심 가정 (n₀μ, σ=4πGt_P, ψⁿ a priori).
2. analysis pipeline 코드 git commit hash (현 main HEAD = 372b3f7).
3. DR3 예측: w_a 점추정 + 1σ 구간, S_8 점추정, BAO 13pt → ~30pt 확장 시 Δχ² 예측.
4. KILL criteria 명시 (예: DR3 best-fit w_a > −0.4 면 universal fluid IDE branch KILL).

---

## 6. 권고 결정 (8인 리뷰 전 단일 메모)

| 결정 항목 | 권고 |
|---|---|
| Publish 라인 | JCAP "honest falsifiable phenomenology" |
| Pre-DR3 vs Post-DR3 | **Pre-DR3 publish** |
| 타깃 제출일 | 2026-08 중순 (arXiv + JCAP 동시) |
| OSF pre-reg | 2026-08 초 (arXiv 2주 전) 락인 |
| PRD Letter 라인 | **포기** (Q17 완전달성 없이는 무리) |
| 마지노선 | 2026-12 (preprint 필수), 2027-03 (절대) |
| 8인 리뷰 (Rule-A) | 본 메모 publish 결정 전 필수 |
| 4인 코드 리뷰 (Rule-B) | reproducibility 패키지 freeze 전 필수 |

### 한 줄 정직
**현 paper 는 publish-ready 아님. 3–5개월 내 JCAP 라인으로 락인 가능. DR3 윈도우는 12–18개월로 시간 충분 — 서두를 이유 없지만 미루면 priority 잃는다.**

---

## Sources

- [DESI DR2 Cosmology Chains Released (Oct 2025)](https://www.desi.lbl.gov/2025/10/06/desi-dr2-cosmology-chains-and-data-products-released/)
- [DESI Reaches Mapping Milestone (Apr 2026)](https://www.desi.lbl.gov/2026/04/15/desi-reaches-mapping-milestone-surpassing-expectations/)
- [DESI Completes Planned 3D Map (LBL Newscenter, Apr 2026)](https://newscenter.lbl.gov/2026/04/15/desi-completes-planned-3d-map-of-the-universe-and-continues-exploring/)
- [DESI DR2 Publications Index](https://data.desi.lbl.gov/doc/papers/dr2/)
- [DESI DR2 Results II BAO (arXiv:2503.14738)](https://arxiv.org/abs/2503.14738)
