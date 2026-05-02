# L447 NEXT_STEP — PASS_STRUCTURAL 격상 판정 후 행동

## 분기

### Case A. 8 인 합의 = PASS_STRUCTURAL
조건: dark-only μ_eff 채널 SQT 의 *모든* 자유 파라미터 정의역에서 ΔS_8 > 0
(부호 단조성), 그리고 amplitude-locking 이 β_d 와 독립이 아니라 sign-locked
인 경우.

- L448: paper/base.md 에 *양면 falsifiability* 절 신설.
  - 본문: "SQT (dark-only μ_eff branch) 는 LSST-Y1 / Euclid 가 ΔS_8 ≤ 0
    을 σ ≥ 3 으로 측정하면 falsify 됨. 현재 ΔS_8 = +1.14 % 는 SQT 부호 예측과
    일치 (방향 PASS), 단 크기 평가는 K15 정량 σ 분해능 향상 필요."
- L449: prediction registry (paper/PREDICTIONS.md) 에 P_S8_sign 등재.
  - 측정 기준: LSST-Y1 (2026 first cosmology), σ(ΔS_8) ≈ 0.005 예상.
  - falsifier: ΔS_8 ≤ −0.003 (3σ down) 발견 시 SQT dark-only branch 즉시 dead.

### Case B. 8 인 합의 = OBS-FAIL 유지
조건: SQT 자유 파라미터 정의역에 ΔS_8 ≤ 0 영역이 존재 (부호 비단조), 또는
amplitude-locking 이 β_d 와 진정 독립이라 ΔS_8 부호가 fine-tuning 으로 변경
가능한 경우.

- L448: paper/base.md K15 OBS-FAIL 유지. 격상 시도 *실패* 정직 기록.
- L449: 대신 *크기* (ΔS_8 = +1.14 %) 가 KiDS-1000 / DES-Y3 1σ 안인지의
  *수치 일치* 를 K15-soft (보조 지표) 로만 보고. PASS 미주장.

### Case C. 8 인 의견 분열 (4:4 등)
- 코드 / 식 검증 4 인팀이 부호 단조성 시뮬 (δ-ODE + dark-only μ_eff toy) 직접 실행.
  - 격자: β_d ∈ [0, 0.15], n_lock ∈ [0, 2] (amplitude-locking exponent).
  - 출력: ΔS_8 부호 맵.
- 단조 ⇒ Case A. 비단조 ⇒ Case B.

## 추가 검증 (모든 Case 공통)

1. **L1 Cassini 정합성 재확인**: dark-only embedding 이 PPN γ = 1 유지하는지
   (L2 C10k 표 인용). Solar-system 에서 baryon 비결합 명시.
2. **GW170817 정합성**: c_T = c (background-only μ ≠ G_T) 유지.
3. **부호 단조성 증명 시도**: 분석적 (δ-ODE 1 차 perturbation) 으로
   d(ΔS_8) / d(β_d²) > 0, d(ΔS_8) / d(amplitude-locking 강도) > 0 동시성.
   ⇒ 두 자유도가 *독립적으로* 부호를 같은 방향으로 미는지가 PASS_STRUCTURAL
   의 핵심 조건.

## 일정 / 자원
- Stage 1 (8 인): 1 세션. 토의만.
- Stage 2 (4 인): 1 세션 + δ-ODE toy 실행 (수십 초, multiprocessing 9 워커).
- Stage 3: 30 분 합의 + REVIEW.md 작성.

## 비목표 (스코프 제한)
- *크기* 격상 시도 (+1.14 % 가 K15 통과로 격상) 는 본 라벨 범위 외.
  L5 재발방지 "Background-only + μ_eff = 1 의 S_8 해결 불가" 그대로 유지.
- Q17 amplitude-locking 의 exact derivation (E(0)=1 정규화 이상) 은 별 라벨.
- Phase 6 (DR3 mock) 은 DR3 공개 후 별도 진행 (L6 재발방지 준수).
