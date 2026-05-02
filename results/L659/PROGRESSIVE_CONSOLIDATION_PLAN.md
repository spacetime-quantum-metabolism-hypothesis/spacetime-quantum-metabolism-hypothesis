# L659 — Progressive Consolidation Plan

본 세션 Phase 11–51 = 112 산출물을 단일 paper 본문으로 흡수하기 위한 mapping plan.
[최우선-1] 준수: 본 문서는 수식 0줄, 파라미터 값 0개. consolidation plan 만 기술.

---

## §1 §0–§8 Mapping 매트릭스

| Paper 절 | 흡수 대상 산출물 | 비고 |
|---------|----------------|------|
| §0 Abstract | L643 §0 본문 예시; L568/L593/L623 trajectory; L647 정직성 ★★★★★+ 자산; 4 priori 박탈 + fabrication 90% disclosure; 6 falsifier (DR3 conditional) | 정직성 자산을 abstract 첫 줄급 위치에 |
| §1 Introduction | L640 §1 본문 예시; L625 scope axiom A0; 4-pillar 도입; L569 phenomenology pivot (조건부, L654 어휘 갱신) | pivot 어휘는 L654 갱신본 사용 |
| §2 Foundational principle | L640 §2 본문 예시; axiom 1+2 / axiom 3+4 (paper/base.md §3 인용) | base.md §3 직접 참조 |
| §3 4-pillar covariance | L640 §3 + L646 §3 본문 예시; SK pillar (L292), Wetterich pillar (L293), Holographic pillar (L294), Z_2 pillar (L295); L601 unification 가설 (조건부) | unification 은 Rule-A 통과 후만 |
| §4 Layered axioms | L640 §4 + L646 §4 본문 예시; §4.1 core axioms; §4.2 derived (B1/a4/a6); §4.3 Hidden DOF 9–13 (L495/L502) | Hidden DOF 는 §4.3 별도 sub |
| §5 Quantitative predictions | L640 §5 본문 예시; a₀ PASS_MODERATE (L482/L489/L491–L494/L502/L506); σ₀ dimensional uniqueness; 6 falsifier (L498 N_eff 8.87σ) | 수치는 paper 본 단계에서 결정, plan 에서는 명시 금지 |
| §6 Active limitations | L639 §6.1–§6.7 + L591; 4 priori 박탈 (L549/L552/L562/L566); L564 fabrication 90% disclosure; L578/L587/L588/L589 회의적 0/4; Hidden DOF 9–13; L582 mass redef 영구 종결; multi-session 의무 (L633 H2); paradigm shift 박탈 risk (Phase 31–40) | 정직 disclosure 의 핵심 절 |
| §7 Outlook | L643 §7 본문 예시; DR3 (2027 Q2) BCNF protocol (L583); L657 3 시나리오 trajectory; multi-session H2 (L633); paradigm shift conditional | DR3 conditional 명시 |
| §8 Reproducibility | L643 §8 본문 예시; verify_*.py 7/7 PASS (L637); claims_status v1.3 (L638 plan); erratum 디렉터리 (L635); OSF DOI workflow plan | erratum + OSF 둘 다 |

---

## §2 흡수 우선순위

1. **즉시 흡수 가능** (8인 Rule-A 사후 검토만 필요)
   - L640/L643/L646 본문 예시 28+ paragraph 이미 작성됨
   - §0/§1/§2/§3/§4/§5/§6/§7/§8 골격 paragraph 존재
   - 흡수 = paper 본문에 paragraph 단위로 병합

2. **Rule-A 의무 (8인 순차 리뷰 선행)**
   - L601 4-pillar unification 가설 → §3 말미 또는 §7 outlook
   - L633 H2 multi-session 의무 → §7
   - paradigm shift 후보 paragraph (Phase 31–40 결과) → §6 limitations / §7 outlook 어느 쪽에 둘지 8인 합의 필요

3. **Rule-B 의무 (4인 코드리뷰 선행)**
   - L637 verify_*.py 7/7 PASS cross-check → §8 reproducibility 인용 전
   - L638 claims_status v1.3 schema 검증 → §8 인용 전
   - erratum 디렉터리 구조 (L635) → §8 인용 전

---

## §3 8인 Rule-A 의무 항목

| 항목 | 출처 | 흡수 절 | 리뷰 포커스 |
|------|------|--------|-------------|
| 4-pillar unification 가설 | L601 | §3 말미 / §7 | 4 pillar 가 단일 covariance 로 환원 가능한지 |
| H2 multi-session 의무 | L633 | §7 | 단일 세션 결론의 박탈 risk |
| Phenomenology pivot 어휘 | L569 / L654 갱신본 | §1 | "phenomenology" vs "framework" 어휘 일관성 |
| Paradigm shift 박탈 risk | Phase 31–40 | §6 / §7 | limitations 포함 vs outlook 분리 |
| Fabrication 90% disclosure 위치 | L564 | §0 vs §6 | abstract 노출 수준 |
| 4 priori 박탈 통합 disclosure | L549 / L552 / L562 / L566 | §6 | 박탈 4건 묶음 narrative |
| 회의적 0/4 결과 처리 | L578 / L587 / L588 / L589 | §6 | 단일 paragraph 통합 vs 분산 |
| 6 falsifier DR3 conditional | L498 + L583 BCNF | §5 / §7 | falsifier 명시는 §5, DR3 timeline 은 §7 분리 |

---

## §4 4인 Rule-B 의무 항목

| 항목 | 출처 | 검증 포커스 |
|------|------|-------------|
| verify_*.py 7/7 PASS cross-check | L637 | 7 스크립트 재현 + exit code; 의존성 lock |
| claims_status v1.3 schema | L638 plan | JSON schema 적합성, 필드 drift guard |
| erratum 디렉터리 구조 | L635 | 파일 명명 규칙, 인덱스 자동생성 여부 |
| OSF DOI workflow | §8 plan | 업로드 manifest, 버전 동결 절차 |
| BCNF protocol DR3 trigger | L583 | DR3 공개 전 실행 차단 (CLAUDE.md L6 규칙 준수) |

---

## §5 정직 한 줄

본 plan 은 mapping 만 정의. paper / claims_status / 디스크 본문 0건 edit. 흡수 실행은 8인 Rule-A + 4인 Rule-B 통과 이후에만 가능.
