# L317 ATTACK_DESIGN — Paper Section 7 (Outlook + Future) Finalization

## 0. 컨텍스트
- 누적 ~317 loop. Sec 1–6 finalized (L311–L316). Sec 7 = 마지막 본문 섹션 (Outlook + Future Work).
- 7 falsifier 타임라인 확정: P15 PIXIE μ-distortion (2025–2030), P17 DESI DR3 w_a (2025–2026), P21 LSST WL (2030+).
- Microscopic 4-pillar 통합 완료 (L300–L303). β-function 정량화는 future task 로 분리.
- DR3 (P17) 가 가장 가까운 falsifier — 12–18 개월 내 결정 가능.

## 1. Section 7 목표 (8인 합의)
"이론의 현재 위치를 정직하게 'falsifiable phenomenology' 로 못 박고, 단기 (DR3) → 중기 (PIXIE) → 장기 (LSST) decadal vision 을 7-falsifier 타임라인에 정렬해 reviewer 가 'kill 또는 promote' 의 시점을 한눈에 보게 한다. 동시에 이론 자체의 미완성 (full β-function, V(n,t) 완전유도) 을 같은 섹션에서 정직히 노출한다."

## 2. 8인 자율 분담 결과 (역할 사후 분류)
- A (positioning): "JCAP-grade falsifiable phenomenology" 재확인. PRD Letter 진입 조건 미달 명시 (L6 재발방지).
- B (DR3 immediate): P17 — DESI DR3 w_a 5σ separation, 2025–2026 데이터, kill-or-confirm 가장 가까운 시점.
- C (PIXIE mid-term): P15 — μ-distortion 예측 (V(n,t) ext), 2025–2030 미션 윈도. CMB-S4 보조 채널.
- D (LSST late-decade): P21 — WL Σ(z), σ_8 tension 영구 한계 (L242/L243) 와의 직접 충돌 시점.
- E (theory: β-function): RG FP (L301) → full β(g_*) 양적 유도가 미완. Future calculation queue.
- F (theory: V(n,t)): L207 T^μν_n / Λ origin 부분 유도. Complete derivation 은 microscopic→macroscopic bridge 의 다음 단계.
- G (companion paper): numerical methods (BAO ODE, growth ODE, MCMC pipeline) 분리 논문 — 본 논문 reproducibility 보강.
- H (code/data release): GitHub 레포 + 시뮬레이션 코드 + 13-pt DESI 공분산 사용법 + L317 시점 결과 freeze tag.

## 3. 단락 구조 (최종 8 sub-section)
- 7.1 Decadal vision — 이론 현 위치와 향후 5–10년 전략.
- 7.2 P17 DESI DR3 (immediate, 12–18 mo) — kill criterion + expected separability.
- 7.3 P15 PIXIE μ-distortion (mid-term, 2025–2030) — V(n,t) ext 예측.
- 7.4 P21 LSST WL (late-decade, 2030+) — σ_8 한계 직접 검증 시점.
- 7.5 7-falsifier timeline 종합표 — P15/P17/P21 + 보조 P9/P11/P19/P22 동기.
- 7.6 Theoretical future I: full β-function 정량화 (RG FP, L301 follow-up).
- 7.7 Theoretical future II: V(n,t) complete derivation (microscopic → macroscopic bridge).
- 7.8 Companion paper + code/data release — 재현성 commitment.

## 4. Top 3 (가중치 순)
- B (P17 DR3): 가장 가까운 falsifier. Section 7 의 머리 단락.
- A (positioning): JCAP 포지셔닝 가드. 한 섹션 안에서 "promotion claim" 새어나가는 것 방지.
- E+F (이론 미완): β-function + V(n,t) 미완성을 동일 섹션에서 정직 노출 — reviewer 의 "왜 PRD Letter 가 아닌가" 질문에 본 섹션이 답해야 함.

## 5. 정직성 가드 (위반 시 섹션 reject)
- "SQMH solves H0 / σ_8" 표현 절대 금지 (L242/L243 + L6 재발방지). σ_8 는 영구 한계.
- "DR3 will confirm" 류 단정 표현 금지. "kill-or-confirm window" / "5σ separable under L284 forecast assumptions" 만 허용.
- P17 forecast 인용 시 L284 가정 (CPL template, fiducial Om/h, DR3 covariance assumption) 명시 필수.
- β-function "유도 완료" 주장 금지 — "RG FP motivation + future quantitative β-function" 으로만.
- V(n,t) "완전 유도" 주장 금지 — Q17 부분 달성 (L207) + future complete derivation.
- "fixed-θ Δ ln Z" 단독 인용 금지 (L6 재발방지). marginalized 병기.
- Companion paper 를 "이미 작성 중" 으로 약속 금지 — "planned" 또는 "in preparation" 만.
- DR3 스크립트 (simulations/l6/dr3/run_dr3.sh) 는 DR3 공개 후만 실행 — Sec 7 본문에 "executed pre-release" 표기 절대 금지.

## 6. 산출물 체크리스트
- [ ] §7 LaTeX draft (8 sub-section).
- [ ] Table 7.1: 7-falsifier timeline (P9/P11/P15/P17/P19/P21/P22 × 미션 × 시기 × kill criterion).
- [ ] Table 7.2: P17 DR3 forecast (L284 인용) — separability vs DR2 baseline.
- [ ] Fig 7.1: timeline schematic (2026 → 2035).
- [ ] §7.6/7.7 outline-only, 수식 minimal — 본 논문 분량 폭주 방지.
- [ ] §7.8 GitHub URL + Zenodo DOI 확보 후 채움 (지금은 placeholder).

## 7. Open issue (다음 loop)
- §7.6 (β-function) 와 §7.7 (V(n,t)) 을 합쳐 단일 sub-section "Theoretical Future" 로 줄일지 — 4인 코드리뷰에서 본문 분량 측정 후 결정.
- DR3 forecast 그림을 §5 (Cosmology) 와 §7 (Outlook) 중 어디에 둘지 — §5 는 결과, §7 은 미래. L315 합의: §5 에 fiducial forecast, §7 에 timeline-summary 만.
- Companion paper 분리 vs 본 논문 Appendix 흡수 — 8인 재투표 필요 (L318).
