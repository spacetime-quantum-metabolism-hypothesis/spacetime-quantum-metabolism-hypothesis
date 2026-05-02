# L408 ATTACK DESIGN — V(n,t)-extension derivation gate

8인 적대팀 시뮬레이션. 역할 사전 지정 없음 (CLAUDE.md 최우선-1, LXX 공통원칙).
공격 표적: 22행 한계표 #12 — "DESI Tier B (V(n,t)-확장) prediction" 을 derivation 없이 인용 시 발생할 over-claim 위험.

---

## A1. Frame: reviewer 가 칠 가장 강한 단일 일격

> "당신들의 V(n,t) 확장은 (i) 공리에서 functional form 이 유도되지 않았고, (ii) toy fit 은 (w0, wa) DESI 박스를 동시에 만족하지 못했으며 AICc 가 LCDM 보다 나쁘다. 그럼에도 'SQMH 가 DESI w0-wa 를 예측한다' 고 쓰면 이는 phenomenological back-fit 이다. Tier A (wa=0) 만 사전 등록하라."

이 한 줄로 PRD/JCAP referee 가 종결 가능. 따라서 공격 8개는 모두 이 한 줄을 다른 각도에서 보강하는 형태로 설계.

---

## A2. 8인 공격 (자율 분담, 사후 정리)

### Attack-1 (axiom-traceability)
V(n,t) 의 functional form 이 L0/L1/L2 공리 어디에서 *직접* 나오는지 명시 불가. L408 이전 결과는 ratio_m1, sqrt_m1, cpl_blend(erf) 등 *templates* 를 스캔했을 뿐. "공리 → V(n,t) 형태" 의 화살표가 비어 있음. → over-claim FATAL.

### Attack-2 (template-zoo over-fitting)
L33 base_keys 만 60+ 개. AICc 페널티 k=2 는 family 선택 자유도 (template-meta-parameter) 를 흡수하지 못함. 실효 자유도는 k≈4~6. 실효 dAICc 재계산 시 LCDM 우위.

### Attack-3 (Tier B box 동시미충족)
DESI DR2 (DESI+CMB+SN-all) 1σ 박스: w0 ∈ [-0.815, -0.699], wa ∈ [-1.04, -0.59]. L33 챔피언 (Q93, c=1.35 mix) w0 ≈ -0.95, wa ≈ -0.53 → wa 가 박스 외부. "박스 동시 적합" 주장 즉시 반박.

### Attack-4 (Om degeneracy)
L33 챔피언 Om ≈ 0.07~0.12. 이는 BAO-only artefact (CLAUDE.md L33 재발방지 명시). joint (BAO+SN+CMB) 에서 Om ≈ 0.30 으로 끌려가면 amp 을 다시 fit 해야 하므로 Tier B 사전등록 시 Om 의 prior 를 어디 두느냐가 결과를 결정. 이는 "사전등록 가능한 prediction" 이 아닌 "사후 calibration".

### Attack-5 (slow-roll / thawing 매칭의 비유일성)
V(n,t) 를 thawing quintessence V(φ) ∝ exp(-λφ) 또는 V(φ) ∝ φ² 와 매칭하려 해도, 매칭 변환이 (n,t) → φ 로 *one-to-many* — 어떤 매칭을 택해도 동일 background w(z) 에 도달 가능. 이는 V(n,t) 도출이 underdetermined.

### Attack-6 (시간평행성 위반 의심)
V 를 (n,t) 두 변수로 두면 explicit t-dependence — Noether 에너지 보존이 자동 보장되지 않음. SQMH 공리가 이 위반을 *허용*한다는 보강 논증이 없으면, V(n,t) 는 ad-hoc.

### Attack-7 (Tier B 가 Tier A 결과를 오염시킬 위험)
Tier A (w_a=0 base, sigma8 calibration) 의 DESI prediction 이 *이미 사전 등록 가능* 하다고 23행 표 #12 가 명시. 여기에 Tier B 를 묶어 "확장된 사전 등록" 이라고 패키징하면, Tier B 의 미충족이 Tier A credibility 까지 끌어내림. → **분리 보존 권고**.

### Attack-8 (Bayesian evidence 실패)
DESI DR2 pure-LCDM 13pt χ² ≈ 10.2. L33 best Q93 χ² ≈ 5.7 정도. ΔAICc ≈ -4.6 은 marginalised log-evidence 로는 ln Z gap < 1.5 (Occam). Jeffreys 척도 "barely worth mentioning". 사전등록 prediction 으로 부족.

---

## A3. 합의된 공격 강도

- **사망급 (단일 KO)**: Attack-1 (axiom-traceability), Attack-3 (box 동시미충족).
- **기각급 (referee KO 가능)**: Attack-2 (실효 k), Attack-4 (Om degeneracy), Attack-7 (Tier A 오염).
- **약점 노출**: Attack-5, 6, 8.

→ **사망급 2건 동시 존재 = Tier B 사전등록은 over-claim**. 닫혀야 할 gate.

## A4. gate 조건 (이번 L408 에서 충족 필요)

| Gate | 내용 | 필요 증거 |
|------|------|-----------|
| G1 | V(n,t) functional form 이 공리에서 유일 도출 | derivation chain |
| G2 | toy fit 이 DESI box 동시 만족 (w0 ∈ box AND wa ∈ box) | run.py 결과 |
| G3 | dAICc < -4 with k=4 (V(n,t) 추가 파라미터 정직 반영) | run.py 결과 |
| G4 | thawing quintessence (또는 slow-roll inflation) 매칭이 one-to-one | 매칭 표 |

L408 에서 G1~G4 중 하나라도 미충족 시 Tier B gate **닫음 (영구 보류 권고)**.
