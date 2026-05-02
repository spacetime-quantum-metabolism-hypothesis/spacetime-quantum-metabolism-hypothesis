# L423 NEXT_STEP — 8인 다음 단계 설계

목적: outer asymptotic velocity 영역에서 SQT 와 MOND 가 (a) 정확히 같은 limit 으로 떨어지는지, (b) 떨어지는 속도/형태에서 차이가 있는지 정량 비교.

## CLAUDE.md 준수
- 방향만 제공. 수식 미기재.
- 8인 자율 분담. 사전 역할 없음.

## 단계 1 — outer 영역 정의 표준화
- SPARC 카탈로그 V_flat, e_Vflat, Q flag 사용.
- 보조 정의: rotmod 에서 R > k · R_disk (k 후보 2/3/4) 평균 V_obs.
- 두 정의가 일치하는 sample 만 1차 분석에 사용.

## 단계 2 — Tully-Fisher 일반화 fit
- 대상 함수형: V_flat^n = K · M_bar^m (n, m, K 자유). M_bar = M_disk + M_gas + M_bul (추정 Υ_disk = 0.5 M⊙/L⊙ default).
- 비교 대상:
  - 모델 A (MOND/SQT 공통 limit): n=4, m=1 고정.
  - 모델 B: 자유 (n, m).
  - AICc 차이 < 4 → 데이터가 추가 자유도 정당화 못함.
- 출력: posterior 또는 best-fit + 1σ + AICc.

## 단계 3 — sub-leading 잔차 분석
- 잔차 r_i = ln V_flat,obs - 0.25 ln(G M_i a0_global) (a0_global 전체 fit 으로 결정).
- r_i 가 (a) M_bar, (b) Σ_disk (SBdisk), (c) Q flag 와 상관 있는지.
- 상관이 nominal noise 보다 크면 SQT 차별 미세항 영역. 작으면 SQT vs MOND 구분 불능.

## 단계 4 — outer rotation curve shape (sub-leading)
- 각 은하 outer 점에서 V(R)/V_flat 의 R 의존을 phenomenological 함수형으로 fit.
- 모든 175 은하의 평균 잔차 곡선이 R 의 함수로 평탄하면 deep-MOND 와 구분 안 됨.
- 평균 잔차에 systematic 곡률 발견 시 SQT 검증 첫 실증 신호.

## 단계 5 — Q flag / SB 분리 cross check
- Q=1 highest-quality 은하만 재실행. n, m posterior 변화 모니터.
- HSB vs LSB 분리. implied a0 차이 시 보편상수 가설 위반.

## 단계 6 — bulge-dominant subsample
- V_bul,max / V_obs,max > 0.5 은하에서 1/4 power 보존성 시험. 위반 시 deep-MOND limit assumption 재검토 필요.

## 결정 기준 (kill / pass)
- PASS (SQT 차별 가능성 유지): 단계 3 또는 단계 4 에서 σ_systematic > σ_data noise.
- KILL (MOND 와 phenomenological 등가): 모든 단계에서 (n, m) ≈ (4, 1) 1σ 내 및 잔차 무상관.

## 4인 실행 위임
- 4인 코드리뷰 팀이 단계 1 + 2 를 run.py 로 실행. 단계 3~6 은 결과에 따라 후속.
