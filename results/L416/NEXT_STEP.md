# L416 NEXT_STEP — 8인팀 다음 단계 설계

세션 일자: 2026-05-01
입력: ATTACK_DESIGN.md (8인팀 공격 시뮬), L407 REVIEW (priori 영구 불가),
L405 REVIEW (R=10 collapse toy 신호).
원칙: CLAUDE.md 최우선-1/2 — 방향만 제공, 수식·수치·유도 경로 힌트 금지.

---

## 1. §3.4 caveat 강화 — 새 문구 방향

핵심 메시지 (방향만):
1. cubic-RG topology 호환률 96.8% 는 *허용 조건* 이며 saddle *위치* 와는
   분리 개념.
2. saddle 위치 자연성 (cluster band 떨어질 priori 확률) 은 자유 cubic
   scan 에서 1.4%, 표준 between-FPs 가정 시 0% — **본 RG truncation 안에서
   priori 도출 영구 불가**.
3. 따라서 saddle 위치는 *외부 anchor* (cluster 데이터) 만으로 결정 가능.
   이는 postdiction 인정과 같은 의미이며 §3.5 의 mock injection FDR 100%,
   anchor circularity 와 일관.
4. 회복 경로는 *비표준 RG* (Wetterich Wilsonian, holographic, gradient-flow,
   1-loop EFT) 에 한정 — future work 로 분리.

문구 톤: 정직, 단호, "영구 불가" 명시. PRD Letter 진입 자격 미달 재확인.

## 2. §3.6 caveat 강화 — 새 표/문구 방향

핵심 메시지 (방향만):
1. Lindley paradox 인정: marginalized Δln Z 는 prior width R 에 강하 의존.
2. R={2,3,5,10} 4개값 모두 본문 표로 보고. (현재 §3.6 마지막 줄 "★ R=3/5/10
   모두 보고 필수" 가 *지시* 로만 있고 *실제 표* 가 없음 → 표 신설.)
3. R=5 → R=10 에서 toy 5배 collapse 관찰. 실 데이터 marginalized Δln Z=0.8
   (R=5) 는 R=10 에서 음수 가능성 실재 — fragility 신호 명기.
4. L406 production dynesty (실 데이터 R={2,3,5,10}) 미수행은 budget 한계
   인정 + 향후 작업 명시.
5. BMA weight 31% (R=5) 도 R 의존 → "weight at R=5" 로 명시.

문구 톤: 정직 fragility disclosure. "inconclusive" 가능성을 referee 보다
먼저 본문에 인정.

## 3. 4인팀 실행 지침 (paper/base.md 직접 수정)

R-A (자율 분담, 사전 역할 지정 없음):
1. §3.4 본문 — saddle 위치 priori 도출 영구 불가 + 외부 anchor 의존 + 회복
   경로 명기.
2. §3.6 본문 — R-grid 표 (toy + 실데이터 가용분), Lindley paradox 인용,
   R=10 collapse 인정, BMA weight prior 명기.
3. cross-link: §3.4 → §3.5 anchor circularity. §3.6 → §3.4 postdiction.
4. README "Claims status" 와 §6.1 22행 표는 본 세션 범위 *외* — 별도 세션
   처리. 본 세션은 §3.4 + §3.6 본문만.

## 4. 8인팀 합의 (만장)

본 NEXT_STEP 의 4 단계 메시지를 §3.4/§3.6 에 직접 반영. 수식 추가 금지
(최우선-1). 한 줄 ~ 표 1개 수준의 minimal patch.

## 5. 한 줄 요약

§3.4: priori 도출 영구 불가 + 외부 anchor 의존. §3.6: R-grid 4점 표 +
R=10 collapse 인정 + Lindley paradox.
