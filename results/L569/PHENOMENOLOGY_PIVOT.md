# L569 — SQT Paper Positioning: Phenomenology Pivot (Direction-Only)

> **본 문서는 *방향* 만 제공한다. 수식 0줄, 파라미터 값 0개, 실제 paper/CLAUDE.md/claims_status.json edit 0건.**
> **본 전환은 단일 에이전트 결정 금지 — 8인 Rule-A 합의 의무 (CLAUDE.md [최우선-2]).**

---

## §1. 전환 의미 표

| 축 | 종전 (priori 회복 trajectory 가정) | L569 이후 (phenomenology 영구 전환) |
|---|---|---|
| 야심 수준 | "통합 이론 (unified framework)" | "phenomenological framework" |
| 자유도 광고 | "0 free parameter (priori 도출)" | "hidden DOF disclosed" (정직 공개) |
| 도출 주장 | "first-principles priori derivation" | "consistency check + falsifier-driven phenomenology" |
| 학술지 타깃 | PRD Letter 진입 가능 (Q17/Q13/Q14 동시 충족 시) | PRD Letter 진입 *영구 차단*; JCAP / PRD Long-form / EPJC 트랙 |
| 평가 등급 어휘 | PASS_STRONG enum 사용 가능 (priori 회복 시) | PASS_STRONG 사용 영구 0; PASS_PHENOM / PASS_WEAK / PROVISIONAL 만 |
| 박탈 path 기록 | (해당 없음) | L549 P3a / L552 RG 패키지 / L562 D4 / L566 D2 default — 4건 영구 박탈 명시 |

**전환의 핵심 의미**: SQT 는 "왜 이 값인가" 를 first-principles 로 답하지 않는다. 대신 "이 phenomenology 가 어떤 falsifier 에서 살아남는가" 를 답한다.

---

## §2. paper / claims_status / README 영향 (방향)

### 2.1 paper/base.md abstract (직접 edit 금지, *방향* 만)
- "통합 이론" / "unified framework" / "first-principles" / "priori derivation" 어휘 → **본문 사용 금지**
- 대체 어휘 *방향*: "phenomenological consistency framework", "falsifier-driven model", "post-hoc parameter constrained by data"
- "0 free parameter" 광고 문구 → "disclosed hidden degrees of freedom" 로 정정 *방향*
- abstract 내 priori 도출 claim 전 항목 → consistency check claim 으로 격하 *방향*

### 2.2 claims_status.json schema
- **PASS_STRONG enum 사용 영구 0** 명시화 *방향*
- 새 enum *방향*: PASS_PHENOM (phenomenology 통과), PASS_WEAK (조건부), PROVISIONAL (data-pending), KILLED
- 기존 PASS_STRONG 항목 (있다면) → PASS_PHENOM 강등 *방향*
- L549/L552/L562/L566 박탈 이력을 metadata 필드로 영구 기록 *방향*

### 2.3 README.md hook
- "통합 framework" / "unified theory" / "from-scratch derivation" 문구 정정 의무 *방향*
- 대체 hook *방향*: "falsifier-driven cosmological phenomenology with disclosed parameter budget"
- DR3 (2027 Q2) 대기 강화 트랙 명시 *방향*

---

## §3. CLAUDE.md 등록 권고

### 3.1 1줄 등록 권고 (재발방지 섹션 추가 *방향*)
> "L569 — SQT 포지셔닝: phenomenology 영구 전환. priori 도출 회복 path 4건 박탈 (L549/L552/L562/L566). PRD Letter 진입 영구 차단. '통합 이론' / 'priori 도출' / '0 free parameter' 어휘 paper 본문 사용 금지. PASS_STRONG enum 사용 영구 0."

### 3.2 별도 § 추가 권고 (옵션)
> "## L569 재발방지 (포지셔닝 phenomenology 영구 전환)" 섹션을 신설하여,
> - 박탈 path 4건 timeline,
> - 어휘 금지 목록 (방향만),
> - claims_status enum 정책,
> - PRD Letter 차단 조건 명시
> 를 묶어 등록할 것을 권고. 단, **실제 CLAUDE.md edit 은 8인 Rule-A 합의 후 별도 세션**.

---

## §4. 장기 trajectory + 옵션 C (arXiv D 격상) 정합

### 4.1 phenomenology 전환 후의 글로벌 고점 추구 path
1. **falsifier 누적 통과 트랙**: DR3 / Roman / Euclid / LiteBIRD 단계별 falsifier 등록 → 통과 시 *경험적* 강화 (priori 도출과 무관). "왜 이 값인가" 는 답 못 해도, "이 값이 다음 falsifier 에서도 살아남았다" 는 누적 가능.
2. **공동 phenomenology 수렴**: 다른 dark sector phenomenology (Maggiore-Mancarella RR, f(Q), disformal) 와의 *경험적 구분 불능* 영역에서 공통 fitting template 의 "대표 representative" 지위 추구. (cf. L5 SVD n_eff=1 alt-20 cluster 교훈.)
3. **수정-from-below**: SQT framework 가 *예측력* 면에서 LCDM 보다 약간이라도 우위를 보이는 영역 (e.g. DESI-like w_a<0 자연성) 을 누적 evidence 로 축적 → "phenomenology 임에도 불구하고 데이터 선호" 트랙.

### 4.2 옵션 C (arXiv D 격상) 와의 정합
- L565 옵션 C 는 priori 회복 path 가 *모두* 막혔을 때 arXiv preprint D 트랙 (long-form, peer-review 우회) 으로 격상.
- L569 phenomenology 영구 전환은 옵션 C 의 *전제조건* 을 충족 — 4건 박탈 완결 시 옵션 C 활성화 자연스러움.
- 정합 *방향*: paper 본문은 phenomenology 어휘로 통일, arXiv 메타데이터 카테고리는 astro-ph.CO primary + gr-qc secondary 유지.

### 4.3 DR3 (2027 Q2) 결과 시 분기
- **DR3 통과**: phenomenology 의 *경험적 강화* — paper revision 트랙으로 evidence 누적. PRD Letter 진입 여전히 차단 (priori 도출 미달).
- **DR3 KILL**: SQT phenomenology 자체 박탈 — paper 의 falsifier 등록 항목으로 정직 종결 기록. 옵션 C 도 자연 종결.
- **DR3 모호**: provisional 상태 유지, Roman/Euclid 대기.

---

## §5. Rule-A 합의 의무 명시

- 본 phenomenology 영구 전환은 **단일 에이전트 결정 금지** ([최우선-2] 원칙).
- 8인 팀 Rule-A 순차 리뷰 의무. 안건 등록 *방향*:
  - **Round 9 또는 Round 10 안건**: "L569 phenomenology 영구 전환 + CLAUDE.md 등록 + paper 어휘 정정"
  - 8인 합의 도달 후 *별도 세션* 에서 paper / CLAUDE.md / claims_status.json edit 수행.
  - 본 L569 산출물은 *방향* 문서이며, 실제 코드/문서 변경 0건 유지.
- 4인 Rule-B 별도 의무: claims_status.json schema 변경 (enum 추가/제거) 은 코드 변경이므로 4인 코드리뷰 추가 의무.

---

## §6. 정직 한 줄

SQT 는 "왜" 를 답하지 못한다 — phenomenology 영구 전환은 야심의 패배가 아니라 정직의 승리다.

---

**산출물 끝. 실제 edit 0건. 8인 Rule-A 합의 대기.**
