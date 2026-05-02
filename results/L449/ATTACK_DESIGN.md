# L449 ATTACK_DESIGN — 8인팀 reviewer 공격 설계

**주제**: dSph anchor 추가가 paper §6.1 row #5 (three-regime 강제성)
강화 channel 인지, 아니면 *cherry-pick 자유도 우위* 인지를 분리하기 위한
**사전등록 (pre-registration) path 자체의 ATTACK**.

**선행**:
- L424 ATTACK/NEXT_STEP/REVIEW (8인 + 4인) — dSph 추가 시 ΔlnZ 가
  -22 ~ +34 의 시나리오/매핑 의존, mock false-rate 변동 부재.
  4 조건 사전등록 후에만 강화 주장 가능 결론.
- paper §6.1 row #5 ACK_REINFORCED 강화 권고.
- L420 Λ_UV postdiction caveat 강화 (post-naming KILL 사례 학습).

**원칙**: CLAUDE.md [최우선-1, 2] — 4 조건의 *수치값* 또는 *부호*
미지정. 사전등록 *path* 의 메타-거버넌스만 설계.

---

## 8인팀 자율 발생 비판 채널 (B1–B8)

### B1 — "사전등록 자체가 cherry-pick" 의 메타 risk
"4 조건 사전등록" 이라는 행위 자체가, 등록 *시점* 을 사후에 (사실상 데이터를
이미 본 후) 잡으면 cherry-pick 와 동치. timestamp 가 OSF/GitHub release tag
의 *data-blind* 시점인지 검증 가능해야 한다. 즉 등록 즉시 archive 측정값
입력 금지 — 단, 측정값은 *공개 카탈로그* (McConnachie 2012, Gaia DR3) 이므로
"등록 시점에 이미 alkaesst" 라는 약식 cherry-pick 가능. 따라서 등록 문서는
"공개 카탈로그 기반이며 이 시점 이후 어떤 archive 도 추가하지 않는다"
*잠금 진술* 을 포함해야 한다.

### B2 — 부호-결정 임계의 사전 부호 자체가 cherry-pick risk
ATTACK B6 (L424) 의 "saturation 부등식 부호 미지정" 은 사전등록으로
해결되는 듯 보이나, *부호 자체* 를 어느 쪽으로 정할지가 또 다른 free
parameter. 사전등록은 (i) cosmic regime 재진입, (ii) cluster 위치 이동,
(iii) galactic 단조 회복 *세 분기* 모두를 명기해야 하며, "결과가 어느
분기에 떨어지면 어떤 결정" 인지 *결정 매트릭스* 를 사전 고정. 분기 중
하나만 등록하면 사전등록 의미 상실.

### B3 — ρ_env 매핑 prior 의 자유도
L424 4인팀 결과: LG-outer vs galactic-internal 매핑만으로 부호 반전.
사전등록은 (i) 어느 매핑을 *primary* 로 쓸지, (ii) secondary 매핑은
*sensitivity check* 로만 보고할지 명시. primary/secondary 결정이
사전등록 후 변경되지 않는다는 잠금 진술 필요. 두 매핑 중 *결과가 좋은*
쪽을 사후 primary 로 선택하면 사전등록 무효.

### B4 — σ₀ 변환 prior 의 axiom 경제성 페널티
L424 ATTACK B4: 측정 (M_dyn, σ_los, r_half) → SQMH σ₀ 변환식 자체가
paper 에 없음. 변환 prior 를 추가하면 axiom 경제성 페널티. 사전등록
문서는 변환식의 *함수 형태* + *prior 분포* + *유도 출처* (Walker 2009 /
McConnachie 2012 어느 식) 를 명시. 변환 prior 가 fitting 후에 폭이
조정되면 사전등록 무효.

### B5 — 175-point mock false-rate Δ 의 base-rate 함정
L424 4인팀: toy mock 에서 false-rate 가 baseline 0% — 강제력 회복 측정
유의 신호 부재. paper §3.5 175-point SPARC mock 의 100% false-rate 와
비교 시, dSph 5점 추가가 false-rate 를 *낮추는지* 측정 가능. 그러나
"낮춘다" 의 기준 자체 (예: ≤80%, ≤50%, ≤20%) 가 사전 고정되지 않으면
사후 cherry-pick. 결정 임계값 (false-rate threshold) 을 사전등록.

### B6 — OSF/GitHub timestamp 의 cryptographic 검증 가능성
사전등록 timestamp 는 (a) GitHub release tag (commit hash + tag date),
(b) OSF DOI (project freeze + DOI mint date), (c) arXiv preprint
(submission date) 세 채널 동시 등록이 표준. 단일 채널 (예: GitHub only)
은 force-push 또는 tag-rewrite 로 사후 조작 가능. 본 dSph 사전등록은
*triple-timestamp* (GitHub tag + OSF DOI + paper §6.1 row 14 의
"v-preDR1-2026.NN" 표준 차용) 권장.

### B7 — 사전등록 *후* 추가 dSph (Fornax, Leo I/II) 의 처리
McConnachie 2012 카탈로그 8개 dSph 중 5개 (Draco/UMi/Scl/Sextans/Carina)
만 anchor pool. 나머지 3개 (Fornax, Leo I, Leo II) 를 *왜 제외* 했는지
사전등록 문서에 기록 필수 — L424 ATTACK B5 sample selection bias 지속
risk. 등록 후 추가 dSph 발견 (Gaia DR4) 시 *automatic addition* 인지
*re-registration* 인지 정책 사전 고정.

### B8 — falsifier 등급 (P9 conditional) 의 정합 점검
L424 권고: P9 falsifier 등급을 *conditional* (사전등록 후만 falsifier)
로 격하. 본 사전등록이 paper §4 22-예측 표 P9 row 의 *수정* 을 동반
해야 함. 사전등록은 했는데 P9 등급은 그대로면 메타-부조화. paper
update PR 이 사전등록 commit 과 *동일 commit* 또는 *직속 후속 commit*
에 포함되는지 확인.

---

## 8인팀 합의 결론

- 본 L449 는 dSph anchor 사전등록 *path* 의 메타-거버넌스 설계.
  4 조건 (B2/B3/B4/B5) 의 *수치값* 은 본 ATTACK 단계에서 *결정하지 않으며*,
  결정 매트릭스의 *형식* 만 합의.
- triple-timestamp (GitHub release tag + OSF DOI + paper commit) 가 표준
  채널. 단일 채널 등록 금지 — B6 cryptographic 검증.
- 사전등록 문서는 (i) primary mapping 잠금, (ii) 부호-결정 매트릭스,
  (iii) 변환 prior 함수형 + 분포 출처, (iv) false-rate threshold,
  (v) sample lock (5 dSph + 제외 3개 사유), (vi) post-registration
  추가 dSph 정책 6항목 필수.
- paper §6.1 row #5 + §4 P9 row 의 동일-PR 갱신 (B8) — 사전등록 commit
  과 paper update commit 의 cross-reference 의무.

---

## NEXT_STEP / REVIEW 로 이행

- **NEXT_STEP**: 6항목 메타-거버넌스를 task list 로. dSph_PREREG.md draft
  의 섹션 골격 제시. paper/base.md §6.1 row #5 + §4 P9 row 의 정책
  추가 안 작성.
- **REVIEW**: 4인팀이 dSph_PREREG.md draft 의 *형식 적합성* 검토 — 4 조건
  잠금 진술이 모두 포함되어 있는지, triple-timestamp 채널이 명시되어
  있는지, post-registration 정책이 드리프트 방지 가능한지 자율 분담.
  *수치값* 은 검토 대상 아님 (CLAUDE.md [최우선-1] 준수).
