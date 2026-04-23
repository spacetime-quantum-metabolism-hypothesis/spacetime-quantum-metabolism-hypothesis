# -*- coding: utf-8 -*-
"""Run l32_test.py N times and aggregate statistics."""
import os, sys, json, subprocess, statistics, time

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RUNNER = os.path.join(_SCRIPT_DIR, 'l32_test.py')
OUT_DIR = os.path.join(_SCRIPT_DIR, 'repeat_runs')
os.makedirs(OUT_DIR, exist_ok=True)

N_RUNS = 10

all_runs = []

for i in range(1, N_RUNS + 1):
    t0 = time.time()
    print(f'Run {i}/{N_RUNS} ...', flush=True)
    result = subprocess.run(
        [sys.executable, RUNNER],
        capture_output=True, text=True, timeout=600
    )
    elapsed = time.time() - t0
    print(f'  done in {elapsed:.1f}s', flush=True)

    json_path = os.path.join(_SCRIPT_DIR, 'l32_results.json')
    with open(json_path) as f:
        data = json.load(f)

    run_path = os.path.join(OUT_DIR, f'run_{i:02d}.json')
    with open(run_path, 'w') as f:
        json.dump(data, f, indent=2)
    all_runs.append(data)

# Aggregate
theory_ids = [t['id'] for t in all_runs[0]['theories']]

agg = {}
for tid in theory_ids:
    vals = {}
    for run in all_runs:
        for t in run['theories']:
            if t['id'] == tid:
                for key in ('chi2', 'aicc', 'd_aicc', 'w0', 'wa', 'Om', 'H0'):
                    vals.setdefault(key, []).append(t[key])
                vals.setdefault('status', []).append(t['status'])
                break
    agg[tid] = vals

# Summary table
print('\n' + '='*90)
print('L32 10-RUN AGGREGATE (mean +/- std)')
print('='*90)
print(f"{'ID':<6} {'chi2_mean':>10} {'chi2_std':>9} {'dAICc_mean':>11} {'wa_mean':>9} {'wa_std':>8} {'Q90_cnt':>8} {'K93_cnt':>8}")
print('-'*90)

rows = []
for tid in theory_ids:
    v = agg[tid]
    chi2_m = statistics.mean(v['chi2'])
    chi2_s = statistics.stdev(v['chi2']) if len(v['chi2']) > 1 else 0.0
    daicc_m = statistics.mean(v['d_aicc'])
    wa_m = statistics.mean(v['wa'])
    wa_s = statistics.stdev(v['wa']) if len(v['wa']) > 1 else 0.0
    q90 = sum(1 for s in v['status'] if s in ('Q90','Q91','Q92'))
    k93 = sum(1 for s in v['status'] if s == 'K93')
    rows.append((tid, chi2_m, chi2_s, daicc_m, wa_m, wa_s, q90, k93))

rows.sort(key=lambda x: x[3])
for r in rows:
    print(f"{r[0]:<6} {r[1]:>10.4f} {r[2]:>9.4f} {r[3]:>11.4f} {r[4]:>9.4f} {r[5]:>8.4f} {r[6]:>8d} {r[7]:>8d}")

print('='*90)

# Overall pass counts across all runs
pass_total = sum(run['pass_count'] for run in all_runs)
q91_total = sum(run['q91'] for run in all_runs)
q92_total = sum(run['q92'] for run in all_runs)
k93_total = sum(
    sum(1 for t in run['theories'] if t['status'] == 'K93')
    for run in all_runs
)

print(f'\nOver {N_RUNS} runs (300 theory-trials total):')
print(f'  Q90 PASS  : {pass_total} / 300 ({pass_total/300*100:.1f}%)')
print(f'  Q91 STRONG: {q91_total} / 300')
print(f'  Q92 GAME  : {q92_total} / 300')
print(f'  K93 KILL  : {k93_total} / 300')

# Save aggregate
agg_out = {
    'n_runs': N_RUNS,
    'theories': []
}
for r in rows:
    tid = r[0]
    v = agg[tid]
    agg_out['theories'].append({
        'id': tid,
        'chi2_mean': r[1], 'chi2_std': r[2],
        'd_aicc_mean': r[3],
        'wa_mean': r[4], 'wa_std': r[5],
        'q90_count': r[6], 'k93_count': r[7]
    })

agg_path = os.path.join(_SCRIPT_DIR, 'l32_repeat_agg.json')
with open(agg_path, 'w') as f:
    json.dump(agg_out, f, indent=2)
print(f'\nAggregate saved: {agg_path}')
