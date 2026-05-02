"""L464 free speculation: tau_q vs cluster crossing time anti-resonance toy.

목적
----
- cluster 특성 timescale (~Gyr) 과 Planck time tau_q 사이의 비를 계산
- forced damped oscillator 토이로 resonance / anti-resonance 패턴 스캔
- stochastic averaging 으로 빠른 진동 평균화 시 "dip" (anti-resonance) 가능성 점검

주의: 이는 자유 추측 (speculation) 토이임. 실제 BAO 피팅과 무관하며 직관 탐색용.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np

# 워커당 스레드 고정 (CLAUDE.md 규칙)
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

OUT = Path(__file__).resolve().parents[2] / "results" / "L464"
OUT.mkdir(parents=True, exist_ok=True)


# -----------------------------------------------------------------------------
# 1. 시간 척도 비
# -----------------------------------------------------------------------------
# Planck time
tau_q = 5.391247e-44  # s
# 1 Gyr in seconds
gyr = 3.1557e16  # s
# cluster crossing time ~ R/sigma; R~1 Mpc, sigma~1000 km/s -> ~1 Gyr
t_cluster_cross = 1.0 * gyr  # s (대표값)
# cluster dynamical time (M~1e15 Msun, R~Mpc) ~ 2-3 Gyr
t_cluster_dyn = 2.5 * gyr

ratios = {
    "tau_q [s]": tau_q,
    "t_cluster_cross [s]": t_cluster_cross,
    "t_cluster_dyn [s]": t_cluster_dyn,
    "ratio_cross/tau_q": t_cluster_cross / tau_q,
    "ratio_dyn/tau_q": t_cluster_dyn / tau_q,
    "log10(ratio_cross/tau_q)": np.log10(t_cluster_cross / tau_q),
    "log10(ratio_dyn/tau_q)": np.log10(t_cluster_dyn / tau_q),
}

# Hubble time 비교
hubble_time = 4.55e17  # s
ratios["t_H/tau_q"] = hubble_time / tau_q
ratios["log10(t_H/tau_q)"] = np.log10(hubble_time / tau_q)

# log-period gap from cluster to Planck
ratios["log10(t_cluster/t_H)"] = np.log10(t_cluster_dyn / hubble_time)


# -----------------------------------------------------------------------------
# 2. Forced damped oscillator: amplitude vs forcing frequency
# -----------------------------------------------------------------------------
# 시스템: 우주 거시 모드(자연주파수 omega_0 ~ 1/t_H) 가 미시 driver(omega ~ 1/tau_q) 에 의해 강제됨.
# 표준 응답:  A(omega) = F0 / sqrt((omega_0^2 - omega^2)^2 + (gamma*omega)^2)
# anti-resonance 는 결합된 이중-모드 (예: 두 oscillator 가 서로 반대 위상으로 강제) 시 발생.
# 여기서는 두 모드 간섭으로 응답이 dip 을 보이는 구조를 토이로 보여줌.

def coupled_response(omega, omega1, omega2, g1, g2, gamma=0.05, mix=1.0):
    """두 oscillator 합성 응답. mix<0 이면 destructive interference."""
    chi1 = g1 / (omega1**2 - omega**2 + 1j * gamma * omega)
    chi2 = g2 / (omega2**2 - omega**2 + 1j * gamma * omega)
    return np.abs(chi1 + mix * chi2)


# 정규화: omega 단위 = 1/Gyr
omega_grid = np.geomspace(1e-3, 1e3, 4000)  # 1/Gyr 단위
omega_H = 1.0 / 14.0      # ~ Hubble freq in 1/Gyr
omega_cl = 1.0 / 2.5      # cluster dyn freq ~ 0.4/Gyr
# Planck mode 는 토이 안에 직접 못 넣음 (스케일 차 ~10^60). 대신
# stochastic averaging argument: 빠른 driver 의 평균 효과를 effective coupling 으로.

resp_constructive = coupled_response(omega_grid, omega_H, omega_cl, 1.0, 1.0, gamma=0.05, mix=+1.0)
resp_destructive = coupled_response(omega_grid, omega_H, omega_cl, 1.0, 1.0, gamma=0.05, mix=-1.0)

# dip 위치: 두 자연주파수 사이 내부 dip 만 본다 (고주파 tail 자명한 감쇠 제외)
band = (omega_grid > min(omega_H, omega_cl) * 1.05) & (omega_grid < max(omega_H, omega_cl) * 0.95)
sub_grid = omega_grid[band]
sub_dest = resp_destructive[band]
sub_cons = resp_constructive[band]
i_min = int(np.argmin(sub_dest))
omega_dip = float(sub_grid[i_min])
amp_dip = float(sub_dest[i_min])
amp_constructive_at_dip = float(sub_cons[i_min])
suppression_ratio = amp_dip / amp_constructive_at_dip


# -----------------------------------------------------------------------------
# 3. Stochastic averaging argument
# -----------------------------------------------------------------------------
# 빠른 micro-driver 가 white noise 처럼 보일 때, slow mode 응답은
# <A^2> ~ S(omega_slow) / (gamma * omega_slow^2)  (Lorentzian-like averaging)
# 만약 micro spectrum 이 cluster 스케일에서 spectral hole 을 가지면 dip 발생 가능.
# 토이로 spectrum S(omega) 에 인공적 dip 을 넣어 슬로우 응답을 계산.

def micro_spectrum(omega, omega_dip_freq, dip_width, dip_depth):
    """1 - dip_depth * exp(-(log(omega/omega_dip)/dip_width)^2)."""
    base = 1.0 / (1.0 + (omega / 10.0) ** 2)  # red-tilt
    hole = 1.0 - dip_depth * np.exp(-((np.log(omega / omega_dip_freq) / dip_width) ** 2))
    return base * hole


omega_test = np.geomspace(1e-3, 1e2, 2000)
S_no_hole = micro_spectrum(omega_test, omega_cl, 0.5, 0.0)
S_with_hole = micro_spectrum(omega_test, omega_cl, 0.5, 0.7)

# slow-mode response after stochastic averaging
gamma_slow = 0.05
A2_no_hole = S_no_hole / (gamma_slow * omega_test ** 2 + 1e-12)
A2_with_hole = S_with_hole / (gamma_slow * omega_test ** 2 + 1e-12)


# -----------------------------------------------------------------------------
# 4. 저장
# -----------------------------------------------------------------------------
np.savez(
    OUT / "L464_oscillator.npz",
    omega_grid=omega_grid,
    resp_constructive=resp_constructive,
    resp_destructive=resp_destructive,
    omega_test=omega_test,
    S_no_hole=S_no_hole,
    S_with_hole=S_with_hole,
    A2_no_hole=A2_no_hole,
    A2_with_hole=A2_with_hole,
)

summary = {
    "ratios": {k: float(v) for k, v in ratios.items()},
    "oscillator": {
        "omega_H_inv_Gyr": omega_H,
        "omega_cluster_inv_Gyr": omega_cl,
        "omega_dip_inv_Gyr": omega_dip,
        "amp_destructive_at_dip": amp_dip,
        "amp_constructive_at_dip": amp_constructive_at_dip,
        "suppression_ratio": suppression_ratio,
    },
    "stochastic_averaging": {
        "max_A2_no_hole": float(A2_no_hole.max()),
        "max_A2_with_hole": float(A2_with_hole.max()),
        "min_A2_with_hole_in_cluster_band": float(
            A2_with_hole[(omega_test > 0.2) & (omega_test < 0.8)].min()
        ),
        "relative_suppression_in_cluster_band": float(
            A2_with_hole[(omega_test > 0.2) & (omega_test < 0.8)].min()
            / A2_no_hole[(omega_test > 0.2) & (omega_test < 0.8)].min()
        ),
    },
    "interpretation": (
        "Toy 결과: 두 mode destructive interference 시 cluster 대역에서 응답이 "
        f"{suppression_ratio:.3f} 배로 억제됨. 마이크로 스펙트럼에 cluster band hole 을 "
        "강제하면 stochastic averaging 으로도 dip 재현 가능. 단 이는 phenomenological "
        "토이이며 SQMH 동역학 도출이 아님."
    ),
}

with open(OUT / "L464_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("[L464] tau_q =", tau_q, "s")
print("[L464] t_cluster_dyn / tau_q =", t_cluster_dyn / tau_q,
      "(log10 =", np.log10(t_cluster_dyn / tau_q), ")")
print("[L464] omega_dip =", omega_dip, "1/Gyr; suppression =", suppression_ratio)
print("[L464] stochastic dip relative depth =",
      summary["stochastic_averaging"]["relative_suppression_in_cluster_band"])
print("[L464] saved:", OUT)
