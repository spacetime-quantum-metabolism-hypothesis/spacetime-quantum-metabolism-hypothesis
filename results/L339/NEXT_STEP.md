# L339 NEXT_STEP — Cross-validation 실행 권고

## 1) 시뮬 스크립트 (simulations/L339/run.py) — 방향만

- N = 100 realisations.
- Truth model: SymG f(Q), Frusciante 2021 원본 배경 ODE (n ≥ 1 강제, L2 R3 C33 부호 검증 적용).
- Truth 파라미터: SymG joint best-fit (L329 SymG row) — 8인 합의된 single point. 분포 시험 단계에서는 grid 확장 보류.
- Mock data:
  - BAO: DESI DR2 13 pt + 공식 공분산 (CobayaSampler/bao_data).
  - SN: DESY5 zHD + 해석적 M marginalisation.
  - CMB: compressed θ* + 0.3% theory floor.
  - RSD: L4 setup 동일.
- 각 realisation 에 SymG f(Q), SQT BB 두 모델 적합. ΔAICc 기록.

## 2) 병렬 실행

- multiprocessing spawn pool, 9 worker.
- worker 당 OMP/MKL/OPENBLAS_NUM_THREADS=1 강제 (CLAUDE.md 시뮬 원칙).
- 모델별 worker 분리, 전역 singleton 의존 금지.

## 3) 4인 코드리뷰 (자율 분담, 역할 사전배정 없음)

- mock generator 의 SymG ODE 안정성 (forward shooting 강제, backward 폭주 방지 — CLAUDE.md k-essence/quintessence 항 준용).
- noise covariance 적용 정확성 (BAO 13pt 풀 공분산, DESY5 해석적 M, θ* floor).
- AICc k 비대칭: k_SQT (BB 3-regime) vs k_SymG (f_1, n) 정확히.
- 시뮬 실패 시 코드 버그 우선 의심 (CLAUDE.md 재발방지).

## 4) 판정 후 분기

- <5% : L329 SymG-cell ⚠ → ✓ 승격 — 논문에 "alternative-mock cross-validation passed" box.
- 5–30% : ⚠ 유지 + paper 정직 기록 (L329 표 footnote).
- >30% : SymG-cell ✗ 격하. MOND-mock, TeVeS-mock 추가 시험 권고. 논문 글로벌 압승 주장 격하.

## 5) 차후 (L340+ 후보)

- 통과 시: MOND analogue mock (TeVeS 우주론적 거리 surrogate) 도 cross-test — full 5-alternative robustness.
- 실패 시: SQT BB anchor 를 *theory-prior* 로 사전 동결 (L272 권고와 동일) — 동결 후 재시험.

## 6) 절대 금지 사항

- L3 저z 전개 toy 로 SymG mock 생성 (부호 역전 위험).
- 좁은 Om bounds (L33 재발방지 — [0.05, 0.50] 등 충분히 넓게).
- 결과가 BB 우위로 나와도 "SQT 가 우위" 로 보고 (false-positive 정의상 *bad news*).
- 이 NEXT_STEP 자체에 수식/구체 파라미터 명시 (CLAUDE.md 최우선-1 — 8인 팀이 자율 도출).
