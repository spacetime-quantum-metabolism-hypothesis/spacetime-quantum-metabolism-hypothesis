# Figure 01: 대사 정상상태 검증

## 내용
SQMH 연속방정식 정상상태: v(r) = sigma*M/(4*pi*r^2) = g(r)*t_P.
유입속도 = 중력가속도 x 플랑크시간. (Issue #28 해결 반영)

## 주요 결과
- **좌측 패널**: SQMH v(r)와 g(r)*t_P 정확히 일치 (로그 스케일)
- **우측 패널**: 상대오차 ~1.5e-16 (기계정밀도, IEEE 754 double)
- sigma = 4*pi*G*t_P는 도출값 (피팅 아님)

## 핵심 수치
- sigma = 4.522e-53 m^3/kg/s (SI)
- v(지구표면) = 5.29e-43 m/s, v/c = 1.77e-51
- g(지구표면) = 9.82 m/s^2

## 검증 상태
- **base.md III.1 (sigma=4piG*t_P)**: 검증 완료
- 추가 자유 매개변수: 0개

## 데이터 출처
- G = 6.67430e-11 m^3/kg/s^2 -- CODATA 2018
- t_P = 5.391e-44 s -- G, hbar, c에서 도출
- M_Earth = 5.972e24 kg, R_Earth = 6.371e6 m -- IAU 2015

## 해석
sigma=4piG*t_P 항등식: 시공간 양자 유입속도 = g*t_P. 중력은 플랑크 밀도 매질(n0*mu ~ 4.1e95 kg/m^3)을 통한 느린 유입에서 발생.

## 재생성
```
cd simulations && python metabolism_equation.py
```
