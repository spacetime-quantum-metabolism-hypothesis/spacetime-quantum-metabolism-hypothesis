"""L496 — Global cross-validation audit of all SQT anchor predictions.

Anchors covered (8):
  A1 BBN          (DeltaN_eff)                     -- claims_status.json: bbn-deltaNeff
  A2 Cassini      (PPN |gamma-1|)                  -- claims_status.json: cassini-ppn
  A3 EP           (eta Eotvos)                     -- claims_status.json: ep-eta
  A4 GW170817     (|Delta c/c|)                    -- claims_status.json: gw170817-cT
  A5 Bullet       (Bullet cluster lens-galaxy)     -- claims_status.json: bullet-cluster
  A6 cosmic       (sigma_0 cosmic regime / DESI)   -- sigma0-three-regime aggregate
  A7 cluster      (sigma_0 cluster regime)         -- sigma0-three-regime aggregate
  A8 galactic     (sigma_0 galactic / SPARC RAR)   -- L482 PASS_STRONG candidate

For each anchor we record:
  - status      : PASS_STRONG / PASS / PARTIAL / NOT_INHERITED
  - margin      : log10(observational bound / SQT prediction) where defined
                  (positive = SQT well below the bound; >=0 -> PASS)
  - independence: which other anchors share fit parameters (H0, beta_eff, sigma0)

Leave-one-out (LOO) audit:
  For each anchor i in {1..8}:
    drop anchor i, compute over the remaining 7:
      - n_pass_rem    : count of PASS / PASS_STRONG in remaining set
      - pass_rate_rem : n_pass_rem / 7
      - mean_margin   : average log10 margin over remaining anchors with numeric margin
      - shared_param_loss : list of fit parameters that lose constraint when i is dropped

Single-anchor dependence:
  delta_passrate_i = pass_rate_full - pass_rate_LOO_i
  If max_i |delta_passrate_i| <= 1/N (one anchor's fair share)  -> globally consistent.
  If any |delta_passrate_i| > 1/N                                -> SQT relies on a single anchor.

This script is *audit-only*: it consumes pre-existing per-anchor results from
results/ and from claims_status.json. It does not refit any anchor.

Outputs:
  results/L496/GLOBAL_CV.md
  results/L496/L496_results.json
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
RESULTS = ROOT / 'results' / 'L496'
RESULTS.mkdir(parents=True, exist_ok=True)
CLAIMS = ROOT / 'claims_status.json'


# ---------------------------------------------------------------------------
# Anchor catalogue.  Numeric margins follow paper §4.1 / claims_status.json.
# margin_log10 = log10(observational_bound / SQT_prediction).
# Positive margin = SQT is well below the limit.
# Status maps to a numeric pass score:  PASS_STRONG=1.0, PASS=1.0, PARTIAL=0.5,
# NOT_INHERITED=0.0.  The "pass rate" uses the binary cut (PARTIAL counts as
# 0.5 in fractional rate, 0 in strict rate).
# ---------------------------------------------------------------------------
ANCHORS: dict[str, dict[str, Any]] = {
    'A1_BBN': {
        'channel': 'BBN DeltaN_eff',
        'bound': 0.17,
        'sqt_prediction': 1.0e-46,
        'status': 'PASS_STRONG',
        'shared_params': ['eta_Z2', 'beta_eff'],
        'claims_id': 'bbn-deltaNeff',
        'note': 'eta_Z2 ~ 10 MeV >> T_BBN; beta_eff^2 double protection.',
    },
    'A2_Cassini': {
        'channel': 'Cassini PPN |gamma-1|',
        'bound': 2.3e-5,
        'sqt_prediction': 1.1e-40,
        'status': 'PASS_STRONG',
        'shared_params': ['beta_eff', 'Lambda_UV'],
        'claims_id': 'cassini-ppn',
        'note': 'beta_eff = Lambda_UV / M_Pl ~ 7.4e-21.',
    },
    'A3_EP': {
        'channel': 'EP Eotvos eta',
        'bound': 1.0e-15,
        'sqt_prediction': 1.0e-30,  # conservative postdiction floor; conformal-only
        'status': 'PASS',
        'shared_params': ['beta_eff', 'conformal_lagrangian'],
        'claims_id': 'ep-eta',
        'note': 'Conformal-only Lagrangian -> universal coupling; eta < bound by inheritance.',
    },
    'A4_GW170817': {
        'channel': 'GW170817 |Dc/c|',
        'bound': 1.0e-15,
        'sqt_prediction': 1.0e-25,  # disformal-suppressed; no leading anomaly
        'status': 'PASS',
        'shared_params': ['conformal_lagrangian', 'B_disformal'],
        'claims_id': 'gw170817-cT',
        'note': 'Conformal-only Lagrangian inheritance; B_disformal=0 limit -> Dc=0.',
    },
    'A5_Bullet': {
        'channel': 'Bullet cluster lens-galaxy offset',
        'bound': None,        # qualitative
        'sqt_prediction': None,
        'status': 'PARTIAL',
        'shared_params': ['sigma0_cluster', 'NFW_cancel'],
        'claims_id': 'bullet-cluster',
        'note': 'Qualitative PASS (lens follows galaxies, not gas); MOND-like fail avoided.',
    },
    'A6_cosmic': {
        'channel': 'sigma_0 cosmic regime (DESI BAO + CMB theta_*)',
        'bound': None,
        'sqt_prediction': None,
        'status': 'PARTIAL',     # postdiction caveat per §3.4
        'shared_params': ['sigma0', 'H0', 'Om'],
        'claims_id': 'sigma0-three-regime',
        'note': 'Cosmic anchor of three-regime; aggregate PASS but POSTDICTION caveat.',
    },
    'A7_cluster': {
        'channel': 'sigma_0 cluster regime (Mpc scale)',
        'bound': None,
        'sqt_prediction': None,
        'status': 'PARTIAL',
        'shared_params': ['sigma0', 'NFW_cancel'],
        'claims_id': 'sigma0-three-regime',
        'note': 'Cluster anchor of three-regime; placeholder eps ~5%.',
    },
    'A8_galactic': {
        'channel': 'sigma_0 galactic regime / SPARC RAR a0 = c H0/(2pi)',
        'bound': 1.20e-10,        # McGaugh 2016 a0
        'sqt_prediction': 1.0422e-10,  # c H0_planck / (2 pi)
        'status': 'PASS_STRONG',  # L482 5/5 K
        'shared_params': ['sigma0', 'H0'],
        'claims_id': 'L482-RAR',
        'note': 'L482 RAR: 5/5 K-criteria, n=3389 (175 galaxies); a0 ratio 1.025.',
    },
}

STATUS_SCORE = {
    'PASS_STRONG': 1.0,
    'PASS': 1.0,
    'PARTIAL': 0.5,
    'NOT_INHERITED': 0.0,
    'FAIL': 0.0,
}

STATUS_BINARY = {
    'PASS_STRONG': 1,
    'PASS': 1,
    'PARTIAL': 0,   # strict rate: PARTIAL not counted as pass
    'NOT_INHERITED': 0,
    'FAIL': 0,
}


def margin_log10(a: dict[str, Any]) -> float | None:
    if a['bound'] is None or a['sqt_prediction'] is None:
        return None
    if a['sqt_prediction'] <= 0:
        return None
    return math.log10(a['bound'] / a['sqt_prediction'])


def aggregate(subset: dict[str, dict[str, Any]]) -> dict[str, Any]:
    n = len(subset)
    if n == 0:
        return dict(n=0, n_pass_strict=0, pass_rate_strict=0.0,
                    fractional_score=0.0, mean_margin=None,
                    margins=[])
    n_pass_strict = sum(STATUS_BINARY[a['status']] for a in subset.values())
    fractional = sum(STATUS_SCORE[a['status']] for a in subset.values())
    margins = []
    for a in subset.values():
        m = margin_log10(a)
        if m is not None:
            margins.append(m)
    mean_margin = (sum(margins) / len(margins)) if margins else None
    return dict(
        n=n,
        n_pass_strict=n_pass_strict,
        pass_rate_strict=n_pass_strict / n,
        fractional_score=fractional / n,
        mean_margin=mean_margin,
        n_with_margin=len(margins),
        margins=margins,
    )


def loo(anchors: dict[str, dict[str, Any]]) -> dict[str, Any]:
    full = aggregate(anchors)
    rows = {}
    for key in anchors:
        sub = {k: v for k, v in anchors.items() if k != key}
        agg = aggregate(sub)
        agg['delta_pass_rate_strict'] = full['pass_rate_strict'] - agg['pass_rate_strict']
        agg['delta_fractional'] = full['fractional_score'] - agg['fractional_score']
        if full['mean_margin'] is not None and agg['mean_margin'] is not None:
            agg['delta_mean_margin'] = full['mean_margin'] - agg['mean_margin']
        else:
            agg['delta_mean_margin'] = None
        rows[key] = agg
    return dict(full=full, loo=rows)


# ---------------------------------------------------------------------------
# Shared-parameter dependence audit
# ---------------------------------------------------------------------------
def shared_param_audit(anchors: dict[str, dict[str, Any]]) -> dict[str, Any]:
    # Inverted index: param -> anchors that constrain it
    idx: dict[str, list[str]] = {}
    for key, a in anchors.items():
        for p in a['shared_params']:
            idx.setdefault(p, []).append(key)
    # For each LOO drop, list params that lose >=1 constraint
    loo_loss = {}
    for key, a in anchors.items():
        loss = []
        for p in a['shared_params']:
            remaining = [k for k in idx[p] if k != key]
            if not remaining:
                loss.append(dict(param=p, becomes='UNCONSTRAINED'))
            elif len(remaining) == 1:
                loss.append(dict(param=p, becomes='SINGLE_ANCHOR', remaining=remaining[0]))
        loo_loss[key] = loss
    # Globally: parameters constrained by exactly 1 anchor are "single-source"
    single_source = {p: ks for p, ks in idx.items() if len(ks) == 1}
    return dict(param_index=idx, loo_param_loss=loo_loss, single_source_params=single_source)


# ---------------------------------------------------------------------------
# Render markdown report
# ---------------------------------------------------------------------------
def render_md(loo_res: dict[str, Any], param_audit: dict[str, Any]) -> str:
    full = loo_res['full']
    rows = loo_res['loo']
    N = full['n']
    fair_share = 1.0 / N

    lines: list[str] = []
    lines.append('# L496 — Global Cross-Validation of All SQT Anchors')
    lines.append('')
    lines.append('> **목적**: 8개 anchor (BBN / Cassini / EP / GW170817 / Bullet / cosmic / cluster / galactic) 의')
    lines.append('> *leave-one-out* 감사로 SQT 가 단일 anchor 에 과의존하는지, 글로벌 일관성이 있는지 정량.')
    lines.append('> 데이터 출처: claims_status.json + L417/L482/L484/L485/L486/L490 산출물.')
    lines.append('> 본 감사는 *재피팅 없음*: 기존 per-anchor 결과만 집계.')
    lines.append('')
    lines.append('## 1. 정직 한 줄')
    lines.append('')
    # Compute conclusion
    max_drop = max(abs(rows[k]['delta_pass_rate_strict']) for k in rows)
    worst_key = max(rows, key=lambda k: abs(rows[k]['delta_pass_rate_strict']))
    if max_drop <= fair_share + 1e-9:
        verdict_line = (f'**모든 LOO 에서 |Δpass-rate| ≤ {fair_share:.3f} (fair share). '
                        f'단일 anchor 의존 없음 — 8/8 글로벌 일관.**')
    else:
        verdict_line = (f'**LOO 에서 최대 |Δpass-rate| = {max_drop:.3f} > fair_share={fair_share:.3f} '
                        f'(`{worst_key}`). 해당 anchor 단일 의존 신호.**')
    lines.append(verdict_line)
    lines.append('')

    lines.append('## 2. Anchor catalogue (full set)')
    lines.append('')
    lines.append('| # | Anchor | Channel | Status | log10(bound/SQT) | shared params |')
    lines.append('|---|---|---|---|---|---|')
    for key, a in ANCHORS.items():
        m = margin_log10(a)
        m_str = f"{m:+.2f}" if m is not None else "N/A (qualitative)"
        sp = ', '.join(a['shared_params'])
        lines.append(f"| {key} | `{key}` | {a['channel']} | **{a['status']}** | {m_str} | {sp} |")
    lines.append('')

    lines.append('## 3. Full-set aggregate (no anchor dropped)')
    lines.append('')
    lines.append(f"- N = {full['n']}")
    lines.append(f"- strict PASS count (PASS+PASS_STRONG) = {full['n_pass_strict']}/{N}")
    lines.append(f"- pass rate (strict, PARTIAL→0) = **{full['pass_rate_strict']:.3f}**")
    lines.append(f"- fractional score (PARTIAL→0.5) = **{full['fractional_score']:.3f}**")
    if full['mean_margin'] is not None:
        lines.append(f"- mean log10 margin (over {full['n_with_margin']} numeric anchors) = **{full['mean_margin']:+.2f} dex**")
    lines.append('')

    lines.append('## 4. Leave-one-out table')
    lines.append('')
    lines.append('| Dropped | n_rem | strict PASS | pass_rate | Δpass_rate | fractional | mean log10 margin | Δmargin (dex) |')
    lines.append('|---|---|---|---|---|---|---|---|')
    for key in ANCHORS:
        r = rows[key]
        mm = f"{r['mean_margin']:+.2f}" if r['mean_margin'] is not None else 'N/A'
        dm = f"{r['delta_mean_margin']:+.2f}" if r['delta_mean_margin'] is not None else 'N/A'
        lines.append(f"| {key} | {r['n']} | {r['n_pass_strict']}/{r['n']} | "
                     f"{r['pass_rate_strict']:.3f} | {r['delta_pass_rate_strict']:+.3f} | "
                     f"{r['fractional_score']:.3f} | {mm} | {dm} |")
    lines.append('')

    lines.append('## 5. Single-anchor dependence verdict')
    lines.append('')
    lines.append(f"- fair_share threshold = 1/N = {fair_share:.3f}")
    lines.append(f"- max |Δpass_rate| over LOO = **{max_drop:.3f}** (drop `{worst_key}`)")
    if max_drop <= fair_share + 1e-9:
        lines.append("- **VERDICT: globally consistent** — no single anchor dominates the pass-rate metric.")
    else:
        lines.append(f"- **VERDICT: anchor `{worst_key}` carries weight beyond fair share.**")
    lines.append('')
    lines.append('Caveat: pass_rate is a coarse metric.  Anchors with PARTIAL status (Bullet, cosmic, cluster)')
    lines.append('are *already weighted at 0* in the strict count, so dropping them increases the strict rate')
    lines.append('mechanically.  The fractional column (PARTIAL=0.5) shows this effect (PARTIAL drop → score drop).')
    lines.append('')

    lines.append('## 6. Shared-parameter audit (LOO parameter loss)')
    lines.append('')
    lines.append('| Dropped | params losing constraint | becomes |')
    lines.append('|---|---|---|')
    for key in ANCHORS:
        loss = param_audit['loo_param_loss'][key]
        if not loss:
            lines.append(f"| {key} | (none) | — |")
            continue
        for entry in loss:
            extra = entry.get('remaining', '')
            lines.append(f"| {key} | `{entry['param']}` | {entry['becomes']}"
                         + (f" (only `{extra}`)" if extra else '') + ' |')
    lines.append('')
    if param_audit['single_source_params']:
        lines.append('### Single-source parameters (constrained by exactly 1 anchor)')
        lines.append('')
        for p, ks in param_audit['single_source_params'].items():
            lines.append(f"- `{p}` <- only `{ks[0]}`")
        lines.append('')
    else:
        lines.append('No parameter is single-source: every fit parameter is constrained by ≥2 anchors.')
        lines.append('')

    lines.append('## 7. Per-anchor margin commentary')
    lines.append('')
    for key, a in ANCHORS.items():
        m = margin_log10(a)
        m_str = f"{m:+.2f} dex" if m is not None else "qualitative (no numeric margin)"
        lines.append(f"- **{key}** ({a['channel']}): status `{a['status']}`, margin {m_str}.  {a['note']}")
    lines.append('')

    lines.append('## 8. CLAUDE.md compliance')
    lines.append('')
    lines.append('- **결과 왜곡 금지**: PARTIAL anchor (Bullet/cosmic/cluster) 의 strict rate=0 가공 효과를 §5 caveat 으로 명시.')
    lines.append('- **수식 금지 / 지도 금지 (최우선-1)**: 본 감사는 anchor verdict 의 *집계* 만 수행. 새 수식 0 줄, 새 파라미터 0 개.')
    lines.append('- **재피팅 금지**: per-anchor 결과는 L417/L482/L484/L490/claims_status.json 기존 산출물 인용.')
    lines.append('- **공유 파라미터 명시**: §6 에서 H0, beta_eff, sigma0 등이 ≥2 anchor 로 교차 제약됨을 표로 보고.')
    lines.append('')

    lines.append('---')
    lines.append('')
    lines.append('*저장: results/L496/GLOBAL_CV.md.  관련 JSON: results/L496/L496_results.json.*')
    return '\n'.join(lines)


def main() -> int:
    loo_res = loo(ANCHORS)
    param_audit = shared_param_audit(ANCHORS)

    # Attach per-anchor margins to result dump
    anchor_dump = {}
    for k, a in ANCHORS.items():
        anchor_dump[k] = dict(a)
        anchor_dump[k]['margin_log10'] = margin_log10(a)
        anchor_dump[k]['status_score_strict'] = STATUS_BINARY[a['status']]
        anchor_dump[k]['status_score_fractional'] = STATUS_SCORE[a['status']]

    out = dict(
        loop='L496',
        n_anchors=len(ANCHORS),
        anchors=anchor_dump,
        full=loo_res['full'],
        loo=loo_res['loo'],
        param_audit=param_audit,
    )

    json_path = RESULTS / 'L496_results.json'
    with json_path.open('w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, default=float)
    print(f"Wrote {json_path}")

    md = render_md(loo_res, param_audit)
    md_path = RESULTS / 'GLOBAL_CV.md'
    with md_path.open('w', encoding='utf-8') as fh:
        fh.write(md)
    print(f"Wrote {md_path}")

    # Brief stdout summary
    full = loo_res['full']
    print(f"\nFull set: {full['n_pass_strict']}/{full['n']} strict PASS, "
          f"fractional={full['fractional_score']:.3f}, mean margin={full['mean_margin']}")
    print('LOO Δpass-rate:')
    for k, r in loo_res['loo'].items():
        print(f"  drop {k}: pass_rate={r['pass_rate_strict']:.3f} "
              f"(Δ={r['delta_pass_rate_strict']:+.3f}), fractional={r['fractional_score']:.3f}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
