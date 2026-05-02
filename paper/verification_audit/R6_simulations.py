#!/usr/bin/env python3
"""
R6 — 시뮬레이션 검증 (root /base.md §14.6 의 3개 시뮬 claim 이
paper/base.md framework 로 유효한가, 매우 냉철하게 검증).

paper/base.md framework
- 미시 4 축: Schwinger-Keldysh / Wetterich RG / Holographic / Z_2 SSB
- 5번째 축 후보: Causet meso (4/5 조건부). GFT 명시 없음.
- minimal SQT: w_a = 0
- V(n,t)-확장: w_0 ~ -0.95, w_a ~ -0.3 (gate OPEN, derivation 미확정)
- DESI DR2: w_0=-0.757±0.058, w_a=-0.83 (DESI+CMB+SN 결합)
- BBN/CMB consistency PASS (예측 아님)

root /base.md §14.6 (3 claim)
  25. DESI DR2 피팅: ξ_q>0 joint fit Δχ²=-4.83, r_d=149.8 Mpc 필요
  26. 3자 정합성: #25 의존
  27. GFT BEC 해밀토니안: 수학적 도출 ✅

검증 절차: 각 claim 에 대해
 (a) paper/base.md w(z) 예측이 ξ_q joint fit 과 정합한가
 (b) r_d=149.8 Mpc 이동이 paper/base.md 도 요구하는가 (BBN/CMB consistency 와 양립?)
 (c) GFT 해밀토니안이 paper/base.md 의 4 축 (또는 5번째 후보 Causet) 에 포함되는가
 (d) 분석적/수치적 비교
 (e) PASS / PARTIAL / NOT_INHERITED 판정
"""
import os
os.environ['OMP_NUM_THREADS'] = '1'
import numpy as np
import json

# =========================================================
# 0. paper/base.md framework 상수 (검증 대상)
# =========================================================
W0_MIN_SQT      = -1.0      # minimal SQT: cosmological constant 등가 → w=-1, w_a=0
WA_MIN_SQT      = 0.0
W0_VNT_EXT      = -0.95     # paper/base.md §5.4 V(n,t)-확장 (gate OPEN)
WA_VNT_EXT      = -0.30
W0_DESI         = -0.757
W0_DESI_ERR     = 0.058
WA_DESI         = -0.83
WA_DESI_ERR_LO  = 0.21
WA_DESI_ERR_HI  = 0.24

# root /base.md §14.6 / §10.5 시뮬 claim 결과
XI_Q_FIT        = +0.04
DCHI2_FIT       = -4.83     # Planck r_d 고정 vs 자유화
RD_FIT          = 149.8     # Mpc
RD_PLANCK       = 147.09    # Mpc (root /base.md 서술)
W0_FROM_XI_POS  = "w_0 > -1, w_a > 0"   # root §10.2 (선도차수 2체 결합)
W0_FROM_XI_NEG  = "w < -1 (phantom)"     # root §10.5 — SQMH 위반

# =========================================================
# Claim 25 — DESI DR2 ξ_q>0 joint fit (Δχ²=-4.83, r_d=149.8)
# =========================================================
# (1) w(z) 예측 정합성:
#     - root /base.md §10.2: ξ_q>0 → w_a > 0 (선도차수 2체 결합)
#     - paper/base.md §5.4: minimal SQT w_a=0; V(n,t)-확장 w_a ~ -0.3
#     → ξ_q>0 가 만드는 w_a>0 와 paper/base.md 의 두 모델 모두 정합 안 됨.
#       (minimal: w_a=0 ; V(n,t)-확장: w_a<0)
#     → root §10.5 ξ_q<0 (phantom) 만 w_a<0 을 만들지만 SQMH 물리 위반.

c25_w_a_sign_root_xi_pos = +1   # root §10.2: ξ_q>0 → w_a > 0
c25_w_a_paper_minimal    =  0
c25_w_a_paper_extended   = -1   # 부호 음수
c25_consistency_minimal  = (c25_w_a_sign_root_xi_pos == 0)        # False
c25_consistency_extended = (c25_w_a_sign_root_xi_pos < 0)         # False

# (2) r_d 이동 149.8 vs Planck 147.09:
#     paper/base.md §5/§6 BBN 및 재결합 무영향 (consistency PASS).
#     → 재결합 시기 sound horizon 이 LCDM 과 동일해야 함.
#     → r_d 자유화 = 재결합 물리 변경 → paper/base.md framework 가
#        '요구' 하지 않으며 오히려 BBN/CMB consistency 와 충돌 가능.
rd_shift_pct = abs(RD_FIT - RD_PLANCK) / RD_PLANCK * 100.0
c25_rd_required_by_paper = False   # paper/base.md 는 r_d 이동을 도출하지 않음

# (3) Δχ² = -4.83 (~2.2σ) 의 의미:
#     root /base.md 자체 인정: "ξ_q<0 fit 은 phantom" → 물리적이지 않음
#     ξ_q>0 fit 은 r_d 자유화 (이론 외부 nuisance) 를 통해서만 -4.83 달성.
#     paper/base.md framework 에서는 ξ_q 자체가 1차 자유 매개변수가 아님
#     (V(n,t)-확장 gate OPEN, derivation 미확정 — paper/base.md §5.4).
c25_xi_q_in_paper_framework = False   # paper/base.md 에 ξ_q 직접 도출 없음

c25_verdict = "NOT_INHERITED"
# 사유: (a) ξ_q>0 의 w_a>0 가 paper/base.md 양 모델과 부호 불일치
#       (b) r_d=149.8 Mpc 이동을 paper/base.md 가 요구 안 함
#       (c) ξ_q 자체가 paper/base.md framework 에서 직접 도출되지 않음
#       → root /base.md 의 fit 결과는 paper/base.md framework 로 상속 불가.

# =========================================================
# Claim 26 — 3자 정합성 (BBN/CMB/late-time DE)
# =========================================================
# root /base.md §14.6: "조건부 유효, #25 에 의존"
# paper/base.md framework:
#   - BBN PASS (consistency, prediction 아님 — paper §3 표 161)
#   - CMB 1차 이방성: r_d 이동 없는 LCDM 등가 (root §4 BBN/CMB 표 189-190)
#   - late-time DE: minimal w_a=0, V(n,t)-확장 w_a~-0.3
# #25 가 NOT_INHERITED → #26 의존 claim 도 자동 NOT_INHERITED.
# 또한 r_d 이동 149.8 Mpc 가 paper/base.md 의 "재결합 시기 GR 과 동일"
# (root §10 표 BBN/CMB) 와 텐션.
c26_depends_on_c25 = True
c26_paper_BBN_CMB_requires_r_d_shift = False
c26_verdict = "NOT_INHERITED"

# =========================================================
# Claim 27 — GFT BEC 해밀토니안
# =========================================================
# root /base.md §VI: GFT 작용 + BEC 응축 → ψ†ψ(a+a†) 해밀토니안 도출.
# paper/base.md 미시 4 축 (§2.4):
#   1. Schwinger-Keldysh open-system
#   2. Wetterich functional RG
#   3. Holographic dimensional bound
#   4. Z_2 spontaneous symmetry breaking
# GFT 는 4 축에 *부재*. 5번째 축 후보 (§2.5) 는 Causet meso 만.
# → GFT 도출이 수학적으로 옳더라도 paper/base.md framework 에는 *상속되지 않음*.
#   해밀토니안의 형태가 우연히 일치하더라도, paper/base.md 의 4 축 (또는
#   Causet meso 5번째 후보) 으로부터의 *재도출* 이 별도로 필요.
paper_pillars = [
    "Schwinger-Keldysh", "Wetterich RG",
    "Holographic foundation", "Z_2 SSB"
]
paper_pillar5_candidates = ["Causet meso"]      # GFT 미포함
gft_in_paper_pillars     = False
gft_in_paper_pillar5     = False
c27_math_derivation_correct = True              # root §VI 내부에서는 정합
c27_paper_inheritance       = (gft_in_paper_pillars or gft_in_paper_pillar5)
c27_verdict = "NOT_INHERITED"
# 사유: GFT 가 paper/base.md 의 4 축에 없고 5번째 후보도 Causet 만 명시.
# 수학적 도출이 옳다는 점은 인정하나, paper/base.md framework 로
# 자동 상속되지 않음. 별도 GFT-축 추가 또는 Causet 경로 재도출 필요.

# =========================================================
# 종합
# =========================================================
results = {
  "framework": "paper/base.md (4 미시 축 + minimal SQT/V(n,t)-extended + BBN/CMB consistency)",
  "source_claims": "root /base.md §14.6 (시뮬 검증 3개)",
  "claim_25_DESI_DR2_xi_q_fit": {
    "root_chi2_improvement": DCHI2_FIT,
    "root_xi_q": XI_Q_FIT,
    "root_r_d_Mpc": RD_FIT,
    "r_d_shift_vs_Planck_pct": rd_shift_pct,
    "paper_minimal_w_a": WA_MIN_SQT,
    "paper_extended_w_a": WA_VNT_EXT,
    "root_xi_q_pos_w_a_sign": "+",
    "consistency_w_a_minimal_extended": [
        c25_consistency_minimal, c25_consistency_extended
    ],
    "r_d_shift_required_by_paper": c25_rd_required_by_paper,
    "xi_q_in_paper_framework": c25_xi_q_in_paper_framework,
    "verdict": c25_verdict,
    "reason": (
      "ξ_q>0 가 만드는 w_a>0 (root §10.2) 는 paper/base.md "
      "minimal(w_a=0) 및 V(n,t)-확장(w_a~-0.3) 양쪽 모두와 부호 불일치. "
      "r_d=149.8 Mpc 이동(1.84%) 는 paper/base.md 의 BBN/CMB consistency "
      "와 양립하지 않으며 framework 가 도출하지 않음. "
      "ξ_q 자체가 paper/base.md V(n,t) gate OPEN 상태로 직접 정의되지 않음."
    )
  },
  "claim_26_three_way_consistency": {
    "depends_on_25": c26_depends_on_c25,
    "paper_requires_r_d_shift": c26_paper_BBN_CMB_requires_r_d_shift,
    "verdict": c26_verdict,
    "reason": (
      "#25 가 NOT_INHERITED 이므로 의존 claim 도 자동 NOT_INHERITED. "
      "또한 r_d 이동이 paper/base.md 의 '재결합 시기 GR 과 동일' 과 텐션."
    )
  },
  "claim_27_GFT_BEC_Hamiltonian": {
    "math_derivation_in_root": c27_math_derivation_correct,
    "paper_pillars": paper_pillars,
    "paper_pillar5_candidates": paper_pillar5_candidates,
    "gft_in_paper": c27_paper_inheritance,
    "verdict": c27_verdict,
    "reason": (
      "root §VI 의 GFT BEC → ψ†ψ(a+a†) 도출은 GFT framework 내부에서 정합. "
      "그러나 paper/base.md 의 4 미시 축 (Schwinger-Keldysh / Wetterich / "
      "Holographic / Z_2 SSB) 에 GFT 가 부재하며, 5번째 축 후보도 Causet "
      "meso 만 명시. 따라서 수학적 정확성과 별개로 paper/base.md framework "
      "로 상속되지 않음."
    )
  },
  "summary": {
    "PASS": 0,
    "PARTIAL": 0,
    "NOT_INHERITED": 3,
    "rate_inherited": 0.0
  }
}

# =========================================================
# 출력
# =========================================================
print("=" * 70)
print("R6 simulation-claim audit (paper/base.md framework)")
print("=" * 70)
for k, v in results["claim_25_DESI_DR2_xi_q_fit"].items():
    if k != "reason":
        print(f"  c25.{k}: {v}")
print(f"  c25.verdict: {results['claim_25_DESI_DR2_xi_q_fit']['verdict']}")
print()
for k, v in results["claim_26_three_way_consistency"].items():
    if k != "reason":
        print(f"  c26.{k}: {v}")
print()
for k, v in results["claim_27_GFT_BEC_Hamiltonian"].items():
    if k != "reason":
        print(f"  c27.{k}: {v}")
print()
print("Summary:", results["summary"])

out = "/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/paper/verification_audit/R6_simulations.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f"\nSaved -> {out}")
