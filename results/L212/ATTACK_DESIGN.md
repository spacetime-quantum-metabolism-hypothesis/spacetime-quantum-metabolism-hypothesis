# L212 — OPEN #1: tau_q micro origin 정량 검증

## 8인팀 공격 설계

**Target**: L210에서 OPEN으로 분류된 5개 회피 항목 중 #1 — `tau_q` (metabolism 시간 척도) 의 미시 기원.

### 약점 진단 (8인 합의)

1. **A1 (Theorist)**: tau_q는 a3에서 phenomenological 도입. SM 입자 lifetime 계열 (tau_neutron ~ 880s, tau_muon ~ 2.2e-6s) 과 무관하게 tau_q ~ t_Planck * (n0/n_Pl)^k 형태로 도입됨. k의 값이 free? — 만약 k=1 이면 tau_q ~ t_Pl/Upsilon ~ 1e-30s 이고, k=0 이면 t_Pl ~ 1e-44s. 실측 부재.
2. **A2 (Phenomenologist)**: 만약 tau_q가 우주 나이 스케일 (Hubble time ~ 1/H0) 과 무관하다면, σ_0 calibration 이 tau_q 에 의존해야 함. L207 Bianchi 결과 ρ_q/ρ_Λ=1.0000 가 *어떤* tau_q 에서나 성립하는지 증명 필요.
3. **A3 (Skeptic)**: 자유 파라미터 1개 추가 (tau_q 자체 또는 k). Branch B 3 params + tau_q = 4 params. AICc 패널티 +2 → ΔAICc 99 → 97. 여전히 큰 우위지만 zero-free-parameters claim 약화.
4. **A4 (Observer)**: tau_q가 cosmological 인지 microscopic 인지 구분하는 관측 없음. CMB μ-distortion (FIRAS |μ|<9e-5) 가 tau_q ~ 1/H_recombination 에 sensitive 하다면 제약 가능.
5. **A5 (Math)**: dimensional analysis 만으로는 tau_q ~ (n0 σ_0)^{-1} 도 가능. 이 경우 tau_q는 n0, σ_0 derivable. 독립 free parameter 아님.
6. **A6 (Numerical)**: Python 토이로 tau_q grid scan [t_Pl, 1/H0] 7 decade, ρ_q/ρ_Λ 변화 측정.
7. **A7 (Devil's advocate)**: tau_q가 정말 cosmic 이라면 dark energy 가 tau_q^{-1} 에 비례 → today's H0 와 결합. 우연 일치 의심.
8. **A8 (Editor)**: JCAP referee 가 "what determines tau_q?" 질문 100% 던짐. 기존 a3 정의로 답 불충분.

### 합의 KILL 기준

- **K-tau1**: tau_q grid scan 결과 ρ_q/ρ_Λ 가 tau_q 에 의존하면 (Δ > 1%), Bianchi balance 가 fine-tuning 임. SQT 자기일관성 약화.
- **K-tau2**: tau_q ~ (n0 σ_0)^{-1} derivable 증명 실패 시, 4번째 free parameter 인정.

### 실행 방향

1. 토이 Python: tau_q ∈ [1e-44, 1e17] s 의 ρ_q/ρ_Λ 계산 (7 decade).
2. (n0 σ_0)^{-1} 와 tau_q 비교 — 일치하면 derivable.
3. 결론: derivable 인지, 진짜 free 인지 정직 기록.
