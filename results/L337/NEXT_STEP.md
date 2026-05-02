# L337 — NEXT STEP

## 본 L337 산출
- 5 gap 별 pillar 매핑 + 등급 예측 (ATTACK_DESIGN.md)
- 8인 자율 분담 리뷰 (REVIEW.md)
- closure 등급: 1 OPEN + 4 partial (closed 0)

## 우선순위 (8인 합의 기반)

### 즉시 (L338)
- **gap_1 (a2 ↔ SK + KMS)** 도출 시도 — partial → closed 가능성 높음
  - 방향: SK contour 의 KMS 조건이 시간 평행이동 invariance 의
    *결과* 임을 보이고, a2 를 정리로 강등
  - 수락: 비평형 (Γ_0 > 0) 보정항이 자연스럽게 도출되는지 확인
  - 8인 팀 자율 도출, 수식 사전 제공 금지

### 다음 (L339)
- **gap_2 (Γ_0 ≈ H_0 ↔ RG IR FP)** 도출 시도 — partial
  - 방향: Wetterich β-function 의 IR FP scale 과 cosmic 시간 scale 매칭
  - 8인 팀 자율 도출, AICc 패널티 고려
  - 위험: scale matching uniqueness 미보장 (도출 후 ablation 필수)

### 이후 (L340)
- **gap_5 + gap_6 결합** (시간 스케일 root cause) — partial 양측
  - 두 gap 가 동일 root (시간 스케일) 가설 검증
  - causal patch ring topology (2π) vs horizon area (4π) factor 도출
  - τ_q ↔ RG flow time 매핑

### 중장기 (L341+)
- **gap_3 (emergent metric)** — OPEN, 5번째 pillar (Verlinde / tensor network)
  도입 결정 후 진행
  - 4 pillar 만으로 부족 — 외부 채널 도입은 framework 확장 결정 필요
  - 8인 팀 사전 검토: "5번째 pillar 도입이 SQMH 정합성 위반인가?"

## 검증 게이트

각 gap closure 시도 후 다음 체크 (CLAUDE.md 준수):
- [ ] axiom 순환 의존 없는가? (a_x → pillar → a_x 금지)
- [ ] 자유 파라미터 수가 도출 *전* 보다 줄었는가?
- [ ] AICc 패널티 적용 후 단순 모델 대비 개선?
- [ ] 8인 팀 자율 분담 후 합의 도달?
- [ ] 4인 코드리뷰 (수치 검증 시) 통과?

## 정직 한 줄
**L338 우선 = gap_1 SK+KMS closure (closed 가능성). gap_3 metric emergence 는
4 pillar 부족 — 5번째 pillar 도입 필요성 사전 검토 필수.**
