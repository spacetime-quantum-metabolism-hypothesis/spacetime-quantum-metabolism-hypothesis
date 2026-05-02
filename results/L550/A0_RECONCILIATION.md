# L550 — verify_milgrom_a0.py 디스크 cross-check 재현 보고서

세션: L550 (4인 Rule-B 시뮬, 단일 세션, 코드 읽기/실행만, 파일 수정 0건)
일자: 2026-05-02
대상 파일:
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/paper/verification/verify_milgrom_a0.py`
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/paper/verification/expected_outputs/verify_milgrom_a0.json`
- 참조: `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/paper/MNRAS_DRAFT.md`

목적: paper §3.2 "0.42σ" vs 자체 검증 "0.71σ" 충돌을 디스크 사실로 결정.

---

## §1 코드 로직 (verify_milgrom_a0.py)

전체 20줄, 의존성 numpy 단독, 외부 데이터 호출 없음. 핵심 입력/출력:

| 항목 | 값 / 정의 | 코드 라인 |
|------|----------|-----------|
| `c` | 2.998e8 m/s | L8 |
| `H0` | `73e3 / 3.086e22` s⁻¹ (= H₀ = **73.0** km/s/Mpc, SH0ES 2022) | L9 |
| `a0_SQT` 공식 | `c * H0 / (2π)` | L11 |
| `a0_obs` | 1.2e-10 m/s² (Begeman+ 1991, Famaey-McGaugh 2012) | L12 |
| `a0_err` | **0.1e-10** m/s² (= 1.0e-11; RAR M16 / Lelli+ 2017 fit unc.) | L13 |
| `dev` (residual 정의) | `abs(a0_SQT - a0_obs) / a0_err` (절대 차이를 1σ 단위로 환산) | L15 |
| PASS 판정 | `dev < 2` | L19 |

핵심: H₀=73 입력, σ_obs=0.1×10⁻¹⁰ 단일 정의. Planck H₀=67.4 branch 코드 미포함.

---

## §2 expected_outputs JSON 디스크 값

`paper/verification/expected_outputs/verify_milgrom_a0.json` (19줄) 디스크 그대로:

```json
{
  "expected": {
    "a0_SQT_m_s2": 1.129e-10,
    "a0_obs_m_s2": 1.2e-10,
    "a0_err_m_s2": 1.0e-11,
    "deviation_sigma": 0.71,
    "verdict": "PASS"
  },
  "stdout_lines": [
    "a_0 (SQT)   = 1.129e-10 m/s^2",
    "a_0 (obs)   = 1.200e-10 +/- 1e-11",
    "deviation   = 0.71 sigma",
    "PASS"
  ]
}
```

JSON 디스크는 **0.71σ 단일 값**만 명시. 0.42σ 흔적 없음.

---

## §3 실제 실행 stdout

명령: `python3 paper/verification/verify_milgrom_a0.py`
런타임: < 0.1 s

```
a_0 (SQT)   = 1.129e-10 m/s^2
a_0 (obs)   = 1.200e-10 +/- 1e-11
deviation   = 0.71 sigma
PASS
```

JSON expected stdout 와 line-by-line 완전 일치.

수동 산수 검증:
- H₀ = 73e3 / 3.086e22 = 2.3655e-18 s⁻¹
- a₀_SQT = 2.998e8 × 2.3655e-18 / (2π) = 1.1287e-10 m/s² ≈ 1.129e-10 ✓
- |1.129 − 1.200| / 0.10 = 0.071 / 0.10 = **0.71** ✓ (단위 10⁻¹⁰)

---

## §4 4인 자율 분담 검토 (Rule-B, 역할 사전 지정 없음)

자율 분담 결과 (자연 발생):

- **R1 (코드 정합성)**: verify_milgrom_a0.py L8–L19 검토. 입력 H₀=73, σ=0.1e-10 하드코딩 확인. Planck 67.4 branch 없음, σ를 0.05×10⁻¹⁰ 으로 좁히는 옵션 없음. → 코드는 단일 0.71σ 만 출력.
- **R2 (JSON 정합성)**: expected_outputs JSON `deviation_sigma: 0.71` 단일 값. 0.42σ 키 부재. stdout_lines 도 0.71. → JSON disk 진실은 0.71σ.
- **R3 (산수 재현)**: 손계산 0.71σ 일치, 실행 stdout 0.71σ 일치, JSON 0.71σ 일치 → 3-way concordance.
- **R4 (paper 본문 충돌 매핑)**: MNRAS_DRAFT.md 검색 결과:
  - L14: "0.42σ deviation, PASS_STRONG" — abstract/intro 인용
  - L28: "gives a 0.42σ deviation" — §3.2 본문
  - L87: "|1.129 − 1.20| / 0.10 = 0.71σ" — §3.2 산수 표기
  - L89: "(... script 0.42σ; we adopt 0.71σ as the conservative number for the published table and quote 0.42σ as the verification-script result)" — 자체 모순 인정
  - L92: "With H₀=67.4 → 1.6σ low. With H₀=73.0 → 0.71σ" — H₀ 의존성 명시
  - L130: JSON-quoted block "deviation_sigma: 0.71"

  → 본문 산수, table snippet, JSON quote 는 모두 **0.71σ**. "0.42σ" 는 abstract / intro / §3.2 도입부 narrative 에만 잔존하며 디스크 어디에도 근거가 없음. paper 자체가 L89 에서 "0.42σ 와 0.71σ 가 둘 다 verification-script 결과"라고 잘못 기술하지만, 디스크 verify_milgrom_a0.py 는 0.42σ 를 절대 출력하지 않음.

4인 합의: paper 본문의 "0.42σ" 는 **disk 근거 없는 stale 숫자** (이전 σ_obs=0.17×10⁻¹⁰ 가정 또는 다른 H₀ 입력의 잔재 추정). 디스크 verify_milgrom_a0.py + JSON 모두 0.71σ.

---

## §5 결정: paper 본문 cite 값 = **0.71σ**

### 사유
1. **디스크 코드 (verify_milgrom_a0.py)**: 0.71σ 단일 출력. 다른 값 산출 경로 없음.
2. **디스크 JSON (expected_outputs/verify_milgrom_a0.json)**: `deviation_sigma: 0.71` 단일 명시.
3. **실제 실행 stdout**: 0.71σ.
4. **paper 자체 산수 (L87)**: 0.71σ.
5. **L546 portfolio plan §2.2 / §3.2 권고**: "0.71σ 단일 채택 확정 — expected_outputs JSON cross-check 의무" — 본 검증으로 충족.
6. **재현성 (MNRAS reviewer 관점)**: reviewer 가 clone → run → 0.71σ 만 본다. abstract 의 0.42σ 를 보고 cross-check 하면 즉시 충돌 발견 → reject 위험.

### 다음 라운드 (8인 Rule-A) 권고 사항 (참고용, 본 세션 실행 없음)
- abstract L14, §3.2 도입 L28 의 "0.42σ" → "0.71σ" 일괄 수정
- L89 의 자체모순 괄호("we adopt 0.71σ ... and quote 0.42σ as the verification-script result") 전면 제거 — 0.42σ 는 verification-script 결과가 아님
- L92 의 H₀ 의존성 표 (67.4 → 1.6σ low, 73.0 → 0.71σ) 는 디스크 사실 정합 → 유지

본 결정은 어디까지나 **디스크 verify_milgrom_a0.py + JSON + stdout 의 3-way 합의** 에 근거. paper edit 은 L550 scope 외 (다음 8인 라운드).

---

## 정직 한 줄

본 세션은 코드/JSON 읽기 + 1회 실행 + paper grep 만 수행했고, paper 본문 / MNRAS_DRAFT.md / verify_milgrom_a0.py / JSON 어느 파일도 수정하지 않았다. "0.42σ" 가 디스크 어디에서도 산출되지 않는다는 사실은 이번 세션의 가장 단단한 발견이며, paper 의 abstract/intro 가 디스크와 불일치한다는 점을 정직하게 기록한다.
