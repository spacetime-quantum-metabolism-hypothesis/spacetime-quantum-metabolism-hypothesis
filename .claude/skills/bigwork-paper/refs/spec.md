# Spec — SQMH Paper Repository

## 레포 구조 (목표)
```
sqmh/
├── README.md                    # 영문 개요 + 핵심 수식 + 실행 방법
├── base.md                      # 원본 가설 문서 (한국어)
├── paper/
│   ├── 01_introduction.md       # 가설 소개 + 동기
│   ├── 02_metabolism_equation.md # 대사 연속방정식
│   ├── 03_gravity_derivation.md # 뉴턴 중력 도출
│   ├── 04_lagrangian.md         # 라그랑지안 + 관측 검증
│   ├── 05_dark_energy.md        # 암흑에너지 + w(z) 예측
│   ├── 06_quantum_classical.md  # 양자-고전 전이
│   ├── 07_connections.md        # 5개 독립 프로그램 연결
│   ├── 08_predictions.md        # DESI DR3 사전 예측
│   └── 09_discussion.md         # 한계 + 검증 로드맵
├── simulations/
│   ├── requirements.txt
│   ├── config.py                # 물리 상수 + SQMH 매개변수
│   ├── metabolism_equation.py   # 대사 연속방정식 시뮬레이션
│   ├── gravity_derivation.py    # 뉴턴 중력 도출
│   ├── dark_energy_w.py         # w(z) 계산 + DESI 비교
│   ├── cosmic_three_eras.py     # 우주 3시대 재현
│   ├── quantum_classical.py     # Q 전이 매개변수
│   ├── desi_fitting.py          # DESI DR2 피팅
│   └── desi_dr3_prediction.py   # DR3 사전 예측
├── figures/                     # 생성된 그래프
└── LICENSE
```

## Rules
- Python 3.10+, numpy/scipy/matplotlib/astropy
- 모든 상수는 config.py에서 중앙 관리
- 각 시뮬레이션 독립 실행 가능 (standalone)
- 그래프는 figures/에 자동 저장
- KPI (define.md) 기준으로 검증
- 자유 매개변수 0개 원칙 유지 — G, H₀, Ωₘ 등 관측값만 사용
