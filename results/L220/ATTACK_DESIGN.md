# L220 — PARTIAL #4: Bianchi full ODE (10%/Hubble)

## 8인팀 공격
**Target**: L207 Bianchi balance ρ_q/ρ_Λ=1.0000 점근. 시간 의존 ODE 풀어 cosmological 진화 추적, 10%/Hubble 변동 한계 검증.

### 약점
1. L207 결과 정적 비율. 시간 진화 미검증.
2. ∇μ T^μν_q + ∇μ T^μν_Λ = 0 가 모든 z 에서 유지?
3. dρ_q/dt + 3H ρ_q = -dρ_Λ/dt 토이.

### 실행
- ODE: dρ_q/dN = -3 ρ_q + 3 ρ_Λ (Bianchi balance), 초기 z=1100, today z=0.
