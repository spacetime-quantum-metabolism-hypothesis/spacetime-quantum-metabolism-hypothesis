# L416 REVIEW — 4인팀 paper 직접 수정 결과

세션 일자: 2026-05-01
주제: paper/base.md §3.4 (RG saddle priori-impossible, L407) + §3.6 (R-grid
R=10 collapse, L405) caveat 본문 강화.
원칙: CLAUDE.md Rule-B — 4인팀 자율 분담, 사전 역할 지정 없음.

---

## 1. 4인팀 자율 분담 결과

- **R1 (자율: §3.4 patch 검토)**: 추가된 단락이 §3.5 anchor-circularity 및
  mock injection FDR 100% 와 cross-link 됨. "priori 도출 영구 불가" 표현은
  단호하나 정확 (현 truncation 한정). future work 회복 경로 (Wetterich,
  holographic, 1-loop EFT) 명시. PRD Letter 미달성 + JCAP 포지셔닝 재확인.
  → **승인**.
- **R2 (자율: §3.6 patch 검토)**: R-grid 4점 표 (R={2,3,5,10}) 추가, R=10
  collapse 정량 (78→15, 5배) 인정. "음수 가능성" 명기로 Lindley fragility
  선제 disclosure. method dependence (Laplace +4.27 gap) 명기. Kass-Raftery
  |Δln Z|<1 inconclusive 인정. → **승인**. 단, R-grid 절대값은 toy 임을
  본문에 명시 — 표 헤더 "(toy)" 및 단락에 "*toy 절대값* 만 신뢰" 명기 확인.
  → 통과.
- **R3 (자율: 정합성/cross-link)**: §3.4 새 단락 → §3.5 anchor circularity
  로 link, §3.6 새 단락 → §3.4 postdiction + §3.5 anchor circularity 로
  link. §3.7 cluster anchor 확장이 두 caveat 의 회복 경로 (다중 cluster
  joint) 와 자연스럽게 이어짐. base.md 다른 곳 (§0, §6.1, §7) 영향: 본
  세션 범위 외이며 기존 caveat 표현과 충돌 없음. → **승인**.
- **R4 (자율: 정직성/CLAUDE.md 준수)**: CLAUDE.md 최우선-1 (수식·수치 도식
  제공 금지) 검토 — 추가 단락의 1.4%, 0.5%, 78→15, 5배, +4.27 등은 모두
  *과거 시뮬 결과 보고* 이며 새 이론 수식 아님. 위반 없음. 최우선-2 (팀
  독립성) — 본 세션은 paper 본문 수정으로 이론 도출 단계 아님. 위반 없음.
  print 유니코드 검토 — 본 patch 는 markdown 본문 (matplotlib/print 아님)
  → 정합. → **승인**.

### 4인팀 합의

§3.4 + §3.6 patch 모두 정상 반영. CLAUDE.md 원칙 위반 없음. 결과 승인.

---

## 2. paper/base.md 수정 요약

### §3.4 (line 727~739, 13행 추가)
새 단락: cubic-RG topology 96.8% 호환 vs saddle 위치 자연성 분리 명시. 자유
cubic-RG scan priori 확률 1.4% / 표준 between-FPs 가정 P=0 인정. **"saddle
위치 priori 도출 영구 불가"** 단호 표현. 외부 anchor 의존 = §3.5 circularity
와 일관. 회복 경로 비표준 RG 3종 (Wetterich/holographic/1-loop EFT) 으로
future work 격하. PRD Letter 미달성 + JCAP 포지셔닝 재확인.

### §3.6 (line 753~776, 24행 추가)
새 단락 + R-grid 4점 표. R={2, 3, 5, 10} toy Δln Z 명기. R=10 에서 78→15
(5배 collapse) 인정. "실 데이터 R=5 0.8 → R=10 음수 가능" 명기. Lindley
fragility, method dependence (+4.27 Laplace gap), BMA weight R=5 한정,
Kass-Raftery |Δln Z|<1 inconclusive 본문 정직 인정. cross-link §3.4/§3.5.

---

## 3. ATTACK_DESIGN ↔ REVIEW 매핑

| 공격벡터 | caveat 적용 후 차단 |
|----------|----------------------|
| A1 topology vs 위치 혼동 | §3.4 첫 줄에서 명시 분리 |
| A2 fit-vs-prediction | §3.4 외부 anchor 의존 명기 |
| A3 fine-tuning | priori 도출 영구 불가 인정으로 무력화 |
| A4 Occam | §3.4 SPARC -1.84 + §3.6 inconclusive |
| A5 anchor-circularity | §3.4 → §3.5 cross-link |
| A6 PRD double-violation | §3.4 PRD 미달성 재확인 |
| A7 Wetterich truncation | §3.4 future work 명기 |
| A8 assumption coverage | §3.4 표준 between-FPs 가정 명시 |
| B1 prior cherry-pick | §3.6 R-grid 4점 표 |
| B2 본문-부록 불일치 | §3.6 본문에 R-grid 표 직접 |
| B3 wide-prior 점근 | §3.6 R=10 포함 |
| B4 결론 반전 | §3.6 inconclusive 인정 |
| B5 Lindley paradox | §3.6 명시 인용 |
| B6 BMA-fragility | §3.6 "at R=5" 명기 |
| B7 small-N robustness | §3.6 "*toy*" 명기 |
| B8 method dependence | §3.6 +4.27 Laplace gap 명기 |

→ 16/16 공격 벡터 모두 본문 caveat 로 선제 차단.

---

## 4. 산출 파일 목록

- `results/L416/ATTACK_DESIGN.md` — 8인팀 reviewer 공격 시뮬 (16 벡터)
- `results/L416/NEXT_STEP.md` — 8인팀 caveat 강화 메시지 (방향만)
- `results/L416/REVIEW.md` — 4인팀 코드/본문 검토 (본 파일)
- `paper/base.md` — §3.4 (13행 추가), §3.6 (24행 추가) 직접 수정

---

## 5. 정직 한 줄

§3.4 saddle 위치 priori 도출 영구 불가 + 외부 anchor 의존 본문 명시,
§3.6 R-grid 4점 표 + R=10 collapse + Lindley fragility 본문 정직 인정 —
JCAP 포지셔닝 강화, PRD 미달성 재확인, 16/16 reviewer 공격 벡터 본문 선제
차단.
