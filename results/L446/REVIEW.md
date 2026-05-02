# L446 REVIEW — paper/GLOSSARY.md + paper/NOTATION.md 신설

- **Date / 일자**: 2026-05-01
- **Scope / 범위**: paper/GLOSSARY.md, paper/NOTATION.md 두 문서 신설.
  results/ 또는 simulations/ 의 코드는 변경하지 않았다.
- **Independence / 독립성**: L446은 L445 이전 결과(특히 L33, L46, L100, L5,
  L6 ratio·세 영역·KILL 라벨링)를 *참조*만 했고, 어떤 수치 결과나 수식도
  새로 도출하지 않았다. 두 문서는 메타 정의 통일을 위한 정리 작업이다.

## 산출물

1. `paper/GLOSSARY.md` — 4개 섹션 (이론 용어, 상태/판정 라벨, 방법론,
   작업 흐름 태그). 영문/한국어 병기. SQT, three-regime (구 Branch B),
   postdiction, prediction(a priori), OBS-FAIL, FRAMEWORK-FAIL,
   CONSISTENCY_CHECK, PASS_IDENTITY, KILL, PROVISIONAL, joint analysis,
   AICc penalty, Occam-corrected Δ ln Z, dark-only embedding, disformal
   coupling, compressed CMB, Lxx 마일스톤, Rule-A/Rule-B, negative-result
   registry 포함.
2. `paper/NOTATION.md` — 5개 섹션 (기본 SQMH 기호, 유효·현상학 기호,
   배경량, 금지/폐기 기호, 상호 참조). σ₀, n_∞, ε, τ_q, Γ_0, ρ_q, μ_eff,
   β_eff, Λ_UV, ξ, ξ_q, E(z), ω_X, r, amp 모두 영문/한국어 정의 + SI 단위
   포함. CLAUDE.md 의 SI 규약(σ = 4πG·t_P, n₀μ = ρ_Planck/(4π) ≈
   4.1×10⁹⁵ kg m⁻³)과 일관.

## 주요 정합성 결정 (CLAUDE.md 근거)

- **σ vs σ₀**: SI에서는 σ₀ = 4πG·t_P 만 사용. σ = 4πG 는 플랑크 단위 전용으로
  명시. (CLAUDE.md `재발방지` 라인 참조)
- **Branch B 폐기**: L100 이후 three-regime 구조로 대체. NOTATION 의 `금지·
  폐기 기호` 표에 명시.
- **ξ_q 부호 규약**: ξ_q ≥ 0 만 SQMH-consistent 로 표기, ξ_q < 0 phantom
  branch 는 분리 보고 의무 명시.
- **μ_eff ≈ 1**: S_8 tension 해결 불가 점을 NOTATION 정의에 직접 경고로
  포함 (L6 G3 학습 반영).

## 정직 한 줄

GLOSSARY/NOTATION 두 문서는 *기존* 합의된 용어·기호를 정리한 메타 문서이며,
새로운 물리적 주장이나 수치는 한 줄도 포함하지 않았다.
