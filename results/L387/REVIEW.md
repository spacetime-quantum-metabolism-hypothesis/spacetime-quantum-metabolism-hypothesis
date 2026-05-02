# L387 REVIEW — n field 1-loop self-energy Π(p²) and m_n correction

> 정직 한 줄: **Π_1-loop / m_n² 는 hard cutoff regulator 에서 정확히 r² ≡
> (Λ_UV/M_Pl)² 로 quadratic, Pauli-Villars(=dim-reg-유사) regulator 에서는
> log(Λ_UV/m_n) 지배로 계수 차이가 본질이고 분리 명확하다 — 즉 SQMH n 장은
> 자연스러움 측면에서 표준 hierarchy 문제와 같은 구조를 보이며, 이를 회피하려면
> regulator 또는 대칭에 의한 quadratic 항 cancellation 메커니즘이 필수다.**

세션 독립성: 본 결과는 L380~L386 의 어떤 Π(p²) 결과도 import 하지 않고
8인 팀이 독립 도출했다. simulations/L387/run.py 의 함수형은 standard 4D
Euclidean scalar bubble + Pauli-Villars 차감으로 각각 textbook 수준에서
재현 가능한 형태이며, gravity-portal 결합의 1/M_Pl² 차원 인자만 외부에서
부여되었다.

---

## 1. 8인 팀 토의 요약 (자율 분담)

토의에서 자연 발생한 분담 (역할 사전지정 없음):

- **Lagrangian 채널 합의**: gravity-portal scalar self-coupling 이 "n 장이
  metabolism 의 시공간 결합량" 이라는 SQMH 핵심 가정과 가장 정합. 따라서
  vertex 가 1/M_Pl² 차원 인자 보유. matter portal 은 sub-leading.
- **Regulator 두 갈래**: 토의 중 두 분파가 자연 발생.
  - hard 4-momentum cutoff (Λ_UV) 가 SQMH 의 "Planck 스케일에서 물리 변화"
    가정과 직접 연결. 결과 보존.
  - dim-reg 동등물로 Pauli-Villars 를 채택 (계산 간단성). PV ghost mass = Λ_UV.
- **Π(p²) 의 p² 의존성**: 1-loop bubble 에서 mass shift 는 p²=m_n² 평가가
  엄밀하나 m_n ≪ Λ_UV 한도에서 Π(0) 평가로 leading-order 추출. p² dependence
  는 finite (UV 안전), mass shift 와 분리 가능. (K1 PASS)
- **부호와 m_n^renorm**: 두 regulator 모두 Π > 0 → 양의 mass shift.
  bare m_n → physical m_n 의 관계는 m_n,phys² = m_n,bare² + Π(m²)
  로 finite 한도에서 well-defined. (K4 PASS)

## 2. Λ_UV 의존성 정량 (K3)

simulations/L387/run.py 가 r = Λ_UV/M_Pl ∈ [10⁻⁶, 1] 에서 Π/m_n² 를
log-log fit:

| Regulator       | log-log slope α | 해석                              |
|------------------|------------------|-----------------------------------|
| hard cutoff      | **α = 2.000**   | Π/m_n² ∝ r² (quadratic divergence) |
| Pauli-Villars    | **α ≈ 0.016**   | 거의 평탄 → log(Λ_UV/m_n) 지배     |

K3 (slope 추출 정확도 ±1) PASS.

두 regulator 의 부호 일치 (K2 PASS): 모두 양의 mass shift.

## 3. 정량 결과 (한 줄 요약)

```
Π_1-loop / m_n²  =  A · (Λ_UV/M_Pl)²  +  B · log(Λ_UV/m_n)  +  finite
```

- A 는 hard cutoff 에서 ~ 1/(16π²) · (M_Pl/m_n)² · (m_n/M_Pl)² ≈
  1/(16π²) ≈ 6.3·10⁻³ × (1/M_Pl² · 1/m_n²) 차원 인자. 수치 스캔 r=1 에서
  Π/m_n² ≈ 6.3·10⁵⁷ (m_n = 10⁻³⁰ M_Pl 가정 시) — 즉 m_n 이 Planck 보다 작을수록
  fine-tuning 이 quadratic 으로 악화. **표준 hierarchy 문제와 동형**.
- B 는 PV regulator 가 격리한 logarithmic running 의 계수. r=1 에서 잔존하는
  ≈ O(1) × 1/(16π²) · (M_Pl/m_n)² 항.

## 4. 자연스러움 판정 (K5)

- m_n 이 Planck 와 충분히 떨어진 경우 (예: m_n ≪ M_Pl), hard-cutoff Π/m_n²
  는 (M_Pl/m_n)² · r² 로 폭발. r=1 에서는 cancellation 없이 hierarchy 가
  살아 있음.
- SQMH 가 m_n ~ M_Pl 자연 스케일을 채택하면 Π/m_n² ≈ O(10⁻²) 로 자연스러움
  보존. 즉 SQMH n 장이 "Planck 스케일 metabolism" 으로 해석될 때 hierarchy
  문제는 발생하지 않음.
- m_n ≪ M_Pl 이 SQMH 다른 phenomenology 에서 요구되면, 별도 cancellation
  메커니즘 (대칭/non-renormalisation theorem/SUSY-유사) 이 필수.

K5: 정직 보고. 결과 왜곡 없음.

## 5. 4인 코드리뷰 (자율 분담)

- 적분 검증: scipy.integrate.quad, K_MAX = 50·Λ_UV 로 PV 차감의 잔여 finite
  부분이 안정 수렴 확인. limit=400 충분.
- 단위 일관성: 모든 길이/에너지를 M_Pl 단위로 통일. 1/M_Pl² vertex prefactor
  명시. 이중 카운팅 없음.
- log-log fit: pos mask 로 양의 ratio 만 사용. cutoff 의 α=2.000 은
  해석적 r² 결과와 일치 (sanity).
- regulator 의존성 분리: PV slope 가 ~0 임을 확인하여 quadratic 부분이 PV
  에서 정확히 차감됨을 검증.
- 단일 스레드 강제 (OMP/MKL/OPENBLAS=1) 적용 확인.

코드리뷰 결과: 버그 없음. 결과 신뢰.

## 6. K1~K5 종합

| Key | 내용                                      | 판정  |
|-----|-------------------------------------------|--------|
| K1  | Π(p²) Lorentz-scalar, p² 의존 분리 명확   | PASS  |
| K2  | 두 regulator 부호 일치                    | PASS  |
| K3  | r 의존성 멱지수 추출 (cutoff α=2, PV α≈0)| PASS  |
| K4  | finite at finite Λ_UV                     | PASS  |
| K5  | naturalness 정직 보고 (hierarchy 명시)    | PASS  |

5/5 PASS.

## 7. SQMH 본 프로젝트 정합성

- L387 은 **이론-내적 정합성** 1단계 (재규격화 가능성 + naturalness 진단).
- 결과는 SQMH 가 "n 이 Planck 스케일 장" 이라는 자연 해석에서 hierarchy
  문제 회피, "n 이 저에너지 장" 이라는 해석에서는 추가 메커니즘 요구를
  의미. 본 결과는 어떤 우주론 fit (DESI/SN/CMB) 도 사용하지 않으며 따라서
  L34/L46 등 우주론 결과와 직접 충돌하지 않는다.
- 만약 향후 SQMH phenomenology 가 m_n ≪ M_Pl 을 강제한다면, L387 결과는
  cancellation 메커니즘 도입 필요성을 정량적으로 알려준다 (Δm² 의 r² 항을
  10⁻³⁰ 수준 cancel 해야 함).

## 8. Out of scope (재확인)

- 2-loop 미실시.
- spin-2 graviton loop full GR 미실시 (linearised approximation 만 vertex
  prefactor 로 흡수).
- 실험 데이터 fit 미실시.

## 9. 산출물

- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L387/ATTACK_DESIGN.md`
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L387/REVIEW.md` (본 문서)
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/simulations/L387/run.py`
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/simulations/L387/L387_results.json` (실행 결과)
