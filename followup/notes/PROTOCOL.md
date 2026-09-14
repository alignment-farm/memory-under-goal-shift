# Frozen evaluation protocol

14 September 2026, after eight development fits and six diagnostic optimizer
phases, before evaluation. Use the unchanged `scripts/experiment.py` recipe
described in DESIGN.md: 2,000 steps, Adam .01, 128 independent uniform records
per step, two objectives, two capacities, seeds 0–4. No selection of successful
seeds, early stopping, hyperparameter search or retraining after evaluation.

Each seed uses 4,096 fresh eight-record histories (data seed 1700000+seed),
and 512 separate diagnostic-reader histories (1700100+seed). Training RNG
is 10000+seed; initialization seed is the model seed. Development seeds 90,91
and its data seeds are distinct. Shared support contains only 16 record types;
all are present in the training distribution. Generalization here means new
histories and training draws, not held-out record types. The exhaustive
population calculation is an analytic distribution diagnostic, not test data.

Primary comparison: expected vs broad at four slots, expected-task acquisition,
changed MSE for ordinary, empirical lookup and exhaustive optimal readers.
Population ordinary minus optimal MSE separates reader excess error from
irreducible uncertainty in a frozen code. Report each seed and ranges; five
seeds are descriptive, not a broad-population estimate. Fresh-history scores
check the population analysis. Two slots remain an acquisition/optimization
diagnostic and a capacity tradeoff, never silently dropped.

Development: four-slot expected parity error <1e-12 and broad raw error <1e-8
for both seeds. Two-slot joint expected learning failed (.50/.44); exhaustive
readers still failed (.50/.4167). Supplied exact parity codes allowed the same
decoder to acquire both parities (<1e-12); direct supervision of the learned
encoder also recovered exact parity codes for both seeds, followed by successful
reader fitting. Therefore two-slot failure does not establish insufficient
architecture or storage capacity. The factorization diagnosis used privileged
intermediate targets; it is not ordinary task performance.

All five explicit controls in DESIGN.md receive the same histories and lookup
budgets. Explicit parity, balanced and hybrid transforms encode known task
structure by hand; full raw storage is the competent four-slot reference.
The invertible nonlinear control tests the analysis, not learned performance.
Only episode payload is matched. Each float32 slot costs four implemented
bytes but carries one bit here. Shared neural parameters are 1,816 bytes
(r=2) or 2,336 (r=4), plus Adam moments during training. Decoder lookup tables
have 2^r×6 float64 values (192/768 bytes), with 2^r int64 fitting counts
(32/128 bytes). Neural temporary activations/logits and optimizer are discarded
at reading. A reader can query any key but sees no previous history.

Writing a learned record uses 128+32r dense multiply-accumulates, 32+r tanh
evaluations and r thresholds; the gradient write adds r subtractions and r
updates. Reading all fields uses 32r+128 multiply-accumulates, 32 tanh and
two products, plus bias additions. Explicit formulas need at most two products
to encode, and no learned parameters; lookup costs r bit tests and six indexed
outputs. Timings separately record write, ordinary read and empirical fitting.
Training counts and loop time include data generation and optimizer steps,
but exclude installation, reading, diagnostics and documentation. No teacher.

Retain all network weights, curves, code partitions, lookup tables, data/state
hashes and configurations in JSON. Verification must regenerate held-out data,
restore networks and recompute metrics, and independently enumerate conditional
means using NumPy. Git-freeze this protocol and code before the evaluation.
