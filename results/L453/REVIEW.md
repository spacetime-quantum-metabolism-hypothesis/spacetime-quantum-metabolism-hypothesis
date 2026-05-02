# L453 — CI/CD verify.yml REVIEW

## Scope
- Create `.github/workflows/verify.yml` running the 5 verification scripts in
  `paper/verification/` on every push and PR touching that directory, comparing
  stdout against `expected_outputs/*.json`, and emitting a PASS/FAIL badge.

## Deliverable
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/.github/workflows/verify.yml`

## Design choices
- **Triggers**: `push` + `pull_request` on `main`, path-filtered to
  `paper/verification/**` and the workflow file itself; `workflow_dispatch`
  for manual reruns.
- **Matrix**: 5 parallel jobs, one per script (`fail-fast: false`) so a single
  failure does not mask the others.
- **Python**: 3.11 (README states "tested 3.11 / 3.13"). `numpy>=2.0`,
  `scipy>=1.10` from `requirements.txt`.
- **Comparison**: each `expected_outputs/<stem>.json` carries a
  `stdout_lines` array. The workflow asserts every expected line is a
  substring of captured stdout. Numeric tolerance is already baked into the
  scripts (seeded RNG, deterministic output strings), so a strict
  substring match is sufficient and avoids float-formatting drift.
- **Encoding**: `PYTHONIOENCODING=utf-8` set to avoid the cp949 issue
  flagged in CLAUDE.md, even though Ubuntu runners default to UTF-8.
- **Artifacts**: per-script `output.log` uploaded for 14 days; badge JSON
  uploaded for 90 days.
- **Badge**: shields.io endpoint format
  (`{schemaVersion, label, message, color}`) — green `PASS` if all 5 jobs
  succeed, red `FAIL` otherwise. Aggregation job runs `if: always()` and
  re-fails when any verify job failed so the PR check is red.

## Local smoke test
- `python3 paper/verification/verify_milgrom_a0.py` reproduces the 4
  expected stdout lines exactly (`a_0 (SQT) = 1.129e-10 m/s^2`, etc.).
- Substring-based comparator therefore passes against
  `expected_outputs/verify_milgrom_a0.json`.

## Honesty (한 줄)
- 정직 한 줄: 비교는 `stdout_lines` 부분문자열 일치만 검사. 수치 톨러런스는 스크립트 내부 PASS 판정에 위임하며, JSON `expected.deviation_sigma` 등 필드는 워크플로에서 사용하지 않음 — float 포맷 드리프트 방지를 위한 의도적 단순화.

## Follow-ups (out of scope for L453)
- Badge JSON is uploaded as a build artifact; publishing it to
  `gh-pages` or a gist for live README embedding is a separate task.
- Script 4 (`verify_mock_false_detection.py`) takes < 1 minute; if it
  drifts above the 10-minute job timeout in future, split into its own
  job with a higher `timeout-minutes`.
