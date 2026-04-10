"""Run all simulations with Agg backend (headless, no GUI)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import os

# Ensure utf-8 output
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Add simulations dir to path
sys.path.insert(0, os.path.dirname(__file__))

def run_safe(name, func):
    print(f"\n{'='*60}")
    print(f"Running: {name}")
    print('='*60)
    try:
        func()
        plt.close('all')
        print(f"[OK] {name}")
    except Exception as e:
        print(f"[FAIL] {name}: {e}")
        import traceback
        traceback.print_exc()

# Patch plt.show to no-op
plt.show = lambda *a, **kw: None

# 1. Metabolism equation (figures 01, 02, 03)
import metabolism_equation
run_safe("01_metabolism_steady_state", metabolism_equation.plot_steady_state)
run_safe("02_metabolism_1d_convergence", metabolism_equation.plot_convergence)
run_safe("03_three_regimes", metabolism_equation.plot_three_regimes)

# 2. Gravity derivation (figures 04, 05)
import gravity_derivation
run_safe("04_gravity_derivation", gravity_derivation.plot_gravity_matching)
run_safe("05_gravity_vector_field", gravity_derivation.plot_force_field_2d)

# 3. Dark energy w(z) (figure 06)
import dark_energy_w
run_safe("06_dark_energy_w", dark_energy_w.plot_w_z)

# 4. Cosmic three eras (figure 08)
import cosmic_three_eras
run_safe("08_cosmic_three_eras", cosmic_three_eras.plot_three_eras)

# 5. Quantum-classical transition (figures 09, 10)
import quantum_classical
run_safe("09_quantum_classical_transition", quantum_classical.plot_Q_mass_scan)
run_safe("10_Q_steepness", quantum_classical.plot_Q_steepness_comparison)

# 6. DESI DR2 fitting (figure 11)
import desi_fitting
run_safe("11_desi_dr2_fit", desi_fitting.plot_desi_fit)

# 7. DESI DR3 prediction (figure 12)
import desi_dr3_prediction
run_safe("12_desi_dr3_prediction", desi_dr3_prediction.plot_dr3_prediction)

print("\n" + "="*60)
print("ALL DONE")
print("="*60)
