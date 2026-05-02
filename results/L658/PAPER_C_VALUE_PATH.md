# L658 — Paper C (arXiv-D-as-paper, JCAP) Value-Path Identification

**Frame**: 가치 향상 = acceptance 향상 (사용자 명시)
**Baseline**: L655 Paper C 1순위, 55-65% acceptance
**Goal**: *어떤 sub-task* 가 Paper C 가치 향상에 가장 큰 net 기여를 하는가? — 정직 평가

본 문서는 [최우선-1] 준수: 수식 0줄, 파라미터 값 0개. 등급/평가만.

---

## §1. 7-Path 등급 매트릭스

| # | Path                         | 효과    | 비용  | net    | 본 세션 가능 | Rule-A 8인 의무 |
|---|------------------------------|---------|-------|--------|--------------|-----------------|
| 1 | 정직 disclosure 강화         | ★★★★★ | 작음  | ★★★★★ | YES          | 일부 (포지셔닝) |
| 2 | 4-pillar 미시 도출 강화      | ★★★★   | 중간  | ★★★    | 부분         | YES (이론 클레임) |
| 3 | 정량 예측 정밀화             | ★★★★   | 중간  | ★★★★   | 부분         | YES (uniqueness 주장) |
| 4 | 6 falsifier 정량화           | ★★★★   | 큼    | ★★★    | NO           | 부분 (preregistration) |
| 5 | paper 본문 *완전화*          | ★★★★★ | 작음  | ★★★★★ | YES          | NO (편집/통합) |
| 6 | 외부 검증 의뢰 (cross-agent) | ★★★★   | 큼    | ★★★    | NO (대기)    | NO (외부 산출물) |
| 7 | verify_*.py 확장             | ★★★    | 중간  | ★★     | YES          | NO (Rule-B 4인) |

### 등급 해설 (정직)

- **Path 1 (disclosure 강화) ★★★★★**: L564 90% 자발 disclosure 가 paper 의 *유일한 trust 자산*. 4 priori 박탈 (L549/L552/L562/L566) 본문 cross-mention 강화 시 reviewer "이 저자는 정직하다" 신호 강화. 비용 작음 (편집 작업), 효과 결정적.
- **Path 2 (4-pillar 미시) ★★★**: L601 unification 가설은 *이론 깊이* 에 기여. 그러나 Constructor theory pillar (L626) 시기상조 단 가능. cross-validation 강화 비용은 중간이지만, JCAP reviewer 가 "이론 깊이" 보다 "정직성 + falsifiability" 에 가중 → net ★★★.
- **Path 3 (정량 정밀화) ★★★★**: a₀ prefactor uniqueness, σ₀ uniqueness 정량 검증은 paper *empirical 정확도* 강화. 단 미시 도출 미완 상태에서 정량 정밀화는 "post-hoc fit" 의심 위험 → Rule-A 8인 의무. net ★★★★.
- **Path 4 (falsifier 정량) ★★★**: paradigm-specific 부호 예측 (L623 1-2/5 → 3-4/5) 강화는 *DR3 preregistration* 강도 결정. 그러나 비용 큼 (각 falsifier 별 separate analysis). DR3 공개 전 실행 의미 있음. net ★★★.
- **Path 5 (paper 본문 완전화) ★★★★★**: L639/L640/L643 28+ paragraph 본문 예시가 이미 존재. arXiv draft §3/§4 sync (L646) 까지 흡수 시 paper *완성도* 결정적 향상. 비용 작음 (편집/통합), 효과 즉시. net ★★★★★.
- **Path 6 (외부 검증) ★★★**: cross-agent 정합 (L648 template) 은 high-value 이지만 외부 의존 + 응답 대기 비용 큼. 본 세션 즉시 불가. net ★★★.
- **Path 7 (verify 확장) ★★**: 7 → 9-10 스크립트는 reproducibility 점수에 marginal 기여. Constructor theory verifier 는 시기상조. net ★★.

---

## §2. Top-2 권고

### Path 5 + Path 1 동시 진행

- **Path 5 (paper 본문 완전화)** — 본 세션 즉시 가능, 효과 ★★★★★. 28+ paragraph 본문 예시를 paper §3/§4 로 흡수, arXiv draft sync. CLAUDE.md "paper / claims_status / 디스크 edit 0건" 제약과 충돌 → *별도 후속 세션* 에서 실행 (현 L658 은 path 식별까지).
- **Path 1 (disclosure 강화)** — 본 세션 가능, trust 회복. 4 priori 박탈 cross-mention + Hidden DOF 9-13 정량 disclosure 시도. 포지셔닝 변경 부분만 Rule-A 8인 필요.

### 동시 진행 근거

- 두 path 모두 net ★★★★★, 비용 작음
- 상호 보완적: Path 5 = 완성도, Path 1 = 정직성
- JCAP reviewer 의 두 핵심 평가 축 (rigor + transparency) 직접 타격

---

## §3. 본 세션 직접 실행 가능 vs 8인 Rule-A 의무

| Path | 본 세션 직접 실행 | Rule-A 8인 필요 | 이유 |
|---|---|---|---|
| 1 disclosure 강화 | 편집 가능 | 포지셔닝 변경 시 필요 | "JCAP 정직 phenomenology" 포지셔닝은 이론 클레임 |
| 2 4-pillar 미시 | NO | YES | 4-pillar unification 은 이론 클레임 |
| 3 정량 정밀화 | NO | YES | uniqueness 주장은 이론 클레임 |
| 4 falsifier 정량 | 부분 | 부분 | DR3 preregistration text 는 편집, 부호 예측 변경은 이론 |
| 5 paper 완전화 | YES | NO | 기존 본문 통합/편집 |
| 6 외부 검증 | NO | NO | 외부 산출물 대기 |
| 7 verify 확장 | YES | Rule-B 4인 | 코드 작성 |

**본 세션 (L658) 자체는 path 식별 까지만**. 실제 실행은 후속 세션 + 적절한 리뷰 게이트.

---

## §4. Acceptance 향상 추정 (정직)

**Baseline (L655)**: 55-65%

| 시나리오 | 추가 path | acceptance 추정 |
|---|---|---|
| (A) 현재 상태 유지 | — | 55-65% |
| (B) Path 5 단독 (paper 완전화) | +5 | 60-70% |
| (C) Path 5 + Path 1 (본 권고) | +5,+1 | 63-72% |
| (D) Top-3 (5+1+3) | +5,+1,+3 | 65-75% |
| (E) 전체 7 path | all | 68-78% (단, 비용 폭증 + Rule-A/B 게이트 다중) |

**정직 평가**: (C) 시나리오가 *비용 대비 net* 최적. (D)/(E) 는 marginal gain 대비 비용 + 게이트 누락 리스크 큼.

**중요 한계**: acceptance 추정 자체가 추정치이며, JCAP 의 ±α 변동 + reviewer 개별 편향은 모델링 불가. 본 추정은 "상대 비교 sense" 로만 사용.

---

## §5. 정직 한 줄

> **Path 5 + Path 1 의 net ★★★★★ 두 축이 paper C 의 acceptance 를 결정하며, 나머지 path 는 marginal gain 에 비해 비용 + 게이트 부담이 비대칭적으로 크다.**

---

## CLAUDE.md 정합 확인

- [x] paper / claims_status / 디스크 edit 0건 (본 문서는 results/L658/ 평가 산출물)
- [x] 등급/평가만 (수식 0줄, 파라미터 값 0개)
- [x] [최우선-1] 준수
- [x] Rule-A/B 의무 path 별 명시

**기간**: ~5min (식별 단계)
**다음 단계**: 사용자 승인 시 후속 세션에서 Path 5 → Path 1 순차 실행
