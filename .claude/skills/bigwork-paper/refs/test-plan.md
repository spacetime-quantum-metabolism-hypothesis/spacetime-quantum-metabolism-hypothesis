# Test Plan

## 체크포인트별 검증

### CP1: 기반 구조 (config + metabolism_equation)
- [ ] config.py: G, H₀, Ωₘ, σ=4πG 값 정확
- [ ] metabolism_equation.py: 1D 정상상태 → v(r) = GM/r² 수렴 (오차 <1%)
- [ ] 그래프 출력: v(r) vs 1/r² overlay

### CP2: 중력 + 우주론
- [ ] gravity_derivation.py: 포텐셜 U(r) = -GMm/r 재현
- [ ] cosmic_three_eras.py: 복사(a⁻⁴)→물질(a⁻³)→DE 전이 시점 정확
- [ ] dark_energy_w.py: w₀ > -1, wₐ < 0 확인

### CP3: 양자 + DESI
- [ ] quantum_classical.py: Q ∝ m² 스케일링, 전이점 ~10⁻¹⁴ kg
- [ ] desi_fitting.py: ΛCDM 대비 Δχ² < 0 확인
- [ ] desi_dr3_prediction.py: 변곡점 위치 + 신뢰구간 출력

### CP4: 논문 + README
- [ ] README.md: 설치→실행→그래프 재현 가능
- [ ] paper/ 섹션 9개: base.md 내용 완전 커버
- [ ] figures/: 최소 7개 핵심 그래프

### CP5: 최종 검증
- [ ] fresh clone → pip install → 전체 실행 성공
- [ ] 물리 상수 교차 검증 (PDG/Planck 2018)
- [ ] 자유 매개변수 0개 원칙 위반 없음 확인

## Evaluator 검증 시점
- CP1 완료 후: 수식 정확성 리뷰
- CP3 완료 후: DESI 피팅 로직 리뷰
- CP5: 전체 리뷰
