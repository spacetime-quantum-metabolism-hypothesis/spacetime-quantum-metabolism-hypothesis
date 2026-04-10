# CLASS 설치 및 SQMH 패치 가이드

## 요구사항
- gcc/clang (C99 이상)
- GNU make
- Python 3.8+ (classy wrapper)
- Cython (classy 빌드용)

## Linux / WSL
```
git clone https://github.com/lesgourg/class_public.git class_sqmh
cd class_sqmh
make clean
make -j4
make classy  # Python wrapper
python -c "from classy import Class; print('CLASS import OK')"
```

## Windows 주의사항

네이티브 Windows에서 CLASS 빌드는 권장하지 않음. **WSL2 (Ubuntu 22.04)** 사용:
```
wsl --install Ubuntu-22.04
# in WSL
sudo apt update
sudo apt install build-essential gcc make python3-dev python3-pip cython3
pip install cython numpy
# 이후 Linux 절차 동일
```

## Planck 2018 likelihood (clik)
```
wget http://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_Likelihood_Code-v3.0_R3.10.tar.gz
tar -xzf COM_Likelihood_Code-v3.0_R3.10.tar.gz
cd code/plc_3.0/plc-3.1
./waf configure --install_all_deps
./waf install
source bin/clik_profile.sh
```

## DESI DR2 likelihood (Cobaya 용)
```
pip install cobaya
cobaya-install cosmo -p packages/
# DESI BAO 2025 likelihood는 Cobaya 3.5+ 에 내장
```

## 빌드 검증 체크리스트
- [ ] `./class explanatory.ini` → `.dat` 파일 생성 확인
- [ ] Python `from classy import Class` 성공
- [ ] `cosmo = Class(); cosmo.set({'h': 0.67, 'Omega_cdm': 0.26}); cosmo.compute()` 무에러
- [ ] baseline Planck 2018 chi2 재현 (~2350)

## SQMH 패치 적용
1. `class_sqmh/source/background.c` 에 `background_sqmh_functions()` 추가 (패치 파일 참조)
2. `class_sqmh/source/perturbations.c` 에 scalar field perturbation 블록 추가
3. `class_sqmh/include/background.h` 의 struct background 에 필드 추가
4. `make clean && make -j4` 재빌드
5. `simulations/class_patch/verify_background.py` 로 Phase 1 모듈과 cross-check
