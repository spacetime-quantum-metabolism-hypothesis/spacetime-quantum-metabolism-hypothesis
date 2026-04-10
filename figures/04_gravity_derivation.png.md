# Figure 04: SQMH에서 뉴턴 중력 도출

## 내용
sigma = 4*pi*G*t_P 항등식을 3가지 측면에서 검증: (1) v(r) = g(r)*t_P, (2) 기계정밀도 일치, (3) 포텐셜 U=-GMm/r.

## 주요 결과
- **패널 1**: SQMH sigma*M/(4*pi*r^2) = g(r)*t_P -- 정확히 일치
- **패널 2**: 상대오차 ~1.5e-16 (기계정밀도)
- **패널 3**: 포텐셜 유동 (Lamb 1932) -> U(r) = -GMm/r

## 핵심 수치
- sigma = 4.522e-53 m^3/kg/s (SI)
- sigma/(4*pi*t_P)에서 G 복원: 상대오차 = 3.9e-16
- v(지구표면) = 5.29e-43 m/s, v/c = 1.77e-51

## 검증 상태
- **base.md III.1 (sigma=4piG*t_P, Issue #28 해결)**: 검증 완료
- G 복원 기계정밀도 달성

## 데이터 출처
- G = 6.67430e-11 m^3/kg/s^2 -- CODATA 2018
- t_P = 5.391e-44 s -- 플랑크 시간
- Lamb, H. (1932), *Hydrodynamics*, 6th ed., Cambridge Univ. Press

## n0, mu 참고 (base.md 3.4)
G = n0*mu*sigma^2/(4pi)는 변수 치환. n0*mu = rho_P/(4pi) ~ 4.1e95 kg/m^3. 개별 n0, mu는 미결정.

## 재생성
```
cd simulations && python gravity_derivation.py
```
