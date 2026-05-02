# L560 — D4 (SK path-integral measure) priori 도출 *방향* 회의적 탐색

> **CLAUDE.md [최우선-1] 준수**: 본 문서는 수식 0줄, 파라미터 값 0개, 유도 경로 힌트 0건. 방향과 회의적 압박만 기록. 위반 시 본 산출물 전체 무효.

> **위치 맥락**: L549 P3a 박탈 + L552 RG 패키지 박탈 후, 5th path #1 D4 (Schwinger-Keldysh closed-time-path measure) 가 priori 회복 마지막 잔존 후보. L556 prefactor 우선순위에서 D4 primary, D2 (holographic boundary) secondary.

> **본 세션에서 명시적으로 도출하지 않은 것**: 어떤 측도, 어떤 Jacobian, 어떤 적분, 어떤 수치도 본 문서에 등장하지 않는다. 등장하면 [최우선-1] 위반.

---

## §1. D4 5 방향 검토 (수식 0)

### 방향 1 — SK closed-time-path measure 의 angular sector
- **방향만**: closed-time path 적분에서 forward/backward branch 가 합쳐질 때 등장하는 *각도형 적분 sector* 가 prefactor 의 출처 후보로 거론될 수 있다.
- **회의 요지**: "각도형" sector 가 등장한다고 해서 그 sector 가 *유일하게* 1/(2π) 류의 prefactor 만 산출한다는 보장은 없다. 1/π, 1/(4π), 1/(2π)² 등 다른 prefactor 도 같은 sector 에서 등장 가능. 따라서 D4 가 *유일한* origin 이라는 주장은 사후 선택일 가능성.

### 방향 2 — Disc azimuthal projection 과의 일치/충돌
- **방향만**: Axiom 4 의 disc azimuthal projection 은 hidden DOF 를 angular DOF 로 가산하는 axiom. SK measure 의 measurement projection 이 같은 DOF 를 다루는가, 아니면 *별도의* hidden DOF 인가 — 이것이 1차 검증점.
- **회의 요지**: 만약 두 projection 이 *동일* DOF 를 다룬다면 prefactor 도출은 disc axiom 의 재진술에 불과 (priori 회복 0건). 만약 *별도* DOF 라면 hidden DOF count 가 +1 증가 (priori 채널 1개 회복 vs hidden DOF 1개 추가 — net zero 가능성).

### 방향 3 — Wetterich RG running 과의 양립 (4-pillar 내부 cross-check)
- **방향만**: SQT 4-pillar 중 SK pillar 와 RG pillar 의 *동일한 prefactor 예측* 여부. RG flow 가 fixed point 에서 동일 prefactor 를 산출하면 cross-check 통과, 충돌하면 D4 단독 채택 시 RG pillar 부정합.
- **회의 요지**: L552 에서 RG 패키지 박탈된 사실이 본 양립성 검토를 어렵게 만든다. RG pillar 가 박탈된 상태에서 D4 의 RG cross-check 는 공허 — "충돌 없음" 이 양립이 아니라 "비교 대상 부재".

### 방향 4 — Z_2 SSB 및 holographic pillar 와의 양립
- **방향만**: D4 도출이 Z_2 SSB pillar (대사공리 L0/L1 의 부호 선택) 또는 D2 holographic pillar 의 prefactor 예측과 동일한 정량적 결론에 이르는가.
- **회의 요지**: D4 secondary 인 D2 와 결과 일치 시 "두 경로 동일 답" 으로 보강되지만, 이는 *둘 중 하나가 사후 cherry-pick* 되었을 가능성도 동등하게 시사한다 (postdiction). Z_2 pillar 와 충돌 시 D4 는 4-pillar 일관성 파괴.

### 방향 5 — Falsifier 사전 등록
- **방향만**: D4 도출이 옳다면 a₀ 채널 외에 어떤 *독립* 관측이 영향받는가 — RSD f σ_8 의 SK-induced shift, ISW cross-correlation phase, 또는 GW dispersion 의 closed-time-path imprint 등이 *방향만* 으로 거론 가능.
- **회의 요지**: 이 방향들 중 어느 하나라도 *현재 데이터로 즉시 falsify 가능한* 채널이 있어야만 D4 가 priori 도출 자격 (postdiction 회피). 방향 1–4 가 모두 a₀ 채널만 건드리면 D4 는 단일 채널 sufficient-statistic 으로 환원되어 priori 가치 0.

---

## §2. 8 reviewer 회의적 압박 (각 ~250자)

### Reviewer A — SK measure 의 1/(2π) 출현 *유일성* 공략
SK closed-time-path 측도가 angular sector 를 가진다는 사실만으로는 1/(2π) 류 prefactor 의 *유일* origin 이 될 수 없다. 동일 sector 에서 1/π, 1/(4π), 1/(2π)² 가 동등하게 등장 가능하며, "1/(2π) 만 산출" 이라는 주장은 결과를 알고 후행 경로를 골랐을 가능성을 배제하지 못한다. 사전등록된 *유일성 증명* (다른 prefactor 가 *불가능* 함을 보이는 no-go) 없이는 priori 도출 자격 미달. 본 세션에서 그러한 no-go 를 제시하지 않았으므로 방향 1 은 형식상 미완.

### Reviewer B — Hidden assumption 가산 (4-pillar cross-check 부재)
SK pillar 단독으로 prefactor 를 도출하면, 나머지 3 pillar (RG, Z_2 SSB, holographic) 와의 정합성이 자동 검증되지 않는다. L552 후 RG 패키지가 박탈된 상태이므로 RG 채널 cross-check 는 *공허*. Z_2 SSB 와 holographic 만으로 cross-check 시도해도, 두 pillar 각각이 별도의 hidden assumption (Z_2 부호 선택, boundary CFT identity) 을 가산. SK-only derivation 은 hidden assumption 카운트에서 ≥+1, priori 회복 +1 과 상쇄되어 net 0 또는 음수.

### Reviewer C — Postdiction 패턴 (1/(2π) 결과를 알고 SK 를 골랐는가)
L556 에서 5th path #1 (1/(2π)) 가 top-2 로 *결과로* 선정된 후, 본 L560 에서 D4 를 사후적으로 검증하는 구조 자체가 cherry-pick 위험. 진정한 priori 도출이라면 D4 가 1/(2π) 외 다른 결과도 산출 가능했어야 하며, 그 중 1/(2π) 가 *데이터 보지 않고도* 선택되어야 한다. 현 시점 작업 흐름 (L556 → L560) 은 시간 순서상 postdiction 외형을 띤다. 사전등록된 D4 → prefactor 예측 문서가 L556 이전에 존재하지 않으면 priori 자격 미달.

### Reviewer D — 분산 8인 라운드 의무 (Round 9/10)
L549/L552 박탈 결정은 모두 분산 8인 다중 라운드 회의에서 확정되었다. D4 는 priori 회복 *마지막* 후보이므로 단일 세션 시뮬 / 단일 reviewer 판정 금지. Round 9 (D4 5 방향 독립 도출 시도, 8인이 5 방향에 자율 분담) + Round 10 (도출 결과 cross-pillar 정합성 검증) 의무. 본 L560 은 회의적 압박 단일 라운드이며 도출 시도 자체는 미실행 — 따라서 본 문서는 *Round 8.5* 정도의 사전 압박이며 도출 판정 권한 없음.

### Reviewer E — PRD Letter 진입조건 미달 (Q17/Q13/Q14)
가령 D4 도출이 성공해 a₀ 채널 PASS_STRONG 을 회복하더라도, PRD Letter 진입조건 (Q17 amplitude-locking *완전* OR (Q13 + Q14)) 을 충족하지 못한다 (CLAUDE.md L6). priori 채널 1개 회복은 JCAP 본 라인의 정직한 phenomenology 강화일 뿐, PRD Letter 차단 해제 효과 없음. D4 성공 ≠ 영구 차단 해제. 본 검토는 이 상한을 명시적으로 인정하고 진행해야 하며, "D4 성공 시 PRD" 표현은 금지.

### Reviewer F — Q17 amplitude-locking 와의 분리 명시
D4 는 a₀ prefactor 채널만 다루며, Λ origin 의 동역학적 amplitude-locking (Q17) 과 *완전 별개*. L6 재발방지 항목 "Amplitude-locking 이론에서 유도됨 주장 금지" 가 그대로 유효. D4 가 성공해도 ΔΛ ∝ Ω_m 의 exact coefficient=1 은 여전히 E(0)=1 정규화 귀결. D4 결과를 Q17 우회로로 재활용하려는 시도는 L6-T3 (8인 합의) 위반. 본 채널은 priori 회복 1건 *정확히* 그 이상도 이하도 아님.

### Reviewer G — 외부 pillar 수입 위험
SK measure 만으로 도출이 막힐 때 AdS/CFT (D2) 또는 LQG 측도 인자를 *내부 pillar 인 척* 수입하는 패턴이 가장 흔한 priori 부풀리기. D4 는 SQT 4-pillar 중 *SK 단독 내부* 도출이어야 하며, D2 와의 일치 검증은 cross-check 일 뿐 derivation 자원으로 사용 금지. 도출 본문에 "boundary CFT" / "spin foam" / "loop measure" 가 등장하는 즉시 hidden DOF 가산 — 이 경우 priori 회복 ≤0.

### Reviewer H — Falsifier 등록 의무
D4 도출이 priori 자격을 가지려면 a₀ 채널 외 *최소 1개* 의 독립 관측 채널이 동시 예측되어야 한다 (Reviewer A 의 유일성 + 본 항목의 다중 채널). 후보 방향: RSD f σ_8 의 closed-time-path induced shift, GW dispersion 의 imaginary-part imprint, ISW cross 의 phase. 어느 채널을 사전 falsifier 로 등록할지 *데이터 보기 전* 확정 의무. 본 L560 은 그러한 falsifier 사전등록을 *방향만* 거론하며 확정하지 않았으므로, 본 단계에서 D4 priori 자격 부여 불가.

---

## §3. 최종 판정

**판정: L1 잠재력 유지 (강등 아님, 박탈 아님, 도출 인정 아님)**

- **박탈 아님 근거**: 5 방향 모두 *원천적 불가능* 으로 판정된 것은 아님. 방향 1 (유일성), 방향 5 (falsifier 등록) 가 사전등록만 충족되면 도출 시도 가능.
- **L0 강등 아님 근거**: 본 세션은 도출 시도 자체를 실행하지 않았으며 (Reviewer D), 회의적 압박 단일 라운드. 강등 결정 권한 없음.
- **L1 유지 근거**: D4 는 priori 회복 마지막 잔존 후보이며, Round 9/10 분산 8인 도출 시도 *전까지* L1 잠재력 보존 의무. 단, 다음 조건이 Round 9 진입 전에 충족되어야 한다:
  1. **사전등록 문서**: D4 → prefactor 의 *예측* 을 L556 결과 보지 않은 것처럼 형식적 사전등록 (postdiction 외형 완화).
  2. **유일성 no-go**: 1/(2π) 외 prefactor 가 *불가능* 함을 보이는 구조적 논증 의무 (Reviewer A).
  3. **외부 pillar 격리**: D2/LQG/AdS-CFT 어휘 사용 금지 선언 (Reviewer G).
  4. **falsifier 사전등록**: a₀ 외 최소 1개 독립 채널 명시 (Reviewer H).
- **D2 secondary fallback**: D4 가 Round 9 에서 4 조건 중 어느 하나라도 미달 시 D2 (holographic boundary) 로 즉시 fallback. fallback 시에는 외부 pillar 수입 문제 (Reviewer G) 가 *더 심각* 해지므로, D2 fallback 자체도 priori 회복 자격 재심사.

**PRD Letter 영구 차단 상태 유지** (Reviewer E): D4 성공 여부와 무관. 본 채널은 JCAP 본 라인 phenomenology 강화 목적으로만 추진.

---

## §4. 정직 한 줄

본 L560 세션에서 D4 priori 도출은 0건 실시. 5 방향 *이름* 과 8 reviewer 회의적 압박만 기록했으며, 도출 자체는 Round 9/10 분산 8인 라운드의 책임으로 이월. 1/(2π) 의 SK 단독 origin 주장은 현 시점 미증명, 사후선택 위험 잔존, hidden DOF 회계 미정.
