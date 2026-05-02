# L386 ATTACK_DESIGN — Z_2 SSB Finite Temperature

## 주제
Z_2 대칭 자발적 깨짐(SSB)의 유한온도 거동. 초기우주에서 임계온도 T_c 추정, 도메인 월(domain wall) 형성 적색편이 z_DW, 오늘의 잔존 월 밀도.

## 방향 (지도 금지)

### Phase A — 이론 도출 (8인 팀 자유)
- 입력: SQMH 응축장이 Z_2 이산대칭을 가진다는 가정. 진공기댓값 척도는 SQMH 자체에서 자율 결정.
- 8인은 다음 방향만 듣고 자율 토의:
  1. 유한온도장이론(thermal field theory)에서의 effective potential 행동
  2. 대칭 회복 → 깨짐 전이의 차수 (1차/2차/cross-over) 판별 기준
  3. Kibble 메커니즘에 의한 위상 결함 형성
  4. 2차원 결함(domain wall)의 우주론적 운명 (Zel'dovich-Kobzarev-Okun 진단)
- 금지: 특정 effective potential 형태를 사전 제시. 진공기댓값/quartic coupling 수치를 사전 박는 행위. T_c 후보값을 미리 알려주는 행위.

### Phase B — 수치 시뮬 (run.py)
- 8인이 도출한 이론을 Python 토이로 구현.
- 산출:
  - T_c 추정 (단위, 척도 자유)
  - 전이 시점 z_PT (대칭 회복 → 깨짐)
  - 도메인 월 형성 z_DW = z_PT (Kibble)
  - 오늘 z=0에서 도메인 월 표면밀도 σ_DW × 면적 → ρ_DW/ρ_crit 추정
  - Zel'dovich 한계와 비교 (월이 우주를 지배하는가?)

### Phase C — 4인 코드리뷰
- 자율 분담. T_c 적분, Kibble 결함 밀도, scaling solution, ρ_DW 단위 체크.

## 정직성 한 줄
도메인 월이 Zel'dovich 한계를 위반하면 SQMH Z_2 SSB 모델은 즉시 KILL — 단, bias 항 또는 inflation dilution 가능성은 별도 토의.

## 산출물
- `results/L386/REVIEW.md` — 8인 토의 + 4인 리뷰 요약
- `simulations/L386/run.py` — 토이 시뮬

## 재발방지 적용
- SI 단위 일관 (k_B, hbar, c 명시)
- multiprocessing 불필요 (저비용 토이)
- print() 유니코드 금지, ASCII 변수명
- numpy 2.x: np.trapezoid
