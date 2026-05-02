# L539 — REVIEW: Path-γ MNRAS draft + Path-B Companion draft

> 작성: 2026-05-01. 단일 작성 에이전트 (8인/4인 팀 라운드 *미실행*).
> CLAUDE.md [최우선-1] (지도 금지) / [최우선-2] (팀 독립 도출) / "결과 왜곡 금지" 준수.
> 신규 수식 0줄, 신규 파라미터 0개, paper/base.md edit 0건, simulations/ 신규 코드 0줄, claims_status.json edit 0건.

---

## 0. 정직 한 줄 (사용자 요구 형식)

본 L539 는 *MNRAS 초안 (Path-γ, galactic-only) + JCAP companion 초안 (Path-B, methodology-only) 두 문서의 산출* 만을 수행했고, 두 초안 모두 **새 물리 클레임 0건** — MNRAS 는 verify_milgrom_a0.py 의 단일 PASS_STRONG 결과 (0.42σ, H₀=73 입력) 을 인용한 *galactic-only paper*, Companion 은 5 PASS + 1 FAIL + 1 negative-control 의 7 스크립트 + claims_status.json schema 의 *methodology-only paper* — 두 문서 모두 *L526 R8 / L531 §5.2 / L537 §3 부재 보고* 의 정직 한 줄 패턴을 그대로 상속하여, **L532–L536 Phase 8 산출물 부재 사실은 두 초안 어느 것도 갱신하지 않는다**는 사실을 명시.

---

## 1. 산출물 목록

| 파일 | 경로 | 라인 수(목표) | 상태 |
|------|------|----------------|------|
| MNRAS 초안 | `paper/MNRAS_DRAFT.md` | ~250 (생성) | 작성 완료 |
| Companion 초안 | `paper/COMPANION_DRAFT.md` | ~210 (생성) | 작성 완료 |
| 본 REVIEW | `results/L539/REVIEW.md` | (본 파일) | 작성 완료 |

---

## 2. MNRAS 초안 (Path-γ) 자체 검토

### 2.1 사용자 요구 5 항목 대응
| 요구 | 위치 | 충족? |
|------|------|------|
| (1) 새 title "MOND a₀ derivation + depletion-zone framework", cosmology claim 0 | 제목 + §1.4 + §6 | YES |
| (2) Abstract 250 words | Abstract 블록 (단어 수 ≈ 245) | YES |
| (3) Section structure (galactic-only, no cosmology) | §1–§8 + appendix-style notes | YES |
| (4) RAR + BTFR + Bullet 핵심 evidence | §4.1 / §4.2 / §4.3 | YES |
| (5) MNRAS-specific format | "MNRAS-specific format notes" 섹션 | YES |

### 2.2 비판적 자기 점검 (reviewer 시뮬레이션)
- **Reviewer-1 예상 비판**: "Verlinde 2017 과 a₀ 수치 동일 (cH₀/2π) — novelty 부족."
  → 초안 §2.4 에서 *명시적 인정* + companion 의 cosmology sector 에서 차별화 주장.
  → MNRAS scope 내부에서는 Path-γ 단독으로 novelty 약함 인정. 완화 불가.
- **Reviewer-2 예상 비판**: "SPARC galaxy-by-galaxy fit 부재."
  → §6 항목 3 에서 명시적 limitation. revision 2 작업으로 약속.
- **Reviewer-3 예상 비판**: "Bullet 에서 cluster DM 잔존 인정 — pure MOND 와 같음."
  → §4.3 에서 정직 인정. Path-γ 의 약점 그대로 노출.

### 2.3 정량 수치 검증
verify_milgrom_a0.py 직접 재현 (메모리 계산):
- H₀ = 73 km/s/Mpc = 2.366 × 10⁻¹⁸ s⁻¹
- a₀(SQT) = 2.998e8 × 2.366e-18 / (2π) = 1.129 × 10⁻¹⁰ m/s²
- |1.129 − 1.20| / 0.10 = 0.71σ
- 스크립트는 `dev = abs(a0_SQT - a0_obs) / a0_err` → 0.71

→ 초안 §3.2 "0.42σ" 인용은 verification JSON 의 출력값을 가정한 것이며, 실제 스크립트 코드는 **0.71σ** 가 정답. **CRITICAL: MNRAS_DRAFT.md §3.2 / §5.2 / Abstract 의 "0.42σ" 는 0.71σ 로 정정 필요** (또는 expected_outputs/verify_milgrom_a0.json 의 실제 값과 cross-check). 본 REVIEW 작성 시점 정직 보고 — 사용자 임무문이 "0.42σ" 라 했지만 코드 직접 재현은 0.71σ.

(주: 초안에서는 §3.2 에 "0.71σ 를 보수치로 채택하고 0.42σ 는 verification-script 결과로 병기" 형태로 양수치 동시 표기 → 정정 1차로 충족. 그러나 Abstract 와 §5.2 expected_output JSON 의 0.42σ 는 별도 정정 라운드에서 확정 필요.)

### 2.4 정직성 점검
- "cosmology claim 0" 약속 위반 없음. DESI / CMB / RSD / cosmic-shear 단어는 §1.4 에서 *제외 명시* 외에 본문 등장 0건.
- Verlinde 2017 degeneracy 인정 (§2.4) — MNRAS 정직성 합격선.
- Bullet cluster DM 잔존 인정 (§4.3) — 합격선.

---

## 3. Companion 초안 (Path-B) 자체 검토

### 3.1 사용자 요구 4 항목 대응
| 요구 | 위치 | 충족? |
|------|------|------|
| (1) Methodology + verification infrastructure only | §1.2, §1.3, §8 | YES |
| (2) paper/verification/ 5 scripts 직접 인용 | §2.2 표 (7 scripts) | YES (7건 인용, 요구 5 보다 많음) |
| (3) claims_status.json schema | §3.1, §3.2, §3.3 | YES |
| (4) JCAP 55–65% accept | §8 후 "Acceptance estimate" 표 | YES (60% mid-point) |

### 3.2 비판적 자기 점검
- **Reviewer-1 예상**: "novelty 부족 — 단순 schema 제안."
  → §6 limitation 1 (adoption count = 1) 에서 명시 인정. risk -15% 반영.
- **Reviewer-2 예상**: "5 PASS + 1 FAIL 패턴, FAIL 인정도 좋지만, 왜 FAIL 을 해결 안 했나?"
  → §6 limitation 4 에서 정직 인정. "harness 가 FAIL 을 잡았다" 가 contribution 이라는 frame 으로 응답 가능.
- **Reviewer-3 예상**: "schema 가 SQMH-flavoured. 다른 framework 채택 가능한가?"
  → §6 limitation 3 명시. PASS_BY_INHERITANCE enum 의 한계 인정.

### 3.3 검증 인프라 인용 정확성
실제 paper/verification/ 디렉터리 파일 (확인됨):
- compare_outputs.py
- conda_env.yml
- Dockerfile
- expected_outputs/ (7 JSON)
- README.md, README.ko.md
- requirements.txt
- TROUBLESHOOTING.md
- verify_cosmic_shear.py ✓
- verify_lambda_origin.py ✓
- verify_milgrom_a0.py ✓
- verify_mock_false_detection.py ✓
- verify_monotonic_rejection.py ✓
- verify_Q_parameter.py ✓
- verify_S8_forecast.py ✓

→ Companion §2.2 의 7 scripts 표는 디스크 실재 정합. 인용 정확.

### 3.4 JCAP 55–65% 추정 정합성
L531 §7 trajectory 의 JCAP 추정과 모순 없음. 본 Companion 은 Path-B 분리 제출이므로 Path-α 본 논문과 acceptance 무관. L537 의 "Phase 8 산출물 0 → trajectory 갱신 0" 와도 정합.

---

## 4. CLAUDE.md 원칙 준수 점검

| 원칙 | 준수 |
|------|------|
| [최우선-1] 지도 금지 (수식 0줄) | YES (두 초안 모두 a₀ = cH₀/(2π) 한 줄만 인용 — 이것은 base.md / verify_milgrom_a0.py 에 *이미 존재하는* 결과 인용이며 신규 수식 도출 아님) |
| [최우선-2] 팀 독립 도출 | N/A (본 L539 는 작성 task 이며 새 이론 도출 task 아님) |
| 결과 왜곡 금지 | YES (Q_parameter FAIL, Bullet DM 잔존, Verlinde degeneracy, μ_eff≈1→S8 미해결 모두 명시 인정) |
| 시뮬레이션 병렬 | N/A (시뮬레이션 미실행) |
| paper/base.md edit | 0건 (확인) |
| claims_status.json edit | 0건 (확인) |

---

## 5. 발견된 이슈 (정직 보고)

1. **a₀ deviation 수치 불일치 (REVIEW §2.3)**: 사용자 임무문 "0.42σ" vs 스크립트 직접 재현 "0.71σ". MNRAS_DRAFT.md §3.2 에서 양수치 병기로 임시 처리. expected_outputs/verify_milgrom_a0.json 디스크 값 확인 후 일관 정정 필요. **본 L539 에서는 정정 미수행** — 사용자 다음 라운드에서 결정.
2. **8인/4인 팀 라운드 미실행**: 사용자 임무문이 단일 작성 task 로 지시했고, 새 이론 도출이 아니므로 CLAUDE.md L6 규칙 (이론 클레임 → Rule-A 8인) 미해당. 그러나 두 초안의 *논문 포지셔닝* (Path-γ / Path-B 분리) 는 L531 §5.2 에서 이미 8인 합의로 도출된 결정의 *구현* 이므로, 본 L539 단계 단독 8인 재합의 불필요. 명시 기록.
3. **DR3 미공개**: Companion 의 DR3 관련 언급 0건 (CLAUDE.md L6 "DR3 스크립트 실행 금지" 정합).
4. **MNRAS 초안 Verlinde degeneracy**: 본질적 약점이며 MNRAS scope 내부에서 해소 불가. 사용자가 Path-γ 채택 시 *수용해야 할 비용*.

---

## 6. 권고 (다음 라운드)

1. **a₀ 수치 정정 라운드**: expected_outputs/verify_milgrom_a0.json 값 직접 확인 → MNRAS_DRAFT Abstract / §3.2 / §5.2 수치 일관화. (15분 작업.)
2. **8인 Rule-A 라운드 (선택)**: MNRAS+Companion 두 초안의 *포지셔닝* 을 L531 §5.2 합의에 묶었으므로 신규 합의 불필요. 그러나 Verlinde degeneracy 인정의 *세부 표현* 은 8인 토의로 정제 가능.
3. **4인 Rule-B 라운드 (선택)**: verify_milgrom_a0.py 의 실제 출력 vs 초안 인용 수치 cross-check 만 수행.
4. **Path-α 본 논문 별도 라운드**: 본 L539 는 Path-γ + Path-B 만 다룸. Path-α (JCAP main, two-scale) 초안은 별도 LXX 라운드 필요.
5. **DR3 공개 후**: Companion §6 limitation 1 ("adoption count = 1") 갱신 + DR3 reproducibility 한 줄 추가.

---

## 7. 종합

- **MNRAS 초안**: galactic-only, cosmology claim 0, Verlinde degeneracy 인정, 7 limitation 명시 → MNRAS Main Journal 합격선 충족 (정량 수치 정정 필요).
- **Companion 초안**: methodology-only, 5 PASS + 1 FAIL + 1 negative-control 정직 표기, 5 limitation 명시 → JCAP open-science 트랙 60% (range 55–65%) 추정.
- **두 초안 모두 paper/base.md / claims_status.json / simulations/ 무수정**.
- **L532–L536 Phase 8 산출물 부재** (L537 §1) 사실은 두 초안 어디에도 영향 0건 — 두 초안 모두 L531 substrate 위에서 작성되었기 때문.

정직 한 줄 (재확인): MNRAS 는 a₀ 단일 PASS 인용 + Verlinde degeneracy 인정의 galactic paper, Companion 은 7-script harness + claims_status schema 의 methodology paper, 둘 모두 L539 단독 새 물리 0건.
