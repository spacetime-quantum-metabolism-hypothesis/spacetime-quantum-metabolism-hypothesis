# L359 REVIEW — Convergence Threshold Spec

## 핵심 결정
Rhat ≤ 1.01, ESS-bulk/tail ≥ 400, N/τ ≥ 50, PPC p ∈ [0.05, 0.95], MCSE/std < 0.05 의 5중 PASS 게이트를 SQMH MCMC 결과의 인용 자격으로 채택.

## 근거
- Vehtari et al. 2021 (Rank-normalized split-Rhat 1.01)
- Stan/ArviZ 권고 ESS ≥ 400
- emcee 매뉴얼 권고 N ≥ 50τ
- PRD/JCAP 게재 관행: PPC tail 0.05 양측

## 위험 / 주의
1. L4 C28 K13 fail (Rhat=1.3653) 은 본 spec FAIL 확정 — 해당 chain의 Δχ²=+5.272 인용 금지 (CLAUDE.md L6 규칙과 일치).
2. emcee stretch move 의 `np.random` 전역 의존성은 `np.random.seed(42)` 명시로만 재현 가능 (CLAUDE.md 기재).
3. PPC 계산 시 chi^2 재계산은 100ms/call × 200 draw = 20s/chain 으로 수용 가능.
4. Rank-normalized Rhat은 raw Rhat과 다름 — `arviz.rhat(method="rank")` 명시 필수.
5. ESS는 파라미터별 산정. 최악 파라미터(보통 nuisance)가 게이트 결정.

## 8인 합의 사항 (CLAUDE.md Rule-A 적용 시)
이론 클레임 없음 — 본 산출물은 진단 절차 spec이므로 Rule-B 4인 코드 리뷰 대상. 도구 구현 (`mcmc_diag.py`) 작성 시 4인 자율 분담 검토.

## 과적합 방지 (CLAUDE.md)
PPC 임계값을 데이터에 맞춰 사후 조정 금지. 0.05 양측은 사전 고정.

## 한국어 한 줄
정직: 본 spec은 엄격하므로 기존 chain 상당수가 FAIL 판정될 가능성이 있고, 재실행 없이는 논문 인용 자격이 없는 결과가 다수 발생할 수 있다.
