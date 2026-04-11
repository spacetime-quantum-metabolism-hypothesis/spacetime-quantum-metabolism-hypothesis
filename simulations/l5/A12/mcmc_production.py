# -*- coding: utf-8 -*-
"""L5-B A12 production MCMC (error-function diffusion drift)."""
from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_L5 = os.path.dirname(_HERE)
if _L5 not in sys.path:
    sys.path.insert(0, _L5)

from _alt_production import run_alt  # noqa: E402


if __name__ == '__main__':
    run_alt('A12', _HERE)
