# L363 ATTACK DESIGN — Tensor Network Holography (MERA) as SQT 5th Pillar?

## 목적
Swingle (2009, 2012) 의 MERA ↔ AdS/holography 대응이 SQT (Spacetime Quantum
Theory) 의 기존 4-pillar 구조 — (P1) 양자 metabolic 소멸항, (P2) ψ-필드 기반
배경 동역학, (P3) holographic UV 정합 (Bekenstein-'t Hooft), (P4) 거시
관측가능량 (BAO/SN/CMB/RSD) — 위에 **5번째 pillar (P5: tensor-network
discrete holography)** 로 추가될 수 있는지를, 이론·시뮬레이션·관측 3축에서
독립 평가한다.

핵심 질문: **MERA bond / entanglement entropy 스케일링이 SQT 의 4차 항 (a4)
계수를 a priori 로 고정하거나, 또는 독립 측정 가능한 상관량을 만들 수 있는가?**

## 검증 축

### Axis A — 이론 일관성 (8인 자율팀, 역할 사전지정 금지)
- A1. MERA 의 RG 층 깊이 ↔ SQT 동역학 시간 스케일 대응 여부
- A2. ψ-필드 양자 상태의 entanglement entropy 와 MERA bond capacity 정합성
- A3. 연속극한 (cMERA) 에서 SQT 배경 메트릭 회복 여부
- A4. 4번째 차수 항 (a4) 의 도출 경로가 P1–P4 와 독립적 (= 새로운 pillar) 인지,
  아니면 P3 의 sub-corollary 인지 판정

> 주의: 본 Command 는 a4 의 형태·계수·부호에 대한 어떤 힌트도 제공하지 않는다
> (CLAUDE.md 최우선-1). 8인 팀이 방향 ("MERA, entanglement scaling, holographic
> bound") 만 듣고 독립 유도.

### Axis B — 시뮬레이션 (4인 자율 코드리뷰)
- B1. 작은 cMERA 토이 (qubit chain, bond dim 한정) 에서 entanglement
  scaling exponent 추출
- B2. SQT 배경 ODE 의 a4 항을 자유 파라미터로 두고 BAO/SN/CMB/RSD joint
  posterior 위치 — pillar 가 데이터에 의해 요구되는지 (Δ ln Z, AICc)
- B3. 0-parameter (a4 fixed by MERA) vs 1-parameter (a4 free) 비교.
  Occam 패널티 명시 (CLAUDE.md L5 규칙).
- 병렬: `multiprocessing spawn(9)`, OMP/MKL/OPENBLAS=1.

### Axis C — 관측 falsifiability
- C1. a4 가 영향 줄 수 있는 채널 (성장 D(z), σ_8, BAO 잔차) 식별
- C2. 현행 데이터 (DESI DR2 + DESY5 + Planck compressed + RSD) 로 5σ
  배제 가능 영역 사전 계산
- C3. DR3 / Euclid / LSST 시점에서 pairwise discrimination Fisher 예상

## 5-pillar 승격 판정 기준 (Pre-registered)

| 기준 | PASS | WARN | FAIL |
|---|---|---|---|
| K-T1 이론 독립성 (P3 와 분리 가능) | 명확히 새 정보 | 부분 중복 | P3 의 재진술 |
| K-T2 a4 a priori 고정 가능 | 자유도 0 도출 | 1 자유도 잔존 | 도출 불가 |
| K-T3 cMERA 연속극한 정합 | 회복 명확 | 토이 한정 | 회복 실패 |
| K-D1 joint Δ AICc (P5 추가 vs 미추가) | < −4 | −4 ~ 0 | > 0 |
| K-D2 fully-marginalized Δ ln Z | > +2 | 0 ~ +2 | < 0 |
| K-D3 Cassini PPN / GW170817 | 자동 통과 | 부가 가정 | 위반 |
| K-D4 S_8 tension 영향 | ≥ 중립 | < 0.5σ 악화 | ≥ 0.5σ 악화 |
| K-O1 falsifiable DR3 prediction | pairwise > 1σ | 0.3–1σ | < 0.3σ |

승격: K-T1, K-T2, K-D2 동시 PASS + K-D3 위반 없음.

## 가능한 결과 시나리오 (사전 등록)
- (S1) MERA 가 P3 의 미세화 → 별도 pillar 아님, P3 보강으로 흡수.
- (S2) MERA 가 a4 를 자유도 없이 고정 → P5 정식 등록, 데이터 검증으로 이행.
- (S3) MERA 토이가 cMERA 극한에서 SQT 배경과 충돌 → SQT 또는 MERA 한 쪽
  수정 필요 (위기 시나리오).

## 위반 시 무효화
- Command 안에 a4 에 대한 어떤 수치·수식·부호 힌트가 있으면 즉시 재작성.
- 시뮬레이션 결과가 base.md 와 충돌 시 base.fix.md 에 정직 기록 (CLAUDE.md).

## 한국어 한 줄
정직: MERA 가 P3 holographic pillar 의 보강일 가능성이 가장 크며, 독립 5번째 pillar 등극은 K-T2 (a4 자유도 0 도출) 에서 막힐 확률이 높다고 사전 평가한다.
