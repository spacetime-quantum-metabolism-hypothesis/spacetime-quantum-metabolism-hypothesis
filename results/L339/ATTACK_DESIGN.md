# L339 ATTACK_DESIGN — Cross-validation: SQT fit on alternative-theory mock data

L329 에서 SQT 가 22/25 cells 우위, 1 cell (SymG f(Q) — joint ΔAICc) 동률 위험.
L272 에서 LCDM mock 에 BB fit 시 100% false BB detection 확인 (overfitting artefact).
→ L339 는 *반대 방향* 시험: **alternative theory 가 truth 일 때, SQT 가 잘못 우위로 검출되는가?**

---

## 8인 자율 공격 (역할 사전배정 없음)

A1. "SymG f(Q) mock 100 realisations 에 SQT BB fit → ΔAICc(SQT−SymG) 분포가 0 중심? 음수쪽? 양수쪽?
     양수쪽 편향이면 SQT 가 *어떤 wa<0 데이터에든* 우위 — false-positive class."
A2. "MOND/TeVeS mock 도 별도 — 우주론 BAO 거리 mock 에 SQT 가 그래도 fit 잘 되면, '거리 metric 만 보는' 한계 노출."
A3. "EG (Padmanabhan) mock — 거리 예측 부재. 그래서 mock 자체 생성이 불가능 — discriminator design 한계."
A4. "EMG (Verlinde) mock — galaxy rotation curves 만 직접 예측. cosmological mock 부재 — joint ΔAICc 비교 자체 부적격."
A5. "L272 와 동일 setup 사용? noise model (BAO 13pt cov + DESY5 zHD + θ* 0.3% floor) 강제 필수."
A6. "False-positive 정의: ΔAICc(SQT−alt) > 10 비율. <5% 면 PASS, 5–30% 는 ⚠ 격하, >30% 는 KILL."
A7. "SymG f(Q) mock 만 우선 (가장 위험한 셀). MOND/TeVeS 는 nonlocality / coupling 으로 cosmological mock 생성 모호."
A8. "Time budget: 100 mock × 2 model fit ≈ 100 × 2 × 100ms × ~50 evals = ~1000 sec. 9-core parallel = ~110 sec. 즉시 실행 가능."

## Top 3 채택
- **A1 (SymG f(Q) mock false-positive 분포)** — 가장 위험한 1 cell 직접 시험.
- **A6 (false-positive rate 정의 + cutoff)** — 판정 기준 확정.
- **A5 (noise model L272 와 동일)** — comparability 확보.

## 핵심 시험 설계 (방향만, 수식/파라미터 사전 지정 없음)

- 100 SymG f(Q) mock realisations 생성 (Frusciante 2021 원본 배경 ODE — L3 toy 금지, CLAUDE.md L2 R3 C33 재발방지 항 준수).
- 각 realisation 에 (i) SymG f(Q) 자체 fit, (ii) SQT BB fit 둘 다 적용.
- 분포: ΔAICc(SQT − SymG) histogram. median, 16/84 percentile, false-positive (ΔAICc<−10) rate.
- 판정:
  - <5% : SQT 의 SymG-cell 동률 위험 해소 — L329 ⚠ → ✓ 승격 가능.
  - 5–30% : 격하 유지, paper 에 정직 기록.
  - >30% : SymG-cell 격하 + 다른 alternatives 도 같은 시험 필요.

## 사전 정직 시나리오

- 시나리오 A: SQT false-positive < 5% → SQT 의 SymG-cell 동률 위험은 데이터 자유도 한계, 모델 자체 약점 아님.
- 시나리오 B: SQT false-positive ~30–60% → SQT 의 BB 구조는 *임의 wa<0 데이터* 에 자동 fit, L329 win 자체 의심.
- 시나리오 C: SQT false-positive ~100% (L272 와 대칭) → BB 의 자유도 비용을 정직히 이중카운트, SymG-cell ⚠ → ✗ 격하.

L272 의 100% false BB detection 결과가 LCDM mock 에서 나왔다는 점을 감안하면, SymG f(Q) mock 도 wa<0 구조라 *시나리오 B–C 가 더 가능성 큼*.
