# L355 ATTACK DESIGN — SQT UV FP ↔ AS Reuter FP 연결 가능성

## 0. 한 줄 요약 (정직)
SQT의 UV 고정점이 Reuter–Saueressig의 비섭동 G–Λ 평면 NGFP와 **공통 RG 매니폴드 위의 동일 점**으로 식별 가능한지를 묻는 독립적 RG 사상(mapping) 시도. 현재 시점에선 가능성은 열려 있으나 동치성은 입증되지 않음.

## 1. 배경 (방향만, 수식 금지)
- Asymptotic Safety (AS): Reuter 1998 이후, FRGE (Wetterich-type) 로 truncate한 EAA 흐름에서 G와 Λ가 UV에서 **non-Gaussian fixed point** 로 모이는 시나리오. Einstein–Hilbert truncation, R^2, f(R), Einstein–Hilbert + scalar matter 등 다양한 truncation에서 NGFP 존속 보고.
- SQT (본 프로젝트 공리계): 시공간을 양자대사(quantum metabolism) 흐름으로 보는 가설. 거시 결과로 BAO/SN/CMB phenomenology의 background-only 수정을 생산. UV 한도에서는 흐름 소스/싱크 균형이 정지하는 **자기 일관 고정점** 존재가 공리(L0/L1)에서 시사됨.

## 2. 핵심 질문
Q1. SQT UV FP가 존재한다면 그 차원수(coupling 개수)와 임계 지수(critical exponents) 스펙트럼이 AS NGFP의 그것과 양립 가능한가?
Q2. SQT 흐름 변수(metabolic rate, 정보 밀도, 유입속도 등)와 EAA의 G,Λ,ξ_φ 사이에 가역적 RG 사상이 존재하는가?
Q3. SQT의 거시 결과(예: 본 프로젝트 후기 BAO 챔피언의 g(z) 함수 형태)가 NGFP 근방의 1차 임계 지수로 재현 가능한가?

## 3. 공격 단계 (단계별 산출 정의)

### Step A — 좌표계 식별 (책상)
- AS 측: dimensionless g = G k², λ = Λ k⁻². EH truncation에서 임계 지수 θ₁,₂ 복소쌍.
- SQT 측: 본 프로젝트의 흐름 변수 사전을 한 페이지 표로 정리. 각 변수의 RG 차원(스케일링 가중치)을 공리 단위에서 추출.
- 산출: 두 좌표계의 **차원-매칭 표** (이 단계까지는 수식 없이 차원만).

### Step B — gravity-coupled scalar truncation 채택 (이론 한도)
- AS literature에서 gravity + 비최소 결합 scalar의 NGFP 존속/사라짐이 보고된 truncation 군을 인용 (Eichhorn-Held 2017 계열, Percacci-Vacca, Wetterich-Yamada).
- SQT의 흐름 자유도가 그 truncation 안에서 **어떤 좌표 부분공간**에 사상되는지를 식별. 추가 자유도는 irrelevant direction 후보.

### Step C — 정합성 조건 (정직 체크리스트)
- C1. SQT UV FP의 차원수 ≤ AS NGFP relevant direction 수.
- C2. 두 FP의 critical exponent 부호 패턴 일치 (UV-attractive 방향 일치).
- C3. IR로 흘렀을 때 SQT가 만드는 거시 phenomenology가 AS IR window (G_N, Λ_obs) 와 모순 없음.
- C4. Cassini PPN, GW170817 c_T=c, BBN — 3대 LV 안전장치를 모두 통과.

### Step D — 사상 시도 (한 truncation에서 한 변환만)
- 한 번의 변수치환만 허용: SQT 좌표 → (g, λ, ξ_φ). 다단계 phenomenological fit 금지.
- 실패 양식: 사상 후 SQT FP가 g<0 또는 λ가 AS NGFP 지정 부호와 반대면 즉시 KILL.

### Step E — phenomenology 단방향 검증
- AS NGFP 근방에서 IR로 흘러나온 effective action이 본 프로젝트 L33–L34 챔피언 g(z) 형태(저z tanh + 고z 선형)를 **재현 가능한 함수족 안에 들어가는지** 확인. 직접 fit은 금지(과적합 방지). 함수족 포함관계만 본다.

## 4. KILL 조건 (사전 명시)
- K1. C1 위반 — SQT FP 자유도가 AS truncation의 relevant 수보다 많음.
- K2. C2 위반 — 임계 지수 부호 패턴 불일치.
- K3. C4 위반 — Cassini 또는 GW170817 자동 위반.
- K4. Step D에서 1회 변환으로 g<0/λ 부호 위반.
- K5. Step E에서 IR effective action의 함수족이 SQT 챔피언 g(z) 함수족을 포함하지 못함.

## 5. PASS 조건
- 위 K1–K5 모두 회피 + Step C의 C1–C4 모두 충족 + 사상이 단일 변수치환으로 명시 가능.
- 이 경우 결과는 "동치 후보(equivalence candidate)" 등급. 동치 자체 주장은 하지 않음.

## 6. 출력 등급 정의
- A: PASS, 단일 사상 명시, 임계 지수까지 일치.
- B: PASS, 사상 명시 가능하나 임계 지수 일치는 미확인.
- C: 일부 KILL 회피 / 일부 위반.
- D: K1–K5 중 하나라도 명백 위반.

## 7. 비범위 (이번 라운드 명시 제외)
- AS truncation 자체의 자기일관성 검증 (이미 외부 문헌에 위임).
- FRGE 코드 직접 작성 — 본 라운드는 책상 수준 사상만.
- Phase 5/6 MCMC 재실행. 본 라운드는 RG 구조 비교만.

## 8. 정직 단서
- SQT 측 UV FP는 본 프로젝트 공리에서 "존재 시사"이지 RG 미분방정식으로 도출된 점이 아니다. 따라서 본 라운드의 결과는 **구조 양립성 시그널**이며 동치 증명이 아니다.
