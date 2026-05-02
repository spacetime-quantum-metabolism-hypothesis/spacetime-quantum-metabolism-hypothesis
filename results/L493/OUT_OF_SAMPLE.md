# L493 -- SPARC RAR out-of-sample test
Seed: 20260501   Train fraction: 0.7
Galaxies: total 175 = train 122 + test 53
Radial points: train 2236, test 1153

## SQT a-priori prediction (no data used)
a0_SQT = c H0_Planck / (2 pi) = 1.0422e-10 m s^-2

## Train-only fit
a0_train = 1.0938e-10 m s^-2  (log10 a0 = -9.9611 +/- 0.0080)
a0_train / a0_SQT = 1.050
chi2/dof (train, free-a0)  = 1.298
chi2/dof (train, SQT)      = 1.301
chi2/dof (train, Newton)   = 12.570

## Held-out test set (30 %, evaluation only)
| model | params | chi2 | chi2/dof | AICc |
|---|---|---|---|---|
| SQT-locked (a0 = c H0/2pi)   | 0 | 1478.83 | 1.283 | 1478.83 |
| Train-fit a0                 | 1 | 1484.93 | 1.288 | 1486.93 |
| Newton-only (g_obs = g_bar)  | 0 | 17453.13 | 15.137 | 17453.13 |
| McGaugh PRL a0 = 1.20e-10    | 0 | 1517.05 | 1.316 | 1517.05 |

## Train/test accuracy comparison
chi2/dof (train, train-a0)  = 1.298
chi2/dof (test, SQT-locked) = 1.283
|test - train| = 0.016

## K-criteria
- K_OOS1 chi2/dof_test_SQT <= 1.5             : True
- K_OOS2 |test - train chi2/dof| <= 0.30      : True
- K_OOS3 AICc(SQT)-AICc(train) <= 2           : True
- K_OOS4 AICc(SQT)-AICc(Newton) <= -10        : True
- K_OOS5 a0_train within 30 % of a0_SQT       : True
- n_pass = 5/5

## dAICc (test set)
dAICc(SQT - trained-a0)  = -8.10
dAICc(SQT - Newton)      = -15974.30
dAICc(SQT - McGaugh PRL) = -38.22

## Honest one-line
SQT a0 = c H0 / 2pi predicts the held-out 30 % SPARC RAR with no fitting; out-of-sample accuracy matches train, consistent with the 0-free-parameter claim.
