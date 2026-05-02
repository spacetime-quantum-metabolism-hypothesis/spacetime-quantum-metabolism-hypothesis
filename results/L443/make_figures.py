"""L443: Generate F0-F9 PNGs for paper/figures/.

F0 axiom-derivation dependency graph (matplotlib DAG-like layout)
F5 rho_q evolution (uses results/L207/report.json absorption_per_hubble)
F6 GMM SPARC log_sigma_0 (synthetic 2-component placeholder, marked as schematic)
F7 mock injection vs real fit dAICc histogram (schematic)
F9 facility forecast Gantt (manual timeline)
F1, F2, F3, F4, F8 placeholders.
"""
import json, os, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

OUT = "/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/paper/figures"
os.makedirs(OUT, exist_ok=True)


# ---------- F0: axiom-derivation dependency graph ----------
def f0_axiom_graph():
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")

    axioms = [
        ("L0\nspacetime quanta", 1.0, 6.0),
        ("L1\nmetabolic flux Q", 1.0, 5.0),
        ("L2\ncoherence length", 1.0, 4.0),
        ("L3\nabsorption rate", 1.0, 3.0),
        ("L4\nlocal vacuum eq.", 1.0, 2.0),
        ("L5\nbackground emerg.", 1.0, 1.0),
    ]
    derived = [
        ("D1: Newton g(r) = G M/r^2", 6.0, 6.0),
        ("D2: a0 = c H0 / (2 pi)", 6.0, 5.0),
        ("D3: rho_q ~ rho_Lambda(Pl)", 6.0, 4.0),
        ("D4: w(z) ~ -1 + delta(z)", 6.0, 3.0),
        ("D5: sigma0(env) 3-regime", 6.0, 2.0),
    ]

    for name, x, y in axioms:
        ax.add_patch(FancyBboxPatch((x-0.55, y-0.3), 1.6, 0.6,
                                    boxstyle="round,pad=0.05",
                                    fc="#cfe7ff", ec="#1f4e79", lw=1.2))
        ax.text(x+0.25, y, name, ha="center", va="center", fontsize=8.5)

    for name, x, y in derived:
        ax.add_patch(FancyBboxPatch((x-0.4, y-0.3), 3.4, 0.6,
                                    boxstyle="round,pad=0.05",
                                    fc="#ffe1c4", ec="#a0522d", lw=1.2))
        ax.text(x+1.3, y, name, ha="center", va="center", fontsize=9)

    edges = [
        (0, 0), (1, 0),                # L0,L1 -> D1
        (1, 1), (2, 1),                # L1,L2 -> D2
        (1, 2), (3, 2),                # L1,L3 -> D3
        (3, 3), (4, 3), (5, 3),        # L3,L4,L5 -> D4
        (1, 4), (2, 4), (3, 4),        # L1,L2,L3 -> D5
    ]
    for ai, di in edges:
        ax_ = axioms[ai]; dx_ = derived[di]
        arr = FancyArrowPatch((ax_[1]+1.1, ax_[2]),
                              (dx_[1]-0.45, dx_[2]),
                              arrowstyle="->", mutation_scale=10,
                              color="#555", lw=0.8, alpha=0.7)
        ax.add_patch(arr)

    ax.text(1.0, 6.7, "Axioms (L0-L5)", ha="center",
            fontsize=11, fontweight="bold", color="#1f4e79")
    ax.text(7.3, 6.7, "Derived predictions", ha="center",
            fontsize=11, fontweight="bold", color="#a0522d")
    ax.set_title("F0  SQMH axiom -> derivation dependency graph", fontsize=12)
    fig.tight_layout()
    fig.savefig(f"{OUT}/F0_axiom_graph.png", dpi=160)
    plt.close(fig)


# ---------- F5: rho_q evolution from L207 report.json ----------
def f5_rho_q():
    path = "/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L207/report.json"
    rep = json.load(open(path))
    rho0 = rep["rho_q_0"]
    abs_h = rep["absorption_per_hubble"]   # dimensionless ~0.104
    z = np.linspace(0, 5, 400)
    a = 1.0 / (1.0 + z)
    # Bianchi-style toy: drho/dt = -3H(rho_q + p_q) - sigma rho_q
    # Use ratio rho_q(z)/rho_q(0) = a^{-3 abs_h} as visual proxy
    ratio = a ** (-3.0 * abs_h)
    rho = rho0 * ratio

    fig, axs = plt.subplots(1, 2, figsize=(11, 4.2))
    axs[0].plot(z, rho, color="#1f4e79", lw=1.6)
    axs[0].axhline(rho0, color="grey", ls="--", lw=0.8,
                   label=r"$\rho_q(z=0)=\rho_\Lambda^{\rm Pl}$")
    axs[0].set_xlabel("redshift z"); axs[0].set_ylabel(r"$\rho_q(z)$  [kg m$^{-3}$]")
    axs[0].set_yscale("log"); axs[0].legend(fontsize=8)
    axs[0].set_title("rho_q(z) (Bianchi toy)")

    axs[1].plot(z, ratio, color="#a0522d", lw=1.6)
    axs[1].axhline(1.0, color="grey", ls=":", lw=0.8)
    axs[1].set_xlabel("redshift z"); axs[1].set_ylabel(r"$\rho_q(z)/\rho_q(0)$")
    axs[1].set_title(f"absorption per Hubble = {abs_h:.3f}")

    fig.suptitle("F5  rho_q evolution (L207 report.json input)", fontsize=12)
    fig.tight_layout()
    fig.savefig(f"{OUT}/F5_rho_q_evolution.png", dpi=160)
    plt.close(fig)


# ---------- F6: GMM SPARC log_sigma_0 (schematic 2-component) ----------
def f6_gmm():
    rng = np.random.default_rng(42)
    # Schematic: simulated 2-component mixture intended to mirror SPARC
    # log_sigma_0 distribution. Real fit must be regenerated from SPARC data.
    g1 = rng.normal(loc=2.0, scale=0.18, size=140)
    g2 = rng.normal(loc=2.55, scale=0.14, size=80)
    data = np.concatenate([g1, g2])

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.hist(data, bins=28, density=True, color="#aaa", edgecolor="white",
            alpha=0.85, label="SPARC (schematic)")
    x = np.linspace(1.4, 3.1, 400)

    def gauss(x, mu, s, w):
        return w / (s * math.sqrt(2*math.pi)) * np.exp(-0.5*((x-mu)/s)**2)

    w1 = len(g1)/len(data); w2 = len(g2)/len(data)
    c1 = gauss(x, 2.0, 0.18, w1)
    c2 = gauss(x, 2.55, 0.14, w2)
    ax.plot(x, c1, color="#1f77b4", lw=1.5, label="component 1")
    ax.plot(x, c2, color="#d62728", lw=1.5, label="component 2")
    ax.plot(x, c1+c2, color="black", lw=1.2, ls="--", label="total")
    ax.set_xlabel(r"$\log_{10}\sigma_0$  [km/s]")
    ax.set_ylabel("density")
    ax.set_title("F6  SPARC log_sigma_0 GMM 2-component (schematic)")
    ax.legend(fontsize=8)
    ax.text(0.02, 0.97,
            "schematic; replace with real SPARC GMM fit",
            transform=ax.transAxes, fontsize=7, color="grey", va="top")
    fig.tight_layout()
    fig.savefig(f"{OUT}/F6_gmm_sparc.png", dpi=160)
    plt.close(fig)


# ---------- F7: mock injection dAICc histogram ----------
def f7_mock():
    rng = np.random.default_rng(7)
    null = rng.normal(loc=0.0, scale=1.2, size=2000)        # null mocks
    inj  = rng.normal(loc=-3.5, scale=1.6, size=2000)       # injected signal
    real = -2.9                                              # real fit dAICc

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    bins = np.linspace(-10, 6, 50)
    ax.hist(null, bins=bins, density=True, color="#888",
            alpha=0.55, label="null mocks")
    ax.hist(inj, bins=bins, density=True, color="#1f77b4",
            alpha=0.55, label="injected signal mocks")
    ax.axvline(real, color="#d62728", lw=2.0,
               label=f"real fit dAICc = {real:.2f}")
    ax.set_xlabel(r"$\Delta {\rm AICc}$  (SQMH - LCDM)")
    ax.set_ylabel("density")
    ax.set_title("F7  Mock injection vs real fit (schematic)")
    ax.legend(fontsize=8)
    ax.text(0.02, 0.97,
            "schematic; replace with real mock pipeline output",
            transform=ax.transAxes, fontsize=7, color="grey", va="top")
    fig.tight_layout()
    fig.savefig(f"{OUT}/F7_mock_injection.png", dpi=160)
    plt.close(fig)


# ---------- F9: facility forecast Gantt ----------
def f9_gantt():
    facilities = [
        ("DESI DR3",          2026.5, 2027.0, "#1f77b4"),
        ("DESI DR4 final",    2027.0, 2028.5, "#1f77b4"),
        ("Euclid DR1",        2026.0, 2027.5, "#2ca02c"),
        ("Euclid DR3 final",  2028.0, 2030.5, "#2ca02c"),
        ("Rubin LSST Y1",     2026.5, 2027.5, "#ff7f0e"),
        ("Rubin LSST Y10",    2028.0, 2034.0, "#ff7f0e"),
        ("CMB-S4 first light", 2030.0, 2031.5, "#9467bd"),
        ("LiteBIRD launch",    2032.0, 2034.0, "#9467bd"),
        ("SKA1 cosmology",     2029.0, 2032.0, "#d62728"),
    ]
    fig, ax = plt.subplots(figsize=(10, 5))
    for i, (name, t0, t1, col) in enumerate(facilities):
        ax.add_patch(Rectangle((t0, i-0.35), t1-t0, 0.7,
                                fc=col, ec="black", lw=0.6, alpha=0.85))
        ax.text(t1+0.05, i, name, va="center", fontsize=8.5)
    ax.axvline(2026.33, color="grey", ls="--", lw=0.8)
    ax.text(2026.33, len(facilities)-0.2, " today (2026-05)",
            color="grey", fontsize=7.5, va="top")
    ax.set_yticks([]); ax.set_xlim(2025.5, 2034.5)
    ax.set_ylim(-0.8, len(facilities)-0.2)
    ax.set_xlabel("year")
    ax.set_title("F9  SQMH falsifier facility forecast (Gantt)")
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(f"{OUT}/F9_facility_gantt.png", dpi=160)
    plt.close(fig)


# ---------- placeholders F1, F2, F3, F4, F8 ----------
def placeholder(name, title, note):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.axis("off")
    ax.text(0.5, 0.65, name, ha="center", va="center",
            fontsize=28, fontweight="bold", color="#444")
    ax.text(0.5, 0.45, title, ha="center", va="center", fontsize=11)
    ax.text(0.5, 0.22, note, ha="center", va="center",
            fontsize=8.5, color="grey", wrap=True)
    ax.add_patch(Rectangle((0.02, 0.02), 0.96, 0.96,
                           fill=False, ec="#bbb", lw=1.2,
                           transform=ax.transAxes))
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}_placeholder.png", dpi=160)
    plt.close(fig)


def main():
    f0_axiom_graph()
    f5_rho_q()
    f6_gmm()
    f7_mock()
    f9_gantt()

    placeholder("F1", "sigma_0(env) 3-regime + non-monotonic dip",
                "spec: log-scale, color-coded; aggregator pending")
    placeholder("F2", "SPARC fit examples (3 galaxies)",
                "spec: 3-panel + residual; standardisation pending")
    placeholder("F3", "a0 = c H0 / (2 pi) derivation diagram",
                "spec: vector graphics, disc projection; manual draw")
    placeholder("F4", "Cluster mass profile (Bullet)",
                "spec: X-ray + stellar + lensing overlay; standardisation pending")
    placeholder("F8", "IC comparison (AIC/BIC/DIC/WAIC)",
                "spec: grouped bar; aggregator pending")

    print("F0-F9 written to", OUT)


if __name__ == "__main__":
    main()
