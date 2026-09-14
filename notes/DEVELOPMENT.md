# Acquisition calibration

The 12 planned development fits completed without a recipe change. Seeds
90–91, independent fields only, 1,200 Adam updates at learning rate .02.
Evidence: `analysis/development/` and `analysis/development.log`.

Expected-objective rank 4 and 8 fits all reached development expected MSE
below 6e-15, versus zero-prediction MSE near one. Rank 2 stayed near .5 as
predicted by insufficient capacity; it is preserved as a capacity diagnostic,
not used as evidence of failed optimization. Broad rank 8 reconstruction also
acquired all fields. No failed acquisition run was excluded or overwritten.

Rank 8 expected-only fits had ordinary changed MSE .915 and .948, yet the
privileged frozen-state readers recovered changed fields at MSE below 2e-13.
Rank 4 changed MSE stayed near one even with the fitted reader, consistent
with the analytic Gaussian conditional variance. These observations motivate
the primary capacity × reader contrast to be tested on fresh seeds/history.
They are development observations, not confirmatory results.

The sequential SGD and algebraic training shortcut agree in output exactly
and in outer gradient within 4.55e-13 in float64. Independent autograd checks
the inner update and overwrite semantics. These mechanics alone were not
treated as acquisition evidence; the above task results are the acquisition
check. Full checks are in `analysis/preflight.json`.
