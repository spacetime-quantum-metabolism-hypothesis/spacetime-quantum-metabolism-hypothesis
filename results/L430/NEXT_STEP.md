# L430 — NEXT STEP (8인팀 다음 단계 설계)

세션: L430
날짜: 2026-05-01
의제: bilinear (σ · n · ρ_m) mass-action 함수형 가정의 *도출* 경로 설계.
공격 결과 (ATTACK_DESIGN A1–A8) → 즉시 paper-fix (4인 위임) + 미래 도출 시도 (8인 권고).

---

## (i) 도출 후보 경로 — 우선순위

### P1. SK 4-vertex + KMS detailed balance (미시 축 #1 강화)

- **방향**: SK contour 의 forward/backward branch 의 4-vertex `g · ψ̄ψ · n̂`
  를 *minimal coupling* 가정에서 출발. detailed balance (KMS, T = T_dS) +
  vertex renormalisation 1-loop 에서 함수형 자동 고정 시도.
- **검증 가능 기준**: bilinear 가 *유일한* IR-stable fixed point 가 되는지
  Wetterich functional renormalization (미시 축 #2) 로 cross-check.
- **불가시**: 다른 vertex (`g · (ψ̄ψ)² · n`, `g · ψ̄ψ · n²`) 가 동등하게
  IR-안정이면 bilinear 는 ansatz 로 *영구* 남는다 → §3.4 caveat 추가 의무.

### P2. axiom 1 강화 — "absorption is single-quantum process"

- **방향**: axiom 1 진술을 "물질이 시공간 양자 *하나* 를 단위 시간당 단위
  부피당 흡수" 로 *세분화*. 이러면 R = σ · n · ρ_m 가 미시 정의로 환원
  (Boltzmann mass-action 의 1-1-collision 한도).
- **위험**: axiom 수가 6 → 7 로 늘면 framework 단순성 잃음. 또한 single-quantum
  은 자체로 추가 가정 (multi-quantum 흡수 non-zero 가능성 차단).
- **수단**: §2.1 표 axiom 1 한 줄에 "(single-quantum, leading-order; multi-quantum
  은 NLO suppression 으로 추정)" 부언만 추가하는 *minimal patch* 권고.

### P3. holographic counting (미시 축 #3 결합)

- **방향**: σ₀ = 4πG·t_P 의 holographic 도출 (SQMH H bound) 에서, 흡수
  cross-section 자체가 area 단위 (m²) 라는 observation 으로부터 R 형태
  추정. 그러나 *함수형 univalence* 미보장 (A4).
- **상태**: 보조 증거만, primary 도출 불가.

### P4. EFT matching at IR (Phase 5 hi_class)

- **방향**: 전체 EFT 를 작성 후 IR limit 에서 mass-action 함수형 *유도* 시도.
  Phase 5 수준 (CLASS / hi_class) 에서만 의미. 현 paper 단계 over-spec.
- **상태**: future work, JCAP 본문 외.

---

## (ii) Phase별 일정 — 정직 권고

| Phase | 작업 | 결과물 |
|-------|------|--------|
| 즉시 (L430 4인) | §2.2 derived 1 sketch 에 bilinear 명시 + B1 ansatz 단락 신설 | paper/base.md 수정 |
| L431+ (8인) | P1 SK vertex IR-stable fixed point 분석 | results/Lxxx/SK_VERTEX.md |
| L432+ (8인) | P2 axiom 1 minimal patch 검토 (단일 양자 vs 다중 양자) | axiom 표 update 제안 |
| Phase 5 | P4 EFT matching | hi_class branch |

---

## (iii) 가드레일 — 절대 금지 사항

(CLAUDE.md 최우선-1 준수)

- **bilinear 의 "유도 경로 힌트" 를 paper 에 적지 않는다** — 도출 *성공* 까지
  ansatz 명시 + 정직 caveat 만. axiom 4 와 동일 (미시 OPEN 표기).
- **SK vertex 형태 를 paper 에 미리 적지 않는다** — P1 결과 도출 후만.
- **axiom 1 자체 진술 변경 금지** (P2 는 부언 patch 만, 본문 진술 유지).

---

## (iv) Hidden-postulate 재분류 권고

§6.5(e) "PARTIAL 8" 표 의 "mass-action 함수형" 한 줄 옆에 다음 한 줄 추가:

> **B1 (bilinear absorption ansatz)**: derived 1 의 함수형 입력. axiom 1–6
> 어느 것의 결론도 아닌 *추가 ansatz* — 따라서 PARTIAL 보다 *hidden
> postulate* (paper postulate 등록 필요) 분류가 정직. 도출 시도는
> P1 (SK vertex) 가 우선 (§7 future work).

이 한 줄 추가 + §2.2 sketch 명시화 = L430 최소 산출물.

---

## (v) 4인팀 실행 위임 (REVIEW.md 산출)

다음 작업을 4인팀이 자율 분담으로 실행:
1. paper/base.md §2.2 derived 1 row sketch 컬럼 → bilinear 명시
2. §2.2 직후 1단락 신설 — "B1 absorption-rate ansatz (bilinear)" + 정직 caveat
3. §6.5(e) PARTIAL 8 표 cross-link (B1 → §2.2)
4. 본 변경 README claims_status.json 동기는 *불필요* (분류 등급 변동 없음 — PARTIAL 유지, naming 만 명시화).
