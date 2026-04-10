# Figure 03: 세 영역 (공동 / 경계 / 클러스터)

## 내용
SQMH 순대사율 R(rho_m) = Gamma_0 - sigma*n0*rho_m 부호에 따른 3개 영역 결정.

## 주요 결과
- **파란 영역** (rho_m < rho_eq): 순생성 -> 시공간 팽창 (공동)
- **빨간 영역** (rho_m > rho_eq): 순소멸 -> 중력 수축 (클러스터)
- **초록선**: 평형밀도 rho_eq = Gamma_0/(sigma*n0)
- 우주 평균 rho_m0 ~ 2.69e-27 kg/m^3

## n0 임시값 참고
n0는 개별적으로 미결정 (mu=1 가정). rho_eq는 n0 선택에 의존. 3영역 구조는 정성적으로 견고. sigma*n0*rho_m0/Gamma_0 비율은 n0 선택과 무관하게 일관.

## 검증 상태
- **base.md II**: 3영역 구조 확인
- 우주 스케일에서 순생성 -> 가속 팽창과 정합

## 데이터 출처
- Gamma_0, sigma, n0: config.py (sigma = 4*pi*G*t_P, Issue #28 해결)
- rho_m0 = Omega_m * rho_crit -- Planck 2018 (arXiv:1807.06209, Table 2)

## 재생성
```
cd simulations && python metabolism_equation.py
```
