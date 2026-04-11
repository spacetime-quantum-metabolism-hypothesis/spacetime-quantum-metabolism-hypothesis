# arXiv Submission Checklist — SQMH Paper v1

**Target**: arXiv astro-ph.CO (primary), gr-qc (cross-listing).
**Title**: *Matter-Locked Dark-Energy Drift and the DESI DR2 w₀–wₐ
Signal: Twenty Zero-Parameter Candidates from the Spacetime Quantum
Metabolism Hypothesis*

## Pre-submission checklist

### Content

- [ ] Abstract ≤ 250 words, states:
  - DESI DR2 (w₀, wₐ) signal
  - SQMH L0/L1 axioms
  - Zero-parameter alt-20 family finding
  - Δχ² ≈ −21 joint (BAO+SN+CMB+RSD)
  - DESI DR3 forecast conclusions
  - Number of Phase-5 main candidates
- [ ] Introduction cites DESI 2503.14738, Planck 2018, DES-Y5 SN,
  Abbott DES-Y3 cosmic shear, Asgari KiDS-1000
- [ ] Methods section reproducible from repo alone (no proprietary
  codes)
- [ ] All figures produced by `simulations/l5/*/` scripts
- [ ] All numerical claims traced to a JSON result file
- [ ] Limitations section (§8) honestly states:
  - μ(a,k) = 1 structural constraint — S₈ tension not resolved
  - H₀ tension not resolved
  - DR3 will NOT distinguish C28 from alt-class (0.19 σ)
  - Alt-20 drift degeneracy: n_eff = 1, one drift direction
  - SQMH L0/L1 origin of amplitude-locking is a *postulate*, not a
    derived consequence of a UV-complete theory
- [ ] Negative results declared: eliminated candidates listed with
  reasons (C11D K3, C26 ansatz failure or success, C33 S₈ concerns)

### Figures

- [ ] `paper/figures/l5_C28_corner.png` — C28 production MCMC corner
- [ ] `paper/figures/l5_C33_corner.png` — C33 production MCMC corner
- [ ] `paper/figures/l5_A01_corner.png` — A01 2-D corner
- [ ] `paper/figures/l5_A05_corner.png`
- [ ] `paper/figures/l5_A12_corner.png`
- [ ] `paper/figures/l5_A17_corner.png`
- [ ] `paper/figures/l5_alt_class_svd.png` — SVD spectrum + modes
- [ ] `paper/figures/l5_dr3_forecast.png` — DR3 Fisher ellipses
- [ ] `paper/figures/l5_w_of_z.png` — w(z) curves for Phase-5 winners
- [ ] Each figure has a self-contained caption in the main text
- [ ] DPI ≥ 150, PNG or PDF vector

### References

- [ ] `paper/references.bib` BibTeX verified; every \cite resolves
- [ ] Key refs:
  - DESI Coll. 2024 (DR2 BAO, 2503.14738)
  - DESI Coll. 2024 (DR2 cosmological implications)
  - Planck Coll. 2020 (compressed CMB)
  - DES Coll. 2024 (DESY5 SN)
  - Abbott et al. 2022 (DES-Y3 cosmic shear)
  - Asgari et al. 2021 (KiDS-1000)
  - Maggiore & Mancarella 2014 (RR non-local)
  - Dirian et al. 2015 (RR localised)
  - Frusciante 2021 (f(Q) teleparallel)
  - Zumalacárregui-Koivisto-Bellini 2013 (disformal)
  - Foreman-Mackey et al. 2013 (emcee)
  - Speagle 2020 (dynesty)
  - Jeffreys 1961 / Trotta 2008 (Bayes factor scale)

### Reproducibility

- [ ] `README.md` has one-command reproduction: `python -m simulations.l5.runner_all`
- [ ] All constants in `simulations/config.py` (zero free params at
  the paper level)
- [ ] SHA-256 hashes of data files recorded in
  `simulations/l5/<ID>/review.md`
- [ ] emcee `np.random.seed(42)` inside sampler (reproducibility rule)
- [ ] Environment: Python ≥ 3.11, numpy ≥ 2.0, scipy, emcee, dynesty,
  corner, matplotlib — pinned in `requirements.txt`

### Format

- [ ] Markdown → LaTeX via pandoc (`scripts/build_paper.sh`)
- [ ] PDF build test: `tectonic paper.tex` produces PDF
- [ ] Abstract encoded as plain text (no LaTeX markup)
- [ ] Author block: `${AUTHOR_NAME}, ${AFFILIATION}` — placeholder
  until user fills in
- [ ] arXiv category: astro-ph.CO; cross: gr-qc
- [ ] MSC / PACS optional

### Source upload

- [ ] `paper/paper.tex` main LaTeX source
- [ ] `paper/figures/*.png` (or `.pdf`)
- [ ] `paper/references.bib`
- [ ] `paper/appendix_A_alt20.tex` included
- [ ] zip: `paper/arxiv_submission_YYYYMMDD.zip`

### Post-submission

- [ ] arXiv endorsement (if required for first-time astro-ph.CO author)
- [ ] Announce on relevant mailing lists or social media
- [ ] Update `base.l5.result.md` with arXiv ID once assigned
- [ ] Prepare referee response template for journal submission
  (Phys. Rev. D or JCAP)

## Open issues before upload

- [ ] Author name and affiliation — **user must supply**
- [ ] Acknowledgements section — **user must supply**
- [ ] Funding disclosure — **user must supply**
- [ ] Data availability statement — repository URL pending
  (GitHub mirror planned)
- [ ] Conflict of interest — none declared

## Do NOT submit until

1. All Phase-5 main candidates have production MCMC with R̂ < 1.02
2. Bayesian evidence computed for all candidates vs LCDM
3. Cosmic shear S₈ check completed for all candidates
4. C11D and C26 re-evaluations closed (promote or KILL)
5. At least one candidate achieves Δ ln Z ≥ +2.5 (Q8)
6. Paper v1 passes a 4-person team code review
7. User has reviewed and approved the final abstract and conclusions
