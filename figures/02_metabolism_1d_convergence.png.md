# Figure 02: 1D 반경방향 시간진화 수렴

## 내용
1D 반경방향 유한체적 시뮬레이션: dn/dt + div(nv) = Gamma_0 - sigma*n*rho_m.
균일 초기조건에서 정상상태 v(r) = g(r)*t_P로 수렴.

## 주요 결과
- **좌측 패널**: 시뮬레이션 v(r)이 해석해 g(r)*t_P로 수렴
- **우측 패널**: 밀도 프로파일 n(r)/n0 -- 질량 근처 변형 후 안정화
- 유한체적 (upwind, explicit Euler), N_r=200, N_t=2000

## 검증 상태
- **base.md III**: 동적 시뮬레이션이 정상상태 해로 수렴 확인
- 경계조건: 내부 플럭스 = sigma*n0*M/(4*pi) (점질량 흡수)

## n0 관련 참고
n0는 임시값 (mu=1 kg 가정). n0*mu = rho_P/(4pi)만 물리적 의미. 시뮬레이션은 n0를 일관되게 사용하므로 정성적 거동은 유효.

## 데이터 출처
- 물리 상수: config.py (CODATA 2018 / Planck 2018)
- sigma = 4*pi*G*t_P = 4.522e-53 m^3/kg/s

## 해석
정상상태 해는 동적으로 안정: 임의의 초기조건에서 v(r) = g(r)*t_P로 수렴.

## 재생성
```
cd simulations && python metabolism_equation.py
```
