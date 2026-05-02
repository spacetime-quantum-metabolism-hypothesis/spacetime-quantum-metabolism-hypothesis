# L553 — MNRAS_DRAFT 0.42σ → 0.71σ 정정 검증 (4인 Rule-B)

세션: L553 (4인 Rule-B 시뮬, 단일 세션, 읽기/grep 만, **paper edit 0건**)
일자: 2026-05-02
대상:
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/paper/MNRAS_DRAFT.md`
- 디스크 사실 근거: `results/L550/A0_RECONCILIATION.md` (3-way concordance: 코드 + JSON + stdout 모두 0.71σ)

배경: L549 가 P3a priori 박탈. L550 가 디스크 사실 우선 0.71σ 채택 권고. 본 L553 은 paper edit *방향만* 명시 (실제 edit 은 8인 Rule-A 의무).

자율 분담 (역할 사전 지정 없음, 자연 발생):
- R1: paper grep / line context
- R2: 디스크 사실 cross-check (L550 결과 인계)
- R3: reviewer 신뢰 영향 평가
- R4: §4 / §5 추가 mismatch 탐색

---

## §1 "0.42σ" grep 위치 표 (paper/MNRAS_DRAFT.md)

| Line | Section | 컨텍스트 (인용) | 권고 정정 문장 (8인 Rule-A 입력용, 본 세션 적용 0건) |
|------|---------|---------------|-----|
| 14 | abstract / 위치 표시문 | "MOND a₀ 정량 PASS (verify_milgrom_a0.py: **0.42σ** deviation, PASS_STRONG)" | "MOND a₀ 정량 PASS (verify_milgrom_a0.py: **0.71σ** deviation, PASS)" — `0.42σ → 0.71σ`, `PASS_STRONG → PASS` (script verdict 와 정합; JSON `verdict: "PASS"` L43, stdout `PASS` 기준; abstract 의 PASS_STRONG 은 디스크 미산출) |
| 28 | §1 Introduction | "gives a **0.42σ** deviation. A reproducible single-file verification (...) is provided." | "gives a **0.71σ** deviation. A reproducible single-file verification (...) is provided." — 단일 토큰 치환 |
| 89 | §3.2 본문 괄호 | "(A second computation with the verification script's H₀=73 input and σ_a₀ = 0.1 × 10⁻¹⁰ yields **0.42σ**; cf. `paper/verification/verify_milgrom_a0.py`. The two agree within rounding; we adopt 0.71σ as the conservative number for the published table and **quote 0.42σ as the verification-script result**.)" | **괄호 전체 삭제 권고**. 사유: 디스크 verify_milgrom_a0.py 는 0.42σ 를 절대 출력하지 않음 (L550 §3 stdout 0.71σ). "verification-script result = 0.42σ" 는 거짓. L87 산수 "|1.129−1.20|/0.10=0.71σ" 와 L92 H₀=73→0.71σ 가 이미 본문에 있으므로 자체모순 괄호는 불필요. |

(L130 `"deviation_sigma": 0.71` JSON quote, L87 산수, L92 H₀ 의존성표 모두 디스크 정합 → 수정 불필요)

---

## §2 추가 mismatch 검색 결과 (§4 RAR / §5 falsifier / 기타)

R4 검토 — "0.42σ" 외 디스크 ↔ paper 정합 issue:

1. **L14 `PASS_STRONG` vs JSON `verdict: "PASS"`** (paper L131 본문 JSON snippet 도 `PASS_STRONG` 표기). 디스크 `expected_outputs/verify_milgrom_a0.json` 은 `verdict: "PASS"` (L550 §2 인용). 둘 다 동일 정정 라운드에서 처리 권고.
   - paper L14: "PASS_STRONG"
   - paper L131: `"verdict": "PASS_STRONG"` ← JSON snippet 본문
   - 디스크 JSON: `"verdict": "PASS"`
   - 권고: paper 본문 `PASS_STRONG → PASS` 일괄 (또는 디스크 JSON 을 `PASS_STRONG` 으로 업그레이드, 단 이는 코드 임계값 재정의 필요 → 8인 토의).

2. **§4.1 RAR universality** (L104): paper 본문은 "depletion-zone framework predicts ... monotonic μ" 정성 일치만 주장하므로 정량 mismatch 없음. **단**, `claims_status.json` L641–L644 가 "RAR a₀ NOT universal (per-galaxy spread 0.427 dex, K_X 1/4 PASS, environment FAIL — aggregate-only match)" 로 보편성 철회 등록 (L491/L492/L503). MNRAS_DRAFT §4.1 / §1 어디에도 "subset-stability ACK" 캐비엣이 없음 → **신규 mismatch 후보**. 8인 라운드에서 §4.1 말미에 "We acknowledge that aggregate-RAR a₀ match does not extend to per-galaxy / environment-stratified subsets (L491/L492/L503); universality is *not* claimed in this paper." 추가 권고.

3. **§4.3 Bullet** (L110): "we *do not* claim that this framework eliminates cluster dark matter" 명시 — 정직 한도 내. 추가 mismatch 없음.

4. **§5 falsifier** (L137 `verify_mock_false_detection.py`): "≥ 5σ deviation" 토큰의 디스크 산출값 본 세션에서 직접 재현 안 함 (scope 외). L550 도 mock 스크립트는 미실행. 차후 L554 등에서 cross-check 권고 (본 L553 에서 mismatch 단정 불가).

5. **L92 H₀=67.4 → 1.6σ low**: paper 산수 `(1.04 − 1.20)/0.10 = 1.6σ`. 손계산 `0.16/0.10 = 1.6` ✓. 정합.

6. **L87 산수**: `|1.129 − 1.20|/0.10 = 0.71σ` ✓. 정합.

→ 본 §1 의 3개 라인 (14/28/89) + §2.1 의 PASS_STRONG/PASS verdict + §2.2 의 RAR universality 캐비엣 부재가 본 라운드의 mismatch 전체.

---

## §3 reviewer 신뢰에 미치는 영향 (R3)

R3 평가 — 0.42σ ↔ 0.71σ 차이가 위치별 reviewer 영향:

1. **abstract (L14)**: 가장 치명적. MNRAS reviewer 가 abstract → §3.2 산수 (L87 0.71σ) → JSON snippet (L130 0.71) → 본문 자체모순 괄호 (L89) 순으로 읽으면 **첫 30초 내 충돌 발견**. abstract 가 0.42σ + PASS_STRONG, 본문 산수가 0.71σ + 본문 verdict 가 PASS 인 비대칭은 "저자가 자신의 산수도 검증 안 함" 신호 → reject 위험 매우 높음.

2. **§1 Introduction (L28)**: 역시 본문 산수와 직접 충돌. §3.2 L87 와 L28 사이 ~60줄 거리에서 0.42 vs 0.71 모순 → reviewer 가 "어느 게 진짜냐" 질문 자동 생성.

3. **§3.2 자체모순 괄호 (L89)**: 가장 위험. paper 가 "we adopt 0.71σ as conservative ... and quote 0.42σ as the verification-script result" 라고 명시하지만, 디스크 `verify_milgrom_a0.py` 는 0.42σ 를 절대 출력하지 않음 (L550 §1 코드 분석: `dev = abs(a0_SQT - a0_obs) / a0_err` 단일 경로, σ_obs=0.1×10⁻¹⁰ 단일 정의, Planck branch / σ_obs=0.05×10⁻¹⁰ option 부재). 즉 paper 가 "verification-script 결과"라고 부르는 0.42σ 는 **실재하지 않는 결과를 인용**. reviewer 가 clone → run → 0.71σ 만 출력되는 것을 확인하면 paper L89 진술 자체가 거짓 → MNRAS reviewer 입장에서 "data fabrication" 의심 트리거. **이 한 줄이 abstract 의 0.42σ 보다 더 위험**.

4. **abstract `PASS_STRONG` vs JSON `PASS`**: minor 대비 abstract 충돌. 단독으로는 reject 사유 아님.

5. **§4.1 RAR universality 캐비엣 부재**: claims_status.json 에 보편성 철회 기록되어 있는데 paper 본문에 ACK 없음 → 외부 reviewer 가 L491/L492/L503 결과를 모르면 발각 안 되지만, 추후 referee response 라운드에서 노출 시 신뢰 타격.

영향 가중 (R1–R4 합의 추정):
- L89 거짓 인용: **HIGH** (single-handed reject 가능)
- L14 / L28 0.42σ: **HIGH** (abstract-table 모순)
- L14 PASS_STRONG: **MEDIUM**
- §4.1 universality 캐비엣 부재: **MEDIUM** (referee round 위험)
- §5 mock falsifier 미검증: **LOW** (본 라운드 scope 외)

---

## §4 8인 Rule-A 의무: paper edit 트리거 조건

본 L553 은 4인 Rule-B (시뮬 / 코드 검증 / 디스크 fact-check) 한정. 다음 트리거 조건 충족 시 8인 Rule-A 라운드 의무:

**Trigger A (필수, 즉시)**: paper/MNRAS_DRAFT.md 의 §1 표 3개 라인 (L14, L28, L89) edit
- Rule-A 8인 순차 리뷰 필수 (이론적/포지셔닝 클레임 변경 = abstract 수정 = "PASS_STRONG → PASS" verdict 다운그레이드 포함)
- 사유: abstract / introduction / §3.2 narrative 모두 *논문 외부에 보이는 클레임 표면* → CLAUDE.md L6 규칙 "이론 클레임 → Rule-A 8인 순차 리뷰" 적용.

**Trigger B (조건부)**: §2.1 verdict 라벨 정정 (PASS_STRONG ↔ PASS)
- digital JSON `verdict` 필드는 코드 산출 + 임계값 정의 조합. 임계값 재정의 (예: < 1σ 를 PASS_STRONG 으로 격상) 시도는 "사후 임계값 조정" 으로 적합 안 함. → JSON 디스크 사실 (`PASS`) 을 paper 에 반영.
- 8인 라운드에서 단순 표기 정정으로 처리 가능.

**Trigger C (권고)**: §4.1 RAR universality ACK 캐비엣 추가
- claims_status.json 과 paper 본문 동기화. 8인 라운드에서 본문 한 줄 추가 권고 처리.

**Non-trigger (본 라운드 외)**:
- §5 mock falsifier 5σ 토큰 — L554+ 에서 별도 verify_mock_false_detection.py 디스크 검증 후 처리.
- L130 / L87 / L92 0.71 토큰 — 이미 디스크 정합, 수정 불필요.

**금지 (Rule-A 미경유)**:
- paper/MNRAS_DRAFT.md 직접 edit
- paper/base.md 직접 edit
- claims_status.json 직접 edit
- verify_milgrom_a0.py 코드 / 임계값 변경 (코드 변경은 별도 4인 Rule-B 라운드 + 8인 검토)

---

## 정직 한 줄

본 세션은 grep + L550 보고서 인계 + paper 본문 텍스트 분석만 수행했고, paper/MNRAS_DRAFT.md / paper/base.md / claims_status.json / verify_milgrom_a0.py 어느 디스크 파일도 수정하지 않았다. "0.42σ 는 verification-script 결과" 라는 paper L89 의 진술이 디스크 코드와 모순된다는 사실은 본 라운드의 가장 위험한 발견이며, 이를 정직하게 기록한다 — abstract / §1 / §3.2 의 정정은 8인 Rule-A 의무이고 본 4인 Rule-B 세션의 권한 밖이다.
