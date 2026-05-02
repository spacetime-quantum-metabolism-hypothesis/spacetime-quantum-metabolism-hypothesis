# L424 NEXT_STEP — 8인팀 다음 단계 설계

선행: L424/ATTACK_DESIGN.md (B1–B8) — dSph saturation "prediction" 의
*post-naming* 위험과 P9 anchor 추가의 *강제력 ≠ pool 확대* 분리 요구.

원칙: CLAUDE.md [최우선-1, 2] — 방향만 기술, 수식/파라미터값 미지정.
역할 사전 지정 없음 (Rule-A).

---

## 1. 8인팀 토의 (요약 — Local Group dSph σ₀ 측정값 archive 가용성)

**P1**: "L405 P9 forecast 의 (-0.3, 0.85, 0.12) 는 toy. 실 dSph 측정치를
아카이브에서 확보해야 forecast 가 데이터-기반 forecast 로 이행한다.
Local Group 전통 dSph (classical 8개) 의 운동학·structural 파라미터는
McConnachie 2012 (AJ 144, 4) 카탈로그가 표준 — public, peer-reviewed, ADS."

**P2**: "Gaia DR3 (2022) 이후 Draco / UMi / Sculptor / Fornax / Carina /
Leo I / Leo II / Sextans 의 별별 시선속도 + proper motion 결합 mass 추정이
가용. NIH/NASA ADS 검색 키워드로 'dwarf spheroidal velocity dispersion
Gaia DR3' 가 표준. Spitzer/SAGE-SMC 광도계는 보조 채널."

**P3**: "그러나 σ₀ (SQMH 정의: 4πG·t_P × 환경 보정) 와 dSph 관측량
(중심 시선속도분산 σ_los, half-light radius r_half, 동력학질량 M_dyn)
사이의 변환식이 paper 에 없다. ATTACK B4. 변환 prior 자체를 anchor 화
하면 prior 자유도 +1, ATTACK B2 의 자유도-우위 위험과 충돌. 변환 *없이*
사용하려면 dSph 환경 ρ_env 만 anchor 로 쓰고 σ₀ 자체는 fit 결과로 read-out
하는 *환경-only anchor* 로 전환."

**P4**: "환경-only anchor 는 (a) ρ_env(dSph) 자체를 anchor 로 추가하고
(b) 모델이 그 위치에서 예측하는 σ₀ 를 *후* 비교, (c) 비교가 통과하면
강화 / 실패하면 기각. 즉 'saturation' 의 부호 (B6) 가 결정될 때까지
σ₀ 값 자체는 anchor pool 에 넣지 않는다. 이게 사후 cherry-pick 회피."

**P5**: "데이터 가용성 정리:
- McConnachie 2012 카탈로그: 모든 Local Group dSph 의 (D_LG[kpc], M_V,
  r_half, σ_los, M_dyn) — public TXT/PDF, ADS 2012AJ....144....4M.
- Gaia DR3 RVS subsample (Vallenari et al. 2023): classical dSph 별별 RV
  + PM, ESA Gaia archive open.
- Walker et al. 2009 (ApJ 704, 1274): dSph velocity dispersion profile 통합.
이 셋 조합이면 dSph anchor pool (Draco, UMi, Scl, Sextans, Carina) 5개
구성 가능. r_env 매핑은 D_LG (Local Group barycenter 거리) 로 1차 근사
— 단, ATTACK B3 regime 양다리 caveat."

**P6**: "철학: SQMH P9 가 *prediction* 이 되려면 σ₀_dSph 의 priori 구간이
paper §4 에 *수치 등록* 되어야 한다. 현재는 'low-ρ_env regime 재진입'
정성 진술 only. 본 L424 NEXT_STEP 의 task 는 (1) 측정 archive 정리,
(2) 환경-only anchor 모드 forecast, (3) 부호-결정 임계 사전등록.
*priori 수치 등록 없이는* 본 forecast 도 ATTACK B1 post-naming 안에 머문다."

**P7**: "JCAP timeline: paper submission *전* dSph anchor 추가 시도는
'optional disclosure' 로만 가능. 본 L424 forecast 가 강화 (compat) 든
약화 (tension) 든 결과는 §6.1 row #5 disclosure 표 update 로만 반영,
abstract / headline 수정 금지. ATTACK B7 toy-caveat 동반 필수."

**P8 (synthesizer)**: "다음 단계 합의:
(a) 즉시 (이번 세션): 5개 dSph anchor pool (Draco, UMi, Scl, Sextans, Carina)
    의 archive 측정값 (McConnachie 2012 + Gaia DR3) 을 *문헌 표준값* 으로
    하드코딩. ρ_env 매핑은 D_LG 기반 1차 근사 (galactic-internal regime
    버전 / Local Group regime 버전 두 매핑 비교).
(b) 환경-only anchor + σ₀-anchor 두 모드 forecast. 각 R={2,3,5,10}.
(c) Mock injection (LCDM mock 200) 의 false-detection rate 가 dSph 추가로
    *낮아지는가* 측정 — ATTACK B2 의 강제력 ≠ pool 확대 검증 핵심 지표.
(d) 부호-결정 임계 사전등록: σ₀_dSph 가 (i) cosmic regime 값 (≈1.0–1.15)
    근처 → V-shape 강화, (ii) cluster regime 값 (≈0.4–0.5) 근처 → V-shape
    위치 이동, (iii) galactic regime 값 (≈0.95–1.00) 근처 → 단조 모델 회복.
    세 분기를 GitHub release tag 로 사전등록 (별도 PR)."

---

## 2. 다음 단계 task list

| # | task | 즉시? | budget |
|---|------|------|--------|
| N1 | 5 dSph anchor archive 측정값 + ρ_env 매핑 (D_LG → log10 ρ_env) | YES | <1min |
| N2 | 환경-only anchor 모드 forecast (R-grid 4점) | YES | <1min |
| N3 | σ₀-anchor 모드 forecast (3 시나리오 × R-grid) | YES | <1min |
| N4 | Mock injection false-rate Δ (without dSph vs with dSph) | YES | ~30s |
| N5 | dSph 측정치 변환 prior (M_dyn → σ₀) 1-paragraph 정리 | NO (L425) | 0.5d |
| N6 | 부호-결정 임계 GitHub release tag pre-registration | NO (paper) | 1d |
| N7 | Walker 2009 + Gaia DR3 RVS profile 재분석 (실 측정) | NO (long-tail) | 1mo |

본 세션은 N1–N4 만 수행 → simulations/L424/run.py.

---

## 3. 회복 가능성 정직 판정

- N4 (mock false-rate) 가 dSph 추가로 *유의 감소* (예: 100% → ≤80%) 시
  ATTACK B2 의 자유도-우위 위험 일부 완화 — three-regime 강제력 약 회복.
- false-rate 가 *변화 없음* 또는 *증가* 시 dSph anchor 는 paper §6.1 row #5
  해결 *불가* 결정. row #5 ACK_REINFORCED 로 강화하고 P9 falsifier 등급
  격하 권고.
- 환경-only anchor 모드 (N2) 의 Δln Z 가 σ₀-anchor 모드 (N3) 의 Δln Z 보다
  *낮으면* 강화 효과의 상당 부분이 σ₀ 측정값-circular 임을 시사 (ATTACK B4).
  이 경우 변환 prior 명시 (N5) 가 paper 인용 조건.

→ 본 L424 run.py 결과 (results/L424/report.json + run_log.txt) 가 P9 anchor
강화 path 의 *2차 진단* (L405 forecast 후속). REVIEW.md 에서 4인팀이
결과 해석 자율 분담.
