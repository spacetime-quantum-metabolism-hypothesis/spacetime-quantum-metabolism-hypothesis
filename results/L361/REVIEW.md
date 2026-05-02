# L361 — 4인 review (사전 설계 검토, 시뮬 실행 전)

대상: ATTACK_DESIGN.md + NEXT_STEP.md (5-dataset SQT mock injection-recovery 설계).
시뮬 실행 전 설계 단계 review. 실행 후 결과 review 는 별도 추가.

## 4인 자율 분담 (역할 사전 지정 없음)

### P (방법론 점검)
- Mock 생성 시 cross-dataset covariance 누락 위험: BAO-SN 사이 lensing/peculiar-velocity 연관은 무시 가능 (CobayaSampler 표준 가정 일치).
- SPARC-like rotation curves 는 cosmology mock 과 generative model 이 다름 — joint chi² 에 단순 합산 시 weight 왜곡. 별도 module 권고.

### N (코드 함정 점검)
- emcee `np.random` 전역 의존 → `run_mcmc` 내부 seed 강제 (CLAUDE.md 등재).
- numpy 2.x: `np.trapezoid` 직접 호출 (trapz import 금지).
- BAO D_H 단위: c[m/s] / (H0[s⁻¹]·E·Mpc) — 중간 km/s/Mpc 변환 금지.
- Compressed CMB: chi2_joint 의 'cmb' 키 직접 사용, Hu-Sugiyama 재계산 금지 (L6-G3 4.6e6 chi2 함정).
- emcee 비수렴 mock silent drop 금지 — 별도 카운트 명시.

### O (통계 정합성)
- AICc penalty: BB 추가 파라미터 수 명시. SQT injection 인데 universal 이 우위면 prior volume artefact 가능 — Bayes evidence 도 같이 계산 권고.
- Coverage 측정 시 √N=10 noise → ±10% 신뢰구간. PASS 경계 (68%) 에서는 N=100 이 아슬아슬, N=200 권고하나 wall-clock 2배.
- Branch P vs Branch F 비교는 paired (같은 mock seed) 로. unpaired 비교 금지.

### H (이론/해석 정합성)
- SQT truth 파라미터는 L33 Q93 의 BAO-only low-Om 함정 회피 — joint-driven Om≈0.3 사용 명시 (CLAUDE.md L33 룰).
- Anchor σ_0 *theory-prior* 는 dimensional ground (Planck 단위 에서 도출) 에서 fix, *data-fit* 처럼 보이는 정당화 금지.
- Recovery 실패 시 SQT 모델 부정 vs BB 메서드 부정 분리 — coverage 결함이면 메서드 결함, bias 면 모델 결함.

## 정직 결론 (사전 설계 단계)
- 설계 자체에 치명 결함 없음. 단 N=100 은 PASS 경계에서 통계 noise 위험 (O 지적).
- L272 의 100% false-detection 결과를 보완하는 정대칭 실험으로 적절.
- SPARC module 분리 + AICc/Bayes evidence 병기 + paired Branch P/F 비교 — 세 보강 후 실행 승인.

→ 등급 영향: 사전 단계는 영향 없음. 실행 결과에서 recovery < 50% 시 paper BB 섹션 강등 (-0.03 등급), recovery ≥ 68% 시 L272 처방 정당화 (+0.01 등급).

핵심 한 줄: 설계는 합격이나 N=100 통계 noise 와 SPARC 결합 처리가 실행 단계 최대 위험이다.
