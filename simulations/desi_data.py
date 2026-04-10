"""
DESI DR2 Official BAO Data
Source: CobayaSampler/bao_data (github.com/CobayaSampler/bao_data)
Paper: arXiv:2503.14738 (DESI DR2 Results II, Table IV)

Data extracted from:
  desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt
  desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt
"""
import numpy as np

# === DESI DR2 BAO measurements (official, 13 data points) ===

# Measurement types: 'DV' = isotropic, 'DM' = transverse, 'DH' = radial
DESI_DR2 = {
    'tracers': [
        'BGS',
        'LRG1', 'LRG1',
        'LRG2', 'LRG2',
        'LRG3+ELG1', 'LRG3+ELG1',
        'ELG2', 'ELG2',
        'QSO', 'QSO',
        'Lya', 'Lya',
    ],
    'z_eff': np.array([
        0.295,
        0.510, 0.510,
        0.706, 0.706,
        0.934, 0.934,
        1.321, 1.321,
        1.484, 1.484,
        2.330, 2.330,
    ]),
    'quantity': [
        'DV_over_rs',
        'DM_over_rs', 'DH_over_rs',
        'DM_over_rs', 'DH_over_rs',
        'DM_over_rs', 'DH_over_rs',
        'DM_over_rs', 'DH_over_rs',
        'DM_over_rs', 'DH_over_rs',
        'DH_over_rs', 'DM_over_rs',
    ],
    'value': np.array([
        7.94167639,
        13.58758434, 21.86294686,
        17.35069094, 19.45534918,
        21.57563956, 17.64149464,
        27.60085612, 14.17602155,
        30.51190063, 12.81699964,
        8.631545674846294, 38.988973961958784,
    ]),
}

# Covariance matrix (13x13 block-diagonal)
# Diagonal blocks: BGS(1x1), LRG1(2x2), LRG2(2x2), LRG3+ELG1(2x2),
#                  ELG2(2x2), QSO(2x2), Lya(2x2)
DESI_DR2_COV = np.zeros((13, 13))

# BGS block (1x1)
DESI_DR2_COV[0, 0] = 5.79e-03

# LRG1 block (2x2)
DESI_DR2_COV[1, 1] = 2.83e-02
DESI_DR2_COV[1, 2] = -3.26e-02
DESI_DR2_COV[2, 1] = -3.26e-02
DESI_DR2_COV[2, 2] = 1.84e-01

# LRG2 block (2x2)
DESI_DR2_COV[3, 3] = 3.24e-02
DESI_DR2_COV[3, 4] = -2.37e-02
DESI_DR2_COV[4, 3] = -2.37e-02
DESI_DR2_COV[4, 4] = 1.11e-01

# LRG3+ELG1 block (2x2)
DESI_DR2_COV[5, 5] = 2.62e-02
DESI_DR2_COV[5, 6] = -1.13e-02
DESI_DR2_COV[6, 5] = -1.13e-02
DESI_DR2_COV[6, 6] = 4.04e-02

# ELG2 block (2x2)
DESI_DR2_COV[7, 7] = 1.05e-01
DESI_DR2_COV[7, 8] = -2.90e-02
DESI_DR2_COV[8, 7] = -2.90e-02
DESI_DR2_COV[8, 8] = 5.04e-02

# QSO block (2x2)
DESI_DR2_COV[9, 9] = 5.83e-01
DESI_DR2_COV[9, 10] = -1.95e-01
DESI_DR2_COV[10, 9] = -1.95e-01
DESI_DR2_COV[10, 10] = 2.68e-01

# Lya block (2x2)
DESI_DR2_COV[11, 11] = 1.02e-02
DESI_DR2_COV[11, 12] = -2.31e-02
DESI_DR2_COV[12, 11] = -2.31e-02
DESI_DR2_COV[12, 12] = 2.83e-01

# Diagonal uncertainties (for quick access)
DESI_DR2['sigma'] = np.sqrt(np.diag(DESI_DR2_COV))

# Inverse covariance for chi2 calculation
DESI_DR2_COV_INV = np.linalg.inv(DESI_DR2_COV)

# === Convenience: grouped by redshift bin ===
DESI_BINS = [
    {'tracer': 'BGS',         'z': 0.295, 'type': 'DV', 'DV': 7.94167639,  'DV_err': np.sqrt(5.79e-03)},
    {'tracer': 'LRG1',        'z': 0.510, 'type': 'DM_DH', 'DM': 13.58758434, 'DH': 21.86294686,
     'DM_err': np.sqrt(2.83e-02), 'DH_err': np.sqrt(1.84e-01), 'rho': -3.26e-02 / np.sqrt(2.83e-02 * 1.84e-01)},
    {'tracer': 'LRG2',        'z': 0.706, 'type': 'DM_DH', 'DM': 17.35069094, 'DH': 19.45534918,
     'DM_err': np.sqrt(3.24e-02), 'DH_err': np.sqrt(1.11e-01), 'rho': -2.37e-02 / np.sqrt(3.24e-02 * 1.11e-01)},
    {'tracer': 'LRG3+ELG1',   'z': 0.934, 'type': 'DM_DH', 'DM': 21.57563956, 'DH': 17.64149464,
     'DM_err': np.sqrt(2.62e-02), 'DH_err': np.sqrt(4.04e-02), 'rho': -1.13e-02 / np.sqrt(2.62e-02 * 4.04e-02)},
    {'tracer': 'ELG2',        'z': 1.321, 'type': 'DM_DH', 'DM': 27.60085612, 'DH': 14.17602155,
     'DM_err': np.sqrt(1.05e-01), 'DH_err': np.sqrt(5.04e-02), 'rho': -2.90e-02 / np.sqrt(1.05e-01 * 5.04e-02)},
    {'tracer': 'QSO',         'z': 1.484, 'type': 'DM_DH', 'DM': 30.51190063, 'DH': 12.81699964,
     'DM_err': np.sqrt(5.83e-01), 'DH_err': np.sqrt(2.68e-01), 'rho': -1.95e-01 / np.sqrt(5.83e-01 * 2.68e-01)},
    {'tracer': 'Lya',         'z': 2.330, 'type': 'DM_DH', 'DM': 38.98897396, 'DH': 8.63154567,
     'DM_err': np.sqrt(2.83e-01), 'DH_err': np.sqrt(1.02e-02), 'rho': -2.31e-02 / np.sqrt(1.02e-02 * 2.83e-01)},
]


def print_summary():
    print("DESI DR2 Official BAO Measurements")
    print("=" * 70)
    print(f"{'Tracer':<14} {'z_eff':>5} {'Type':>5} {'Value':>10} {'Sigma':>8}")
    print("-" * 70)
    for i in range(len(DESI_DR2['value'])):
        qtype = 'D_V' if 'DV' in DESI_DR2['quantity'][i] else ('D_M' if 'DM' in DESI_DR2['quantity'][i] else 'D_H')
        print(f"{DESI_DR2['tracers'][i]:<14} {DESI_DR2['z_eff'][i]:>5.3f} {qtype:>5} "
              f"{DESI_DR2['value'][i]:>10.4f} {DESI_DR2['sigma'][i]:>8.4f}")
    print(f"\nSource: arXiv:2503.14738 + github.com/CobayaSampler/bao_data")


if __name__ == "__main__":
    print_summary()
