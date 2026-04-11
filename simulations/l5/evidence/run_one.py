# -*- coding: utf-8 -*-
"""L5-C single-candidate evidence runner.

Usage: python run_one.py <ID>

Writes evidence_<ID>.json. Designed for parallel launch (one OS process
per candidate). OMP/MKL/OPENBLAS threads fixed to 1 per worker.
"""
from __future__ import annotations

import json
import os
import sys
import time
import traceback

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')

import numpy as np  # noqa: E402

np.seterr(all='ignore')

_THIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS)

from run_evidence import (  # noqa: E402
    CANDIDATES, nested_evidence, _jsonify, classify,
)


def main():
    if len(sys.argv) != 2:
        print("usage: run_one.py <ID>")
        sys.exit(2)
    target = sys.argv[1]
    rec = next((c for c in CANDIDATES if c[0] == target), None)
    if rec is None:
        print(f"unknown id: {target}")
        sys.exit(2)
    aid, name, builder, nlive, note = rec
    out = os.path.join(_THIS, f'evidence_{aid}.json')
    t0 = time.time()
    print(f"[{aid}] {name}  (nlive={nlive}, {note})", flush=True)
    try:
        ll, pt, ndim = builder()
        ev = nested_evidence(ll, pt, ndim, nlive=nlive, seed=42)
        ev['elapsed_sec'] = time.time() - t0
        ev['ndim'] = ndim
        ev['id'] = aid
        ev['name'] = name
        ev['note'] = note
        print(f"[{aid}] ln Z = {ev['logz']:+.3f} +/- {ev['logz_err']:.3f}"
              f"  niter={ev['niter']}  [{ev['elapsed_sec']:.1f}s]", flush=True)
        with open(out, 'w', encoding='utf-8') as f:
            json.dump(_jsonify(ev), f, indent=2)
    except Exception as e:
        dt = time.time() - t0
        err = {'id': aid, 'name': name, 'note': note,
               'error': str(e), 'trace': traceback.format_exc(),
               'elapsed_sec': dt}
        with open(out, 'w', encoding='utf-8') as f:
            json.dump(err, f, indent=2)
        print(f"[{aid}] FAILED after {dt:.1f}s: {e}", flush=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
