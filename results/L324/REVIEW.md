# L324 — REVIEW (8인 자율 분담, Rule-A)

**대상**: ATTACK_DESIGN.md 의 8 공격 + KPI K1-K9
**규칙**: Rule-A 8인. 역할 사전 지정 없음. 자유 접근.

---

## P1 — Selection bias 형식론
A1 의 strata 분류는 (incl, dist-method, gas-frac) 3축. 직교성 부족 (gas-frac 와 dist-method
는 H I 거리법 통해 상관). 직교 PCA 후 strata 권장. K4 임계 0.5σ 는 strata 수
n_s 와 함께 Bonferroni 보정 필요: 3 strata × 2 컷 = 6 검정 → effective 2.4σ.

## P2 — DESI tracer 분리의 정보량
A2 tracer-block 분리는 정보량 손실 (13pt → 8 group, 일부 그룹 1pt). 통계
power 부족으로 K5 가 trivially pass 할 위험. 권고: tracer-pair (BGS+LRG)
vs (ELG+QSO+Lyα) 2-block 으로 합쳐서 power 보존.

## P3 — CMB Z_CUT 의 의미
A3 의 Z_CUT 변동은 CLAUDE.md "phase 2 CMB 적분 z~1100 까지" 룰과 연관.
Z_CUT={2,3,5,10} 중 5,10 은 LCDM bridge 비대칭 줄여줌. 다만 Z_CUT=10 이상
가면 SQT 효과 영역 일부 bridge 에 편입 → 자기제거 위험. Z_CUT=5 까지만 안전.

## P4 — IOI metric 의 funnel 함정
A4 IOI 는 nearly-Gaussian posterior 가정. BB σ_0 posterior 가 SPARC-only 에서
non-Gaussian (anchor saturation tail) 이라 raw IOI 과대평가 가능.
권고: Hellinger distance 또는 posterior-overlap (Marshall et al 2006 R)
보조지표 병용.

## P5 — Q_DMAP suspiciousness 둘 다 필요한가
A5 Q_DMAP 와 A5 suspiciousness S 는 정보 중복 (둘 다 Bayesian tension).
K7 만 main, K8 은 supplement 로 충분. 추가 비용 0.

## P6 — leave-SPARC-out 의 결정성
A7 K9 가 사실상 "BB 가 SPARC-anchor 이상 무엇이냐" 의 직접 시험. 본 loop 의
**핵심**. K9 fail 이면 다른 K1-K8 결과와 무관하게 영구 limitation 추가.
ATTACK_DESIGN 4절의 사전 예측 (K9 fail ~60%) 정직, 동의.

## P7 — distance-ladder coupling 의 분리 가능성
A8 SPARC 거리 ±5% 섭동은 데이터 재로딩 부담. 본 loop 미실행, 별도 L325+ 권고.
ATTACK_DESIGN 우선순위 1-7 만 본 loop, 8 은 deferred.

## P8 — 영구 limitation 추가의 acceptance 영향
ATTACK_DESIGN 4절 -1~-2% acceptance 추정은 낙관 가능성. JCAP reviewer 의
"global fit claim" 약화 효과는 더 클 수 있음 (-3~-5%). 다만 235-loop
누적 trust 가 buffering. 최종 추정: -2% (93~97% → 91~95%) 안전한
honest 시나리오.

---

## 합의 사항

1. **본 loop 실행 범위**: K1-K7 + K9. K8 supplement, A6/A8 deferred.
2. **strata Bonferroni**: K4 임계 2.4σ effective.
3. **DESI tracer-block**: 2-group (low-z BGS+LRG, high-z ELG+QSO+Lyα) 로 합침.
4. **CMB Z_CUT 범위**: {2, 3, 5} 만. 10 제외.
5. **IOI 보조**: Hellinger 병용.
6. **K9 fail 시 영구 limitation 추가** Sec 6.5 — 사전 합의.
7. **Acceptance 영향 추정 -2%** 보수적.
8. **본 loop 는 설계+검토 단계**. 실측 시뮬레이션은 NEXT_STEP 의 분리 세션.

## 미해결

- A6 selection-corrected reweighting 은 V_eff 모델링 부담 큼. L325 별도 loop
  로 분리. 본 L324 에서 다루면 over-scope.
- A8 distance-ladder ±5% 도 동일.

---

## 위반 점검 (CLAUDE.md 최우선 원칙)

- ATTACK_DESIGN 에 수식 없음 (KPI 임계만 숫자, 이는 통계 임계로 이론 형태 힌트 아님). PASS
- 팀 역할 사전 지정 없음. PASS
- 시뮬레이션 실행 시 multiprocessing.spawn + 워커 1-thread 강제 룰 — NEXT_STEP 에 명시.
- DESI 13pt + cov 사용, D_V 만 금지 — NEXT_STEP 에 명시.

위반 없음. 본 loop 진행 정당.
