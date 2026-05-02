# L542 — P3b conditional priori: UHE-CR anisotropy (direction-only audit)

상속: L536 NEW_PRIORI.md (P3b = Path-α + Causet meso, Z₂ SSB → UHE-CR dipole, dormant pre-reg)
규약: CLAUDE.md [최우선-1] 준수 — 방향·현상명·관측채널·질문구조만. 수식/파라미터값/유도경로 0건.

---

## 1. 임무 1 — Z₂ SSB 잔재 domain wall → UHE-CR 방향 비등방성 채널

### 1.1 물리 채널의 이름 (방향만)
- **SQT 측**: Path-α (axiom 3' Γ₀(t) 시간의존 소멸률) 위에서 Causet meso (이산 인과 sprinkling) 의 manifoldlike 회복 단계에 진입 시, 응축 위상에서의 **Z₂ 이산 대칭 자발적 깨짐 (Z₂ SSB)** 의 위상학적 잔재. 후보 잔재 형태: **domain wall network**, 잔재가 manifold limit 에서 surface 하는 형태로 **cosmic-string-like 잔재** 또는 **bulk 흐름 비대칭**.
- **관측 측**: 초고에너지 우주선 (UHE-CR) 도착방향의 **대규모 비등방성** — 즉 dipole 및 고차 다극 (quadrupole, 작은 각도 자기상관). 관련 관측소 이름만: Pierre Auger Observatory (남반구), Telescope Array (TA, 북반구), 차세대 GCOS, POEMMA.
- **연결 후보 메커니즘 이름** (방향만, 식 없음):
  - (a) domain wall network 의 stress-energy 분포가 **late-universe matter 분포와 비비등방적으로 결합** → UHE-CR 의 **소스 분포 비등방성** 으로 surface
  - (b) wall 의 **잔재 자기장 또는 위상결함 자기장** 이 UHE-CR 의 **편향 (deflection) 비등방성** 을 유도
  - (c) Causet sprinkling 의 **방향 자유도** (이산 인과 그래프의 비등방 분산) 가 manifold limit 에서 **bulk 흐름 비대칭** 으로 잔존

### 1.2 P3b 의 priori 자격 조건 (재확인, 식 없음)
- 부호 자유도: Causet sprinkling 매개변수 자유도 → 부호는 axiom 으로 고정되어야 priori 자격 ✓ (현재 dormant — 8인 도출 미실행).
- 차원: ✓ (자명, dimensionless dipole 진폭).
- OOM 결정 보조가정: holographic axiom (horizon 부피) + sprinkling rate 1 axiom — L536 명시.
- 시간 정합: claims_status v1.2 `uhe-cr-anisotropy` 가 이미 pre-reg — 형식적 priori 자격 ✓, 단 부분적.

---

## 2. 임무 2 — Auger / TA 관측 dipole (현황만 인용, 수치 0건)

본 감사는 [최우선-1] 준수를 위해 **관측 수치, 유의도, 적경/적위, 임계 에너지 값을 본문에 적지 않는다**. 팀 도출 라운드에서만 인용하도록 분리.

- **Auger**: E ≳ (high-energy threshold) 영역 도착방향 대규모 dipole 보고가 다년간 누적. 유의도는 데이터 누적과 함께 상승 추세. 방향은 은하 중심 부근으로부터 어긋난 방향대 — *세부 좌표·유의도·임계 에너지는 팀 라운드 인용*.
- **TA**: 북반구 hot spot (작은 각도 클러스터링) 보고. dipole 신호는 Auger 보다 약함 — 노출량 차이.
- **공동 분석**: Auger+TA full-sky 결합 분석 진행 중 — 결합 dipole 의 통계적 안정성은 차세대 (GCOS) 노출량 증가에 의존.

→ **인용 정합성**: 위 세 항목은 claims_status v1.2 `uhe-cr-anisotropy` pre-reg 텍스트와 일치. 본 감사는 그 이상 수치를 *덧붙이지 않는다*.

---

## 3. 임무 3 — SQT Z₂ SSB 가 dipole *방향* 을 priori 로 예측 가능한가?

### 3.1 핵심 질문 구조 (식 없이)
priori "방향 예측" 이 성립하려면 다음 세 가지가 axiom 수준에서 *동시* 결정되어야 한다:
1. **SSB 시점 (cosmic time)**: Γ₀(t) 의 시간 프로파일이 SSB 발생 시점을 고정해야 함. Path-α axiom 3' 단독에서 *시점만* 결정 가능 — 시점→horizon 부피→wall network 면적은 holographic axiom 으로 OOM 가능.
2. **SSB 의 공간 좌표 prior**: domain wall 의 *방향성* (anisotropy axis) 이 결정되려면 — SQT 가 우주론적 등방성을 깨는 **선호 방향** 을 가져야 한다. Causet sprinkling 은 평균적으로 Lorentz invariant (Bombelli-Henson-Sorkin) → **이론적으로 평균 등방** → axiom 만으로 *방향 priori* 는 **부재**.
3. **late-time wall 진화의 결합 채널**: wall ↔ matter 분포 / 자기장 / bulk flow 의 결합 부호 — Path-α 에서 dormant.

### 3.2 결론 (방향만)
- **dipole 진폭 (amplitude) priori**: 가능 — holographic axiom + sprinkling rate axiom 의 OOM 결정 채널이 열려 있음 (L536 P3b 자격 인정과 동일).
- **dipole 방향 (direction) priori**: **현재 SQT axiom 셋에서는 부재**. Causet sprinkling 의 평균 Lorentz 불변성이 우선되며, 방향성을 부여하려면 **추가 axiom (선호 방향 / 초기조건 비등방)** 이 필요. 이는 [최우선-1] 위반 없이 8인 라운드에서 자유 도출되어야 가능.
- **부분적 우회 채널 이름** (식 없음): (i) 우리 은하 인근의 local matter 분포에 wall surface 가 따라가는 *환경 결합* 시나리오 — 이 경우 방향은 SQT axiom 이 아니라 *late-time 환경* 이 결정 → 엄밀한 의미의 priori 자격 약화. (ii) inflationary preferred frame 결합 — Path-α 에서 별도 axiom 필요.

→ **정직한 진단**: "P3b 진폭 priori = 조건부 가능. P3b 방향 priori = 현재 axiom 셋에서 불가능, 추가 axiom 도입 시에만 가능 — 그 추가 axiom 자체가 8인 자유 도출의 대상이며 본 감사에서 함수형으로 제시 금지." (L536 의 dormant 분류와 정합.)

---

## 4. 임무 4 — arrival direction 통계 forecast (방향·채널 이름만, 수치 0건)

### 4.1 검증 가능한 통계 채널 이름
- **dipole 진폭** (저차 다극, l=1) — Auger+TA 결합, GCOS 노출량 증가 → 유의도 상승 곡선.
- **dipole 방향 안정성** — 에너지 임계값 변동 하에서 방향이 보존되는지 (SQT 시나리오라면 single-axis 보존 기대).
- **다극 스펙트럼** (l=1,2,3) — wall network 시나리오는 dipole 우세 + 작은 quadrupole; cosmic-string scar 시나리오는 quadrupole/소각도 자기상관 비중 증가.
- **에너지 의존성** — 임계 에너지 상승 시 deflection 감소 → SQT 결합 채널 (자기장 vs 소스 분포) 식별 가능.
- **이웃 매칭** — 도착방향과 local large-scale structure (LSS) 카탈로그 (2MRS, Swift-BAT, starburst galaxies) 의 cross-correlation. SQT 시나리오 (axiom 결정형 wall) vs 환경 결정형 시나리오의 분기 채널.

### 4.2 forecast 의 falsifiability 조건 (식 없음)
- GCOS / POEMMA 노출량 도달 시점에 **dipole 방향이 random walk 으로 흐트러지면** → P3b SQT 시나리오 약화 (single-axis 부재).
- dipole 진폭 OOM 이 holographic axiom OOM 과 자릿수 일치하지 않으면 → P3b 진폭 priori 도 KILL (L0/L1 강등 → L2).
- LSS cross-correlation 이 random 보다 강하게 환경에 결합하면 → axiom-driven priori 보다 environment-driven postdiction 으로 분류 변경.

### 4.3 8인 자유 도출 라운드 임무 항목 (L536 위임)
- (T1) Z₂ SSB 시점의 axiom-수준 결정 — Γ₀(t) 프로파일 → SSB 시점 → wall network 면적 OOM. *함수형은 본 감사 외부, Rule-A 라운드 산출.*
- (T2) wall ↔ matter / 자기장 결합 부호 — sprinkling 자유도 부호 고정 가능성.
- (T3) 방향 priori 의 추가 axiom 후보 (있다면) — 도입 시 [최우선-1] 위반 여부 자체검토.
- (T4) UHE-CR 다극 스펙트럼 forecast 의 OOM template — 수치 fit 금지, OOM 비율만.

---

## 5. P3b 등급 갱신 제안 (L536 → L542)

| 항목 | L536 | L542 (본 감사 갱신) |
|---|---|---|
| 진폭 priori | △ dormant | △ 조건부 가능 (holographic + sprinkling axiom OOM 채널 확정) |
| 방향 priori | (미평가) | **× 현재 axiom 셋에서 부재** — 추가 axiom 필요, 그 자체가 8인 도출 의무 |
| 시간정합 | ✓ pre-reg | ✓ (Auger 누적 진행 중 — postdiction 경계 상승 주의) |
| 종합 등급 | L1 cond (dormant) | **L1 cond (dormant) 유지, 단 "방향 priori 부재" 명시 추가** |

→ P3b 가 진정 priori 로 격상되려면 **방향 priori 채널이 axiom 으로 닫혀야** 한다. 현재 unblocked.

---

## 6. 본 감사가 *하지 않은 것* (CLAUDE.md 정합 자기검토)
- 수식 0건. 파라미터 값 0건. "A = ..." 형태 0건. ✓ [최우선-1]
- 8인 팀 도출 결과를 미리 적지 않음. ✓ [최우선-2]
- L14/L22 등 과거 결과의 이론 형태 재사용 0건. ✓
- 관측 수치 (Auger dipole 진폭/방향/유의도/임계 E) 본문 인용 0건 — 팀 라운드용 분리. ✓

---

## 7. 정직 한 줄

**P3b 의 진폭 priori 는 holographic + sprinkling axiom 으로 OOM 채널이 열려 있으나 dipole *방향* priori 는 현재 SQT axiom 셋 안에서 부재하며 추가 axiom 없이는 SQT 가 Auger dipole 방향을 사전에 지정할 수 없다 — 따라서 P3b 는 L1 conditional dormant 등급 유지, "방향 priori 부재" 단서를 명시 첨부함이 정직하다.**
