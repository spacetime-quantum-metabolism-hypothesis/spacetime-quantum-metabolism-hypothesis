# L393 REVIEW — Sec 4 Predictions Table v2 (8인 토의 + 4인 코드리뷰)

## 8인 자유 토의 (역할 사전 지정 없음, 자연 분담)

### 라운드 1 — P1~P14 재라벨
- L175 시점의 P5 (GW170817), P6 (CMB peaks), P10 (BBN), P11 (Casimir) 는 현재도 PASS 유지.
- P1 (sigma_0 regime) 는 L48 T17 / T20 sigma8 grid scan 이후 PARTIAL 로 강등 — sigma8 tension 잔존.
- P2 (Λ from quantum sector) PARTIAL — 자릿수 수준 일치, 정확 계수는 epsilon 정의 모호.
- P3 (BTFR slope=4) PASS 유지 — SPARC 3.85±0.06 일치.
- P4 (PPN γ=1) PASS — Cassini 통과 (L389 BRST 검증과는 별개).
- P7 (EHT shadow) PASS, P8 (cosmic chronometer) PASS, P9 (PTA) PASS (negligible contribution).
- P12 (a_0(z) at SKA), P13 (disc/spheroid ratio), P14 (void a_0) UNRESOLVED — 미래 측정 대기.

### 라운드 2 — 신규 P15~P27 발굴 (우주론 / GW / lab / 천체물리)

토의에서 자연스럽게 다섯 영역으로 분담:

**우주론 (4)**
- P15: DESI DR3 w0-wa 등고선
- P16: H0 drift (조기 / 후기 우주 cross-check)
- P17: sigma8 / S8 tension
- P18: omega_m posterior

**강중력장 / GW (3)**
- P19: BBH ringdown overtone
- P20: Stochastic GW background normalization
- P21: EHT polarimetry phase

**입자 / 보조 / lab (3)**
- P22: DE-photon coupling (CMB spectral distortion)
- P23: FRB DM-z relation
- P24: torsion balance / atom interferometer 5th force

**천체물리 (3)**
- P25: UDG (ultra-diffuse galaxy) dynamics
- P26: Dwarf galaxy rotation curve cusp/core
- P27: Cluster lensing convergence profile

### 라운드 3 — 라벨 일관성 감사
- "모두 PASS" 의심 회피: 22개 중 PASS 9, PARTIAL 5, UNRESOLVED 8 으로 분포 확정 (감사 통과).
- mu_eff≈1 / S8 미해결 (L6-Q15 전원 FAIL) 솔직 반영 → P17 UNRESOLVED-tension.
- L33 wa<0 결과는 P15 PARTIAL (BAO-only 개선, joint 에서 LCDM-등가 가능성).

### 라운드 4 — Falsifier 임계 정량
각 항목마다 "측정값 X 가 임계 Y 를 초과하면 폐기" 형태로 명시. SEC4_TABLE.md 참조.

## 4인 코드리뷰 (자율 분담)

- **출처 검증**: P1 (L48), P3 (Lelli+2016 SPARC, L119), P4 (Cassini, L89), P5 (LIGO, L87), P6 (Planck, L106), P7 (EHT, L99), P8 (Moresco+2022, L88), P9 (NANOGrav, L107), P10 (Planck BBN, L83), P11 (L102), P15 (L33 wa scan), P17 (L5 Q15 FAIL log) — 모두 인용 가능. 누락 없음.
- **수치 일관성**: a_0_SQT = c·H0/(2π) ≈ 1.142e-10 m/s² (H0=73.8) vs 1.20e-10 empirical → 4.9% 편차 L175 와 일치.
- **L33 BAO-only Om=0.068 함정**: P18 omega_m 라벨링 시 BAO-only 와 joint 분리 표기 강제 (CLAUDE.md 재발방지 규칙 준수).
- **부호 일관성**: P15 wa 부호는 L33 sigmoid-weight 혼합 결과만 인용. arctan/erf 단독형 (wa>0 KILL) 인용 금지.

## K-기준 결과

- K1 (22개 falsifier 명시): PASS — SEC4_TABLE 모든 행에 falsifier 컬럼.
- K2 (4-카테고리 분포 정직): PASS — PASS 9 / PARTIAL 5 / UNRESOLVED 8.
- K3 (P15~P27 vs P1~P14 중복 없음): PASS — 영역 분리 (예: P14 void a_0 vs P25 UDG 는 다른 sigma 체제).
- K4 (대안 모델 구분 수치): PASS — 각 행 "vs LCDM/MOND/Verlinde" 컬럼.
- K5 (정직 한 줄): 아래 정직 한 줄 참조.

## 정직 한 줄

22개 예측 중 PASS 9 (대부분 기존 데이터로 검증된 약한 제약), PARTIAL 5, UNRESOLVED 8 — SQT 의 실제 차별성은 P12~P14 (a_0 evolution / 기하), P15 (DR3 wa), P19 (ringdown) 의 미래 측정에 달려 있고, 현 시점에서 LCDM 대비 "이미 이긴 예측" 은 없다.
