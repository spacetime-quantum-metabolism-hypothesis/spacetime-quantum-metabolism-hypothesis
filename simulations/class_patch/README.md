# Phase 2 Option A — CLASS C Patch (DEFERRED)

> **상태: 보류 (2026-04-10)**. Phase 2 는 Python 확장 경로 (Option B) 로 진행.
> 이 디렉토리는 full Planck TTTEEE Cl 이 필요한 Phase 3 단계에서만 재활성화.
> Option B 구현은 `simulations/phase2/` 참조.
>
> 보류 이유: (1) 1-2 개월 C 패치 비용 과대, (2) BAO+SN+RSD+compressed CMB 만으로
> Phase 2 판별력의 ~90% 확보 가능, (3) Windows 빌드 리스크 회피.

---

# Phase 2 Option A — CLASS/CAMB Patch (Coupled Quintessence + SQMH IDE)

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

### 수정 파일 (CLASS v3.x)

주의: CLASS v3.x 에는 별도 `source/quintessence.c`가 없음. Scalar field DE는
`source/background.c`의 `background_functions()` 내부에 통합되어 있고 (v2에서
존재하던 `quintessence.c`는 v3에서 제거됨), `fluid` module의 특수 케이스
(scf: scalar field dark energy)로 처리됨. 섭동 측은 `perturbations_derivs()`
(v3에서 `perturb_derivs`에서 이름 변경) 내부에 scf 블록이 있음.

| 파일 | 수정 내용 |
|------|-----------|
| `include/background.h` | `struct background`에 `SQMH_*` 필드 추가 (`scf` 블록 바로 뒤) |
| `include/input.h` | `struct precision`에 파서 엔트리 추가 |
| `source/input.c` | `input_read_parameters()`에 `SQMH_enabled`, `SQMH_V_family`, `SQMH_xi`, `SQMH_V_params` 파싱 |
| `source/background.c` | `background_functions()` 내부 기존 `scf` 블록 옆에 `SQMH` 분기 추가. coupled KG + matter continuity. |
| `source/perturbations.c` | `perturbations_derivs()` 내부 scf perturbation 블록 확장: coupled source term 추가 |

### 섭동 방정식 (Synchronous gauge, Fourier k)

Amendola 2000 (astro-ph/9908023) Eq. 18-20 (perturbation equations)과
Amendola, Quercellini, Tocchini-Valentini 2003 (astro-ph/0304325) 참조.
SQMH convention (beta = -Q_A, 부호 quintessence.py 문서 참조):

Scalar field perturbation (synchronous gauge, conformal time tau):
```
delta_phi'' + 2*a*H*delta_phi' + (k^2 + a^2*V''(phi)) * delta_phi
             + 0.5 * phi'*h' = -a^2 * beta * delta_rho_m
```
Matter density/velocity perturbations:
```
delta_m' + theta_m - 0.5*h' = -beta * phi'*delta_m + beta * delta_phi'
theta_m' + a*H*theta_m = -beta*k^2*delta_phi + beta*phi'*theta_m
```
(여기서 prime은 d/d(conformal tau); a*H = H_conformal = a*H_cosmic; beta는
quintessence.py 신호 규약과 동일)

## 구현 단계

### 단계 1: fork + 환경 구축 (1-3일)
```
git clone https://github.com/lesgourg/class_public.git simulations/class_patch/class_sqmh
cd simulations/class_patch/class_sqmh
make clean && make
./class explanatory.ini  # baseline sanity check
```

### 단계 2: background 패치 (1-2주)
- `patch_template.py`의 V(phi) 함수를 C로 포팅 (static inline helpers in background.c)
- 기존 `background.c`의 scf 분기를 템플릿으로 삼아 SQMH 분기 추가
- coupled KG: `phi'' + 2*H_conf*phi' + a^2 * dV/dphi = -a^2 * sqrt(2/3)*beta*rho_m` (conformal)
- coupled matter: `rho_m' + 3*H_conf*rho_m = +sqrt(2/3)*beta*phi'*rho_m`
- 초기조건: attractor (Amendola & Tsujikawa 교과서 §9.4) 또는 slow-roll
- Phase 1 `quintessence.py` 결과와 cross-check: `verify_background.py` 로 E(z), Omega_DE(z) 0.1% 이내 일치 확인

### 단계 3: 섭동 패치 (3-4주)
- `source/perturbations.c`의 `perturbations_derivs()` 내부 scf 블록 확장
- delta_phi, theta_m, delta_m 연립방정식에 coupled source term 추가
- gauge-invariant check: synchronous vs Newtonian 두 게이지에서 동일 결과
- TT/EE/lensing 출력 vs LCDM 잔차 확인 (Delta C_l/C_l < 0.1% at LCDM limit)
- 주의: 라디에이션 우세기 결합으로 BBN 제약 위반 방지 — phi 초기 frozen 확인

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
