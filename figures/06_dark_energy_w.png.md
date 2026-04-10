# Figure 06: 암흑에너지 상태방정식 w(z) -- SQMH 이차 IDE

## 요약
SQMH 이차 IDE (Q가 rho_DE*rho_m에 비례) w(z) 진화. xi_q > 0만 SQMH 물리적.

## 결과

### w0-wa 값 (최소자승 CPL 피팅, z=[0,1])
| xi_q | w0 | wa | 상태 |
|------|----|----|------|
| -0.05 | -1.016 | -0.092 | phantom (w<-1), SQMH 위반 |
| 0.00 | -1.000 | 0.000 | LCDM |
| +0.02 | -0.994 | +0.034 | SQMH 물리적 |
| +0.05 | -0.984 | +0.083 | SQMH 물리적 |
| +0.10 | -0.968 | +0.156 | SQMH 물리적 |
| +0.20 | -0.937 | +0.274 | SQMH 물리적 |

### 패널 설명
- **패널 1**: w(z) -- xi_q>0: w>-1 (phantom divide 위), xi_q<0: w<-1
- **패널 2**: omega_DE(z) = rho_DE/rho_crit,0 물리적 밀도 진화
- **패널 3**: w0-wa 평면 -- SQMH 궤적 vs DESI DR2 타원 (상관 rho~-0.8)

### SQMH vs DESI w0-wa 방향
- **SQMH (xi_q>0)**: w0>-1, wa>0 -> 우상 사분면
- **DESI DR2**: w0~-0.757, wa~-0.83 -> 우하 사분면
- **wa 부호 불일치**: 선도차수 2체 결합은 wa>0. wa<0은 V(phi) 감쇠 역학 필요 (base.md XVI.6)

## 주의사항
- DESI 타원 = DESI+Planck+DES-all 결합 분석 (BAO 단독 아님)
- xi_q<0는 SQMH 물리 위반 (phantom)

## 데이터 출처
- DESI DR2 w0-wa: w0=-0.757+/-0.058, wa=-0.83+0.24/-0.21 (arXiv:2503.14738, arXiv:2507.09981)
- Planck 2018: arXiv:1807.06209

## 재생성
```
cd simulations && python dark_energy_w.py
```
