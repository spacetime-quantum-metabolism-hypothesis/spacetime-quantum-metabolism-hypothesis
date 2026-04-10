# Figure 09: 양자-고전 전이 -- Q proportional to m^2

## 내용
SQMH 양자-고전 전이 매개변수 Q = Gamma_dec/Gamma_dyn의 질량 의존성. Q << 1 -> 양자, Q >> 1 -> 고전.

## 주요 결과
- 전이 질량: ~1e-14 kg (바이러스~박테리아 사이)
- Q proportional to m^2 -> **극히 가파른** 전이 (연속적이지만 사실상 이분법적)
- 주요 물체 위치:
  - 전자 (9.1e-31 kg): Q ~ 1e-34 -> 완전 양자
  - 양성자 (1.7e-27 kg): Q ~ 1e-26 -> 완전 양자
  - C60 (1.2e-24 kg): Q ~ 1e-20 -> 양자 (간섭 실험 성공과 일치)
  - 박테리아 (1e-15 kg): Q ~ 1e-2 -> 양자 경계
  - 모래알 (1e-6 kg): Q ~ 1e16 -> 완전 고전

## 검증 상태
- **base.md VIII.1**: Q proportional to m^2, 전이점 ~1e-14 kg 확인
- 추가 자유 매개변수: 0개

## 데이터 출처
- 전자/양성자 질량 -- CODATA 2018
- C60 질량 -- 720.66 u (IUPAC 2016)
- 양자 간섭 실험: Arndt et al. (1999), Nature 401, 680

## 해석
SQMH에서 양자-고전 경계는 시공간 대사 디코히어런스율 vs 양자 역학적 시간척도의 경쟁으로 결정. m^2 의존성은 Penrose-Diosi 모델과 유사하지만, SQMH에서는 시공간 양자 소멸에서 자연스럽게 도출됨.

## 재생성
```
cd simulations && python quantum_classical.py
```
