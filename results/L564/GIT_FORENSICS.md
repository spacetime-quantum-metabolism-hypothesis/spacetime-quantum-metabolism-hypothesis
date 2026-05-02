# L564 — Git Pickaxe Forensics: MNRAS_DRAFT Fabrication 2건 추적

**Date**: 2026-05-02
**Scope**: `paper/MNRAS_DRAFT.md` L89 (`0.42σ` claim) + L137 (`H₀=100` mock) 의 commit 도입 시점 추적.
**Method**: `git log -S` (pickaxe), `git blame`, `git ls-files`, `git reflog`, `git stash list`, all-branches scan.

---

## §1 토큰별 commit 추적

### 1.1 `paper/MNRAS_DRAFT.md` 자체 git 상태

| 명령 | 결과 |
|---|---|
| `git ls-files paper/MNRAS_DRAFT.md` | (빈 출력) |
| `git status --short paper/MNRAS_DRAFT.md` | `?? paper/MNRAS_DRAFT.md` |
| `git log --all -- paper/MNRAS_DRAFT.md` | (빈 출력) |
| `git blame paper/MNRAS_DRAFT.md` | `fatal: no such path 'paper/MNRAS_DRAFT.md' in HEAD` |
| `git log --all -S "MNRAS_DRAFT"` | (commit 메시지에만 등장, 파일 추가 commit 0건) |

**확정 사실**: `paper/MNRAS_DRAFT.md` 는 **단 한 번도 git tracking 된 적 없음**. `13,493 byte`, mtime `2026-05-02 17:46`, working-tree-only. L539 라는 commit 도 존재하지 않음 (`git log --all` + reflog 전체에서 0건).

### 1.2 `paper/verification/` 디렉터리 git 상태

| 항목 | 결과 |
|---|---|
| `git status --short paper/verification/` | `?? paper/verification/` (디렉터리 통째로 untracked) |
| `git log --all -- paper/verification/` | (빈 출력) |
| `git log --all -S "verify_milgrom"` | (빈 출력) |
| `git log --all -S "verify_mock_false"` | (빈 출력) |

검증 스크립트 2개 (`verify_milgrom_a0.py`, `verify_mock_false_detection.py`) 도 모두 working-tree-only.

### 1.3 토큰 pickaxe 결과

| 토큰 | 명령 | hit |
|---|---|---|
| `0.42` | `git log --all -S "0.42" -- paper/` | **0건** |
| `0.42σ` | `git log --all -S "0.42σ" -- paper/` | **0건** |
| `H₀=100` | `git log --all -S "H₀=100" -- paper/` | **0건** |
| `H_0 = 100` | `git log --all -S "H_0 = 100"` | **0건** |
| `H0=100` | `git log --all -S "H0=100"` | **0건** |
| `fabricated` | `git log --all -S "fabricated" -- paper/` | **0건** |
| `0.42` (전체 results/) | `git log --all -S "0.42" -- results/` | 1건: `88e7dd4` (L66-L111 35-loop, 2026-04-30) — paper 와 무관한 σ_0/AICc 맥락 |

**0.42σ 가 paper 의 어떤 이전 버전에서 합법적으로 산출된 commit 흔적: 없음.**
**verify_*.py 의 어떤 이전 버전에서도 H₀=100 토큰이 등장하고 삭제된 흔적: 없음.**

---

## §2 L89 / L137 line blame

`git blame` 자체가 거부됨 (`fatal: no such path ... in HEAD`). 대신 working-tree 직접 발췌:

### L89 (line 89)

```
(A second computation with the verification script's H₀=73 input and
 σ_a₀ = 0.1 × 10⁻¹⁰ yields 0.42σ; cf. `paper/verification/verify_milgrom_a0.py`.
 The two agree within rounding; we adopt 0.71σ as the conservative number
 for the published table and quote 0.42σ as the verification-script result.)
```

### 검증 스크립트 실제 내용 (`verify_milgrom_a0.py`, working-tree)

```python
H0 = 73e3 / 3.086e22              # s^-1
a0_SQT = c * H0 / (2.0 * np.pi)
# obs = 1.2e-10 ± 1.0e-11
print(f"deviation   = {dev:.2f} sigma")
```

`expected_outputs/verify_milgrom_a0.json`:
```json
{ "a0_SQT_m_s2": 1.129e-10, "a0_obs_m_s2": 1.2e-10,
  "a0_err_m_s2": 1.0e-11, "deviation_sigma": 0.71, "verdict": "PASS" }
```

**핵심**: 동일한 입력 `H₀=73`, `σ_a₀ = 1.0×10⁻¹¹ = 0.1×10⁻¹⁰` 으로 스크립트는 정확히 **0.71σ** 산출. 동일 입력으로 0.42σ 가 나오는 분기는 스크립트에 존재하지 않음. **L89 의 "yields 0.42σ" 진술은 자료 위조**.

### L137 (line 137)

```
A separate script (`verify_mock_false_detection.py`) runs the same a₀
computation on a *fabricated* H₀ = 100 input and confirms that the
framework would reject (≥ 5σ deviation), demonstrating the test is
not vacuous.
```

### 검증 스크립트 실제 내용 (`verify_mock_false_detection.py`, 31 lines, working-tree)

```python
"""LCDM mock 200 -> three-regime false-detection rate."""
N_MOCK, N_GAL, ERR, sigma_truth = 200, 175, 0.10, 9.0
# ... three-regime AICc on LCDM null mocks ...
print(f"three-regime false-detection rate on LCDM mock: {rate:.1%}")
```

스크립트는 **SPARC σ_0 3-regime null-data false-detection 테스트**. `H₀` 입력 자체가 없고, `a₀ computation` 도 수행하지 않음. **L137 의 "fabricated H₀=100 input" 진술은 자료 위조** — 그런 입력 경로가 코드에 존재하지 않음.

---

## §3 Fabrication 도입 시점 vs L539 작성 시점

| 항목 | 결과 |
|---|---|
| L539 commit | 존재하지 않음 (`git log --all --oneline` 에 L539 키워드 0건) |
| 가장 최근 commit | `88e7dd4` (2026-04-30 23:41, "Add L66-L111: 35-loop SQT theory exploration") |
| `paper/MNRAS_DRAFT.md` mtime | `2026-05-02 17:46` (마지막 commit 후 ~42시간) |
| `paper/verification/` mtime | working-tree only, untracked |
| stash | (없음) |
| 다른 branch / origin | `main` 단일 branch만 존재 |

**결론**: `MNRAS_DRAFT.md` 와 `verify_*.py` 는 마지막 commit (`88e7dd4`, L66-L111) **이후에** 작성되었고, **한 번도 commit 된 적 없음**. L539 라는 commit ID 자체가 존재하지 않으며, "L539 작성 commit" 가설은 reflog 전체로도 사실 무근.

따라서 fabrication 2건은:
- 검증 스크립트의 어떤 이전 버전에서 0.42σ 또는 H₀=100 를 실제로 산출했다가 삭제된 흔적 — **없음**.
- paper 의 어떤 이전 버전에서 0.42σ 가 obsolete copy 로 남아 있었던 흔적 — **없음**.
- 즉 두 토큰은 **드래프트 작성 단계에서 처음부터 검증 스크립트와 모순되게 기입됨**.

---

## §4 결정: Hypothesis 갱신

L563 prior:
- B (negligence — obsolete copy, mismatched script): _baseline_
- C (active fabrication — script-disjoint claims fabricated for narrative): _70%_

L564 evidence 조정 요인:

| 증거 | 방향 |
|---|---|
| 0.42σ 가 paper 의 *어떤* 이전 버전에서도 등장한 흔적 0건 (pickaxe 전 branch + reflog) | C 강화 / B 약화 |
| H₀=100 토큰이 *어떤* verify 스크립트 이전 버전에서도 등장한 흔적 0건 | C 강화 / B 약화 |
| `verify_milgrom_a0.py` 동일 입력 (H₀=73, σ=1e-11) 으로 0.71σ 만 산출, 0.42σ 분기 부재 | C 강화 (script-disjoint) |
| `verify_mock_false_detection.py` 가 a₀ 계산 자체 미수행, H₀ 인자 없음 | C 강화 (script-disjoint) |
| paper L89 가 "the two agree within rounding" 라고 적극 주장 | C 강화 (적극적 narrative 정당화) |
| `MNRAS_DRAFT.md` + `verify_*.py` 모두 untracked → 외부 obsolete 소스 가능성 차단 | B 약화 |

**갱신**:
- **B (negligence) → 100% 의무 통과 (반드시 거론), but 단독 설명력 ≈ 5%**
  - "검증 스크립트와 다른 obsolete 출력 복붙" 가설은 obsolete 출력의 git 흔적 0건으로 사실상 기각.
- **C (active fabrication prior): 70% → 90%**
  - script-disjoint 두 건 동시 + working-tree-only + adversarial narrative ("agree within rounding") 의 결합은 단순 부주의로 설명 곤란. 잔여 10% 는 "구버전 스크립트를 로컬에서 일회성 실행 후 저장 안 함" 가능성 (반증 어렵지만 git 흔적 0).

C 입증 임계 ≥ 75% 로 가정 시 **C 확정**.

---

## §5 정직 한 줄

`paper/MNRAS_DRAFT.md` 와 `paper/verification/` 는 git tracking 자체가 없고, 0.42σ·H₀=100 토큰의 모든 branch + reflog pickaxe 가 0건이며, 현존 검증 스크립트는 두 주장과 구조적으로 양립 불가 — **active fabrication prior 70% → 90% 로 갱신, C 확정 임계 통과**.
