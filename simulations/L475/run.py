"""
L475 toy — cluster decoherence-boundary qualitative check.

CLAUDE.md 준수:
- speculation only. paper 인용 금지.
- 수치 prefactor 사전 지정 없음 (8인 자율 도출).
- chi2 / dAICc / fitting 절대 사용 금지 (L33~L34 재발방지 규칙).
- 본 스크립트는 H475-B (transition window peak-and-recover) 의 *질적*
  z-shape 만 시각화. parameter 는 임의 placeholder.

목적:
  decoherence rate Γ_dec(z) / H(z) 가 cluster scale 근방에서 1 을 통과하는
  sigmoid-form weight w(z) 를 가정했을 때, BAO 잔차에 *단조하지 않은*
  peak-and-recover 패턴이 자연 발생할 수 있는지 시각적으로만 확인.

산출: results/L475/toy_qualitative.png (선택, matplotlib 있을 때만).
"""

from __future__ import annotations

import os

import numpy as np


def coherence_weight(z: np.ndarray, z_t: float, w_z: float) -> np.ndarray:
    """양자 coherence 잔여 weight. transition center z_t, width w_z. prefactor 미지정."""
    return 1.0 / (1.0 + np.exp((z - z_t) / w_z))


def transition_pulse(z: np.ndarray, z_t: float, w_z: float) -> np.ndarray:
    """transition window 자체가 만드는 z-localised pulse. peak-and-recover proxy."""
    x = (z - z_t) / w_z
    # Γ_dec/H 가 1 부근에서 활성화되는 영역만 비-제로 → 미분 형태 (sech^2)
    return 1.0 / np.cosh(x) ** 2


def main() -> None:
    z = np.linspace(0.05, 2.5, 400)

    # 임의 transition center 와 width — 8인이 추후 도출. 본 값은 placeholder.
    centers = [0.4, 0.7, 1.0]
    widths = [0.1, 0.2, 0.4]

    out_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "results",
        "L475",
    )
    os.makedirs(out_dir, exist_ok=True)

    # 텍스트 표만 저장 — 수치 fitting 아님.
    rows = ["# z, w_coh(z_t=0.7,w_z=0.2), pulse(z_t=0.7,w_z=0.2)"]
    w_demo = coherence_weight(z, 0.7, 0.2)
    p_demo = transition_pulse(z, 0.7, 0.2)
    for zz, ww, pp in zip(z[::20], w_demo[::20], p_demo[::20]):
        rows.append(f"{zz:.3f}\t{ww:.4f}\t{pp:.4f}")
    with open(os.path.join(out_dir, "toy_shape.tsv"), "w", encoding="utf-8") as f:
        f.write("\n".join(rows))

    # plot (matplotlib 있을 때만 — 없으면 silently skip)
    try:
        import matplotlib

        matplotlib.use("Agg")  # corner / pyplot import 전 호출 (CLAUDE.md 규칙).
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        for zt, wz in zip(centers, widths):
            axes[0].plot(z, coherence_weight(z, zt, wz), label=f"z_t={zt}, w={wz}")
            axes[1].plot(z, transition_pulse(z, zt, wz), label=f"z_t={zt}, w={wz}")
        axes[0].set_xlabel("z")
        axes[0].set_ylabel("coherence weight w_coh(z)  [arbitrary]")
        axes[0].set_title("H475-B sigmoid dropout")
        axes[0].legend(fontsize=8)
        axes[1].set_xlabel("z")
        axes[1].set_ylabel("transition pulse  [arbitrary]")
        axes[1].set_title("peak-and-recover (sech^2)")
        axes[1].legend(fontsize=8)
        fig.suptitle(
            "L475 toy - cluster decoherence boundary (qualitative only, prefactor unspecified)"
        )
        fig.tight_layout()
        fig.savefig(os.path.join(out_dir, "toy_qualitative.png"), dpi=120)
        plt.close(fig)
        print("L475 toy plot saved:", os.path.join(out_dir, "toy_qualitative.png"))
    except Exception as exc:  # noqa: BLE001
        print("matplotlib unavailable, skipping plot:", exc)

    print("L475 toy done. Speculation only — no chi2 / no fitting.")


if __name__ == "__main__":
    main()
