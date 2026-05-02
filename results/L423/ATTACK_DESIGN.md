# L423 ATTACK_DESIGN — 8인 공격 (Rule-A 자율 분담)

주제: outer-region 평탄 회전속도 V_flat = (G·M·a0)^(1/4) (MOND-like Tully-Fisher 잔향)
질문: 이 한계법칙이 SQT 만의 차별성인가, 아니면 MOND/Verlinde/CDM-halo 모두에서 동일하게 도출되는가?

## CLAUDE.md 준수
- 본 문서는 "방향만" 기록한다. 구체 수식/파라미터는 팀 자율 도출 영역.
- 8인은 사전 역할 배정 없음. 토의 중 자연 분업.

## 공격 1 — Tully-Fisher exponent uniqueness
- 방향: V^4 ∝ M 의 4 제곱은 (a) MOND deep-MOND limit, (b) Verlinde EVH, (c) SQT outer-asymptotic regime, (d) NFW halo with mass-concentration relation 모두에서 출현 가능.
- 검토 대상: 동일 exponent 가 나오는 다른 이론군이 있다면 SQT "유일성 주장" 은 즉시 무효.
- 공격 결론 후보: "유일하지 않음. 그러나 SPARC outer slope d ln V / d ln R 의 sub-leading correction 이 이론마다 다르다."

## 공격 2 — SPARC outer 영역 정의의 자의성
- 방향: "outer flat region" 정의가 R > R_flat, V 변동 < ε 등 cutoff 의존.
- cutoff 변화에 따라 V_flat 추정이 바뀌면 (G M a0)^{1/4} 적합도 자체가 cutoff artefact.
- 카탈로그 e_Vflat / Q flag 활용 검증 필요.

## 공격 3 — a0 보편상수 vs 은하별 변동
- 방향: MOND 는 a0 ≈ 1.2e-10 m/s^2 보편 상수. SQT 가 a0 를 "ψ-기반 거시 길이/시간 척도" 에서 도출한다면 은하 환경 (Σ_baryon, ρ_local) 에 따라 미세 변동 가능.
- SPARC 175 은하 over residual 분포에서 a0 변동 detection 가능 여부.

## 공격 4 — V_flat^4/(G M) 의 outlier 은하군
- 방향: low-surface-brightness vs high-SB 은하에서 implied a0 차이.
- Q=1/2/3 quality flag 별 분리 fit. Q=1 (highest) sample 만으로 재시험.

## 공격 5 — 차별 미세항 (sub-leading correction)
- 방향: V(R) = V_flat · [1 + δ(R)] 에서 δ(R) 의 R 의존 함수 형태가 MOND vs SQT 다른지.
- MOND: μ(x) interpolation function 으로 fixed.
- SQT: outer regime 에서 ψ 가 어떤 함수형태로 흐르는지에 따라 δ(R) 다른 prediction 가능.
- 이 미세 차이가 SPARC σ_Vobs 보다 큰지가 차별 가능성의 정량 기준.

## 공격 6 — bulge 우세 은하의 위반
- 방향: V_bul dominant 은하에서 deep-MOND 가설은 약화. SQT 가 bulge regime 에서도 같은 (G M a0)^{1/4} 를 주장한다면 falsifiable.

## 공격 7 — Vflat 정의 자체의 정의 의존성
- 방향: SPARC 카탈로그 V_flat 는 outer fit 의 평균. 다른 정의 (V_max, V_2.2 disk-scale) 와 비교 시 1/4 power 가 보존되는지.

## 공격 8 — fit 비교의 통계적 등가성
- 방향: SPARC 175 sample 에서 두 모델 (V_flat^4 = G M a0 vs 일반화 V_flat^n = K M^m) 자유 파라미터 fit. n, m 의 posterior 가 (4, 1) 을 포함하는지.
- AICc 비교: free (n,m) 모델이 자유도 +2 패널티를 정당화하는지.

## 8인 합의 (자율 분담 후)
- 공격 1, 5, 8 이 falsifiable test 의 핵심.
- 공격 2, 7 은 데이터 정의 sanity check.
- 공격 3, 4, 6 은 이론간 미세 차이 탐색용.
- 4인 코드리뷰 팀이 공격 1 + 8 을 정량 실행 (run.py).
