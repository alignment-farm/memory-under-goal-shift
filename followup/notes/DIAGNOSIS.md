# Bounded acquisition diagnosis, before additional fits

The eight initial development fits completed. Both four-slot expected fits
acquire both parities (<1e-12 MSE); both broad fits acquire raw fields (<1e-8).
Two-slot expected fits fail (.50 and .44 expected MSE), despite sufficient
representational capacity: two explicit parity bits achieve zero error.
Exhaustive readers leave .50 and .4167 expected MSE respectively, locating
much of this failure in the learned encoding, rather than only its reader.

Before evaluation, diagnose two-slot optimization using the same development
seeds only. For each seed: fit an ordinary decoder on a supplied exact parity
encoder (1,000 steps); separately fit the learned encoder directly to supplied
parity codes (1,000 steps), then fit its decoder (1,000 steps). These are
privileged factorization diagnostics, not main contenders: they disclose the
desired intermediate representation. At most six optimizer phases, inside the
16-development-fit envelope. Keep the original joint-training recipe for final
comparison, and retain two-slot failures. Four slots already provide a
functioning nonlinear memory in which both selection and reader failure can
be measured. No obligation to tune the two-slot system indefinitely.
