# Phase 2 — CLASS/CAMB Patch (Coupled Quintessence + SQMH IDE)

## 목적

base.fix.class.md Phase 2. Phase 1 (BAO-only background)이 V(phi) 구분 불가로 판명됨에 따라:

1. **CMB TT/EE/lensing** 스펙트럼으로 $w_a < 0$ 판별력 확보
2. **Linear perturbations** (density + velocity + metric) 일관 계산
3. **S_8 tension** 독립 진단

## 대상 코드

**권장**: CLASS (`github.com/lesgourg/class_public`)
- C 기반, MontePython/Cobaya 즉시 통합 가능
- 기존 quintessence 모듈 존재 (`source/quintessence.c`) — fork하여 V(phi) 교체

**대안**: CAMB (`github.com/cmbant/CAMB`)
- Python API 편의성 (f2py), 그러나 IDE coupled 지원 제한적

## 패치 범위

### 수정 파일 (CLASS)
| 파일 | 수정 내용 |
|------|-----------|
| `include/background.h` | `struct background`에 `xi_q`, `V_family`, `V_params[]` 필드 추가 |
| `source/background.c` | `background_functions()` 에 coupled KG equation 통합; V(phi) 3종 callable |
| `source/perturbations.c` | scalar field perturbation delta_phi, theta_phi 방정식 추가 (Amendola 2000 Eq. 8-10 참조) |
| `include/input.h` | 신규 파라미터 입력 (`SQMH_xi`, `SQMH_V_family`, `SQMH_V_params`) |

### 섭동 방정식 (Synchronous gauge, Fourier k)
```
delta_phi'' + 2H*delta_phi' + (k² + a²*V''(phi)) * delta_phi
  = -0.5*phi'*h' - a²*xi_q*delta_rho_m
delta_rho_m' + ... = + xi_q*phi'*delta_rho_m + xi_q*rho_m*delta_phi'
```
(Amendola 2000, Phys. Rev. D 62, 043511, Eq. 15-17)

## 구현 단계

### 단계 1: fork + 환경 구축 (1-3일)
```
git clone https://github.com/lesgourg/class_public.git simulations/class_patch/class_sqmh
cd simulations/class_patch/class_sqmh
make clean && make
./class explanatory.ini  # baseline sanity check
```

### 단계 2: background 패치 (3-5일)
- `patch_template.py` 의 V(phi) 함수를 C로 포팅
- `source/quintessence.c` 복제 후 `source/sqmh_background.c` 신규
- Phase 1 `quintessence.py` 결과와 cross-check: 동일 (phi, phi_N) 해 얻는지 검증

### 단계 3: 섭동 패치 (5-10일)
- `source/perturbations.c` 에 `perturb_sqmh_derivs()` 추가
- gauge-invariant check (synchronous vs Newtonian)
- TT/EE/lensing 출력 vs LCDM 잔차 확인

### 단계 4: Planck likelihood 실행 (2-3일)
- `clik` 인스톨 (Planck 2018 공식)
- MontePython 또는 Cobaya 구동:
  - `yamls/sqmh_planck.yaml` (Phase 3 디렉토리 참조)

## 예상 결과

| 시나리오 | Delta_AIC (Planck + DESI) | 판정 |
|----------|---------------------------|------|
| V_RP 강한 개선 | < -6 | **Path A 성공** — SQMH-RP 변형 생존 |
| V_RP 약한 개선 | -6 ~ -2 | Phase 3 full joint 필수 |
| V_RP 개선 없음 | > -2 | **Path F 반증** — base.md §XVII 갱신 |

## 리스크 및 함정

1. **gauge 선택 오류**: synchronous vs Newtonian. CLASS 기본은 synchronous, 단 perturbation 진단은 둘 다 체크.
2. **초기조건 설정**: phi(z=1e10), phi'(z=1e10) 의 선택. Amendola는 attractor 초기조건 사용.
3. **Coupled matter 부호**: Amendola 2000 convention vs SQMH $\xi\phi T^a_a$ 부호 일치 확인. Phase 1 `quintessence.py` 의 `+sqrt(2/3)` vs `-sqrt(6)` 부호 참조.
4. **상대론적 matter**: 방사 우세기에 xi coupling이 BBN 제약 위반 금지 → phi 초기 frozen 확인.

## 파일 구조 (이 디렉토리)

```
simulations/class_patch/
|-- README.md            # 이 문서
|-- install_notes.md     # CLASS 빌드 가이드 (Windows/Linux)
|-- patch_template.py    # V(phi) 함수 레퍼런스 (Python → C 포팅 원본)
|-- verify_background.py # Phase 1 vs CLASS patched background 교차검증
|-- (class_sqmh/)        # git clone 이후 생성되는 CLASS fork
```

## Phase 1 → Phase 2 교차 검증

`verify_background.py`:
- 동일 (V_family, beta, params)로 Phase 1 quintessence.py 및 CLASS-SQMH 각각 실행
- E(z), Omega_DE(z), w_DE(z) 비교
- |delta| < 1% 요구

## 참고 문헌

- Amendola, Phys. Rev. D 62, 043511 (2000) — coupled quintessence 기본 문헌
- Amendola & Tsujikawa, *Dark Energy: Theory and Observations* (Cambridge, 2010), Ch. 9
- Lesgourgues & Tram, "The Cosmic Linear Anisotropy Solving System (CLASS) IV", 1104.2935
- Brinckmann & Lesgourgues, "MontePython 3", 1804.07261
