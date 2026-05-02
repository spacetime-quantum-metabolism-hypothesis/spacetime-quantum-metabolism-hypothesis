# L411 — PAPER_UPDATE_PLAN v2 (paper/base.md 갱신 지침)

날짜: 2026-05-01
근거: L402..L410 9 REVIEW + L411 SYNTHESIS_paper_base_md_v2.md
원칙: CLAUDE.md [최우선-1/2] — 수식/파라미터/유도 경로 도입 금지. *정책 텍스트만* 갱신. 수식이 필요하면 본문에 *플레이스홀더* 만 두고 별도 LXX 8인 도출 세션으로 위임.

8인 Rule-A 순차 리뷰 필수 절: §2.5, §5.2, §6.5(e), abstract, README TL;DR (이론 클레임/포지셔닝).
4인 Rule-B 코드리뷰 필수: 갱신 PR 의 cross-ref drift 점검 (verification_audit JSON, README claims-table) — drift guard assertion 추가.

---

## A. 절별 변경 지침

### A.1 §2.5 (L404 Dual coexistence)
- 1단락 → 2단락 확장.
- 두 후보 (Causet meso, GFT) 본문 명시.
- 보조 표 신설: NEXT_STEP §3 의 "Causet 채택 시 / GFT 채택 시 / 양립 정책 시" 3 시나리오 row 영향 표.
- 결정 유보 명시 + micro-decision register 별도 등록.
- §6.5(b) 와 cross-ref.

### A.2 §3.2 (L407 ★★ topology caveat)
- 신규 ★★ 캐비엣 1단락 추가:
  > "★★ cubic β(σ) saddle topology 정합성 미입증: σ_cluster (7.75) < σ_cosmic (8.37) 부등식이 표준 monotone-RG 와 부합 안 됨. quintic-RG 또는 다단계 flow 가 future work 핵심."
- §3.4 기존 postdiction caveat 와 cross-ref.

### A.3 §3.4 (L405 Lindley fragility 강화)
- 기존 caveat 에 1 문장 추가:
  > "Lindley fragility risk: toy R-grid (L405) 에서 ΔlnZ 가 R=5→R=10 에서 factor ~5 로 collapse. 실 데이터 production dynesty 미수행 — referee 가 'which lnZ method' 질문 시 ±1–2 lnZ 변동 가능 명시."

### A.4 §3.6 (R=10 production dynesty 권고 row 추가)
- "production dynesty pending (LXX-future)" placeholder 1줄.

### A.5 §4.6 (L406 S_8 영구 OBS-FAIL + Euclid falsifier)
- S_8 mitigation 4채널 enumeration 표 추가 (A1 dark-only, A2 disformal, A3/A4 forbidden).
- 영구 OBS-FAIL 등급 명시.
- Euclid 4.4σ DR1 falsifier 사전등록 (toy linear-bias forecast 명시).
- abstract footnote 추가: "forecast assumes Gaussian likelihood with literature σ(S_8); full hi_class + Euclid mock chain is Phase-7 work."

### A.6 §5.2 (L402 회피 불가 tautology — 최우선)
- **첫 줄 수정**:
  - 현행: "ρ_q/ρ_Λ(Planck) = 1.0000 *exact* 일치."
  - 신: "ρ_q/ρ_Λ(Planck) = 1.000000 *by construction* (axiom-3 단위변환 항등식). 본 일치는 *prediction* 이 아니라 *dimensional self-consistency check* 이며, ρ_Λ scale 의 a priori 도출은 본 paper 에서 미달성."
- L402 negative control (Path-ε ratio invariant 검증) 본문 인용.
- Path-α naive H₀+Planck 60자리 어긋남 명시.

### A.7 §6.1.1 (claims-table 정직 갱신)
- **row 13 (Λ origin)**: PASS_STRONG → **CONSISTENCY_CHECK** (신설 등급) 강등.
- **row 1 (S_8)**: NOT_INHERITED → **OBS-FAIL permanent** flag 추가, Euclid 4.4σ falsifier row 활성.
- **row 8 (Cluster)**: status "RECOVERY 진행중" 유지 + dominance threshold (3-metric simultaneous < 30%) 명시 + N=13 mock 16% 도달 정직 기록.
- **row 10, 11 (5번째 축)**: "Future plan" 컬럼에 "Dual coexistence; Causet/GFT 결정 유보" 추가.
- **#17 (Jacobson δQ=TdS)**: §6.5(e) footnote 분리 — "어느 5번째 축으로도 단독 회복 안 됨".

### A.8 §6.1.2 (NOT_INHERITED 표 컬럼 확장)
- "5번째 축 결정 후 회복" 컬럼 추가 (Causet 시 / GFT 시 / Dual 시 3 시나리오).
- §6.1.2.1 문장 정직 수정 (L404 §1.3 권고문 그대로).

### A.9 §6.5(b) (L404 iterative refinement caveat)
- 1 문장 추가:
  > "5번째 축 결정 유보 자체가 iterative refinement 의 한 사례 — 결정은 데이터 *불의존* micro-decision register 에 사전 등록한다."

### A.10 §6.5(e) (L409 reframing — 이미 적용)
- 본문은 이미 적용됨 (L409 REVIEW.md 참조).
- **cross-ref drift sync 필수** (L409 §4인팀 합의 #2): README §0 / line 149 / line 614 / line 750 등 9개 위치 광고 "31%" → "31% raw / 13% substantive / 9% identity" 양면 표기.
- enum 확장 (`PASS_IDENTITY`, `CONSISTENCY_CHECK`) → README §Status enum + verification_audit JSON schema 동기 수정.

### A.11 §7 (Future plan priority 갱신)
- **P1**: Wetterich Wilsonian truncation (L407) — RG b/c 1차원 도출.
- **P2**: 1-loop EFT matching (L407) — topology 정합성.
- **P3**: production dynesty Lindley sweep (L405).
- **P4**: published cluster σ₀(env) archive crawl (L410).
- **Tier B (V(n,t)-extension)**: **영구 보류** 명시 (L408). 부활 조건: axiom 으로부터 V(n,t) 의 단일 functional class 도출 + 자동 DESI box 진입.

### A.12 abstract / README TL;DR 동시 갱신
- "31% PASS_STRONG" 광고 → **"13% substantive PASS / 9% σ₀ identity / 25% inheritance / 25% partial / 25% NI"** 헤드라인.
- "Λ origin 1.0000 *exact*" → "Λ origin 1.000000 *consistency check (not prediction)*".
- "S_8 mitigation explored" → "**S_8 mitigation structurally unreachable; Euclid DR1 4.4σ falsifier pre-registered**".
- "5번째 축 후보 OPEN" → "Dual coexistence (Causet meso / GFT) — decision deferred to micro-register".

---

## B. 변경 우선순위 (PR 분할 권고)

| PR | 절 | 8인/4인 리뷰 | 우선순위 |
|----|-----|------------|----------|
| PR1 | §5.2 + §6.1.1 row13 + abstract Λ | 8인 (이론 클레임) | P0 |
| PR2 | §4.6 + §6.1.1 row1 + abstract S_8 | 8인 (이론 클레임) + 4인 (Euclid forecast 코드) | P0 |
| PR3 | §6.5(e) cross-ref sync (9곳) + verification_audit JSON enum | 4인 (cross-ref drift) | P0 |
| PR4 | §2.5 + §6.1.2 + §6.5(b) Dual coexistence | 8인 (정책) | P1 |
| PR5 | §3.2 + §3.4 + §3.6 + §7 (RG + Lindley + Tier B 보류) | 8인 (포지셔닝) | P1 |
| PR6 | §6.1.1 row 8 (Cluster N=13 forecast 갱신) | 4인 (mock vs published) | P2 |

P0 = JCAP 제출 전 필수 (정직성 위반 직결).
P1 = JCAP 제출 전 강력 권고.
P2 = revise & resubmit 시점 가능.

---

## C. drift guard assertion (L6 재발방지 규칙 준수)

- `assert verification_audit['advert_pct'] == 31` 같은 하드 광고값 제거.
- 대신 `assert verification_audit['substantive_pct'] in (12, 13, 16)` (보수 카운트 옵션 허용).
- enum drift: `assert 'CONSISTENCY_CHECK' in STATUS_ENUM` + `assert 'PASS_IDENTITY' in STATUS_ENUM`.
- README claims-table 와 §6.1.1 표 cross-ref: `import paper.base; assert paper.base.row13.status == 'CONSISTENCY_CHECK'`.

---

## D. 위반 위험 (정직 점검)

- **A.6 (§5.2)**: 광고 강등을 안 하면 L402 negative control 결과를 *은폐* 한 것 — 정직성 위반 P0.
- **A.5 (§4.6)**: Euclid falsifier 사전등록 안 하면 paper falsifiability 약점 P0.
- **A.10 cross-ref sync**: 9개 위치 중 1곳이라도 "31% PASS_STRONG" 잔존 시 §6.5(e) reframing 무력화 — single-source-of-truth 위반.
- **A.11 Tier B 영구 보류**: 안 하면 future LXX 에서 V(n,t) post-hoc template-zoo 재시작 risk — L408 §7 재발방지 위반.

---

## E. 미위임 사항

- **L403 K3 (canonical Q definition)**: 본 plan 은 §X placeholder 1단락 추가만. 격상 결정은 별도 LXX 8인 axiom-도출 세션 위임.
- **L405 production dynesty**: §3.4 caveat 강화 + §3.6 placeholder 만. 실 dynesty run 은 별도 LXX 위임.
- **L410 published archive crawl**: §6.1 row 8 status 만 갱신. 실 crawl 은 LXX-archive 위임.

---

## F. 정직 한 줄

P0 6개 절 (§5.2 / §4.6 / §6.5(e) cross-ref / abstract / README / verification_audit enum) 동시 갱신 없이 JCAP 제출 시 정직성 위반 — L402/L406/L409 발견의 *은폐* 가 되며, 회피 불가능 항진명제와 영구 OBS-FAIL을 광고 31% 뒤에 숨기는 결과가 됨.
