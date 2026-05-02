"""L220 — Bianchi full ODE evolution of rho_q/rho_Lambda."""
import os; os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np, json
from scipy.integrate import odeint

# Toy: rho_q + rho_Lambda = constant (Bianchi balance)
# drho_q/dN = alpha (rho_Lambda - rho_q),  N=ln a
# Steady state: rho_q = rho_Lambda
def rhs(rho_q, N, alpha, rho_total):
    rho_L = rho_total - rho_q
    return alpha * (rho_L - rho_q)

rho_total = 2.0  # arbitrary
alpha = 3.0  # coupling rate
# z=1100 (early matter era) -> N = -ln(1101)
N_arr = np.linspace(-np.log(1101), 0, 200)
rho_q0 = 0.5 * rho_total  # symmetric init
sol = odeint(rhs, rho_q0, N_arr, args=(alpha, rho_total))
rho_q = sol[:,0]
rho_L = rho_total - rho_q
ratio = rho_q / rho_L
z_arr = np.exp(-N_arr) - 1
final_ratio = ratio[-1]
max_dev = np.max(np.abs(ratio - 1)) * 100  # %
print(f"Final ratio rho_q/rho_L = {final_ratio:.6f}")
print(f"Max deviation from 1    = {max_dev:.3f}%")
print(f"Within 10%/Hubble?      = {max_dev<10}")
out={'final_ratio':float(final_ratio),'max_dev_pct':float(max_dev),
     'within_10pct':bool(max_dev<10)}
with open(os.path.join(os.path.dirname(__file__),'report.json'),'w') as f:
    json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
