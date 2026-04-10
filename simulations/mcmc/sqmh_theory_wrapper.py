# -*- coding: utf-8 -*-
"""
sqmh_theory_wrapper.py

Cobaya theory class wrapping patched CLASS-SQMH (Phase 2).
STUB: finalize once CLASS patch is in place.
"""
try:
    from cobaya.theories.classy import classy as _classy_base
except ImportError:
    _classy_base = object  # allows file to parse without cobaya installed


class SQMHClassy(_classy_base):
    """
    Extends Cobaya's classy theory to pass SQMH-specific parameters.

    Required in YAML:
      theory:
        sqmh_theory_wrapper.SQMHClassy:
          extra_args:
            SQMH_enabled: 1
            SQMH_V_family: RP
    """

    _sqmh_params = ['SQMH_xi', 'SQMH_V_param_n', 'SQMH_V_param_lambda']

    def must_provide(self, **requirements):
        return super().must_provide(**requirements)

    def calculate(self, state, want_derived=True, **params_values_dict):
        # Pull SQMH params from sample
        sqmh_kwargs = {}
        for p in self._sqmh_params:
            if p in params_values_dict:
                sqmh_kwargs[p] = params_values_dict[p]

        # Map to CLASS input keys (patched CLASS reads SQMH_V_params as array)
        if 'SQMH_V_param_n' in sqmh_kwargs:
            sqmh_kwargs['SQMH_V_params'] = [
                0.685,  # amplitude calibrated to Omega_DE_0
                sqmh_kwargs.pop('SQMH_V_param_n'),
            ]

        # Forward to classy base
        self.set(sqmh_kwargs)
        return super().calculate(state, want_derived=want_derived,
                                 **params_values_dict)
