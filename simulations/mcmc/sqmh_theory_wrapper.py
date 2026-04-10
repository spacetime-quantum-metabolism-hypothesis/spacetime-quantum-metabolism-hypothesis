# -*- coding: utf-8 -*-
"""
sqmh_theory_wrapper.py

Cobaya theory class wrapping patched CLASS-SQMH (Phase 3 entry point).

STATUS: STUB. Do NOT import from yaml until Phase 2 CLASS patch exposes the
SQMH_* input keys in classy's Python binding (simulations/class_patch/).

Why not the naive `self.set()` pattern?
  Cobaya's classy theory does NOT expose a `.set()` method on the theory
  instance. The underlying classy.Class() instance is held privately and is
  configured by Cobaya from (a) `extra_args` given in the yaml and (b) the
  `params_values_dict` sampled each step. Overriding `.set()` therefore
  crashes at runtime.

Correct pattern (Cobaya >= 3.3): override `calculate()` to mutate
`self.extra_args` before delegating to super. Cobaya reads `self.extra_args`
and passes the union of (extra_args, sampled params) into classy.Class.set()
on every evaluation. SQMH_* must be declared as valid input keys in the
patched CLASS `input_read_parameters()` (class_patch/README.md step 2).
"""
try:
    from cobaya.theories.classy import classy as _classy_base
except ImportError:
    _classy_base = object  # allows file to parse without cobaya installed


# Canonical V_family strings — must match patch_template.py / quintessence.py.
_V_FAMILIES = {"mass", "RP", "exp"}


class SQMHClassy(_classy_base):
    """
    Extends Cobaya's classy theory to pass SQMH-specific parameters.

    YAML usage (Phase 3):
      theory:
        sqmh_theory_wrapper.SQMHClassy:
          extra_args:
            SQMH_enabled: 1
            SQMH_V_family: RP   # canonical string
      params:
        SQMH_xi:            {prior: {min: 0.0, max: 1.0}, ...}
        SQMH_V_param_n:     {prior: {min: 0.01, max: 5.0}, ...}   # RP slope
    """

    # Parameters sampled by MCMC that must be forwarded to CLASS on each step.
    _sqmh_sampled_params = (
        'SQMH_xi',
        'SQMH_V_param_n',        # Ratra-Peebles slope
        'SQMH_V_param_lambda',   # exponential slope (if V_family == 'exp')
    )

    def initialize(self):
        super().initialize()
        fam = self.extra_args.get('SQMH_V_family', 'RP')
        if fam not in _V_FAMILIES:
            raise ValueError(
                f"SQMH_V_family must be one of {_V_FAMILIES}, got {fam!r}")

    def calculate(self, state, want_derived=True, **params_values_dict):
        # Extract SQMH sampled params; keep them out of the kwargs classy
        # would otherwise reject.
        sqmh_here = {}
        for p in self._sqmh_sampled_params:
            if p in params_values_dict:
                sqmh_here[p] = params_values_dict.pop(p)

        # Pack V-shape params into the array CLASS expects.
        fam = self.extra_args.get('SQMH_V_family', 'RP')
        if fam == 'RP' and 'SQMH_V_param_n' in sqmh_here:
            self.extra_args['SQMH_V_params'] = [
                0.685,  # amplitude calibrated to Omega_DE_0 at CLASS init
                sqmh_here['SQMH_V_param_n'],
            ]
        elif fam == 'exp' and 'SQMH_V_param_lambda' in sqmh_here:
            self.extra_args['SQMH_V_params'] = [
                0.685,
                sqmh_here['SQMH_V_param_lambda'],
            ]
        elif fam == 'mass':
            self.extra_args['SQMH_V_params'] = [1.37]  # 2*Omega_DE_0

        if 'SQMH_xi' in sqmh_here:
            self.extra_args['SQMH_xi'] = sqmh_here['SQMH_xi']

        return super().calculate(state, want_derived=want_derived,
                                 **params_values_dict)

    def get_can_provide_params(self):
        # Derived params the patched CLASS exports for analysis.
        base = list(super().get_can_provide_params())
        return base + ['w0_eff', 'wa_eff']
