# L394 ATTACK DESIGN — Sec 5 (Cosmology) Final Draft

## 주제
논문 Section 5 "Cosmology" 최종 원고 작성. L207 의 ρ_q/ρ_Λ = 1.0000 결과,
T^{μν}_n 의 fluid 형식 + Bianchi identity (energy-exchange source), 그리고
DESI w_a 와의 정량적 거리(10.4% per Hubble vs DESI 권고)를 정직하게 기술한다.

## 스코프
- L207 결과를 Section 5 의 핵심 논거로 통합.
- ρ_q_0 = ρ_Λ(Planck) = 6.86e-27 kg/m³ 의 의미: SQT 에서 Λ-scale 자연 도출.
- T^{μν}_n = (ρ_q+p_q) u^μ u^ν + p_q g^{μν} fluid form 명시.
- Bianchi: ∇_μ T^{μν}_n = -∇_μ T^{μν}_m (matter ↔ n 교환 채널) — 10.4% per Hubble absorption.
- DESI DR2 w_0 = -0.757, w_a = -0.83 와의 *거리*: SQT toy 가 effective w_a ~ -0.3 수준,
  즉 정량 일치까지는 *아직 도달 못함*. 정직하게 명시.
- L208 (SPARC anchor) / L209 (DM cross-section FAIL) 참조는 cross-link 만, Sec 5 본문은
  배경+우주상수+DE phenomenology 에 집중.

## 방향 (지도 금지)
- Section 5 의 논리 흐름: (i) 배경 ρ_Λ scale matching → (ii) T^{μν}_n covariant form →
  (iii) Bianchi-derived energy exchange → (iv) DESI-comparable phenomenology → (v) 한계.
- 수식은 도출된 결과만 표기 (L207 report.json 의 명시 form). 새 수식 도입 금지.
- "DESI 정량 일치" 주장 금지. "정량적으로 가까우나 직접 fit 미달" 정직 표현.

## 8인 팀 자유 분담 (역할 사전 지정 금지)
- 8인 자율 분담. 자연스럽게 등장할 영역:
  1. ρ_Λ matching 의 의미 (coincidence vs prediction)
  2. fluid stress-energy 의 SQMH 해석
  3. Bianchi source term 의 물리 (matter→n 흡수율)
  4. DESI w_0/w_a 와의 정량 비교 + gap 기술
  5. 다른 DE 모델 (CPL, IDE, RVM) 과의 위치
  6. Falsifiable predictions (DR3, RSD, S8)
  7. 한계/caveat 정직 기록
  8. 논문 톤 (PRD vs JCAP) 및 cross-section L208/L209 link

## 4인 코드리뷰
- 수식 transcription / 단위 / 인용 (L207, L33, L34, L46~L56, DESI DR2 arXiv) 검증.
- 역할 사전 배정 금지.

## K-기준 (사전 정의)
- K1: ρ_q_0 = ρ_Λ(Planck) match_ratio=1.0000 정확 인용 + Planck 단위 명시.
- K2: T^{μν}_n fluid form 정확 표기 (covariant, signature 명시).
- K3: Bianchi source 10.4% per Hubble 수치 정확 인용 (L207 absorption_per_hubble).
- K4: DESI DR2 w_0=-0.757, w_a=-0.83 (DESI+Planck+DES-all) 출처 명시 (CLAUDE.md 규칙 준수).
- K5: "DESI 정량 일치" 미주장. "구조적 근접 + 직접 fit 미달" 정직 표현.
- K6: 유니코드 깨짐 없음 (cp949 호환 — 본문 ASCII, 라벨/수식 한정 unicode).
- K7: BAO-only vs joint 결과 혼동 없음 (CLAUDE.md L33/L34 규칙).
- K8: L208 SPARC anchor by-construction caveat / L209 DM null tension 정직 cross-link.

## 산출
- ATTACK_DESIGN.md (이 문서)
- REVIEW.md: 8인 토의 + 4인 코드리뷰 + K1~K8 판정 + 정직 한 줄.
- SEC5_DRAFT.md: 논문 Section 5 최종 원고 본문.

## 정직 원칙
- ρ_q/ρ_Λ = 1.0000 은 강력하지만 *coincidence vs prediction* 구분 필요.
- 10.4% per Hubble absorption 은 DESI w_a 와 *방향 일치*, 크기는 *factor ~3 부족*.
- 미증명/직접 fit 미달은 그대로 명시. 결과 왜곡 금지.
