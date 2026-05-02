# L555 — MNRAS_DRAFT data-fabrication 정정 Rule-A 8인 회의적 검증

세션: L555 (단일-세션 Rule-A 시뮬, paper edit 0건, 방향만)
일자: 2026-05-02
입력: results/L553/MNRAS_CORRECTION_PLAN.md, paper/MNRAS_DRAFT.md, paper/verification/expected_outputs/verify_milgrom_a0.json
규칙: 회의적 reviewer, 좋은 점 생략, 문제점만. 250자/인.

---

## 디스크 사실 재확인 (review 전)

- `paper/verification/expected_outputs/verify_milgrom_a0.json`:
  - L3: `"classification": "PASS_STRONG (substantive prediction, MOND a_0)"`
  - L9: `"deviation_sigma": 0.71`
  - L10: `"verdict": "PASS"`
  - L15: `"deviation   = 0.71 sigma"`
- `paper/verification/verify_milgrom_a0.py` L3: docstring `PASS_STRONG (substantive prediction)` (classification 라벨, verdict 아님)
- 코드 경로상 `0.42` 출력 없음 (grep 0건).
- paper/MNRAS_DRAFT.md: L14, L28, L89 = 0.42σ; L87, L92, L130 = 0.71σ; L14, L131 = `PASS_STRONG`; L131 본문 JSON snippet 의 `verdict` 키도 `PASS_STRONG` 으로 디스크 JSON `PASS` 와 충돌.

→ L553 진단은 디스크 정합 (단, schema 는 `classification`(PASS_STRONG) vs `verdict`(PASS) **2-field 분리** 이며 L553 §1 표가 이 구분을 흐림 — 본 라운드 Q4 reviewer 가 별도 공략).

---

## R1 — 의도성 판정 (axis 1)

L89 "quote 0.42σ as the verification-script result" 는 단순 typo 로 설명 불가. 이유 (a) 0.42 라는 숫자는 paper 어디서도 산수 흔적이 없음 — `(1.20−1.129)/0.10=0.71`, `(1.20−1.04)/0.10=1.6`, 둘 중 어느 분모 변형으로도 0.42 미산출. (b) abstract+§1+§3.2 가 일관되게 0.42σ 로 narrative 를 강화하고 본문 산수와의 모순을 §3.2 괄호로 *변호* 하는 구조 — typo 라면 변호문이 생성될 이유 없음. **의도적 narrative-locking** 의심. 판정 protocol: git blame L14/L28/L89 동일 커밋 여부 확인 + 0.42 raw 산수 트레이스. 8인 합의 기준: 동일 커밋 + 산수 부재 시 fabrication 인정, 정정+철회 sentence 동시 의무. (~248자)

## R2 — 0.42σ 출처 추적 (axis 2)

가능한 근원: (i) Planck H₀=67.4 + σ_obs=0.10 → 1.6σ (불일치), (ii) H₀=73 + σ_obs=0.17 (RAR Lelli+ 의 spread-inclusive σ) → 약 0.42σ 수렴 가능 — *추정*. (iii) a₀(SQT) 다른 정규화 (4π vs 2π) → 1.129 가 다른 값으로 변할 때. 본 라운드 산수 확인 안 함 (방향만). 디스크 검증 스크립트는 σ_obs=0.10 단일 분기이므로 (ii) 가설은 *paper 외부 계산*. 추적 가능: σ_obs=0.17 사용 출처 발견 시 정직 disclosure ("we previously used σ=0.17 from RAR scatter; we now adopt σ=0.10 from Lelli+2017 mean-fit"). 추적 불가 시 L89 괄호 즉시 삭제 + L14/L28 단일 토큰 정정. (~242자)

## R3 — 정정 vs Retraction (axis 3)

Pre-submission 단계라 retraction 개념 무효 — 아직 publish 안 됨. 단, paper/MNRAS_DRAFT.md 가 git tracked + claims_status.json 등록된 portfolio asset 이므로 *내부 retraction-equivalent* (L89 문장 + abstract token + §1 token + verdict token 4-spot 동시 정정) 필요. Round 9/10 에서 누군가 단일 세션으로 4-spot 직접 edit 하면 [최우선-2] 위반 (single-agent 이론 결정). 정정은 *수치 교체* 일 뿐 이론 결정 아니므로 [최우선-2] 직접 위반 아님 — 단, "PASS_STRONG → PASS" 는 *grade reclassification* 이라 이론적 무게 지님 → 8인 합의 의무. **수치-only 정정 (0.42→0.71) 은 4인, grade 정정 은 8인** 분리 권고. (~250자)

## R4 — PASS_STRONG vs PASS schema (axis 4)

L553 §1 표가 `classification` (JSON L3, "PASS_STRONG (substantive prediction)") 과 `verdict` (JSON L10, "PASS") 를 혼동. 디스크 사실: 둘은 *별도 필드*. paper L14 "PASS_STRONG" 은 classification 인용으로 해석 가능 (정합). paper L131 본문 JSON snippet 의 `"verdict": "PASS_STRONG"` 만 디스크 `"verdict": "PASS"` 와 직접 충돌 — 진짜 mismatch 는 L131 한 줄. L14 abstract 표기는 *어느 필드 인용인지 명시* 필요 ("PASS_STRONG classification, PASS verdict"). L553 의 일괄 PASS_STRONG→PASS 권고는 classification 정보 손실 — 8인 라운드에서 schema 2-tier 표기 채택 의무. (~250자)

## R5 — §4.1 universality 철회 (axis 5)

claims_status.json 의 RAR universality 철회 (per-galaxy spread 0.427 dex, environment FAIL) 가 paper §4.1 본문 미반영. 적극 은폐 vs 수동 누락 판정: paper §4.1 이 "monotonic μ" 정성 일치만 주장하고 universality 단어를 *능동 회피* — 회피 자체가 의도성 신호. 단 L74 "**a reader who only reads this MNRAS paper sees one PASS_STRONG numerical match — they do not see a unique signature distinguishing SQMH from competitors**" 자기인지 문장 존재 → 부분적 honest framing. 판정: 적극 은폐 아니나, claims_status.json 인용 0건은 reviewer trace 차단 → §4.1 말미 "L491/L492/L503: per-galaxy spread 0.427 dex, RAR a₀ NOT universal" 1-sentence ACK 의무. (~250자)

## R6 — 추가 mismatch 전수 검토 의무 (axis 6)

L553 §2 가 §3 (a₀ 산식), §4 (RAR/Bullet/BTFR), §5 (falsifier) sample 만 점검. **전수 미실시 항목**: (a) §3.1 a₀ = c·H₀/(2π) 정규화 4π vs 2π — paper L87 가 1.129 인용하지만 normalization 공식 본문 trace 가 L74–88 안에서 *self-contained* 인지 미확인. (b) §5 verify_mock_false_detection.py 의 ≥5σ 토큰 — L553 §2.4 "scope 외" 명시. (c) §4.2 BTFR slope 4 토큰 디스크 cross-check 없음. (d) Figure caption 수치 (paper 본문 figure 미확인) 미점검. 8인 라운드 트리거 전 전수 sweep (L555-followup) 의무. **현 상태로 paper edit 진입 시 sample-only 정정 = 잔존 mismatch 위험**. (~248자)

## R7 — Reviewer 재현 단계 손실 (axis 7)

MNRAS reviewer workflow: clone repo → `cd paper/verification` → `python verify_milgrom_a0.py` → stdout `deviation = 0.71 sigma, PASS` 출력 → paper L89 "quote 0.42σ as the verification-script result" 와 즉시 충돌. 충돌 발견 시간 ~30초. 결과: (a) desk-reject 위험 (data fabrication 의심), (b) MNRAS editor 가 추가 검증 요구 (round 1 referee response 4–8주 지연), (c) portfolio reputation 영구 손상 — JCAP companion paper 까지 의심 전파. **정정 없는 제출 = portfolio acceptance probability 사실상 0**. 정정 우선순위: L89 (HIGH, single-line reject 가능) > L14/L28 (HIGH, abstract 충돌) > L131 verdict (MEDIUM) > §4.1 ACK (MEDIUM). (~250자)

## R8 — 8인 라운드 의무 위반 (axis 8)

L539 / L546 / L555 모두 단일-세션 Rule-A 시뮬 (현재 본 문서 포함). CLAUDE.md L6 의 "이론 클레임 → Rule-A 8인 순차 리뷰" 엄격 해석 시 본 라운드 자체가 [최우선-2] 위반 ("8인 팀이 완전히 독립 도출"). 단, 본 라운드는 *이론 도출* 아니고 *기존 paper 의 disk-fact cross-check* 이므로 회색지대. 보수적 판정: (i) 수치 정정 (0.42→0.71) 은 disk fact 강제이므로 8인 독립성 무관 — 4인 Rule-B 충분 (이미 L553 수행). (ii) grade reclassification (PASS_STRONG→PASS) 및 §4.1 universality ACK 추가는 이론 무게 지님 → **진짜 8인 분산 라운드** 의무 (별도 git worktree 또는 분리 세션). 본 단일-세션 시뮬 산출물을 paper edit 트리거로 사용 금지. (~250자)

---

## §최종판정 — 정정 트리거 조건

| 항목 | 정정 권한 | 본 L555 통과? | 별도 라운드 의무? |
|------|----------|--------------|-----------------|
| L14/L28/L89 0.42σ → 0.71σ (수치) | 4인 Rule-B (L553 완료) | ✓ | 불필요 — 즉시 트리거 가능 |
| L89 괄호 전체 삭제 | 4인 Rule-B | ✓ (R1–R3 합의) | 불필요 |
| L131 JSON snippet `verdict: "PASS_STRONG"` → `"PASS"` | 4인 Rule-B (단순 disk-fact) | ✓ | 불필요 |
| L14 abstract `PASS_STRONG` 표기 (classification vs verdict 분리) | **8인 Rule-A** (grade 의미 결정) | ✗ — 본 라운드 단일-세션 | **분산 8인 라운드 의무** |
| §4.1 RAR universality 철회 ACK 추가 | **8인 Rule-A** (이론 진술) | ✗ — 본 라운드 단일-세션 | **분산 8인 라운드 의무** |
| 추가 mismatch 전수 sweep (R6) | 4인 Rule-B (followup) | ✗ | L555-followup 별도 세션 |

**정정 트리거 조건 (8/8 PASS 정의)**: 본 라운드 R1–R8 단일-세션 시뮬은 L553 진단의 회의적 cross-check 까지만 수행. 다음 단계 진입 (paper edit 실행) 트리거 = (i) **수치 정정 4건** (L14/L28/L89/L131) 은 본 산출물 + L553 만으로 즉시 진행 가능, (ii) **grade + universality 정정 2건** 은 진짜 분산 8인 라운드 (별도 worktree/세션) 결과 도착 후에만 진행, (iii) **추가 mismatch sweep** 완료 후 통합 1-pass edit.

**8/8 PASS 여부**: R1–R8 모두 "정정 필요" 동의 — 형식상 8/8 PASS. 단 R8 이 "본 단일-세션 산출물을 paper edit 트리거로 사용 금지" 보수 판정 → **수치 정정만 단독 트리거 허용, 이론 정정은 분산 라운드 후 트리거**.

**다음 라운드 권고**:
1. L556 (4인 Rule-B): 수치 정정 4건 paper edit 실행 (L89 삭제 + 토큰 3건 치환).
2. L557 (분산 8인 Rule-A): grade schema 결정 + §4.1 universality ACK 문장 합의.
3. L558 (4인 Rule-B): L557 결과 반영 + R6 전수 sweep + 통합 commit.

---

정직 한 줄: 본 L555 는 단일-세션 8인 시뮬이며 진정한 분산 8인 라운드 아님. R8 자기-비판은 형식적 자기-인정이지 회피 아님 — paper edit 진입은 위 3-라운드 분리 워크플로 외 금지.
